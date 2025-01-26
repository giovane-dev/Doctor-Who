import mysql.connector as MySql
from tkinter import *
from tkinter import ttk, messagebox
from PIL import ImageTk, Image

def connect_to_database():
    conn=MySql.connect(
        host="localhost",
        user="root",
        password="",
        database="pharmacy_system",
        port=4000
    )
    return conn

def setup_database():
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS medicine(
                   id INT PRIMARY KEY AUTO_INCREMENT,
                   name VARCHAR(255) NOT NULL,
                   price DECIMAL(10,2) NOT NULL,
                   quantity INT NOT NULL,
                   code VARCHAR(255) NOT NULL
                   )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS customer(
                   id INT PRIMARY KEY AUTO_INCREMENT,
                   customer_name VARCHAR(255) NOT NULL,
                   phone VARCHAR(255) NOT NULL
                   )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS seller(
                   id INT PRIMARY KEY AUTO_INCREMENT,
                   seller_name VARCHAR(255) NOT NULL,
                   phone VARCHAR(255) NOT NULL,
                   email VARCHAR(255) NOT NULL,
                   company_name VARCHAR(255) NOT NULL
                   )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS cart(
                   id INT PRIMARY KEY AUTO_INCREMENT,
                   medicine_id INT NOT NULL,
                   medicine_name VARCHAR(255) NOT NULL,
                   quantity INT NOT NULL,
                   price DECIMAL(10,2),
                   total DECIMAL(10,2) NOT NULL,
                   customer_id INT,
                   customer_name VARCHAR(255) NOT NULL,
                   FOREIGN KEY (customer_id) REFERENCES customer(id) ON DELETE CASCADE,
                   FOREIGN KEY (medicine_id) REFERENCES medicine(id) ON DELETE CASCADE
                   )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS sales(
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    medicine_id INT,
                    medicine_name VARCHAR(255) NOT NULL,
                    price DECIMAL(10,2),
                    quantity INT NOT NULL,
                    total DECIMAL(10,2),
                    customer_id INT,
                    customer_name VARCHAR(255),
                    FOREIGN KEY (customer_id) REFERENCES customer(id) ON DELETE CASCADE,
                    FOREIGN KEY (medicine_id) REFERENCES medicine(id) ON DELETE CASCADE
            )""")    
    cursor.execute("""CREATE TABLE IF NOT EXISTS pur_view(
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    medicine_id INT,
                    medicine_name VARCHAR(255) NOT NULL,
                    price DECIMAL(10,2),
                    quantity INT NOT NULL,
                    total DECIMAL(10,2),
                    seller_id INT,
                    seller_name VARCHAR(255),
                    FOREIGN KEY (seller_id) REFERENCES seller(id) ON DELETE CASCADE,
                    FOREIGN KEY (medicine_id) REFERENCES medicine(id) ON DELETE CASCADE
            )""")    
    cursor.execute("""CREATE TABLE IF NOT EXISTS purchase(
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    medicine_id INT NOT NULL,
                    medicine_name VARCHAR(255) NOT NULL,
                    price DECIMAL(10,2) NOT NULL,
                    quantity INT NOT NULL,
                    total DECIMAL(10,2),
                    seller_id INT NOT NULL,
                    seller_name VARCHAR(255) NOT NULL,
                    FOREIGN KEY (seller_id) REFERENCES seller(id) ON DELETE CASCADE,
                    FOREIGN KEY (medicine_id) REFERENCES medicine(id) ON DELETE CASCADE

            ) """)  
                             
setup_database()  

root=Tk()
root.title("Pharmacy System")
root.state("zoomed")
root.iconbitmap('icon.ico')
background = ImageTk.PhotoImage(Image.open('bg.jpg'))
background_label = Label(root, image=background)
background_label.pack(fill="both", expand=True)

main_menu =Menu(root)
root.config(menu=main_menu)

def center_window(window, width, height):
     screen_width = window.winfo_screenwidth() 
     screen_height = window.winfo_screenheight() 
     x = (screen_width // 2) - (width // 2) 
     y = (screen_height // 2) - (height // 2) 
     window.geometry(f'{width}x{height}+{x}+{y}')

#=================================================================CUSTOMER MENU================================================================

def customer_insert():
    customer_insert_window = Toplevel(root)
    customer_insert_window.iconbitmap('icon.ico')
    customer_insert_window.config(bg='#95c1ca')
    center_window(customer_insert_window, 450, 200)
    customer_insert_window.resizable(0,0)
    customer_insert_window.grab_set()
    customer_insert_window.title("Customers | Add new customers")

    def send_to_database():
        conn=connect_to_database()
        cursor=conn.cursor()
        customer_name = customer_name_entry.get()
        phone = customer_phone_entry.get()
        if customer_name.strip():
            cursor.execute(f"INSERT INTO customer(customer_name, phone) VALUE('{customer_name}', '{phone}')")
            conn.commit()
            conn.close()
            customer_name_entry.delete(0, END)
            customer_name_entry.insert(0, "")
            customer_phone_entry.delete(0, END)
            messagebox.showinfo("Success","Customer Added successfully") 
            customer_insert_window.destroy()  
        else:
            messagebox.showerror("Error","Please fill all fields", parent=customer_insert_window)

    # labels
    empty=Label(customer_insert_window, text="  "*10,bg='#95c1ca')
    empty.grid(row=0, column=0)
    empty2=Label(customer_insert_window, text="  "*10,bg='#95c1ca')
    empty2.grid(row=0, column=4)
    customer_name_label=Label(customer_insert_window, text="customer name", font=("arial", 11),bg='#95c1ca')
    customer_name_label.grid(row=1, column=2, padx=10, pady=15)
    customer_phone_label=Label(customer_insert_window, text="customer phone", font=("arial", 11),bg='#95c1ca')
    customer_phone_label.grid(row=2, column=2, padx=10, pady=15)
    #Entries
    customer_name_entry=Entry(customer_insert_window, width=20, font=("arial", 11))
    customer_name_entry.grid(row=1, column=3, padx=10, pady=15)
    customer_phone_entry=Entry(customer_insert_window, width=20, font=("arial", 11))
    customer_phone_entry.grid(row=2, column=3, padx=10, pady=15)
    #Buttons
    submit=Button(customer_insert_window, text="Add", command=send_to_database, width=10)
    submit.grid(row=4, column=2, padx=10, pady=15)
    cancel=Button(customer_insert_window, text="Cancel", command=customer_insert_window.destroy, width=10)
    cancel.grid(row=4, column=3, padx=10, pady=15)


def customer_edit():
    customer_edit_window = Toplevel(root)
    customer_edit_window.iconbitmap('icon.ico')
    customer_edit_window.config(bg='#95c1ca')
    center_window(customer_edit_window, 500, 480)
    customer_edit_window.resizable(0,0)
    customer_edit_window.grab_set()
    customer_edit_window.title("Customers | Edit existing customers")
    style = ttk.Style()
    style.theme_use("default")

    #Functions

    def fetch_data():
        try:
            conn=connect_to_database()
            cursor=conn.cursor()
            cs_id=customer_id_entry.get()
            cursor.execute(f"SELECT * FROM customer WHERE id={cs_id}")
            data=cursor.fetchone()

            if data:
                cs_name_var.set(data[1],)
                cs_phone_var.set(data[2],)
            else:
                messagebox.showerror("Error","Customer ID not found")
                conn.close()
                customer_id_entry.delete(0, END)
                customer_id_entry.insert(0,"")
                customer_name_entry.delete(0, END)
                customer_phone_entry.delete(0, END)
        except Exception as exx:
            messagebox.showerror("Error", "Missing ID",parent=customer_edit_window)


    def update_customers():
        try:
            conn = connect_to_database()
            cursor = conn.cursor()
            cs_id = customer_id_entry.get()
            cs_name = cs_name_var.get()
            cs_phone = cs_phone_var.get()
            cursor.execute(f"UPDATE customer SET customer_name='{cs_name}', phone='{cs_phone}' WHERE id={cs_id}")
            conn.commit()
            conn.close()
            messagebox.showinfo("Success","Customer updated successfully",parent=customer_edit_window)
            customer_id_entry.delete(0, END)
            customer_name_entry.delete(0, END)
            customer_phone_entry.delete(0, END)
            customer_id_entry.insert(0,"")

            #   REFRESH THE TREE VIEW
            conn=connect_to_database()
            cursor=conn.cursor()
            cursor.execute("SELECT * FROM customer")
            rows = cursor.fetchall()
            count = 0
            for item in my_tree.get_children():
                my_tree.delete(item)
            for row in rows:
                
                if count % 2 == 0:
                    my_tree.insert('', 'end', values=(row[0], row[1], row[2]), tags=('even',))
                else:
                    my_tree.insert('', 'end', values=(row[0], row[1], row[2]), tags=('odd',))
                conn.close()
                count +=1
        except Exception as exc:
            messagebox.showerror("Error", "Missing Data",parent=customer_edit_window)

    def delete_customer():
        try:
            root.bell()
            response = messagebox.askokcancel("Warning", "This will delete a customer", icon="warning",parent=customer_edit_window)
            if response:
                x = my_tree.selection()[0]
                cs_id = my_tree.item(x, 'values')[0]
                my_tree.delete(x)
                conn = connect_to_database()
                cursor = conn.cursor()
                cursor.execute(f"DELETE FROM customer WHERE id={cs_id}")
                conn.commit()
                conn.close()
                messagebox.showinfo("Success","Customer deleted successfully",parent=customer_edit_window)    
        except Exception as ex:
            messagebox.showerror("Error", "No Record Selected",parent=customer_edit_window)

    #setup the view
    my_tree = ttk.Treeview(customer_edit_window,)
    my_tree['columns'] = ('id','customer_name', 'phone')
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("id", anchor=CENTER, width=80, minwidth=50)
    my_tree.column("customer_name", anchor=CENTER, width=200, minwidth=150)
    my_tree.column("phone", anchor=CENTER, width=200, minwidth=150)

    my_tree.heading("#0", text='', anchor=W)
    my_tree.heading('id', text="ID", anchor=CENTER)
    my_tree.heading('customer_name', text="Customer Name", anchor=CENTER)
    my_tree.heading('phone', text="Phone Number", anchor=CENTER)
    my_tree.tag_configure('odd', background="white")
    my_tree.tag_configure('even', background='lightblue')

    #Fetch data
    conn=connect_to_database()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM customer")
    rows = cursor.fetchall()
    count=0
    for row in rows:
        if count % 2 == 0:
            my_tree.insert('', 'end', values=(row[0], row[1], row[2]), tags=('even',))
        else:
             my_tree.insert('', 'end', values=(row[0], row[1], row[2]), tags=('odd',))
        conn.close()
        count += 1

    #       update
    update_frame=LabelFrame(customer_edit_window, bg='#95c1ca',text="Update")
    #labels
    customer_id_label=Label(update_frame, text="customer id", font=("arial", 11),bg='#95c1ca')
    customer_id_label.grid(row=0, column=0, padx=5, pady=5)
    customer_name_label=Label(update_frame, text="customer name", font=("arial", 11),bg='#95c1ca')
    customer_name_label.grid(row=0, column=1, padx=5, pady=5)
    customer_phone_label=Label(update_frame, text="customer phone", font=("arial", 11),bg='#95c1ca')
    customer_phone_label.grid(row=0, column=2, padx=5, pady=5)
    #entries
    customer_id_entry=Entry(update_frame, width=18, font=("arial", 11))
    customer_id_entry.grid(row=1, column=0, padx=5, pady=5)
    cs_name_var=StringVar()
    customer_name_entry=Entry(update_frame, width=18,textvariable=cs_name_var, font=("arial", 11))
    customer_name_entry.grid(row=1, column=1, padx=5, pady=5)
    cs_phone_var=StringVar()
    customer_phone_entry=Entry(update_frame,textvariable=cs_phone_var, width=18, font=("arial", 11))
    customer_phone_entry.grid(row=1, column=2, padx=5, pady=5)
    #button
    customer_fetch_button=Button(update_frame, text="Fetch", width=15, command=fetch_data)
    customer_fetch_button.grid(row=2, column=0, padx=5, pady=10)
    customer_update_button=Button(update_frame, text="Update",width=15, command=update_customers, bg='#1bf254')
    customer_update_button.grid(row=2, column=2, padx=5, pady=10)



    # Buttons' Frame
    buttons_frame = Frame(customer_edit_window, bg='#95c1ca')
    buttons_frame.pack(side=BOTTOM, fill=X, padx=5, pady=5)
    
    empty_area1=Label(buttons_frame, bg='#95c1ca', width=7)
    customer_delete_button=Button(buttons_frame,bg='red', fg='white', width=18, text='Delete',command=delete_customer)
    cancel_button=Button(buttons_frame, width=18, command=customer_edit_window.destroy, text='Cancel')
    empty_area2=Label(buttons_frame, bg='#95c1ca', width=7)

    #pack buttons
    empty_area1.grid(row=0,column=0,pady=5, padx=5)
    customer_delete_button.grid(row=0, column=1,pady=5,padx=25)
    cancel_button.grid(row=0,column=2, pady=5,padx=25)
    empty_area2.grid(row=0, column=3, pady=5, padx=5)


    #packing data   
    my_tree.pack(pady=10)
    update_frame.pack(pady=10)
    buttons_frame.pack(fill=X, pady=15)
    

def customer_view():
    customer_view_window=Toplevel(root)
    customer_view_window.iconbitmap('icon.ico')
    customer_view_window.config(bg='#95c1ca')
    center_window(customer_view_window, 500, 350)
    customer_view_window.title("Customers | View all customers")
    customer_view_window.grab_set()
    style = ttk.Style()
    style.theme_use("default")
    

    #setup the view
    my_tree = ttk.Treeview(customer_view_window,)
    my_tree['columns'] = ('id','customer_name', 'phone')
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("id", anchor=CENTER, width=80, minwidth=50)
    my_tree.column("customer_name", anchor=CENTER, width=200, minwidth=150)
    my_tree.column("phone", anchor=CENTER, width=200, minwidth=150)

    my_tree.heading("#0", text='', anchor=W)
    my_tree.heading('id', text="ID", anchor=CENTER)
    my_tree.heading('customer_name', text="Customer Name", anchor=CENTER)
    my_tree.heading('phone', text="Phone Number", anchor=CENTER)
    my_tree.pack(pady=10)

    my_tree.tag_configure('odd', background="white")
    my_tree.tag_configure('even', background='lightblue')
    #Fetch data
    conn=connect_to_database()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM customer")
    rows = cursor.fetchall()
    count=0
    for row in rows:
        if count % 2 == 0:
            my_tree.insert('', 'end', values=(row[0], row[1], row[2]), tags=('even',))
        else:
             my_tree.insert('', 'end', values=(row[0], row[1], row[2]), tags=('odd',))
        conn.close()
        count += 1

    my_tree.pack(fill='both', expand=True, pady=10,padx=10)

#=================================================================SUPPLIER MENU================================================================

def seller_insert():
    seller_insert_window = Toplevel(root)
    seller_insert_window.iconbitmap('icon.ico')
    seller_insert_window.config(bg='#95c1ca')
    center_window(seller_insert_window, 450, 330)
    seller_insert_window.resizable(0,0)
    seller_insert_window.grab_set()
    seller_insert_window.title("Supplier | Add new supplier")

    def send_to_database():
        conn=connect_to_database()
        cursor=conn.cursor()
        seller_name=seller_name_entry.get()
        seller_phone=seller_phone_entry.get()
        seller_email=seller_email_entry.get()
        company_name=seller_company_name_entry.get()

        if seller_name.strip() and seller_phone.strip() and seller_email.strip() and company_name.strip():
            cursor.execute(f"""INSERT INTO seller(seller_name, phone, email, company_name)
                        VALUES
                        ('{seller_name}', '{seller_phone}', '{seller_email}', '{company_name}')
                        """)
            conn.commit()
            conn.close()
            seller_insert_window.destroy()
            messagebox.showinfo("Success","Supplier Added successfully")   
        else:
            messagebox.showerror("Error","Please fill all fields", parent=seller_insert_window)

    # labels
    empty=Label(seller_insert_window, text="  "*10,bg='#95c1ca')
    empty.grid(row=0, column=0)
    # empty2=Label(seller_insert_window, text="  "*10,bg='#95c1ca')
    # empty2.grid(row=0, column=4)
    seller_name_label=Label(seller_insert_window, text="Supplier name", font=("arial", 11),bg='#95c1ca')
    seller_name_label.grid(row=1, column=2, padx=10, pady=15)
    seller_phone_label=Label(seller_insert_window, text="Supplier phone", font=("arial", 11),bg='#95c1ca')
    seller_phone_label.grid(row=2, column=2, padx=10, pady=15)
    seller_email_label=Label(seller_insert_window, text="Supplier email", font=("arial", 11),bg='#95c1ca')
    seller_email_label.grid(row=3, column=2, padx=10, pady=15)
    seller_company_name_label=Label(seller_insert_window, text="Company name", font=("arial", 11),bg='#95c1ca')
    seller_company_name_label.grid(row=4, column=2, padx=10, pady=15)
    #Entries
    seller_name_entry=Entry(seller_insert_window, width=20, font=("arial", 11))
    seller_name_entry.grid(row=1, column=3, padx=10, pady=15)
    seller_phone_entry=Entry(seller_insert_window, width=20, font=("arial", 11))
    seller_phone_entry.grid(row=2, column=3, padx=10, pady=15)
    seller_email_entry=Entry(seller_insert_window, width=20, font=("arial", 11))
    seller_email_entry.grid(row=3, column=3, padx=10, pady=15)
    seller_company_name_entry=Entry(seller_insert_window, width=20, font=("arial", 11))
    seller_company_name_entry.grid(row=4, column=3, padx=10, pady=15)
    #Buttons
    submit=Button(seller_insert_window, text="Add", command=send_to_database, width=10)
    submit.grid(row=5, column=2, padx=10, pady=15)
    cancel=Button(seller_insert_window, text="Cancel", command=seller_insert_window.destroy, width=10)
    cancel.grid(row=5, column=3, padx=10, pady=15)

def seller_edit():
    seller_edit_window=Toplevel(root)
    seller_edit_window.iconbitmap('icon.ico')
    seller_edit_window.config(bg='#95c1ca')
    center_window(seller_edit_window, 910, 480)
    seller_edit_window.resizable(0,0)
    seller_edit_window.grab_set()
    seller_edit_window.title("Supplier | Edit existing suppliers")
    style= ttk.Style()
    style.theme_use("default")

    #Functions

    def fetch_seller_data():
        try:
            conn=connect_to_database()
            cursor=conn.cursor()
            s_id=seller_id_entry.get()
            cursor.execute(f"SELECT * FROM seller WHERE id={s_id}")
            data=cursor.fetchone()

            if data:
                s_name_var.set(data[1],)
                s_phone_var.set(data[2],)
                s_email_var.set(data[3],)
                s_company_name_var.set(data[4],)
            else:
                messagebox.showerror("Error","Supplier ID not found", parent=seller_edit_window)
                conn.close()
                seller_id_entry.delete(0, END)
                seller_id_entry.insert(0,"")
                seller_name_entry.delete(0, END)
                seller_phone_entry.delete(0, END)
                seller_email_entry.delete(0, END)
                seller_company_name_entry.delete(0, END)

        except Exception as exx:
            messagebox.showerror("Error", "Missing ID",parent=seller_edit_window)
    
    def update_seller():
        try:
            conn = connect_to_database()
            cursor = conn.cursor()
            s_id = seller_id_entry.get()
            s_name = s_name_var.get()
            s_phone = s_phone_var.get()
            s_email = s_email_var.get()
            s_company_name = s_company_name_var.get()
            if s_id.strip and s_name.strip() and s_phone.strip() and s_email.strip() and s_company_name.strip():
                supplier_found= False
                cursor.execute('SELECT id FROM seller')
                data = cursor.fetchall()
                for row in data:
                    if row[0] == int(s_id):
                        supplier_found = True
                        cursor.execute(f"UPDATE seller SET seller_name='{s_name}', phone='{s_phone}',email='{s_email}', company_name='{s_company_name}' WHERE id={s_id}")
                        conn.commit()
                        conn.close()
                        messagebox.showinfo("Success","Supplier updated successfully",parent=seller_edit_window)
                        seller_id_entry.delete(0, END)
                        seller_name_entry.delete(0, END)
                        seller_phone_entry.delete(0, END)
                        seller_email_entry.delete(0, END)
                        seller_company_name_entry.delete(0, END)
                        seller_id_entry.insert(0,"")
                if not supplier_found:
                    messagebox.showerror("Error","Supplier ID not found",parent=seller_edit_window)
            else:
                messagebox.showerror("Error","Please fill all fields",parent=seller_edit_window)

            #   REFRESH THE TREE VIEW
            conn=connect_to_database()
            cursor=conn.cursor()
            cursor.execute("SELECT * FROM seller")
            rows = cursor.fetchall()
            count = 0 
            for item in my_tree.get_children():
                my_tree.delete(item)
            for row in rows:
                if count % 2 == 0:
                    my_tree.insert('', 'end', values=(row[0], row[1], row[2],row[3],row[4]), tags=('even',))
                else:
                    my_tree.insert('', 'end', values=(row[0], row[1], row[2],row[3],row[4]), tags=('odd',))
                conn.close()
                count +=1
        except Exception as exc:
            messagebox.showerror("Error", "Missing Data",parent=seller_edit_window)

    #setup the view

    my_tree = ttk.Treeview(seller_edit_window,)
    my_tree['columns'] = ('id','customer_name', 'phone','email', 'company_name')
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("id", anchor=CENTER, width=80, minwidth=50)
    my_tree.column("customer_name", anchor=CENTER, minwidth=200)
    my_tree.column("phone", anchor=CENTER, minwidth=150)
    my_tree.column("email", anchor=CENTER, minwidth=200 )
    my_tree.column("company_name", anchor=CENTER, minwidth=150)

    my_tree.heading("#0", text='', anchor=W)
    my_tree.heading('id', text="ID", anchor=CENTER)
    my_tree.heading('customer_name', text="Supplier Name", anchor=CENTER)
    my_tree.heading('phone', text="Phone Number", anchor=CENTER)
    my_tree.heading('email', text="email", anchor=CENTER)
    my_tree.heading('company_name', text="Company name", anchor=CENTER)
    my_tree.tag_configure('odd', background="white")
    my_tree.tag_configure('even', background='lightblue')

     #Fetch data
    conn=connect_to_database()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM seller")
    rows = cursor.fetchall()
    count=0
    for row in rows:
        if count % 2 == 0:
            my_tree.insert('', 'end', values=(row[0], row[1], row[2],row[3],row[4]), tags=('even',))
        else:
             my_tree.insert('', 'end', values=(row[0], row[1], row[2],row[3],row[4]), tags=('odd',))
        conn.close()
        count += 1

     #       update
    update_frame=LabelFrame(seller_edit_window, bg='#95c1ca',text="Update")
    #labels
    selle_id_label=Label(update_frame, text="Supplier id", font=("arial", 11),bg='#95c1ca')
    selle_id_label.grid(row=0, column=0, padx=5, pady=5)
    selle_name_label=Label(update_frame, text="Supplier name", font=("arial", 11),bg='#95c1ca')
    selle_name_label.grid(row=0, column=1, padx=5, pady=5)
    seller_phone_label=Label(update_frame, text="Supplier phone", font=("arial", 11),bg='#95c1ca')
    seller_phone_label.grid(row=0, column=2, padx=5, pady=5)
    seller_email_label=Label(update_frame, text="Supplier email", font=("arial", 11),bg='#95c1ca')
    seller_email_label.grid(row=0, column=3, padx=5, pady=5)
    seller_company_label=Label(update_frame, text="Company name", font=("arial", 11),bg='#95c1ca')
    seller_company_label.grid(row=0, column=4, padx=5, pady=5)
    #entries
    seller_id_entry=Entry(update_frame, width=21, font=("arial", 11))
    seller_id_entry.grid(row=1, column=0, padx=5, pady=5)
    s_name_var=StringVar()
    seller_name_entry=Entry(update_frame, width=18,textvariable=s_name_var, font=("arial", 11))
    seller_name_entry.grid(row=1, column=1, padx=5, pady=5)
    s_phone_var=StringVar()
    seller_phone_entry=Entry(update_frame,textvariable=s_phone_var, width=21, font=("arial", 11))
    seller_phone_entry.grid(row=1, column=2, padx=5, pady=5)
    s_email_var=StringVar()
    seller_email_entry=Entry(update_frame,textvariable=s_email_var, width=21, font=("arial", 11))
    seller_email_entry.grid(row=1, column=3, padx=5, pady=5)
    s_company_name_var=StringVar()
    seller_company_name_entry=Entry(update_frame,textvariable=s_company_name_var, width=21, font=("arial", 11))
    seller_company_name_entry.grid(row=1, column=4, padx=5, pady=5)
    #button
    seller_fetch_button=Button(update_frame, text="Fetch", width=15, command=fetch_seller_data)
    seller_fetch_button.grid(row=2, column=1, padx=5, pady=10)
    seller_update_button=Button(update_frame, text="Update",width=15, bg='#1bf254',command=update_seller)
    seller_update_button.grid(row=2, column=3, padx=5, pady=10)    

    #packing data
    my_tree.pack(pady=10)
    update_frame.pack(pady=10)

    def delete_customer():
        try:
            root.bell()
            response = messagebox.askokcancel("Warning", "This will delete a supplier", icon="warning",parent=seller_edit_window)
            if response:
                x = my_tree.selection()[0]
                s_id = my_tree.item(x, 'values')[0]
                my_tree.delete(x)
                conn = connect_to_database()
                cursor = conn.cursor()
                cursor.execute(f"DELETE FROM seller WHERE id={s_id}")
                conn.commit()
                conn.close()
                messagebox.showinfo("Success","supplier deleted successfully",parent=seller_edit_window)    
        except Exception as ex:
            messagebox.showerror("Error", "No Record Selected",parent=seller_edit_window)


    buttons_frame = Frame(seller_edit_window, bg='#95c1ca')
    buttons_frame.pack(side=BOTTOM, fill=X, padx=5, pady=5)
    
    empty_area1=Label(buttons_frame, bg='#95c1ca', width=20)
    seller_delete_button=Button(buttons_frame,bg='red', fg='white', width=20, text='Delete',command=delete_customer)
    cancel_button=Button(buttons_frame, width=20, command=seller_edit_window.destroy, text='Cancel')
    empty_area2=Label(buttons_frame, bg='#95c1ca', width=20)

    #pack buttons
    empty_area1.grid(row=0,column=0,pady=5, padx=35)
    seller_delete_button.grid(row=0, column=1,pady=20,padx=40)
    cancel_button.grid(row=0,column=2, pady=20,padx=40)
    empty_area2.grid(row=0, column=3, pady=20, padx=40)    

def seller_view():
    seller_view_window=Toplevel(root)
    seller_view_window.iconbitmap('icon.ico')
    seller_view_window.config(bg='#95c1ca')
    center_window(seller_view_window, 910, 480)
    seller_view_window.grab_set()
    seller_view_window.title("Supplier | View existing suppliers")
    

    my_tree = ttk.Treeview(seller_view_window)
    my_tree['columns'] = ('id','customer_name', 'phone','email', 'company_name')
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("id", anchor=CENTER, width=80 , minwidth=50)
    my_tree.column("customer_name", anchor=CENTER ,minwidth=200)
    my_tree.column("phone", anchor=CENTER, minwidth=200)
    my_tree.column("email", anchor=CENTER, minwidth=200)
    my_tree.column("company_name", anchor=CENTER, minwidth=200)

    my_tree.heading("#0", text='', anchor=W)
    my_tree.heading('id', text="ID", anchor=CENTER)
    my_tree.heading('customer_name', text="Seller Name", anchor=CENTER)
    my_tree.heading('phone', text="Phone Number", anchor=CENTER)
    my_tree.heading('email', text="email", anchor=CENTER)
    my_tree.heading('company_name', text="Company name", anchor=CENTER)
    my_tree.tag_configure('odd', background="white")
    my_tree.tag_configure('even', background='lightblue')

     #Fetch data
    conn=connect_to_database()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM seller")
    rows = cursor.fetchall()
    count=0
    for row in rows:
        if count % 2 == 0:
            my_tree.insert('', 'end', values=(row[0], row[1], row[2],row[3],row[4]), tags=('even',))
        else:
             my_tree.insert('', 'end', values=(row[0], row[1], row[2],row[3],row[4]), tags=('odd',))
        conn.close()
        count += 1

    #packing data
    my_tree.pack(fill='both', expand=True, pady=10, padx=10)

 #=============================================================================================================================================

#=================================================================MEDICINE MENU================================================================

medicine_quantity=20

def insert_medicine():
    insert_medicine_window=Toplevel(root)
    insert_medicine_window.iconbitmap('icon.ico')
    insert_medicine_window.config(bg='#95c1ca')
    center_window(insert_medicine_window, 450, 300)
    insert_medicine_window.resizable(0,0)
    insert_medicine_window.grab_set()
    insert_medicine_window.title("Medicine | Insert new medicine")

    def send_to_database():
        conn=connect_to_database()
        cursor=conn.cursor()
        m_name=medicine_name_entry.get()
        m_price=medicine_price_entry.get()
        m_code=medicine_code_entry.get()
        if m_name.strip() and m_price.strip()  and m_code.strip():
            cursor.execute(f"""INSERT INTO medicine(name, price, quantity, code) 
                            VALUES ('{m_name}', {m_price}, {medicine_quantity}, '{m_code}') """)
            conn.commit()
            conn.close()
            messagebox.showinfo("Success","Medicine Added successfully") 
            insert_medicine_window.destroy()
        else:
            messagebox.showerror("Error","Please fill all fields", parent=insert_medicine_window)


    empty=Label(insert_medicine_window, text="  "*10,bg='#95c1ca')
    empty.grid(row=0, column=0)
    empty2=Label(insert_medicine_window, text="  "*10,bg='#95c1ca')
    empty2.grid(row=0, column=4)
    medicine_name_label=Label(insert_medicine_window, text="Medicine name", font=("arial", 11),bg='#95c1ca')
    medicine_name_label.grid(row=1, column=2, padx=10, pady=15)
    medicine_price_label=Label(insert_medicine_window, text="price", font=("arial", 11),bg='#95c1ca')
    medicine_price_label.grid(row=2, column=2, padx=10, pady=15)
    medicine_code_label=Label(insert_medicine_window, text="code", font=("arial", 11),bg='#95c1ca')
    medicine_code_label.grid(row=4, column=2, padx=10, pady=15)
    #Entries
    medicine_name_entry=Entry(insert_medicine_window, width=20, font=("arial", 11))
    medicine_name_entry.grid(row=1, column=3, padx=10, pady=15)
    medicine_price_entry=Entry(insert_medicine_window, width=20, font=("arial", 11))
    medicine_price_entry.grid(row=2, column=3, padx=10, pady=15)
    medicine_code_entry=Entry(insert_medicine_window, width=20, font=("arial", 11))
    medicine_code_entry.grid(row=4, column=3, padx=10, pady=15)
    #Buttons
    submit=Button(insert_medicine_window, text="Add", command=send_to_database, width=10)
    submit.grid(row=5, column=2, padx=10, pady=15)
    cancel=Button(insert_medicine_window, text="Cancel", command=insert_medicine_window.destroy, width=10)
    cancel.grid(row=5, column=3, padx=10, pady=15)

def medicine_edit():
    medicine_edit_window=Toplevel(root)
    medicine_edit_window.iconbitmap('icon.ico')
    medicine_edit_window.config(bg='#95c1ca')
    medicine_edit_window.resizable(0,0)
    medicine_edit_window.grab_set()
    medicine_edit_window.title("Medicine | Edit existing medicine")
    center_window(medicine_edit_window, 910, 480)
    style = ttk.Style()
    style.theme_use("default")

    #Functions

    def fetch_medicine_data():
        try:
            conn=connect_to_database()
            cursor=conn.cursor()
            m_id=medicine_id_entry.get()
            cursor.execute(f"SELECT * FROM medicine WHERE id={m_id}")
            data=cursor.fetchone()

            if data:
                m_name_var.set(data[1],)
                m_price_var.set(data[2],)
                m_quantity_var.set(data[3],)
                m_code_var.set(data[4],)
            else:
                messagebox.showerror("Error","Medicine ID not found", parent=medicine_edit_window)
                conn.close()
                medicine_id_entry.delete(0, END)
                medicine_id_entry.insert(0,"")
                medicine_name_entry.delete(0, END)
                medicine_price_entry.delete(0, END)
                medicine_quantity_entry.delete(0, END)
                medicine_code_entry.delete(0, END)

        except Exception as exx:
            messagebox.showerror("Error", "Missing ID",parent=medicine_edit_window)


    def update_medicine():
        try:
            conn = connect_to_database()
            cursor = conn.cursor()
            m_id = medicine_id_entry.get()
            m_name = m_name_var.get()
            m_price = m_price_var.get()
            m_quantity = m_quantity_var.get()
            m_code = m_code_var.get()
            if m_id.strip and m_name.strip() and m_code.strip():
                medicine_found=False
                cursor.execute('SELECT id FROM medicine')
                data = cursor.fetchall()
                for row in data:
                    if row[0] == int(m_id):
                        medicine_found = True
                        cursor.execute(f"UPDATE medicine SET name='{m_name}', price={m_price}, quantity={m_quantity}, code='{m_code}' WHERE id={m_id}")
                        conn.commit()
                        conn.close()
                        messagebox.showinfo("Success","Medicine updated successfully",parent=medicine_edit_window)
                        medicine_id_entry.delete(0, END)
                        medicine_name_entry.delete(0, END)
                        medicine_price_entry.delete(0, END)
                        medicine_quantity_entry.delete(0, END)
                        medicine_code_entry.delete(0, END)
                        medicine_id_entry.insert(0,"")
                if not medicine_found:
                    messagebox.showerror("Error","Medicine ID not found",parent=medicine_edit_window)
            else:
                messagebox.showerror("Error","Please fill all fields",parent=medicine_edit_window)

            #   REFRESH THE TREE VIEW
            conn=connect_to_database()
            cursor=conn.cursor()
            cursor.execute("SELECT * FROM medicine")
            rows = cursor.fetchall()
            count = 0
            for item in my_tree.get_children():
                my_tree.delete(item)
            for row in rows:
                if count % 2 == 0:
                    my_tree.insert('', 'end', values=(row[0], row[1], row[2],row[3],row[4]), tags=('even',))
                else:
                    my_tree.insert('', 'end', values=(row[0], row[1], row[2],row[3],row[4]), tags=('odd',))
                conn.close()
                count+=1
        except Exception as exc:
            messagebox.showerror(f"Error", exc ,parent=medicine_edit_window)

    def delete_medicine():
        try:
            root.bell()
            response = messagebox.askokcancel("Warning", "This will delete a medicine", icon="warning",parent=medicine_edit_window)
            if response:
                x = my_tree.selection()[0]
                m_id = my_tree.item(x, 'values')[0]
                my_tree.delete(x)
                conn = connect_to_database()
                cursor = conn.cursor()
                cursor.execute(f"DELETE FROM medicine WHERE id={m_id}")
                conn.commit()
                conn.close()
                messagebox.showinfo("Success","Medicine deleted successfully",parent=medicine_edit_window)    
        except Exception as ex:
            messagebox.showerror("Error", ex ,parent=medicine_edit_window)
    #setup the view

    my_tree = ttk.Treeview(medicine_edit_window,)
    my_tree['columns'] = ('id','medicine_name', 'price', 'quantity', 'code')
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("id", anchor=CENTER, width=80, minwidth=50)
    my_tree.column("medicine_name", anchor=CENTER, minwidth=200)
    my_tree.column("price", anchor=CENTER, minwidth=100)
    my_tree.column("quantity", anchor=CENTER, minwidth=100)
    my_tree.column("code", anchor=CENTER, minwidth=200)

    my_tree.heading("#0", text='', anchor=W)
    my_tree.heading('id', text="ID", anchor=CENTER)
    my_tree.heading('medicine_name', text="Medicine Name", anchor=CENTER)
    my_tree.heading('price', text="Price", anchor=CENTER)
    my_tree.heading('quantity', text="Quantity", anchor=CENTER)
    my_tree.heading('code', text="Code", anchor=CENTER)
    my_tree.tag_configure('odd', background="white")
    my_tree.tag_configure('even', background='lightblue')

    #Fetch data
    conn=connect_to_database()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM medicine")
    rows = cursor.fetchall()
    count=0
    for row in rows:
        if count % 2 == 0:
            my_tree.insert('', 'end', values=(row[0], row[1], row[2], row[3], row[4]), tags=('even',))
        else:
             my_tree.insert('', 'end', values=(row[0], row[1], row[2], row[3], row[4]), tags=('odd',))
        conn.close()
        count += 1

    # update

    update_frame=LabelFrame(medicine_edit_window, bg='#95c1ca',text="Update")
    #labels
    medicine_id_label=Label(update_frame, text="ID", font=("arial", 11),bg='#95c1ca')
    medicine_id_label.grid(row=0, column=0, padx=5, pady=5)
    medicine_name_label=Label(update_frame, text="Medicine name", font=("arial", 11),bg='#95c1ca')
    medicine_name_label.grid(row=0, column=1, padx=5, pady=5)
    medicine_price_label=Label(update_frame, text="Price", font=("arial", 11),bg='#95c1ca')
    medicine_price_label.grid(row=0, column=2, padx=5, pady=5)
    medicine_quantity_label=Label(update_frame, text="Quantity", font=("arial", 11),bg='#95c1ca')
    medicine_quantity_label.grid(row=0, column=3, padx=5, pady=5)
    medicine_code_label=Label(update_frame, text="Code", font=("arial", 11),bg='#95c1ca')
    medicine_code_label.grid(row=0, column=4, padx=5, pady=5)
    #entries
    medicine_id_entry=Entry(update_frame, width=20, font=("arial", 11))
    medicine_id_entry.grid(row=1, column=0, padx=5, pady=5)
    m_name_var=StringVar()
    medicine_name_entry=Entry(update_frame, width=20,textvariable=m_name_var, font=("arial", 11))
    medicine_name_entry.grid(row=1, column=1, padx=5, pady=5)
    m_price_var=IntVar()
    medicine_price_entry=Entry(update_frame,textvariable=m_price_var, width=20, font=("arial", 11))
    medicine_price_entry.grid(row=1, column=2, padx=5, pady=5)
    m_quantity_var=IntVar()
    medicine_quantity_entry=Entry(update_frame,textvariable=m_quantity_var, width=20, font=("arial", 11))
    medicine_quantity_entry.grid(row=1, column=3, padx=5, pady=5)
    m_code_var=StringVar()
    medicine_code_entry=Entry(update_frame,textvariable=m_code_var, width=20, font=("arial", 11))
    medicine_code_entry.grid(row=1, column=4, padx=5, pady=5)
    #button
    medicine_fetch_button=Button(update_frame, text="Fetch", width=15, command=fetch_medicine_data)
    medicine_fetch_button.grid(row=2, column=1, padx=5, pady=10)
    medicine_update_button=Button(update_frame, text="Update",width=15, bg='#1bf254', command=update_medicine)
    medicine_update_button.grid(row=2, column=3, padx=5, pady=10)

    # Buttons' Frame
    buttons_frame = Frame(medicine_edit_window, bg='#95c1ca')
    buttons_frame.pack(side=BOTTOM, fill=X, padx=5, pady=5)
    
    empty_area1=Label(buttons_frame, bg='#95c1ca', width=20)
    medicine_delete_button=Button(buttons_frame,bg='red', fg='white', width=20, text='Delete', command=delete_medicine)
    cancel_button=Button(buttons_frame, width=20, command=medicine_edit_window.destroy, text='Cancel')
    empty_area2=Label(buttons_frame, bg='#95c1ca', width=20)

    #pack buttons
    empty_area1.grid(row=0,column=0,pady=5, padx=35)
    medicine_delete_button.grid(row=0, column=1,pady=20,padx=40)
    cancel_button.grid(row=0,column=2, pady=20,padx=40)
    empty_area2.grid(row=0, column=3, pady=20, padx=40)

    #packing data 

    my_tree.pack(pady=10)
    update_frame.pack(pady=10)
    buttons_frame.pack(fill=X , pady=15)
 
def medicine_view():
    medicine_view_window=Toplevel(root)
    medicine_view_window.title("Medicine | View All Medicines")
    medicine_view_window.iconbitmap('icon.ico')
    medicine_view_window.config(bg='#95c1ca')
    medicine_view_window.resizable(0,0)
    medicine_view_window.grab_set()
    center_window(medicine_view_window, 910, 480)
    style=ttk.Style()
    style.theme_use('default')
    #setup the view

    my_tree = ttk.Treeview(medicine_view_window,)
    my_tree['columns'] = ('id','medicine_name', 'price', 'quantity', 'code')
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("id", anchor=CENTER, width=80, minwidth=50)
    my_tree.column("medicine_name", anchor=CENTER, minwidth=200)
    my_tree.column("price", anchor=CENTER, minwidth=200)
    my_tree.column("quantity", anchor=CENTER, minwidth=200)
    my_tree.column("code", anchor=CENTER, minwidth=200)

    my_tree.heading("#0", text='', anchor=W)
    my_tree.heading('id', text="ID", anchor=CENTER)
    my_tree.heading('medicine_name', text="Medicine Name", anchor=CENTER)
    my_tree.heading('price', text="Price", anchor=CENTER)
    my_tree.heading('quantity', text="Quantity", anchor=CENTER)
    my_tree.heading('code', text="Code", anchor=CENTER)
    my_tree.tag_configure('odd', background="white")
    my_tree.tag_configure('even', background='lightblue')

    #Fetch data
    conn=connect_to_database()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM medicine")
    rows = cursor.fetchall()
    count=0
    for row in rows:
        if count % 2 == 0:
            my_tree.insert('', 'end', values=(row[0], row[1], row[2], row[3], row[4]), tags=('even',))
        else:
             my_tree.insert('', 'end', values=(row[0], row[1], row[2], row[3], row[4]), tags=('odd',))
        conn.close()
        count += 1


    #packing data 

    my_tree.pack(pady=10, expand=True, fill=Y)

#=================================================================SALES MENU===================================================================

def cart():
    cart_window=Toplevel(root)
    cart_window.grab_set()
    cart_window.title("Cart | Insert Medicine")
    cart_window.iconbitmap('icon.ico')
    cart_window.config(bg='#95c1ca')
    sub_menu=Menu(cart_window)
    cart_window.config(menu=sub_menu)
    cart_window.focus_set()
    center_window(cart_window, 1100, 550)
    cart_window.resizable(0,0)
    style = ttk.Style()
    style.theme_use("default")
    

    # Functions 

    def insert_cart():
        cart_insert_window=Toplevel(cart_window)
        cart_insert_window.title("Cart | Insert Medicine")
        cart_insert_window.iconbitmap('icon.ico')
        cart_insert_window.config(bg='#95c1ca')
        cart_insert_window.grab_set()
        cart_insert_window.resizable(0,0)
        center_window(cart_insert_window, 470, 270)
        cart_insert_window.focus_force()
        cart_insert_window.grab_set()
        
        # cart_insert_window.transient(root)
        # cart_insert_window.attributes('-topmost', True)
        # cart_insert_window.attributes('-topmost', False)


        def send_to_database():
            conn=connect_to_database()
            cursor=conn.cursor()
            med_name=medicine_name_entry.get()
            medicine_found = False
            cursor.execute("SELECT name FROM medicine")
            names = cursor.fetchall()
            for name in names:
                if med_name == name[0]:
                    medicine_found= True
       
                    cursor.execute(f"SELECT id FROM medicine WHERE name='{med_name}'")
                    med_id=cursor.fetchone()
                    cursor.execute(f"SELECT price FROM medicine WHERE name='{med_name}'")
                    med_price=cursor.fetchone()[0]
                    try:
                        quantity=int(quantity_entry.get())
                        c_id=int(customer_id_entry.get())
                        cursor.execute("SELECT id FROM customer")
                        customer_id=cursor.fetchall()
                        customer_found= False
                        cursor.execute(f"SELECT customer_name FROM customer WHERE id={c_id}")
                        
                        for customer in customer_id:
                            if c_id == customer[0]:
                                customer_found = True
                                customer_name=cursor.fetchone()[0]
                                if med_name.strip() and quantity!=0 and c_id!=0:
                                    total= float(med_price * quantity)
                                    cursor.execute("SELECT quantity FROM medicine")
                                    quantity_in_stock = cursor.fetchall()
                                    medicine_stock_found= False
                                    for quantity_stock in quantity_in_stock:
                                        if quantity_stock[0] >= quantity:
                                            medicine_stock_found = True
                                            if med_id:
                                                med_id=int(med_id[0])
                                                cursor.execute(f"""INSERT INTO cart (medicine_id, medicine_name, quantity, price, total, customer_id, customer_name)
                                                                VALUES({med_id}, '{med_name}', {quantity}, {med_price}, {total}, {c_id}, '{customer_name}'
                                                    )""")
                                                # cursor.execute(f"""INSERT INTO sales (medicine_id, medicine_name,price,quantity,total, customer_id, customer_name)
                                                #                 VALUES({med_id}, '{med_name}',{med_price},{quantity}, {total}, {c_id}, '{customer_name}'
                                                # ) """)    
                                                conn.commit()
                                                conn.close()
                                                
                                            #   REFRESH THE TREE VIEW
                                                conn=connect_to_database()
                                                cursor=conn.cursor()
                                                cursor.execute("SELECT * FROM cart")
                                                rows = cursor.fetchall()
                                                count = 0
                                                conn=connect_to_database()
                                                cursor=conn.cursor()
                                                cursor.execute("SELECT SUM(total) FROM cart ")
                                                total_sec=cursor.fetchone()[0]
                                                total_label.config(text=f"Total     |     {total_sec}")
                                                for item in my_tree.get_children():
                                                    my_tree.delete(item)
                                                for row in rows:
                                                    
                                                    if count % 2 == 0:
                                                        my_tree.insert('', 'end', values=(row[0], row[2], row[3],row[4], row[5],row[7]), tags=('even',))
                                                    else:
                                                        my_tree.insert('', 'end', values=(row[0], row[2], row[3],row[4], row[5],row[7]), tags=('odd',))
                                                    conn.close()
                                                    count +=1

                                                cart_insert_window.destroy()
                                            else:
                                                messagebox.showerror("Error", "Medicine not found")
                                                cart_insert_window.destroy()
                                    if not medicine_stock_found:
                                        messagebox.showerror("Error", "Insufficient quantity in stock", parent=cart_window)
                                        cart_insert_window.destroy()
                                else:
                                    messagebox.showerror("Error", "Please fill all fields", parent=cart_insert_window)
                                break
                    except Exception as kkk :
                        messagebox.showerror("Error", "Please fill all fields", parent=cart_insert_window)
                    if not customer_found:
                        messagebox.showerror("Error", "Customer ID not found", parent=cart_insert_window)
                        customer_id_entry.delete(0, END)
                        customer_id_entry.insert(0,'')
                        
            if not medicine_found:
                messagebox.showerror("Error", "Medicine not found", parent=cart_insert_window)


        # labels
        empty=Label(cart_insert_window, text="  "*7,bg='#95c1ca')
        empty.grid(row=0, column=0)
        empty2=Label(cart_insert_window, text="  "*7,bg='#95c1ca')
        empty2.grid(row=0, column=2)
        empty3=Label(cart_insert_window, text="  "*7,bg='#95c1ca')
        empty3.grid(row=0, column=4)
        medicine_name_label=Label(cart_insert_window, text="Medicine name", font=("arial", 11),bg='#95c1ca')
        medicine_name_label.grid(row=1, column=1, padx=10, pady=15)
        quantity_label=Label(cart_insert_window, text="Quantity", font=("arial", 11),bg='#95c1ca')
        quantity_label.grid(row=2, column=1, padx=10, pady=15)
        customer_id_label=Label(cart_insert_window, text="Customer ID", font=("arial", 11),bg='#95c1ca')
        customer_id_label.grid(row=3, column=1, padx=10, pady=15)
        #Entries
        medicine_name_entry=Entry(cart_insert_window, width=20, font=("arial", 11))
        medicine_name_entry.grid(row=1, column=3, padx=10, pady=15)
        quantity_entry=Entry(cart_insert_window, width=20, font=("arial", 11))
        quantity_entry.grid(row=2, column=3, padx=10, pady=15)
        customer_id_entry=Entry(cart_insert_window, width=20, font=("arial", 11))
        customer_id_entry.grid(row=3, column=3, padx=10, pady=15)
        #Buttons
        submit=Button(cart_insert_window, text="Add", command=send_to_database, width=10)
        submit.grid(row=4, column=1, padx=10, pady=15)
        cancel=Button(cart_insert_window, text="Cancel", command=cart_insert_window.destroy, width=10)
        cancel.grid(row=4, column=3, padx=10, pady=15)
 
    def fetch_data():
        try:
            conn=connect_to_database()
            cursor=conn.cursor()
            id=id_entry.get()
            cursor.execute(f"SELECT * FROM cart WHERE id={id}")
            data=cursor.fetchone()

            if data:
                m_name_var.set(data[2],)
                q_var.set(data[3],)
                cs_name_var.set(data[7],)
            else:
                messagebox.showerror("Error","item ID not found", parent=cart_window)
                conn.close()
                id_entry.delete(0, END)
                id_entry.insert(0,"")
                medicine_name_entry.delete(0, END)
                quantity_entry.delete(0, END)
                customer_name_entry.delete(0, END)
        except Exception as exx:
            messagebox.showerror("Error", "Missing ID",parent=cart_window)

    def update_data():
        try:
            conn = connect_to_database()
            cursor = conn.cursor()
            id = id_entry.get()
            m_name = m_name_var.get()
            quantity = q_var.get()
            cs_name = cs_name_var.get()
            cursor.execute(f"SELECT price FROM medicine WHERE name='{m_name}'")
            med_price=cursor.fetchone()[0]
            p_total= float(med_price * quantity)
            id_found =False
            cursor.execute('SELECT id FROM cart')
            data = cursor.fetchall()
            for ids in data:
                if ids[0] == int(id):
                    id_found=True
                    cursor.execute(f"UPDATE cart SET medicine_name='{m_name}', quantity={quantity}, customer_name='{cs_name}', total={p_total} WHERE id={id}")
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Success","Cart updated successfully",parent=cart_window)
                    id_entry.delete(0, END)
                    id_entry.insert(0, "")
                    medicine_name_entry.delete(0, END)
                    quantity_entry.delete(0, END)
                    customer_name_entry.delete(0, END)
                    

                    #   REFRESH THE TREE VIEW
                    conn=connect_to_database()
                    cursor=conn.cursor()
                    cursor.execute("SELECT * FROM cart")
                    rows = cursor.fetchall()
                    count = 0
                    conn=connect_to_database()
                    cursor=conn.cursor()
                    cursor.execute("SELECT SUM(total) FROM cart ")
                    total_sec=cursor.fetchone()[0]
                    total_label.config(text=f"Total     |     {total_sec}")
                    for item in my_tree.get_children():
                        my_tree.delete(item)
                    for row in rows:
                        
                        if count % 2 == 0:
                            my_tree.insert('', 'end', values=(row[0], row[2], row[3],row[4], row[5],row[7]), tags=('even',))
                        else:
                            my_tree.insert('', 'end', values=(row[0], row[2], row[3],row[4], row[5],row[7]), tags=('odd',))
                        conn.close()
                        count +=1
            if not id_found:
                messagebox.showerror("Error", "ID not found", parent=cart_window)
        except Exception as exc:
            messagebox.showerror("Error", exc,parent=cart_window)
            print(exc)

    def delete_medicine():
        try:
            root.bell()
            response = messagebox.askokcancel("Warning", "This will delete an item", icon="warning",parent=cart_window)
            if response:
                x = my_tree.selection()[0]
                m_id = my_tree.item(x, 'values')[0]
                my_tree.delete(x)
                conn = connect_to_database()
                cursor = conn.cursor()
                cursor.execute(f"DELETE FROM cart WHERE id={m_id}")
                conn.commit()
                conn.close()
                conn=connect_to_database()
                cursor=conn.cursor()
                cursor.execute("SELECT SUM(total) FROM cart ")
                total_sec=cursor.fetchone()[0]
                total_label.config(text=f"Total     |     {total_sec}")
                messagebox.showinfo("Success","Medicine deleted successfully",parent=cart_window)    
        except Exception as ex:
            messagebox.showerror("Error", "No Record Selected",parent=cart_window)   

    def send_to_sales():
        try:
            root.bell()
            conn = connect_to_database()
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(total) FROM cart ")
            total_sec=cursor.fetchone()[0]
            if total_sec == 0:
                messagebox.showerror("Error", "No items in cart",parent=cart_window)
            else:
                response = messagebox.askokcancel("Warning", "This will send all items to sales", icon="warning", parent=cart_window)
                if response:
                    cursor.execute("SELECT * FROM cart")
                    rows = cursor.fetchall()
                    for row in rows:
                        cursor.execute(f"""INSERT INTO sales (medicine_id, medicine_name,price,quantity,total, customer_id, customer_name)
                                                            VALUES({row[1]}, '{row[2]}',{row[4]},{row[3]}, {row[5]}, {row[6]}, '{row[7]}'
                                            ) """)                    
                        cursor.execute("DELETE FROM cart")
                        conn.commit()
                        conn.close()
                        #   REFRESH THE TREE VIEW
                        conn=connect_to_database()
                        cursor=conn.cursor()
                        cursor.execute("SELECT * FROM cart")
                        rows = cursor.fetchall()
                        count = 0
                        conn=connect_to_database()
                        cursor=conn.cursor()
                        cursor.execute("SELECT SUM(total) FROM cart ")
                        total_sec=cursor.fetchone()[0]
                        total_label.config(text=f"Total     |     {total_sec}")
                        for item in my_tree.get_children():
                            my_tree.delete(item)
                        for row in rows:
                            
                            if count % 2 == 0:
                                my_tree.insert('', 'end', values=(row[0], row[2], row[3],row[4], row[5],row[7]), tags=('even',))
                            else:
                                my_tree.insert('', 'end', values=(row[0], row[2], row[3],row[4], row[5],row[7]), tags=('odd',))
                            conn.close()
                            count +=1
                
        except Exception:
            messagebox.showerror("Error", "No Record Selected",parent=cart_window)



