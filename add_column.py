import sqlite3

def update_product_images():
    """Обновляет пути к изображениям товаров в базе данных."""
    conn = sqlite3.connect('sports_store.db')
    cursor = conn.cursor()

    # Словарь, где ключ - название товара, значение - путь к изображению.
    product_images = {
        "Беговая дорожка ProForm": "images/dorozka.jpg",
        "Гантели наборные 20 кг": "images/ganteli.jpg",
        "Футбольный мяч Adidas": "images/ball.jpg",
        "Футболка Nike женская": "images/tshirt.jpg"
    }
    for product_name, image_path in product_images.items():
        try:
            # Обновляем столбец image_path для товара с соответствующим именем.
            cursor.execute("UPDATE products SET image_path = ? WHERE name = ?", (image_path, product_name))
            print(f"Путь к изображению для товара '{product_name}' обновлен.")
        except sqlite3.Error as e:
            print(f"Ошибка при обновлении товара '{product_name}': {e}")
    conn.commit()
    conn.close()

# Вызываем функцию для обновления изображений
update_product_images()