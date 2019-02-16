from main import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)


def row2dict(row):
    return {c.name: str(getattr(row, c.name)) for c in row.__table__.columns}


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # id = db.relationship('Post', backref='Poster')
    name = db.Column(db.Text(), nullable=False)

    # How the Person object is printed out
    def __repr__(self):
        return "<Person {}: {}>".format(self.id, self.name)


class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    content = db.Column(db.String)

    def __repr__(self):
        return "<Post {}: {}>".format(self.post_id, self.user_id, self.content)


class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'))
    commenter_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    comment = db.Column(db.String)

    def __repr__(self):
        return "<Comment {}: {}>".format(self.comment_id, self.post_id, self.commenter_id, self.comment)