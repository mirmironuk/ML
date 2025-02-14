import json
import shutil
import zipfile
from io import BytesIO
from tkinter import *
from tkinter import ttk
import PIL.Image
import requests
from PIL import ImageTk, ImageDraw
import minecraft_launcher_lib
import subprocess
import os
import ast
import threading
import random
import string
import time
import re
import webbrowser


from pypresence import Presence
def discord_piar():
    # Ваш application ID з порталу Discord Developer
    CLIENT_ID = "1331602132931055626"

    # Ініціалізація клієнта Presence
    rpc = Presence(CLIENT_ID)
    rpc.connect()

    states = [
        "Слава Україні!",
        "Героям слава!",
        "Донатив на ЗСУ???",
        "https://mirlauncher.infy.uk",
    ]

    # Інформація для Rich Presence з кнопками
    rpc.update(state=random.choice(states),
        details="Український Лаунчер Майнкрафт",
        large_image="https://github.com/mirmironuk/ML/raw/main/ico.png"
    )

    print("Rich Presence активовано!")
    try:
        while True:
            # Оновлення Rich Presence з новим випадковим станом
            rpc.update(
                state=random.choice(states),
                details="Український Лаунчер Майнкрафт",
                large_image="https://github.com/mirmironuk/ML/raw/main/ico.png",
            )
            time.sleep(10)
    except KeyboardInterrupt:
        print("Завершення роботи...")
        rpc.close()


threading.Thread(target=lambda :discord_piar()).start()

def open_folder_in_explorer():
    global minecraft_directory

    os.startfile(minecraft_directory)
def check_option_file():
    global minecraft_directory
    option_file_path = "data/option.txt"
    if not os.path.exists(option_file_path):
        # Якщо файл не існує, створюємо його з певними значеннями за замовчуванням
        default_options = [
            "",  # Параметр JVM Arguments
            "",  # Шлях до виконуваного файлу
            "",  # За замовчуванням виконуваний файл
            "False",  # Параметр Custom Resolution
            "",  # Ширина роздільної здатності
            "",  # Висота роздільної здатності
            "False",  # Режим демо-версії
            "",  # Директорія Minecraft
            "False" #Консоль
        ]
        #{jvm_arguments}\n{exec_path}\n{default_exec_path}\n{custom_resolution}\n{resolution_width}\n{resolution_height}\n{demo_mode}\n{mine_directory}
        # Записуємо значення за замовчуванням у файл
        with open(option_file_path, 'w') as file:
            for option in default_options:
                file.write(f"{option}\n")
    with open("data/option.txt", 'r') as file:
        opter = file.read().splitlines()
    if opter[7]:
        minecraft_directory=opter[7]
    namedata="data/nick.txt"
    if not os.path.exists(namedata):
        prefix = ''.join(random.choices(string.ascii_letters, k=random.randint(1, 5)))  # вибираємо 3 випадкові літери

        suffix = str(random.randint(1, 999))  # випадкове ціле число від 100 до 999

        # Збираємо нік разом
        nick = f"ML_{prefix}{suffix}"
        with open(namedata, 'w') as file:
            file.write(f"{nick}")
            
    option_file_path = "data/type_version.txt"
    if not os.path.exists(option_file_path):
        # Якщо файл не існує, створюємо його з певними значеннями за замовчуванням
        default_options = [
            "True",  
            "False",  
            "False",  
            "False",  
        ]
        with open(option_file_path, 'w') as file:
            for option in default_options:
                file.write(f"{option}\n")
def first_start():
    if not os.path.exists(minecraft_launcher_lib.utils.get_minecraft_directory()):
        os.makedirs(minecraft_launcher_lib.utils.get_minecraft_directory())
        os.makedirs(os.path.join(minecraft_launcher_lib.utils.get_minecraft_directory(),"versions"))
    if not os.path.exists("data"):
        os.makedirs("data")
    with open("data/option.txt", 'r') as file:
        opter = file.read().splitlines()
    if opter[7]:
        minecraft_directory = opter[7]
        if not os.path.exists(minecraft_directory):
            os.makedirs(minecraft_directory)
            os.makedirs(os.path.join(minecraft_directory,"versions"))
    
def start_game(name):
    global minecraft_directory, selected_option, options, minecraft_command, haver, playbtn
    def button_reload():
        playbtn.configure(state=DISABLED)
        info = Label(tk, text="3", bg='white')
        info.place(x=50, y=305)
        time.sleep(1)
        info.config(text="2")
        time.sleep(1)
        info.config(text="1")
        time.sleep(1)
        info.destroy()
        playbtn.configure(state=NORMAL)

    def is_valid_minecraft_version(version: str) -> bool:
        # Регулярний вираз для версій Minecraft
        pattern = re.compile(
            r"^(?:"
            r"(?:\d+\.\d+(?:\.\d+)?(?:-pre\d+)?)|"  # Релізні версії (наприклад, 1.20, 1.20.1, 1.20-pre2)
            r"(?:alpha \d+\.\d+\.\d+)|"  # Альфа-версії (наприклад, alpha 1.2.3)
            r"(?:beta \d+\.\d+\.\d+)|"  # Бета-версії (наприклад, beta 1.3.4)
            r"(?:\d+w\d+[a-z]?)"  # Снапшоти (наприклад, 23w45a)
            r")$"
        )
        return bool(pattern.match(version))

    gamerstarter = threading.Thread(target=button_reload)
    gamerstarter.start()
    with open("data/option.txt", 'r') as file:
         opter = file.read().splitlines()
    if opter[7]:
        minecraft_directory=opter[7]
    minecraft_directory_version = os.path.join(minecraft_directory, "versions")
    folders = [f for f in os.listdir(minecraft_directory_version) if os.path.isdir(os.path.join(minecraft_directory_version, f))]
    haver = selected_option.get() in folders

    if not haver:
        dowloader()
    options = {
        "username": name.get(),
        "uuid": "e74d23a9-3a45-4b76-8591-544f346bbc50",
        "token": "12345"
    }
    with open("data/option.txt", 'r') as file:
         opter = file.read().splitlines()
    if opter[0]:
        options["jvmArguments"]=ast.literal_eval(opter[0])
    if opter[1]:
        options["executablePath"]=opter[1] 
    if opter[2]:
        options["defaultExecutablePath"]=opter[2]
    options["customResolution"]=opter[3]
    if opter[4]:
        options["resolutionWidth"]=opter[4]
    if opter[5]:
        options["resolutionHeight"]=opter[5] 
    if ast.literal_eval(opter[6]):
        options["demo"]=ast.literal_eval(opter[6])
    if opter[7]:
        minecraft_directory=opter[7]
    nointver=True
    try:
        for i in minecraft_launcher_lib.utils.get_available_versions(os.path.join(minecraft_directory, "versions")):
            if selected_option.get() == i["id"]:
                print(selected_option.get() == i["id"])
                nointver=False
        if nointver:
            options["gameDirectory"] = os.path.join(os.path.join(minecraft_directory, "versions"),selected_option.get())
            print(options["gameDirectory"],"АААААА")
        else:
            options["gameDirectory"] = minecraft_directory
    except Exception as e:
        if is_valid_minecraft_version(selected_option.get()):
            options["gameDirectory"] = minecraft_directory
        else:
            options["gameDirectory"] = os.path.join(os.path.join(minecraft_directory, "versions"),
                                                    selected_option.get())
    print(selected_option.get(), minecraft_directory, options)
    minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(selected_option.get(), minecraft_directory, options)
    print("Старт")
    if not ast.literal_eval(opter[8]):
        subprocess.run(minecraft_command, creationflags=subprocess.CREATE_NO_WINDOW, cwd=options["gameDirectory"])
    else:
        subprocess.run(minecraft_command, cwd=options["gameDirectory"])
    print("Фінал")
