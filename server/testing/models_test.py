
import pytest
import logging
from faker import Faker
from server.app import app
from server.models import db, Author, Post

LOGGER = logging.getLogger(__name__)

class TestAuthor:
    def test_requires_name(self):
        with app.app_context():
            Author(name=Faker().name(), phone_number='1234567890')  # valid
            with pytest.raises(ValueError):
                Author(name='', phone_number='1234567890')  # invalid

    def test_requires_unique_name(self):
        with app.app_context():
            db.drop_all()
            db.create_all()

            author_a = Author(name='Ben', phone_number='1234567890')
            db.session.add(author_a)
            db.session.commit()

            with pytest.raises(ValueError):
                author_b = Author(name='Ben', phone_number='0987654321')  # duplicate

            db.drop_all()

    def test_requires_ten_digit_phone_number(self):
        with app.app_context():
            with pytest.raises(ValueError):
                Author(name='Jane', phone_number='123')  # too short
            with pytest.raises(ValueError):
                Author(name='Jane', phone_number='1234567890123')  # too long
            with pytest.raises(ValueError):
                Author(name='Jane', phone_number='123456789a')  # not digits

class TestPost:
    def test_requires_title(self):
        with app.app_context():
            content_string = "A" * 250
            with pytest.raises(ValueError):
                Post(title='', content=content_string, category='Non-Fiction')

    def test_content_length(self):
        with app.app_context():
            Post(title='Top Secret', content='A'*250, category='Non-Fiction')  # valid
            with pytest.raises(ValueError):
                Post(title='Top Guess', content='A'*249, category='Non-Fiction')  # too short

    def test_summary_length(self):
        with app.app_context():
            content_string = 'A'*250
            Post(title='Top Secret', content=content_string, summary='T'*250, category='Non-Fiction')  # valid
            with pytest.raises(ValueError):
                Post(title='Top Secret', content=content_string, summary='T'*251, category='Non-Fiction')  # too long

    def test_category(self):
        with app.app_context():
            content_string = 'A'*250
            with pytest.raises(ValueError):
                Post(title='Top Ten', content=content_string, category='Banana')  # invalid category

    def test_clickbait(self):
        with app.app_context():
            content_string = 'A'*260
            with pytest.raises(ValueError):
                Post(title='I love programming', content=content_string, category='Fiction')  # not clickbait