# SETUP THE VIEW

    my_tree = ttk.Treeview(cart_window)
    my_tree['columns'] = ('id','medicine_name','quantity', 'price','total', 'customer_name')
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("id", anchor=CENTER, width=80, minwidth=50)
    my_tree.column("medicine_name", anchor=CENTER, minwidth=200)
    my_tree.column("quantity", anchor=CENTER, minwidth=150)
    my_tree.column("price", anchor=CENTER, minwidth=200 )
    my_tree.column("total", anchor=CENTER, minwidth=200 )
    my_tree.column("customer_name", anchor=CENTER, minwidth=150)

    my_tree.heading("#0", text='', anchor=W)
    my_tree.heading('id', text="ID", anchor=CENTER)
    my_tree.heading('medicine_name', text="Medicine name", anchor=CENTER)
    my_tree.heading('quantity', text="Quantity", anchor=CENTER)
    my_tree.heading('price', text="Price", anchor=CENTER)
    my_tree.heading('total', text="Total", anchor=CENTER)
    my_tree.heading('customer_name', text="Customer Name", anchor=CENTER)
    my_tree.tag_configure('odd', background="white")
    my_tree.tag_configure('even', background='lightblue')

    #Fetch data
    conn=connect_to_database()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM cart")
    rows = cursor.fetchall()
    count=0
    for row in rows:
        if count % 2 == 0:
            my_tree.insert('', 'end', values=(row[0], row[2], row[3],row[4],row[5], row[7]), tags=('even',))
        else:
             my_tree.insert('', 'end', values=(row[0], row[2], row[3],row[4],row[5], row[7]), tags=('odd',))
        conn.close()
        count += 1

    conn=connect_to_database()
    cursor=conn.cursor()
    cursor.execute("SELECT SUM(total) FROM cart ")
    total = cursor.fetchone()[0]
    total_label=Label(cart_window, padx=90, width=100, anchor=E, text=f"Total     |     {total}" , font=("arial", 12))



    #UPDATE FRAME
    #-------------
    update_frame=LabelFrame(cart_window, bg='#95c1ca',text="Edit cart")
    #labels
    id_label=Label(update_frame, text="ID", font=("arial", 11),bg='#95c1ca')
    id_label.grid(row=0, column=0, padx=5, pady=5)
    medicine_name_label=Label(update_frame, text="Medicine name", font=("arial", 11),bg='#95c1ca')
    medicine_name_label.grid(row=0, column=1, padx=5, pady=5)
    quantity_label=Label(update_frame, text="Quantity", font=("arial", 11),bg='#95c1ca')
    quantity_label.grid(row=0, column=2, padx=5, pady=5)
    customer_name_label=Label(update_frame, text="Customer name", font=("arial", 11),bg='#95c1ca')
    customer_name_label.grid(row=0, column=3, padx=5, pady=5)
    #entries
    id_entry=Entry(update_frame, width=22, font=("arial", 11))
    id_entry.grid(row=1, column=0, padx=45, pady=5)
    m_name_var=StringVar()
    medicine_name_entry=Entry(update_frame, width=22,textvariable=m_name_var, font=("arial", 11))
    medicine_name_entry.grid(row=1, column=1, padx=45, pady=5)
    q_var=IntVar()
    quantity_entry=Entry(update_frame,textvariable=q_var, width=22, font=("arial", 11))
    quantity_entry.grid(row=1, column=2, padx=45, pady=5)
    cs_name_var=StringVar()
    customer_name_entry=Entry(update_frame,textvariable=cs_name_var, width=22, font=("arial", 11))
    customer_name_entry.grid(row=1, column=3, padx=45, pady=5)
    #button
    customer_fetch_button=Button(update_frame, text="Fetch", width=20, command=fetch_data)
    customer_fetch_button.grid(row=2, column=1, padx=5, pady=15 )
    customer_update_button=Button(update_frame, text="Update",width=20, bg='#1bf254', command=update_data)
    customer_update_button.grid(row=2, column=2, padx=5, pady=15 )


    # Buttons' Frame
    buttons_frame = Frame(cart_window, bg='#95c1ca')
    buttons_frame.pack(side=BOTTOM, fill=X, padx=60, pady=5,anchor=CENTER)
    
    insert_button=Button(buttons_frame, text="Add", width=20, command=insert_cart)
    send_data_button=Button(buttons_frame, text="Send", width=20, command=send_to_sales)
    medicine_delete_button=Button(buttons_frame,bg='red', fg='white', width=20, text='Delete', command=delete_medicine)
    cancel_button=Button(buttons_frame, width=20, command=cart_window.destroy, text='Cancel')

    #pack buttons
    insert_button.grid(row=0,column=0,pady=5, padx=48)
    send_data_button.grid(row=0, column=1, pady=20, padx=48)
    medicine_delete_button.grid(row=0, column=2,pady=20,padx=48)
    cancel_button.grid(row=0,column=3, pady=20,padx=48)
    

    # PACKING DATA

    my_tree.pack(pady=10)
    total_label.pack(expand=0)
    update_frame.pack(fill="both", expand=False, padx=10, pady=5)







    customer_menu = Menu(sub_menu, tearoff=False)
    sub_menu.add_cascade(label="Customers", menu=customer_menu)
    customer_menu.add_command(label="  "*5 + "Add" + "  "*5, command=customer_insert)
    customer_menu.add_separator()
    customer_menu.add_command(label="  "*5 + "Edit" + "  "*5, command=customer_edit)
    customer_menu.add_separator()
    customer_menu.add_command(label="  "*5 + "View" + "  "*5, command=customer_view)


    seller_menu = Menu(sub_menu, tearoff=False)
    sub_menu.add_cascade(label="Suppliers", menu=seller_menu)
    seller_menu.add_command(label="  "*5 + "Add" + "  "*5, command=seller_insert)
    seller_menu.add_separator()
    seller_menu.add_command(label="  "*5 + "Edit" + "  "*5, command=seller_edit)
    seller_menu.add_separator()
    seller_menu.add_command(label="  "*5 + "View" + "  "*5, command=seller_view)

    medicine_menu = Menu(sub_menu, tearoff=False)
    sub_menu.add_cascade(label="Medicines", menu=medicine_menu)
    medicine_menu.add_command(label="  "*5 + "Add" + "  "*5, command=insert_medicine)
    medicine_menu.add_separator()
    medicine_menu.add_command(label="  "*5 + "Edit" + "  "*5, command=medicine_edit)
    medicine_menu.add_separator()
    medicine_menu.add_command(label="  "*5 + "View" + "  "*5, command=medicine_view)

    purchase_menu = Menu(sub_menu, tearoff=False)
    sub_menu.add_cascade(label="Purchase", menu=purchase_menu)
    # purchase_menu.add_command(label="  "*5 + "Add" + "  "*5, command=purchase_window)
    # purchase_menu.add_separator()
    # purchase_menu.add_command(label="  "*5 + "Edit" + "  "*5)
    # purchase_menu.add_separator()
    purchase_menu.add_command(label="  "*5 + "View" + "  "*5, command=view_purchase)


    cart_menu = Menu(sub_menu, tearoff=False)
    sub_menu.add_cascade(label="Sales", menu=cart_menu)
    # cart_menu.add_command(label="  "*5 + "Insert" + "  "*5)
    # cart_menu.add_separator()
    cart_menu.add_command(label="  "*5 + "View" + "  "*5, command=view_sales)

