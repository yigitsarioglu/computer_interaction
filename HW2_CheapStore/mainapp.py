import customtkinter

import sqlite3
from CTkMessagebox import CTkMessagebox
from CTkListbox import *
from tkcalendar import Calendar
import tkinter as tk
from tkinter import ttk
from datetime import datetime


from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import os

# Sets the appearance of the window Supported modes : Light, Dark, System
# "System" sets the appearance mode to  the appearance mode of the system
customtkinter.set_appearance_mode("dark")   
 
# Sets the color of the widgets in the window
# Supported themes : green, dark-blue, blue    
customtkinter.set_default_color_theme("green")    
 
# Dimensions of the window
appWidth, appHeight = 850, 800

 
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Sets the title of the window to "App"
        self.title("Cheap Store Page")   
        # Sets the dimensions of the window to 600x700
        self.geometry(f"{appWidth}x{appHeight}")  

        


        # Database initialization
        self.conn = sqlite3.connect('library.db')
        self.c = self.conn.cursor()
        self.create_table()

        # Create main frame
        self.main_frame = customtkinter.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew")  # Ana pencereye grid yöneticisini kullanarak yerleştiriyoruz
        self.grid_rowconfigure(0, weight=1)  # Ana pencerenin satırını genişletmek için ağırlık belirliyoruz
        self.grid_columnconfigure(0, weight=1)  # Ana pencerenin sütununu genişletmek için ağırlık belirliyoruz

        # Create order list
        self.username=""
        self.order_list = []  # Siparişlerin listesi
        self.total_cost = 0   # Toplam tutar
        self.load_product_prices()



        
        # Show main page initially
        self.show_main_page() 


    def create_table(self):
        
        self.c.execute('''CREATE TABLE IF NOT EXISTS users (
         username TEXT NOT NULL PRIMARY KEY,
         password TEXT NOT NULL,
         name TEXT,
         surname TEXT,
         age INTEGER,
         gender TEXT,
         occupation TEXT,
         address TEXT,
         state TEXT,
         city TEXT)''')
        

        self.c.execute (''' CREATE TABLE IF NOT EXISTS products (
	        product_id	INTEGER NOT NULL PRIMARY KEY,
	        price	INTEGER NOT NULL,
	        name	TEXT,
	        stock	INTEGER ) ''' )
        
        self.c.execute (''' CREATE TABLE IF NOT EXISTS  myorders (
	        order_id	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT ,
	        catalog_number	INTEGER NOT NULL,
	        quantity	INTEGER NOT NULL,
	        total_cost	INTEGER NOT NULL,
	        username	TEXT NOT NULL,
	        receipt_number	INTEGER NOT NULL,
            FOREIGN KEY (receipt_number) REFERENCES receipt(receipt_number) )  ''' )
        

        self.c.execute (''' CREATE TABLE IF NOT EXISTS  receipt (
	        receipt_number	INTEGER NOT NULL PRIMARY KEY ,
            username	TEXT NOT NULL,
            name	TEXT NOT NULL,
            phone	INTEGER NOT NULL,
            postalcode	INTEGER NOT NULL,
            province	TEXT NOT NULL,
            city	TEXT NOT NULL,            
            delivery_adress	TEXT NOT NULL,
            creditcard	INTEGER,
	        validation_id	INTEGER,
            totalcosts	INTEGER,
	        orderdate	TEXT NOT NULL )  ''' )
          
        self.conn.commit()


       # Function to validate login
    def validate_login(self):

        username = self.entry_login_username.get()
        password = self.entry_login_password.get()
    
        # Query the database for the given username
        self.c.execute("SELECT * FROM users WHERE username=?", (username,))
        user = self.c.fetchone()
    
        if user:
            # Check if the password matches
            if user[1] == password:
                # CTkMessagebox(title="Success" , message="Login successful" , icon="check")
                self.username = username
                self.show_entrance_page()
               
            else:
                CTkMessagebox(title="Warning" , message="Invalid password" , icon="warning")
                
        else:
            CTkMessagebox(title="Error" , message="User not found" , icon="cancel")

    
    # Function to register a new user
    def register_user(self):
        
        username = self.entry_register_username.get()
        password = self.entry_register_password.get()

        dbname = self.nameEntry.get()
        dbsurname = self.surnameEntry.get()
        dbage= self.ageEntry.get()
        dbcity = self.cityEntry.get()
        dbstate =self.stateEntry.get()
        dbadress = self.addressEntry.get()
        selected_gender = self.genderVar.get()
        selected_occupation = self.occupationOptionMenu.get()

        if username == '' :
            CTkMessagebox(title="Warning" , message="Username cannot be empty" , icon="warning")
        
        elif password == '' :
            CTkMessagebox(title="Warning" , message="Password cannot be empty" , icon="warning")

        else :
            # Check if username already exists in the database
            self.c.execute("SELECT * FROM users WHERE username=?", (username,))
            existing_user = self.c.fetchone()
        
            if existing_user:
                CTkMessagebox(title="Warning" , message="Username already exists" , icon="warning")
                
            else:
                # Insert new user into the database
                self.c.execute("INSERT INTO users (username, password,name,surname,age,gender,occupation,address,state,city) VALUES (?, ?,?,?,?,?,?,?,?,?)", (username, password,dbname,dbsurname,dbage,selected_gender,selected_occupation,dbadress,dbstate,dbcity))
                self.conn.commit()
                CTkMessagebox(title="Success", message="Registration successful" , icon="check")


    def load_product_prices(self):
        # Ürün fiyatlarını products veritabanından yükle
        try:
            conn = sqlite3.connect('library.db')
            c = conn.cursor()
            c.execute("SELECT product_id, price FROM products")
            self.product_prices = dict(c.fetchall())
            print(self.product_prices)
            conn.close()
        except sqlite3.Error as e:
            print("Error loading product prices:", e)       




    def create_order_page(self):
        # Sipariş oluşturma işlevi
        self.show_create_order_page()

    def show_orders(self):
        # Siparişleri görüntüleme işlevi
        self.show_myorder_page()
        

    def edit_profile(self):
        # Kullanıcı bilgilerini düzenleme işlevi
        print("Edit profile")
    
    def add_catalog_item(self):
        #Adding catalog item
        self.add_catalog_item_page()
    



     
 

    def show_main_page(self):
        # Clear existing widgets
        self.clear_widgets()

       
        # Create widgets for main page
        my_font=customtkinter.CTkFont(family='Calibri', size=48, weight='bold')
        self.label_main = customtkinter.CTkLabel(self.main_frame, font=my_font, text="Welcome to Cheap Store App" )
        self.label_main.grid(row=0, column=3, padx=100, pady=100, sticky="ew")

        self.login_button = customtkinter.CTkButton(self.main_frame, text="Login", command=self.show_login_page)
        self.login_button.grid(row=1, column=3, padx=20, pady=20 )

        self.register_button = customtkinter.CTkButton(self.main_frame, text="Register", command=self.show_register_page)
        self.register_button.grid(row=2, column=3, padx=20, pady=20)

    def show_login_page(self): 

         # Clear existing widgets
        self.clear_widgets()

        # Create widgets for login page
        my_font=customtkinter.CTkFont(family='Calibri', size=48, weight='bold')
        self.label_login = customtkinter.CTkLabel(self.main_frame, text="Login Page", font=my_font)
        self.label_login.grid(row=0, column=0, columnspan=3 , padx=(280,0) , pady=(100,50) )
        

        label_font=customtkinter.CTkFont(family='Calibri', size=16)
        # Your login page widgets here...
        self.label_login_username = customtkinter.CTkLabel(self.main_frame, text="Username", font=label_font)
        self.label_login_username.grid(row=1, column=0, sticky="w", padx=(220,0),pady=(0, 10))
        
        self.entry_login_username = customtkinter.CTkEntry(self.main_frame)
        self.entry_login_username.grid(row=1, column=1, pady=(0, 10), padx=10)
        

        self.label_login_password = customtkinter.CTkLabel(self.main_frame, text="Password" , font=label_font)
        self.label_login_password .grid(row=2, column=0, sticky="w", padx=(220,0), pady=(0, 10))
        self.entry_login_password = customtkinter.CTkEntry(self.main_frame, show="*")
        self.entry_login_password.grid(row=2, column=1, pady=(0, 10), padx=10)

         # Remember Me check button
        self.remember_me =  customtkinter.CTkCheckBox(self.main_frame, text="Remember Me")
        self.remember_me.grid(row=3, column=1, pady=(0, 10))
       

        self.login_button = customtkinter.CTkButton(self.main_frame, text="Login", command=self.validate_login)
        self.login_button.grid(row=4, column=1, pady=(10, 20), sticky="ew")

       
        #Back button
        self.back_button = customtkinter.CTkButton(self.main_frame, text="Back", command=self.show_main_page)
        self.back_button.grid(row=6, column=1, pady=(10, 20), sticky="ew")

 


    def show_register_page(self):

          # Clear existing widgets
        self.clear_widgets()


         # Create widgets for register page
        my_font=customtkinter.CTkFont(family='Calibri', size=22, weight='bold')
        self.label_register = customtkinter.CTkLabel(self.main_frame, text="Register Page", font=my_font)
        self.label_register.grid(row=0, column=1, columnspan=3, padx=20, pady=20, sticky="ew")


        self.label_register_username = customtkinter.CTkLabel (self.main_frame, text="Username")
        self.label_register_username.grid(row=1, column=0, padx=20, pady=20, sticky="ew")

        self.entry_register_username = customtkinter.CTkEntry(self.main_frame)
        self.entry_register_username.grid(row=1, column=1, padx=20, pady=20, sticky="ew")

        self.label_register_password = customtkinter.CTkLabel(self.main_frame, text="Password")
        self.label_register_password.grid(row=1, column=2, padx=20, pady=20, sticky="ew")

        self.entry_register_password = customtkinter.CTkEntry(self.main_frame, show="*")
        self.entry_register_password.grid(row=1, column=3, padx=20, pady=20, sticky="ew")


         # Name Label
        self.nameLabel = customtkinter.CTkLabel( self.main_frame, text="Name")
        self.nameLabel.grid(row=2, column=0, padx=20, pady=20, sticky="ew")
 
        # Name Entry Field
        self.nameEntry = customtkinter.CTkEntry( self.main_frame, placeholder_text="Mehmet")
        self.nameEntry.grid(row=2, column=1, padx=20, pady=20, sticky="ew")

        # SurnaName Label
        self.surnameLabel = customtkinter.CTkLabel( self.main_frame, text="Surname")
        self.surnameLabel.grid(row=2, column=2, padx=20, pady=20, sticky="ew")
 
        # Name Entry Field
        self.surnameEntry = customtkinter.CTkEntry( self.main_frame, placeholder_text="Yılmaz")
        self.surnameEntry.grid(row=2, column=3, columnspan=3, padx=20, pady=20, sticky="ew")
 
        # Age Label
        self.ageLabel = customtkinter.CTkLabel(self.main_frame , text="Age")
        self.ageLabel.grid(row=3, column=0, padx=20, pady=20, sticky="ew")
 
        # Age Entry Field
        self.ageEntry = customtkinter.CTkEntry(self.main_frame , placeholder_text="18")
        self.ageEntry.grid(row=3, column=1, columnspan=3, padx=20, pady=20, sticky="ew")


        # Gender Label
        self.genderLabel = customtkinter.CTkLabel(self.main_frame ,  text="Gender")
        self.genderLabel.grid(row=4, column=0, padx=20, pady=20, sticky="ew")
 
        # Gender Radio Buttons
        self.genderVar = customtkinter.StringVar(value="Prefer\ not to say")
 
        self.maleRadioButton = customtkinter.CTkRadioButton(self.main_frame, text="Male", variable=self.genderVar, value="He is")
        self.maleRadioButton.grid(row=4, column=1, padx=20, pady=20, sticky="ew")
 
        self.femaleRadioButton = customtkinter.CTkRadioButton(self.main_frame, text="Female", variable=self.genderVar, value="She is")
        self.femaleRadioButton.grid(row=4, column=2, padx=20, pady=20, sticky="ew")
         
        self.noneRadioButton = customtkinter.CTkRadioButton(self.main_frame, text="Prefer not to say", variable=self.genderVar, value="They are")
        self.noneRadioButton.grid(row=4, column=3, padx=20, pady=20,  sticky="ew")


        # City Label
        self.cityLabel = customtkinter.CTkLabel(self.main_frame , text="City")
        self.cityLabel.grid(row=5, column=0, padx=20, pady=20, sticky="ew")

        # City Entry Field
        self.cityEntry = customtkinter.CTkEntry(self.main_frame , placeholder_text="Ankara")
        self.cityEntry.grid(row=5, column=1, padx=20, pady=20, sticky="ew")


        # State Label
        self.stateLabel = customtkinter.CTkLabel(self.main_frame , text="State/Region")
        self.stateLabel.grid(row=5, column=2, padx=20, pady=20, sticky="ew")

        # State Entry Field
        self.stateEntry = customtkinter.CTkEntry(self.main_frame , placeholder_text="Mamak")
        self.stateEntry.grid(row=5, column=3, padx=20, pady=20, sticky="ew")


        # Adress Label
        self.addressLabel = customtkinter.CTkLabel(self.main_frame , text="Adress")
        self.addressLabel.grid(row=6, column=0, padx=20, pady=20, sticky="ew")

        # Address Entry Field
        self.addressEntry = customtkinter.CTkEntry(self.main_frame , placeholder_text="Main Street")
        self.addressEntry.grid(row=6, column=1, columnspan=3, padx=20, pady=20, sticky="ew")
 

        
 
        # Occupation Label
        self.occupationLabel = customtkinter.CTkLabel(self.main_frame, text="Occupation")
        self.occupationLabel.grid(row=7, column=0, padx=20, pady=20, sticky="ew")
 
        # Occupation combo box
        self.occupationOptionMenu = customtkinter.CTkOptionMenu(self.main_frame,
                                        values=["Customer",
                                        "Working Professional"])
        self.occupationOptionMenu.grid(row=7, column=1, padx=20, pady=20, columnspan=2, sticky="ew")

        # Register Button
        self.registerButton = customtkinter.CTkButton(self.main_frame , text="Register" , command=self.register_user)
        self.registerButton.grid(row=8, column=1, columnspan=2, padx=20, pady=20, sticky="ew")


        self.back_button = customtkinter.CTkButton(self.main_frame, text="Back", command=self.show_main_page)
        self.back_button.grid(row=10, column=1, columnspan=1, padx=20, pady=20, sticky="ew")


    def show_entrance_page(self):

        # Clear existing widgets
        self.clear_widgets()

        self.c.execute("SELECT name, surname FROM users WHERE username=?", (self.username,))
        user_info = self.c.fetchone()

        # Eğer kullanıcı bilgisi bulunduysa, bilgileri al ve göster
        if user_info:
            name, surname = user_info
            CTkMessagebox(title="User Info", message= f"Welcome to Store App \n {name} {surname}")
        else:
            CTkMessagebox( title= "Error", message= "User information not found")

        test_txt= "Username :  " + self.username
        self.label_user_name = customtkinter.CTkLabel (self.main_frame, text= test_txt) 
        self.label_user_name.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        # Sipariş oluşturma butonu
        btn_create_order = customtkinter.CTkButton(self.main_frame, text="Create Order", command=self.create_order_page )
        btn_create_order.grid(row=1, column=1, padx=20, pady=20, sticky="ew")

        # Siparişleri görüntüleme butonu
        btn_show_orders = customtkinter.CTkButton(self.main_frame, text="Show My Orders", command=self.show_orders )
        btn_show_orders.grid(row=1, column=2, padx=20, pady=20, sticky="ew")

        # Add new catalog item
        btn_edit_profile = customtkinter.CTkButton(self.main_frame, text="Add New Catalog Item", command=self.add_catalog_item )
        btn_edit_profile.grid(row=1, column=3, padx=20, pady=20, sticky="ew")

        #Back button
        self.back_button = customtkinter.CTkButton(self.main_frame, text="Back", command=self.ask_logout )
        self.back_button.grid(row=2, column=1, padx=20, pady=20, sticky="ew")

        #Program Quit Button
        self.quit_button = customtkinter.CTkButton(self.main_frame, text="Quit", command=self.ask_question )
        self.quit_button.grid(row=2, column=2, padx=20, pady=20, sticky="ew")

    
    def show_create_order_page(self):

        # Clear existing widgets
        self.clear_widgets()

        # Create widgets for purchaser
        my_font=customtkinter.CTkFont(family='Calibri', size=22, weight='bold')
        self.label_purchaser = customtkinter.CTkLabel(self.main_frame, text="Purchaser", font=my_font)
        self.label_purchaser.grid(row=0, column=1, columnspan=3, padx=20, pady=20, sticky="ew")

        # Name
        label_name = customtkinter.CTkLabel(self.main_frame, text="Name:")
        label_name.grid(row=1, column=0, padx=5, pady=5)
        self.purch_name_entry = customtkinter.CTkEntry(self.main_frame)
        self.purch_name_entry.grid(row=1, column=1, padx=5, pady=5)

        # Phone
        label_phone = customtkinter.CTkLabel(self.main_frame, text="Phone:")
        label_phone.grid(row=1, column=2, padx=5, pady=5)
        self.purch_phone_entry = customtkinter.CTkEntry(self.main_frame)
        self.purch_phone_entry.grid(row=1, column=3, padx=5, pady=5)

        # Postal Code
        label_postal_code = customtkinter.CTkLabel(self.main_frame, text="Postal Code:")
        label_postal_code.grid(row=2, column=0, padx=5, pady=5)
        self.postal_code_entry = customtkinter.CTkEntry(self.main_frame)
        self.postal_code_entry.grid(row=2, column=1, padx=5, pady=5)

        # Province
        label_province = customtkinter.CTkLabel(self.main_frame, text="Province:")
        label_province.grid(row=2, column=2, padx=5, pady=5)
        self.province_entry = customtkinter.CTkEntry(self.main_frame)
        self.province_entry.grid(row=2, column=3, padx=5, pady=5)

        # City
        label_city = customtkinter.CTkLabel(self.main_frame, text="City:")
        label_city.grid(row=2, column=4, padx=5, pady=5)
        self.city_entry = customtkinter.CTkEntry(self.main_frame)
        self.city_entry.grid(row=2, column=5, padx=5, pady=5)

        # Delivery Address
        label_delivery_address = customtkinter.CTkLabel(self.main_frame, text="Delivery Address:")
        label_delivery_address.grid(row=3, column=0, padx=5, pady=5)
        self.delivery_address_entry = customtkinter.CTkEntry(self.main_frame, width=500)
        self.delivery_address_entry.grid(row=3, column=1, columnspan=3, padx=5, pady=5)
        

        # Today's Date
        label_date = customtkinter.CTkLabel(self.main_frame, text="Today's Date:")
        label_date.grid(row=4, column=0, padx=5, pady=5)
        #self.date_entry = customtkinter.CTkEntry(self.main_frame)
        #self.date_entry.grid(row=4, column=1, padx=5, pady=5)

        style = ttk.Style(self)
        style.theme_use("default")

        self.cal_entry = Calendar(self.main_frame , selectmode='day', locale='en_US', disabledforeground='red',
               cursor="hand2", background=customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"][1],
               selectbackground=customtkinter.ThemeManager.theme["CTkButton"]["fg_color"][1])
        self.cal_entry.grid(row=4, column=1, padx=10, pady=10)



        # Credit Card Number
        label_credit_card = customtkinter.CTkLabel(self.main_frame, text="Credit Card No:")
        label_credit_card.grid(row=5, column=0, padx=5, pady=5)
        self.credit_card_entry = customtkinter.CTkEntry(self.main_frame)
        self.credit_card_entry.grid(row=5, column=1, padx=5, pady=5)

        # Validation ID
        label_validation_id = customtkinter.CTkLabel(self.main_frame, text="Validation ID:")
        label_validation_id.grid(row=5, column=2, padx=5, pady=5)
        self.validation_id_entry = customtkinter.CTkEntry(self.main_frame)
        self.validation_id_entry.grid(row=5, column=3, padx=5, pady=5)



        # Create widgets for catalog items
        self.label_catalog_item = customtkinter.CTkLabel(self.main_frame, text="Catalog item", font=my_font)
        self.label_catalog_item.grid(row=6, column=1, columnspan=3, padx=20, pady=20, sticky="ew")


        # Katalog numarası girişi için etiket ve giriş kutusu
        label_item = customtkinter.CTkLabel(self.main_frame, text="Catalog number:")
        label_item.grid(row=7, column=0, padx=5, pady=5)
        self.item_entry = customtkinter.CTkEntry(self.main_frame)
        self.item_entry.grid(row=7, column=1, padx=5, pady=5)

        # Miktar girişi için etiket ve giriş kutusu
        label_quantity = customtkinter.CTkLabel(self.main_frame, text="Quantity:")
        label_quantity.grid(row=8, column=0, padx=5, pady=5)
        self.quantity_entry = customtkinter.CTkEntry(self.main_frame)
        self.quantity_entry.grid(row=8, column=1, padx=5, pady=5)

        # Ekle butonu
        btn_add = customtkinter.CTkButton(self.main_frame, text="Add", command=self.add_order)
        btn_add.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

        # Sil butonu
        btn_delete = customtkinter.CTkButton(self.main_frame, text="Drop", command=self.delete_order)
        btn_delete.grid(row=9, column=2, padx=5, pady=5)

        # Siparişlerin listeleneceği liste kutusu
        self.order_listbox = CTkListbox(self.main_frame, width=200)
        self.order_listbox.grid(row=10, column=1, columnspan=2, padx=5, pady=5)


        # Fatura oluştur butonu
        btn_create_invoice = customtkinter.CTkButton(self.main_frame, text="Trigger Invoice", command=self.create_invoice)
        btn_create_invoice.grid(row=11, column=1, padx=5, pady=5)

        self.back_button = customtkinter.CTkButton(self.main_frame, text="Back", command=self.show_entrance_page)
        self.back_button.grid(row=11, column=2, columnspan=1, padx=20, pady=20, sticky="ew")

        # Toplam tutar etiketi
        self.label_total_cost = customtkinter.CTkLabel(self.main_frame , text="Toplam Tutar: 0")
        self.label_total_cost.grid(row=12, column=0, columnspan=2, padx=5, pady=5)


    


    
    def add_catalog_item_page(self):
        
        # Clear existing widgets
        self.clear_widgets()

        # Product ID
        self.label_id = customtkinter.CTkLabel(self.main_frame, text="Product ID:")
        self.label_id.grid(row=0, column=0, padx=5, pady=5)
        self.entry_id = customtkinter.CTkEntry(self.main_frame)
        self.entry_id.grid(row=0, column=1, padx=5, pady=5)

        # Price
        self.label_price = customtkinter.CTkLabel(self.main_frame, text="Price:")
        self.label_price.grid(row=1, column=0, padx=5, pady=5)
        self.entry_price = customtkinter.CTkEntry(self.main_frame)
        self.entry_price.grid(row=1, column=1, padx=5, pady=5)

        # Name
        self.label_name = customtkinter.CTkLabel(self.main_frame, text="Name:")
        self.label_name.grid(row=2, column=0, padx=5, pady=5)
        self.entry_name = customtkinter.CTkEntry(self.main_frame)
        self.entry_name.grid(row=2, column=1, padx=5, pady=5)

        # Stock
        self.label_stock = customtkinter.CTkLabel(self.main_frame, text="Stock:")
        self.label_stock.grid(row=3, column=0, padx=5, pady=5)
        self.entry_stock = customtkinter.CTkEntry(self.main_frame)
        self.entry_stock.grid(row=3, column=1, padx=5, pady=5)

        # Save Button
        self.btn_save = customtkinter.CTkButton(self.main_frame, text="Save", command=self.save_product)
        self.btn_save.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        self.back_button = customtkinter.CTkButton(self.main_frame, text="Return Home", command=self.show_entrance_page)
        self.back_button.grid(row=4, column=2, columnspan=1, padx=20, pady=20, sticky="ew")

    def save_product(self):

        # Get values from entries
        product_id = self.entry_id.get()
        price = self.entry_price.get()
        name = self.entry_name.get()
        stock = self.entry_stock.get()

        # Check if all fields are filled
        if product_id and price and name and stock:
            try:
                # Connect to the database
                conn = sqlite3.connect('library.db')
                c = conn.cursor()

                # Check if the product_id already exists
                c.execute("SELECT * FROM products WHERE product_id=?", (product_id,))
                existing_product = c.fetchone()
                if existing_product:
                    CTkMessagebox( title= "Error", icon="warning", message= "Product ID already exists. Please choose a different one.")
                
                else:
                    # Insert values into the table
                    c.execute("INSERT INTO products (product_id, price, name, stock) VALUES (?, ?, ?, ?)", (product_id, price, name, stock))
                    conn.commit()
                    conn.close()

                    CTkMessagebox( title= "Success", icon="check",  message= "Product saved successfully!")
                    self.load_product_prices()

                    # Clear entries after saving
                    self.entry_id.delete(0, customtkinter.END)
                    self.entry_price.delete(0, customtkinter.END)
                    self.entry_name.delete(0, customtkinter.END)
                    self.entry_stock.delete(0, customtkinter.END)

            except sqlite3.Error as e:
                CTkMessagebox( title= "Error", icon="warning", message= f"Error saving product: {e}" )
               
        else:
            CTkMessagebox( title= "Error", message= "Please fill all fields.")
    
    def add_order(self):
        try:
            item = int(self.item_entry.get())
            quantity = int(self.quantity_entry.get())

            if quantity<=0 :
                CTkMessagebox( title= "Warning", message= "Invalid quantity, it should be a positive number")

            else:
                if item in self.product_prices:
                    # Siparişi sepete ekle
                    self.order_list.append((item, quantity))

                    # Sepete eklenen siparişi göster
                    self.order_listbox.insert(customtkinter.END, f"catalog no:{item} -  quantity: {quantity}")

                    # Toplam tutarı güncelle
                    self.total_cost += self.product_prices[item] * quantity
                    self.label_total_cost.configure(text=f"Toplam Tutar: {self.total_cost}")

                    # Giriş kutularını temizle
                    self.item_entry.delete(0, customtkinter.END)
                    self.quantity_entry.delete(0, customtkinter.END)
    
                else :
                    CTkMessagebox( title= "Warning", message= "Invalid catalog number")

        except ValueError:
            CTkMessagebox( title= "Error", message= "Invalid entry")

    def delete_order(self):

        try:
            # Seçilen siparişi sil
            selected_index = self.order_listbox.curselection()

            if selected_index >= 0:
                
                # Toplam tutarı güncelle
                product_id = self.order_list[selected_index][0]
                quantity = self.order_list[selected_index][1]
                self.total_cost -= self.product_prices[product_id] * quantity
                self.label_total_cost.configure(text=f"Toplam Tutar: {self.total_cost}")

                # Clears from the screen
                self.order_listbox.delete(selected_index)
                print("selected index: ", selected_index)
                del self.order_list[selected_index]
                
        except Exception as e:
            CTkMessagebox( title= "Error", message= "Invalid selection for drop")


    def create_invoice(self):

        if self.order_list:
            try:
                # Connect to the database
                conn = sqlite3.connect('library.db')
                c = conn.cursor()

                # Get the last receipt_id
                c.execute("SELECT MAX(receipt_number) FROM myorders")
                last_receipt_id = c.fetchone()[0]  or 0  # If the table is empty, set last_order_id to 0
                last_receipt_id= last_receipt_id +1
                
                # print(last_receipt_id)

                # Insert new orders
                for order in self.order_list:
                     
                    pr_price = self.product_prices[order[0]]
                    cost= pr_price * order[1]
                    c.execute("INSERT INTO myorders (catalog_number, quantity, total_cost, username, receipt_number) VALUES (?, ?, ?, ?, ?)", (order[0], order[1], cost, self.username, last_receipt_id ))
                

               

                # Convert the date string to the appropriate format
                selected_date = self.cal_entry.get_date()
                selected_date_obj = datetime.strptime(selected_date, "%m/%d/%y")  # Parse the string to a datetime object
                formatted_date_str = selected_date_obj.strftime("%Y-%m-%d")  # Format the datetime object to the desired format
                name = self.purch_name_entry.get()
                phone = int (self.purch_phone_entry.get())
                postalcode = int(self.postal_code_entry.get() )
                province = self.province_entry.get()
                city = self.city_entry.get()
                delivery_adress = self.delivery_address_entry.get()
                creditcard = int ( self.credit_card_entry.get() )
                validation_id = int ( self.validation_id_entry.get() )


            
                # Insert the data into the receipt table
                c.execute("INSERT INTO receipt (receipt_number, username, name, phone, postalcode, province, city, delivery_adress, creditcard, validation_id, totalcosts, orderdate) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?)",
                (last_receipt_id, self.username, name , phone , postalcode, province ,city , delivery_adress , creditcard, validation_id, self.total_cost, formatted_date_str ) )        


                conn.commit()
                conn.close()
                
                CTkMessagebox( title= "Invoice", message= "Your invoice has been created.")
                

                # Clear the order list and update the total cost label
                self.order_list = []
                self.order_listbox.delete(0, customtkinter.END)
                self.label_total_cost.configure(text="Toplam Tutar: 0")
                self.total_cost=0

            except sqlite3.Error as e:
                CTkMessagebox( title= "Error", message= f"Error creating invoice: {e}")
                
        else:
            CTkMessagebox( title= "Error", message= "Your cart is empty.")
            
       
    def show_myorder_page(self):

        # Clear existing widgets
        self.clear_widgets()

         
         # Create widgets for purchaser
        my_font=customtkinter.CTkFont(family='Calibri', size=24, weight='bold')
        self.label_myorder = customtkinter.CTkLabel(self.main_frame, text="MY ORDERS", font=my_font)
        self.label_myorder.grid(row=0, column=1, columnspan=3, padx=20, pady=20, sticky="ew")

        self.treeview = ttk.Treeview(self.main_frame, columns=("receipt_number", "orderdate", "totalcost"))
        self.treeview.heading("#0", text="Number")
        self.treeview.heading("receipt_number", text="Receipt Number")
        self.treeview.heading("orderdate", text="Order Date")
        self.treeview.heading("totalcost", text="Total Cost")
        self.treeview.bind("<ButtonRelease-1>", self.show_order_details )
        self.treeview.bind("<ButtonRelease-3>", self.release_selection)

        self.treeview.grid(row=1, column=1, padx=10, pady=10)

        #Back button
        self.back_button = customtkinter.CTkButton(self.main_frame, text="Back", command=self.show_entrance_page)
        self.back_button.grid(row=10, column=1, padx=5, pady=5, sticky="ew")

        #Create invoice
        self.create_invoice_button = customtkinter.CTkButton(self.main_frame, text="Create Invoice Pdf File", command=self.create_pdf_file )
        self.create_invoice_button.grid(row=10, column=2, padx=5, pady=5, sticky="ew")

        #Program Quit Button
        self.quit_button = customtkinter.CTkButton(self.main_frame, text="Quit", command=self.ask_question )
        self.quit_button.grid(row=12, column=1, padx=5, pady=5, sticky="ew")
        # Get orders from the database
        self.load_orders()



    def release_selection(self, event):
    # Seçimi bırak
        self.treeview.selection_remove(self.treeview.selection())

    def load_orders(self):
        # Connect to the database
        conn = sqlite3.connect('library.db')
        c = conn.cursor()

        # Fetch orders from the receipt table
        c.execute("SELECT receipt_number, orderdate, totalcosts FROM receipt")
        orders = c.fetchall()

        # Insert orders into the treeview
        for order in orders:
            self.treeview.insert("", "end", text=order[0], values=(order[0], order[1], order[2]))

        # Close the connection
        conn.close()

 
    def show_order_details(self, event):
    # Get the selected item from the treeview
        selected_items = self.treeview.selection()

        # If any item is selected
        if selected_items:
            # Get the first selected item
            item = selected_items[0]
            receipt_number = self.treeview.item(item, "text")

            # Create a new window to display order details
            order_details_window = customtkinter.CTkToplevel(self)
            order_details_window.title("Order Details")

            # Add labels to display order details
            receipt_label = customtkinter.CTkLabel(order_details_window, text="Order Details for Receipt Number: " + str(receipt_number) )
            receipt_label.grid(row=0, column=0, padx=10, pady=10)

            # Fetch order details from the myorders table
            conn = sqlite3.connect('library.db')
            c = conn.cursor()
            c.execute("SELECT order_id, catalog_number, quantity, total_cost FROM myorders WHERE receipt_number=?", (receipt_number,))
            orders = c.fetchall()

            # Display order details in a listbox
            order_listbox = CTkListbox(order_details_window , width=500)
            order_listbox.grid(row=2, column=0, padx=10, pady=10)

            for order in orders:
                order_listbox.insert("end", f"Order ID: {order[0]}, Catalog Number: {order[1]}, Quantity: {order[2]}, Cost: {order[3]}")

            # Close the connection
            conn.close()
        else:
            # If no item is selected, do nothing or show a message
            pass  # Or you can show a message to the user indicating no item is selected


