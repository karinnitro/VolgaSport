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
        self.window.title(f"Отзыв: {product_name}")
        self.window.geometry("600x500")
        self.window.resizable(False, False)
        self.window.configure(bg='#f0f5ff')
        
        # Стили
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f5ff')
        self.style.configure('TLabel', font=('Arial', 12), background='#f0f5ff', foreground='#333333')
        self.style.configure('TButton', font=('Arial', 12))
        self.style.configure('Submit.TButton', 
                           background="#3B98F4", 
                           foreground='white',
                           font=('Arial', 12, 'bold'))
        
        # Основной контейнер
        main_frame = ttk.Frame(self.window, padding=20, style='TFrame')
        main_frame.pack(expand=True, fill='both')
        
        # Заголовок
        ttk.Label(main_frame, 
                 text=f"Оставить отзыв на товар:\n«{product_name}»",
                 font=('Arial', 14, 'bold'),
                 style='TLabel',
                 justify='center').pack(pady=10)
        
        # Блок оценки
        rating_frame = ttk.Frame(main_frame, style='TFrame')
        rating_frame.pack(pady=15)
        
        ttk.Label(rating_frame, text="Оценка:", style='TLabel').pack(side='left')
        
        self.rating = tk.IntVar(value=3)
        for i in range(1, 6):
            ttk.Radiobutton(rating_frame, 
                           text=str(i),
                           variable=self.rating,
                           value=i,
                           style='TLabel').pack(side='left', padx=5)
        
        # Поле комментария
        ttk.Label(main_frame, text="Текст отзыва:", style='TLabel').pack(anchor='w')
        
        self.comment = tk.Text(main_frame, 
                             height=12,
                             width=60,
                             wrap='word',
                             font=('Arial', 11),
                             bg='white',
                             fg='#333333',
                             padx=5,
                             pady=5)
        self.comment.pack(fill='both', expand=True)
        
        # Блок кнопок
        button_frame = ttk.Frame(main_frame, style='TFrame')
        button_frame.pack(fill='x', pady=15)
        
        # Кнопка "Отправить отзыв"
        ttk.Button(button_frame,
                  text="Отправить отзыв",
                  style='Submit.TButton',
                  command=self.submit_review).pack(side='right', 
                                                 ipadx=20, 
                                                 ipady=5)
        
        # Кнопка отмены
        ttk.Button(button_frame,
                  text="Отмена",
                  command=self.window.destroy).pack(side='right', 
                                                  padx=10,
                                                  ipadx=20,
                                                  ipady=5)
    
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