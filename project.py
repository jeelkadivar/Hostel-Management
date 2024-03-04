import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import pandas as pd
from playsound import playsound
from datetime import datetime
from functools import partial


home = tk.Tk()
home.geometry("1920x1080")
home.title('Main menu')

#This function provides system time.
def time_giver():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return str(current_time)


#This function provides system date.
def date_giver():
    now = datetime.now()
    current_date = now.today().strftime('%d/%m/%Y')
    return current_date


#This function takes input of unique QR code of student.
def scanner(EnEx):

    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()
    while True:
        _, img = cap.read()
        data, one, _ = detector.detectAndDecode(img)
        if data:
            qr_data = data
            break
        cv2.imshow("QRCODEscanner", img)
        if cv2.waitKey(1) == ord("q"):
            break
    playsound("beep.mp3")
    qr_check(qr_data, EnEx)
    cv2.destroyAllWindows()
    cap.release()


#This function verifies unique QR code of student.
def qr_check(data, EnEx):

    if data in names:
        entry_exit(data, EnEx)
    else:
        messagebox.showerror("Invalid QR", "Invalid QR code")


#This function gives exact time&date of entry and exit of student.
def entry_exit(name, EnEx):
    df = pd.read_excel("EntryExit.xlsx")
    df = df.append({"Name": name, "Date": date_giver(), "Time": time_giver(), "Entry/Exit": EnEx}, ignore_index = True)
    df.to_excel("EntryExit.xlsx", index=False)


#This function displays Login interface.
def login():
    global user, passw, Login
    Login = Toplevel(home)
    Login.geometry("1920x1080")
    Login.title('Login')

    Label(Login, text='Username').place(relx=0.44, rely=0.37, anchor=CENTER)
    Label(Login, text='Password').place(relx=0.44, rely=0.42, anchor=CENTER)
    user = StringVar()
    passw = StringVar()
    Entry(Login, textvariable=user).place(relx=0.53, rely=0.37, anchor=CENTER)
    Entry(Login, show="*", textvariable=passw).place(relx=0.53, rely=0.42, anchor=CENTER)
    Button(Login, text='login', width=10, bg='#801213', fg="#f5f5f5", command=validateLogin).place(relx=0.556, rely=0.5, anchor=CENTER)
    Button(Login, text='Back', width=10, bg='#801213', fg="#f5f5f5", command=Login.destroy).place(relx=0.44, rely=0.5, anchor=CENTER)
    Login.mainloop()


#This function displays Food menu.
def B_L_D(name):

    menu = Toplevel(home)
    menu.geometry("1920x1080")
    canvas = Canvas(menu, width=1500, height=700)
    canvas.pack()
    Button(menu, text='Back', width=25, bg='#801213', fg="#f5f5f5", command=menu.destroy).place(x=660, y=750)
    img = (Image.open(name))
    resized_image = img.resize((1500, 700), Image.ANTIALIAS)
    new_image = ImageTk.PhotoImage(resized_image)
    canvas.create_image(10, 10, anchor=NW, image=new_image)

    menu.mainloop()


#This function displays Food menu interface.
def FoodMenu_Show():

    FoodMenu = Tk()
    FoodMenu.title("FoodMenu")
    FoodMenu.geometry("1919x1079")

    Button(FoodMenu, text='Breakfast', width=25, bg='#801213', fg="#f5f5f5", command=partial(B_L_D, "images\Breakfast.png")).place(x=660, y=150)
    Button(FoodMenu, text='Lunch', width=25, bg='#801213', fg="#f5f5f5", command=partial(B_L_D, "images\Lunch.png")).place(x=660, y=250)
    Button(FoodMenu, text='Snacks', width=25, bg='#801213', fg="#f5f5f5", command=partial(B_L_D, "images\Snacks.png")).place(x=660, y=350)
    Button(FoodMenu, text='Dinner', width=25, bg='#801213', fg="#f5f5f5", command=partial(B_L_D, "images\Dinner.png")).place(x=660, y=450)
    Button(FoodMenu, text='Back', width=25, bg='#801213', fg="#f5f5f5", command=FoodMenu.destroy).place(x=660, y=550)
    FoodMenu.mainloop()


#This function displays complain.
def complain_show():

    global CS2
    CS2 = Tk()
    CS2.title("Complains")
    CS2.geometry("1919x1079")

    txtarea = Text(CS2, width=150, height=40)
    txtarea.pack(pady=20)
    tf = open("complains.txt")
    data = tf.read()
    txtarea.insert(END, data)
    Button(CS2, text='Back', width=25, bg='#801213', fg="#f5f5f5", command=CS2.destroy).place(x=460, y=700)
    Button(CS2, text='Reset', width=25, bg='#801213', fg="#f5f5f5", command=partial(reset_text, "complains.txt")).place(x=860, y=700)
    tf.close()
    CS2.mainloop()