# Method creates a pdf file
    def create_pdf_file(self):

        selected_items = self.treeview.selection()

        # If any item is selected
        if selected_items:
            # Get the first selected item
            item = selected_items[0]
            receipt_number = self.treeview.item(item, "text")
        

            # Fetch order details from the myorders table
            conn = sqlite3.connect('library.db')
            c = conn.cursor()
        
            c.execute("SELECT receipt_number, name , phone , postalcode, province, city, delivery_adress, orderdate, totalcosts FROM receipt")
            orders = c.fetchall()

            
            # Fatura bilgileri sözlüğü oluştur
            invoice_information = {}
            
            for order in orders:
                receipt_number, name, phone, postalcode, province, city, delivery_address, orderdate, totalcosts = order
                invoice_information[receipt_number] = {
                    "Receipt no": receipt_number,
                    "Name": name,
                    "Phone": phone,
                    "Postalcode": postalcode,
                    "Province": province,
                    "City": city,
                    "Delivery address": delivery_address,
                    "Date of Order": orderdate,
                    "Total Cost": totalcosts
                }

            # Close the connection
            conn.close()

            # Dosya numarasını belirle
            invoice_id = 1
            while True:
                pdf_filename = f"invoice{invoice_id:02d}.pdf"  # Dosya adını oluştur
                if not os.path.exists(pdf_filename):  # Dosya daha önce oluşturulmuş mu kontrol et
                    break
                invoice_id += 1

            doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
            styles = getSampleStyleSheet()

            elements = []
            for key, value in invoice_information.items():
                para = Paragraph(f"<b>{key}:</b> {value}", styles["Normal"])
                elements.append(para)

            doc.build(elements)

            print(f"PDF dosyası oluşturuldu: {pdf_filename}") 
            CTkMessagebox( title="Info", icon="check", option_1="Thanks", message= f"PDF dosyası oluşturuldu: {pdf_filename}") 

        else:
            # If no item is selected, do nothing or show a message
            CTkMessagebox( title= "Warning", message= "Nothing selected. You should select one receipt")   


    # Quit method for program end
    def ask_question(self):
        # get yes/no answers
        msg = CTkMessagebox(title="Exit?", message="Do you want to close the program?",
                            icon="question", option_1="Cancel", option_2="No", option_3="Yes")
        response = msg.get()
        
        if response=="Yes":
            self.destroy()       
        else:
            print("Click 'Yes' to exit!")

    
     # logging out method  
    def ask_logout(self):
        # get yes/no answers
        msg = CTkMessagebox(title="Exit?", message="Do you want to log out?",
                            icon="question", option_1="Cancel", option_2="No", option_3="Yes")
        response = msg.get()
        
        if response=="Yes":
            self.username=""
            self.show_main_page()      
        else:
            print("Click 'Yes' to exit!")

    # Clears the widgets on the screen
    def clear_widgets(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()



app = App()
app.mainloop()