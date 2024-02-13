#!/usr/bin/env python3

# Script goes here!
from faker import Faker
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Restaurant, Customer, Review

if __name__ == '__main__':
    engine = create_engine('sqlite:///db/restaurants.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(Restaurant).delete()
    session.query(Customer).delete()
    session.query(Review).delete()


    fake = Faker()

    restaurants = []
    for i in range(10):
        restaurant = Restaurant(
            name=fake.last_name(),
            price=random.randint(5, 60)
        )

        # add and commit individually to get IDs back
        session.add(restaurant)
        session.commit()

        restaurants.append(restaurant)


    customers = []
    for i in range(50):
        customer = Customer(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
        )

        session.add(customer)
        session.commit()

        customers.append(customer)

    reviews = []
    for customer in customers:
        for restaurant in restaurants:
            # For each restaurant, it picks a random number of customers (between 1 and 5) to write a review
            for i in range(random.randint(1,5)):
                customer = random.choice(customers)

                # It ensures that a customer can only review a restaurant once. 
                if restaurant not in customer.restaurants:

                    customer.restaurants.append(restaurant)
                    session.add(customer)
                    session.commit()


                # Create association between customer and restaurant
                # customer.restaurants.append(restaurant)
                # restaurant.customers.append(customer)
                
                # Add the review to the lis
                review = Review(
                        star_rating = random.randint(0,5),
                        restaurant_id=restaurant.id,
                        customer_id=customer.id,
                    )


                reviews.append(review)

        # Save all reviews to the database

    session.bulk_save_objects(reviews)
    session.commit()

    session.close()