def view_sales():
    view_sales_window=Toplevel(root)
    view_sales_window.grab_set()
    view_sales_window.title("Sales | View All Sales")
    view_sales_window.iconbitmap('icon.ico')
    view_sales_window.config(bg='#95c1ca')
    sub_menu=Menu(view_sales_window)
    view_sales_window.config(menu=sub_menu)
    view_sales_window.focus_set()
    center_window(view_sales_window, 1100,300)
    style = ttk.Style()
    style.theme_use("default")

    my_tree = ttk.Treeview(view_sales_window)
    my_tree['columns'] = ('id','medicine_name','price','quantity' ,'total', 'customer_name')
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("id", anchor=CENTER, width=80, minwidth=50)
    my_tree.column("medicine_name", anchor=CENTER, minwidth=200)
    my_tree.column("price", anchor=CENTER, minwidth=200 )
    my_tree.column("quantity", anchor=CENTER, minwidth=150)
    my_tree.column("total", anchor=CENTER, minwidth=200 )
    my_tree.column("customer_name", anchor=CENTER, minwidth=150)

    my_tree.heading("#0", text='', anchor=W)
    my_tree.heading('id', text="ID", anchor=CENTER)
    my_tree.heading('medicine_name', text="Medicine name", anchor=CENTER)
    my_tree.heading('price', text="Price", anchor=CENTER)
    my_tree.heading('quantity', text="Quantity", anchor=CENTER)   
    my_tree.heading('total', text="Total", anchor=CENTER)
    my_tree.heading('customer_name', text="Customer Name", anchor=CENTER)
    my_tree.tag_configure('odd', background="white")
    my_tree.tag_configure('even', background='lightblue')



    #Fetch data
    conn=connect_to_database()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM sales")
    rows = cursor.fetchall()
    count=0
    for row in rows:
        if count % 2 == 0:
            my_tree.insert('', 'end', values=(row[0], row[2], row[3],row[4],row[5], row[7]), tags=('even',))
        else:
            my_tree.insert('', 'end', values=(row[0], row[2], row[3],row[4],row[5], row[7]), tags=('odd',))
        conn.close()
        count += 1

    # PACKING DATA

    my_tree.pack(pady=10, expand=True , fill=Y)

