import tkinter as tk
import sqlite3
import os.path

# class is used to access the database
class database:
    def __init__ (self):
        self.conn = sqlite3.connect("Account_database.db")
        self.cursor = self.conn.cursor()
        self.connbooks = sqlite3.connect("Account_books.db")
        self.bookcursor = self.connbooks.cursor()  

    def create_database(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS accounts (User TEXT, password TEXT, name TEXT, last_name TEXT, email TEXT, gender TEXT, age TEXT)")
        self.bookcursor.execute("CREATE TABLE IF NOT EXISTS books (username TEXT, password TEXT, book TEXT, author TEXT)")
    
    def register_database(self,user,password,name,lname,email,gender,age):
        self.cursor.execute("INSERT INTO accounts (User, password, name, last_name, email, gender, age) VALUES (?,?,?,?,?,?,?)",
                  (user,password,name,lname,email,gender,age))
        self.conn.commit()

    def get_accounts(self):
        self.cursor.execute("SELECT * FROM accounts")
        return self.cursor.fetchall()

    def get_name(self,username,passwords):
        self.cursor.execute('SELECT name FROM accounts WHERE User = ? AND password = ?',(username,passwords,))
        for row in self.cursor.fetchall():
            return row

    def get_lname(self,username,passwords):
        self.cursor.execute("SELECT last_name FROM accounts WHERE User = ? AND password = ?",(username,passwords,))
        for row in self.cursor.fetchall():
            return row
    
    def get_email(self,username,passwords):
        self.cursor.execute('SELECT email FROM accounts WHERE User =? AND password =?',(username,passwords,))
        for row in self.cursor.fetchall():
            return row

    def get_gender(self,username,passwords):
        self.cursor.execute("SELECT gender FROM accounts WHERE User = ? AND password = ?",(username,passwords,))
        for row in self.cursor.fetchall():
            return row
        
    def get_age(self,username,passwords):
        self.cursor.execute("SELECT age FROM accounts WHERE User = ? AND password = ?",(username,passwords,))
        for row in self.cursor.fetchall():
            return row
        
    def edited_info(self,username,passwords,NAME,LASTNAME,EMAIL,GENDER,AGE):
        self.cursor.execute('UPDATE accounts SET name = ?, last_name = ?, email = ?, gender = ?, age = ? WHERE User = ? AND password = ?',
                            (NAME,LASTNAME,EMAIL,GENDER,AGE,username,passwords,))
        self.conn.commit()

    def insert_book(self,user,temppass,tempbook,tempauthor):
        self.bookcursor.execute("INSERT INTO books(username, password, book, author) VALUES (?,?,?,?)",
                            (user,temppass,tempbook,tempauthor))
        self.connbooks.commit()

    def get_books(self,tempuser,temppass):
        self.bookcursor.execute("SELECT book, author FROM books WHERE username = ? AND password = ?",(tempuser,temppass,))
        return self.bookcursor.fetchall()

    def return_book(self,tempuser,temppass,return_book,tempauthor):
        self.bookcursor.execute("DELETE FROM books WHERE book =? AND author = ? AND username = ? AND password = ?",(return_book,tempauthor,tempuser,temppass,))
        self.connbooks.commit()
        return True        


#main class
class Library(tk.Tk):
    def __init__(self,HEIGHT,WIDTH):
        self.canvas = tk.Canvas(root, height = HEIGHT, width = WIDTH)
        self.canvas.pack()
        self.username = self.check_accounts
        self.password = self.check_accounts
        self.access = database()
    
    def starting_page(self):
        #GUI
        self.login_frame = tk.Frame(self.canvas, bg = 'blue')
        self.login_frame.place(relheight = 1, relwidth = 1)
        message = tk.Message (self.login_frame,width = 1000, font = ('courier',40), text = "PAULS LIBRARY") 
        message.place(relx = 0.5, anchor ='n', rely= 0.01)
        user = tk.Message (self.login_frame,width = 1000, font = ('courier',20), text = "USERNAME")
        user.place (relx = 0.25, rely = 0.3)
        password = tk.Message(self.login_frame,width = 1000, font = ('courier',20), text = "PASSWORD") 
        password.place (relx = 0.25, rely = 0.4)
        log_in = tk.Button (self.login_frame, text = 'LOG IN', width = 10, command = self.check_accounts )
        log_in.place (relx = 0.5, anchor = 'n',rely = 0.75)
        register = tk.Button (self.login_frame, text = 'Register', width = 20 , command = self.register_page)
        register.place (relx = 0.5, anchor = 'n',rely = 0.85)

        #User inputs their username and passwords
        self.username_entry = tk.Entry(self.login_frame, width = 30)
        self.username_entry.place(relx = 0.45, rely = 0.3)
        self.password_entry = tk.Entry(self.login_frame, width = 30, show ='*')
        self.password_entry.place(relx = 0.45, rely = 0.4)

    #class method is used to see if the users input is in the database
    def check_accounts(self):
        check = self.access.get_accounts()
        for row in check:
            if self.username_entry.get() == row[0]:
                if self.password_entry.get() == row[1]:
                    self.username = self.username_entry.get()
                    self.password = self.password_entry.get()
                    self.central_frame()
                else:
                    coverframe = tk.Frame(self.login_frame, bg = 'blue',height = 30)
                    coverframe.place(relx = 0.5, anchor = 'n', rely= 0.6,relwidth = 1)
                    message = tk.Message (self.login_frame,width = 1000, font = ('courier',15), text = "incorrect password")
                    message.place(relx = 0.5, anchor ='n', rely= 0.6)
                    break

            message = tk.Message (self.login_frame,width = 1000, font = ('courier',15), text = "Username not in database") 
            message.place(relx = 0.5, anchor ='n', rely= 0.6)

    def register_page(self):
        #GUI
        self.register_frame = tk.Frame(self.canvas, bg = 'blue')
        self.register_frame.place(relheight = 1, relwidth = 1)
        message = tk.Message(self.register_frame ,width = 1000, font = ('courier',40), text = "REGISTER") 
        message.place(relx = 0.5, anchor ='n', rely= 0.01)
        Username = tk.Message(self.register_frame,width = 1000, font = ('courier',15), text = "Username") 
        Username.place (relx = 0.05, rely = 0.2)
        password = tk.Message(self.register_frame,width = 1000, font = ('courier',15), text = "Password") 
        password.place (relx = 0.05, rely = 0.27)
        password_check = tk.Message(self.register_frame,width = 1000, font = ('courier',15), text = "Password check") 
        password_check.place (relx = 0.05, rely = 0.34)
        Name = tk.Message(self.register_frame,width = 1000, font = ('courier',15), text = "Name") 
        Name.place (relx = 0.05, rely = 0.41)
        Lastname = tk.Message(self.register_frame,width = 1000, font = ('courier',15), text = "Last Name") 
        Lastname.place (relx = 0.05, rely = 0.48)
        email = tk.Message(self.register_frame,width = 1000, font = ('courier',15), text = "Email") 
        email.place (relx = 0.05, rely = 0.55)
        gender = tk.Message(self.register_frame,width = 1000, font = ('courier',15), text = "Gender") 
        gender.place (relx = 0.05, rely = 0.62)
        age = tk.Message(self.register_frame,width = 1000, font = ('courier',15), text = "Age") 
        age.place (relx = 0.05, rely = 0.69)
        check_register = tk.Button(self.register_frame, text = 'Check password', font = ('courier',10), width = 20,command = self.password_check)
        check_register.place (relx = 0.67, rely = 0.34)
        register_button = tk.Button(self.register_frame, text ='Register', font = ('courier',15), width = 20, command = self.register)
        register_button.place (relx = 0.5, rely = 0.8, anchor = 'n')
        back_button = tk.Button(self.register_frame, text = 'Go back', font = ('courier',15), width =10, command = self.starting_page)
        back_button.place(relx = 0.05, rely = 0.9)

        #user is able to input their information into the database
        self.name_register_entry = tk.Entry(self.register_frame, width = 30 )
        self.name_register_entry.place(relx = 0.20, rely = 0.41)
        self.lastname_register_entry = tk.Entry(self.register_frame, width = 30 )
        self.lastname_register_entry.place(relx = 0.20, rely = 0.48)
        self.email_register_entry = tk.Entry(self.register_frame, width = 30 )
        self.email_register_entry.place(relx = 0.20, rely = 0.55)
        self.gender_register_entry = tk.Entry(self.register_frame, width = 30 )
        self.gender_register_entry.place(relx = 0.20, rely = 0.62)
        self.age_register_entry = tk.Entry(self.register_frame, width = 30 )
        self.age_register_entry.place(relx = 0.20, rely = 0.69)
        self.username_register_entry= tk.Entry(self.register_frame, width = 30 )
        self.username_register_entry.place(relx = 0.20, rely = 0.2)
        self.password_register_entry = tk.Entry(self.register_frame, width = 30, show = '*')
        self.password_register_entry.place(relx = 0.20, rely = 0.27)
        self.passwordcheck_register_entry = tk.Entry(self.register_frame, width = 30, show = '*')
        self.passwordcheck_register_entry.place(relx = 0.25, rely = 0.34)


    def password_check(self):

        if self.password_register_entry.get() == self.passwordcheck_register_entry.get():
            right = tk.Message(self.register_frame ,width = 1000, font = ('courier',20), text = "MATCH", fg = 'green', bg ='blue') 
            right.place(relx = 0.85, rely= 0.34)
            
        else:
            wrong = tk.Message(self.register_frame ,width = 1000, font = ('courier',20), text = "WRONG", fg = 'red', bg ='blue') 
            wrong.place(relx = 0.85, rely= 0.34)

    def register(self):

        message = tk.Message(self.register_frame,width = 1000, font = ('courier',15), text = "You have been succesfully register please click 'Go back' to log in") 
        message.place (relx = 0.5, rely = 0.85, anchor = 'n')
        account = database()
        account.register_database(self.username_register_entry.get(),self.password_register_entry.get(),self.name_register_entry.get(),self.lastname_register_entry.get(),self.email_register_entry.get(),self.gender_register_entry.get(),self.age_register_entry.get())
        
    def central_frame(self):
        
        self.lobby = tk.Frame(self.canvas, bg = 'blue')
        self.lobby.place(relheight = 1, relwidth = 1)
        check_books = tk.Button (self.lobby, text = 'check books', width = 35, command = self.checkbook_page,height = 10 )
        check_books.place (relx = 0.25, anchor = 'n',rely = 0.1)
        check_profile = tk.Button (self.lobby, text = 'check profile', width = 35, command = self.checkprofile_page,height = 10 )
        check_profile.place (relx = 0.75, anchor = 'n',rely = 0.1)
        log_out = tk.Button(self.lobby, text = 'log out', width = 35, command = self.starting_page,height = 5 )
        log_out.place (relx = 0.5, anchor = 'n',rely = 0.7)

    def checkprofile_page(self):
        #GUI
        #Information is retrieved from the database then displayed
        self.profile = tk.Frame(self.canvas, bg = 'blue')
        self.profile.place(relheight = 1, relwidth = 1)
        self.profilepage_format()
        Name_detail = tk.Message(self.profile,width = 1000, font = ('courier',15), text = self.access.get_name(self.username,self.password)) 
        Name_detail.place (relx = 0.2, rely = 0.3)
        Lname_detail = tk.Message(self.profile,width = 1000, font = ('courier',15), text = self.access.get_lname(self.username,self.password)) 
        Lname_detail.place (relx = 0.2, rely = 0.4)
        email_detail = tk.Message(self.profile,width = 1000, font = ('courier',15), text = self.access.get_email(self.username,self.password)) 
        email_detail.place (relx = 0.2, rely = 0.5)
        gender_detail = tk.Message(self.profile,width = 1000, font = ('courier',15), text = self.access.get_gender(self.username,self.password)) 
        gender_detail.place (relx = 0.2, rely = 0.6)
        age_detail = tk.Message(self.profile,width = 1000, font = ('courier',15), text = self.access.get_age(self.username,self.password)) 
        age_detail.place (relx = 0.2, rely = 0.7)
        back_button = tk.Button(self.profile, text = 'Go back', font = ('courier',15), width =10, command = self.central_frame)
        back_button.place(relx = 0.05, rely = 0.9)
        edit_button = tk.Button(self.profile, text = 'Edit profile', font = ('courier',15), width = 15, command = self.editprofile_page)
        edit_button.place(relx = 0.75, rely = 0.9)

    def profilepage_format(self):
        #GUI
        message = tk.Message(self.profile ,width = 1000, font = ('courier',40), text = "PROFILE") 
        message.place(relx = 0.5, anchor ='n', rely= 0.01)
        Name = tk.Message(self.profile,width = 1000, font = ('courier',15), text = "Name") 
        Name.place (relx = 0.05, rely = 0.3)
        Lastname = tk.Message(self.profile,width = 1000, font = ('courier',15), text = "Last Name") 
        Lastname.place (relx = 0.05, rely = 0.4)
        email = tk.Message(self.profile,width = 1000, font = ('courier',15), text = "Email") 
        email.place (relx = 0.05, rely = 0.5)
        gender = tk.Message(self.profile,width = 1000, font = ('courier',15), text = "Gender") 
        gender.place (relx = 0.05, rely = 0.6)
        age = tk.Message(self.profile,width = 1000, font = ('courier',15), text = "Age") 
        age.place (relx = 0.05, rely = 0.7)
        back_button = tk.Button(self.profile, text = 'Go back', font = ('courier',15), width =10, command = self.central_frame)
        back_button.place(relx = 0.05, rely = 0.9)
        

    def editprofile_page(self):
        
        self.profile = tk.Frame(self.canvas, bg = 'blue')
        self.profile.place(relheight = 1, relwidth = 1)
        self.profilepage_format()
        self.name_entry = tk.Entry(self.profile, width = 30 )
        self.name_entry.place(relx = 0.20, rely = 0.3)
        self.lastname_entry = tk.Entry(self.profile, width = 30 )
        self.lastname_entry.place(relx = 0.20, rely = 0.4)
        self.email_entry = tk.Entry(self.profile, width = 30 )
        self.email_entry.place(relx = 0.20, rely = 0.5)
        self.gender_entry = tk.Entry(self.profile, width = 30 )
        self.gender_entry.place(relx = 0.20, rely = 0.6)
        self.age_entry = tk.Entry(self.profile, width = 30 )
        self.age_entry.place(relx = 0.20, rely = 0.7)
        newedit_button = tk.Button(self.profile, text = 'EDIT', font = ('courier',15), width = 10, command = self.changeprofile_info)
        newedit_button.place(relx = 0.5, rely = 0.9,anchor = 'n')

    def changeprofile_info(self):
        self.access.edited_info(self.username,self.password,self.name_entry.get(),self.lastname_entry.get(),
            self.email_entry.get(),self.gender_entry.get(),self.age_entry.get())
        back_button = tk.Button(self.profile, text = 'You have changed your information', font = ('courier',15), width = 40, command = self.central_frame)
        back_button.place(relx = 0.5, rely = 0.85,anchor = 'n')
        

    def checkbook_page(self):
        books = self.access.get_books(self.username,self.password)
        print(books)
        yaxis = 0.25
        self.checkbook = tk.Frame(self.canvas, bg = 'blue')
        self.checkbook.place(relheight = 1,relwidth = 1)
        message = tk.Message(self.checkbook ,width = 1000, font = ('courier',40), text = "BOOKS") 
        message.place(relx = 0.5, anchor ='n', rely= 0.01)
        back_button = tk.Button(self.checkbook, text = 'Go back', font = ('courier',15), width = 10, command = self.central_frame)
        back_button.place(relx = 0.05, rely = 0.9)
        for item in books:
           
            book = tk.Message(self.checkbook,width = 1000, font = ('courier',15), text = item[0]) 
            book.place (relx = 0.05, rely = yaxis)
            author = tk.Message(self.checkbook,width = 1000, font = ('courier',15), text = item[1]) 
            author.place (relx = 0.8, rely = yaxis)
            yaxis += 0.08
            
        addbook_button = tk.Button(self.checkbook, text = 'add book', font = ('courier',15), width = 10, command = self.addbook_page)
        addbook_button.place(relx = 0.8, rely = 0.75,anchor = 'n')
        returnbook_button = tk.Button(self.checkbook, text = 'return book', font = ('courier',15), width = 15, command = self.returnbook)
        returnbook_button.place(relx = 0.8, rely = 0.8,anchor = 'n')
        book_title = tk.Message(self.checkbook,width = 1000, font = ('courier',20), text = 'BOOKS') 
        book_title.place (relx = 0.05, rely = 0.15)
        author_title = tk.Message(self.checkbook,width = 1000, font = ('courier',20), text = 'AUTHOR') 
        author_title.place (relx = 0.8, rely = 0.15)
        return_title = tk.Message(self.checkbook,width = 1000, font = ('courier',20), text = 'RETURN/CHECK OUT') 
        return_title.place (relx = 0.05, rely = 0.65)
        book_return = tk.Message(self.checkbook,width = 1000, font = ('courier',15), text = 'book')
        book_return.place(relx = 0.05, rely = 0.73)
        author_return = tk.Message(self.checkbook,width = 1000, font = ('courier',15), text = 'author')
        author_return.place(relx = 0.05, rely = 0.8)
        self.book_entry = tk.Entry(self.checkbook, width = 30 )
        self.book_entry.place(relx = 0.2, rely = 0.73)
        self.author_entry = tk.Entry(self.checkbook, width = 30 )
        self.author_entry.place(relx = 0.2, rely = 0.8)
     

    def returnbook(self):
        #User is able to return books but must be written exactly as shown
        self.access.return_book(self.username,self.password,self.book_entry.get(),self.author_entry.get())
        self.checkbook_page()
        

    def addbook_page(self):
        #User is able to add books unless they are over the 5 limit
        if len(self.access.get_books(self.username,self.password)) < 5:
            if len(self.author_entry.get()) > 0 and len(self.book_entry.get()) > 0:
                self.access.insert_book(self.username,self.password,self.book_entry.get(),self.author_entry.get())
                self.checkbook_page()
            else:
                message = tk.Message(self.checkbook,width = 1000, font = ('courier',15), text = "Please fill in the boxes") 
                message.place(relx = 0.5, anchor ='n', rely= 0.9)
        else:
            message = tk.Message(self.checkbook,width = 1000, font = ('courier',15), text = "Limit of books reached,return at least 1") 
            message.place(relx = 0.5, anchor ='n', rely= 0.9)
        
        
                                                                                                                                                                                                          

HEIGHT = 500
WIDTH = 700            
        
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "Account_database.db")
db_path2 = os.path.join(BASE_DIR, "Account_books.db")

root = tk.Tk()
screen = Library(HEIGHT, WIDTH)
create_database = database()
create_database.create_database()
screen.starting_page()
root.mainloop()






        
        



    
        




