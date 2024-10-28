from tkinter import *
from tkinter import filedialog  # Імпорт діалогів
from PIL import Image, ImageTk
import requests
from io import BytesIO
import os
import winshell
from win32com.client import Dispatch

from PIL.ImageOps import mirror
from wget import download

tk = Tk()
tk.title('MirLauncher')
tk.geometry("1000x600")
tk.resizable(0, 0)

def ownermenu():
    global  text_field
    # Завантажуємо зображення з URL
    response = requests.get("https://raw.githubusercontent.com/mirmironuk/ML/main/background.png")
    background_image = Image.open(BytesIO(response.content))  # Використовуємо BytesIO для відкриття зображення
    background_photo = ImageTk.PhotoImage(background_image)

    # Додаємо фон
    background_label = Label(tk, image=background_photo)
    background_label.place(relwidth=1, relheight=1)
    background_label.image = background_photo  # Зберігаємо посилання на зображення

    # Додаємо текстове поле
    director_lab = Label(tk, text="Куди устанавлюєм?", font=("Helvetica", 32), fg='#FFD700', bg='white', bd=0)
    director_lab.place(relx=0.5, rely=0.3, anchor='center')
    text_field = Entry(tk, font=("Arial", 18), width=50)
    text_field.place(relx=0.5, rely=0.45, anchor='center')
    text_field.insert(0,  os.path.join(os.getenv('APPDATA'), '.mirlauncher'))

    # Функція для вибору директорії
    def choose_directory():
        directory = filedialog.askdirectory()  # Відкриваємо діалог вибору директорії
        if directory:  # Якщо користувач вибрав директорію
            text_field.delete(0, END)  # Очищаємо поле
            text_field.insert(0, directory)  # Вставляємо вибрану директорію

    # Додаємо кнопку
    select_button = Button(tk, text="Вибрати директорію", font=("Arial", 18), command=choose_directory)
    select_button.place(relx=0.5, rely=0.6, anchor='center')

    down_button = Button(tk, text="Установити", font=("Arial", 18), command=installer)
    down_button.place(relx=0.5, rely=0.7, anchor='center')

def installer():
    global  text_field
    def download_file(url, save_directory):
        # Отримуємо назву файлу з URL
        filename = url.split('/')[-1]
        # Створюємо повний шлях для збереження файлу
        file_path = os.path.join(save_directory, filename)

        # Завантажуємо файл
        response = requests.get(url)
        response.raise_for_status()  # Перевіряємо, чи не виникла помилка під час завантаження

        # Записуємо файл у вказану директорію
        with open(file_path, 'wb') as file:
            file.write(response.content)

        print(f"Файл '{filename}' збережено в '{save_directory}'.")
    print(text_field.get())
    if not os.path.exists(text_field.get()):
        os.makedirs(text_field.get())
    download_file("https://github.com/mirmironuk/ML/raw/main/launcher.exe",text_field.get())

    if not os.path.exists(os.path.join(text_field.get(),"data")):
        os.makedirs(os.path.join(text_field.get(),"data"))

    if not os.path.exists(os.path.join(text_field.get(),"images")):
        os.makedirs(os.path.join(text_field.get(),"images"))

    download_file("https://github.com/mirmironuk/ML/raw/main/seting.png", os.path.join(text_field.get(),"images"))
    download_file("https://github.com/mirmironuk/ML/raw/main/reload.png", os.path.join(text_field.get(),"images"))
    download_file("https://github.com/mirmironuk/ML/raw/main/ico.png", os.path.join(text_field.get(),"images"))
    download_file("https://github.com/mirmironuk/ML/raw/main/ico.ico", os.path.join(text_field.get(),"images"))
    download_file("https://github.com/mirmironuk/ML/raw/main/file.png", os.path.join(text_field.get(),"images"))
    download_file("https://github.com/mirmironuk/ML/raw/main/background.png", os.path.join(text_field.get(),"images"))

    # Створення ярлика на робочому столі
    install_path = text_field.get()
    image_path = os.path.join(install_path, "images")

    desktop_path = winshell.desktop()
    shortcut_path = os.path.join(desktop_path, "MirLauncher.lnk")
    target_path = os.path.join(install_path, "launcher.exe")
    icon_path = os.path.join(image_path, "ico.ico")

    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = target_path
    shortcut.WorkingDirectory = install_path
    shortcut.IconLocation = icon_path
    shortcut.save()
    print("Ярлик створено на робочому столі.")
ownermenu()
tk.mainloop()
