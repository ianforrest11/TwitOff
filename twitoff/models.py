"""SQLAlchemy models for TwitOff assignment."""

from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

class User(DB.Model):
    """Create class 'User' for TwitOff
    User have methods:
    - id
    - name
    - newest_tweet_id
    - tweets (from linked relationship to 'Tweet' class)
    
    added __repr__ function to show content of User class as text (vs. as location in memory)"""
    id = DB.Column(DB.BigInteger, 
                   primary_key = True)
    name = DB.Column(DB.String(15), 
                     nullable = False)
    newest_tweet_id = DB.Column(DB.BigInteger)
    
    def __repr__(self):
        return '<USER {}>'.format(self.name)
    
class Tweet(DB.Model):
    """Create class 'Tweet' for TwitOff
    Tweet has methods:
    - id
    - text
    - embeddings (from Basilica API)
    - user_id (foreign key linked from 'User' class)
    - user (relationship identified with 'User' class, facilitates '.tweets' User method)
    
    
    added __repr__ function to show content of Tweet class as text (vs. as location in memory)"""
    # added date property to each tweet
    id = DB.Column(DB.BigInteger, 
                   primary_key = True)
    text = DB.Column(DB.Unicode(500))
    date = DB.Column(DB.DateTime)
    embedding = DB.Column(DB.PickleType,
                          nullable = False)
    user_id = DB.Column(DB.BigInteger,
                        DB.ForeignKey('user.id'),
                        nullable = False)
    user = DB.relationship('User',
                           backref = DB.backref('tweets', lazy = True))
    
    def __repr__(self):
        return '<TWEET {}>'.format(self.text)