def dowloader():
    global minecraft_directory, selected_option, playbtn
    print("Тест")
    info=Label(tk, text="Привіт, світ!", bg='white')
    info.place(x=50, y=305)
    playbtn.configure(state=DISABLED)
    stat="Нема"
    def set_status(status: str):
        global stat
        stat=status
        info.config(text=status)
    def set_progress(progress: int):
        global stat
        if current_max != 0:
            info.config(text=f"{progress}/{current_max}, {stat}")
    def set_max(new_max: int):
        global current_max
        current_max = new_max
    
    callback = {
        "setStatus": set_status,
        "setProgress": set_progress,
        "setMax": set_max
    }
    with open("data/option.txt", 'r') as file:
         opter = file.read().splitlines()
    print(f"-- {opter[7]} {opter}")
    if opter[7]:
        minecraft_directory=opter[7]
    #else: Було до глобальной переоботки но не памятаю начо
    minecraft_launcher_lib.install.install_minecraft_version(selected_option.get(), minecraft_directory, callback=callback)
    info.destroy()
    playbtn.configure(state=NORMAL)
    sel_ver_game()
def sel_ver_game(event=None):
    global minecraft_directory, playbtn, selected_option, haver
    with open("data/option.txt", 'r') as file:
        opter = file.read().splitlines()
    if opter[7]:
        minecraft_directory = opter[7]
    minecraft_directory_version = os.path.join(minecraft_directory, "versions")
    folders = [f for f in os.listdir(minecraft_directory_version) if os.path.isdir(os.path.join(minecraft_directory_version, f))]

    haver = selected_option.get() in folders
    if haver:
        playbtn.config(text="Запустити")
    else:
        playbtn.config(text="Скачати")
        
tk = Tk()
tk.title('MirLauncher')
tk.geometry("1000x600")
tk.resizable(0, 0)

fon = Canvas(tk, width=1000, height=600)
fon.pack()

try:
    icon = PhotoImage(file="images/ico.png")
    tk.iconphoto(False, icon)
    check_option_file()
except Exception as e:
    pass


#######################
######ФОН#############
def namenik():
    global name, name_option, nameall
    with open("data/nick.txt", 'r') as file:
        nameall = file.read().splitlines()
    nameall.append("Налаштування")
    name = StringVar(tk)
    name.set(nameall[0])
    name_option = ttk.Combobox(tk, textvariable=name, values=nameall, width=15, font=("Arial", 24))
    name_option.bind("<<ComboboxSelected>>", nameader)
    name_option.place(x=100, y=125)
yestcanvname=False
def nameader(event=None):
    global name_option, nameall, yestcanvname, canvname, versall, redactor_menu, nameadder, name_option
    def radact_sell(event=None):
        if not nameopti.get()=="Додати":
            text_field.delete(0, END)
            text_field.insert(0, nameopti.get())
        else:
            text_field.delete(0, END)

    def reloadname():
        global redactor_menu, nameadder, indexer, name_option
        redactor_menu.destroy()
        
        nameadder.append("Додати")
        nameopti.set(nameadder[indexer])
        
        redactor_menu = ttk.Combobox(canvname, textvariable=nameopti, values=nameadder, width=15, state='readonly', font=("Arial", 24))
        redactor_menu.bind("<<ComboboxSelected>>", radact_sell)
        redactor_menu.place(x=60, y=50)

        name_option.destroy()
        namenik()
    def saveder():
        global nameadder, indexer
        indexer=nameadder.index(nameopti.get())
        nameadder.pop(indexer)
        nameadder.insert(indexer,text_field.get())
        if "Додати" in nameadder:
            dobindex=nameadder.index("Додати")
            nameadder.pop(dobindex)
        with open('data/nick.txt', 'w') as file:
            for name in nameadder:
                file.write(name + '\n')
        reloadname()
    if name_option.get() == nameall[-1]:
        yestcanvname=True
        canvname = Canvas(tk, width=400, height=500, bg="LightBlue")
        canvname.place(x=550, y=70)
        
        nameadder=nameall
        nameadder.pop(len(nameadder)-1)
        nameadder.append("Додати")
        
        nameopti = StringVar(canvname)
        nameopti.set(nameadder[0])
        redactor_menu = ttk.Combobox(canvname, textvariable=nameopti, values=nameadder, width=15, state='readonly', font=("Arial", 24))
        redactor_menu.bind("<<ComboboxSelected>>", radact_sell)
        redactor_menu.place(x=60, y=50)

        canvname.create_text(200, 25, text="Редагувати нік", font=("Arial", 20), fill="black")
        
        text_field = Entry(canvname, font=("Arial", 18))
        text_field.place(x=75, y=175)

        canvname.create_text(200, 155, text="Нік", font=("Arial", 20), fill="black")
        
        button = Button(canvname, text="Зберегти НІК", font=("Arial", 35), command=saveder)
        button.place(x=40, y=300)

        radact_sell()
def ownermenu():
    global transparent_photo, transparent_photo2, filephoto, photo, reloadphoto
    global fon,infname,name,infver,option_menu,playbtn,starterbtn,reloadbtn,setingbtn, filesbtn,setingbtn, verplusbtn, murworldbtn
    global selected_option, minecraft_directory, name, versall
    image = PIL.Image.open("images/background.png")
    
    resized_image = image.resize((1000, 600), PIL.Image.LANCZOS)

    photo = ImageTk.PhotoImage(resized_image)
    fon.create_image(0, 0, anchor=NW, image=photo)
    minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()
    with open("data/option.txt", 'r') as file:
        opter = file.read().splitlines()
    if opter[7]:
        minecraft_directory = opter[7]
    
    if not os.path.exists(minecraft_directory):
        os.mkdir(minecraft_directory)
    if not os.path.exists(os.path.join(minecraft_directory, "versions")):
        os.mkdir(os.path.join(minecraft_directory, "versions"))
    try:
        allversget=minecraft_launcher_lib.utils.get_available_versions(minecraft_directory)
        versall=[]
        with open("data/type_version.txt", 'r') as file:
            opver = file.read().splitlines()
        for i in allversget:
            if i["type"]=="release" and ast.literal_eval(opver[0]):
                versall.append(i["id"])
            elif i["type"]=="snapshot" and ast.literal_eval(opver[1]):
                versall.append(i["id"])
            elif i["type"]=="old_beta" and ast.literal_eval(opver[2]):
                versall.append(i["id"])
            elif i["type"]=="old_alpha" and ast.literal_eval(opver[3]):
                versall.append(i["id"])
        minecraft_directory_version = os.path.join(minecraft_directory, "versions")
        versaller = [f for f in os.listdir(minecraft_directory_version) if os.path.isdir(os.path.join(minecraft_directory_version, f))]
        print(versall)
        print(versaller)
        new_list_test=[]
        for item in versall+versaller:
            if item not in new_list_test:
                new_list_test.append(item)
        versall=new_list_test
        for ir in versaller:
            versall.remove(ir)
            versall.insert(0,ir)
    except Exception as e:
        print(e)
        minecraft_directory_version = os.path.join(minecraft_directory, "versions")
        versall = [f for f in os.listdir(minecraft_directory_version) if os.path.isdir(os.path.join(minecraft_directory_version, f))]
    transparent_image = PIL.Image.new("RGBA", (500, 600), (0, 0 , 0, 128))  # Створення частково прозорого зображення
    transparent_photo = ImageTk.PhotoImage(transparent_image)  # Конвертація у формат, який підтримує tkinter

    fon.create_image(0, 0, anchor=NW, image=transparent_photo)  # Відображення прозорого прямокутника на canvas

    transparent_image2 = PIL.Image.new("RGBA", (1000, 50), (53, 1, 225, 128))  # Створення частково прозорого зображення
    transparent_photo2 = ImageTk.PhotoImage(transparent_image2)  # Конвертація у формат, який підтримує tkinter

    fon.create_image(0, 0, anchor=NW, image=transparent_photo2)  # Відображення прозорого прямокутника на canvas

    infname = Label(tk, text="Ваш нік", font=("Helvetica", 32), fg='#FFD700', bg='white', bd=0)
    infname.place(x=160,y=60)

    namenik()

    infver = Label(tk, text="Версія", font=("Helvetica", 32), fg='#FFD700', bg='white', bd=0)
    infver.place(x=175,y=180)

    selected_option = StringVar(tk)
    selected_option.set(versall[0])
    option_menu = ttk.Combobox(tk, textvariable=selected_option, values=versall, width=15, state='readonly', font=("Arial", 24))
    option_menu.bind("<<ComboboxSelected>>", sel_ver_game)
    option_menu.place(x=100, y=245)

    playbtn = Button(tk, text="Запустити гру", font=("Arial", 32), width=15, height=1, command=lambda: startergumero())
    playbtn.place(x=50, y=345)

    starterbtn = Button(tk, text="Стартер",bg="yellow", font=("Arial", 16), width=15, height=1, command=lambda: startergumero())
    starterbtn.place(x=50, y=5)

    verplusbtn = Button(tk, text="Моди", font=("Arial", 16), width=15, height=1, command=lambda: castomversion())
    verplusbtn.place(x=280, y=5)

    fileimg = PIL.Image.open("images/file.png")  # Змініть шлях до вашого зображення
    fileimg = fileimg.resize((60,50))
    filephoto = ImageTk.PhotoImage(fileimg)
    filesbtn = Button(tk, image=filephoto, width=75, height=60, command=lambda: open_folder_in_explorer())
    filesbtn.place(x=50, y=500)

    reloadimg = PIL.Image.open("images/reload.png")  
    reloadimg = reloadimg.resize((75, 60))  # Змініть розмір зображення, якщо потрібно
    reloadphoto = ImageTk.PhotoImage(reloadimg)
    reloadbtn = Button(tk, image=reloadphoto, width=75, height=60, command=lambda: reloadbter())
    reloadbtn.image = reloadphoto  # Зберігаємо посилання на зображення для уникнення видалення з пам'яті
    reloadbtn.place(x=200, y=500)

    setingimg = PIL.Image.open("images/seting.png")  
    setingimg = setingimg.resize((75, 60))  # Змініть розмір зображення, якщо потрібно
    setingphoto = ImageTk.PhotoImage(setingimg)
    setingbtn = Button(tk, image=setingphoto, width=75, height=60, command=lambda: seting())
    setingbtn.image = setingphoto
    setingbtn.place(x=350, y=500)

    sel_ver_game()
