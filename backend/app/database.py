from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# SQLite база данных
DATABASE_URL = "sqlite:///./optic_store.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False  # Выключим логирование для продакшена
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    from .models import Base, Product

    # Создаем все таблицы
    Base.metadata.create_all(bind=engine)

    # Добавляем тестовые данные в рублях
    db = SessionLocal()
    try:
        # Проверяем, есть ли уже товары
        if db.query(Product).count() == 0:
            sample_products = [
                Product(
                    name="Leupold VX-Freedom 3-9x40",
                    brand="Leupold",
                    category="Оптический прицел",
                    magnification="3-9x40",
                    reticle="Duplex",
                    illumination=False,
                    price=34999.99,  # Рубли вместо долларов
                    discount=0.0,
                    rating=4.8,
                    description="Надежный прицел для охоты с просветленной оптикой",
                    features='{"поле зрения":"100м/33ft", "вес":"340г", "длина":"330мм"}',
                    image_url="https://via.placeholder.com/300x200/3D5A80/FFFFFF?text=Leupold",
                    in_stock=True,
                    stock_quantity=15
                ),
                Product(
                    name="Vortex Razor HD Gen III 1-10x24",
                    brand="Vortex",
                    category="Оптический прицел",
                    magnification="1-10x24",
                    reticle="EBR-9 MRAD",
                    illumination=True,
                    price=219999.99,  # Рубли
                    discount=199999.99,
                    rating=4.9,
                    description="Профессиональный LPVO прицел с подсветкой",
                    features='{"поле зрения":"113ft/34m", "вес":"680г", "длина":"260мм"}',
                    image_url="https://via.placeholder.com/300x200/98C1D9/000000?text=Vortex",
                    in_stock=True,
                    stock_quantity=8
                ),
                Product(
                    name="EOTech EXPS3 Holographic",
                    brand="EOTech",
                    category="Коллиматорный прицел",
                    magnification="1x",
                    reticle="Holographic Ring",
                    illumination=True,
                    price=64999.99,  # Рубли
                    discount=59999.99,
                    rating=4.7,
                    description="Голографический прицел с всепогодным исполнением",
                    features='{"время работы":"600ч", "вес":"312г", "батарея":"CR123"}',
                    image_url="https://via.placeholder.com/300x200/EE6C4D/FFFFFF?text=EOTech",
                    in_stock=True,
                    stock_quantity=12
                ),
                Product(
                    name="NightForce ATACR 5-25x56",
                    brand="NightForce",
                    category="Тактический прицел",
                    magnification="5-25x56",
                    reticle="TREMOR3",
                    illumination=True,
                    price=379999.99,  # Рубли
                    discount=0.0,
                    rating=5.0,
                    description="Премиальный прицел для дальнобойной стрельбы",
                    features='{"поле зрения":"21ft/6.4m", "вес":"1247г", "длина":"381мм"}',
                    image_url="https://via.placeholder.com/300x200/293241/FFFFFF?text=NightForce",
                    in_stock=True,
                    stock_quantity=5
                ),
                Product(
                    name="Sig Sauer Romeo5 Red Dot",
                    brand="Sig Sauer",
                    category="Коллиматор",
                    magnification="1x",
                    reticle="2 MOA Dot",
                    illumination=True,
                    price=14999.99,  # Рубли
                    discount=12999.99,
                    rating=4.5,
                    description="Компактный и надежный коллиматорный прицел",
                    features='{"время работы":"40000ч", "вес":"152г", "крепление":"Picatinny"}',
                    image_url="https://via.placeholder.com/300x200/3D5A80/FFFFFF?text=Sig+Sauer",
                    in_stock=True,
                    stock_quantity=25
                ),
                Product(
                    name="Бурта АС-3-9х40",
                    brand="Бурта",
                    category="Оптический прицел",
                    magnification="3-9x40",
                    reticle="P4",
                    illumination=False,
                    price=8999.99,
                    discount=7999.99,
                    rating=4.3,
                    description="Российский прицел для охоты и спортивной стрельбы",
                    features='{"поле зрения":"32м/100м", "вес":"450г", "длина":"320мм"}',
                    image_url="https://via.placeholder.com/300x200/4CAF50/FFFFFF?text=Бурта",
                    in_stock=True,
                    stock_quantity=20
                ),
                Product(
                    name="ВОМЗ Пиленгас 8х56",
                    brand="ВОМЗ",
                    category="Ночной прицел",
                    magnification="8x56",
                    reticle="Прицельная марка ПМ",
                    illumination=True,
                    price=45999.99,
                    discount=0.0,
                    rating=4.6,
                    description="Отечественный ночной прицел с подсветкой",
                    features='{"диаметр объектива":"56мм", "вес":"850г", "удаление выходного зрачка":"70мм"}',
                    image_url="https://via.placeholder.com/300x200/2196F3/FFFFFF?text=ВОМЗ",
                    in_stock=True,
                    stock_quantity=7
                ),
                Product(
                    name="Калев Зенит 4х32",
                    brand="Калев",
                    category="Оптический прицел",
                    magnification="4x32",
                    reticle="Duplex",
                    illumination=False,
                    price=12999.99,
                    discount=11999.99,
                    rating=4.2,
                    description="Эстонский прицел для мелкокалиберного оружия",
                    features='{"поле зрения":"8м/100м", "вес":"380г", "длина":"290мм"}',
                    image_url="https://via.placeholder.com/300x200/FF9800/000000?text=Калев",
                    in_stock=True,
                    stock_quantity=15
                )
            ]
            db.add_all(sample_products)
            db.commit()
            print("Тестовые данные добавлены")
    except Exception as e:
        print(f"Ошибка при добавлении тестовых данных: {e}")
        db.rollback()
    finally:
        db.close()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()