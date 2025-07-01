import sqlite3
def add_product(name, category, price, quantity, description="", image_path=""):
    conn = sqlite3.connect('sports_store.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO products (name, category, price, quantity, description, image_path)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, category, price, quantity, description, image_path))
    conn.commit()
    conn.close()
    print("Товар добавлен!")


add_product(
    name="Сумка спортивная",
    category="Спортивные аксессуары",
    price=3499.00,
    quantity=42,
    description="Сумка для спорта Adidas",
    image_path="images/bag.jpg"
)