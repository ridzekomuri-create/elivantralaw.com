import os
import secrets
from datetime import datetime, timedelta
from functools import wraps

from sqlalchemy import distinct, func

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.utils import secure_filename

from constants import ICONS
from models import Page, PageView, Review, Service, db

admin_bp = Blueprint("admin", __name__, url_prefix="/admin", template_folder="templates/admin")

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "static", "uploads")
ALLOWED_IMAGE_EXT = {"jpg", "jpeg", "png", "webp"}


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin.login", next=request.path))
        return view(*args, **kwargs)

    return wrapped


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password", "")
        expected = current_app.config.get("ADMIN_PASSWORD")
        if expected and secrets.compare_digest(password, expected):
            session["admin_logged_in"] = True
            session.permanent = True
            dest = request.args.get("next") or url_for("admin.dashboard")
            return redirect(dest)
        flash("Неверный пароль.", "error")
    return render_template("admin/login.html")


@admin_bp.route("/logout")
def logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("admin.login"))


@admin_bp.route("/stats")
@login_required
def stats():
    now = datetime.utcnow()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    base = PageView.query

    totals = {
        "today": base.filter(PageView.created_at >= today_start).count(),
        "week": base.filter(PageView.created_at >= now - timedelta(days=7)).count(),
        "month": base.filter(PageView.created_at >= now - timedelta(days=30)).count(),
        "all": base.count(),
    }
    unique_visitors = (
        db.session.query(func.count(distinct(PageView.visitor_id)))
        .filter(PageView.visitor_id.isnot(None))
        .scalar()
    )

    start_day = today_start - timedelta(days=13)
    rows = (
        db.session.query(func.date(PageView.created_at), func.count(PageView.id))
        .filter(PageView.created_at >= start_day)
        .group_by(func.date(PageView.created_at))
        .all()
    )
    by_day = {str(day): count for day, count in rows}
    series = []
    for i in range(14):
        day = (start_day + timedelta(days=i)).date().isoformat()
        series.append({"label": day[5:], "count": by_day.get(day, 0)})
    peak = max((d["count"] for d in series), default=0) or 1

    top_pages = (
        db.session.query(PageView.path, func.count(PageView.id).label("n"))
        .group_by(PageView.path)
        .order_by(func.count(PageView.id).desc())
        .limit(10)
        .all()
    )
    top_referrers = (
        db.session.query(PageView.referrer_host, func.count(PageView.id).label("n"))
        .filter(PageView.referrer_host.isnot(None))
        .group_by(PageView.referrer_host)
        .order_by(func.count(PageView.id).desc())
        .limit(10)
        .all()
    )
    devices = db.session.query(PageView.device, func.count(PageView.id)).group_by(PageView.device).all()

    return render_template(
        "admin/stats.html",
        totals=totals,
        unique_visitors=unique_visitors,
        series=series,
        peak=peak,
        top_pages=top_pages,
        top_referrers=top_referrers,
        devices=devices,
    )


@admin_bp.route("/")
@login_required
def dashboard():
    return render_template(
        "admin/dashboard.html",
        services_count=Service.query.count(),
        pages_count=Page.query.count(),
    )


# ---------------------------------------------------------------- services
@admin_bp.route("/services")
@login_required
def services_list():
    items = Service.query.order_by(Service.sort_order, Service.id).all()
    return render_template("admin/services_list.html", items=items)


@admin_bp.route("/services/new", methods=["GET", "POST"])
@login_required
def service_new():
    return _service_form(None)


@admin_bp.route("/services/<int:service_id>/edit", methods=["GET", "POST"])
@login_required
def service_edit(service_id):
    item = Service.query.get_or_404(service_id)
    return _service_form(item)


