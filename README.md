# ShopComm

The link of the web site that has been deployed to the Heroku:
https://quiet-sands-71880.herokuapp.com/

# Project Capabilities
- Any type of user can access the website and "add to cart" any items/products existing in the product catalog
- Any type of user can be: authenticated user, non-authenticated user (aka guest user)
- Any item that was selected by authenticated user will be stored directly in the data-base
- An optimized cookie management system, which means that the selected items of an unauthenticated user (also known as a guest user) will be stored in the device's web browser memory (cookies). After navigating to the Shipping Information page, the user's cookies will be converted to Java Script objects, then to Python objects, and ultimately stored in the database according to the user supplied username and email address.
- In this projects there is a connection between each user and customer, which means that each created user will have its own customer, they are connected with "OneToOneField" (Django's model). 

# Super User
Yes, in this project there can be created the super user (thanks to the Django). Super User has rights to manage almost everything related to the internal information:
- Super User can register and add new items (can add images, descriptions, and id of the product)
- Super User edit info regarding the order items
- Super User has ablities to see new registered users, customers, products, order items, shipping addresses, email adresses (it has not ability to see users passwords)
- Super User can delete users (customer is connected to the user with OneToOneField, which means that if the user is deleted its customer will be also deleted)

# API management

 
