# TwitOff
TwitOff is a Twitter analysis product designed to showcase text analysis, modeling database architecture, front-end development, and back-end development skills.

URL: https://ianforrest11-twitoff.herokuapp.com/

# Summary
TwitOff is a predictor function that analyzes the text of Twitter users.  Users are added to the SQLite3 database, and from that database two Users are selected for analysis.

A given body of text is entered for the two Users, and the TwitOff predictor does the rest!  The following have been selected in the image below:
- Tweeter 1 - Hillary Clinton - Former Democratic candidate for president
- Tweeter 2 - Bill Simmons - Sports Columnist/Podcaster
- Tweet Text - **"Go democrats!"**
![Alt text](images/menu.png?raw=true "Title")

A logistic regression model analyzes the Twitter history of the two Users selected, and then makes a prediction for likelihood that one of the Users tweeted the body of text:
- Result - **"Go democrats!" is more likely to be said by hillaryclinton than billsimmons, with 84% confidence**
![Alt text](images/results.png?raw=true "Title")