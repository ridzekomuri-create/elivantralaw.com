from datetime import date, datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Service(db.Model):
    __tablename__ = "services"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(80), unique=True, nullable=False)
    icon = db.Column(db.String(40), nullable=False, default="globe")
    sort_order = db.Column(db.Integer, nullable=False, default=0)

    title = db.Column(db.String(255), nullable=False)
    title_en = db.Column(db.String(255), nullable=False, default="")
    short = db.Column(db.Text, nullable=False, default="")
    short_en = db.Column(db.Text, nullable=False, default="")
    text = db.Column(db.Text, nullable=False, default="")
    text_en = db.Column(db.Text, nullable=False, default="")
    points_raw = db.Column(db.Text, nullable=False, default="")       # one bullet per line
    points_en_raw = db.Column(db.Text, nullable=False, default="")    # one bullet per line

    @property
    def points(self):
        return [line.strip() for line in self.points_raw.splitlines() if line.strip()]

    @property
    def points_en(self):
        return [line.strip() for line in self.points_en_raw.splitlines() if line.strip()]


class PageView(db.Model):
    __tablename__ = "page_views"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    path = db.Column(db.String(255), nullable=False)
    referrer_host = db.Column(db.String(255), nullable=True)
    device = db.Column(db.String(16), nullable=False, default="desktop")
    visitor_id = db.Column(db.String(64), nullable=True, index=True)


class News(db.Model):
    __tablename__ = "news"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    published = db.Column(db.Boolean, nullable=False, default=True)
    published_at = db.Column(db.Date, nullable=False, default=date.today)
    service_slug = db.Column(db.String(80), nullable=True)      # related service, links to /services#slug
    source_name = db.Column(db.String(160), nullable=False, default="")
    source_url = db.Column(db.String(500), nullable=False, default="")

    title = db.Column(db.String(255), nullable=False)
    title_en = db.Column(db.String(255), nullable=False, default="")
    excerpt = db.Column(db.Text, nullable=False, default="")
    excerpt_en = db.Column(db.Text, nullable=False, default="")
    content = db.Column(db.Text, nullable=False, default="")       # blank-line-separated paragraphs
    content_en = db.Column(db.Text, nullable=False, default="")

    @property
    def paragraphs(self):
        return [p.strip() for p in self.content.split("\n\n") if p.strip()]

    @property
    def paragraphs_en(self):
        return [p.strip() for p in self.content_en.split("\n\n") if p.strip()]


class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    name = db.Column(db.String(120), nullable=False)
    country = db.Column(db.String(80), nullable=False, default="")
    text = db.Column(db.Text, nullable=False)
    published = db.Column(db.Boolean, nullable=False, default=False, index=True)


class Page(db.Model):
    __tablename__ = "pages"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    published = db.Column(db.Boolean, nullable=False, default=True)
    cover_image = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    title = db.Column(db.String(255), nullable=False)
    title_en = db.Column(db.String(255), nullable=False, default="")
    excerpt = db.Column(db.Text, nullable=False, default="")
    excerpt_en = db.Column(db.Text, nullable=False, default="")
    content = db.Column(db.Text, nullable=False, default="")       # blank-line-separated paragraphs
    content_en = db.Column(db.Text, nullable=False, default="")

    @property
    def paragraphs(self):
        return [p.strip() for p in self.content.split("\n\n") if p.strip()]

    @property
    def paragraphs_en(self):
        return [p.strip() for p in self.content_en.split("\n\n") if p.strip()]
