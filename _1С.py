import tkinter as tk
import sqlite3
import datetime
import time

# create a table in a datebase
conn = sqlite3.connect('tags.db')
conn.execute('''CREATE TABLE IF NOT EXISTS tags (
                    tag_id INTEGER PRIMARY KEY NOT NULL,
                    name INTEGER NOT NULL,
                    tag_date TEXT,
                    pos_x REAL,
                    pos_y REAL
                );''')
conn.close()

# Создание основного окна
root = tk.Tk()
root.title("Tracker")
root.geometry("800x600")

# Функция для добавления нового персонажа
def add_character():
    name = character_name_entry.get()
    conn = sqlite3.connect('tags.db')
    cursor = conn.cursor()

    # find character with this name
    cursor.execute(''' SELECT COUNT(*)
                       FROM tags
                       WHERE name = ?;
                   ''', (name,))
    if cursor.fetchone()[0] is 1:
        message = f"Character already exist\n"
        message_output.config(state=tk.NORMAL)
        message_output.insert(tk.END, message)
        message_output.config(state=tk.DISABLED)
        return

    # create a unique id
    cursor.execute(''' SELECT MAX(tag_id)
                       FROM tags;''')

    result = cursor.fetchone()
    if result[0] is None:
        tag_id = 0
    else:
        tag_id = result[0] + 1
    
    cursor.execute(''' INSERT INTO tags (tag_id, name, tag_date, pos_x, pos_y)
                       VALUES (?, ?, ?, ?, ?)
                   ''', (tag_id, name, None, None, None))
    conn.commit()
    conn.close()





# Функция для отображения позиций персонажей на карте
def show_character_positions():
    return

# Функция для отображения траекторий движения персонажей
def show_character_trajectories():
    return

# Создание кнопок
add_button = tk.Button(root, text="Add person", command=add_character)
show_positions_button = tk.Button(root, text="Show positions", command=show_character_positions)
show_trajectories_button = tk.Button(root, text="Show trajectories", command=show_character_trajectories)

# Размещение кнопок с использованием grid
add_button.grid(row=0, column=0, padx=10, pady=10)
show_positions_button.grid(row=0, column=1, padx=10, pady=10)
show_trajectories_button.grid(row=0, column=2, padx=10, pady=10)

# Поле для ввода имени персонажа
character_name_label = tk.Label(root, text="Character name:")
character_name_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
character_name_entry = tk.Entry(root)
character_name_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

# Поле для вывода сообщений
message_output = tk.Text(root, height=5, width=50)
message_output.grid(row=0, column=3, rowspan=2, padx=10, pady=10)
message_output.config(state=tk.DISABLED)

# Запуск основного цикла
root.mainloop()
