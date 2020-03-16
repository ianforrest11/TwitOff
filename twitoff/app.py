"""main application and routing logic for twitoff."""

from decouple import config
from flask import Flask, render_template, request
from .models import DB, User
from .twitter import add_or_update_user, update_all_users, remove_user
from .predict import predict_user

def create_app():
    """create/configure flask application."""
    app = Flask(__name__)
    
    # config link to database and env from .env file
    # remove flask shell warning about tracking modifications
    # initiate app
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DB.init_app(app)
    
    # create route to pass Users to application
    # populate user object in html template
    # sets title of application
    @app.route('/')
    def root():
        users = User.query.all()
        return render_template('base.html',
                               title = 'Home',
                               users = users)
        
    # define what to do when user enters /reset at end of URL
    # resets app! clears users
    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html',
                               title = 'DB Reset!',
                               users = [])
    
    # add route to update tweets for twitter users in database
    # to be triggered by 'update' button on base.html page
    @app.route('/update')
    def update():
        update_all_users()
        users = User.query.all()
        return render_template('base.html', title='Update all users!', users=users)
    
    # add user and user/<name>
    @app.route('/user', methods=['POST']) # trigger this if post request (adding to db)
    @app.route('/user/<name>', methods=['GET']) # trigger this if get request (pulling existing from db)
    def user(name=None, message=''):
        name = name or request.values['user_name']
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = "User {} successfully added!".format(name)
            tweets = User.query.filter(User.name == name).one().tweets # 'one()' means pull first user
        except Exception as e:
            message = "Error adding {}: {}".format(name, e)
            tweets = []
        return render_template('user.html', title=name, tweets=tweets,
                               message=message)
    
    # add route for logistic regression comparision; used for tweet predictor
    # will always be post
    @app.route('/compare', methods=['POST'])
    def compare(message=''):
        # pull users from DB
        user1, user2 = sorted([request.values['user1'],
                               request.values['user2']])
        # account for situation where users are the same - invalid
        if user1 == user2:
            message = 'Cannot compare a user to themselves!'
        # pull tweet text value from User entry
        # turned logistic regression prediction to an integer, to be desplayed in message
        # add messages, space for confidence interval to be displayed in response message
        else:
            tweet_text = request.values['tweet_text']
            confidence = int(predict_user(user1, user2, tweet_text) * 100)
            if confidence >= 50:
                message = f'"{tweet_text}" is more likely to be said by {user1} than {user2}, with {confidence}% confidence'
            else:
                message = f'"{tweet_text}" is more likely to be said by {user2} than {user1}, with {100-confidence}% confidence'
        return render_template('prediction.html', title='Prediction', message=message)
    
    # @app.route('/remove', methods = ['POST'])
    # def remove():
    #     name = request.values['user_name']
    #     try:
    #         # if request.method == 'POST':
    #         remove_user(name)
    #         message = "User {} (and related tweets) successfully deleted!".format(name)
    #     except Exception as e:
    #         message = "Error removing {}: {}".format(name, e)
    #     users = User.query.all()
    #     return render_template('base.html', title='not working', 
    #                            message=message, users=users)
    
    return app
    