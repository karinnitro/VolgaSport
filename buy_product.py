import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
from styles import configure_styles


class ProductPurchaseWindow:
    def __init__(self, parent, product_info):
        self.parent = parent
        self.product_info = product_info
        
        self.purchase_window = tk.Toplevel(parent)
        self.purchase_window.title("Покупка товара")
        self.purchase_window.geometry("600x500")
        self.purchase_window.resizable(False, False)
        self.purchase_window.configure(bg='#D9EBFF')
        
        # Применяем стили
        self.style = configure_styles(self.purchase_window)
        
        # Основной фрейм
        self.main_frame = ttk.Frame(self.purchase_window, style='TFrame')
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Заголовок
        ttk.Label(
            self.main_frame, 
            text="Оформление покупки", 
            style='Header.TLabel'
        ).pack(pady=10)
        
        # Информация о товаре
        self.create_product_info_section()
        
        # Поля для ввода данных
        self.create_input_fields()
        
        # Кнопки
        self.create_buttons()
        
        # Подключение к базе данных
        self.conn = sqlite3.connect('sports_store.db')
        self.cursor = self.conn.cursor()
        
        # Создание таблицы покупок, если не существует
        self.create_purchases_table()
    
    def center_window(self, width, height):
        screen_width = self.purchase_window.winfo_screenwidth()
        screen_height = self.purchase_window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.purchase_window.geometry(f'{width}x{height}+{x}+{y}')
    
    def configure_styles(self):
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('Header.TLabel', 
                           font=('Arial', 18, 'bold'), 
                           foreground=self.text_color, 
                           background=self.bg_color)
        self.style.configure('ProductInfo.TLabel', 
                           font=('Arial', 12), 
                           foreground=self.text_color, 
                           background=self.bg_color)
        self.style.configure('Price.TLabel',
                           font=('Arial', 14, 'bold'),
                           foreground=self.price_color,
                           background=self.bg_color)
        self.style.configure('TLabel', 
                           font=('Arial', 11), 
                           foreground=self.text_color, 
                           background=self.bg_color)
        self.style.configure('TEntry', 
                           font=('Arial', 11), 
                           padding=5)
        self.style.configure('Buy.TButton', 
                           font=('Arial', 12, 'bold'), 
                           foreground='white', 
                           background=self.button_color, 
                           padding=8)
        self.style.map('Buy.TButton', 
                      background=[('active', self.button_hover), 
                                 ('!active', self.button_color)])
    
    def create_product_info_section(self):
        # Фрейм для информации о товаре
        product_frame = ttk.Frame(self.main_frame, style='TFrame')
        product_frame.pack(fill='x', pady=10)
        
        # Название товара
        ttk.Label(
            product_frame, 
            text=f"Товар: {self.product_info[0]}", 
            style='ProductInfo.TLabel'
        ).pack(anchor='w')
        
        # Категория
        ttk.Label(
            product_frame, 
            text=f"Категория: {self.product_info[1]}", 
            style='ProductInfo.TLabel'
        ).pack(anchor='w')
        
        # Цена
        ttk.Label(
            product_frame, 
            text=f"Цена: {self.product_info[2]} руб.", 
            style='Price.TLabel'
        ).pack(anchor='w', pady=5)
        
        # Описание
        ttk.Label(
            product_frame, 
            text=f"Описание: {self.product_info[4]}", 
            style='ProductInfo.TLabel'
        ).pack(anchor='w')
    
    def create_input_fields(self):
        # Фрейм для полей ввода
        input_frame = ttk.Frame(self.main_frame, style='TFrame')
        input_frame.pack(fill='x', pady=20)
        
        # Имя покупателя
        ttk.Label(
            input_frame, 
            text="Ваше имя:", 
            style='TLabel'
        ).grid(row=0, column=0, padx=5, pady=5, sticky='w')
        
        self.customer_name_entry = ttk.Entry(input_frame, width=30)
        self.customer_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        # Email покупателя
        ttk.Label(
            input_frame, 
            text="Ваш email:", 
            style='TLabel'
        ).grid(row=1, column=0, padx=5, pady=5, sticky='w')
        
        self.customer_email_entry = ttk.Entry(input_frame, width=30)
        self.customer_email_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        
        # Телефон покупателя
        ttk.Label(
            input_frame, 
            text="Ваш телефон:", 
            style='TLabel'
        ).grid(row=2, column=0, padx=5, pady=5, sticky='w')
        
        self.customer_phone_entry = ttk.Entry(input_frame, width=30)
        self.customer_phone_entry.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        
        # Количество товара
        ttk.Label(
            input_frame, 
            text="Количество:", 
            style='TLabel'
        ).grid(row=3, column=0, padx=5, pady=5, sticky='w')
        
        self.quantity_entry = ttk.Spinbox(input_frame, from_=1, to=100, width=5)
        self.quantity_entry.set(1)  # Значение по умолчанию
        self.quantity_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        
        # Способ доставки
        ttk.Label(
            input_frame, 
            text="Способ доставки:", 
            style='TLabel'
        ).grid(row=4, column=0, padx=5, pady=5, sticky='w')
        
        self.delivery_var = tk.StringVar()
        self.delivery_combobox = ttk.Combobox(
            input_frame, 
            textvariable=self.delivery_var,
            values=["Самовывоз", "Курьером", "Почта России"],
            state="readonly",
            width=27
        )
        self.delivery_combobox.current(0)
        self.delivery_combobox.grid(row=4, column=1, padx=5, pady=5, sticky='w')
        
        # Настройка расширения колонок
        input_frame.columnconfigure(1, weight=1)
    
    def create_buttons(self):
        # Фрейм для кнопок
        button_frame = ttk.Frame(self.main_frame, style='TFrame')
        button_frame.pack(fill='x', pady=10)
        
        # Кнопка подтверждения покупки
        ttk.Button(
            button_frame,
            text="Подтвердить покупку",
            command=self.confirm_purchase,
            style='Buy.TButton'
        ).pack(side='left', padx=5, ipady=5, ipadx=10)
        
        # Кнопка отмены
        ttk.Button(
            button_frame,
            text="Отмена",
            command=self.purchase_window.destroy,
            style='Buy.TButton'
        ).pack(side='right', padx=5, ipady=5, ipadx=10)
    
    def create_purchases_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS purchases
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            product_name TEXT NOT NULL,
                            product_category TEXT NOT NULL,
                            product_price REAL NOT NULL,
                            customer_name TEXT NOT NULL,
                            customer_email TEXT NOT NULL,
                            customer_phone TEXT NOT NULL,
                            quantity INTEGER NOT NULL,
                            delivery_method TEXT NOT NULL,
                            purchase_date TEXT NOT NULL,
                            total_amount REAL NOT NULL)''')
        self.conn.commit()
    
    def confirm_purchase(self):
        # Получение данных из полей ввода
        customer_name = self.customer_name_entry.get().strip()
        customer_email = self.customer_email_entry.get().strip()
        customer_phone = self.customer_phone_entry.get().strip()
        quantity = self.quantity_entry.get().strip()
        delivery_method = self.delivery_var.get()
        
        # Валидация данных
        if not customer_name:
            messagebox.showerror("Ошибка", "Пожалуйста, введите ваше имя")
            return
            
        if not customer_email or '@' not in customer_email:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректный email")
            return
            
        if not customer_phone or len(customer_phone) < 5:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректный телефон")
            return
            
        try:
            quantity = int(quantity)
            if quantity < 1 or quantity > 100:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Количество должно быть от 1 до 100")
            return
        
        # Расчет общей суммы
        price = float(self.product_info[2])
        total_amount = price * quantity
        
        # Дата покупки
        purchase_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Сохранение покупки в базу данных
        try:
            self.cursor.execute('''INSERT INTO purchases 
                                (product_name, product_category, product_price,
                                 customer_name, customer_email, customer_phone,
                                 quantity, delivery_method, purchase_date, total_amount)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                                (self.product_info[0], self.product_info[1], price,
                                 customer_name, customer_email, customer_phone,
                                 quantity, delivery_method, purchase_date, total_amount))
            self.conn.commit()
            
            # Показать подтверждение
            confirmation = (
                f"Покупка оформлена успешно!\n\n"
                f"Товар: {self.product_info[0]}\n"
                f"Категория: {self.product_info[1]}\n"
                f"Цена за единицу: {price} руб.\n"
                f"Количество: {quantity}\n"
                f"Общая сумма: {total_amount:.2f} руб.\n"
                f"Способ доставки: {delivery_method}\n"
                f"Дата покупки: {purchase_date}\n\n"
                f"Спасибо за покупку в нашем спортивном магазине!"
            )
            messagebox.showinfo("Покупка подтверждена", confirmation)
            
            # Закрыть окно покупки
            self.purchase_window.destroy()
            
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка базы данных", f"Не удалось сохранить данные о покупке: {e}")
    
    def __del__(self):
        # Закрытие соединения с БД при уничтожении объекта
        if hasattr(self, 'conn'):
            self.conn.close()

# Пример использования (для тестирования)
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Скрываем основное окно
    
    # Тестовые данные товара (название, категория, цена, количество, описание)
    test_product = ("Беговая дорожка ProForm", "Кардио оборудование", 45990.00, 10, 
                   "Профессиональная беговая дорожка с мощным двигателем 2.5 л.с.")
    
    # Создание окна покупки
    purchase_app = ProductPurchaseWindow(root, test_product)
    
    root.mainloop()