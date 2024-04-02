
# Spotify Podcast Search

Spotify Podcast Search is a tool designed to help users find specific episodes from a specified podcast on Spotify.

This project was also designed to showcase my proficiency in Python/Flask, and using PostgreSQL,
SQLAlchemy, Jinja, RESTful APIs, JavaScript, HTML, and CSS.

## How To Use 

You can either create a copy of the app, which ls a little difficult due to the Spotify API, or go to [my website](https://www.lipsum.com/) and use the app from there. If you'd like setup your own app, please refer to the [Spotify API documentation](https://developer.spotify.com/documentation/web-api) to better understand how the API requests are working, and refer to the environment variables near the bottom of the readme.  

### To use the app from [my website](https://www.lipsum.com/)

1. Register for an account
2. Select one of the podcast from the list
3. Enter the keyword that you'd like to search for and option episode offset 
4. Click the search button.  The app will return any episodes thatt contain your keyword in it's description

### Extra Info

Only admins can add and remove podcasts. To make your account into an admin account either use the User.make_admin_by_id() method inline, or edit an account in database. 

The offset field starts offsetting on the most recent episodes. Lets use a podcast with 200 episodes as an example. Leaving the offset field blank will search for the keyword from episode 200 to episode 150. If you offset by 50 the tool will search from episode 150 to episode 100, etc. The spotify API can only return 50 episodes at once, which is why the offset field is needed. 

Users can also add podcasts to their watchlsit. The watchlist can be viewed in the top left while on the podcast list page. 

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

#### For the Spotify API:
`CLIENT_ID`

`CLIENT_SECRET`
#### For Flask and the database:

`SECRET_KEY`

`SQLALCHEMY_DATABASE_URI`

#### For the testing (optional):

`SQLALCHEMY_DATABASE_URI_TEST`

`TEST_CODE`

