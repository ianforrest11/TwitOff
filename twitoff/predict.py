"""predictions of Users based on Tweet embeddings."""
# function called with two usernames, tweet text to predict

# imports
from .models import User
import numpy as np
from sklearn.linear_model import LogisticRegression
from .twitter import BASILICA

# embeddings for each tweet already exist, so function just has to iterate over therm
def predict_user(user1_name, user2_name, tweet_text):
    user1 = User.query.filter(User.name == user1_name).one()
    user2 = User.query.filter(User.name == user2_name).one()
    user1_embeddings = np.array([tweet.embedding for tweet in user1.tweets])
    user2_embeddings = np.array([tweet.embedding for tweet in user2.tweets])
    # THESE EMBEDDINGS...
    # add all embeddings into one giant matrix with np.vstack
    embeddings = np.vstack([user1_embeddings,
                            user2_embeddings])
    
    # ...GENERATED THE FOLLOWING LABELS:
    # assign value of 1 to user 1, value of 0 to user 2
    # arbitrary number, for choosing purposes
    # however many tweets user 1 has as 1s, however many tweets user 2 has as 0s
    labels = np.concatenate([np.ones(len(user1.tweets)),
                             np.zeros(len(user2.tweets))])
    log_reg = LogisticRegression().fit(embeddings, labels)
    # get embeddings for sentence we are predicting
    tweet_embedding = BASILICA.embed_sentence(tweet_text, model = 'twitter')
    # return 1 if tweet more likely to be tweeted by user1, 0 if user2
    # running predict_proba will give you probabilities of how likely 1 or 0
    return log_reg.predict_proba(np.array([tweet_embedding]))[:,1]
    
    