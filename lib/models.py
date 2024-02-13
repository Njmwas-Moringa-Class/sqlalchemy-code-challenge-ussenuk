import os
import sys

sys.path.append(os.getcwd)

from sqlalchemy import (create_engine, 
                        PrimaryKeyConstraint, 
                        Column, 
                        String, 
                        Integer,
                        Table,
                        ForeignKey, MetaData, desc)
from sqlalchemy.orm import relationship, backref


from sqlalchemy.ext.declarative import declarative_base


convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

restaurant_customer = Table(
    'restaurant_customers',
    Base.metadata,
    Column('restaurant_id', ForeignKey('restaurants.id'), primary_key=True),
    Column('customer_id', ForeignKey('customers.id'), primary_key=True),
    extend_existing=True,
)

class Restaurant(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key=True)
    name = Column(String())
    price = Column(Integer)

    reviews = relationship('Review', backref=backref('restaurant'))

    customers = relationship('Customer', secondary=restaurant_customer, back_populates='restaurants')


    def __repr__(self):
        return f'Restaurant: {self.name}'
    
    @classmethod
    def fanciest(cls, session):
        # Query the Restaurant table, order by price in descending order, and get the first result
        return session.query(cls).order_by(desc(cls.price)).first()
    def all_reviews(self):
        # Initialize an empty list to store the review strings
        review_strings = []

        # Loop over all reviews for this restaurant
        for review in self.reviews:
            # Get the customer's full name
            customer_full_name = review.customer.full_name()

            # Format the review string
            review_string = f"Review for {self.name} by {customer_full_name}: {review.star_rating} stars."

            # Add the review string to the list
            review_strings.append(review_string)

        # Return the list of review strings
        return review_strings

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    first_name = Column(String())
    last_name = Column(String())

    reviews = relationship('Review', backref=backref('customer'))

    restaurants = relationship ('Restaurant', secondary = restaurant_customer, back_populates = 'customers')

    def __repr__(self):
        return f'Customer: {self.name}'
    
    def full_name(self):
        return f'customer Full name:{self.first_name} {self.last_name}'
    
    @property
    def favorite_restaurant(self):
        # Get the review with the highest star rating for this customer
        highest_rated_review = max(self.reviews, key=lambda review: review.star_rating, default=None)

        if highest_rated_review is not None:
            # Return the Restaurant instance associated with the highest-rated review
            return highest_rated_review.restaurant
        else:
            return None
        
    def add_review(self, restaurant, rating):
        # Create a new Review instance
        new_review = Review(star_rating=rating, restaurant_id=restaurant.id, customer_id=self.id)

        # Add the new review to the customer's list of reviews
        self.reviews.append(new_review)

    def delete_reviews(self, restaurant, session):
        # Find all reviews for the given restaurant in the customer's list of reviews
        reviews_to_delete = [review for review in self.reviews if review.restaurant_id == restaurant.id]

        # Remove the reviews from the customer's list of reviews
        for review in reviews_to_delete:
            self.reviews.remove(review)

        # Delete the reviews from the database
        for review in reviews_to_delete:
            session.delete(review)

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer(), primary_key=True)
    star_rating = Column(Integer())

    restaurant_id = Column(Integer(), ForeignKey('restaurants.id'))

    customer_id = Column(Integer(), ForeignKey('customers.id'))

    def __repr__(self):
        return f'Review(id={self.id},' + \
            f'star_rating={self.star_rating}, ' + \
            f'restaurant_id={self.restaurant_id}, ' + \
            f'customer_id={self.customer_id})'
    
    def full_review(self):
        # Get the restaurant name
        restaurant_name = self.restaurant.name

        # Get the customer's full name
        customer_full_name = self.customer.full_name()

        # Return the formatted string
        return f"Review for restaurant {restaurant_name} by {customer_full_name}: {self.star_rating} stars."