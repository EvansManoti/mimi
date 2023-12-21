from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Restaurant(Base):
    __tablename__ = 'restaurants'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    reviews = relationship('Review', back_populates='restaurant')
    customers = relationship('Customer', secondary='reviews')

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    reviews = relationship('Review', back_populates='customer')

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    star_rating = Column(Integer)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    customer_id = Column(Integer, ForeignKey('customers.id'))
    restaurant = relationship('Restaurant', back_populates='reviews')
    customer = relationship('Customer', back_populates='reviews')

engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


class Review(Base):

    def customer(self):
        return self.customer

    def restaurant(self):
        return self.restaurant

class Restaurant(Base):

    def reviews(self):
        return self.reviews

    def customers(self):
        return [review.customer for review in self.reviews]

class Customer(Base):

    def reviews(self):
        return self.reviews

    def restaurants(self):
        return [review.restaurant for review in self.reviews]


class Customer(Base):

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def favorite_restaurant(self):
        favorite_review = max(self.reviews, key=lambda x: x.star_rating, default=None)
        return favorite_review.restaurant if favorite_review else None

    def add_review(self, restaurant, rating):
        new_review = Review(star_rating=rating, restaurant=restaurant, customer=self)
        session.add(new_review)
        session.commit()

    def delete_reviews(self, restaurant):
        reviews_to_delete = [review for review in self.reviews if review.restaurant == restaurant]
        for review in reviews_to_delete:
            session.delete(review)
        session.commit()

# ... (previous code)

class Review(Base):
    # ... (previous code)

    def full_review(self):
        return f"Review for {self.restaurant.name} by {self.customer.full_name()}: {self.star_rating} stars."

class Restaurant(Base):

    @classmethod
    def fanciest(cls):
        return max(session.query(cls).all(), key=lambda x: x.price, default=None)

    def all_reviews(self):
        return [review.full_review() for review in self.reviews]

