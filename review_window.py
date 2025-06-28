import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class ProductReviewWindow:
    def __init__(self, parent, product_id, product_name, username):
        self.parent = parent
        self.product_id = product_id
        self.username = username
        self.product_name = product_name
        
        self.window = tk.Toplevel(parent)
        self.window.title(f"VolgaShop - Отзыв: {product_name}")
        self.window.geometry("600x500")
        self.window.resizable(False, False)
        self.window.configure(bg='#D9EBFF')  # Изменен фон
        
        # Стили
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Единая тема
        self.style.configure('TFrame', background='#f5f5f5')  # Изменен фон
        self.style.configure('TLabel', 
                           font=('Segoe UI', 12),  # Изменен шрифт
                           background='#f5f5f5', 
                           foreground='#333333')
        self.style.configure('TButton', 
                           font=('Segoe UI', 12),  # Изменен шрифт
                           background='#72a8fe',  # Изменен цвет
                           foreground='white')
        self.style.configure('Submit.TButton', 
                           font=('Segoe UI', 12, 'bold'),  # Изменен шрифт
                           background="#72a8fe",  # Изменен цвет
                           foreground='white')
        
        # Основной контейнер
        main_frame = ttk.Frame(self.window, style='TFrame')
        main_frame.pack(expand=True, fill='both', padx=20, pady=15)

        # Верхняя часть - заголовок и форма
        form_frame = ttk.Frame(main_frame, style='TFrame')
        form_frame.pack(fill='both', expand=True)
        
        # Заголовок (без изменений)
        ttk.Label(form_frame, 
                 text=f"Оставить отзыв на товар:\n«{product_name}»",
                 font=('Poppins', 14, 'bold'),
                 foreground='#478dff',
                 style='TLabel',
                 justify='center').pack(pady=(0, 15))
        
        # Блок оценки (без изменений)
        rating_frame = ttk.Frame(form_frame, style='TFrame')
        rating_frame.pack(pady=5)  # Уменьшен отступ
        
        ttk.Label(rating_frame, text="Оценка:", style='TLabel').pack(side='left')
        
        self.rating = tk.IntVar(value=3)
        for i in range(1, 6):
            ttk.Radiobutton(rating_frame, 
                           text=str(i),
                           variable=self.rating,
                           value=i,
                           style='TLabel').pack(side='left', padx=5)
        
        # Поле комментария с фиксированной высотой
        ttk.Label(form_frame, text="Текст отзыва:", style='TLabel').pack(anchor='w', pady=(10, 5))
        
        self.comment = tk.Text(form_frame, 
                             height=8,  # Уменьшена высота
                             width=50,
                             wrap='word',
                             font=('Segoe UI', 11),
                             bg='white',
                             fg='#333333',
                             padx=5,
                             pady=5)
        self.comment.pack(fill='x')
        
         # Нижняя часть - только кнопки
        button_frame = ttk.Frame(main_frame, style='TFrame')
        button_frame.pack(fill='x', pady=(10, 0))  # Верхний отступ

        # Кнопки с фиксированным расположением
        ttk.Button(button_frame,
                 text="Отмена",
                 command=self.window.destroy,
                 style='TButton').pack(side='right', padx=10, ipadx=15, ipady=3)

        ttk.Button(button_frame,
                 text="Отправить отзыв",
                 style='Submit.TButton',
                 command=self.submit_review).pack(side='right', ipadx=15, ipady=3)

        # Уменьшаем общий размер окна
        self.window.geometry("500x400")  # Более компактный размер
    
    def submit_review(self):
        """Обработчик отправки отзыва"""
        comment = self.comment.get("1.0", tk.END).strip()
        rating = self.rating.get()
        
        # Валидация
        if not comment:
            messagebox.showwarning("Ошибка", "Напишите текст отзыва")
            return
            
        if len(comment) < 20:
            messagebox.showwarning("Ошибка", "Отзыв должен содержать минимум 20 символов")
            return
            
        try:
            conn = sqlite3.connect('sports_store.db')
            cursor = conn.cursor()
            
            # Проверка существующего отзыва
            cursor.execute('''SELECT id FROM reviews 
                            WHERE product_id=? AND username=?''',
                         (self.product_id, self.username))
            
            if cursor.fetchone():
                # Обновление существующего отзыва
                cursor.execute('''UPDATE reviews 
                                SET rating=?, comment=?, review_date=?
                                WHERE product_id=? AND username=?''',
                             (rating, comment, datetime.now(), self.product_id, self.username))
                action = "обновлен"
            else:
                # Новый отзыв
                cursor.execute('''INSERT INTO reviews 
                                (product_id, username, rating, comment, review_date)
                                VALUES (?, ?, ?, ?, ?)''',
                             (self.product_id, self.username, rating, comment, datetime.now()))
                action = "опубликован"
            
            conn.commit()
            messagebox.showinfo("Готово", 
                              f"Ваш отзыв успешно {action}!\nСпасибо за ваше мнение.")
            self.window.destroy()
            
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить отзыв: {str(e)}")
        finally:
            if conn:
                conn.close()

# Пример использования (для тестирования)
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    review_app = ProductReviewWindow(root, 1, "Беговая дорожка ProForm", "test_user")
    root.mainloop()