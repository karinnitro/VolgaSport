import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from buy_product import ProductPurchaseWindow
from review_window import ProductReviewWindow
from view_reviews import ViewProductReviewsWindow
from styles import configure_styles


class CustomerStatisticsWindow:
    def __init__(self, parent, username):
        self.username = username
        self.parent = parent
        
        # Создаем окно
        self.window = tk.Toplevel(parent)
        self.window.title(f"Статистика покупателя - {username}")
        self.window.geometry("600x400")
        self.window.configure(bg="#c6e3ff")
        self.center_window(600, 400)
        self.window.resizable(False, False)

        # Стили
        style = ttk.Style(self.window)
        style.theme_use('clam')
        style.configure('TFrame', background="#e0e6f5")
        style.configure('TLabel', background="#e0e6f5", foreground="#000000", font=('Helvetica', 12))
        style.configure('Large.TLabel', font=('Segoe UI', 16, 'bold'), background='#e0e6f5', foreground='#1a3e72')

        # Основной фрейм
        main_frame = ttk.Frame(self.window, style='TFrame')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Заголовок
        ttk.Label(main_frame, text=f"{username}", style='Large.TLabel').pack(pady=10)

        # Получение статистики
        self.load_statistics(main_frame)

        # Закрытие окна
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

    def center_window(self, width, height):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.window.geometry(f'{width}x{height}+{x}+{y}')

    def load_statistics(self, frame):
        conn = sqlite3.connect('sports_store.db')
        cursor = conn.cursor()
        
        # Количество купленных товаров
        cursor.execute('''SELECT COUNT(DISTINCT product_id) FROM reviews WHERE username=?''', (self.username,))
        purchased_products_count = cursor.fetchone()[0]
        
        # Самый популярный товар у покупателя
        cursor.execute('''SELECT p.name, COUNT(*) as review_count FROM reviews r
                        JOIN products p ON r.product_id = p.id
                        WHERE r.username=? GROUP BY p.name ORDER BY review_count DESC LIMIT 1''', (self.username,))
        favorite_product = cursor.fetchone()
        favorite_product_name = favorite_product[0] if favorite_product else "Нет отзывов"
        
        # Общая сумма покупок
        cursor.execute('''SELECT SUM(total_amount) FROM purchases WHERE customer_email = 
                         (SELECT email FROM users WHERE username=?)''', (self.username,))
        total_spent = cursor.fetchone()[0] or 0
        
        # Отображаем статистику
        ttk.Label(frame, text=f"Количество купленных товаров: {purchased_products_count}", 
                 font=('Segoe UI', 14)).pack(pady=5)
        ttk.Label(frame, text=f"Самый популярный товар: {favorite_product_name}", 
                 font=('Segoe UI', 14)).pack(pady=5)
        ttk.Label(frame, text=f"Общая сумма покупок: {total_spent:.2f} руб.", 
                 font=('Segoe UI', 14)).pack(pady=5)
        conn.close()

    def on_close(self):
        self.window.destroy()

def init_store_db():
    conn = sqlite3.connect('sports_store.db')
    cursor = conn.cursor()

    # Таблица пользователей
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        loyalty_points INTEGER DEFAULT 0
    )''')

    # Таблица товаров
    cursor.execute('''CREATE TABLE IF NOT EXISTS products
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    price REAL NOT NULL,
                    quantity INTEGER NOT NULL,
                    description TEXT)
                   
            ''')

    # Таблица отзывов
    cursor.execute('''CREATE TABLE IF NOT EXISTS reviews
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id INTEGER NOT NULL,
                    username TEXT NOT NULL,
                    rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
                    comment TEXT,
                    review_date TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (product_id) REFERENCES products(id))''')

    # Таблица покупок
    cursor.execute('''CREATE TABLE IF NOT EXISTS purchases
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

    # Тестовые данные
    if cursor.execute("SELECT COUNT(*) FROM products").fetchone()[0] == 0:
        test_products = [
            ('Беговая дорожка ProForm', 'Кардио оборудование', 45990.00, 10, 
             'Профессиональная беговая дорожка с мощным двигателем 2.5 л.с.', 'images/velosiped.jpg'),
            ('Гантели наборные 20 кг', 'Силовое оборудование', 3490.00, 25,
             'Наборные гантели с неопреновым покрытием, максимальный вес 20 кг'),
            ('Футбольный мяч Adidas', 'Спортивные товары', 2490.00, 30,
             'Официальный мяч для матчей, размер 5'),
            ('Штаны спортивные Kappa', 'Спортивная одежда', 1490.00, 10,
             'Штаны мужские оригинал Kappa')
        ]
        cursor.executemany("INSERT INTO products VALUES (NULL,?,?,?,?,?)", test_products)
        conn.commit()

    conn.commit()
    conn.close()