#=================================================================PURCHASE MENU==================================================================


def purchase_window():
    purchase_window=Toplevel(root)
    purchase_window.grab_set()
    purchase_window.title("Cart | Insert Medicine Purchased")
    purchase_window.iconbitmap('icon.ico')
    purchase_window.config(bg='#95c1ca')
    sub_menu=Menu(purchase_window)
    purchase_window.config(menu=sub_menu)
    purchase_window.focus_set()
    center_window(purchase_window, 1100, 550)
    purchase_window.resizable(0,0)
    style = ttk.Style()
    style.theme_use("default")

    # Functions 

    def insert_purchase():
        purchase_insert_window=Toplevel(purchase_window)
        purchase_insert_window.title("Cart | Insert Medicine")
        purchase_insert_window.iconbitmap('icon.ico')
        purchase_insert_window.config(bg='#95c1ca')
        purchase_insert_window.grab_set()
        purchase_insert_window.resizable(0,0)
        center_window(purchase_insert_window, 470, 270)
        purchase_insert_window.focus_force()
        purchase_insert_window.grab_set()


        def send_to_database():
            conn=connect_to_database()
            cursor=conn.cursor()
            med_name=medicine_name_entry.get()
            medicine_found = False
            cursor.execute("SELECT name FROM medicine")
            names = cursor.fetchall()
            for name in names:
                if med_name == name[0]:
                    medicine_found = True
       
                    cursor.execute(f"SELECT id FROM medicine WHERE name='{med_name}'")
                    med_id=cursor.fetchone()
                    cursor.execute(f"SELECT price FROM medicine WHERE name='{med_name}'")
                    med_price=cursor.fetchone()[0]
                    try:
                        quantity=int(quantity_entry.get())
                        s_id=int(supplier_id_entry.get())
                        cursor.execute("SELECT id FROM seller")
                        supplier_id=cursor.fetchall()
                        supplier_found= False
                        cursor.execute(f"SELECT seller_name FROM seller WHERE id={s_id}")
                        
                        for supplier in supplier_id:
                            if s_id == supplier[0]:
                                supplier_found = True
                                supplier_name=cursor.fetchone()[0]
                                if med_name.strip() and quantity!=0 and quantity !=''and s_id!=0:
                                    total= float(med_price * quantity)
                                    
                                    if med_id:
                                        med_id=med_id[0]
                                        cursor.execute(f"""INSERT INTO purchase (medicine_id, medicine_name, price, quantity, total, seller_id, seller_name)
                                                        VALUES({med_id}, '{med_name}', {med_price}, {quantity}, {total}, {s_id}, '{supplier_name}'
                                            )""")
                                        # cursor.execute(f"""INSERT INTO pur_view (medicine_id, medicine_name,price,quantity,total, seller_id, seller_name)
                                        #                 VALUES({med_id}, '{med_name}',{med_price},{quantity}, {total}, {s_id}, '{supplier_name}'
                                        # ) """)    
                                        conn.commit()
                                        conn.close()
                                        
                                    #   REFRESH THE TREE VIEW
                                        conn=connect_to_database()
                                        cursor=conn.cursor()
                                        cursor.execute("SELECT * FROM purchase")
                                        rows = cursor.fetchall()
                                        count = 0
                                        conn=connect_to_database()
                                        cursor=conn.cursor()
                                        cursor.execute("SELECT SUM(total) FROM purchase ")
                                        total_sec=cursor.fetchone()[0]
                                        total_label.config(text=f"Total     |     {total_sec}")
                                        for item in my_tree.get_children():
                                            my_tree.delete(item)
                                        for row in rows:
                                            
                                            if count % 2 == 0:
                                                my_tree.insert('', 'end', values=(row[0], row[2], row[4],row[3], row[5],row[7]), tags=('even',))
                                            else:
                                                my_tree.insert('', 'end', values=(row[0], row[2], row[4],row[3], row[5],row[7]), tags=('odd',))
                                            conn.close()
                                            count +=1

                                        purchase_insert_window.destroy()
                                    else:
                                        messagebox.showerror("Error", "Medicine not found")
                                        purchase_insert_window.destroy()
                                else:
                                    messagebox.showerror("Error", "Please fill all fields", parent=purchase_insert_window)
                                break
                    except Exception: 
                        messagebox.showerror("Error", "Please fill all fields", parent=purchase_insert_window)
                    if not supplier_found:
                        messagebox.showerror("Error", "Supplier ID not found", parent=purchase_insert_window)
                        supplier_id_entry.delete(0, END)
                        supplier_id_entry.insert(0,'')
            if not medicine_found:
                messagebox.showerror("Error", "Medicine not found", parent=purchase_insert_window)


        # labels
        empty=Label(purchase_insert_window, text="  "*7,bg='#95c1ca')
        empty.grid(row=0, column=0)
        empty2=Label(purchase_insert_window, text="  "*7,bg='#95c1ca')
        empty2.grid(row=0, column=2)
        empty3=Label(purchase_insert_window, text="  "*7,bg='#95c1ca')
        empty3.grid(row=0, column=4)
        medicine_name_label=Label(purchase_insert_window, text="Medicine name", font=("arial", 11),bg='#95c1ca')
        medicine_name_label.grid(row=1, column=1, padx=10, pady=15)
        quantity_label=Label(purchase_insert_window, text="Quantity", font=("arial", 11),bg='#95c1ca')
        quantity_label.grid(row=2, column=1, padx=10, pady=15)
        supplier_id_label=Label(purchase_insert_window, text="Supplier ID", font=("arial", 11),bg='#95c1ca')
        supplier_id_label.grid(row=3, column=1, padx=10, pady=15)
        #Entries
        medicine_name_entry=Entry(purchase_insert_window, width=20, font=("arial", 11))
        medicine_name_entry.grid(row=1, column=3, padx=10, pady=15)
        quantity_entry=Entry(purchase_insert_window, width=20, font=("arial", 11))
        quantity_entry.grid(row=2, column=3, padx=10, pady=15)
        supplier_id_entry=Entry(purchase_insert_window, width=20, font=("arial", 11))
        supplier_id_entry.grid(row=3, column=3, padx=10, pady=15)
        #Buttons
        submit=Button(purchase_insert_window, text="Add", command=send_to_database, width=10)
        submit.grid(row=4, column=1, padx=10, pady=15)
        cancel=Button(purchase_insert_window, text="Cancel", command=purchase_insert_window.destroy, width=10)
        cancel.grid(row=4, column=3, padx=10, pady=15)


    def fetch_data():
        try:
            conn=connect_to_database()
            cursor=conn.cursor()
            id=id_entry.get()
            cursor.execute(f"SELECT * FROM purchase WHERE id={id}")
            data=cursor.fetchone()

            if data:
                m_name_var.set(data[2],)
                q_var.set(data[4],)
                s_name_var.set(data[7],)
            else:
                messagebox.showerror("Error","item ID not found", parent=purchase_window)
                conn.close()
                id_entry.delete(0, END)
                id_entry.insert(0,"")
                medicine_name_entry.delete(0, END)
                quantity_entry.delete(0, END)
                supplier_name_entry.delete(0, END)
        except Exception as exx:
            messagebox.showerror("Error", "Missing ID",parent=purchase_window)


    def update_data():
        try:
            conn = connect_to_database()
            cursor = conn.cursor()
            id = id_entry.get()
            m_name = m_name_var.get()
            quantity = q_var.get()
            s_name = s_name_var.get()
            cursor.execute(f"SELECT price FROM medicine WHERE name='{m_name}'")
            med_price=cursor.fetchone()[0]
            p_total= float(med_price * quantity)
            id_found =False
            cursor.execute(f"SELECT id FROM purchase")
            data=cursor.fetchall()
            for ids in data:
                if ids[0]==int(id):
                    id_found=True
                    
                    cursor.execute(f"UPDATE purchase SET medicine_name='{m_name}', quantity={quantity}, seller_name='{s_name}', total={p_total} WHERE id={id}")
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Success","Cart updated successfully",parent=purchase_window)
                    id_entry.delete(0, END)
                    id_entry.insert(0, "")
                    medicine_name_entry.delete(0, END)
                    quantity_entry.delete(0, END)
                    supplier_name_entry.delete(0, END)
                    

                    #   REFRESH THE TREE VIEW
                    conn=connect_to_database()
                    cursor=conn.cursor()
                    cursor.execute("SELECT * FROM purchase")
                    rows = cursor.fetchall()
                    count = 0
                    conn=connect_to_database()
                    cursor=conn.cursor()
                    cursor.execute("SELECT SUM(total) FROM purchase ")
                    total_sec=cursor.fetchone()[0]
                    total_label.config(text=f"Total     |     {total_sec}")
                    for item in my_tree.get_children():
                        my_tree.delete(item)
                    for row in rows:
                        
                        if count % 2 == 0:
                            my_tree.insert('', 'end', values=(row[0], row[2], row[3],row[4], row[5],row[7]), tags=('even',))
                        else:
                            my_tree.insert('', 'end', values=(row[0], row[2], row[3],row[4], row[5],row[7]), tags=('odd',))
                        conn.close()
                        count +=1
            if not id_found:
                messagebox.showerror("Error","ID not found",parent=purchase_window)
        except Exception as exc:
            messagebox.showerror("Error", "Please fill all fields",parent=purchase_window)
            print(exc)


    def delete_medicine():
        try:
            root.bell()
            response = messagebox.askokcancel("Warning", "This will delete an item", icon="warning",parent=purchase_window)
            if response:
                x = my_tree.selection()[0]
                m_id = my_tree.item(x, 'values')[0]
                my_tree.delete(x)
                conn = connect_to_database()
                cursor = conn.cursor()
                cursor.execute(f"DELETE FROM purchase WHERE id={m_id}")
                conn.commit()
                conn.close()
                conn=connect_to_database()
                cursor=conn.cursor()
                cursor.execute("SELECT SUM(total) FROM purchase ")
                total_sec=cursor.fetchone()[0]
                total_label.config(text=f"Total     |     {total_sec}")
                messagebox.showinfo("Success","Medicine deleted successfully",parent=purchase_window)    
        except Exception as ex:
            messagebox.showerror("Error", "No Record Selected",parent=purchase_window)   


    def send_to_pur_view():
        try:
            root.bell()
            conn = connect_to_database()
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(total) FROM purchase ")
            total_sec=cursor.fetchone()[0]
            if total_sec == 0:
                messagebox.showerror("Error", "No items in cart",parent=purchase_window)
            else:
                response = messagebox.askokcancel("Warning", "This will send all items to sales", icon="warning", parent=purchase_window)
                if response:
                    cursor.execute("SELECT * FROM purchase")
                    rows = cursor.fetchall()
                    for row in rows:
                        cursor.execute(f"""INSERT INTO pur_view (medicine_id, medicine_name,price,quantity,total, seller_id, seller_name)
                                                            VALUES({row[1]}, '{row[2]}',{row[4]},{row[3]}, {row[5]}, {row[6]}, '{row[7]}'
                                            ) """)                    
                        cursor.execute("DELETE FROM purchase")
                        conn.commit()
                        conn.close()
                        #   REFRESH THE TREE VIEW
                        conn=connect_to_database()
                        cursor=conn.cursor()
                        cursor.execute("SELECT * FROM purchase")
                        rows = cursor.fetchall()
                        count = 0
                        conn=connect_to_database()
                        cursor=conn.cursor()
                        cursor.execute("SELECT SUM(total) FROM purchase ")
                        total_sec=cursor.fetchone()[0]
                        total_label.config(text=f"Total     |     {total_sec}")
                        for item in my_tree.get_children():
                            my_tree.delete(item)
                        for row in rows:
                            
                            if count % 2 == 0:
                                my_tree.insert('', 'end', values=(row[0], row[2], row[3],row[4], row[5],row[7]), tags=('even',))
                            else:
                                my_tree.insert('', 'end', values=(row[0], row[2], row[3],row[4], row[5],row[7]), tags=('odd',))
                            conn.close()
                            count +=1
                
        except Exception as ee:
            messagebox.showerror("Error","No Record Selected",parent=purchase_window)
            print(ee)

    
    # SETUP THE VIEW

    my_tree = ttk.Treeview(purchase_window)
    my_tree['columns'] = ('id','medicine_name','quantity', 'price','total', 'supplier_name')
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("id", anchor=CENTER, width=80, minwidth=50)
    my_tree.column("medicine_name", anchor=CENTER, minwidth=200)
    my_tree.column("quantity", anchor=CENTER, minwidth=150)
    my_tree.column("price", anchor=CENTER, minwidth=200 )
    my_tree.column("total", anchor=CENTER, minwidth=200 )
    my_tree.column("supplier_name", anchor=CENTER, minwidth=150)

    my_tree.heading("#0", text='', anchor=W)
    my_tree.heading('id', text="ID", anchor=CENTER)
    my_tree.heading('medicine_name', text="Medicine name", anchor=CENTER)
    my_tree.heading('quantity', text="Quantity", anchor=CENTER)
    my_tree.heading('price', text="Price", anchor=CENTER)
    my_tree.heading('total', text="Total", anchor=CENTER)
    my_tree.heading('supplier_name', text="Supplier Name", anchor=CENTER)
    my_tree.tag_configure('odd', background="white")
    my_tree.tag_configure('even', background='lightblue')

    #Fetch data
    conn=connect_to_database()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM purchase")
    rows = cursor.fetchall()
    count=0
    for row in rows:
        if count % 2 == 0:
            my_tree.insert('', 'end', values=(row[0], row[2], row[4],row[3],row[5], row[7]), tags=('even',))
        else:
             my_tree.insert('', 'end', values=(row[0], row[2], row[4],row[3],row[5], row[7]), tags=('odd',))
        conn.close()
        count += 1

    conn=connect_to_database()
    cursor=conn.cursor()
    cursor.execute("SELECT SUM(total) FROM purchase ")
    total = cursor.fetchone()[0]
    total_label=Label(purchase_window, padx=90, width=100, anchor=E, text=f"Total     |     {total}" , font=("arial", 12))


    #UPDATE FRAME
    #-------------
    update_frame=LabelFrame(purchase_window, bg='#95c1ca',text="Edit cart")
    #labels
    id_label=Label(update_frame, text="ID", font=("arial", 11),bg='#95c1ca')
    id_label.grid(row=0, column=0, padx=5, pady=5)
    medicine_name_label=Label(update_frame, text="Medicine name", font=("arial", 11),bg='#95c1ca')
    medicine_name_label.grid(row=0, column=1, padx=5, pady=5)
    quantity_label=Label(update_frame, text="Quantity", font=("arial", 11),bg='#95c1ca')
    quantity_label.grid(row=0, column=2, padx=5, pady=5)
    supplier_name_label=Label(update_frame, text="Supplier name", font=("arial", 11),bg='#95c1ca')
    supplier_name_label.grid(row=0, column=3, padx=5, pady=5)
    #entries
    id_entry=Entry(update_frame, width=22, font=("arial", 11))
    id_entry.grid(row=1, column=0, padx=45, pady=5)
    m_name_var=StringVar()
    medicine_name_entry=Entry(update_frame, width=22,textvariable=m_name_var, font=("arial", 11))
    medicine_name_entry.grid(row=1, column=1, padx=45, pady=5)
    q_var=IntVar()
    quantity_entry=Entry(update_frame,textvariable=q_var, width=22, font=("arial", 11))
    quantity_entry.grid(row=1, column=2, padx=45, pady=5)
    s_name_var=StringVar()
    supplier_name_entry=Entry(update_frame,textvariable=s_name_var, width=22, font=("arial", 11))
    supplier_name_entry.grid(row=1, column=3, padx=45, pady=5)
    #button
    supplier_fetch_button=Button(update_frame, text="Fetch", width=20, command=fetch_data)
    supplier_fetch_button.grid(row=2, column=1, padx=5, pady=15 )
    supplier_update_button=Button(update_frame, text="Update",width=20, bg='#1bf254',command=update_data)
    supplier_update_button.grid(row=2, column=2, padx=5, pady=15 )


    # Buttons' Frame
    buttons_frame = Frame(purchase_window, bg='#95c1ca')
    buttons_frame.pack(side=BOTTOM, fill=X, padx=60, pady=5,anchor=CENTER)
    
    insert_button=Button(buttons_frame, text="Add", width=20,command=insert_purchase)
    send_data_button=Button(buttons_frame, text="Send", width=20, command=send_to_pur_view)
    medicine_delete_button=Button(buttons_frame,bg='red', fg='white', width=20, text='Delete', command=delete_medicine)
    cancel_button=Button(buttons_frame, width=20, command=purchase_window.destroy, text='Cancel')

    #pack buttons
    insert_button.grid(row=0,column=0,pady=5, padx=48)
    send_data_button.grid(row=0, column=1, pady=20, padx=48)
    medicine_delete_button.grid(row=0, column=2,pady=20,padx=48)
    cancel_button.grid(row=0,column=3, pady=20,padx=48)
    

    # PACKING DATA

    my_tree.pack(pady=10)
    total_label.pack(expand=0)
    update_frame.pack(fill="both", expand=False, padx=10, pady=5)







    customer_menu = Menu(sub_menu, tearoff=False)
    sub_menu.add_cascade(label="Customers", menu=customer_menu)
    customer_menu.add_command(label="  "*5 + "Add" + "  "*5, command=customer_insert)
    customer_menu.add_separator()
    customer_menu.add_command(label="  "*5 + "Edit" + "  "*5, command=customer_edit)
    customer_menu.add_separator()
    customer_menu.add_command(label="  "*5 + "View" + "  "*5, command=customer_view)


    seller_menu = Menu(sub_menu, tearoff=False)
    sub_menu.add_cascade(label="Suppliers", menu=seller_menu)
    seller_menu.add_command(label="  "*5 + "Add" + "  "*5, command=seller_insert)
    seller_menu.add_separator()
    seller_menu.add_command(label="  "*5 + "Edit" + "  "*5, command=seller_edit)
    seller_menu.add_separator()
    seller_menu.add_command(label="  "*5 + "View" + "  "*5, command=seller_view)

    medicine_menu = Menu(sub_menu, tearoff=False)
    sub_menu.add_cascade(label="Medicines", menu=medicine_menu)
    medicine_menu.add_command(label="  "*5 + "Add" + "  "*5, command=insert_medicine)
    medicine_menu.add_separator()
    medicine_menu.add_command(label="  "*5 + "Edit" + "  "*5, command=medicine_edit)
    medicine_menu.add_separator()
    medicine_menu.add_command(label="  "*5 + "View" + "  "*5, command=medicine_view)

    purchase_menu = Menu(sub_menu, tearoff=False)
    sub_menu.add_cascade(label="Purchase", menu=purchase_menu)
    # purchase_menu.add_command(label="  "*5 + "Add" + "  "*5, command=purchase_window)
    # purchase_menu.add_separator()
    # purchase_menu.add_command(label="  "*5 + "Edit" + "  "*5)
    # purchase_menu.add_separator()
    purchase_menu.add_command(label="  "*5 + "View" + "  "*5, command=view_purchase)


    cart_menu = Menu(sub_menu, tearoff=False)
    sub_menu.add_cascade(label="Sales", menu=cart_menu)
    cart_menu.add_command(label="  "*5 + "Insert" + "  "*5, command=cart)
    cart_menu.add_separator()
    cart_menu.add_command(label="  "*5 + "View" + "  "*5, command=view_sales)

