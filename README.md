# News Scraper

## MVP
- User authentication 
- Frontend ->
- Backend -> Flask 
- Scraping from one/ two news websites based on keyword 
- DB to store user and article information 

## Technologies
- SQLAlchemy
- Beautiful Soup / Scrappy (Python)
- Flask (Python) 
- Unittest/ Pytest 
- Flask_login/ Werkzeug_Security
- Bootstrap/ Bulma

## User stories
- As a user, if I am new to the website, I should be able to sign up
- As a user, if I already have an account, I should be able to log in
- As a user, if I am logged in, I should be able to see my dashboard 
- As a user, when I want to leave the page, I should be able to log out if I was already logged in
- As a user, if I forgot my accound credentials, I should be able to retrieve it through email 
- As a user, on my dashboard, I should be able to see my saved search terms as tabs
- As a user, on my dashboard, I should be able to pin specific search terms onto a UI element 
- As a user, when I look at the search results, I should be able to tell which source they are from 
- As a user, I should be able to see a random article title, which can be refreshed for a new random title 
- __As a user, I should be able to search for a keyword in the app to return a list of scraped articles from a number of news websites__

## Problems faced

## Planning 
- Stage 1: Get the scraper to scrape
- Stage 2: Disect response to get information that we want (e.g. title, link to article)
- Stage 3: Display scraped bits onto a front end 
- Stage 4: Add user authentication and be able to search on front-end
- Stage 5: Show recent searches and pinned search terms
- Stage 6: Random article 
- Stage 7: Sentiment analysis (Stretch) and insights from it 
- Stage 8: Profile stats (searches, articles read, streaking/ goals) (Stretch) 

## Database Architecture
- User table
- Category/ Search term table
