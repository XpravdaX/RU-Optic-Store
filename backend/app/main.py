from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import json
import datetime

from . import models, database
from .database import get_db, init_db

app = FastAPI(title="Optic Store API", version="1.0.0")

# CORS для работы с Tkinter
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Инициализация БД при старте
@app.on_event("startup")
def on_startup():
    init_db()


# Роуты для товаров
@app.get("/api/products", response_model=List[dict])
def get_products(
        skip: int = 0,
        limit: int = 100,
        category: Optional[str] = None,
        brand: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        in_stock: Optional[bool] = None,
        db: Session = Depends(get_db)
):
    """Получить список товаров с фильтрами"""
    query = db.query(models.Product)

    if category:
        query = query.filter(models.Product.category == category)
    if brand:
        query = query.filter(models.Product.brand == brand)
    if min_price is not None:
        query = query.filter(models.Product.price >= min_price)
    if max_price is not None:
        query = query.filter(models.Product.price <= max_price)
    if in_stock is not None:
        query = query.filter(models.Product.in_stock == in_stock)

    products = query.offset(skip).limit(limit).all()

    # Конвертируем в словари
    result = []
    for product in products:
        product_dict = {c.name: getattr(product, c.name) for c in product.__table__.columns}
        # Парсим features из JSON строки
        if product_dict.get('features'):
            try:
                product_dict['features'] = json.loads(product_dict['features'])
            except:
                product_dict['features'] = {}
        result.append(product_dict)

    return result


@app.get("/api/products/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Получить один товар по ID"""
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product_dict = {c.name: getattr(product, c.name) for c in product.__table__.columns}
    if product_dict.get('features'):
        try:
            product_dict['features'] = json.loads(product_dict['features'])
        except:
            product_dict['features'] = {}

    return product_dict


@app.get("/api/categories")
def get_categories(db: Session = Depends(get_db)):
    """Получить список категорий"""
    categories = db.query(models.Product.category).distinct().all()
    return [cat[0] for cat in categories if cat[0]]


@app.get("/api/brands")
def get_brands(db: Session = Depends(get_db)):
    """Получить список брендов"""
    brands = db.query(models.Product.brand).distinct().all()
    return [brand[0] for brand in brands if brand[0]]


# Роуты для заказов
@app.post("/api/orders")
def create_order(order_data: dict, db: Session = Depends(get_db)):
    """Создать новый заказ"""
    # Добавляем дату создания
    order_data['created_at'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_order = models.Order(**order_data)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # Обновляем количество товаров
    items = json.loads(order_data.get('items', '[]'))
    for item in items:
        product = db.query(models.Product).filter(models.Product.id == item['id']).first()
        if product:
            product.stock_quantity -= item['quantity']
            if product.stock_quantity <= 0:
                product.in_stock = False

    db.commit()
    return {"id": new_order.id, "message": "Order created successfully"}


@app.get("/")
def read_root():
    return {"message": "Optic Store API is running", "docs": "/docs"}