def view_purchase():
    view_purchase_window=Toplevel(root)
    view_purchase_window.grab_set()
    view_purchase_window.title("Purchase | View All Purchases")
    view_purchase_window.iconbitmap('icon.ico')
    view_purchase_window.config(bg='#95c1ca')
    sub_menu=Menu(view_purchase_window)
    view_purchase_window.config(menu=sub_menu)
    view_purchase_window.focus_set()
    center_window(view_purchase_window, 1100,300)
    style = ttk.Style()
    style.theme_use("default")

    my_tree = ttk.Treeview(view_purchase_window)
    my_tree['columns'] = ('id','medicine_name','price','quantity' ,'total', 'supplier_name')
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("id", anchor=CENTER, width=80, minwidth=50)
    my_tree.column("medicine_name", anchor=CENTER, minwidth=200)
    my_tree.column("price", anchor=CENTER, minwidth=200 )
    my_tree.column("quantity", anchor=CENTER, minwidth=150)
    my_tree.column("total", anchor=CENTER, minwidth=200 )
    my_tree.column("supplier_name", anchor=CENTER, minwidth=150)

    my_tree.heading("#0", text='', anchor=W)
    my_tree.heading('id', text="ID", anchor=CENTER)
    my_tree.heading('medicine_name', text="Medicine name", anchor=CENTER)
    my_tree.heading('price', text="Price", anchor=CENTER)
    my_tree.heading('quantity', text="Quantity", anchor=CENTER)   
    my_tree.heading('total', text="Total", anchor=CENTER)
    my_tree.heading('supplier_name', text="Supplier Name", anchor=CENTER)
    my_tree.tag_configure('odd', background="white")
    my_tree.tag_configure('even', background='lightblue')



    #Fetch data
    conn=connect_to_database()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM pur_view")
    rows = cursor.fetchall()
    count=0
    for row in rows:
        if count % 2 == 0:
            my_tree.insert('', 'end', values=(row[0], row[2], row[4],row[3],row[5], row[7]), tags=('even',))
        else:
            my_tree.insert('', 'end', values=(row[0], row[2], row[4],row[3],row[5], row[7]), tags=('odd',))
        conn.close()
        count += 1

    # PACKING DATA

    my_tree.pack(pady=10, expand=True, fill=Y)


