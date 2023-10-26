import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter.ttk import Combobox

import mysql.connector

# подключение к бд
db = mysql.connector.connect(
    host="localhost",
    user="alisa",
    password="alisa24462",
    database="contr"
)

cur = db.cursor()


def create_new_win(name, role):
    # создание второго окна
    root = tk.Tk()
    root.geometry('300x200')
    root.title('ЦПКиО им. Маяковского')

    cur.execute("Select name_role from role where id_role = %s",(role,))
    role = cur.fetchall()[0][0]

    name_label = tk.Label(root, text=f'{name} {role}')
    name_label.pack(pady=15)

    order_button = tk.Button(root, text='Create order', command=create_order)
    order_button.pack()

    root.mainloop()


def create_order():
    def get_last_id():
        cur.execute('SELECT MAX(id_order) FROM ordder')
        last_order_number = cur.fetchone()[0]
        return last_order_number if last_order_number else 0

    def handle_order_id(*args):
        data_id = int(id_entry.get())
        cur.execute("""SELECT id_order from ordder""")
        data = cur.fetchall()
        print(data==[], data_id)
        if data == []:
            data = [0]
        if data_id == data[0]:
            messagebox.showinfo('этот id уже есть')
        else:
            add_client_and_services_fields(data_id)

    def add_client_and_services_fields(data_id):
        # Создаем метку и поле для выбора клиента
        client_label = tk.Label(order_window, text="Выберите клиента:")
        client_label.pack()

        # вставляем клиентов
        users = []
        cur.execute("""SELECT name, surname from client""")
        data = cur.fetchall()
        for i in range(len(data)):
            users.append(f'{data[i][0]} {data[i][1]}')
        users.append('Добавить клиента')
        print(users)
        client_combobox = ttk.Combobox(order_window, values=users)
        client_combobox.pack()

        # создание окна создания юзера если выбрано Add user
        def on_change_selection(event):
            if client_combobox.get() == 'Добавить клиента':
                new_user = tk.Tk()
                new_user.geometry('300x300')

                mail_l = tk.Label(new_user, text='E-mail')
                mail_l.pack()
                mail_e = tk.Entry(new_user)
                mail_e.pack()

                name_l = tk.Label(new_user, text='Имя')
                name_l.pack()
                name_e = tk.Entry(new_user)
                name_e.pack()

                surname_l = tk.Label(new_user, text='Фамилия')
                surname_l.pack()
                surname_e = tk.Entry(new_user)
                surname_e.pack()

                adres_l = tk.Label(new_user, text='Адрес')
                adres_l.pack()
                adres_e = tk.Entry(new_user)
                adres_e.pack()

                birthday_l = tk.Label(new_user, text='День рождения')
                birthday_l.pack()
                birthday_e = tk.Entry(new_user)
                birthday_e.pack()

                passport_l = tk.Label(new_user, text='Паспорт')
                passport_l.pack()
                passport_e = tk.Entry(new_user)
                passport_e.pack()

                number_l = tk.Label(new_user, text='Номер')
                number_l.pack()
                number_e = tk.Entry(new_user)
                number_e.pack()

                btn = tk.Button(new_user, text='добавить',
                                command=lambda: insert(name_e.get(), surname_e.get(), adres_e.get(), birthday_e.get(),
                                                       passport_e.get(), number_e.get()))
                btn.pack()

                def insert(name_u, surname_u, adres, birthday, passport, number):
                    cur.execute("""Insert into client(name, surname, address, date_birthday, passport, number) 
                                    VALUES ('%s', '%s','%s', '%s','%s', '%s')"""
                                % (name_u, surname_u, adres, birthday, passport, number))
                    db.commit()
                    users.insert(-1, f'{name_u} {surname_u}')
                    client_combobox.config(values=users)
                    new_user.destroy()

        # привязка команды
        client_combobox.bind("<<ComboboxSelected>>", on_change_selection)


        service_names = []
        cur.execute("""SELECT name from service""")

        for _ in cur.fetchall():
            service_names.append(f'{_[0]}')

        services_listbox = tk.Listbox(order_window, selectmode=tk.MULTIPLE)
        for service_name in service_names:
            services_listbox.insert(tk.END, service_name)
        services_listbox.pack()
        selected_services_array = []

        def save_order_with_services():
            selected_services = [services_listbox.get(i) for i in services_listbox.curselection()]
            selected_services_array.extend(selected_services)
            print("Выбранные сервисы:", selected_services_array)
            print(selected_services_array)
            if not selected_services_array:
                messagebox.showerror("Ошибка", "Выберите хотя бы одну услугу")
            else:
                data_client = client_combobox.get()
                data_client = data_client.split()[0]
                print(type(data_id), data_id)
                print(type(data_client),data_client)
                cur.execute("SELECT id_client FROM client WHERE name = %s", (data_client,))
                # cur.execute("SELECT id_client from client where name = ?", (data_client,))
                client_id = cur.fetchall()[0][0]
                print('client',client_id)

                # Создаем заказ в базе данных
                cur.execute("INSERT INTO ordder (id_order,client) VALUES (%s,%s)",(data_id,client_id))
                db.commit()

                # Получаем ID последнего добавленного заказа
                cur.execute("SELECT MAX(id_order) FROM ordder")
                order_id = cur.fetchone()[0]
                print("order_id",order_id)

                # Записываем выбранные услуги для заказа в базу данных
                for service in selected_services_array:
                    print("service", service)
                    cur.execute("SELECT id_service from service where name = %s", (service,))
                    service_id = cur.fetchone()[0]
                    print(service_id)
                    cur.execute("INSERT INTO compound_order (id_order, service) VALUES (%s, %s)",
                                (order_id, service_id))

                db.commit()
        save_button = tk.Button(order_window, text="Сохранить заказ", command=save_order_with_services)
        save_button.pack()

    order_window = tk.Tk()
    order_window.geometry("500x500")
    # Определяем последний номер заказа
    last_id = get_last_id()

    id_label = tk.Label(order_window, text='id заказа')
    id_label.pack()
    id_entry = tk.Entry(order_window)
    id_entry.insert(0, last_id + 1)
    id_entry.bind("<Return>", handle_order_id)
    id_entry.pack()

    order_window.mainloop()