def _service_form(item):
    if request.method == "POST":
        f = request.form
        slug = f.get("slug", "").strip()

        # Fill in a working copy first so that if validation fails below, the
        # form can be redisplayed with everything the user typed — not blank.
        working = item or Service()
        working.slug = slug
        working.icon = f.get("icon") or "globe"
        try:
            working.sort_order = int(f.get("sort_order") or 0)
        except ValueError:
            working.sort_order = 0
        working.title = f.get("title", "").strip()
        working.title_en = f.get("title_en", "").strip()
        working.short = f.get("short", "").strip()
        working.short_en = f.get("short_en", "").strip()
        working.text = f.get("text", "").strip()
        working.text_en = f.get("text_en", "").strip()
        working.points_raw = f.get("points_raw", "").strip()
        working.points_en_raw = f.get("points_en_raw", "").strip()

        if not slug:
            flash("Slug (URL-имя) обязателен.", "error")
            return render_template("admin/service_form.html", item=working, icons=ICONS.keys())

        if item is None:
            db.session.add(working)
        db.session.commit()
        flash("Услуга сохранена.", "success")
        return redirect(url_for("admin.services_list"))

    return render_template("admin/service_form.html", item=item, icons=ICONS.keys())


@admin_bp.route("/services/<int:service_id>/delete", methods=["POST"])
@login_required
def service_delete(service_id):
    item = Service.query.get_or_404(service_id)
    db.session.delete(item)
    db.session.commit()
    flash("Услуга удалена.", "success")
    return redirect(url_for("admin.services_list"))


# ------------------------------------------------------------------ pages
@admin_bp.route("/pages")
@login_required
def pages_list():
    items = Page.query.order_by(Page.created_at.desc()).all()
    return render_template("admin/pages_list.html", items=items)


@admin_bp.route("/pages/new", methods=["GET", "POST"])
@login_required
def page_new():
    return _page_form(None)


@admin_bp.route("/pages/<int:page_id>/edit", methods=["GET", "POST"])
@login_required
def page_edit(page_id):
    item = Page.query.get_or_404(page_id)
    return _page_form(item)


def _page_form(item):
    if request.method == "POST":
        f = request.form
        slug = f.get("slug", "").strip()

        # Fill in a working copy first so that if validation fails below, the
        # form can be redisplayed with everything the user typed — not blank.
        working = item or Page()
        working.slug = slug
        working.published = bool(f.get("published"))
        working.title = f.get("title", "").strip()
        working.title_en = f.get("title_en", "").strip()
        working.excerpt = f.get("excerpt", "").strip()
        working.excerpt_en = f.get("excerpt_en", "").strip()
        working.content = f.get("content", "").strip()
        working.content_en = f.get("content_en", "").strip()

        if not slug:
            flash("Slug (URL-имя) обязателен.", "error")
            return render_template("admin/page_form.html", item=working)

        if item is None:
            db.session.add(working)

        upload = request.files.get("cover_image")
        if upload and upload.filename:
            ext = upload.filename.rsplit(".", 1)[-1].lower()
            if ext in ALLOWED_IMAGE_EXT:
                os.makedirs(UPLOAD_DIR, exist_ok=True)
                filename = secure_filename(f"{slug}-{secrets.token_hex(4)}.{ext}")
                upload.save(os.path.join(UPLOAD_DIR, filename))
                working.cover_image = filename
            else:
                flash("Изображение должно быть JPG, PNG или WEBP.", "error")

        db.session.commit()
        flash("Страница сохранена.", "success")
        return redirect(url_for("admin.pages_list"))

    return render_template("admin/page_form.html", item=item)


@admin_bp.route("/pages/<int:page_id>/delete", methods=["POST"])
@login_required
def page_delete(page_id):
    item = Page.query.get_or_404(page_id)
    db.session.delete(item)
    db.session.commit()
    flash("Страница удалена.", "success")
    return redirect(url_for("admin.pages_list"))


# ---------------------------------------------------------------- reviews
@admin_bp.route("/reviews")
@login_required
def reviews_list():
    items = Review.query.order_by(Review.created_at.desc()).all()
    return render_template("admin/reviews_list.html", items=items)


@admin_bp.route("/reviews/<int:review_id>/toggle", methods=["POST"])
@login_required
def review_toggle(review_id):
    item = Review.query.get_or_404(review_id)
    item.published = not item.published
    db.session.commit()
    flash("Отзыв опубликован." if item.published else "Отзыв скрыт.", "success")
    return redirect(url_for("admin.reviews_list"))


@admin_bp.route("/reviews/<int:review_id>/delete", methods=["POST"])
@login_required
def review_delete(review_id):
    item = Review.query.get_or_404(review_id)
    db.session.delete(item)
    db.session.commit()
    flash("Отзыв удалён.", "success")
    return redirect(url_for("admin.reviews_list"))
