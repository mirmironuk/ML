from tkinter import *
from tkinter import ttk
import PIL.Image
from PIL import ImageTk
import minecraft_launcher_lib
import subprocess
import sys
import os
import ast
import threading
import random
import string
import urllib.request
import winshell
import shutil
import time

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
    for i in minecraft_launcher_lib.utils.get_available_versions(os.path.join(minecraft_directory, "versions")):
        if selected_option.get() == i["id"]:
            print(selected_option.get() == i["id"])
            nointver=False
    if nointver:
        options["gameDirectory"] = os.path.join(os.path.join(minecraft_directory, "versions"),selected_option.get())
        print(options["gameDirectory"],"АААААА")
    else:
        options["gameDirectory"] = minecraft_directory
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

        canvname.create_text(200, 25, text="Редагувати ник", font=("Arial", 20), fill="black")
        
        text_field = Entry(canvname, font=("Arial", 18))
        text_field.place(x=75, y=175)

        canvname.create_text(200, 155, text="Ник", font=("Arial", 20), fill="black")
        
        button = Button(canvname, text="Сохранити НИК", font=("Arial", 35), command=saveder)  
        button.place(x=10, y=300)

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

    infname = Label(tk, text="Ваш ник", font=("Helvetica", 32), fg='#FFD700', bg='white', bd=0)
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

    verplusbtn = Button(tk, text="Кастом версії", font=("Arial", 16), width=15, height=1, command=lambda: castomversion())
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
    global fon, photo, transparent_photo2, transparentcastom_photo, transparentcastom_image, tk, selectedcast_option, starterbtn, verplusbtn, optioncast_menu, infoprovib, infoprovibforg, infoprodowl, instbtn
    fon.delete("all")
    infoprovib.destroy()
    infoprovibforg.destroy()
    infoprodowl.destroy()
    optioncast_menu.destroy()
    starterbtn.destroy()
    verplusbtn.destroy()
    instbtn.destroy()
def castomtostarter():
    removecastom()
    ownermenu()
#ОТУТ КАСТОМКА
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

    verplusbtn = Button(tk, text="Кастом версії",bg="yellow", font=("Arial", 16), width=15, height=1, command=lambda: castomversion())
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