def roomservice_txt_show():

    global CS1
    CS1 = Tk()
    CS1.title("Room Service Requests")
    CS1.geometry("1920x1080")

    txtarea = Text(CS1, width=150, height=40)
    txtarea.pack(pady=20)
    tf = open("Room_service.txt")
    data = tf.read()
    txtarea.insert(END, data)
    Button(CS1, text='Back', width=25, bg='#801213', fg="#f5f5f5", command=CS1.destroy).place(x=460, y=700)
    Button(CS1, text='Reset', width=25, bg='#801213', fg="#f5f5f5", command=partial(reset_text, "Room_service.txt")).place(x=860, y=700)

    tf.close()
    CS1.mainloop()


def reset_text(file_name):

    if messagebox.askquestion("Delete text", "Are you sure to delete all text?"):
        open(file_name, 'w').close()
        Login.destroy()
        admin_tk.destroy()
        if file_name == "Room_service.txt":
            CS1.destroy()
        else:
            CS2.destroy()


#This function displays Admin menu interface.
def admin():

    global admin_tk
    admin_tk = Tk()
    admin_tk.geometry("1920x1080")
    admin_tk.title('Admin Menu')

    Button(admin_tk, text='Read complain', width=25, bg='#801213', fg="#f5f5f5", command=complain_show).place(x=660, y=200)
    Button(admin_tk, text='Add student', width=25, bg='#801213', fg="#f5f5f5", command=add_student).place(x=660, y=300)
    Button(admin_tk, text='Remove student', width=25, bg='#801213', fg="#f5f5f5", command=del_student).place(x=660, y=400)
    Button(admin_tk, text='Room service requests', width=25, bg='#801213', fg="#f5f5f5", command=roomservice_txt_show).place(x=660, y=500)
    Button(admin_tk, text='Back', width=25, bg='#801213', fg="#f5f5f5", command=admin_tk.destroy).place(x=660, y=600)

    admin_tk.mainloop()


#This function displays Student menu interface.
def user_login(username):

    global UserLogin

    UserLogin = Tk()
    UserLogin.geometry("1920x1080")
    UserLogin.title('Student Menu')

    T = tk.Text(UserLogin, height=1, width=26)
    T.config(font=('Helvatical bold', 15))
    T.pack()
    T.insert(tk.END, f"    Welcome  {username}")

    Button(UserLogin, text='Complain', width=25, bg='#801213', fg="#f5f5f5", command=partial(complains_func, f'{username}')).place(x=660, y=200)
    Button(UserLogin, text='Anonymous Complain', width=25, bg='#801213', fg="#f5f5f5", command=partial(complains_func, "Anonymous")).place(x=660, y=300)
    Button(UserLogin, text='Food Menu', width=25, bg='#801213', fg="#f5f5f5", command=FoodMenu_Show).place(x=660, y=400)
    Button(UserLogin, text='Request Service', width=25, bg='#801213', fg="#f5f5f5", command=room_service_show).place(x=660, y=500)
    Button(UserLogin, text='Change Password', width=25, bg='#801213', fg="#f5f5f5", command=change_pass_show).place(x=660, y=600)
    Button(UserLogin, text='Back', width=25, bg='#801213', fg="#f5f5f5", command=UserLogin.destroy).place(x=660, y=700)
    UserLogin.mainloop()


#This function displays QR code scanner menu interface.
def scan():

    Scan = Toplevel(home)
    Scan.geometry("1920x1080")
    Scan.title('QR code scanner')

    Button(Scan, text='Entry To Hostel', width=15, bg='#801213', fg="#f5f5f5", command=partial(scanner, "Enter")).place(relx=0.44, rely=0.36, anchor=CENTER)
    Button(Scan, text='Exit From Hostel', width=15, bg='#801213', fg="#f5f5f5", command=partial(scanner, "Exit")).place(relx=0.556, rely=0.36, anchor=CENTER)
    Button(Scan, text='Back', width=10, bg='#801213', fg="#f5f5f5", command=Scan.destroy).place(relx=0.498, rely=0.5, anchor=CENTER)

    Scan.mainloop()


