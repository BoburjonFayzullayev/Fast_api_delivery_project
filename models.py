from database import Base
from sqlalchemy import Column, Integer, Boolean, Text, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String(25), unique=True)
    email = Column(String(70), unique=True)
    password = Column(Text, nullable=True)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    orders = relationship("Order", back_populates='users')

    def __repr__(self):
        return f"User {self.username}"


class Order(Base):
    ORDER_STATUS = (
        ('PENDING', 'pending'),
        ('IN_TRANSIT', 'in_transit'),
        ('DELIVERED', 'delivered')
    )
    __tablename__ = 'orders'
    id = Column(Integer,  primary_key=True)
    quantity = Column(Integer, nullable=False)
    order_statutes = Column(ChoiceType(choices=ORDER_STATUS), default='PENDING')
    user_id = Column(Integer, ForeignKey('users.id'))
    users = relationship("User", back_populates='orders')
    product_id = Column(Integer, ForeignKey('products.id'))
    products = relationship("Product", back_populates='orders')

    def __repr__(self):
        return f"User {self.id}"


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    price = Column(Integer)
    orders = relationship("Order", back_populates='products')

    def __repr__(self):
        return f"User {self.name}"
