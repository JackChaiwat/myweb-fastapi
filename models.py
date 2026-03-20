from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)

    def __repr__(self):
        return self.name


class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    price = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey("category.id"))
    category = relationship("Category")

    def __repr__(self):
        return self.name

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    
    def __repr__(self):
        return self.name


class Customer(Base):
    __tablename__ = "customer"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    address = Column(String(200), nullable=True)
    tax_id = Column(String(15), nullable=True)
    
    def __repr__(self):
        return self.name


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    order_no = Column(String(50), nullable=False)
    order_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")
    customer_id = Column(Integer, ForeignKey("customer.id"))
    customer = relationship("Customer")
    amount_untaxed = Column(Float, nullable=True)
    amount_tax = Column(Float, nullable=True)
    amount_total = Column(Float, nullable=True)
    state = Column(String(50), nullable=True)
    details = relationship("OrderDetail", back_populates="order", lazy="selectin")
    
    def __repr__(self):
        return self.order_no
    

class OrderDetail(Base):
    __tablename__ = "order_details"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("product.id"))
    product = relationship("Product", lazy="selectin")
    qty = Column(Integer, nullable=True)
    price = Column(Float, nullable=True)
    amount = Column(Float, nullable=True)
    order = relationship("Order", back_populates="details", lazy="selectin")

    def __repr__(self):
        return self.product.name
