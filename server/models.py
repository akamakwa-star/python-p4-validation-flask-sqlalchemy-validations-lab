# server/models.py
from .extensions import db

class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    phone_number = db.Column(db.String(10), nullable=False)

    def __init__(self, name, phone_number):
        if not name:
            raise ValueError("Name is required")
        if len(phone_number) != 10 or not phone_number.isdigit():
            raise ValueError("Phone number must be exactly 10 digits")
        # Check uniqueness
        if db.inspect(db.engine).has_table('authors') and db.session.query(Author).filter_by(name=name).first():
            raise ValueError(f"Author with name '{name}' already exists")

        self.name = name
        self.phone_number = phone_number

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.String(250))
    category = db.Column(db.String(50))

    def __init__(self, title, content, summary=None, category=None):
        if not title:
            raise ValueError("Title is required")
        if len(content) < 250:
            raise ValueError("Content must be at least 250 characters")
        if summary and len(summary) > 250:
            raise ValueError("Summary must be 250 characters or less")
        if category and category not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Invalid category")
        if not any(keyword in title for keyword in ['Why', 'Secret', 'Top']):
            raise ValueError("Title must be clickbait")

        self.title = title
        self.content = content
        self.summary = summary
        self.category = category