def room_service_save():

    database = (r"database.xlsx")
    data = pd.read_excel(database)
    username_list = data["NAME"].to_list()
    room_list = data["Room Number"].to_list()
    index_no = username_list.index(user.get())
    room_no = room_list[index_no]

    with open('Room_service.txt', "a") as comp:
        comp.write(f"-->{room_no}\t{y}\n")
    if messagebox.showinfo("Room Service", "Room service request saved successfully."):
        service_show.destroy()
        UserLogin.destroy()
        Login.destroy()


def room_service_days(l, x):

    global y
    l.append(x)
    l = list(set(l))
    y = ", ".join(l)
    Label(service_show, text=f"{y}").place(x=560, y=100)


def room_service_show():

    global service_show

    l=[]

    service_show = Tk()
    service_show.geometry("1920x1080")
    service_show.title('Change password')
    Button(service_show, text='Monday', width=20, bg='#801213', fg="#f5f5f5", command=partial(room_service_days, l, "Monday")).place(x=660, y=150)
    Button(service_show, text='Tuesday', width=20, bg='#801213', fg="#f5f5f5", command=partial(room_service_days, l, "Tuesday")).place(x=660, y=200)
    Button(service_show, text='Wednesday', width=20, bg='#801213', fg="#f5f5f5", command=partial(room_service_days, l, "Wednesday")).place(x=660, y=250)
    Button(service_show, text='Thursday', width=20, bg='#801213', fg="#f5f5f5", command=partial(room_service_days, l, "Thursday")).place(x=660, y=300)
    Button(service_show, text='Friday', width=20, bg='#801213', fg="#f5f5f5", command=partial(room_service_days, l, "Friday")).place(x=660, y=350)
    Button(service_show, text='Saturday', width=20, bg='#801213', fg="#f5f5f5", command=partial(room_service_days, l, "Saturday")).place(x=660, y=400)
    Button(service_show, text='Sunday', width=20, bg='#801213', fg="#f5f5f5", command=partial(room_service_days, l, "Sunday")).place(x=660, y=450)
    Button(service_show, text='Save', width=15, bg='#801213', fg="#f5f5f5",  command=room_service_save).place(x=750, y=510)
    Button(service_show, text='Back', width=15, bg='#801213', fg="#f5f5f5", command=service_show.destroy).place(x=600, y=510)
    service_show.mainloop()


#This function displays Complain adding interface.
def complains_func(name):

    global complain_entry, Complain
    Complain = Toplevel(home)
    Complain.geometry("1920x1080")
    Complain.title('Complain')

    Label(Complain, text='Enter your complain here').place(relx=0.44, rely=0.37, anchor=CENTER)
    complain_entry = StringVar()
    Entry(Complain, textvariable=complain_entry).place(relx=0.53, rely=0.37, anchor=CENTER)
    Button(Complain, text='Submit', width=10, bg='#801213', fg="#f5f5f5", command=partial(save_complain, name)).place(relx=0.556, rely=0.5, anchor=CENTER)
    Button(Complain, text='Back', width=10, bg='#801213', fg="#f5f5f5", command=Complain.destroy).place(relx=0.45, rely=0.5, anchor=CENTER)
    Complain.mainloop()


#This function displays Deleting student interface.
def del_student():

    global del_std
    del_std = Toplevel(home)
    del_std.geometry("1920x1080")
    del_std.title('Delete student')
    user = StringVar()
    Label(del_std, text='Username').place(x=640, y=350)
    Entry(del_std, textvariable=user).place(x=750, y=350)
    Button(del_std, text='Delete', width=10, bg='#801213', fg="#f5f5f5", command=partial(save_del_student, user)).place(x=800, y=450)
    Button(del_std, text='Back', width=10, bg='#801213', fg="#f5f5f5", command=del_std.destroy).place(x=630, y=450)
    del_std.mainloop()


#This function delete student's information from database.
def save_del_student(name):

    name = name.get()
    df = pd.read_excel("database.xlsx")
    username_list = df["NAME"].to_list()
    if name in username_list:
        index_no = username_list.index(name)
        df = df.drop(index_no, axis=0)
        df.to_excel("database.xlsx", index=False)
        messagebox.showinfo("STUDENT DELETED", "Student has been removed")
    else:
        messagebox.showerror("STUDENT NOT DELETED", "No student as entered")
    del_std.destroy()


#This function adds student's information to database.
def save_add_student(name, contact, room, password):

    name = name.get()
    contact = contact.get()
    room = room.get()
    password = password.get()
    df = pd.read_excel("database.xlsx")
    df = df.append({"NAME": name, "Contact Number": contact, "Room Number": room, "Password": password}, ignore_index=True)
    df.to_excel("database.xlsx", index=False)
    add_std.destroy()
    messagebox.showinfo("STUDENT ADDED", "Student has been added successfully.")


