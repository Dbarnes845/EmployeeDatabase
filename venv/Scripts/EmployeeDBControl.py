import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk,Image
from datetime import datetime


root = Tk()
root.title('Employee Database')
root.geometry("800x600")
root.iconbitmap()


#Connect to the database for employees
connection = sqlite3.connect('Employ_Database.db')
#Create the cursor for the employee database
cursor = connection.cursor()
#Create The Table in the employee database if its not already there.
crttbl = """CREATE TABLE IF NOT EXISTS
Employees(Name TEXT PRIMARY KEY, Job_Title TEXT, Date_Of_Hire TEXT)"""
cursor.execute(crttbl)

#Connect to login database for user authentication
conn2 = sqlite3.connect('Employ_Database.db')
cursor2 = conn2.cursor()
crttbl2 = """CREATE TABLE IF NOT EXISTS
UserAuth(Username TEXT PRIMARY KEY, Password TEXT, Email TEXT)"""
cursor2.execute(crttbl2)

#Create the Table used for handling notifications
crttbl3 = """CREATE TABLE IF NOT EXISTS
Notifications(Type TEXT,Details TEXT,Date Text)"""
cursor.execute(crttbl3)
usern = "Not Logged In"
usernc = "Not Logged In"
datalogger = []

#Clear all notifications
def clearn():
    for record in ntree.get_children():
        ntree.delete(record)
    connection = sqlite3.connect('Employ_Database.db')
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Notifications")
    connection.commit()
    connection.close()
    messagebox.showinfo("Success","Notifications cleared")

#Create system notifications
def notifsys(type,details,date):
    connection = sqlite3.connect('Employ_Database.db')
    cursor = connection.cursor()

    cursor.execute("INSERT INTO Notifications VALUES (:ty, :det, :dt)",
                   {
                       'ty': type,
                       'det': details,
                       'dt': date
                   }
                )
    ntree.insert(parent='', index='end', iid=len(ntree.get_children()), values=(type,details,date))

    connection.commit()
    connection.close()

#On click event to get details of a row by double clicking
def graber(event):
    clear_entries()
    selected = tree.focus()
    data = tree.item(selected,'values')
    nm.insert(0,data[1])
    jbt.insert(0,data[2])
    doh.insert(0,data[3])
    id.insert(0,data[0])

#Register function, to store a username,password and email to the database
def register():
    conn2 = sqlite3.connect('Employ_Database.db')
    cursor2 = conn2.cursor()

    cursor.execute("INSERT or REPLACE INTO UserAuth VALUES (:un, :ps, :em)",
                   {
                       'un': loginuser.get(),
                       'ps': loginpass.get(),
                       'em': loginemail.get()
                   }
                )
    messagebox.showinfo("Success", "You have successfully Registered your information. Restart to log in.")
    conn2.commit()
    conn2.close()
    return

#Allows a user to logout
def logout():
    conn2 = sqlite3.connect('Login_Database.db')
    cursor2 = conn2.cursor()
    global usern
    usern_label.config(text = usernc)
    logt_btn.grid_remove()
    regi_btn.grid(row=5, column=11, columnspan=2, ipadx=10)
    loginuser_label.grid(row=2, column=8)
    loginpass_label.grid(row=3, column=8)
    loginemail_label.grid(row=4, column=8)
    loginuser.grid(row=2, column=9)
    loginpass.grid(row=3, column=9)
    loginemail.grid(row=4, column=9)
    logn_btn.grid(row=5, column=7, columnspan=2, ipadx=10)
    messagebox.showinfo("Success", "You have successfully Logged out.")
    usern = usernc
    conn2.commit()
    conn2.close()

#Login function
def login():
    conn2 = sqlite3.connect('Employ_Database.db')
    cursor2 = conn2.cursor()
    global usern
    hold = loginuser.get()
    cursor2.execute("SELECT * FROM UserAuth")
    records = cursor2.fetchall()

    i=0
    #Check the username and password from the entry boxes
    for record in records:
        if record[0] == loginuser.get():
            print(record[0]==loginuser.get())
            if record[1] != loginpass.get():
                conn2.commit()
                conn2.close()
                messagebox.showerror("Error","Incorrect Username or password")
                return
            i=1
            usern = record[0]
    if i == 0:
        conn2.commit()
        conn2.close()
        messagebox.showerror("Error","Incorrect Username or passowrd")
        return
    messagebox.showinfo("Success","You have successfully logged in.")
    usern_label.config(text = str(usern))
    #Clean up and getting rid of unneeded elements
    loginuser.grid_remove()
    loginpass.grid_remove()
    loginemail.grid_remove()
    loginuser_label.grid_remove()
    loginpass_label.grid_remove()
    loginemail_label.grid_remove()
    logn_btn.grid_remove()
    regi_btn.grid_remove()
    logt_btn.grid(row=5, column=9, columnspan=2, ipadx=10)
    conn2.commit()
    conn2.close()

