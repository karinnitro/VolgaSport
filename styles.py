from tkinter import ttk

def configure_styles(root):
    """Настройка стилей для ttk виджетов."""
    style = ttk.Style(root)
    style.theme_use('clam')
    
    # Основные стили
    style.configure('.', font=('Segoe UI', 12))
    style.configure('TFrame', background='#f5f5f5')
    style.configure('TLabel', background='#f5f5f5', foreground='#333333')
    style.configure('Large.TLabel', font=('Segoe UI', 14))
    style.configure('Header.TLabel', font=('Poppins', 18, 'bold'), foreground="#478dff")
    
    # Кнопки
    style.configure('TButton', background="#72a8fe", foreground='white')
    style.configure('Large.TButton', font=('Segoe UI', 14, 'bold'), padding=6)
    style.map('TButton',
              background=[('active', '#478dff'), ('!disabled', '#72a8fe')],
              foreground=[('active', 'white'), ('!disabled', 'white')])
    
    # Таблицы
    style.configure('Treeview', 
                   font=('Segoe UI', 12), 
                   background='white',
                   fieldbackground='white',
                   rowheight=30)
    style.configure('Treeview.Heading', 
                   font=('Segoe UI', 12, 'bold'), 
                   background='#72a8fe', 
                   foreground='white')
    style.map('Treeview.Heading',
              background=[('active', '#478dff')])
    
    return style