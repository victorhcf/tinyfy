from flaskr import database

from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from sqlalchemy_serializer import SerializerMixin

#database = SQLAlchemy(app)

from sqlalchemy import inspect

from datetime import datetime

'''

CREATE TABLE stats (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  url_id INTEGER NOT NULL,
  code TEXT NOT NULL,
  url_original TEXT NOT NULL,
  ip TEXT NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_stats_url_id ON stats (url_id); 
CREATE INDEX idx_user_username ON user (username); 


# ALTER TABLE urls ADD user BOOL NOT NULL SET DEFAULT TRUE;
# ALTER TABLE urls ADD CONSTRAINT fk_url_user FOREIGN KEY(user) REFERENCES user (id);




CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
, updated DATETIME);

CREATE TABLE urls (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  url_original TEXT NOT NULL,
  url_secret TEXT NOT NULL,
  code TEXT NOT NULL,
  user_id INTEGER,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, 
  updated DATETIME, 
  user INT NULL, 
  enabled BOOL DEFAULT TRUE,
  FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE stats (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  url_id INTEGER NOT NULL,
  code TEXT NOT NULL,
  url_original TEXT NOT NULL,
  ip TEXT NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_stats_url_id ON stats (url_id);
CREATE INDEX idx_user_username ON user (username);




'''

class User(database.Model, SerializerMixin):
    serialize_rules = ('-urls.user',)
    id = database.Column(database.Integer, primary_key=True) #serializer to avoid recursion problem when encoding to json
    username = database.Column(database.String(40), unique=True, nullable=False)
    password = database.Column(database.String(), nullable=False)
    #created = database.Column(database.DateTime(timezone=True), nullable=False, default=datetime.now)
    updated = database.Column(database.DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)    # The Date of the Instance Update => Changed with Every Update
    urls = database.relationship("Url", primaryjoin="Url.user_id==User.id", back_populates="user")


class Url(database.Model, SerializerMixin):
    __tablename__ = "urls"
    id = database.Column(database.Integer, primary_key=True)
    url_original = database.Column(database.String(250), nullable=False)
    secret = database.Column("url_secret", database.Integer, nullable=False)
    code = database.Column(database.String(10), nullable=False)
    created = database.Column(database.DateTime(timezone=True), nullable=False, default=datetime.now)
    #updated = database.Column(database.DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)    # The Date of the Instance Update => Changed with Every Update
    enabled = database.Column(database.Boolean, nullable=False, default=True )
    user_id = database.Column(database.Integer, ForeignKey('user.id'))
    user = relationship("User", primaryjoin=user_id == User.id, back_populates="urls")

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

    def __repr__(self):
        return "<%r>" % self.code


class Stats(database.Model, SerializerMixin):
    id = database.Column(database.Integer, primary_key=True)
    url_id = database.Column(database.Integer)
    url_original = database.Column(database.String(250), nullable=False)
    code = database.Column(database.String(10), nullable=False)
    created = database.Column(database.DateTime(timezone=True), nullable=False, default=datetime.now)
    ip = database.Column(database.String(250), nullable=False)