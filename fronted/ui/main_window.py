import customtkinter as ctk
from .product_cards import ProductCard
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_client import OpticStoreAPI

import tkinter.messagebox as messagebox
import json


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Кастомная цветовая палитра
        self.colors = {
            "bg_dark": "#121212",  # Основной темный фон
            "bg_card": "#1E1E1E",  # Фон карточек
            "bg_sidebar": "#1A1A1A",  # Фон боковой панели
            "bg_light": "#2D2D2D",  # Светлый фон элементов
            "accent_primary": "#FF6B35",  # Основной акцент (оранжевый)
            "accent_secondary": "#4ECDC4",  # Вторичный акцент (бирюзовый)
            "accent_success": "#4CAF50",  # Успех (зеленый)
            "accent_warning": "#FF9800",  # Предупреждение (оранжевый)
            "accent_danger": "#F44336",  # Ошибка (красный)
            "text_primary": "#FFFFFF",  # Основной текст
            "text_secondary": "#B0B0B0",  # Вторичный текст
            "text_muted": "#808080",  # Приглушенный текст
            "border": "#333333",  # Цвет границ
            "hover": "#2A2A2A",  # Цвет при наведении
            "rating": "#FFD700",  # Цвет рейтинга (золотой)
        }

        # Настройка окна
        self.title("RU Optic Store - Магазин оптических прицелов")
        self.geometry("1400x800")

        # Настройка темы
        ctk.set_appearance_mode("dark")

        # Устанавливаем кастомные цвета для элементов
        ctk.set_widget_scaling(1.0)
        ctk.set_window_scaling(1.0)

        # API клиент
        self.api = OpticStoreAPI()

        # Корзина
        self.cart = []
        self.cart_window = None

        self.setup_ui()
        self.load_products()

    def setup_ui(self):
        # Создаем сетку
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Устанавливаем цвет фона окна
        self.configure(fg_color=self.colors["bg_dark"])

        # Левая панель (фильтры)
        self.sidebar = ctk.CTkFrame(
            self,
            width=250,
            corner_radius=0,
            fg_color=self.colors["bg_sidebar"],
            border_color=self.colors["border"],
            border_width=1
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # Логотип/заголовок
        self.logo_label = ctk.CTkLabel(
            self.sidebar,
            text="🔭 RU Optic Store",
            font=("Arial", 26, "bold"),
            text_color=self.colors["accent_primary"]
        )
        self.logo_label.pack(pady=(25, 30))

        # Кнопка корзины
        self.cart_button = ctk.CTkButton(
            self.sidebar,
            text="🛒 Корзина (0)",
            command=self.open_cart,
            height=45,
            font=("Arial", 14, "bold"),
            fg_color=self.colors["accent_primary"],
            hover_color=self.colors["accent_warning"],
            text_color=self.colors["text_primary"],
            corner_radius=10
        )
        self.cart_button.pack(pady=10, padx=20, fill="x")

        # Фильтры
        self.filters_label = ctk.CTkLabel(
            self.sidebar,
            text="ФИЛЬТРЫ",
            font=("Arial", 16, "bold"),
            text_color=self.colors["text_secondary"]
        )
        self.filters_label.pack(pady=(25, 15))

        # Категории
        self.category_label = ctk.CTkLabel(
            self.sidebar,
            text="Категория:",
            text_color=self.colors["text_secondary"],
            font=("Arial", 12)
        )
        self.category_label.pack(anchor="w", padx=20, pady=(10, 5))

        self.category_var = ctk.StringVar(value="Все")
        self.category_menu = ctk.CTkOptionMenu(
            self.sidebar,
            values=["Все"],
            variable=self.category_var,
            command=self.apply_filters,
            fg_color=self.colors["bg_light"],
            button_color=self.colors["accent_primary"],
            button_hover_color=self.colors["accent_warning"],
            text_color=self.colors["text_primary"],
            dropdown_fg_color=self.colors["bg_light"],
            dropdown_text_color=self.colors["text_primary"],
            dropdown_hover_color=self.colors["hover"],
            corner_radius=8
        )
        self.category_menu.pack(pady=(0, 15), padx=20, fill="x")

        # Бренды
        self.brand_label = ctk.CTkLabel(
            self.sidebar,
            text="Бренд:",
            text_color=self.colors["text_secondary"],
            font=("Arial", 12)
        )
        self.brand_label.pack(anchor="w", padx=20, pady=(5, 5))

        self.brand_var = ctk.StringVar(value="Все")
        self.brand_menu = ctk.CTkOptionMenu(
            self.sidebar,
            values=["Все"],
            variable=self.brand_var,
            command=self.apply_filters,
            fg_color=self.colors["bg_light"],
            button_color=self.colors["accent_primary"],
            button_hover_color=self.colors["accent_warning"],
            text_color=self.colors["text_primary"],
            dropdown_fg_color=self.colors["bg_light"],
            dropdown_text_color=self.colors["text_primary"],
            dropdown_hover_color=self.colors["hover"],
            corner_radius=8
        )
        self.brand_menu.pack(pady=(0, 15), padx=20, fill="x")

        # Цена (в рублях)
        self.price_label = ctk.CTkLabel(
            self.sidebar,
            text="Цена, ₽:",
            text_color=self.colors["text_secondary"],
            font=("Arial", 12)
        )
        self.price_label.pack(anchor="w", padx=20, pady=(10, 5))

        self.price_slider = ctk.CTkSlider(
            self.sidebar,
            from_=0,
            to=500000,
            number_of_steps=50,
            command=self.on_price_slider,
            progress_color=self.colors["accent_primary"],
            button_color=self.colors["accent_primary"],
            button_hover_color=self.colors["accent_warning"]
        )
        self.price_slider.set(500000)
        self.price_slider.pack(pady=(0, 5), padx=20, fill="x")

        self.price_value_label = ctk.CTkLabel(
            self.sidebar,
            text="До: 500 000 ₽",
            text_color=self.colors["text_primary"],
            font=("Arial", 11, "bold")
        )
        self.price_value_label.pack(pady=(0, 20))

        # Только в наличии
        self.in_stock_var = ctk.BooleanVar(value=False)
        self.in_stock_check = ctk.CTkCheckBox(
            self.sidebar,
            text="Только в наличии",
            variable=self.in_stock_var,
            command=self.apply_filters,
            fg_color=self.colors["accent_primary"],
            hover_color=self.colors["accent_warning"],
            border_color=self.colors["border"],
            text_color=self.colors["text_primary"],
            corner_radius=6
        )
        self.in_stock_check.pack(pady=15, padx=20)

        # Кнопка сброса
        self.reset_button = ctk.CTkButton(
            self.sidebar,
            text="Сбросить фильтры",
            command=self.reset_filters,
            height=40,
            font=("Arial", 13),
            fg_color=self.colors["bg_light"],
            hover_color=self.colors["hover"],
            text_color=self.colors["text_primary"],
            border_color=self.colors["border"],
            border_width=1,
            corner_radius=8
        )
        self.reset_button.pack(pady=15, padx=20, fill="x")

        # Основная область (товары)
        self.main_frame = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color=self.colors["bg_dark"],
            border_color=self.colors["border"],
            border_width=1
        )
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 20), pady=20)
        self.main_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="column")
        self.main_frame.grid_rowconfigure(0, weight=1)

        # Canvas с Scrollbar для товаров
        self.canvas = ctk.CTkCanvas(
            self.main_frame,
            bg=self.colors["bg_dark"],
            highlightthickness=0
        )
        self.scrollbar = ctk.CTkScrollbar(
            self.main_frame,
            orientation="vertical",
            command=self.canvas.yview,
            fg_color=self.colors["bg_light"],
            button_color=self.colors["accent_primary"],
            button_hover_color=self.colors["accent_warning"]
        )
        self.scrollable_frame = ctk.CTkFrame(
            self.canvas,
            fg_color=self.colors["bg_dark"]
        )

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=(20, 0))
        self.scrollbar.grid(row=0, column=2, sticky="ns", padx=(0, 20))

        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Загрузка категорий и брендов
        self.load_filters()

    def load_filters(self):
        """Загрузить фильтры из API"""
        categories = ["Все"] + self.api.get_categories()
        self.category_menu.configure(values=categories)

        brands = ["Все"] + self.api.get_brands()
        self.brand_menu.configure(values=brands)

    def load_products(self, **filters):
        """Загрузить товары"""
        # Очистить текущие товары
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Показать индикатор загрузки
        loading_label = ctk.CTkLabel(
            self.scrollable_frame,
            text="Загрузка товаров...",
            font=("Arial", 16),
            text_color=self.colors["text_secondary"]
        )
        loading_label.pack(pady=50)

        self.update()

        # Загрузить товары
        products = self.api.get_products(**filters)

        # Убрать индикатор
        loading_label.destroy()

        if not products:
            no_products_label = ctk.CTkLabel(
                self.scrollable_frame,
                text="Товары не найдены",
                font=("Arial", 16),
                text_color=self.colors["text_muted"]
            )
            no_products_label.pack(pady=50)
            return

        # Создаем сетку с одинаковыми ячейками
        self.scrollable_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="column")

        # Отобразить товары в сетке
        row, col = 0, 0
        max_cols = 3

        for product in products:
            card = ProductCard(
                self.scrollable_frame,
                product,
                colors=self.colors,  # Передаем цвета
                on_add_to_cart=self.add_to_cart,
                width=300,
                height=450
            )
            card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")

            col += 1
            if col >= max_cols:
                col = 0
                row += 1

        # Устанавливаем одинаковую высоту строк
        for i in range(row + 1):
            self.scrollable_frame.grid_rowconfigure(i, weight=1)

        # Обновить canvas
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def apply_filters(self, *args):
        """Применить фильтры"""
        filters = {}

        category = self.category_var.get()
        if category != "Все":
            filters["category"] = category

        brand = self.brand_var.get()
        if brand != "Все":
            filters["brand"] = brand

        max_price = self.price_slider.get()
        filters["max_price"] = max_price

        if self.in_stock_var.get():
            filters["in_stock"] = True

        self.load_products(**filters)

    def on_price_slider(self, value):
        """Обновить label при изменении слайдера"""
        formatted_value = f"{value:,.0f}".replace(",", " ")
        self.price_value_label.configure(text=f"До: {formatted_value} ₽")
        self.apply_filters()

    def reset_filters(self):
        """Сбросить все фильтры"""
        self.category_var.set("Все")
        self.brand_var.set("Все")
        self.price_slider.set(500000)
        self.price_value_label.configure(text="До: 500 000 ₽")
        self.in_stock_var.set(False)
        self.load_products()

    def add_to_cart(self, product):
        """Добавить товар в корзину"""
        # Проверить, есть ли уже в корзине
        for item in self.cart:
            if item['id'] == product['id']:
                item['quantity'] += 1
                break
        else:
            product['quantity'] = 1
            self.cart.append(product)

        # Обновить кнопку корзины
        total_items = sum(item['quantity'] for item in self.cart)
        self.cart_button.configure(text=f"🛒 Корзина ({total_items})")

        messagebox.showinfo("Корзина", f"{product['name']} добавлен в корзину!")

    def open_cart(self):
        """Открыть окно корзины"""
        if self.cart:
            if not hasattr(self, 'cart_window') or self.cart_window is None or not self.cart_window.winfo_exists():
                self.cart_window = CartWindow(self)
                self.cart_window.focus()
        else:
            messagebox.showinfo("Корзина", "Корзина пуста!")

    def update_cart_display(self):
        """Обновить отображение корзины в основном окне"""
        total_items = sum(item.get('quantity', 1) for item in self.cart)
        self.cart_button.configure(text=f"🛒 Корзина ({total_items})")


class CartWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)

        self.master = master
        self.cart = master.cart
        self.colors = master.colors

        self.title("🛒 Корзина")
        self.geometry("600x500")

        # Настройка фона окна
        self.configure(fg_color=self.colors["bg_dark"])

        self.setup_ui()

    def setup_ui(self):
        # Заголовок
        ctk.CTkLabel(
            self,
            text="Ваша корзина",
            font=("Arial", 22, "bold"),
            text_color=self.colors["text_primary"]
        ).pack(pady=25)

        # Фрейм для товаров
        self.cart_frame = ctk.CTkScrollableFrame(
            self,
            height=300,
            fg_color=self.colors["bg_light"],
            border_color=self.colors["border"],
            border_width=1,
            corner_radius=10
        )
        self.cart_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Отобразить товары
        self.update_cart_display()

        # Итого
        total = sum(item.get('price', 0) * item.get('quantity', 1) for item in self.cart)
        formatted_total = f"{total:,.2f}".replace(",", " ")

        total_frame = ctk.CTkFrame(
            self,
            fg_color=self.colors["bg_card"],
            border_color=self.colors["border"],
            border_width=1,
            corner_radius=10
        )
        total_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            total_frame,
            text=f"Итого: {formatted_total} ₽",
            font=("Arial", 18, "bold"),
            text_color=self.colors["text_primary"]
        ).pack(pady=12)

        # Кнопки
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=20)

        ctk.CTkButton(
            button_frame,
            text="Оформить заказ",
            command=self.checkout,
            width=160,
            height=45,
            font=("Arial", 14, "bold"),
            fg_color=self.colors["accent_success"],
            hover_color="#45a049",
            text_color=self.colors["text_primary"],
            corner_radius=10
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            button_frame,
            text="Очистить корзину",
            command=self.clear_cart,
            width=160,
            height=45,
            font=("Arial", 14, "bold"),
            fg_color=self.colors["bg_light"],
            hover_color=self.colors["hover"],
            text_color=self.colors["text_primary"],
            border_color=self.colors["border"],
            border_width=1,
            corner_radius=10
        ).pack(side="left", padx=10)

    def update_cart_display(self):
        """Обновить отображение корзины"""
        for widget in self.cart_frame.winfo_children():
            widget.destroy()

        if not self.cart:
            ctk.CTkLabel(
                self.cart_frame,
                text="Корзина пуста",
                font=("Arial", 16),
                text_color=self.colors["text_muted"]
            ).pack(pady=50)
            return

        for item in self.cart:
            item_frame = ctk.CTkFrame(
                self.cart_frame,
                fg_color=self.colors["bg_card"],
                corner_radius=8,
                height=50
            )
            item_frame.pack(fill="x", pady=5, padx=5)

            # Название и количество
            ctk.CTkLabel(
                item_frame,
                text=f"{item['name']} ×{item.get('quantity', 1)}",
                font=("Arial", 13),
                text_color=self.colors["text_primary"]
            ).pack(side="left", padx=15, pady=10)

            # Цена в рублях
            price = item.get('price', 0) * item.get('quantity', 1)
            formatted_price = f"{price:,.2f}".replace(",", " ")
            ctk.CTkLabel(
                item_frame,
                text=f"{formatted_price} ₽",
                font=("Arial", 13, "bold"),
                text_color=self.colors["accent_primary"]
            ).pack(side="right", padx=15, pady=10)

    def checkout(self):
        """Оформить заказ"""
        if not self.cart:
            messagebox.showwarning("Корзина", "Корзина пуста!")
            return

        # Создаем диалог для данных клиента
        dialog = ctk.CTkInputDialog(
            text="Введите ваше имя:",
            title="Оформление заказа",
            fg_color=self.colors["bg_dark"],
            button_fg_color=self.colors["accent_primary"],
            button_hover_color=self.colors["accent_warning"],
            button_text_color=self.colors["text_primary"],
            entry_fg_color=self.colors["bg_light"],
            entry_border_color=self.colors["border"],
            entry_text_color=self.colors["text_primary"]
        )
        name = dialog.get_input()

        if not name:
            return

        # Создаем заказ
        order_data = {
            "customer_name": name,
            "items": json.dumps([
                {
                    "id": item['id'],
                    "name": item['name'],
                    "quantity": item.get('quantity', 1),
                    "price": item.get('price', 0)
                }
                for item in self.cart
            ]),
            "total_amount": sum(item.get('price', 0) * item.get('quantity', 1) for item in self.cart)
        }

        result = self.master.api.create_order(order_data)

        if "error" not in result:
            messagebox.showinfo("Успех", "Заказ оформлен!")
            self.clear_cart()
            self.destroy()
        else:
            messagebox.showerror("Ошибка", f"Не удалось оформить заказ: {result['error']}")

    def clear_cart(self):
        """Очистить корзину"""
        self.cart.clear()
        self.master.cart.clear()
        self.update_cart_display()
        self.master.update_cart_display()