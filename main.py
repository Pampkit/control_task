import tkinter as tk
from tkinter import messagebox

import mysql.connector

from admin import create_new_win

#подключение к бд
db = mysql.connector.connect(
    host="localhost",
    user="alisa",
    password="alisa24462",
    database="contr"
)

cur = db.cursor()

root = tk.Tk()

def show_password():
    password_entry.config(show="")

root.geometry('300x300')
root.title('ЦПКиО им. Маяковского')
login_label = tk.Label(root, text="Введите логин")
login_label.pack()
login_entry = tk.Entry(root)
login_entry.pack()

password_label = tk.Label(root, text="Введите пароль")
password_label.pack()
password_entry = tk.Entry(root,show='*')
password_entry.pack()
show_button = tk.Button(root, text="Показать пароль", command=show_password)
show_button.pack()

go_button = tk.Button(root, text='Войти',command=lambda: go_to_main_window(login_entry.get(),password_entry.get()))
go_button.pack()



def go_to_main_window(login,password):
    cur.execute("""SELECT * FROM user WHERE login='%s' and password='%s'""" % (login, password))
    data = cur.fetchone()
    if data is None:
        messagebox.showerror(title='Error', message='Data incorrect')
    else:
        root.destroy()
        create_new_win(data[1], data[4])


root.mainloop()
