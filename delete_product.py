import sqlite3

def delete_product(product_name):
    conn = sqlite3.connect('sports_store.db')
    cursor = conn.cursor()
    
    try:
        # Удаляем товар
        cursor.execute("DELETE FROM products WHERE name=?", (product_name,))
        # Удаляем связанные отзывы
        cursor.execute("DELETE FROM reviews WHERE product_id IN (SELECT id FROM products WHERE name=?)", (product_name,))
        conn.commit()
        print(f"Товар '{product_name}' успешно удален")
    except Exception as e:
        print(f"Ошибка при удалении: {e}")
    finally:
        conn.close()

# Укажите название товара для удаления
delete_product("Эспандер 68 кг")  # Замените на нужное