import sqlite3
def add_product(name, category, price, quantity, description=""):
    conn = sqlite3.connect('sports_store.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO products (name, category, price, quantity, description)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, category, price, quantity, description))
    conn.commit()
    conn.close()
    print("Товар добавлен!")

add_product(
    name="Футболка Nike женская",
    category="Спортивная одежда",
    price=999.00,
    quantity=5,
    description="Спортивная футболка Nike женская")

