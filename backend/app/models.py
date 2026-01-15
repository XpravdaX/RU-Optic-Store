from sqlalchemy import Column, Integer, String, Float, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    brand = Column(String(100))
    category = Column(String(100))
    magnification = Column(String(50))
    reticle = Column(String(100))
    illumination = Column(Boolean, default=False)
    price = Column(Float, nullable=False)
    discount = Column(Float, default=0.0)
    rating = Column(Float, default=0.0)
    description = Column(Text)
    features = Column(Text)
    image_url = Column(String(500))
    in_stock = Column(Boolean, default=True)
    stock_quantity = Column(Integer, default=0)

    def __repr__(self):
        return f"<Product(name='{self.name}', price={self.price})>"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(100))
    customer_email = Column(String(100))
    customer_phone = Column(String(20))
    total_amount = Column(Float)
    status = Column(String(50), default="pending")
    items = Column(Text)
    created_at = Column(String(50))

    def __repr__(self):
        return f"<Order(id={self.id}, customer='{self.customer_name}')>"