#==============================================================================================================================================


customer_menu = Menu(main_menu, tearoff=False)
main_menu.add_cascade(label="Customers", menu=customer_menu)
customer_menu.add_command(label="  "*5 + "Add" + "  "*5, command=customer_insert)
customer_menu.add_separator()
customer_menu.add_command(label="  "*5 + "Edit" + "  "*5, command=customer_edit)
customer_menu.add_separator()
customer_menu.add_command(label="  "*5 + "View" + "  "*5, command=customer_view)


seller_menu = Menu(main_menu, tearoff=False)
main_menu.add_cascade(label="Suppliers", menu=seller_menu)
seller_menu.add_command(label="  "*5 + "Add" + "  "*5, command=seller_insert)
seller_menu.add_separator()
seller_menu.add_command(label="  "*5 + "Edit" + "  "*5, command=seller_edit)
seller_menu.add_separator()
seller_menu.add_command(label="  "*5 + "View" + "  "*5, command=seller_view)

medicine_menu = Menu(main_menu, tearoff=False)
main_menu.add_cascade(label="Medicines", menu=medicine_menu)
medicine_menu.add_command(label="  "*5 + "Add" + "  "*5, command=insert_medicine)
medicine_menu.add_separator()
medicine_menu.add_command(label="  "*5 + "Edit" + "  "*5, command=medicine_edit)
medicine_menu.add_separator()
medicine_menu.add_command(label="  "*5 + "View" + "  "*5, command=medicine_view)

purchase_menu = Menu(main_menu, tearoff=False)
main_menu.add_cascade(label="Purchase", menu=purchase_menu)
purchase_menu.add_command(label="  "*5 + "Add" + "  "*5, command=purchase_window)
purchase_menu.add_separator()
# purchase_menu.add_command(label="  "*5 + "Edit" + "  "*5)
# purchase_menu.add_separator()
purchase_menu.add_command(label="  "*5 + "View" + "  "*5, command=view_purchase)

cart_menu = Menu(main_menu, tearoff=False)
main_menu.add_cascade(label="Sales", menu=cart_menu)
cart_menu.add_command(label="  "*5 + "Cart" + "  "*5, command=cart)
# cart_menu.add_separator()
# cart_menu.add_command(label="  "*5 + "Edit" + "  "*5)
cart_menu.add_separator()
cart_menu.add_command(label="  "*5 + "View" + "  "*5, command=view_sales)


root.mainloop()

