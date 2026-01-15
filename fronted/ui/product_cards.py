import customtkinter as ctk
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import threading


class ProductCard(ctk.CTkFrame):
    def __init__(self, master, product_data, colors, on_add_to_cart, **kwargs):
        super().__init__(master, **kwargs)

        self.product_data = product_data
        self.colors = colors
        self.on_add_to_cart = on_add_to_cart

        # Фиксированный размер карточки
        self.configure(
            width=300,
            height=450,
            corner_radius=12,
            border_width=1,
            border_color=self.colors["border"],
            fg_color=self.colors["bg_card"]
        )

        self.setup_ui()
        self.load_image()

    def setup_ui(self):
        # Основной контейнер
        self.main_container = ctk.CTkFrame(
            self,
            fg_color="transparent",
            height=450
        )
        self.main_container.pack(fill="both", expand=True, padx=12, pady=12)

        # Контейнер для содержимого
        self.content_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True)

        # Заголовок с названием
        self.name_label = ctk.CTkLabel(
            self.content_frame,
            text=self.product_data.get('name', 'Название'),
            font=("Arial", 15, "bold"),
            wraplength=270,
            justify="center",
            height=45,
            text_color=self.colors["text_primary"]
        )
        self.name_label.pack(pady=(0, 5), anchor="n")

        # Бренд
        self.brand_label = ctk.CTkLabel(
            self.content_frame,
            text=self.product_data.get('brand', ''),
            font=("Arial", 12),
            text_color=self.colors["accent_secondary"],
            height=20
        )
        self.brand_label.pack(pady=(0, 5), anchor="n")

        # Изображение (фиксированный размер)
        self.image_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color=self.colors["bg_light"],
            corner_radius=8,
            height=150
        )
        self.image_frame.pack(pady=8, fill="x", padx=5)

        self.image_label = ctk.CTkLabel(
            self.image_frame,
            text="Загрузка...",
            width=250,
            height=150,
            text_color=self.colors["text_muted"]
        )
        self.image_label.pack(expand=True)

        # Характеристики
        features_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent", height=50)
        features_frame.pack(fill="x", padx=10, pady=5)

        mag = self.product_data.get('magnification', 'N/A')
        ctk.CTkLabel(
            features_frame,
            text=f"🔍 Увеличение: {mag}",
            font=("Arial", 11),
            text_color=self.colors["text_secondary"]
        ).pack(anchor="w", pady=2)

        reticle = self.product_data.get('reticle', 'N/A')
        ctk.CTkLabel(
            features_frame,
            text=f"🎯 Сетка: {reticle}",
            font=("Arial", 11),
            text_color=self.colors["text_secondary"]
        ).pack(anchor="w", pady=2)

        # Цена в рублях
        price_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent", height=60)
        price_frame.pack(pady=(8, 0), fill="x")

        price = self.product_data.get('price', 0)
        discount = self.product_data.get('discount', 0)

        if discount and discount < price:
            # Старая цена с перечеркиванием
            formatted_old_price = f"{price:,.2f}".replace(",", " ")
            old_price_label = ctk.CTkLabel(
                price_frame,
                text=f"{formatted_old_price} ₽",
                font=("Arial", 12),
                text_color=self.colors["text_muted"]
            )
            old_price_label.pack()

            # Новая цена
            formatted_new_price = f"{discount:,.2f}".replace(",", " ")
            self.price_label = ctk.CTkLabel(
                price_frame,
                text=f"{formatted_new_price} ₽",
                font=("Arial", 20, "bold"),
                text_color=self.colors["accent_success"]
            )
            self.price_label.pack()
        else:
            formatted_price = f"{price:,.2f}".replace(",", " ")
            self.price_label = ctk.CTkLabel(
                price_frame,
                text=f"{formatted_price} ₽",
                font=("Arial", 20, "bold"),
                text_color=self.colors["text_primary"]
            )
            self.price_label.pack()

        # Рейтинг
        rating_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent", height=30)
        rating_frame.pack(pady=(8, 0), fill="x")

        rating = self.product_data.get('rating', 0)
        rating_text = "★" * int(rating) + "☆" * (5 - int(rating))
        self.rating_label = ctk.CTkLabel(
            rating_frame,
            text=f"{rating_text} ({rating})",
            font=("Arial", 13),
            text_color=self.colors["rating"]
        )
        self.rating_label.pack()

        # Кнопка добавления в корзину
        button_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent", height=50)
        button_frame.pack(pady=(15, 0), fill="x", padx=10)

        in_stock = self.product_data.get('in_stock', False)
        button_text = "🛒 В корзину" if in_stock else "⛔ Нет в наличии"

        self.add_button = ctk.CTkButton(
            button_frame,
            text=button_text,
            command=self.add_to_cart,
            font=("Arial", 14, "bold"),
            fg_color=self.colors["accent_primary"] if in_stock else self.colors["bg_light"],
            hover_color=self.colors["accent_warning"] if in_stock else self.colors["hover"],
            text_color=self.colors["text_primary"],
            border_color=self.colors["border"] if not in_stock else None,
            border_width=1 if not in_stock else 0,
            state="normal" if in_stock else "disabled",
            corner_radius=10,
            height=42
        )
        self.add_button.pack(fill="x")

        # Принудительная установка размеров
        self.update_idletasks()

    def load_image(self):
        """Асинхронная загрузка изображения"""

        def load():
            image_url = self.product_data.get('image_url')
            if image_url and image_url.startswith('http'):
                try:
                    response = requests.get(image_url, timeout=5)
                    img = Image.open(BytesIO(response.content))
                    img = img.resize((250, 150), Image.Resampling.LANCZOS)

                    # Добавляем легкую рамку к изображению
                    bordered_img = Image.new('RGB', (254, 154), self.colors["border"])
                    bordered_img.paste(img, (2, 2))

                    photo = ctk.CTkImage(
                        light_image=bordered_img,
                        dark_image=bordered_img,
                        size=(254, 154)
                    )

                    # Обновляем в основном потоке
                    self.after(0, lambda: self.image_label.configure(image=photo, text=""))
                except:
                    self.set_default_image()
            else:
                self.set_default_image()

        thread = threading.Thread(target=load)
        thread.daemon = True
        thread.start()

    def set_default_image(self):
        """Установить изображение по умолчанию"""
        try:
            # Создаем изображение с градиентом
            img = Image.new('RGB', (250, 150), color=self.colors["bg_light"])
            draw = ImageDraw.Draw(img)

            # Добавляем легкий градиент
            for i in range(150):
                color_value = 40 + int(i * 0.5)
                draw.line([(0, i), (250, i)], fill=(color_value, color_value, color_value))

            # Простой текст с брендом
            brand = self.product_data.get('brand', 'Optic')
            try:
                font = ImageFont.truetype("arial.ttf", 24)
            except:
                font = ImageFont.load_default()

            # Центрируем текст
            text_bbox = draw.textbbox((0, 0), brand, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]

            position = ((250 - text_width) // 2, (150 - text_height) // 2)
            draw.text(position, brand, font=font, fill=self.colors["accent_secondary"])

            # Добавляем рамку
            bordered_img = Image.new('RGB', (254, 154), self.colors["border"])
            bordered_img.paste(img, (2, 2))

            photo = ctk.CTkImage(
                light_image=bordered_img,
                dark_image=bordered_img,
                size=(254, 154)
            )
            self.image_label.configure(image=photo, text="")
        except:
            # Просто цветной прямоугольник если что-то пошло не так
            img = Image.new('RGB', (250, 150), color=self.colors["bg_light"])
            bordered_img = Image.new('RGB', (254, 154), self.colors["border"])
            bordered_img.paste(img, (2, 2))

            photo = ctk.CTkImage(
                light_image=bordered_img,
                dark_image=bordered_img,
                size=(254, 154)
            )
            self.image_label.configure(image=photo, text="")

    def add_to_cart(self):
        if self.on_add_to_cart:
            self.on_add_to_cart(self.product_data)