#This function displays Adding student interface.
def add_student():

    global add_std
    add_std = Toplevel(home)
    add_std.geometry("1920x1080")
    add_std.title('Add student')

    user = StringVar()
    contact = StringVar()
    room = StringVar()
    passw = StringVar()

    Label(add_std, text='Username').place(x=640, y=250)
    Label(add_std, text='Contact').place(x=640, y=300)
    Label(add_std, text='Room').place(x=640, y=350)
    Label(add_std, text='Password').place(x=640, y=400)
    Entry(add_std, textvariable=user).place(x=750, y=250)
    Entry(add_std, textvariable=contact).place(x=750, y=300)
    Entry(add_std, textvariable=room).place(x=750, y=350)
    Entry(add_std, textvariable=passw).place(x=750, y=400)
    Button(add_std, text='Add', width=10, bg='#801213', fg="#f5f5f5", command=partial(save_add_student, user, contact, room, passw)).place(x=800, y=450)
    Button(add_std, text='Back', width=10, bg='#801213', fg="#f5f5f5", command=add_std.destroy).place(x=630, y=450)
    add_std.mainloop()


#This function takes complains from students.
def save_complain(name):

    complainlog = complain_entry.get()
    with open('complains.txt', "a") as comp:
        comp.write(f"-->{name}\t{complainlog}\n")
    if messagebox.showinfo("Complain", "Complain saved successfully."):
        Complain.destroy()
        UserLogin.destroy()
        Login.destroy()


#This function displays Password changing interface.
def change_pass_show():

    global changepass
    changepass = Toplevel(home)
    changepass.geometry("1920x1080")
    changepass.title('Change password')

    new_pass = StringVar()

    Label(changepass, text='Password').place(x=640, y=400)
    Entry(changepass, textvariable=new_pass).place(x=750, y=400)
    Button(changepass, text='Change', width=10, bg='#801213', fg="#f5f5f5", command=partial(change_pass, new_pass)).place(x=800,y=450)
    Button(changepass, text='Back', width=10, bg='#801213', fg="#f5f5f5", command=changepass.destroy).place(x=630, y=450)
    changepass.mainloop()


#This function changes password of student.
def change_pass(new_pass):

    new_pass = new_pass.get()
    df = pd.read_excel("database.xlsx")
    df.loc[index_no, "Password"] = new_pass
    df.to_excel("database.xlsx", index=False)
    changepass.destroy()
    UserLogin.destroy()
    Login.destroy()
    messagebox.showinfo("Password changed", "Password changed successfully")


#This function verifies username and password.
def validateLogin():

    global index_no
    username = user.get()
    password = passw.get()

    if username == "ADMIN" and password == "admin":
        admin()
    else:
        database = (r"database.xlsx")
        data = pd.read_excel(database)
        username_list = data["NAME"].to_list()
        password_list = data["Password"].to_list()
        if username in username_list:
            index_no = username_list.index(username)
            if password == password_list[index_no]:
                Login.destroy()
                user_login(username)

            else:
                if messagebox.askretrycancel("Invalid Login", "Invalid username or password"):
                    Login.destroy()
                    login()
        else:
            if messagebox.askretrycancel("Invalid Login", "Username does not exist"):
                Login.destroy()
                login()


database = (r"database.xlsx")
data = pd.read_excel(database)
names = data["NAME"].to_list()

# to show image on home page
canvas = Canvas(home, width=1500, height=700)
canvas.pack()
img = (Image.open("images\AUlogo.png"))
resized_image = img.resize((150,150), Image.ANTIALIAS)
new_image = ImageTk.PhotoImage(resized_image)
canvas.create_image(10, 10, anchor=NW, image=new_image)

Label(home, text='Under guidance of Kuntal Sir').place(x=20, y=750)
Label(home, text='Created by Shrey Bhadja,Jeel Kadivar,Milan Godhaviya').place(x=1220, y=750)
entries = StringVar()
button1 = Button(home, text='Scan', width=25, bg='#801213', fg="#f5f5f5", command=scan).place(x=660, y=200)
button2 = Button(home, text='Login', width=25, bg='#801213', fg="#f5f5f5", command=login).place(x=660, y=300)
button3 = Button(home, text='Close', width=25, bg='#801213', fg="#f5f5f5", command=home.destroy).place(x=660, y=400)
# separator = ttk.Separator(home, orient="vertical").grid(column=2, row=0, rowspan=10, sticky='ns')

home.mainloop()