import os
import re
import smtplib
import uuid
from email.message import EmailMessage
from urllib.parse import urlparse

from dotenv import load_dotenv
from flask import Flask, abort, jsonify, render_template, request

from admin import admin_bp
from constants import ICONS, TRUST
from models import News, Page, PageView, Review, Service, db
from seed import SEED_SERVICES
from seed_news import SEED_NEWS

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-key-change-me")
app.config["ADMIN_PASSWORD"] = os.environ.get("ADMIN_PASSWORD")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
app.register_blueprint(admin_bp)

with app.app_context():
    db.create_all()

    # Auto-seed services and news if the database is empty. This matters on
    # hosts with an ephemeral filesystem (e.g. Render's free tier), where
    # data.db is recreated empty on every deploy/restart — without this the
    # site would come up with no services and no news every time.
    if Service.query.count() == 0:
        for i, data in enumerate(SEED_SERVICES):
            db.session.add(Service(sort_order=i, **data))
    if News.query.count() == 0:
        for data in SEED_NEWS:
            db.session.add(News(**data))
    db.session.commit()

SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "465"))
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
CONTACT_TO_EMAIL = os.environ.get("CONTACT_TO_EMAIL", "elivantralaw@gmail.com")

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@app.context_processor
def inject_globals():
    services = Service.query.order_by(Service.sort_order, Service.id).all()
    return {
        "services": services,
        "trust": TRUST,
        "icons": ICONS,
        "cookie_consent": request.cookies.get("cookie_consent"),
    }


app.config["TRACKING_ENABLED"] = True
BOT_MARKERS = ("bot", "crawler", "spider", "preview", "headless")


def _device_type(ua):
    ua = ua.lower()
    if "ipad" in ua or "tablet" in ua:
        return "tablet"
    if "mobile" in ua or "iphone" in ua or "android" in ua:
        return "mobile"
    return "desktop"


@app.before_request
def track_pageview():
    if not app.config["TRACKING_ENABLED"] or request.method != "GET":
        return
    if request.path.startswith(("/static", "/admin", "/cookie-consent")) or request.path == "/favicon.ico":
        return
    ua = request.user_agent.string or ""
    if any(marker in ua.lower() for marker in BOT_MARKERS):
        return

    referrer_host = None
    if request.referrer:
        host = urlparse(request.referrer).netloc
        if host and host != request.host:
            referrer_host = host[:255]

    visitor_id = None
    if request.cookies.get("cookie_consent") == "accepted":
        visitor_id = request.cookies.get("visitor_id")

    db.session.add(PageView(
        path=request.path[:255],
        referrer_host=referrer_host,
        device=_device_type(ua),
        visitor_id=visitor_id,
    ))
    db.session.commit()


@app.route("/cookie-consent", methods=["POST"])
def cookie_consent():
    data = request.get_json(silent=True) or request.form
    choice = data.get("choice")
    if choice not in ("accepted", "declined"):
        return jsonify({"ok": False}), 400

    year = 365 * 24 * 3600
    resp = jsonify({"ok": True})
    resp.set_cookie("cookie_consent", choice, max_age=year, samesite="Lax", secure=request.is_secure)
    if choice == "accepted":
        if not request.cookies.get("visitor_id"):
            resp.set_cookie("visitor_id", uuid.uuid4().hex, max_age=year, httponly=True, samesite="Lax", secure=request.is_secure)
    else:
        resp.delete_cookie("visitor_id")
    return resp


@app.route("/")
def home():
    reviews = Review.query.filter_by(published=True).order_by(Review.created_at.desc()).limit(12).all()
    return render_template("index.html", reviews=reviews)


@app.route("/reviews", methods=["POST"])
def submit_review():
    data = request.get_json(silent=True) or request.form

    # Honeypot: real visitors leave this hidden field empty; bots fill it in.
    if (data.get("website") or "").strip():
        return jsonify({"ok": True})

    name = (data.get("name") or "").strip()
    country = (data.get("country") or "").strip()
    text = (data.get("text") or "").strip()

    if not (2 <= len(name) <= 120) or not (10 <= len(text) <= 1000) or len(country) > 80:
        return jsonify({"ok": False, "error": "invalid_input"}), 400

    db.session.add(Review(name=name, country=country, text=text, published=False))
    db.session.commit()
    return jsonify({"ok": True})


@app.route("/services")
def services():
    return render_template("services.html")


@app.route("/contacts")
def contacts():
    return render_template("contacts.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/materials")
def materials():
    items = Page.query.filter_by(published=True).order_by(Page.created_at.desc()).all()
    return render_template("materials_list.html", items=items)


@app.route("/materials/<slug>")
def material_detail(slug):
    item = Page.query.filter_by(slug=slug, published=True).first()
    if not item:
        abort(404)
    return render_template("materials_detail.html", item=item)


@app.route("/news")
def news_list():
    items = News.query.filter_by(published=True).order_by(News.published_at.desc(), News.id.desc()).all()
    return render_template("news_list.html", items=items)


@app.route("/news/<slug>")
def news_detail(slug):
    item = News.query.filter_by(slug=slug, published=True).first()
    if not item:
        abort(404)
    return render_template("news_detail.html", item=item)


@app.route("/contact", methods=["POST"])
def contact():
    data = request.get_json(silent=True) or request.form

    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    topic = (data.get("topic") or "").strip()
    message = (data.get("message") or "").strip()

    if not name or not email or not EMAIL_RE.match(email):
        return jsonify({"ok": False, "error": "invalid_input"}), 400

    if not SMTP_USER or not SMTP_PASSWORD:
        app.logger.error("Contact form submitted but SMTP_USER/SMTP_PASSWORD are not configured.")
        return jsonify({"ok": False, "error": "not_configured"}), 503

    subject = f"Заявка с сайта Elivantra Law — {topic or 'Без темы'}"
    body = (
        f"Новая заявка с сайта ELIVANTRA LAW\n\n"
        f"Имя: {name}\n"
        f"Email: {email}\n"
        f"Услуга: {topic or '—'}\n\n"
        f"Сообщение:\n{message or '—'}\n"
    )

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = CONTACT_TO_EMAIL
    msg["Reply-To"] = email
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
    except Exception:
        app.logger.exception("Failed to send contact form email")
        return jsonify({"ok": False, "error": "send_failed"}), 502

    return jsonify({"ok": True})


if __name__ == "__main__":
    # debug=True enables the interactive Werkzeug debugger, which lets anyone
    # who can trigger an error run arbitrary code. Keep it off unless FLASK_DEBUG=1
    # is explicitly set for local development.
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
