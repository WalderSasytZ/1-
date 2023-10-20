import tkinter as tk
import sqlite3
import datetime
import time

# create a table in a datebase
conn = sqlite3.connect('tags.db')
conn.execute('''CREATE TABLE IF NOT EXISTS tags (
                    tag_id INTEGER PRIMARY KEY NOT NULL,
                    name INTEGER,
                    geodate TEXT
                );''')
conn.close()

# create a window
root = tk.Tk()
root.title("Tracker")
root.geometry("800x600")

# add a character
def add_character():
    name = character_name_entry.get()
    conn = sqlite3.connect('tags.db')
    cursor = conn.cursor()

    # find character with this name
    cursor.execute(''' SELECT COUNT(*)
                       FROM tags
                       WHERE name = ?;
                   ''', (name,))
    if cursor.fetchone()[0] == 1:
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
    
    cursor.execute(''' INSERT INTO tags (tag_id, name, geodate)
                       VALUES (?, ?, NULL)
                   ''', (tag_id, name,))
    conn.commit()
    conn.close()
    message = f"Character created\n"
    message_output.config(state=tk.NORMAL)
    message_output.insert(tk.END, message)
    message_output.config(state=tk.DISABLED)

def add_geotag():
    geodate = geo_data_entry.get("1.0", "end-1c")
    request = geodate.split()
    if len(request) != 4:
        message = f"Wrong enter\n"
        message_output.config(state=tk.NORMAL)
        message_output.insert(tk.END, message)
        message_output.config(state=tk.DISABLED)
        return

    request[1] = request[1] + ' ' + request[2] + ' ' + request[3]
    conn = sqlite3.connect('tags.db')
    cursor = conn.cursor()

    # find character with this name
    cursor.execute(''' SELECT COUNT(*)
                       FROM tags
                       WHERE name = ?;
                   ''', (request[0],))

    if cursor.fetchone()[0] == 0:
        message = f"Character is not exist\n"
        message_output.config(state=tk.NORMAL)
        message_output.insert(tk.END, message)
        message_output.config(state=tk.DISABLED)
        return

    cursor.execute(''' SELECT COUNT(*)
                       FROM tags
                       WHERE name = ? AND geodate = ?;
                   ''', (request[0], request[1],))

    if cursor.fetchone()[0] > 0:
        message = f"This character already has that data\n"
        message_output.config(state=tk.NORMAL)
        message_output.insert(tk.END, message)
        message_output.config(state=tk.DISABLED)
        return

    cursor.execute(''' SELECT COUNT(*)
                       FROM tags
                       WHERE name = ? AND geodate = NULL;
                   ''', (request[0],))
    if cursor.fetchone()[0] == 1 :
        cursor.execute(''' SELECT tag_id
                           FROM tags
                           WHERE name = ? AND geodate = NULL;
                   ''', (request[0],))
        tag_id = cursor.fetchone()[0]
        cursor.execute(''' UPDATE tags
                           SET geodate = ?
                           WHERE tag_id = ?;
                   ''', (request[1], tag_id,))
    else:
        # create a unique id
        cursor.execute(''' SELECT MAX(tag_id)
                           FROM tags;''')

        result = cursor.fetchone()
        if result[0] is None:
            tag_id = 0
        else:
            tag_id = result[0] + 1

        cursor.execute(''' INSERT INTO tags (tag_id, name, geodate)
                          VALUES (?, ?, ?)
                       ''', (tag_id, request[0], request[1],))
    message = f"Geodata is added\n"
    message_output.config(state=tk.NORMAL)
    message_output.insert(tk.END, message)
    message_output.config(state=tk.DISABLED)
    conn.commit()
    conn.close()

def show_character_positions():


    return

def show_character_trajectories():
    return


# Поле для ввода имени персонажа
character_name_label = tk.Label(root, text="Character Name:")
character_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

character_name_entry = tk.Entry(root)
character_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

add_character_button = tk.Button(root, text="Add Character", command=add_character)
add_character_button.grid(row=0, column=2, padx=10, pady=5, sticky="w")

# Поле для ввода геопозиции
geo_data_label = tk.Label(root, text="Geolocation:")
geo_data_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

geo_data_entry = tk.Text(root, height=1, width=30)
geo_data_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

add_geo_data_button = tk.Button(root, text="Add Geo Data", command=add_geotag)
add_geo_data_button.grid(row=1, column=2, padx=10, pady=5, sticky="w")

# Создание кнопок
show_positions_button = tk.Button(root, text="Show Positions", command=show_character_positions)
show_positions_button.grid(row=2, column=0, padx=10, pady=10)

show_trajectories_button = tk.Button(root, text="Show Trajectories", command=show_character_trajectories)
show_trajectories_button.grid(row=2, column=1, padx=10, pady=10)

# Поле для вывода сообщений
message_output = tk.Text(root, height=5, width=40)
message_output.grid(row=0, column=3, rowspan=3, padx=10, pady=10)
message_output.config(state=tk.DISABLED)

# Запуск основного цикла
root.mainloop()