#Отут удалялка кастомки
def removecastom():
    global vers_cast_option, text_seart, seart_btn, seting_btn
    global  sel_mod_btn, sel_sheder_btn, sel_texture_btn, sel_world_btn
    global modifi_list, modifi_list_Nowinst
    global  scrollbar, scrollbar_Nowinst

    vers_cast_option.destroy()
    text_seart.destroy()
    seart_btn.destroy()
    seting_btn.destroy()

    sel_mod_btn.destroy()
    sel_sheder_btn.destroy()
    sel_texture_btn.destroy()
    sel_world_btn.destroy()

    modifi_list_Nowinst.destroy()
    modifi_list.destroy()

    scrollbar.destroy()
    scrollbar_Nowinst.destroy()
def castomtostarter():
    removecastom()
    ownermenu()
#ОТУТ КАСТОМКА
"""
def castomversion():
    global fon, photo, transparent_photo2, transparentcastom_photo, transparentcastom_image, tk, selectedcast_option, starterbtn, verplusbtn, optioncast_menu, infoprovib, infoprovibforg, infoprodowl, instbtn
    def select_forg(event=None):
        global selectedcast_option
        if minecraft_launcher_lib.forge.find_forge_version(selectedcast_option.get())==None:
            forg_vers_type="Версії нема"
        else:
            forg_vers_type= minecraft_launcher_lib.forge.find_forge_version(selectedcast_option.get())
        infoprovibforg.config(text=forg_vers_type)
    def dowlonder():
        global selectedcast_option
        current_max = 0
        def set_status(status: str):
            infoprodowl.config(text=status)


        def set_progress(progress: int):
            if current_max != 0:
                infoprodowl.config(text=f"{progress}/{current_max}")


        def set_max(new_max: int):
            global current_max
            current_max = new_max
        
        with open("data/option.txt", 'r') as file:
            opter = file.read().splitlines()
        if opter[7]:
            minecraft_directory=opter[7]
        else:
            minecraft_directory=minecraft_launcher_lib.utils.get_minecraft_directory()
        def dowlondermine():
            minecraft_launcher_lib.forge.install_forge_version(minecraft_launcher_lib.forge.find_forge_version(selectedcast_option.get()), minecraft_directory, callback=callback)
        callback = {
            "setStatus": set_status,
            "setProgress": set_progress,
            "setMax": set_max
        }
        print("старт установки")
        background_thread = threading.Thread(target=dowlondermine)
        background_thread.start()
        pass
    removeownmenu()
    fon.create_image(0, 0, anchor=NW, image=photo)
    fon.create_image(0, 0, anchor=NW, image=transparent_photo2)

    starterbtn = Button(tk, text="Стартер", font=("Arial", 16), width=15, height=1, command=lambda: castomtostarter())
    starterbtn.place(x=50, y=5)

    verplusbtn = Button(tk, text="Моди",bg="yellow", font=("Arial", 16), width=15, height=1, command=lambda: castomversion())
    verplusbtn.place(x=280, y=5)

    when_vers=minecraft_launcher_lib.utils.get_minecraft_directory()
    allversget_ft=minecraft_launcher_lib.utils.get_available_versions(os.path.join(when_vers, "versions"))
    versall_tf=[]
    for i in allversget_ft:
        if i["type"]=="release":
            versall_tf.append(i["id"])
            
    transparentcastom_image = PIL.Image.new("RGBA", (300, 450), (0, 0 , 0, 128))  # Створення частково прозорого зображення
    transparentcastom_photo = ImageTk.PhotoImage(transparentcastom_image)  # Конвертація у формат, який підтримує tkinter

    fon.create_image(350, 100, anchor=NW, image=transparentcastom_photo)

    infoprovib=Label(tk, text="Вибери", width=10, font=("Arial", 24))
    infoprovib.place(x=400, y=150)
    
    selectedcast_option = StringVar(tk)
    selectedcast_option.set(versall_tf[0])
    optioncast_menu = ttk.Combobox(tk, textvariable=selectedcast_option, values=versall_tf, width=10, state='readonly', font=("Arial", 24))
    optioncast_menu.bind("<<ComboboxSelected>>", select_forg)
    optioncast_menu.place(x=395, y=200)

    if minecraft_launcher_lib.forge.find_forge_version(minecraft_launcher_lib.utils.get_latest_version()["release"])==None:
        forg_vers_type="Версії нема"
    else:
        forg_vers_type=minecraft_launcher_lib.forge.find_forge_version(minecraft_launcher_lib.utils.get_latest_version()["release"])
    infoprovibforg=Label(tk, text=forg_vers_type, width=13, font=("Arial", 24))
    infoprovibforg.place(x=375, y=300)

    print(minecraft_launcher_lib.forge.find_forge_version(minecraft_launcher_lib.utils.get_latest_version()["release"]))

    infoprodowl=Label(tk, text="", width=21, font=("Arial", 16))
    infoprodowl.place(x=372, y=350)
    
    instbtn = Button(tk, text="Установити", font=("Arial", 16), width=17, height=1, command=lambda: dowlonder())
    instbtn.place(x=400, y=400)
"""


