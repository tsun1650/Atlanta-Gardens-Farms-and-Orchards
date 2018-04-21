
#import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import hashlib
from WebService import *

LARGE_FONT= ("Verdana", 12)


class Atlanta(Tk):

    def __init__(self, *args, **kwargs):
        
        Tk.__init__(self, *args, **kwargs)
        container = Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}


        #########################################
        #          Make sure you add            #
        #          your new page here           #
        #########################################
        allPages = (loginPage, visitorRegistration, ownerRegistration, adminFunctions, visitorView, visitHistory, viewVisitorList, 
            viewOwnerList, approvedOrganisms, pendingOrganisms, unconfirmedProperties, confirmedProperties, visitorPropertyPage, propertyDetails, otherOwnerProperties, ownerFunctionality, addNewProperty)

        for F in allPages:
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(loginPage)
        #self.show_frame(ownerFunctionality)
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class loginPage(Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        Frame.__init__(self,parent)
        label = Label(self, text="Login Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        f = Frame(self)
        self.f = f
        f.pack(padx=5, pady=20, side=LEFT)
        
        email = Label(f, text="Email: ")
        email.grid(row=0, column=0, sticky='w')
        email.focus_set()

        self.emailEntry = Entry(f, background='white', width=24)
        self.emailEntry.grid(row=0, column=1, sticky='w')
        self.emailEntry.focus_set()

        password = Label(f, text="Password: ")
        password.grid(row=1, column=0, sticky='w')
        password.focus_set()

        self.passwordEntry = Entry(f, background='white', width=24)
        self.passwordEntry.grid(row=1, column=1, sticky='w')

        button0 = Button(f, text="Login", command=self.login)
        button0.grid(row=2, column=1, sticky='w')
        button1 = Button(f, text="New Owner Registration", command=lambda: controller.show_frame(ownerRegistration))
        button1.grid(row=3, column=0, sticky='w')

        button2 = Button(f, text="New Visitor Registration", command=lambda: controller.show_frame(visitorRegistration))
        button2.grid(row=3, column=1, sticky='w')

    #login onclick event
    def login(self):
        # Initialize hash function
        hashfunc = hashlib.sha256()
        # Add the password string inputted into hash function
        hashfunc.update(str(self.passwordEntry).encode())
        # Get hashed password
        hashPass = hashfunc.digest()

        # Call verifyLogin function from web service
        verify = DBManager.verifyLogin(self, self.emailEntry, hashPass)

        if verify:
            # log in was successful; fetch user type
            userType = DBManager.getUserType(self.emailEntry)

            if userType == "Owner":
                self.controller.show_frame(ownerFunctionality)
            elif userType == "Visitor":
                self.controller.show_frame(visitorView)
            else:
                self.controller.show_frame(adminFunctions)
        else:
            error = Label(self.f, text="Email or password was incorrect")
            error.grid(row=4, column=0)


class visitorRegistration(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="New Visitor Registration", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        
        #email.grid(row = 1, column = 0, padx = 20, pady = 10)
        dialog_frame = Frame(self)
        dialog_frame.pack(padx=5, pady=20, side=LEFT)
        
        email = Label(dialog_frame, text="Email*: ")
        email.grid(row=0, column=0, sticky='w')
        self.email = Entry(dialog_frame, background='white', width=24)
        self.email.grid(row=0, column=1, sticky='w')
        self.email.focus_set()
        
        username = Label(dialog_frame, text="Username:* ")
        username.grid(row=1, column=0, sticky='w')
        self.username = Entry(dialog_frame, background='white', width=24)
        self.username.grid(row=1, column=1, sticky='w')
        self.username.focus_set()

        password = Label(dialog_frame, text="Password:* ")
        password.grid(row=2, column=0, sticky='w')
        self.password = Entry(dialog_frame, background='white', width=24)
        self.password.grid(row=2, column=1, sticky='w')
        self.password.focus_set()

        confirmPassword = Label(dialog_frame, text="Confirm Password:* ")
        confirmPassword.grid(row=3, column=0, sticky='w')
        self.confirmPassword = Entry(dialog_frame, background='white', width=24)
        self.confirmPassword.grid(row=3, column=1, sticky='w')
        self.confirmPassword.focus_set()

        
        button1 = Button(dialog_frame, text="Cancel", command=lambda: controller.show_frame(loginPage))
        button1.grid(row=4, column=0, sticky='w')
        #TODO: REGISTER COMPLETE PAGE
        button2 = Button(dialog_frame, text="Register Visitor", command=self.registervisitor)
        button2.grid(row=4, column=1, sticky='w')

    def registervisitor(self):
        # Initialize hash function
        hashfunc = hashlib.sha256()
        # Add the password string inputted into hash function
        hashfunc.update(str(self.password.get()).encode())
        # Get hashed password
        hashPass = hashfunc.digest()
        print("hashed password: ", hashPass)
        register = DBManager.registerNewUser(self, self.email.get(), self.username.get(), hashPass, 'Visitor')

        if register:
            print("success")
        else:
            print("register didn't work")

class visitorView(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Welcome Visitor", font =LARGE_FONT)
        label.grid(row=0, column=0)

        props = Label(self, text="All public, validated properties:")
        props.grid(row=1, column=0)

        frame = Frame(self)

        table = Treeview(frame)
        table['columns'] = ('address', 'city', 'zip', 'size', 'type', 'public', 'commercial', 'id', 'visits', 'rating')
        table.heading('#0', text='Name', anchor='w')
        table.column('#0', anchor='w')
        table.heading('address', text='Address')
        table.column('address', anchor='center', width = 100)
        table.heading('city', text='City')
        table.column('city', anchor='center', width = 100)
        table.heading('zip', text='Zip')
        table.column('zip', anchor='center', width = 100)
        table.heading('size', text='Size')
        table.column('size', anchor='center', width = 100)
        table.heading('type', text='Type')
        table.column('type', anchor='center', width = 100)
        table.heading('public', text='Public')
        table.column('public', anchor='center', width = 100)
        table.heading('commercial', text='Commercial')
        table.column('commercial', anchor='center', width = 100)
        table.heading('id', text='ID')
        table.column('id', anchor='center', width = 100)
        table.heading('visits', text='Visits')
        table.column('visits', anchor='center', width = 100)
        table.heading('rating', text='Avg Rating')
        table.column('rating', anchor='center', width = 100)
        table.grid(sticky=(N,S,W,E))
        frame.treeview = table
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        frame.grid(sticky=(N,S,W,E))
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        # Loads temp Data
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Cooper Middle School', values=('4605 Ewing Rd', 'Austell', '30106', '1', 'Garden', 'True', 'False', '12000', '2', '5.0'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Cooper Middle School', values=('4605 Ewing Rd', 'Austell', '30106', '1', 'Garden', 'True', 'False', '12000', '2', '5.0'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Cooper Middle School', values=('4605 Ewing Rd', 'Austell', '30106', '1', 'Garden', 'True', 'False', '12000', '2', '5.0'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))


        types = {'Search by...', 'Name', 'City', 'Type', 'Visits','Avg Rating'}
        
        search = StringVar()
        search.set('Search by...')
        search_menu = OptionMenu(frame, search, *types)
        search_menu.grid(row=3, column=0, sticky='w', padx=50, pady=10)

        term = Entry(self, text="Search Term")
        term.grid(row=3, column = 0, sticky='w', padx=50, pady=10)

        searchprop = Button(self, text="Search Properties", command=lambda: controller.show_frame(loginPage))
        searchprop.grid(row=4, column=0, sticky='w', padx=50, pady=10)

        viewprop = Button(self, text="View Property", command=lambda: controller.show_frame(loginPage))
        viewprop.grid(row=3, column=0, padx=50, pady=10)

        viewhist = Button(self, text="View Visit History", command=lambda: controller.show_frame(visitHistory))
        viewhist.grid(row=4, column=0, padx=50, pady=10)

        logout = Button(self, text="Log Out", command=lambda: controller.show_frame(loginPage))
        logout.grid(row=3, column=0, sticky='e', padx=50, pady=10)


class visitHistory(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Your Visit History", font=LARGE_FONT)
        label.grid(row=0, column=0, padx=50, pady=20)

        frame = Frame(self)

        table = Treeview(frame)
        table['columns'] = ('date', 'rating')
        table.heading('#0', text='Name', anchor='w')
        table.column('#0', anchor='w')
        table.heading('date', text='Date Logged')
        table.column('date', anchor='center', width = 100)
        table.heading('rating', text='Rating')
        table.column('rating', anchor='center', width = 100)

        table.grid(sticky=(N,S,W,E))
        frame.treeview = table
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        frame.grid(sticky=(N,S,W,E))
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        # loads temp data
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('2018-01-21', '5'))
        frame.treeview.insert('', 'end', text='Kenari Company Farm', values=('2018-01-15', '3'))
        frame.treeview.insert('', 'end', text='Kenari Company Farm', values=('2018-01-15', '3'))
        frame.treeview.insert('', 'end', text='Kenari Company Farm', values=('2018-01-15', '3'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('2018-01-21', '5'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('2018-01-21', '5'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('2018-01-21', '5'))
        frame.treeview.insert('', 'end', text='Kenari Company Farm', values=('2018-01-15', '3'))
        frame.treeview.insert('', 'end', text='Kenari Company Farm', values=('2018-01-15', '3'))
        frame.treeview.insert('', 'end', text='Kenari Company Farm', values=('2018-01-15', '3'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('2018-01-21', '5'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('2018-01-21', '5'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('2018-01-21', '5'))
        frame.treeview.insert('', 'end', text='Kenari Company Farm', values=('2018-01-15', '3'))
        frame.treeview.insert('', 'end', text='Kenari Company Farm', values=('2018-01-15', '3'))
        frame.treeview.insert('', 'end', text='Kenari Company Farm', values=('2018-01-15', '3'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('2018-01-21', '5'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('2018-01-21', '5'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('2018-01-21', '5'))
        frame.treeview.insert('', 'end', text='Kenari Company Farm', values=('2018-01-15', '3'))
        frame.treeview.insert('', 'end', text='Kenari Company Farm', values=('2018-01-15', '3'))
        frame.treeview.insert('', 'end', text='Kenari Company Farm', values=('2018-01-15', '3'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('2018-01-21', '5'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('2018-01-21', '5'))

        propdetails = Button(self, text="View Property Details", command=lambda: controller.show_frame(loginPage))
        propdetails.grid(row=2, column=0, pady=10)

        back = Button(self, text="Back", command=lambda: controller.show_frame(visitorView))
        back.grid(row=3, column=0, pady=10)

class ownerRegistration(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="New Owner Registration", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        frame = Frame(self)
        frame.pack(padx=5, pady=20, side=LEFT)
        
        email = Label(frame, text="Email:* ")
        email.grid(row=0, column=0, sticky='w')
        self.email = Entry(frame, background='white', width=24)
        self.email.grid(row=0, column=1, sticky='w')
        self.email.focus_set()
        
        username = Label(frame, text="Username:* ")
        username.grid(row=1, column=0, sticky='w')
        self.username = Entry(frame, background='white', width=24)
        self.username.grid(row=1, column=1, sticky='w')
        self.username.focus_set()

        password = Label(frame, text="Password:* ")
        password.grid(row=2, column=0, sticky='w')
        self.password = Entry(frame, background='white', width=24)
        self.password.grid(row=2, column=1, sticky='w')
        self.password.focus_set()

        confirmPassword = Label(frame, text="Confirm Password:* ")
        confirmPassword.grid(row=3, column=0, sticky='w')
        self.confirmPassword = Entry(frame, background='white', width=24)
        self.confirmPassword.grid(row=3, column=1, sticky='w')
        self.confirmPassword.focus_set()

        propName = Label(frame, text="Property Name:* ")
        propName.grid(row=4, column=0, sticky='w')
        self.propName = Entry(frame, background='white', width=24)
        self.propName.grid(row=4, column=1, sticky='w')
        self.propName.focus_set()
        
        propAddress = Label(frame, text="Street Address:* ")
        propAddress.grid(row=5, column=0, sticky='w')
        self.propAddress = Entry(frame, background='white', width=24)
        self.propAddress.grid(row=5, column=1, sticky='w')
        self.propAddress.focus_set()
       
        propCity = Label(frame, text="City:* ")
        propCity.grid(row=6, column=0, sticky='w')
        self.propCity = Entry(frame, background='white', width=24)
        self.propCity.grid(row=6, column=1, sticky='w')
        self.propCity.focus_set()

        propZip = Label(frame, text="Zip:* ")
        propZip.grid(row=7, column=0, sticky='w')
        self.propZip = Entry(frame, background='white', width=24)
        self.propZip.grid(row=7, column=1, sticky='w')
        self.propZip.focus_set()
        
        propAcres = Label(frame, text="Acres:* ")
        propAcres.grid(row=8, column=0, sticky='w')
        self.propAcres = Entry(frame, background='white', width=24)
        self.propAcres.grid(row=8, column=1, sticky='w')
        self.propAcres.focus_set()

        propType = Label(frame, text="Property Type:* ")
        propType.grid(row=9, column=0, sticky='w')
        # Rest of GUI depends on property type selected
        types = {'Garden', 'Farm', 'Orchard'}   # Dictionary holding different prop types
        
        propTypeVar = StringVar()
        propTypeVar.set('Garden')   # Set garden as the default prop type
        propType_menu = OptionMenu(frame, propTypeVar, *types)
        propType_menu.grid(row=9, column=1, padx=20, pady=10)

        if propTypeVar.get() == 'Garden':
            # Garden GUI
            # TODO: create a dictionary with approved vegetables and flowers (from DB)
            crop = Label(frame, text="Crop:* ")
            crop.grid(row=10, column=0, padx=20, pady=10)

            # TODO: replace entry box with drop down populated by crop dictionary
            cropTxt = StringVar()
            entry10 = Entry(frame, textvariable=cropTxt)
            entry10.grid(row=10, column=1, padx=20, pady=10)
        elif propTypeVar.get() == 'Farm':
            # Farm GUI
            # TODO: create a dictionary with approved fruits, nuts, vegetables, and flowers (from DB)
            crop = Label(frame, text="Crop:* ")
            crop.grid(row=10, column=0, padx=20, pady=10)

            # TODO: replace entry box with drop down populated by crop dictionary
            cropTxt = StringVar()
            entry10 = Entry(frame, textvariable=cropTxt)
            entry10.grid(row=10, column=1, padx=20, pady=10)

            # TODO: Do same thing with animals as crops ^
            animal = Label(frame, text="Animal:* ")
            animal.grid(row=11, column=0, padx=20, pady=10)
            animalTxt = StringVar()
            entry11 = Entry(frame, textvariable=animalTxt)
            entry11.grid(row=11, column=1, padx=20, pady=10)
        else:
            # Orchard GUI
            # TODO: create a dictionary with approved fruits and nuts (from DB)
            crop = Label(frame, text="Crop:* ")
            crop.grid(row=10, column=0, padx=20, pady=10)

            # TODO: replace entry box with drop down populated by crop dictionary
            cropTxt = StringVar()
            entry10 = Entry(frame, textvariable=cropTxt)
            entry10.grid(row=10, column=1, padx=20, pady=10)

        # Buttons
        button1 = Button(frame, text="Cancel", command=lambda: controller.show_frame(loginPage))
        button1.grid(row=11, column=0, sticky='w')
        #TODO: REGISTER COMPLETE PAGE
        button2 = Button(frame, text="Register Owner", command=self.registerowner)
        button2.grid(row=11, column=1, sticky='w')

    def registerowner(self):
        print("gwsegnoisegnoiseg")

class adminFunctions(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Admin Functionality", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        visListB = Button(self, text="View Visitor List", command=lambda: controller.show_frame(viewVisitorList))
        visListB.pack(fill = X)

        ownListB = Button(self, text="View Owner List", command=lambda: controller.show_frame(viewOwnerList))
        ownListB.pack(fill = X)

        conPropB = Button(self, text="View Confirmed Properties", command=lambda: controller.show_frame(confirmedProperties))       
        conPropB.pack(fill = X)

        unconPropB = Button(self, text="View Unconfirmed Properties", command=lambda: controller.show_frame(unconfirmedProperties))
        unconPropB.pack(fill =X)

        approvedB = Button(self, text="View Approved Animals and Crops", command=lambda: controller.show_frame(approvedOrganisms))
        approvedB.pack(fill = X)

        pendingB = Button(self, text="View Pending Animals and Crops", command=lambda: controller.show_frame(pendingOrganisms))
        pendingB.pack(fill =X)

        logoutB = Button(self, text="Logout", command=lambda: controller.show_frame(loginPage))
        logoutB.pack(fill =X)

class viewVisitorList(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="All Visitors in System", font =LARGE_FONT)
        label.grid(row=0, column=0)

        frame = Frame(self)


        table = Treeview(frame)
        table['columns'] = ('Email', 'Logged Visits')
        table.heading('#0', text='Username', anchor='w')
        table.column('#0', anchor='w')
        
        table.heading('Email', text='Email')
        table.column('Email', anchor='center', width = 100)
        table.heading('Logged Visits', text='Logged Visits')
        table.column('Logged Visits', anchor='center', width = 100)
       
        table.grid(sticky=(N,S,W,E))
        frame.treeview = table
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        frame.grid(sticky=(N,S,W,E))
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        # Loads temp Data
        frame.treeview.insert('', 'end', text='tsun1', values=('ee@email.com','2'))
        frame.treeview.insert('', 'end', text='tsun1', values=('ee@email.com','2'))
        frame.treeview.insert('', 'end', text='tsun1', values=('ee@email.com','2'))

        types = { 'Username', 'Email', 'Logged Visits'}
        
        search = StringVar()
        search.set('Search by...')
        search_menu = OptionMenu(frame, search, *types)
        search_menu.grid(row=3, column=0, sticky='w', padx=50, pady=10)

        term = Entry(self, text="Search Term")
        term.grid(row=3, column = 0, sticky='w', padx=50, pady=10)

        searchprop = Button(self, text="Search Visitors", command=lambda: controller.show_frame(adminFunctions))
        searchprop.grid(row=4, column=0, sticky='w', padx=50, pady=10)

        deletevisitor = Button(self, text="Delete Visitor Account", command=lambda: controller.show_frame(adminFunctions))
        deletevisitor.grid(row=3, column=0, padx=50, pady=10)

        deletelog = Button(self, text="Delete Log History", command=lambda: controller.show_frame(adminFunctions))
        deletelog.grid(row=4, column=0, padx=50, pady=10)

        back = Button(self, text="Back", command=lambda: controller.show_frame(adminFunctions))
        back.grid(row=3, column=0, sticky='e', padx=50, pady=10)

class viewOwnerList(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="All Owners in System", font =LARGE_FONT)
        label.grid(row=0, column=0)

        frame = Frame(self)


        table = Treeview(frame)
        table['columns'] = ('Email', 'Number of Properties')
        table.heading('#0', text='Username', anchor='w')
        table.column('#0', anchor='w')
        
        table.heading('Email', text='Email')
        table.column('Email', anchor='center', width = 100)
        table.heading('Number of Properties', text='Number of Properties')
        table.column('Number of Properties', anchor='center', width = 120)
       
        table.grid(sticky=(N,S,W,E))
        frame.treeview = table
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        frame.grid(sticky=(N,S,W,E))
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        # Loads temp Data
        frame.treeview.insert('', 'end', text='tsun1', values=('ee@email.com','2'))
        frame.treeview.insert('', 'end', text='tsun1', values=('ee@email.com','2'))
        frame.treeview.insert('', 'end', text='tsun1', values=('ee@email.com','2'))

        types = { 'Username', 'Email', 'Number of Properties'}
        
        search = StringVar()
        search.set('Search by...')
        search_menu = OptionMenu(frame, search, *types)
        search_menu.grid(row=3, column=0, sticky='w', padx=50, pady=10)

        term = Entry(self, text="Search Term")
        term.grid(row=3, column = 0, sticky='w', padx=50, pady=10)

        searchowners = Button(self, text="Search Owners", command=lambda: controller.show_frame(adminFunctions))
        searchowners.grid(row=4, column=0, sticky='w', padx=50, pady=10)

        deletevisitor = Button(self, text="Delete Owner Account", command=lambda: controller.show_frame(adminFunctions))
        deletevisitor.grid(row=3, column=0, padx=50, pady=10)

        deletelog = Button(self, text="Delete Owner Account", command=lambda: controller.show_frame(adminFunctions))
        deletelog.grid(row=4, column=0, padx=50, pady=10)

        back = Button(self, text="Back", command=lambda: controller.show_frame(adminFunctions))
        back.grid(row=3, column=0, sticky='e', padx=50, pady=10)

class approvedOrganisms(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Approved Owners/Crops", font =LARGE_FONT)
        label.grid(row=0, column=0)

        frame = Frame(self)

        table = Treeview(frame)
        table['columns'] = ('Type')
        table.heading('#0', text='Name', anchor='w')
        table.column('#0', anchor='w')
        
        table.heading('Type', text='Type')
        table.column('Type', anchor='center', width = 100)
        
        table.grid(sticky=(N,S,W,E))
        frame.treeview = table
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        frame.grid(sticky=(N,S,W,E))
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        # Loads temp Data
        frame.treeview.insert('', 'end', text='Apple', values=('Fruit'))
        frame.treeview.insert('', 'end', text='Antelope', values=('Animal'))
        frame.treeview.insert('', 'end', text='Broccoli', values=('Vegetable'))

        types = {'Fruit', 'Animal', 'Vegetable'}
        
        search = StringVar()
        search.set('Enter name')
        search_menu = OptionMenu(frame, search, *types)
        search_menu.grid(row=3, column=0, sticky='w', padx=50, pady=10)

        nameterm = Entry(self, text="Enter Name")
        nameterm.grid(row=3, column = 0, sticky='w', padx=50, pady=10)

        addB = Button(self, text="Add to Approval List", command=lambda: controller.show_frame(adminFunctions))
        addB.grid(row=4, column=0, sticky='w', padx=50, pady=10)

        searchterm = Entry(self, text="Search Term")
        searchterm.grid(row=3, column = 1, sticky='w', padx=50, pady=10)

        searchB = Button(self, text="Search", command=lambda: controller.show_frame(adminFunctions))
        searchB.grid(row=4, column=1, sticky='w', padx=50, pady=10)


        deleteselection = Button(self, text="Delete Selection", command=lambda: controller.show_frame(adminFunctions))
        deleteselection.grid(row=5, column=0, padx=50, pady=10)


        back = Button(self, text="Back", command=lambda: controller.show_frame(adminFunctions))
        back.grid(row=5, column=1, sticky='e', padx=50, pady=10)

class pendingOrganisms(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Pending Owners/Crops", font =LARGE_FONT)
        label.grid(row=0, column=0)

        frame = Frame(self)
        table = Treeview(frame)
        table['columns'] = ('Type')
        table.heading('#0', text='Name', anchor='w')
        table.column('#0', anchor='w')
        
        table.heading('Type', text='Type')
        table.column('Type', anchor='center', width = 100)
        
        table.grid(sticky=(N,S,W,E))
        frame.treeview = table
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        frame.grid(sticky=(N,S,W,E))
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        # Loads temp Data
        frame.treeview.insert('', 'end', text='Apple', values=('Fruit'))
        frame.treeview.insert('', 'end', text='Antelope', values=('Animal'))
        frame.treeview.insert('', 'end', text='Broccoli', values=('Vegetable'))

        types = {'Fruit', 'Animal', 'Vegetable'}
        
        approveB = Button(self, text="Approve Selection", command=lambda: controller.show_frame(adminFunctions))
        approveB.grid(row=4, column=0, sticky='w')

        deleteselection = Button(self, text="Delete Selection", command=lambda: controller.show_frame(adminFunctions))
        deleteselection.grid(row=5, column=0)

        back = Button(self, text="Back", command=lambda: controller.show_frame(adminFunctions))
        back.grid(row=6, column=0, sticky='e')


class confirmedProperties(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Confirmed Properties:", font =LARGE_FONT)
        label.grid(row=0, column=0)

        frame = Frame(self)

        table = Treeview(frame)
        table['columns'] = ('address', 'city', 'zip', 'size', 'type', 'public', 'commercial', 'id', 'verified', 'rating')
        table.heading('#0', text='Name', anchor='w')
        table.column('#0', anchor='w')
        table.heading('address', text='Address')
        table.column('address', anchor='center', width = 100)
        table.heading('city', text='City')
        table.column('city', anchor='center', width = 100)
        table.heading('zip', text='Zip')
        table.column('zip', anchor='center', width = 100)
        table.heading('size', text='Size')
        table.column('size', anchor='center', width = 100)
        table.heading('type', text='Type')
        table.column('type', anchor='center', width = 100)
        table.heading('public', text='Public')
        table.column('public', anchor='center', width = 100)
        table.heading('commercial', text='Commercial')
        table.column('commercial', anchor='center', width = 100)
        table.heading('id', text='ID')
        table.column('id', anchor='center', width = 100)
        table.heading('verified', text='Verified By')
        table.column('verified', anchor='center', width = 100)
        table.heading('rating', text='Avg Rating')
        table.column('rating', anchor='center', width = 100)
        table.grid(sticky=(N,S,W,E))
        frame.treeview = table
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        frame.grid(sticky=(N,S,W,E))
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', 'admin1', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', 'admin2', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', 'admin1', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', 'admin1', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', 'admin1', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', 'admin1', '3.6'))
        frame.treeview.insert('', 'end', text='Cooper Middle School', values=('4605 Ewing Rd', 'Austell', '30106', '1', 'Garden', 'True', 'False', '12000', 'admin2', '5.0'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', 'admin2', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', 'admin1', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', 'admin2', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', 'admin1', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', 'admin1', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', 'admin1', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', 'admin1', '3.6'))
        frame.treeview.insert('', 'end', text='Cooper Middle School', values=('4605 Ewing Rd', 'Austell', '30106', '1', 'Garden', 'True', 'False', '12000', 'admin2', '5.0'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', 'admin2', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', 'admin2', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', 'admin1', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', 'admin2', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', 'admin1', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', 'admin2', '3.6'))
        frame.treeview.insert('', 'end', text='Cooper Middle School', values=('4605 Ewing Rd', 'Austell', '30106', '1', 'Garden', 'True', 'False', '12000', 'admin2', '5.0'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', 'admin1', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', 'admin2', '3.6'))

        types = {'Search by...', 'Name', 'Zip', 'Type', 'Verified By','Avg Rating'}
        
        search = StringVar()
        search.set('Search by...')
        search_menu = OptionMenu(frame, search, *types)
        search_menu.grid(row=3, column=0, sticky='w', padx=50, pady=10)

        term = Entry(self, text="Search Term")
        term.grid(row=3, column = 0, sticky='w', padx=50, pady=10)

        searchprop = Button(self, text="Search Properties", command=lambda: controller.show_frame(loginPage))
        searchprop.grid(row=4, column=0, sticky='w', padx=50, pady=10)

        mprop = Button(self, text="Manage Selected Property", command=lambda: controller.show_frame(loginPage))
        mprop.grid(row=3, column=0, padx=50, pady=10)

        back = Button(self, text="Back", command=lambda: controller.show_frame(adminFunctions))
        back.grid(row=3, column=0, sticky='e', padx=50, pady=10)
#### TO DO
class unconfirmedProperties(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Unconfirmed Properties:", font =LARGE_FONT)
        label.grid(row=0, column=0)

        frame = Frame(self)

        table = Treeview(frame)
        table['columns'] = ('address', 'city', 'zip', 'size', 'type', 'public', 'commercial', 'id', 'owner')
        table.heading('#0', text='Name', anchor='w')
        table.column('#0', anchor='w')
        table.heading('address', text='Address')
        table.column('address', anchor='center', width = 100)
        table.heading('city', text='City')
        table.column('city', anchor='center', width = 100)
        table.heading('zip', text='Zip')
        table.column('zip', anchor='center', width = 100)
        table.heading('size', text='Size')
        table.column('size', anchor='center', width = 100)
        table.heading('type', text='Type')
        table.column('type', anchor='center', width = 100)
        table.heading('public', text='Public')
        table.column('public', anchor='center', width = 100)
        table.heading('commercial', text='Commercial')
        table.column('commercial', anchor='center', width = 100)
        table.heading('id', text='ID')
        table.column('id', anchor='center', width = 100)
        table.heading('owner', text='Owner')
        table.column('owner', anchor='center', width = 100)

        table.grid(sticky=(N,S,W,E))
        frame.treeview = table
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        frame.grid(sticky=(N,S,W,E))
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', 'owner1'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', 'owner1'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', 'owner1'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', 'owner1'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', 'owner1'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', 'owner1'))
        frame.treeview.insert('', 'end', text='Cooper Middle School', values=('4605 Ewing Rd', 'Austell', '30106', '1', 'Garden', 'True', 'False', '12000', 'owner2'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', 'owner2'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', 'owner1'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', 'owner2'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', 'owner1'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', 'owner1'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', 'owner1'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', 'owner2'))
        frame.treeview.insert('', 'end', text='Cooper Middle School', values=('4605 Ewing Rd', 'Austell', '30106', '1', 'Garden', 'True', 'False', '12000', 'owner2'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', 'owner2'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', 'owner2'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', 'owner1'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', 'owner2'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', 'owner1'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', 'owner1'))
        frame.treeview.insert('', 'end', text='Cooper Middle School', values=('4605 Ewing Rd', 'Austell', '30106', '1', 'Garden', 'True', 'False', '12000', 'owner2'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', 'owner1'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', 'owner1'))

        types = {'Search by...', 'Name', 'Size', 'Owner'}
        
        search = StringVar()
        search.set('Search by...')
        search_menu = OptionMenu(frame, search, *types)
        search_menu.grid(row=3, column=0, sticky='w', padx=50, pady=10)

        term = Entry(self, text="Search Term")
        term.grid(row=3, column = 0, sticky='w', padx=50, pady=10)

        searchprop = Button(self, text="Search Properties", command=lambda: controller.show_frame(loginPage))
        searchprop.grid(row=4, column=0, sticky='w', padx=50, pady=10)

        mprop = Button(self, text="Manage Selected Property", command=lambda: controller.show_frame(loginPage))
        mprop.grid(row=3, column=0, padx=50, pady=10)

        back = Button(self, text="Back", command=lambda: controller.show_frame(adminFunctions))
        back.grid(row=3, column=0, sticky='e', padx=50, pady=10)

class addNewProperty(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Add New Property:", font =LARGE_FONT)
        label.pack(pady=10,padx=10)

        frame = Frame(self)
        frame.pack(padx=5, pady=20, side=LEFT)
        
        name = Label(frame, text="Property Name:* ")
        name.grid(row=0, column=0, sticky='w')
        self.name = Entry(frame, background='white', width=24)
        self.name.grid(row=0, column=1, sticky='w')
        self.name.focus_set()
        
        street = Label(frame, text="Street Address:* ")
        street.grid(row=1, column=0, sticky='w')
        self.street = Entry(frame, background='white', width=24)
        self.street.grid(row=1, column=1, sticky='w')
        self.street.focus_set()

        city = Label(frame, text="City:* ")
        city.grid(row=2, column=0, sticky='w')
        self.city = Entry(frame, background='white', width=24)
        self.city.grid(row=2, column=1, sticky='w')
        self.city.focus_set()

        zipcode = Label(frame, text="Zip:* ")
        zipcode.grid(row=2, column=2, sticky='w')
        self.zipcode = Entry(frame, background='white', width=24)
        self.zipcode.grid(row=2, column=3, sticky='w')
        self.zipcode.focus_set()

        acres = Label(frame, text="Acres:* ")
        acres.grid(row=2, column=4, sticky='w')
        self.acres = Entry(frame, background='white', width=24)
        self.acres.grid(row=2, column=5, sticky='w')
        self.acres.focus_set()

        propType = Label(frame, text="Property Type:* ")
        propType.grid(row=3, column=0, sticky='w')
        # Rest of GUI depends on property type selected
        proptypes = {'Garden', 'Farm', 'Orchard'}   # Dictionary holding different prop types
        
        propTypeVar = StringVar()
        propTypeVar.set('Garden')   # Set garden as the default prop type
        propType_menu = OptionMenu(frame, propTypeVar, *proptypes)
        propType_menu.grid(row=3, column=1, padx=5, pady=10)

        animalType = Label(frame, text="Animal Type:* ")
        animalType.grid(row=3, column=2, sticky='w')
        # Rest of GUI depends on property type selected
        animaltypes = {'Garden', 'Farm', 'Orchard'}   # Dictionary holding different prop types
        
        animalTypeVar = StringVar()
        animalTypeVar.set('Garden')   # Set garden as the default prop type
        animalType_menu = OptionMenu(frame, animalTypeVar, *animaltypes)
        animalType_menu.grid(row=3, column=4, padx=5, pady=10)

        cropType = Label(frame, text="Crop Type:* ")
        cropType.grid(row=3, column=5, sticky='w')
        # Rest of GUI depends on property type selected
        croptypes = {'Garden', 'Farm', 'Orchard'}   # Dictionary holding different prop types
        
        cropTypeVar = StringVar()
        cropTypeVar.set('Garden')   # Set garden as the default prop type
        cropTypeVar_menu = OptionMenu(frame, cropTypeVar, *croptypes)
        cropTypeVar_menu.grid(row=3, column=6, padx=5, pady=10)

        pubType = Label(frame, text="Public?:* ")
        pubType.grid(row=4, column=0, sticky='w')
        # Rest of GUI depends on property type selected
        pubtypes = {'Yes', 'No'}   # Dictionary holding different prop types
        
        pubTypeVar = StringVar()
        pubTypeVar.set('No')   # Set garden as the default prop type
        pubTypeVar_menu = OptionMenu(frame, pubTypeVar, *pubtypes)
        pubTypeVar_menu.grid(row=4, column=1, padx=5, pady=10)

        comType = Label(frame, text="Commercial?:* ")
        comType.grid(row=5, column=0, sticky='w')
        # Rest of GUI depends on property type selected
        comtypes = {'Yes', 'No'}   # Dictionary holding different prop types
        
        comTypeVar = StringVar()
        comTypeVar.set('No')   # Set garden as the default prop type
        comTypeVar_menu = OptionMenu(frame, comTypeVar, *comtypes)
        comTypeVar_menu.grid(row=5, column=1, padx=5, pady=10)

        # Buttons
        button1 = Button(frame, text="Add Property", command=lambda: controller.show_frame(loginPage))
        button1.grid(row=6, column=0, sticky='w')
        #TODO: REGISTER COMPLETE PAGE
        button2 = Button(frame, text="Cancel", command=lambda: controller.show_frame(loginPage))
        button2.grid(row=6, column=1, sticky='w')



class visitorPropertyPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        name = Label(self, text="Name: ")
        name.pack()
        owner = Label(self, text="Owner: ")
        owner.pack()
        ownerEmail = Label(self, text="Owner Email: ")
        ownerEmail.pack()
        visits = Label(self, text="Visits: ")
        visits.pack()
        address = Label(self, text="Address: ")
        address.pack()
        city = Label(self,text='City: ')
        city.pack()
        zipcode = Label(self, text="Zip : ")
        zipcode.pack()
        size = Label(self, text="Size (acres): ")
        size.pack()
        rating = Label(self, text="Avg Rating: ")
        rating.pack()
        typeProp = Label(self, text="Type: ")
        typeProp.pack()
        public = Label(self, text="Public: ")
        public.pack()
        commercial = Label(self, text="Commercial: ")
        commercial.pack()
        idnum = Label(self, text="ID: ")
        idnum.pack()

        crops = Label(self, text="Crops: ")
        crops.pack()

        types = {'1', '2', '3', '4', '5'}
        search = StringVar()
        rating = OptionMenu(self, search, *types)
        rating.pack()

        logvisit = Button(self, text="Log Visit", command=lambda: messagebox.showinfo("Title", "Visit Logged!"))
        
        logvisit.pack()
        back = Button(self, text="Back", command=lambda: controller.show_frame(visitorView))
        back.pack()
        

class propertyDetails(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        name = Label(self, text="Name: ")
        name.pack()
        owner = Label(self, text="Owner: ")
        owner.pack()
        ownerEmail = Label(self, text="Owner Email: ")
        ownerEmail.pack()
        visits = Label(self, text="Visits: ")
        visits.pack()
        address = Label(self, text="Address: ")
        address.pack()
        city = Label(self, text="City: ")
        city.pack()
        zipcode = Label(self, text="Zip : ")
        zipcode.pack()
        size = Label(self, text="Size (acres): ")
        size.pack()
        rating = Label(self, text="Avg Rating: ")
        rating.pack()
        typeProp = Label(self, text="Type: ")
        typeProp.pack()
        public = Label(self, text="Public: ")
        public.pack()
        commercial = Label(self, text="Commercial: ")
        commercial.pack()
        idnum = Label(self, text="ID: ")
        idnum.pack()

        crops = Label(self, text="Crops: ")
        crops.pack()
        back = Button(self, text="Back", command=lambda: controller.show_frame(visitorView))
        back.pack()

class otherOwnerProperties(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="All Other Valid Properties", font =LARGE_FONT)
        label.grid(row=0, column=0)


        frame = Frame(self)

        table = Treeview(frame)
        table['columns'] = ('address', 'city', 'zip', 'size', 'type', 'public', 'commercial', 'id', 'visits', 'rating')
        table.heading('#0', text='Name', anchor='w')
        table.column('#0', anchor='w')
        table.heading('address', text='Address')
        table.column('address', anchor='center', width = 100)
        table.heading('city', text='City')
        table.column('city', anchor='center', width = 100)
        table.heading('zip', text='Zip')
        table.column('zip', anchor='center', width = 100)
        table.heading('size', text='Size')
        table.column('size', anchor='center', width = 100)
        table.heading('type', text='Type')
        table.column('type', anchor='center', width = 100)
        table.heading('public', text='Public')
        table.column('public', anchor='center', width = 100)
        table.heading('commercial', text='Commercial')
        table.column('commercial', anchor='center', width = 100)
        table.heading('id', text='ID')
        table.column('id', anchor='center', width = 100)
        table.heading('visits', text='Visits')
        table.column('visits', anchor='center', width = 100)
        table.heading('rating', text='Avg Rating')
        table.column('rating', anchor='center', width = 100)
        table.grid(sticky=(N,S,W,E))
        frame.treeview = table
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        frame.grid(sticky=(N,S,W,E))
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        # Loads temp Data
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Cooper Middle School', values=('4605 Ewing Rd', 'Austell', '30106', '1', 'Garden', 'True', 'False', '12000', '2', '5.0'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Cooper Middle School', values=('4605 Ewing Rd', 'Austell', '30106', '1', 'Garden', 'True', 'False', '12000', '2', '5.0'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Cooper Middle School', values=('4605 Ewing Rd', 'Austell', '30106', '1', 'Garden', 'True', 'False', '12000', '2', '5.0'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))


        types = {'Search by...', 'Name', 'City', 'Type', 'Visits','Avg Rating'}
        
        search = StringVar()
        search.set('Search by...')
        search_menu = OptionMenu(frame, search, *types)
        search_menu.grid(row=3, column=0, sticky='w', padx=50, pady=10)

        term = Entry(self, text="Search Term")
        term.grid(row=3, column = 0, sticky='w', padx=50, pady=10)

        searchprop = Button(self, text="Search Properties", command=lambda: controller.show_frame(loginPage))
        searchprop.grid(row=4, column=0, sticky='w', padx=50, pady=10)

        viewprop = Button(self, text="View Property Details", command=lambda: controller.show_frame(propertyDetails))
        viewprop.grid(row=3, column=0, padx=50, pady=10)
        ## TO DO: BACK MUST GO TO THE RIGHT PAGE
        back = Button(self, text="Back", command=lambda: controller.show_frame(loginPage))
        back.grid(row=4, column=0, sticky='e', padx=50, pady=10)


class ownerFunctionality(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Welcome Owner", font =LARGE_FONT)
        label.grid(row=0, column=0)

        props = Label(self, text="Your properties:")
        props.grid(row=1, column=0)

        frame = Frame(self)

        table = Treeview(frame)
        table['columns'] = ('address', 'city', 'zip', 'size', 'type', 'public', 'commercial', 'id', 'visits', 'rating', 'isValid')
        table.heading('#0', text='Name', anchor='w')
        table.column('#0', anchor='w')
        table.heading('address', text='Address')
        table.column('address', anchor='center', width = 100)
        table.heading('city', text='City')
        table.column('city', anchor='center', width = 100)
        table.heading('zip', text='Zip')
        table.column('zip', anchor='center', width = 100)
        table.heading('size', text='Size')
        table.column('size', anchor='center', width = 100)
        table.heading('type', text='Type')
        table.column('type', anchor='center', width = 100)
        table.heading('public', text='Public')
        table.column('public', anchor='center', width = 100)
        table.heading('commercial', text='Commercial')
        table.column('commercial', anchor='center', width = 100)
        table.heading('id', text='ID')
        table.column('id', anchor='center', width = 100)
        table.heading('isValid', text='isValid')
        table.column('isValid', anchor='center', width = 100)
        table.heading('visits', text='Visits')
        table.column('visits', anchor='center', width = 100)
        table.heading('rating', text='Avg Rating')
        table.column('rating', anchor='center', width = 100)

        table.grid(sticky=(N,S,W,E))
        frame.treeview = table
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        frame.grid(sticky=(N,S,W,E))
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        # Loads temp Data
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Cooper Middle School', values=('4605 Ewing Rd', 'Austell', '30106', '1', 'Garden', 'True', 'False', '12000', '2', '5.0'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Cooper Middle School', values=('4605 Ewing Rd', 'Austell', '30106', '1', 'Garden', 'True', 'False', '12000', '2', '5.0'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Cooper Middle School', values=('4605 Ewing Rd', 'Austell', '30106', '1', 'Garden', 'True', 'False', '12000', '2', '5.0'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))
        frame.treeview.insert('', 'end', text='Georgia Tech Garden', values=('Spring Street SW', 'Atlanta', '30308', '0.5', 'Garden', 'True', 'False', '00320', '20', '3.6'))


        types = {'Search by...', 'Name', 'City', 'Type', 'Visits','Avg Rating'}
        
        search = StringVar()
        search.set('Search by...')
        search_menu = OptionMenu(frame, search, *types)
        search_menu.grid(row=3, column=0, sticky='w', padx=50, pady=10)

        term = Entry(self, text="Search Term")
        term.grid(row=3, column = 0, sticky='w', padx=50, pady=10)

        searchprop = Button(self, text="Search Properties", command=lambda: controller.show_frame(loginPage))
        searchprop.grid(row=4, column=0, sticky='w', padx=50, pady=10)

        manage = Button(self, text="Manage Property", command=lambda: controller.show_frame(loginPage))
        manage.grid(row=3, column=0, padx=50, pady=10)

        addP = Button(self, text="Add Property", command=lambda: controller.show_frame(loginPage))
        addP.grid(row=4, column=0, padx=50, pady=10)

        logout = Button(self, text="Log Out", command=lambda: controller.show_frame(loginPage))
        logout.grid(row=4, column=0, sticky='e', padx=50, pady=10)

        viewOthers = Button(self, text="View Other Properties", command=lambda: controller.show_frame(otherOwnerProperties))
        viewOthers.grid(row=3, column=0, sticky='e', padx=50, pady=10)

class propertyManagement(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Manage", font =LARGE_FONT)
        label.pack(pady=10,padx=10)

        frame = Frame(self)
        frame.pack(padx=5, pady=20, side=LEFT)
        self.frame = frame

        name = Label(frame, text="Name: ")
        name.grid(row=0, column=0, sticky='w')
        self.name = Entry(frame, background='white', width=24)
        self.name.grid(row=0, column=1, sticky='w')
        self.name.focus_set()

        typ = Label(frame, text="Type: ")
        typ.grid(row=0, column=2, sticky='w')
        
        street = Label(frame, text="Address: ")
        street.grid(row=1, column=0, sticky='w')
        self.street = Entry(frame, background='white', width=24)
        self.street.grid(row=1, column=1, sticky='w')
        self.street.focus_set()

        pub = Label(frame, text="Public: ")
        pub.grid(row=1, column=2, sticky='w')

        # Rest of GUI depends on property type selected
        pubtypes = {'True', 'False'}   # Dictionary holding different prop types
        
        pubTypeVar = StringVar()
        pubTypeVar.set('False')   # Set garden as the default prop type
        pubType_menu = OptionMenu(frame, pubTypeVar, *pubtypes)
        pubType_menu.grid(row=1, column=3, padx=5, pady=10)

        city = Label(frame, text="City: ")
        city.grid(row=2, column=0, sticky='w')
        self.city = Entry(frame, background='white', width=24)
        self.city.grid(row=2, column=1, sticky='w')
        self.city.focus_set()

        com = Label(frame, text="Commercial: ")
        com.grid(row=2, column=2, sticky='w')

        comtypes = {'True', 'False'}   # Dictionary holding different prop types
        
        comTypeVar = StringVar()
        comTypeVar.set('False')   # Set garden as the default prop type
        comType_menu = OptionMenu(frame, comTypeVar, *comtypes)
        comType_menu.grid(row=1, column=3, padx=5, pady=10)

        zipcode = Label(frame, text="Zip: ")
        zipcode.grid(row=3, column=0, sticky='w')
        self.zipcode = Entry(frame, background='white', width=24)
        self.zipcode.grid(row=3, column=1, sticky='w')
        self.zipcode.focus_set()

        ID = Label(frame, text="ID: ")
        ID.grid(row=3, column=2, sticky='w')

        acres = Label(frame, text="Size(Acres): ")
        acres.grid(row=4, column=0, sticky='w')
        self.acres = Entry(frame, background='white', width=24)
        self.acres.grid(row=4, column=1, sticky='w')
        self.acres.focus_set()

        cropType = Label(frame, text="Add new crop: ")
        cropType.grid(row=5, column=0, sticky='w')
        # Rest of GUI depends on property type selected
        croptypes = {'Fruit', 'Nut', 'Flower', 'Vegetable'}   # Dictionary holding different prop types
        
        self.cropTypeVar = StringVar()
        self.cropTypeVar.set('Fruit')   # Set garden as the default prop type

        cropType_menu = OptionMenu(frame, self.cropTypeVar, *croptypes)
        cropType_menu.grid(row=5, column=1, padx=5, pady=10)

        crops = Label(frame, text="Crops: ")
        crops.grid(row=5, column=3, sticky='w')
        global buttonnum
        buttonnum = 0
    

        button1 = Button(frame, text="Add crop to property", command=self.addCrop)
        button1.grid(row=6, column=1, sticky='w')

        crop = Label(frame, text="Request crop approval: ")
        crop.grid(row=7, column=0, sticky='w')
        self.crop = Entry(frame, background='white', width=24)
        self.crop.grid(row=7, column=1, sticky='w')
        self.crop.focus_set()

        newcropType = Label(frame, text="New crop type: ")
        newcropType.grid(row=7, column=2, sticky='w')
        # Rest of GUI depends on property type selected
        newcroptypes = {'Fruit', 'Nut', 'Flower', 'Vegetable'}   # Dictionary holding different prop types
        
        newcropTypeVar = StringVar()
        newcropTypeVar.set('Fruit')   # Set garden as the default prop type
        newcropType_menu = OptionMenu(frame, newcropTypeVar, *newcroptypes)
        newcropType_menu.grid(row=7, column=3, padx=5, pady=10)

        button2 = Button(frame, text="Submit Request", command=lambda: controller.show_frame(loginPage))
        button2.grid(row=8, column=1, sticky='w')

        button3 = Button(frame, text="Save Changes", command=lambda: controller.show_frame(loginPage))
        button3.grid(row=9, column=1, sticky='w')

        button4 = Button(frame, text="Delete Property", command=lambda: controller.show_frame(loginPage))
        button4.grid(row=10, column=0, sticky='w')

        button5 = Button(frame, text="Back (Don't Save)", command=lambda: controller.show_frame(loginPage))
        button5.grid(row=10, column=1, sticky='w')

    def addCrop(self):
        global buttonnum
        buttonnum += 1
        butts = []
        label = "Button " + str(buttonnum)
        for i in range(buttonnum):
            butts.append(Button(self.frame, text=str(self.cropTypeVar.get()) + ' [X]', command=lambda: butts[i].destroy()))
            butts[i].grid(row = buttonnum + 4, column = 4)
        self.butts = butts
        print(butts)



app = Atlanta()
app.mainloop()