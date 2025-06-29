import tkinter as tk
from tkinter import ttk, messagebox, font
import sqlite3
import hashlib
from styles import configure_styles
import tkinter as tk

def create_rounded_entry(parent, width=250, height=35, radius=15, bg_color="#ffffff", border_color="#72a8fe", is_password=False):
    # Создаем фрейм-контейнер
    frame = tk.Frame(parent, bg='#f5f5f5')
    
    # Canvas для рисования
    canvas = tk.Canvas(
        frame,
        width=width,
        height=height,
        bg='#f5f5f5',
        highlightthickness=0
    )
    canvas.pack()

    # 1. Рисуем полную белую заливку (овал + прямоугольник)
    # Левый полукруг с заливкой
    canvas.create_oval(
        0, 0,
        radius*2, height,
        outline='',  # Без контура
        fill=bg_color
    )
    # Правый полукруг с заливкой
    canvas.create_oval(
        width-radius*2, 0,
        width, height,
        outline='',
        fill=bg_color
    )
    # Центральный прямоугольник
    canvas.create_rectangle(
        radius, 0,
        width-radius, height,
        outline='',
        fill=bg_color
    )

    # 2. Рисуем границы поверх заливки
    # Левый полукруг (только контур)
    canvas.create_arc(
        0, 0,
        radius*2, height,
        start=90, extent=180,
        outline=border_color,
        fill='',
        width=1.5,
        style="arc"
    )
    # Правый полукруг (только контур)
    canvas.create_arc(
        width-radius*2, 0,
        width, height,
        start=270, extent=180,
        outline=border_color,
        fill='',
        width=1.5,
        style="arc"
    )
    # Верхняя граница
    canvas.create_line(
        radius, 0,
        width-radius, 0,
        fill=border_color,
        width=1
    )
    # Нижняя граница
    canvas.create_line(
        radius, height,
        width-radius, height,
        fill=border_color,
        width=2
    )

    # Поле ввода
    entry = tk.Entry(
        frame,
        bd=0,
        bg=bg_color,
        font=('Segoe UI', 14),
        highlightthickness=0,
        relief='flat',
        show='*' if is_password else ''  # По умолчанию звездочки для пароля
    )
    entry.place(x=radius+5, y=height//2-10, width=width-radius*2-10, height=20)
    
    # Добавляем кнопку показа пароля только для полей пароля
    if is_password:
        def toggle_password():
            if entry.cget('show') == '*':
                entry.config(show='')
                eye_btn.config(text='🔒')  # Пароль виден - показываем "скрыть"
            else:
                entry.config(show='*')
                eye_btn.config(text='🔓')  # Пароль скрыт - показываем "показать"
        
        eye_btn = tk.Button(
            frame,
            text='🔓',  # Начальное состояние - "показать" (пароль скрыт)
            font=('Segoe UI', 10),
            command=toggle_password,
            bg=bg_color,
            bd=0,
            relief='flat',
            activebackground=bg_color
        )
        eye_btn.place(x=width-30, y=height//2-10, width=25, height=20)
    return frame, entry

def init_db():
    '''Настройка базы данных'''
    conn = sqlite3.connect('sports_store.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            loyalty_points INTEGER DEFAULT 0)''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            description TEXT)''')
    conn.commit()
    conn.close()


def hash_password(password):
    '''Хэширование пароля'''
    return hashlib.sha256(password.encode()).hexdigest()


def delete_account():
    def confirm_delete():
        username = username_entry.get()
        password = password_entry.get()
        if not username or not password:
            messagebox.showerror("Ошибка", "Введите логин и пароль!")
            return
        conn = sqlite3.connect('sports_store.db')
        cursor = conn.cursor()
        cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()

        if result and hash_password(password) == result[0]:
            try:
                cursor.execute('DELETE FROM users WHERE username = ?', (username,))
                conn.commit()
                messagebox.showinfo("Успех", "Аккаунт успешно удален!")
                delete_window.destroy()
            except sqlite3.Error as e:
                messagebox.showerror("Ошибка", f"Ошибка базы данных: {e}")
            finally:
                conn.close()
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль!")
            conn.close()

    # Создаём окно с новыми размерами
    delete_window = tk.Toplevel(root)
    delete_window.title("Удаление аккаунта")
    delete_window.geometry("500x400")  # Новый размер
    delete_window.minsize(400, 300)    # Минимальный размер меньше, чем geometry
    delete_window.resizable(False, False)  # Фиксируем размер
    delete_window.configure(bg='#f5f5f5')

    # Центрирование (обновлённые координаты)
    window_width = 500
    window_height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    delete_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    # Главный фрейм с уменьшенными отступами
    main_frame = tk.Frame(delete_window, bg='#f5f5f5')
    main_frame.pack(expand=True, fill='both', padx=40, pady=40)  # Уменьшено с padx=100

    # Заголовок
    header = ttk.Label(
        main_frame,
        text="Удаление аккаунта",
        style='Large.TLabel',
        font=('Poppins', 18, 'bold'),
        foreground="#478dff"
    )
    header.pack(pady=(5, 20))  # Уменьшен отступ

    # Поля ввода
    ttk.Label(main_frame, text="Логин:", style='Large.TLabel').pack(pady=3)
    username_canvas, username_entry = create_rounded_entry(main_frame)
    username_canvas.pack(pady=3)

    ttk.Label(main_frame, text="Пароль:", style='Large.TLabel').pack(pady=3)
    password_canvas, password_entry = create_rounded_entry(main_frame, is_password=True)
    password_canvas.pack(pady=3)

    # Кнопки
    buttons_frame = ttk.Frame(main_frame, style='TFrame')
    buttons_frame.pack(pady=20)

    ttk.Button(buttons_frame, text="Удалить", command=confirm_delete, style='Large.TButton').pack(side='left', padx=10)
    ttk.Button(buttons_frame, text="Отмена", command=delete_window.destroy, style='Large.TButton').pack(side='left', padx=10)
def register():
    '''Регистрация пользователя'''
    original_button_style = ttk.Style().lookup('Large.TButton', 'font')
    def register_user():
        username = new_username_entry.get()
        password = new_password_entry.get()
        confirm_password = confirm_password_entry.get()
        if not username or not password:
            messagebox.showerror("Ошибка", "Логин и пароль не могут быть пустыми!")
            return
        if password != confirm_password:
            messagebox.showerror("Ошибка", "Пароли не совпадают!")
            return
        
        conn = sqlite3.connect('sports_store.db')
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT 1 FROM users WHERE username = ?', (username,))
            if cursor.fetchone():
                messagebox.showerror("Ошибка", "Пользователь уже существует!")
                return
            
            hashed_password = hash_password(password)
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                         (username, hashed_password))
            conn.commit()
            messagebox.showinfo("Успех", "Регистрация прошла успешно!\nВы получили 100 бонусных баллов!")
            register_window.destroy()
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка базы данных: {e}")
        finally:
            conn.close()

    # Создаем окно регистрации
    register_window = tk.Toplevel(root)
    register_window.title("Регистрация в VolgaShop")
    register_window.geometry("500x600")
    register_window.minsize(500, 600)
    register_window.configure(bg='#f5f5f5')

    style = configure_styles(root)
    
    # Центрирование окна
    window_width = 500
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    register_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    # Настройка стилей с увеличенным шрифтом для кнопки
    style = ttk.Style(register_window)
    style.theme_use('clam')
    style.configure('TFrame', background='#f5f5f5')
    style.configure('TLabel', background='#f5f5f5', foreground='#333333', font=('Segoe UI', 12))
    style.configure('Large.TLabel', font=('Segoe UI', 14), background='#f5f5f5', foreground='#333333')
    
    # Новый стиль для кнопки регистрации - меньшая кнопка с большим шрифтом
    style.configure('Register.TButton', 
                   font=('Segoe UI', 16, 'bold'),  # Увеличенный шрифт
                   padding=6,                     # Меньший отступ (было 10)
                   background="#72a8fe", 
                   foreground='white')

    # Главный фрейм
    main_frame = ttk.Frame(register_window, style='TFrame')
    main_frame.pack(expand=True, fill='both', padx=100, pady=50)

    # Добавляем заголовок "Регистрация" (новый код)
    registration_label = ttk.Label(
        main_frame,
        text="Регистрация",
        style='Large.TLabel',
        font=('Poppins', 18, 'bold'),
        foreground="#478dff"
    )
    registration_label.pack(pady=(0, 20))  # Отступ снизу 20 пикселей

    # Поля ввода с закругленными краями
    ttk.Label(main_frame, text="Логин:", style='Large.TLabel').pack(pady=5)
    username_canvas, new_username_entry = create_rounded_entry(main_frame)
    username_canvas.pack(pady=5)

    ttk.Label(main_frame, text="Пароль:", style='Large.TLabel').pack(pady=5)
    password_canvas, new_password_entry = create_rounded_entry(main_frame, is_password=True)
    password_canvas.pack(pady=5)

    ttk.Label(main_frame, text="Повторите пароль:", style='Large.TLabel').pack(pady=5)
    confirm_canvas, confirm_password_entry = create_rounded_entry(main_frame, is_password=True)
    confirm_canvas.pack(pady=5)

    # Кнопка регистрации
    register_btn = ttk.Button(
        main_frame,
        text="Зарегистрироваться",
        command=register_user,
        style='Register.TButton'
    )
    register_btn.pack(pady=20, ipady=8, ipadx=20,)
    
def login():
    '''Авторизация'''
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showerror("Ошибка", "Введите логин и пароль!")
        return

    conn = sqlite3.connect('sports_store.db')
    cursor = conn.cursor()
    cursor.execute(
        'SELECT password FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()
    conn.close()

    if result and hash_password(password) == result[0]:
        root.destroy()  # Закрываем окно авторизации
        import catalog  # Импортируем модуль спортивного магазина
        catalog.show_store_window(username)  # Открываем окно магазина
    else:
        messagebox.showerror("Ошибка", "Пользователь не зарегистрирован или неверный пароль!")

def on_enter_pressed(event):
    '''Обработчик нажатия Enter'''
    login()

# Главное окно
root = tk.Tk()
root.title("Авторизация в VolgaShop")
root.geometry("1080x600")
root.minsize(1080, 720)
root.configure(bg="#D9EBFF")

# Центрирование главного окна
window_width = 800
window_height = 700
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width/2 - window_width/2)
center_y = int(screen_height/2 - window_height/2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

# Настройка стилей для крупных элементов
style = ttk.Style(root)
style.theme_use('clam')

# Настройка стилей
style.configure('TFrame', background='#f5f5f5')
style.configure('TLabel', background='#f5f5f5',
                foreground='#333333', font=('Segoe UI', 12))
style.configure('Large.TLabel', font=('Segoe UI', 14),
                background='#f5f5f5', foreground='#333333')
style.configure('Large.TEntry', font=('Segoe UI', 12), padding=8, bordercolor='#cccccc',
                lightcolor='#cccccc', darkcolor='#cccccc', relief='flat')
style.map('Large.TEntry',
          fieldbackground=[('active', '#ffffff'), ('!disabled', '#ffffff')],
          foreground=[('active', '#333333'), ('!disabled', '#333333')])

style.configure('Large.TButton', font=('Segoe UI', 14, 'bold'), padding=6,
                background="#72a8fe", foreground='white', borderwidth=0,
                focusthickness=3, focuscolor='#72a8fe')
style.map('Large.TButton',
          background=[('active', '#72a8fe'), ('!disabled', '#72a8fe')],
          foreground=[('active', 'white'), ('!disabled', 'white')])

# Основной фрейм для центрирования содержимого
main_frame = ttk.Frame(root, style='TFrame')
main_frame.pack(expand=True, fill='both', padx=150, pady=150)

# Заголовок
header = ttk.Label(
    main_frame,
    text="VolgaShop",
    style='Large.TLabel',
    font=('Poppins', 18, 'bold'),
    foreground="#478dff")
header.pack(pady=(5, 2))

# Подзаголовок "Спортивный магазин"
subheader = ttk.Label(
    main_frame,
    text="Спортивный магазин",
    style='Large.TLabel',
    font=('Poppins', 14),  # Меньший размер шрифта
    foreground="#636363"  # Более темный серый цвет
)
subheader.pack(pady=(0,10))  # Отступ снизу 20px перед полями ввода

# Поля для ввода
ttk.Label(main_frame, text="Логин:", style='Large.TLabel').pack(pady=3)
username_canvas, username_entry = create_rounded_entry(main_frame)
username_canvas.pack(pady=3)

ttk.Label(main_frame, text="Пароль:", style='Large.TLabel').pack(pady=3)
password_canvas, password_entry = create_rounded_entry(main_frame, is_password=True)
password_canvas.pack(pady=3)

username_entry.bind('<Return>', on_enter_pressed)
password_entry.bind('<Return>', on_enter_pressed)

# Кнопки
buttons_frame = ttk.Frame(main_frame, style='TFrame')
buttons_frame.pack(pady=20)

ttk.Button(buttons_frame, text="Войти", command=login,
           style='Large.TButton').pack(side='left', padx=10, ipady=8, ipadx=20)
ttk.Button(buttons_frame, text="Регистрация", command=register,
           style='Large.TButton').pack(side='left', padx=10, ipady=8, ipadx=20)
ttk.Button(buttons_frame, text="Удалить аккаунт", command=delete_account,
           style='Large.TButton').pack(side='left', padx=10, ipady=8, ipadx=20)

init_db()
root.mainloop()
