# cs290-cs496-final-project
Final project for CS290 and CS496

API Endpoints:

All endpoints are prepended with: http://burleigb-final.appspot.com/

/
  GET|POST: Loads main login page.

/login
  POST: Takes login credentials and creates new user or logs in existing user. Returns auth token.

/book
  GET: Returns a list of all the book reviews created by the user who requested it.

  POST: Adds a new book review to the database.

/book/<id number>
  GET: Returns the book review specified by the id number.

  PUT: Updates the book review specified by the id number.

/book/<id number>/<token>
  DELETE: Deletes book review specified by the id number. Token is passed as kwarg because DELETE does not allow for data payload.

/public
  GET: Returns all book reviews that have been indicated as publicly visible

/public/<id number>
  GET: Returns publicly visible book review specified by id number. Will not return private reviews.

Any HTTP request methods not listed are not supported.


Account System:
  I rolled my own accounts system. Basically, I just let a user specify a login and password. When a user logs in, if the username doesn't exist, an account is created. If the username exists, the password is checked. When a user logs in, an authentication token is returned that is used for all API endpoints except for /public. With the exception of the DELETE call, the token is passed as an argument on the url, or in POST data. Ex: /book?token=<some number>.  Users cannot view/edit private book reviews for which they do not have the appropriate token. It's not hyper-secure because the token could be lifted via packet sniffing and used by a person with malicious intent.
