#!/usr/bin/env python3
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Restaurant, Customer, Review

import ipdb;


if __name__ == '__main__':
    
    engine = create_engine('sqlite:///db/restaurants.db')
    Session = sessionmaker(bind=engine)
    session = Session()
             
    """Customer full_name()"""
    # # returns the full name of the customer, with the first name and the last name concatenated, Western style
    # customers = session.query(Customer).all()

    # # For each customer, print its full name in western sty;e
    # for customer in customers:
    #     print(customer.full_name())

    """Customer favorite_restaurant()"""
    # # Get all customers
    # customers = session.query(Customer).all()

    # # For each customer, print its full name and favorite restaurant
    # for customer in customers:
    #     print(f"{customer.full_name()}")
    #     favorite_restaurant = customer.favorite_restaurant
    #     if favorite_restaurant is not None:
    #         print(f"Favorite restaurant: {favorite_restaurant.name}")
    #     else:
    #         print("This customer has not reviewed any restaurants yet.")

    """Customer add_review(restaurant, rating)"""

    # # Create a new review
    # # Get a customer and a restaurant
    # customer = session.query(Customer).first()
    # restaurant = session.query(Restaurant).first()

    # # Check the initial number of reviews for the customer
    # print(f"Initial number of reviews for the customer: {len(customer.reviews)}")

    # # Create a new review
    # customer.add_review(restaurant, 5)

    # # Check the number of reviews for the customer after adding the new review
    # print(f"Number of reviews for the customer after adding the new review: {len(customer.reviews)}")

    # # Commit the new review to the database
    # session.add(customer)
    # session.commit()

    # # Check the number of reviews for the customer after committing the new review to the database
    # print(f"Number of reviews for the customer after committing the new review to the database: {len(customer.reviews)}")


    """Customer delete_reviews(restaurant)"""

    # # Get a customer and a restaurant
    # customer = session.query(Customer).first()
    # restaurant = session.query(Restaurant).first()

    # # Check the initial number of reviews for the customer
    # print(f"Initial number of reviews for the customer: {len(customer.reviews)}")

    # # Delete all reviews for a restaurant
    # customer.delete_reviews(restaurant, session)

    # # Commit the changes to the database
    # session.commit()

    # # Check the number of reviews for the customer after deleting the reviews
    # print(f"Number of reviews for the customer after deleting the reviews: {len(customer.reviews)}")

    """Review full_review()"""
    # # Get a review
    # review = session.query(Review).first()

    # # Check the output of the full_review method
    # print(review.full_review())

    """Restaurant fanciest()"""
    # # Call the fanciest method and print the result
    # fanciest_restaurant = Restaurant.fanciest(session)
    # print(fanciest_restaurant)

    """Restaurant all_reviews()"""
    # Get a restaurant
    restaurant = session.query(Restaurant).first()

    # Call the all_reviews method and print the result
    all_reviews = restaurant.all_reviews()
    for review in all_reviews:
        print(review)


    ipdb.set_trace()