def show_purchased_products():
    purchased_window = tk.Toplevel()
    purchased_window.title("История покупок")
    purchased_window.geometry("1000x600")
    purchased_window.minsize(1000, 600)
    purchased_window.configure(bg='#f0f5ff')

    # Центрирование окна
    window_width = 1000
    window_height = 600
    screen_width = purchased_window.winfo_screenwidth()
    screen_height = purchased_window.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    purchased_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    style = ttk.Style(purchased_window)
    style.theme_use('clam')

    style.configure('TFrame', background='#f0f5ff')
    style.configure('TLabel', background='#f0f5ff', foreground='#333333', font=('Segoe UI', 12))
    style.configure('Large.TLabel', font=('Segoe UI', 14), background='#f0f5ff', foreground='#1a3e72')

    main_frame = ttk.Frame(purchased_window, style='TFrame')
    main_frame.pack(expand=True, fill='both', padx=20, pady=20)

    ttk.Label(main_frame, text="История покупок:", style='Large.TLabel').pack(pady=10)

    columns = ('product_name', 'product_category', 'quantity', 'total_amount', 'purchase_date', 'delivery_method')
    tree = ttk.Treeview(main_frame, columns=columns, show='headings')
    tree.heading('product_name', text='Товар')
    tree.heading('product_category', text='Категория')
    tree.heading('quantity', text='Количество')
    tree.heading('total_amount', text='Сумма')
    tree.heading('purchase_date', text='Дата покупки')
    tree.heading('delivery_method', text='Доставка')

    # Измените эти строки:
    tree.column('product_name', width=250, anchor='center')    # Было 'w'
    tree.column('product_category', width=150, anchor='center') # Было 'w'
    tree.column('quantity', width=80, anchor='center')         # Уже было 'center'
    tree.column('total_amount', width=100, anchor='center')    # Было 'e'
    tree.column('purchase_date', width=120, anchor='center')   # Уже было 'center'
    tree.column('delivery_method', width=150, anchor='center') # Было 'w'

    # Добавьте для выравнивания заголовков:
    style.configure('Treeview.Heading', anchor='center')

    tree.pack(fill='both', expand=True)

    try:
        conn = sqlite3.connect('sports_store.db')
        cursor = conn.cursor()
        cursor.execute('SELECT product_name, product_category, quantity, total_amount, purchase_date, delivery_method FROM purchases')
        rows = cursor.fetchall()
    except sqlite3.Error as e:
        messagebox.showerror("Ошибка", f"Ошибка базы данных: {e}")
        rows = []
    finally:
        conn.close()

    for row in rows:
        tree.insert('', 'end', values=row)