#Add a employee to the system.
def submit():
    connection = sqlite3.connect('Employ_Database.db')
    cursor = connection.cursor()
    if usern == usernc:
        messagebox.showerror("Not Logged in!", "You have not logged in, please log in to continue")
        connection.commit()
        connection.close()
        return

    #Add to the table
    cursor.execute("INSERT or REPLACE INTO Employees VALUES (:nm, :jbt, :doh)",
                    {
                        'nm': nm.get(),
                        'jbt': jbt.get(),
                        'doh': doh.get()
                    }
                )

    connection.commit()
    connection.close()
    messagebox.showinfo("Success","Employee: " + nm.get() + " Has been Successfully added.")
    now = datetime.now()
    notifsys("New Entry","Added Employee: " + nm.get(),now.strftime("%m-%d-%Y %H:%M:%S"))
    clear_entries()

#clear after entry
def clear_entries():

    nm.delete(0,END)
    jbt.delete(0,END)
    doh.delete(0,END)
    id.delete(0,END)



#Remove an employee from the system
def delete():
    connection = sqlite3.connect('Employ_Database.db')
    cursor = connection.cursor()
    #code to search database here based on id

    if usern == usernc:
        messagebox.showerror("Not Logged in!", "You have not logged in, please log in to continue")
        connection.commit()
        connection.close()
        return

    if id.get() == '':
        connection.commit()
        connection.close()
        messagebox.showerror("Error!","No Id Given")
        return

    cursor.execute("SELECT *  FROM Employees WHERE oid=" + id.get())
    hold = cursor.fetchall()
    cursor.execute("DELETE from Employees WHERE oid=" + id.get())
    #SQL code to remove said found target from the database.
    connection.commit()
    connection.close()
    clear_entries()
    messagebox.showinfo("Deleted!",hold[0][0] + " Has Been removed from the Database!")
    now = datetime.now()
    notifsys("Deletion","Removed Employee: " + hold[0][0],now.strftime("%m-%d-%Y %H:%M:%S"))

#Refresh the table
def refresher():
    # Connect to the database
    connection = sqlite3.connect('Employ_Database.db')

    # Create the cursor
    cursor = connection.cursor()
    cursor.execute("SELECT oid,* FROM Employees")
    records = cursor.fetchall()
    print_records = ''
    i=0



    for record in records:
        if tree.exists(i):
            tree.delete(i)
        tree.insert(parent='',index='end',iid=i,values=record)
        i=i+1
    connection.commit()
    connection.close()
 #   tree.after(10000,refresher())

#Modify an existing employee in the database
def modify():
    connection = sqlite3.connect('Employ_Database.db')
    cursor = connection.cursor()
    if usern == usernc:
        messagebox.showerror("Not Logged in!","You have not logged in, please log in to continue")
        connection.commit()
        connection.close()
        return


#    hold = cursor.fetchall()
    cursor.execute("""UPDATE Employees SET
        Name = :name,
        Job_Title = :jobt,
        Date_Of_Hire = :date
        
        WHERE oid = :oid""",
        {
            'name': nm.get(),
            'jobt': jbt.get(),
            'date': doh.get(),
            'oid': id.get()
        }
        )
    now = datetime.now()
    notifsys("Update Entry","Updated Employee: " + nm.get(),now.strftime("%m-%d-%Y %H:%M:%S"))
    messagebox.showinfo("Success","Employee " + nm.get() + " Has been updated")
    connection.commit()
    connection.close()



#Create textboxes
nm = Entry(root, width=30)
nm.grid(row=0, column=1, padx=10)

jbt = Entry(root, width=30)
jbt.grid(row=1, column=1)

doh = Entry(root, width=30)
doh.grid(row=2, column=1)

id = Entry(root,width=10)
id.grid(row=3,column=1, pady=10)

loginuser = Entry(root,width=20)
loginuser.grid(row=2,column=9)

loginpass = Entry(root,width=20)
loginpass.grid(row=3,column=9)

loginemail = Entry(root,width=20)
loginemail.grid(row=4,column=9)

