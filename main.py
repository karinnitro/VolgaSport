import tkinter as tk
from tkinter import ttk, messagebox, font
import sqlite3
import hashlib


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
    '''Удаление аккаунта'''
    def confirm_delete():
        username = delete_username_entry.get()
        password = delete_password_entry.get()
        if not username or not password:
            messagebox.showerror("Ошибка", "Введите логин и пароль!")
            return
        conn = sqlite3.connect('sports_store.db')
        cursor = conn.cursor()
        cursor.execute(
            'SELECT password FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()

        if result and hash_password(password) == result[0]:
            try:
                cursor.execute(
                    'DELETE FROM users WHERE username = ?', (username,))
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

    # Окно удаления аккаунта
    delete_window = tk.Toplevel(root)
    delete_window.title("Удаление аккаунта")
    delete_window.geometry("800x600")
    delete_window.minsize(800, 600)
    delete_window.configure(bg='#f5f5f5')
    # Центрирование окна
    window_width = 800
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    delete_window.geometry(
        f'{window_width}x{window_height}+{center_x}+{center_y}')

    # Стиль для крупных элементов
    style = ttk.Style(delete_window)
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
              fieldbackground=[('active', '#ffffff'),
                               ('!disabled', '#ffffff')],
              foreground=[('active', '#333333'), ('!disabled', '#333333')])
    style.configure('Large.TButton', font=('Segoe UI', 12, 'bold'), padding=10,
                    background='#6200ee', foreground='white', borderwidth=0,
                    focusthickness=3, focuscolor='#6200ee')
    style.map('Large.TButton',
              background=[('active', '#3700b3'), ('!disabled', '#6200ee')],
              foreground=[('active', 'white'), ('!disabled', 'white')])

    # Фрейм для центрирования содержимого
    main_frame = ttk.Frame(delete_window, style='TFrame')
    main_frame.pack(expand=True, fill='both', padx=100, pady=100)

    ttk.Label(main_frame, text="Введите логин для удаления:",
              style='Large.TLabel').pack(pady=10)
    delete_username_entry = ttk.Entry(main_frame, style='Large.TEntry')
    delete_username_entry.pack(pady=10, ipady=8, fill='x')

    ttk.Label(main_frame, text="Введите пароль для подтверждения:",
              style='Large.TLabel').pack(pady=10)
    delete_password_entry = ttk.Entry(
        main_frame, show="*", style='Large.TEntry')
    delete_password_entry.pack(pady=10, ipady=8, fill='x')

    # Кнопки подтверждения/отмены
    buttons_frame = ttk.Frame(main_frame, style='TFrame')
    buttons_frame.pack(pady=20)

    ttk.Button(buttons_frame, text="Удалить аккаунт",
               command=confirm_delete, style='Large.TButton').pack(side='left', padx=10, ipady=8, ipadx=20)
    ttk.Button(buttons_frame, text="Отмена",
               command=delete_window.destroy, style='Large.TButton').pack(side='left', padx=10, ipady=8, ipadx=20)

def register():
    '''Регистрация пользователя'''
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
    register_window.geometry("800x600")
    register_window.minsize(800, 600)
    register_window.configure(bg='#f5f5f5')

    # Центрирование окна
    window_width = 800
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    register_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    # Настройка стилей
    style = ttk.Style(register_window)
    style.theme_use('clam')
    style.configure('TFrame', background='#f5f5f5')
    style.configure('TLabel', background='#f5f5f5', foreground='#333333', font=('Segoe UI', 12))
    style.configure('Large.TLabel', font=('Segoe UI', 14), background='#f5f5f5', foreground='#333333')
    style.configure('Large.TEntry', font=('Segoe UI', 12), padding=8)
    style.configure('Large.TButton', font=('Segoe UI', 12, 'bold'), padding=10,
                  background='#6200ee', foreground='white')

    # Главный фрейм
    main_frame = ttk.Frame(register_window, style='TFrame')
    main_frame.pack(expand=True, fill='both', padx=100, pady=50)  # Уменьшил pady сверху

    # Поля ввода
    ttk.Label(main_frame, text="Логин:", style='Large.TLabel').pack(pady=5)
    new_username_entry = ttk.Entry(main_frame, style='Large.TEntry')
    new_username_entry.pack(pady=5, ipady=8, fill='x')

    ttk.Label(main_frame, text="Пароль:", style='Large.TLabel').pack(pady=5)
    new_password_entry = ttk.Entry(main_frame, show="*", style='Large.TEntry')
    new_password_entry.pack(pady=5, ipady=8, fill='x')

    ttk.Label(main_frame, text="Повторите пароль:", style='Large.TLabel').pack(pady=5)
    confirm_password_entry = ttk.Entry(main_frame, show="*", style='Large.TEntry')
    confirm_password_entry.pack(pady=5, ipady=8, fill='x')

    # Кнопка регистрации (теперь точно будет видна)
    register_btn = ttk.Button(
        main_frame,
        text="Зарегистрироваться",
        command=register_user,
        style='Large.TButton'
    )
    register_btn.pack(pady=20, ipady=8, ipadx=20, fill='x')  # Добавил fill='x' для растягивания
    
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
        messagebox.showerror("Ошибка", "Неверный логин или пароль!")


# Главное окно
root = tk.Tk()
root.title("Авторизация в VolgaShop")
root.geometry("1080x720")
root.minsize(1080, 720)
root.configure(bg="#D9EBFF")

# Центрирование главного окна
window_width = 800
window_height = 600
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

style.configure('Large.TButton', font=('Segoe UI', 12, 'bold'), padding=10,
                background='#6200ee', foreground='white', borderwidth=0,
                focusthickness=3, focuscolor='#6200ee')
style.map('Large.TButton',
          background=[('active', '#3700b3'), ('!disabled', '#6200ee')],
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
    foreground="#360082")
header.pack(pady=(5, 15))


# Поля для ввода
ttk.Label(main_frame, text="Логин:", style='Large.TLabel').pack(pady=5)
username_entry = ttk.Entry(main_frame, style='Large.TEntry')
username_entry.pack(pady=5, ipady=8, fill='x')

ttk.Label(main_frame, text="Пароль:", style='Large.TLabel').pack(pady=5)
password_entry = ttk.Entry(main_frame, show="*", style='Large.TEntry')
password_entry.pack(pady=5, ipady=8, fill='x')

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