def show_store_window(username):
    init_store_db()

    # Создание окна
    store_window = tk.Tk()
    store_window.title(f"VolgaShop - Добро пожаловать, {username}")
    store_window.geometry("1600x900")
    store_window.configure(bg="#D9EBFF")  # Изменен цвет фона
    store_window.resizable(False, False)  

    # Подключение БД
    conn = sqlite3.connect('sports_store.db')
    cursor = conn.cursor()

    # Стили - полная переработка под единый стиль
    style = ttk.Style()
    style.theme_use('clam')  # Изменена тема
    
    # Основные настройки стиля
    style.configure('.', font=('Segoe UI', 12))
    style.configure('TFrame', background='#f5f5f5')
    
    # Стили для таблицы (как в первом варианте)
    style.configure('Treeview',
                    background="#ffffff",
                    foreground="#333333",
                    rowheight=35,
                    fieldbackground='#ffffff',
                    font=('Segoe UI', 12))  # Изменен шрифт
    style.configure('Treeview.Heading',
                    background="#72a8fe",  # Изменен цвет
                    foreground='white',
                    font=('Segoe UI', 12, 'bold'))  # Изменен шрифт
    style.map('Treeview',
              background=[('selected', "#478dff")],  # Изменен цвет выделения
              foreground=[('selected', 'white')])

    # Стили для кнопок (как в первом варианте)
    style.configure('TButton',
                    font=('Segoe UI', 12),
                    padding=8,
                    relief='flat',
                    background="#72a8fe",  # Изменен цвет
                    foreground='white')
    style.map('TButton',
              background=[('active', '#478dff')],  # Изменен цвет активности
              foreground=[('active', 'white')])

    # Основной интерфейс
    main_frame = ttk.Frame(store_window, style='TFrame')
    main_frame.pack(expand=True, fill='both', padx=20, pady=20)

    # Таблица товаров (оставляем как есть)
    columns = ('name', 'category', 'price', 'quantity', 'rating', 'status')
    tree = ttk.Treeview(main_frame, columns=columns, show='headings')
    
    # Настройка заголовков (можно оставить как есть)
    tree.heading('name', text='Название')
    tree.heading('category', text='Категория') 
    tree.heading('price', text='Цена')
    tree.heading('quantity', text='Наличие')
    tree.heading('rating', text='Рейтинг')
    tree.heading('status', text='Статус')

    # Добавьте эти строки для настройки выравнивания столбцов:
    tree.column('name', anchor='center', width=250)      # Выравнивание по центру
    tree.column('category', anchor='center', width=150)  # Выравнивание по центру
    tree.column('price', anchor='center', width=100)     # Выравнивание по центру
    tree.column('quantity', anchor='center', width=80)   # Выравнивание по центру
    tree.column('rating', anchor='center', width=100)    # Выравнивание по центру
    tree.column('status', anchor='center', width=120)    # Выравнивание по центру

    # Добавьте эту строку для выравнивания заголовков по центру:
    style.configure('Treeview.Heading', anchor='center')

    tree.pack(expand=True, fill='both')

    # Загрузка товаров
    def load_products():
        tree.delete(*tree.get_children())
        cursor.execute('''SELECT p.id, p.name, p.category, p.price, p.quantity, 
                        ROUND(AVG(r.rating),1) FROM products p
                        LEFT JOIN reviews r ON p.id=r.product_id
                        GROUP BY p.id''')
        products = cursor.fetchall()

        for product in products:
            product_id, name, category, price, quantity, avg_rating = product
            status = "В наличии" if quantity > 0 else "Нет в наличии"
            rating = f"{avg_rating}" if avg_rating else "—"
            tree.insert('', 'end', values=(name, category, f"{price:.2f} руб.", quantity, rating, status))

    def get_selected_product_info():
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите товар")
            return None
        product_data = tree.item(selected)['values']
        return (product_data[0], product_data[1], product_data[2], product_data[5])  # name, category, price, status

    def on_add_review():
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите товар")
            return
        product_name = tree.item(selected)['values'][0]
        if product_id := cursor.execute("SELECT id FROM products WHERE name=?", 
                                      (product_name,)).fetchone():
            ProductReviewWindow(store_window, product_id[0], product_name, username)

    def on_view_reviews():
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите товар")
            return
        product_name = tree.item(selected)['values'][0]
        if product_id := cursor.execute("SELECT id FROM products WHERE name=?", 
                                      (product_name,)).fetchone():
            ViewProductReviewsWindow(store_window, product_id[0], product_name)

    def on_purchase():
        product_info = get_selected_product_info()
        if not product_info:
            return
        name, category, price, status = product_info
        if status == "Нет в наличии":
            messagebox.showinfo("Недоступно", "Этот товар отсутствует в наличии")
            return
        
        # Получаем данные о товаре для ProductPurchaseWindow
        cursor.execute("SELECT name, category, price, quantity, description FROM products WHERE name=?", (name,))
        product_data = cursor.fetchone()
        if product_data:
            ProductPurchaseWindow(store_window, product_data, callback=load_products)

    # Панель кнопок
    button_frame = ttk.Frame(main_frame, style='TFrame')
    button_frame.pack(fill='x', pady=10)

    ttk.Button(button_frame, text="Оставить отзыв", command=on_add_review).pack(side='left', padx=5)
    ttk.Button(button_frame, text="Просмотреть отзывы", command=on_view_reviews).pack(side='left', padx=5)
    ttk.Button(button_frame, text="Купить", command=on_purchase).pack(side='left', padx=5)
    ttk.Button(button_frame, text="История покупок", command=show_purchased_products).pack(side='left', padx=5)
    ttk.Button(button_frame, text="Статистика", command=lambda: CustomerStatisticsWindow(store_window, username)).pack(side='left', padx=5)
    ttk.Button(button_frame, text="Обновить", command=load_products).pack(side='right', padx=5)
    ttk.Button(button_frame, text="Выйти", command=store_window.destroy).pack(side='right', padx=5)

    load_products()

    def on_close():
        conn.close()
        store_window.destroy()

    store_window.protocol("WM_DELETE_WINDOW", on_close)
    store_window.mainloop()

if __name__ == "__main__":
    show_store_window("Администратор")