def castomversion():
    global fon, photo, transparent_photo2, transparentcastom_photo, transparentcastom_image, tk, selectedcast_option, starterbtn, verplusbtn, optioncast_menu, infoprovib, infoprovibforg, infoprodowl, instbtn
    global minecraft_directory
    global index, filter_vers, filter_type_vers, filter_field_sort, waiter
    global  sel_mod_btn, sel_sheder_btn, sel_texture_btn, sel_world_btn
    global text_seart, seart_btn, seting_btn, modifi_list, modifi_list_Nowinst
    global scrollbar, scrollbar_Nowinst

    with open("data/option.txt", 'r') as file:
        opter = file.read().splitlines()
    if opter[7]:
        minecraft_directory = opter[7]
    else:
        minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()

    def vers_list():
        global name, name_option, version_castom_all
        global on_active_dowlo_menu
        vers_now_activiti="Виберіть"
        on_active_dowlo_menu=False
        def version_selected(event=None):
            global selectedcast_option, type_vers_list, type_vers_option, vers_now_activiti
            def select_forg(event=None):
                global selectedcast_option , type_vers_option
                if type_vers_option.get()=="Forge":
                    if minecraft_launcher_lib.forge.find_forge_version(selectedcast_option.get()) == None:
                        forg_vers_type = "Версії нема"
                    else:
                        forg_vers_type = minecraft_launcher_lib.forge.find_forge_version(selectedcast_option.get())
                elif type_vers_option.get()=="Fabric":
                    def is_fabric_available(minecraft_version):
                        """
                        Перевіряє, чи існує Fabric версія для вказаної версії Minecraft.

                        :param minecraft_version: Версія Minecraft (наприклад, "1.20.1")
                        :return: True, якщо Fabric доступний для цієї версії, інакше False
                        """
                        url = "https://meta.fabricmc.net/v2/versions/game"
                        try:
                            response = requests.get(url)
                            response.raise_for_status()
                            versions = response.json()
                            for version in versions:
                                if version["version"] == minecraft_version:
                                    return f"Fabric {minecraft_version}"
                            return "Нема Версії"  # Якщо версія не знайдена
                        except requests.RequestException as e:
                            print(f"Помилка при запиті до Fabric Meta API: {e}")
                            return "Ошибка"
                    forg_vers_type = is_fabric_available(selectedcast_option.get())
                infoprovibforg.config(text=forg_vers_type)


            def dowlonder():
                global selectedcast_option, type_vers_option
                current_max = 0

                def set_status(status: str):
                    infoprodowl.config(text=status)

                def set_progress(progress: int):
                    if current_max != 0:
                        infoprodowl.config(text=f"{progress}/{current_max}")

                def set_max(new_max: int):
                    global current_max
                    current_max = new_max

                with open("data/option.txt", 'r') as file:
                    opter = file.read().splitlines()
                if opter[7]:
                    minecraft_directory = opter[7]
                else:
                    minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()

                def dowlondermine():
                    if type_vers_option.get()=="Forge":
                        minecraft_launcher_lib.forge.install_forge_version(
                            minecraft_launcher_lib.forge.find_forge_version(selectedcast_option.get()), minecraft_directory,
                            callback=callback)
                    elif type_vers_option.get()=="Fabric":
                        minecraft_launcher_lib.fabric.install_fabric(selectedcast_option.get(), minecraft_directory, callback=callback)
                    infoprodowl.config(text=f"Встановлено")

                callback = {
                    "setStatus": set_status,
                    "setProgress": set_progress,
                    "setMax": set_max
                }
                print("старт установки")
                background_thread = threading.Thread(target=dowlondermine)
                background_thread.start()
                pass

            global on_active_dowlo_menu
            selected_version = vers_cast.get()
            if selected_version=="Додати" and not on_active_dowlo_menu:
                on_active_dowlo_menu = True
                top_frame = Frame(tk, bg="#ADD8E6", highlightbackground="yellow", highlightthickness=2, width=350,
                                  height=450)
                top_frame.place(relx=0.5, rely=0.5, anchor="center")
                top_frame.lift()

                close_btn=Button(
                    top_frame,
                    text="X",
                    font=100,
                    bg="#ff4d4d",  # Червоний фон
                    fg="white",  # Білий текст
                    activebackground="#ff6666",  # Активний стан
                    activeforeground="white",  # Колір тексту у активному стані
                    relief="flat",  # Згладжені краї
                    command=lambda: closer_dow()
                )
                close_btn.place(relx=1.0, rely=0.0, anchor="ne", width=40, height=40)


                def closer_dow():
                    global on_active_dowlo_menu
                    top_frame.destroy()
                    on_active_dowlo_menu = False

                when_vers = minecraft_launcher_lib.utils.get_minecraft_directory()
                allversget_ft = minecraft_launcher_lib.utils.get_available_versions(os.path.join(when_vers, "versions"))
                versall_tf = []
                for i in allversget_ft:
                    if i["type"] == "release":
                        versall_tf.append(i["id"])

                infoprovib = Label(top_frame, text="Вибери", width=10, font=("Arial", 24))
                infoprovib.place(relx=0.5, y=75, anchor="center")

                type_vers_list=["Forge","Fabric"]
                type_vers_option = StringVar(top_frame)
                type_vers_option.set(type_vers_list[0])
                type_vers_menu = ttk.Combobox(top_frame, textvariable=type_vers_option, values=type_vers_list, width=10,
                                               state='readonly', font=("Arial", 24))
                type_vers_menu.bind("<<ComboboxSelected>>", select_forg)
                type_vers_menu.place(relx=0.5, y=125, anchor="center")

                selectedcast_option = StringVar(top_frame)
                selectedcast_option.set(versall_tf[0])
                optioncast_menu = ttk.Combobox(top_frame, textvariable=selectedcast_option, values=versall_tf, width=10,
                                               state='readonly', font=("Arial", 24))
                optioncast_menu.bind("<<ComboboxSelected>>", select_forg)
                optioncast_menu.place(relx=0.5, y=175, anchor="center")

                if minecraft_launcher_lib.forge.find_forge_version(
                        minecraft_launcher_lib.utils.get_latest_version()["release"]) == None:
                    forg_vers_type = "Версії нема"
                else:
                    forg_vers_type = minecraft_launcher_lib.forge.find_forge_version(
                        minecraft_launcher_lib.utils.get_latest_version()["release"])
                infoprovibforg = Label(top_frame, text=forg_vers_type, width=13, font=("Arial", 24))
                infoprovibforg.place(relx=0.5, y=250, anchor="center")

                infoprodowl = Label(top_frame, text="", width=21, font=("Arial", 16))
                infoprodowl.place(relx=0.5, y=300, anchor="center")

                instbtn = Button(top_frame, text="Установити", font=("Arial", 16), width=17, height=1,
                                 command=lambda: dowlonder())
                instbtn.place(relx=0.5, y=375, anchor="center")

            global type_modifi
            vers_now_activiti = vers_cast.get()
            all_now_install_mod_fn(vers_now_activiti, type_modifi)
        def is_valid_minecraft_version(version: str) -> bool:
            # Регулярний вираз для версій Minecraft
            pattern = re.compile(
                r"^(?:"
                r"(?:\d+\.\d+(?:\.\d+)?(?:-pre\d+)?)|"  # Релізні версії (наприклад, 1.20, 1.20.1, 1.20-pre2)
                r"(?:alpha \d+\.\d+\.\d+)|"  # Альфа-версії (наприклад, alpha 1.2.3)
                r"(?:beta \d+\.\d+\.\d+)|"  # Бета-версії (наприклад, beta 1.3.4)
                r"(?:\d+w\d+[a-z]?)"  # Снапшоти (наприклад, 23w45a)
                r")$"
            )
            return bool(pattern.match(version))

        version_castom_all = []  # Початкове значення
        for i in os.listdir(os.path.join(minecraft_directory, "versions")):
            if not is_valid_minecraft_version(i):
                version_castom_all.append(i)
        version_castom_all.append("Додати")

        global vers_cast_option, vers_cast
        vers_cast = StringVar(tk)
        vers_cast.set("Виберіть")  # Встановити перше значення як активне
        vers_cast_option = ttk.Combobox(tk, textvariable=vers_cast, values=version_castom_all, width=15,
                                        font=("Arial", 24),state="readonly")

        vers_cast_option.bind("<<ComboboxSelected>>", version_selected)  # Correct binding
        vers_cast_option.place(x=55, y=55)


    removeownmenu()
    fon.create_image(0, 0, anchor=NW, image=photo)
    fon.create_image(0, 0, anchor=NW, image=transparent_photo2)

    starterbtn = Button(tk, text="Стартер", font=("Arial", 16), width=15, height=1, command=lambda: castomtostarter())
    starterbtn.place(x=50, y=5)

    verplusbtn = Button(tk, text="Моди", bg="yellow", font=("Arial", 16), width=15, height=1,
                        command=lambda: castomversion())
    verplusbtn.place(x=280, y=5)

    vers_list()

    global  type_modifi, vers_now_activiti
    type_modifi="Моди"
    def btn_vibir(type):
        global  type_modifi, vers_cast_option, vers_now_activiti
        def  all_none():
            sel_mod_btn.config(bg="SystemButtonFace")
            sel_sheder_btn.config(bg="SystemButtonFace")
            sel_texture_btn.config(bg="SystemButtonFace")
            sel_world_btn.config(bg="SystemButtonFace")
            vers_cast_option.config(state="readonly")
        if type=="Моди":
            all_none()
            type_modifi = "Моди"
            sel_mod_btn.config(bg="yellow")
        elif type=="МодПак":
            all_none()
            type_modifi="МодПак"
            vers_cast_option.config(state="disabled")
        elif type=="Шейдери":
            all_none()
            type_modifi="Шейдери"
            sel_sheder_btn.config(bg="yellow")
        elif type=="ТекстурПак":
            all_none()
            type_modifi="ТекстурПак"
            sel_texture_btn.config(bg="yellow")
        elif type=="Світи":
            all_none()
            type_modifi="Світи"
            sel_world_btn.config(bg="yellow")
        try:
            all_now_install_mod_fn(vers_now_activiti,  type_modifi)
        except Exception as e:
            all_now_install_mod_fn("Виберіть",  type_modifi)
        clear_add_modifi()


    sel_mod_btn = Button(tk, text="Моди", bg="yellow", font=("Arial", 16), width=10, height=1,command=lambda: threading.Thread(target=lambda: btn_vibir("Моди")).start())
    sel_mod_btn.place(x=360, y=55)

    sel_sheder_btn = Button(tk, text="Шейдери", font=("Arial", 16), width=10, height=1,
                            command=lambda: threading.Thread(target=lambda: btn_vibir("Шейдери")).start())
    sel_sheder_btn.place(x=508, y=55)

    sel_texture_btn = Button(tk, text="ТекстурПак", font=("Arial", 16), width=10, height=1,
                             command=lambda: threading.Thread(target=lambda: btn_vibir("ТекстурПак")).start())
    sel_texture_btn.place(x=656, y=55)

    sel_world_btn = Button(tk, text="Світи", font=("Arial", 16), width=10, height=1,command=lambda: threading.Thread(target=lambda: btn_vibir("Світи")).start())
    sel_world_btn.place(x=809, y=55)


    def search():
        global searcher
        searcher =text_seart.get()
        clear_add_modifi()
    text_seart = Entry(tk, font=("Arial", 18))
    text_seart.place(x=55, y=110, width=785, height=40)

    seart_btn = Button(tk, text="🔍", font=("Arial", 16), command=search)
    seart_btn.place(x=850, y=110)

    seting_btn = Button(tk, text="⚙️", font=("Arial", 16), command=lambda: filter_sitteng())
    seting_btn.place(x=897, y=110)

    global filter_anabler
    filter_anabler=False
    def filter_sitteng():
        global filter_anabler, versall_tf
        global filter_field_sort
        global filter_type_vers
        global filter_vers
        if not filter_anabler:
            filter_anabler=True
            seting_frame = Frame(tk, bg="#ADD8E6", highlightbackground="yellow", highlightthickness=2, width=330,
                                      height=300)
            seting_frame.place(x=658, y=145)
            seting_frame.lift()
            close_btn = Button(
                seting_frame,
                text="X",
                font=100,
                bg="#ff4d4d",  # Червоний фон
                fg="white",  # Білий текст
                activebackground="#ff6666",  # Активний стан
                activeforeground="white",  # Колір тексту у активному стані
                relief="flat",  # Згладжені краї
                command=lambda: filter_anable()
            )
            close_btn.place(relx=1.0, rely=0.0, anchor="ne", width=40, height=40)

            vers_filter=Label(seting_frame,text="Фільтр", bg="#ADD8E6" ,font=("Arial", 24))
            vers_filter.place(relx=0.5, y=25, anchor="center")






            allversget_ft = minecraft_launcher_lib.utils.get_available_versions(minecraft_directory=os.path.join(minecraft_directory,"versions"))
            versall_tf = ["Всі"]
            for i in allversget_ft:
                if i["type"] == "release":
                    versall_tf.append(i["id"])

            global vers_cast, selectedcast_filter_option
            selectedcast_filter_option = StringVar(seting_frame)
            try:
                try:
                        selectedcast_filter_option.set(filter_vers)
                except Exception as e:
                    with open( os.path.join(os.path.join(os.path.join(minecraft_directory,"versions"),vers_cast.get()),f"{vers_cast.get()}.json"), 'r', encoding='utf-8') as file:
                        data = json.load(file)
                        selectedcast_filter_option.set(data["inheritsFrom"])
            except Exception as e:
                selectedcast_filter_option.set(versall_tf[0])

            optioncast_menu = ttk.Combobox(seting_frame, textvariable=selectedcast_filter_option, values=versall_tf, width=10,
                                           state='readonly', font=("Arial", 24))
            optioncast_menu.place(relx=0.5, y=75, anchor="center")

            #

            try:
                try:
                    var = StringVar(value=filter_type_vers)
                except Exception as E:
                    print("type er"+str(e))
                    if "Forge" in data["arguments"]["game"]:
                        var = StringVar(value="Any")
                    elif "fabric" in data["mainClass"]:
                        var = StringVar(value="Fabric")
            except Exception as E:
                var = StringVar(value="Any")
            options = ["Any", "Forge", "Fabric"]

            def create_radio_button(option, pluser):
                rb = Radiobutton(seting_frame, text=option, variable=var, value=option)
                rb.place(relx=0.3 + pluser, y=125, anchor="center")
                return rb

            pluser = 0
            for option in options:
                create_radio_button(option, pluser)
                pluser += 0.2




            try:
                vars = StringVar(value=filter_field_sort)
            except Exception as E:
                vars = StringVar(value="Кількість завантаження")
            options = ["Кількість завантаження", "Популярність", "Рейтинг"]

            Radiobutton(seting_frame, text=options[0], variable=vars, value=options[0]).place(relx=0.33, y=175, anchor="center")
            Radiobutton(seting_frame, text=options[1], variable=vars, value=options[1]).place(relx=0.75, y=175, anchor="center")
            Radiobutton(seting_frame, text=options[2], variable=vars, value=options[2]).place(relx=0.5, y=205, anchor="center")

            def filter_anable():
                global filter_anabler
                filter_anabler = False
                seting_frame.destroy()

            def savinger():
                global filter_field_sort
                global filter_type_vers
                global filter_vers

                if vars.get() == "Всі":
                    filter_field_sort = ""
                else:
                    filter_field_sort = vars.get()
                filter_type_vers = var.get()
                filter_vers = selectedcast_filter_option.get()

                threading.Thread(target=clear_add_modifi())
            saveder=Button(seting_frame,text="Зберегти", font="Arial, 16", command= lambda: savinger())
            saveder.place(relx=0.5, y=255, anchor="center")

    modifi_list = Canvas(tk, bg="#333333", highlightthickness=0)
    modifi_list.place(x=355, y=155, width=570, height=440)

    # Додавання вертикальної прокрутки
    scrollbar = ttk.Scrollbar(tk, orient="vertical", command=lambda *args: (modifi_list.yview(*args)))
    scrollbar.place(x=925, y=155, height=440)  # Розташування ліворуч

    modifi_list.configure(yscrollcommand=scrollbar.set)

    # Створюємо фрейм всередині Canvas
    scrollable_frame = Frame(modifi_list, bg="#444444")
    scrollable_frame_id = modifi_list.create_window((0, 0), window=scrollable_frame, anchor="nw")

    all_indi=[]
    all_modifer=[]
    def add_modifi(modifi_list,type_modificat):
        if type_modifi == type_modificat:
            fr = Frame(scrollable_frame, bg="#555555", bd=0, highlightthickness=0)
            fr.pack(fill="x", padx=5, pady=5)
            all_modifer.append(fr)
            try:
                # Завантаження зображення
                response = requests.get(modifi_list[1])
                img = PIL.Image.open(BytesIO(response.content))
            except Exception as e:
                print(e)
                img_size = 150
                img = PIL.Image.new('RGB', (img_size, img_size), color=(200, 200, 200))
                draw = ImageDraw.Draw(img)
                text = "No Image"
                draw.multiline_text((10, 20), text, fill=(0, 0, 0), align="center")

            img = img.resize((100, 100), PIL.Image.LANCZOS)
            tk_img = ImageTk.PhotoImage(img)

            label = Label(fr, image=tk_img, bd=0, highlightthickness=0)
            label.image = tk_img
            label.pack(side="left")

            tfr = Frame(fr, bg="#555555", bd=0, highlightthickness=0, width=100, height=25)
            tfr.place(x=100, y=0)

            def url_open(ura):
                webbrowser.open(ura)
            def on_leave(event):
                mod_name.config(fg="white")
            def on_enter(event):
                mod_name.config(fg="blue")
            if modifi_list[2][:25]<modifi_list[2]:
                modn=modifi_list[2][:25]+"..."
            else:
                modn=modifi_list[2][:25]
            mod_name = Label(tfr, text=modn, font=("Arial", 16), bg="#555555", fg="white")
            mod_name.pack(side="left")
            mod_name.bind("<Button-1>", lambda e: url_open(modifi_list[0]))
            mod_name.bind("<Enter>", on_enter)
            mod_name.bind("<Leave>", on_leave)

            if modifi_list[4][:10]<modifi_list[3]:
                moda=modifi_list[4][:10]+"..."
            else:
                moda = modifi_list[4][:10]
            # Додаємо mod_auth під mod_name
            mod_auth = Label(tfr, text=f"| {moda}", font=("Arial", 16), bg="#555555", fg="#b3b6b7")
            mod_auth.pack(side="left")

            mod_desc_one = Label(fr, text=modifi_list[3][:40], font=("Arial", 10), bg="#555555", fg="#b3b6b7")
            mod_desc_one.place(x=100, y=25)

            try:
                all_files = []
                laster_vers_mod=False
                mod_file_name_to_id={}
                if not vers_cast.get()=="Виберіть":
                    with open(os.path.join(os.path.join(os.path.join(minecraft_directory, "versions"), vers_cast.get()),
                                           f"{vers_cast.get()}.json"), 'r', encoding='utf-8') as file:
                        data = json.load(file)
                for i in modifi_list[6]:
                    all_files.append(i["filename"])
                    mod_file_name_to_id[i["filename"]]=i["fileId"]
                    if laster_vers_mod==False and not vers_cast.get()=="Виберіть" and data["inheritsFrom"]==i["gameVersion"]:
                        laster_vers_mod=True
                        all_indi[-1].set(i["filename"])
                all_indi.append(StringVar(fr))
                if laster_vers_mod==False:
                    all_indi[-1].set(all_files[0])
                geter=all_indi[-1]
                optioncast_menu = ttk.Combobox(fr, textvariable=all_indi[-1], values=all_files,
                                               width=22,
                                               state='readonly', font=("Arial", 16))
                #optioncast_menu.bind("<<ComboboxSelected>>", update_filter_version)


                def async_dowlftb():
                    threading.Thread(target=dowlonder_fn_to_btn).start()

                optioncast_menu.place(x=105, y=58)
                dowl_modifi=Button(fr, text="+", font=("Arial", "64"),bg="Lime",activebackground="LimeGreen",
                                   command=async_dowlftb)
                dowl_modifi.place(x=400, y=0, width=160, height=100)
                def dowlonder_fn_to_btn():
                    if vers_cast.get() in ["Виберіть","Додати"] and not type_modifi=="МодПак":
                        warning_window = Toplevel(tk)
                        warning_window.title("Попередження")
                        warning_window.geometry("250x60")
                        warning_window.iconphoto(False, PhotoImage(file="images/ico.png"))

                        # Текст повідомлення
                        warning_label = Label(warning_window, text="Виберіть збірку щоб поставити мод", wraplength=200)
                        warning_label.pack(pady=10)
                    elif not type_modifi in ["МодПак","Світи"]:
                        ifer_vers = {"Моди": "mods", "Шейдери": "shaderpacks", "Світи": "saves","ТекстурПак": "resourcepacks"}
                        director_modifi=os.path.join(os.path.join(os.path.join(minecraft_directory,"versions"),vers_cast.get()),ifer_vers[type_modifi])
                        gmd=get_modificator_dowload(modifi_list[5], mod_file_name_to_id[geter.get()])
                        if gmd.status_code == 200:
                            download_file(gmd.json()["data"],director_modifi)
                            all_now_install_mod_fn(vers_now_activiti, type_modifi)
                        else:
                            warn_window = Toplevel(tk)
                            warn_window.title("Попередження")
                            warn_window.geometry("250x60")
                            warn_window.iconphoto(False, PhotoImage(file="images/ico.png"))

                                # Текст повідомлення
                            warning_label = Label(warn_window , text=f"Помилка {gmd.status_code}",wraplength=200)
                            warning_label.pack(pady=10)
                    else:
                        if type_modifi=="Світи":
                            if not os.path.isdir("cache"):
                                os.makedirs("cache")
                            director_modifi = "cache/world"
                            if not os.path.isdir(director_modifi ):
                                os.makedirs(director_modifi )
                            gmd = get_modificator_dowload(modifi_list[5], mod_file_name_to_id[geter.get()])
                            if gmd.status_code == 200:
                                name=download_file(gmd.json()["data"],director_modifi )
                                director_vers=os.path.join(os.path.join(os.path.join(minecraft_directory, "versions"),vers_cast.get()),"saves")
                                with zipfile.ZipFile(f"cache/world/{name}") as zip_ref:
                                    filelist=zip_ref.namelist()
                                    worlds=""
                                    zip_ref.extractall("cache/world")
                                    for file_path in filelist:
                                        parts = file_path.split('/')

                                        # Відсікання файлів всередині архіву, де є `level.dat`
                                        if len(parts) > 1 and parts[-1] == 'level.dat':
                                            world_name = parts[:len(parts)-1]
                                            print(world_name)
                                            break
                                    for i in parts[:len(parts)-1]:
                                        worlds=f"{worlds}/{i}"
                                    worlds=worlds.lstrip("/")

                                    print(worlds)

                                    shutil.move(f"cache/world/{worlds}", director_vers)

                                shutil.rmtree("cache")

                                all_now_install_mod_fn(vers_now_activiti, type_modifi)
                            else:
                                warn_window = Toplevel(tk)
                                warn_window.title("Попередження")
                                warn_window.geometry("250x60")
                                warn_window.iconphoto(False, PhotoImage(file="images/ico.png"))

                                # Текст повідомлення
                                warning_label = Label(warn_window, text=f"Помилка {gmd.status_code}", wraplength=200)
                                warning_label.pack(pady=10)
            except Exception as e:
                print(e)
                mod_auth = Label(fr, text=f"Файлів не найдено", font=("Arial", 16), bg="#555555", fg="#b3b6b7")
                mod_auth.place(x=105, y=58)
            if not globals()["type_modifi"]==type_modificat:
                fr.destroy()
    def clear_add_modifi():
        global index
        index=0
        for i in all_modifer:
            i.destroy()
        modifi_list.yview_moveto(0)
        on_reach_end()


    def configure_scroll_region(event):
        """Налаштовуємо область прокрутки."""
        modifi_list.configure(scrollregion=modifi_list.bbox("all"))

    def resize_frame(event):
        """Розширюємо фрейм на всю ширину Canvas."""
        modifi_list.itemconfig(scrollable_frame_id, width=event.width)


    def on_scroll(event):
        """Реалізація прокрутки за допомогою миші."""
        modifi_list.yview_scroll(-1 * (event.delta // 120), "units")

        threading.Thread(target=lambda: check_reach_end()).start()

    waiter = False
    def check_reach_end():
        global waiter
        """Перевіряє, чи досягнуто кінця прокрутки."""
        canvas_view = modifi_list.yview()
        if canvas_view[1] >= 1.0 and waiter==False:
            waiter=True
            on_reach_end()
            time.sleep(1)
            waiter=False
    # Прив'язуємо обробники подій
    scrollable_frame.bind("<Configure>", configure_scroll_region)
    modifi_list.bind("<Configure>", resize_frame)

    # Додаємо прокрутку тільки при наведенні
    modifi_list.bind("<Enter>", lambda e: modifi_list.bind_all("<MouseWheel>", on_scroll))
    modifi_list.bind("<Leave>", lambda e: modifi_list.unbind_all("<MouseWheel>"))

    index=0
    def on_reach_end():
        global index, type_modifi
        print(index)
        if not "filter_vers" in globals():
            allversget_ft = minecraft_launcher_lib.utils.get_available_versions(
                minecraft_directory=os.path.join(minecraft_directory, "versions"))
            versall_tf = []
            for i in allversget_ft:
                if i["type"] == "release":
                    versall_tf.append(i["id"])
            filter_vers=versall_tf[0]
        else:
            filter_vers=globals()["filter_vers"]
        if not "searcher" in globals():
            searcher=""
        else:
            searcher=globals()["searcher"]
        if not "filter_type_vers" in globals():
            filter_type_vers=""
        else:
            filter_type_vers=globals()["filter_type_vers"]
        if not "filter_field_sort" in globals():
            filter_field_sort=""
        else:
            filter_field_sort=globals()["filter_field_sort"]
        def asin_geter_lister():
            for i in get_list_modificator(index,type_modifi, filter_vers, searcher,filter_type_vers,filter_field_sort):
                add_modifi(i, type_modifi)
        threading.Thread(asin_geter_lister()).start()
        index+=10


    # Підключаємо події
    scrollable_frame.bind("<Configure>", configure_scroll_region)
    modifi_list.bind("<Configure>", resize_frame)

    # Заповнюємо фрейм для демонстрації

    threading.Thread(target=lambda: on_reach_end()).start()



    #
    modifi_list_Nowinst = Canvas(tk, bg="#333333", highlightthickness=0)
    modifi_list_Nowinst.place(x=55, y=155, width=270, height=440)

    # Додавання вертикальної прокрутки для modifi_list_Nowinst
    scrollbar_Nowinst = ttk.Scrollbar(tk, orient="vertical", command=modifi_list_Nowinst.yview)
    scrollbar_Nowinst.place(x=325, y=155, height=440)  # Розташування для другого Canvas
    modifi_list_Nowinst.configure(yscrollcommand=scrollbar_Nowinst.set)

    scrollable_frame_now = Frame(modifi_list_Nowinst, bg="#444444")
    scrollable_frame_id_now = modifi_list_Nowinst.create_window((0, 0), window=scrollable_frame_now, anchor="nw")

    # Прив'язка прокрутки до другого Canvas
    def on_scroll_Nowinst(event):
        """Обробка прокрутки миші."""
        modifi_list_Nowinst.yview_scroll(-1 * (event.delta // 120), "units")

    def configure_scroll_region_Nowinst(event):
        """Налаштовуємо область прокрутки."""
        modifi_list_Nowinst.configure(scrollregion=modifi_list_Nowinst.bbox("all"))

    def resize_frame_Nowinst(event):
        """Розширюємо фрейм на всю ширину Canvas."""
        modifi_list_Nowinst.itemconfig(scrollable_frame_id_now, width=event.width)


    list_fn_all = []

    def all_now_install_mod_fn(castomka, type):
        """Завантаження та відображення списку модифікацій."""
        for i in list_fn_all.copy():
            i.destroy()
            list_fn_all.remove(i)
        modifi_list_Nowinst.yview_moveto(0)
        if castomka not in ["Виберіть", "Додати"]:
            if type=="Моди" or type=="Шейдери" or type=="Світи" or type=="ТекстурПак":
                ifer_vers = {"Моди": "mods", "Шейдери": "shaderpacks", "Світи": "saves"
                                                                                "", "ТекстурПак": "resourcepacks"}
                direct_modifi = os.path.join(os.path.join(os.path.join(minecraft_directory, "versions"), castomka),
                                             ifer_vers[type])
                if not os.path.exists(direct_modifi):
                    os.makedirs(direct_modifi)
                direct_cast = [f for f in os.listdir(direct_modifi)]

                def create_one_modifi_now(i):
                    fr = Frame(scrollable_frame_now, bg="#555555", padx=0, pady=0, bd=0, highlightthickness=0)
                    fr.pack(fill="x", padx=5, pady=5)
                    list_fn_all.append(fr)

                    st = Label(fr, text=i, bg="#555555", fg="white", anchor="w", width=30)
                    st.pack(side="left")

                    delt = Button(fr, text="🗑", command=lambda: delete_modifi(os.path.join(direct_modifi, i), fr), width=4,
                                  bg="red")
                    delt.pack(side="right")

                for i in direct_cast:
                    create_one_modifi_now(i)
        if type=="МодПак":
            direct_modifi = os.path.join(minecraft_directory, "versions")
            if not os.path.exists(direct_modifi):
                os.makedirs(direct_modifi)

            direct_cast =[f for f in os.listdir(direct_modifi)]

            def create_one_modifi_now(i):
                fr = Frame(scrollable_frame_now, bg="#555555", padx=0, pady=0, bd=0, highlightthickness=0)
                fr.pack(fill="x", padx=5, pady=5)
                list_fn_all.append(fr)

                st = Label(fr, text=i, bg="#555555", fg="white", anchor="w", width=30)
                st.pack(side="left")

                delt = Button(fr, text="🗑", command=lambda: delete_modifi(os.path.join(direct_modifi, i), fr), width=4,
                                bg="red")
                delt.pack(side="right")

            for i in direct_cast:
                create_one_modifi_now(i)

    # Прив'язуємо обробники подій для другого Canvas
    modifi_list_Nowinst.bind("<Enter>", lambda e: modifi_list_Nowinst.bind_all("<MouseWheel>", on_scroll_Nowinst))
    modifi_list_Nowinst.bind("<Leave>", lambda e: modifi_list_Nowinst.unbind_all("<MouseWheel>"))

    scrollable_frame_now.bind("<Configure>", configure_scroll_region_Nowinst)
    modifi_list_Nowinst.bind("<Configure>", resize_frame_Nowinst)

    def delete_modifi(modficator, fr):
        """Видалення модифікації."""

        def show_warning(modficator):
            warning_window = Toplevel(tk)
            warning_window.title("Попередження")
            warning_window.geometry("250x120")
            warning_window.iconphoto(False, PhotoImage(file="images/ico.png"))

            # Текст повідомлення
            warning_label = Label(warning_window, text="Ви впевнені, що хочете продовжити?", wraplength=200)
            warning_label.pack(pady=10)

            # Кнопки "ОК" і "Скасувати"
            button_frame = Frame(warning_window)
            button_frame.pack(pady=10)

            ok_button = Button(button_frame, text="ОК", width=10, command=lambda : on_ok(modficator), bg="red")
            ok_button.grid(row=0, column=0, padx=5)

            cancel_button = Button(button_frame, text="Скасувати", width=10, command=lambda : warning_window.destroy(), bg="green")
            cancel_button.grid(row=0, column=1, padx=5)
            def on_ok(modficator):
                try:
                    os.remove(modficator)
                except Exception as e:
                    shutil.rmtree(modficator)
                fr.destroy()
                list_fn_all.remove(fr)
                warning_window.destroy()
        show_warning(modficator)


def get_list_modificator(index, type_modifi, gameversion="", name="", mod_load="Any",
                         field_sort="Кількість завантаження", sortOrders="desc"):
    if mod_load=="":
        mod_load="Any"
    if field_sort=="":
        field_sort="Кількість завантаження"
    if sortOrders=="":
        sortOrders="desc"
    headers = {
        'Accept': 'application/json',
        'x-api-key': 'НЕДАМ ВАМ ТОКЕН'
    }

    all_type_id_modifi = {"Моди": 6, "МодПак": 4471, "Шейдери": 6552, "ТекстурПак": 12, "Світи": 17}
    all_type_id_field_sort = {"Популярність": 2, "Кількість завантаження": 6, "Рейтинг": 12}
    all_type_id_mod_load = {"Any": "", "Forge": 1, "Fabric": 4}

    r = requests.get('https://api.curseforge.com/v1/mods/search', params={
        'gameId': '432',
        'searchFilter': name,
        'gameVersions': str(gameversion),
        'sortField': all_type_id_field_sort[field_sort],
        'sortOrder': sortOrders,
        'classId': all_type_id_modifi[type_modifi],
        'index': str(index),
        'ModLoaderType': all_type_id_mod_load[mod_load],
        'pageSize': '10'
    }, headers=headers)

    jso = r.json()
    ret = []
    for i in range(len(jso['data'])):
        author = ""
        for j in range(len(jso['data'][i]['authors'])):
            author += jso['data'][i]['authors'][0]['name'] + ","
        ret.append([jso['data'][i]['links']['websiteUrl'], jso['data'][i]['logo']['url'], jso['data'][i]['name'],
                    jso['data'][i]['summary'], author.rstrip(','), jso['data'][i]['id'],
                    jso['data'][i]['latestFilesIndexes']])
    return ret
def get_modificator_dowload(modId,id):
    headers = {
      'Accept': 'application/json',
      'x-api-key': 'НЕДАМ ВАМ ТОКЕН'
    }

    r = requests.get(f'https://api.curseforge.com/v1/mods/{modId}/files/{id}/download-url', headers = headers)

    return r
def download_file(url, save_directory):
    filename = url.split('/')[-1]
    file_path = os.path.join(save_directory, filename)

    response = requests.get(url)
    response.raise_for_status()

    with open(file_path, 'wb') as file:
        file.write(response.content)

    return  filename

def removeownmenu():
    global fon,infname,name,infver,option_menu,playbtn,starterbtn,reloadbtn,setingbtn, filesbtn, setingbtn, verplusbtn, murworldbtn, name_option, yestcanvname, canvname
    fon.delete("all")
    infname.destroy()
    name_option.destroy()
    infver.destroy()
    option_menu.destroy()
    playbtn.destroy()
    starterbtn.destroy()
    filesbtn.destroy()
    reloadbtn.destroy()
    setingbtn.destroy()
    verplusbtn.destroy()
    if yestcanvname:
        canvname.destroy()
def reloadbter():
    removeownmenu()
    ownermenu()
seting_window = Toplevel(tk)
seting_window.title("Settings")
seting_window.geometry("400x300")
seting_window.destroy()

def apply_settings():
    jvm_arguments = jvm_arguments_var.get()
    exec_path = exec_path_var.get()
    default_exec_path = default_exec_path_var.get()
    custom_resolution = custom_resolution_var.get()
    resolution_width = resolution_width_var.get()
    resolution_height = resolution_height_var.get()
    demo_mode = demo_mode_var.get()
    mine_directory = mine_directory_var.get()
    console_mode = Console_mode_var.get()
    texting = f"{jvm_arguments}\n{exec_path}\n{default_exec_path}\n{custom_resolution}\n{resolution_width}\n{resolution_height}\n{demo_mode}\n{mine_directory}\n{console_mode}\n"

    with open("data/option.txt", 'w') as file:
        file.write(texting)

    relise=relise_mode_var.get()
    snap=Snapshot_mode_var.get()
    beta=Beta_mode_var.get()
    alfa=Alfa_mode_var.get()
    veralf= f"{relise}\n{snap}\n{beta}\n{alfa}\n"
    with open("data/type_version.txt", 'w') as file:
        file.write(veralf)
    seting_window.destroy()
def seting():
    global seting_window, seting_frame, canvas_seting, scrollbar_seting
    global jvm_arguments_var, exec_path_var, default_exec_path_var
    global custom_resolution_var, resolution_width_var, resolution_height_var
    global game_directory_var, demo_mode_var, mine_directory_var
    global seting_background_image, seting_resized_image, seting_photo
    global Alfa_mode_var, Beta_mode_var, Snapshot_mode_var, relise_mode_var, Console_mode_var
    if not seting_window or not seting_window.winfo_exists():
        seting_window = Toplevel()
        seting_window.title("Settings")
        seting_window.geometry("400x300")
        
        canvas_seting = Canvas(seting_window, width=400, height=300, bg="light blue")
        canvas_seting.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar_seting = Scrollbar(seting_window, orient=VERTICAL, command=canvas_seting.yview)
        scrollbar_seting.pack(side=RIGHT, fill=Y)

        canvas_seting.configure(yscrollcommand=scrollbar_seting.set)

        seting_frame = Frame(canvas_seting)
        canvas_seting.create_window((0, 0), window=seting_frame, anchor=NW)

        def on_frame_configure(event):
            canvas_seting.configure(scrollregion=canvas_seting.bbox("all"))

        seting_frame.bind("<Configure>", on_frame_configure)

        def on_mouse_scroll(event):
           canvas_seting.yview_scroll(-1 * int(event.delta / 120), "units")

        canvas_seting.bind_all("<MouseWheel>", on_mouse_scroll)

        # Налаштування для JVM Arguments
        jvm_arguments_var = StringVar()
        jvm_arguments_label = Label(seting_frame, text='JVM Arguments (["-Xmx2G", "-Xms2G"]):')
        jvm_arguments_entry = Entry(seting_frame, textvariable=jvm_arguments_var)
        jvm_arguments_label.pack()
        jvm_arguments_entry.pack()

        # Налаштування для Java Executable Paths
        exec_path_var = StringVar()
        default_exec_path_var = StringVar()
        exec_path_label = Label(seting_frame, text="Executable Path:")
        exec_path_entry = Entry(seting_frame, textvariable=exec_path_var)
        default_exec_path_label = Label(seting_frame, text="Default Executable Path:")
        default_exec_path_entry = Entry(seting_frame, textvariable=default_exec_path_var)
        exec_path_label.pack()
        exec_path_entry.pack()
        default_exec_path_label.pack()
        default_exec_path_entry.pack()

        # Налаштування для Custom Resolution
        custom_resolution_var = BooleanVar()
        resolution_width_var = StringVar()
        resolution_height_var = StringVar()
        custom_resolution_var.set(False)  # За замовчуванням вимкнуто
        custom_resolution_checkbox = Checkbutton(seting_frame, text="Enable Custom Resolution", variable=custom_resolution_var)
        resolution_width_label = Label(seting_frame, text="Resolution Width:")
        resolution_width_entry = Entry(seting_frame, textvariable=resolution_width_var)
        resolution_height_label = Label(seting_frame, text="Resolution Height:")
        resolution_height_entry = Entry(seting_frame, textvariable=resolution_height_var)
        custom_resolution_checkbox.pack()
        resolution_width_label.pack()
        resolution_width_entry.pack()
        resolution_height_label.pack()
        resolution_height_entry.pack()

        # Налаштування для Game Directory
        mine_directory_var = StringVar()
        mine_directory_label = Label(seting_frame, text="Mine Directory:")
        mine_directory_entry = Entry(seting_frame, textvariable=mine_directory_var)
        mine_directory_label.pack()
        mine_directory_entry.pack()

        # Налаштування для Demo Mode

        demo_mode_var = BooleanVar()
        demo_mode_var.set(False)  # За замовчуванням вимкнуто
        demo_mode_checkbox = Checkbutton(seting_frame, text="Use Demo Mode", variable=demo_mode_var)
        demo_mode_checkbox.pack()

        # Налаштування для Relis Mode
        relise_mode_var = BooleanVar()
        relise_mode_var.set(True)  
        relise_mode_checkbox = Checkbutton(seting_frame, text="Реліз", variable=relise_mode_var)
        relise_mode_checkbox.pack()
        
        # Налаштування для Snapshot Mode
        Snapshot_mode_var = BooleanVar()
        Snapshot_mode_var.set(False)  # За замовчуванням вимкнуто
        Snapshot_mode_checkbox = Checkbutton(seting_frame, text="Снапшот", variable=Snapshot_mode_var)
        Snapshot_mode_checkbox.pack()

        Beta_mode_var = BooleanVar()
        Beta_mode_var.set(False)  # За замовчуванням вимкнуто
        Beta_mode_checkbox = Checkbutton(seting_frame, text="Бета", variable=Beta_mode_var)
        Beta_mode_checkbox.pack()

        Alfa_mode_var = BooleanVar()
        Alfa_mode_var.set(False)  # За замовчуванням вимкнуто
        Alfa_mode_checkbox = Checkbutton(seting_frame, text="Альфа", variable=Alfa_mode_var)
        Alfa_mode_checkbox.pack()

        Console_mode_var = BooleanVar()
        Console_mode_var.set(False)  # За замовчуванням вимкнуто
        Console_mode_checkbox = Checkbutton(seting_frame, text="Консоль", variable=Console_mode_var)
        Console_mode_checkbox.pack()
        
        save_button = Button(seting_window, text="Зберегти і вийти", command=apply_settings)
        save_button.place(x=280, y=250)
        
        with open("data/option.txt", 'r') as file:
            opter = file.read().splitlines()
    
        jvm_arguments_var.set(opter[0])
        exec_path_var.set(opter[1])
        default_exec_path_var.set(opter[2])
        custom_resolution_var.set(ast.literal_eval(opter[3]))
        resolution_width_var.set(opter[4])
        resolution_height_var.set(opter[5])
        demo_mode_var.set(ast.literal_eval(opter[6]))
        mine_directory_var.set(opter[7])
        Console_mode_var.set(opter[8])

        with open("data/type_version.txt", 'r') as file:
            opver = file.read().splitlines()
            
        relise_mode_var.set(ast.literal_eval(opver[0]))
        Snapshot_mode_var.set(ast.literal_eval(opver[1]))
        Beta_mode_var.set(ast.literal_eval(opver[2]))
        Alfa_mode_var.set(ast.literal_eval(opver[3]))
    else:
        seting_window.destroy()
def startergumero():
    gamerstarter=threading.Thread(target=start_game, args=(name,))
    gamerstarter.start()
#if os.path.exists("images"):
ownermenu()

tk.mainloop()