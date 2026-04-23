import tkinter as tk
from tkinter import messagebox, ttk
import requests
import json

# Файл для хранения избранных пользователей
FAVORITES_FILE = "users.json"

def load_favorites():
    try:
        with open(FAVORITES_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_favorites(favorites):
    with open(FAVORITES_FILE, "w") as f:
        json.dump(favorites, f, indent=4)

def search_user():
    username = entry_search.get().strip()
    if not username:
        messagebox.showwarning("Ошибка", "Поле поиска не должно быть пустым")
        return

    try:
        response = requests.get(f"https://api.github.com/users/{username}")
        response.raise_for_status()
        user_data = response.json()
        display_user(user_data)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Ошибка", f"Пользователь не найден или ошибка сети: {e}")

def display_user(user_data):
    listbox_results.delete(0, tk.END)
    info = (
        f"Имя: {user_data.get('name', 'Нет данных')}\n"
        f"Логин: {user_data.get('login')}\n"
        f"Bio: {user_data.get('bio', 'Нет данных')}\n"
        f"Подписчики: {user_data.get('followers')}\n"
        f"Репозитории: {user_data.get('public_repos')}\n"
    )
    listbox_results.insert(tk.END, info)

def add_to_favorites():
    username = entry_search.get().strip()
    if not username:
        messagebox.showwarning("Ошибка", "Сначала найдите пользователя")
        return

    favorites = load_favorites()
    if username in favorites:
        messagebox.showinfo("Информация", "Пользователь уже в избранном")
    else:
        favorites.append(username)
        save_favorites(favorites)
        messagebox.showinfo("Успех", "Пользователь добавлен в избранное")

# --- GUI ---
root = tk.Tk()
root.title("GitHub User Finder")
root.geometry("500x400")

# Поле ввода и кнопка поиска
frame_search = tk.Frame(root)
frame_search.pack(pady=10, fill=tk.X)

entry_search = tk.Entry(frame_search, font=("Arial", 12))
entry_search.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

btn_search = tk.Button(frame_search, text="Поиск", command=search_user)
btn_search.pack(side=tk.LEFT, padx=5)

# Результаты поиска
listbox_results = tk.Listbox(root, font=("Arial", 10), width=60, height=15)
listbox_results.pack(pady=10)

# Кнопка добавления в избранное
btn_fav = tk.Button(root, text="Добавить в избранное", command=add_to_favorites)
btn_fav.pack(pady=5)

root.mainloop()
