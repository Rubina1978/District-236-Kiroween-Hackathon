# Score Board

### Django Project

- Me and Hana have both agreed we would like a public score board and that we can do this with Django auth and a PostgreSQL database.

- First we just need to rack up some score in the game, and then we can work on saving these scores for registered players and keeping track of their personal best scores.

- I am hoping it will be as easy as: user authenticates, and for the public score board we iterate through every user and display their score. I think it could be this easy as long as sensitive information is appropriately encapsulated.

- Maybe we don't even have to have proper logins, just state your username and away you go and we can store it in the database. This is because I am uncertain as to whether having the django project publically accessible will be a security risk in itself. Actually, yes it would - because a lot of what should be a private / secret key will be exposed.

---
### Let us consider this later