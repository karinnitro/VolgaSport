import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class ViewProductReviewsWindow:
    def __init__(self, parent, product_id, product_name):
        self.parent = parent
        self.product_id = product_id
        
        self.window = tk.Toplevel(parent)
        self.window.title(f"VolgaShop - Отзывы: {product_name}")
        self.window.geometry("900x650")
        self.window.configure(bg='#D9EBFF')  # Изменен фон
        
        # Стили
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Единая тема
        self.style.configure('TFrame', background='#f5f5f5')  # Изменен фон
        self.style.configure('Header.TLabel', 
                           font=('Poppins', 16, 'bold'),  # Изменен шрифт
                           background='#f5f5f5',
                           foreground='#478dff')  # Изменен цвет
        self.style.configure('Treeview', 
                           font=('Segoe UI', 12),  # Изменен шрифт
                           rowheight=30,
                           fieldbackground='white')
        self.style.configure('Treeview.Heading', 
                           font=('Segoe UI', 12, 'bold'),  # Изменен шрифт
                           background='#72a8fe',  # Изменен цвет
                           foreground='white')
        self.style.map('Treeview',
                      background=[('selected', '#478dff')],  # Изменен цвет
                      foreground=[('selected', 'white')])
        
        # Основной фрейм
        main_frame = ttk.Frame(self.window, style='TFrame')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Заголовок
        ttk.Label(main_frame, 
                 text=f"Отзывы на товар: {product_name}", 
                 style='Header.TLabel').pack(pady=10)
        
        # Таблица с отзывами
        self.tree = ttk.Treeview(main_frame, 
                                columns=('user', 'rating', 'comment', 'date'), 
                                show='headings',
                                height=20)
        
        # Настройка колонок
        self.tree.heading('user', text='Покупатель')
        self.tree.heading('rating', text='Оценка')
        self.tree.heading('comment', text='Отзыв')
        self.tree.heading('date', text='Дата')
        
        self.tree.column('user', width=150, anchor='center')
        self.tree.column('rating', width=100, anchor='center')
        self.tree.column('comment', width=450)
        self.tree.column('date', width=150, anchor='center')
        
        self.tree.pack(expand=True, fill='both')
        
        # Полоса прокрутки
        scrollbar = ttk.Scrollbar(main_frame, 
                                 orient=tk.VERTICAL, 
                                 command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Кнопка закрытия
        btn_frame = ttk.Frame(main_frame, style='TFrame')
        btn_frame.pack(fill='x', pady=10)
        
        ttk.Button(btn_frame,
                  text="Закрыть",
                  command=self.window.destroy,
                  style='TButton').pack(side='right', padx=5, ipadx=20)
        
        # Загрузка отзывов
        self.load_reviews()
    
    def load_reviews(self):
        try:
            conn = sqlite3.connect('sports_store.db')
            cursor = conn.cursor()
            
            cursor.execute('''SELECT username, rating, comment, 
                             strftime('%d.%m.%Y', review_date) 
                             FROM reviews 
                             WHERE product_id=? 
                             ORDER BY review_date DESC''', 
                          (self.product_id,))
            
            for row in cursor.fetchall():
                # Добавляем звезды вместо цифр для оценки
                rating_stars = '★' * row[1] + '☆' * (5 - row[1])
                self.tree.insert('', 'end', values=(row[0], rating_stars, row[2], row[3]))
            
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить отзывы: {e}")
        finally:
            if conn:
                conn.close()

# Пример использования (для тестирования)
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    reviews_app = ViewProductReviewsWindow(root, 1, "Беговая дорожка ProForm")
    root.mainloop()