#loginemailn = Entry(root,width=20)
#loginemailn.grid()

#Create labels

nm_label = Label(root, text="Name")
nm_label.grid(row=0,column=0)

jbt_label = Label(root, text="Job Title")
jbt_label.grid(row=1,column=0)

doh_label = Label(root, text="Date of Hire")
doh_label.grid(row=2,column=0)

id_label = Label(root, text="ID of Employee to Modify or Delete")
id_label.grid(row=3, column=0)

user_label = Label(root, text="User: ")
user_label.grid(row=0,column=6,padx=10)

usern_label = Label(root, text=usern)
usern_label.grid(row=0,column=8)

loginuser_label = Label(root, text="Username")
loginuser_label.grid(row=2,column=8)

loginpass_label = Label(root,text="Password")
loginpass_label.grid(row=3,column=8)

loginemail_label = Label(root,text="Email")
loginemail_label.grid(row=4,column=8)

notif_label = Label(root,text="-------------Notifications--------------")
notif_label.grid(row=7,column=7,columnspan=6)

#Submit Button

sbmt_btn = Button(root, text="Add New Entry to Database", command=submit)
sbmt_btn.grid(row=4,column=0,columnspan=2, pady=0, padx=0,ipadx=100)

#Query Button
qry_btn = Button(root, text="Refresh the Table",command=refresher)
qry_btn.grid(row=6,column=0,columnspan=2, pady=0,padx=0,ipadx=137)

#Delete Button
dlt_btn = Button(root, text="Delete Record", command=delete)
dlt_btn.grid(row=5,column=0,columnspan=1, pady=10,padx=10,ipadx=20)

#Update Button
updt_btn = Button(root, text="Update Employee",command=modify)
updt_btn.grid(row=5,column=1,columnspan=1,pady=10,padx=10,ipadx=20)
#Login Button
logn_btn = Button(root, text= "Login", command=login)
logn_btn.grid(row=5,column=7,columnspan=2,ipadx=10)

#Logout button, not initially added
logt_btn = Button(root, text="Logout",command=logout)
#logt_btn.grid(row=5,column=9,columnspan=2,ipadx=10)

#Register button
regi_btn = Button(root,text = "Register",command=register)
regi_btn.grid(row=5,column=9,columnspan=2,ipadx=10)

#Clear all notifications
clrn_btn = Button(root,text = "Clear all Notifications",command=clearn)
clrn_btn.grid(row=6,column=8,columnspan=2)

#Create Tree/Table
tree = ttk.Treeview(root)

#Column Definition
tree['columns'] = ("ID","Name","Job Title","Date of Hire")

tree.column("#0",width=0, minwidth=0)
tree.column("ID",anchor=W,width=20)
tree.column("Name", anchor=W,width=120)
tree.column("Job Title",anchor=W,width=120)
tree.column("Date of Hire",anchor=W,width=120)

#Headings
tree.heading("#0",text="Phantom Column", anchor=W)
tree.heading("ID",text="ID",anchor=W)
tree.heading("Name", text="Name",anchor=W)
tree.heading("Job Title",text ="Job Title",anchor=W)
tree.heading("Date of Hire",text="Date of Hire",anchor=W)

#Add datebase to Table

cursor.execute("SELECT oid,* FROM Employees")
records = cursor.fetchall()
print_records = ''
i = 0
for record in records:
    tree.insert(parent='', index='end', iid=i, values=record)
    i = i + 1
tree.grid(row=8, column=0, columnspan=5)

#Notifcation tree
ntree = ttk.Treeview(root)

ntree['columns'] = ('Type','Details','Date')

ntree.column("#0",width=0, minwidth=0)
ntree.column("Type",width=70,minwidth=50)
ntree.column("Details",width=150,minwidth=100)
ntree.column("Date",width=100,minwidth=25)

ntree.heading("#0",text="Phantom Column",anchor=W)
ntree.heading("Type",text="Type",anchor=W)
ntree.heading("Details",text="Details",anchor=W)
ntree.heading("Date",text="M/D/Y",anchor=W)

ntree.grid(row=8,column=8,columnspan=5)

cursor.execute("SELECT * FROM Notifications")
records = cursor.fetchall()
i = 0
for record in records:
    print(record)
    ntree.insert(parent='',index='end',iid=len(ntree.get_children()),values=record)
    i=i+1

#add data to tree

# Binds!
tree.bind("<Double-1>", graber)




root.mainloop()

connection.commit()
connection.close()