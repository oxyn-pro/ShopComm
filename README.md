# ShopComm

# Project Capabilities
- Any type of user can access the website and "add to cart" any items / products existing in the product catalog
- Any type of user can be: authenticated user, non-authenticated user (aka guest user)
- Any item that was selected by the authenticated user will be stored directly in the database
- An optimized cookie management system, which means that the selected items of an unauthenticated user (also known as a guest user) will be stored in the device's web browser memory (cookies). After navigating to the Shipping Information page, the user's cookies will be converted to JavaScript objects, then to Python objects, and ultimately stored in the database according to the user supplied username and email address.
- In this project there is a connection between each user and customer, which means that each created user will have its own customer, they are connected with "OneToOneField" (Django's model).

# SuperUser
Yes, in this project there can be created the superuser (thanks to Django). SuperUser has right to manage almost everything related to the internal information:
- SuperUser can register and add new items (can add images, descriptions, and id of the product)
- SuperUser edit info regarding the order items
- SuperUser has abilities to see newly registered users, customers, products, order items, shipping addresses, email addresses (it has not able to see users passwords)
- SuperUser can delete users (customer is connected to the user with OneToOneField, which means that if the user is deleted its customer will be also deleted)

# API management
#### In this project, I have used "Tastypie" a web service API framework for Django, and Fetch API for JavaScript in order to control Event Handlers:
    - 127.0.0.1:8000/api/products               -> Will render out the JSON format of all existing products info in the product catalog
    - 127.0.0.1:8000/api/product/<product id>   -> Will render out the JSON format of the particular product's info in the product catalog

Fetch API:
  In order to control event handlers, I used the fetch API "Post" method in order to get CSRF Token and particular Action ("add, remove" to understand better look "static/js/cart.js" file)

CSRF Token:
  CSRF Token is a required token that is necessary in order to work with Django. It prevents possible hacking actions, because of the unique combination of hashing methods.
