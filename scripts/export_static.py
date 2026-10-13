"""Render the Flask routes to static HTML (relative links) for a shareable
read-only preview — used to publish the site without needing a live server."""
import re
import shutil
from pathlib import Path

from app import app
from models import News, Page

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"

# Forms post to the Flask backend, which the static preview does not have,
# so they are left out of the preview to avoid a broken submit.
FORM_RE = re.compile(r'<form class="contact-form[^"]*" id="(?:contactForm|reviewForm)".*?</form>', re.DOTALL)


def fix_links(html: str) -> str:
    html = html.replace('="/static/', '="static/')
    html = html.replace('="/?', '="index.html?')
    html = re.sub(r'="/news/([a-z0-9-]+)(#[^"]*)?"', lambda m: f'="news-{m.group(1)}.html{m.group(2) or ""}"', html)
    html = re.sub(r'="/news(#[^"]*)?"', lambda m: f'="news.html{m.group(1) or ""}"', html)
    html = re.sub(r'="/materials/([a-z0-9-]+)(#[^"]*)?"', lambda m: f'="material-{m.group(1)}.html{m.group(2) or ""}"', html)
    html = re.sub(r'="/materials(#[^"]*)?"', lambda m: f'="materials.html{m.group(1) or ""}"', html)
    html = re.sub(r'="/services(#[^"]*)?"', lambda m: f'="services.html{m.group(1) or ""}"', html)
    html = re.sub(r'="/contacts(#[^"]*)?"', lambda m: f'="contacts.html{m.group(1) or ""}"', html)
    html = re.sub(r'="/privacy(#[^"]*)?"', lambda m: f'="privacy.html{m.group(1) or ""}"', html)
    html = re.sub(r'="/(#[^"]*)?"', lambda m: f'="index.html{m.group(1) or ""}"', html)
    html = FORM_RE.sub("", html)
    return html


def main():
    if BUILD.exists():
        shutil.rmtree(BUILD)
    BUILD.mkdir(parents=True)

    app.config["TRACKING_ENABLED"] = False
    with app.app_context():
        news_slugs = [n.slug for n in News.query.filter_by(published=True).all()]
        material_slugs = [p.slug for p in Page.query.filter_by(published=True).all()]

    pages = {"/": "index.html", "/services": "services.html", "/contacts": "contacts.html",
             "/news": "news.html", "/materials": "materials.html", "/privacy": "privacy.html"}
    pages.update({f"/news/{s}": f"news-{s}.html" for s in news_slugs})
    pages.update({f"/materials/{s}": f"material-{s}.html" for s in material_slugs})

    with app.test_client() as c:
        c.set_cookie("cookie_consent", "declined")
        for route, out_name in pages.items():
            resp = c.get(route)
            html = fix_links(resp.data.decode("utf-8"))
            (BUILD / out_name).write_text(html, encoding="utf-8")

    dst_static = BUILD / "static"
    shutil.copytree(
        ROOT / "static",
        dst_static,
        ignore=shutil.ignore_patterns("source"),
    )

    print("Built:", sorted(p.name for p in BUILD.iterdir()))


if __name__ == "__main__":
    main()
