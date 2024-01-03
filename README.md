# Yu-Gi-Oh! Card Shop
#### Video Demo:  https://youtu.be/Vx14Tt6TXq0
#### Description: A simple Yu-Gi-Oh! Card Shop created using Python, Flask, AJAX, HTML, CSS, SQL and Javascript.

I used various APIs from https://yugiohprices.docs.apiary.io/# and https://ygoprodeck.com/api-guide/ to obtain data for card details and prices. This project's functionalities include: being able to search for a specific card (with search suggestions), registration and login, shopping cart, and checkout. For the login and registration function, it is pretty much the same concept from the previous finance cs50 problem set. For the search function, I used the APIs in order to access the data, format them and display them to the website. Finally for the shopping cart and checkout, a database is used in order to store the user's added items and information. UI is created using plain HTML and CSS.

Main file contents of this project:
*HTML Files:
    -index.html
    -search.html
    -checkout.html
*CSS Files:
    -styles.css
*Python Files:
    -app.py
    -api.py
*Javascript Files:
    -script.js
*Database Files:
    -final-project.db

The main page of the project is the html file index.html. This page includes the search bar, a "Home" button, an "About" button, a "Login" button and the Shopping Cart icon button. Registration form can be located within the Login form if user has no valid credentials for Login yet.

The search.html file displays the specific card that the user has searched, which includes the name of the card, the type of card, the image of the card, all the sets in which the card was printed, it's unique card number, the rarity for each specific set, the price of the card, and the option to add that card to your cart with a specific quantity. For this project, only users who have logged in have the ability to access their carts and be able to add cards to their respective carts.

For the final HTML file: checkout.html is a page which displays all the cards that have been added to the cart, showing some of the same details from the cards added to the cart. It shows a simple form that the user will have to fill up for their potential order. This page also has a "Keep Shopping" hyperlink in order to return to the main page.

styles.css is used to design the look of the webpage.

In order to handle the routing and track the session ID of the current logged in user, app.py is coded using basically the same fundamental concepts from the finance problem set of CS50.

Next is api.py, which handles the API requests sent to https://yugiohprices.docs.apiary.io/# and https://ygoprodeck.com/api-guide/ for all the card details and prices. Also included in this file is the function for requiring log in credentials.

Lastly, script.js is used to modify certain UI related functionalites, which include the popping out of the login form and its shifting to the registration form. It also includes the displaying of the cart from the right side of the page. This is used so all elements can be accessed from the main page. AJAX code is also included in order to dynamically alter the quantity of a specific card in the user's cart, which in turn also modifies the total number of items in the user's cart, and the price for the specific quantity of that card.

The final-project.db file contains a users Table and a cart Table. The users table stores information about the users who have registered. This includes their username, their hashed password, and their email. For the cart Table, it includes information regarding the cards that the users decide to add to their respective carts, which include the name of the card, the set the card is from, the rarity of the card, the quantity of the card the user has decided to add to their cart, the price per unit of the card and the URL for the image of the card (in order to display the specific image of the card in the cart). The table also has a foreign key of the user id to the user Table in order to keep track which user owns that specific cart of cards.
