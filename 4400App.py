
#import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import hashlib
from WebService import *

LARGE_FONT= ("Verdana", 12)
global prop

class Atlanta(Tk):

    def __init__(self, *args, **kwargs):
        
        Tk.__init__(self, *args, **kwargs)
        global prop
        self.container = Frame(self)
        self.container.pack(side="top", fill="both", expand = True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Will eventually hold the email of the current user
        self.username = StringVar()
        prop = []
        self.prop = prop


        #########################################
        #          Make sure you add            #
        #          your new page here           #
        #########################################
        allPages = (loginPage, visitorRegistration, ownerRegistration, adminFunctions, visitorView, visitHistory, viewVisitorList, 
            viewOwnerList, approvedOrganisms, pendingOrganisms, unconfirmedProperties, confirmedProperties, visitorPropertyPage, propertyDetails, otherOwnerProperties, ownerFunctionality, addNewProperty)

        #for F in allPages:
            #frame = F(container, self)
            #self.frames[F] = frame
            #frame.grid(row=0, column=0, sticky="nsew")
        #self.show_frame(login_page)
        #mainFrame = loginPage(self.container, self)
        self._frame = None
        self.show_frame(loginPage)

    def show_frame(self, frame):
        # frame = self.frames[cont]
        # frame.tkraise()

        newFrame = frame(self.container, self)
        #newFrame.grid(row=0, column=0, sticky="nsew")
        newFrame.pack()
        if self._frame is not None:
            self._frame.destroy()
        self._frame = newFrame
        self._frame.pack()


class loginPage(Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        Frame.__init__(self,parent)
        label = Label(self, text="Login Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        f = Frame(self)
        self.f = f
        f.pack(padx=5, pady=20, side=LEFT)
        
        email = Label(f, text="Username: ")
        email.grid(row=0, column=0, sticky='w')
        email.focus_set()

        self.emailEntry = Entry(f, background='white', width=24, textvariable=self.controller.username)

        self.emailEntry.grid(row=0, column=1, sticky='w')
        self.emailEntry.focus_set()

        password = Label(f, text="Password: ")
        password.grid(row=1, column=0, sticky='w')
        password.focus_set()

        self.passwordEntry = Entry(f, background='white', width=24)

        
        self.passwordEntry.grid(row=1, column=1, sticky='w')

        button0 = Button(f, text="Login", command=self.login)
        button0.grid(row=2, column=1, sticky='w')
        button1 = Button(f, text="New Owner Registration", command=lambda: self.controller.show_frame(ownerRegistration))
        button1.grid(row=3, column=0, sticky='w')

        button2 = Button(f, text="New Visitor Registration", command=lambda: self.controller.show_frame(visitorRegistration))
        button2.grid(row=3, column=1, sticky='w')

    #login onclick event
    def login(self):
        # Initialize hash function
        hashfunc = hashlib.sha256()
        # Add the password string inputted into hash function
        hashfunc.update(str(self.passwordEntry.get()).encode())
        # Get hashed password
        hashPass = hashfunc.digest()

        # Call verifyLogin function from web service
        verify = DBManager.verifyLogin(self, self.emailEntry.get(), hashPass)

        if verify:
            self.controller.username = self.emailEntry.get()

            # log in was successful; fetch user type
            userType = DBManager.getUserType(self, self.controller.username)

            if "OWNER" in userType:
                self.controller.show_frame(ownerFunctionality)

            elif "VISITOR" in userType:
                self.controller.show_frame(visitorView)
            else:
                self.controller.show_frame(adminFunctions)
        else:
            error = Label(self.f, text="Email or password was incorrect")
            error.grid(row=4, column=0)


class visitorRegistration(Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        Frame.__init__(self, parent)
        label = Label(self, text="New Visitor Registration", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        
        #email.grid(row = 1, column = 0, padx = 20, pady = 10)
        dialog_frame = Frame(self)
        self.f = dialog_frame
        dialog_frame.pack(padx=5, pady=20, side=LEFT)
        self.frame = dialog_frame

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
        
        button1 = Button(dialog_frame, text="Cancel", command=lambda: self.controller.show_frame(loginPage))
        button1.grid(row=4, column=0, sticky='w')
        button2 = Button(dialog_frame, text="Register Visitor", command=self.registervisitor)
        button2.grid(row=4, column=1, sticky='w')

    def registervisitor(self):

        msg = StringVar()
        
        if len(self.password.get()) < 8:
            messagebox.showerror("Error", "Password must be at least 8 character")
        elif self.password.get() != self.confirmPassword.get():
            messagebox.showerror("Error", "Confirm password does not match")
        elif len(self.username.get()) == 0:
            messagebox.showerror("Error", "Must input Username")
        elif "@" not in self.email.get():
            messagebox.showerror("Error", "Invalid email")
        else:
            temp = self.email.get().split("@")
            if "." not in temp[1]:
                messagebox.showerror("Error", "Invalid email")
            else:
                hashfunc = hashlib.sha256()
                # Add the password string inputted into hash function
                hashfunc.update(str(self.password.get()).encode())
                # Get hashed password
                hashPass = hashfunc.digest()

                # First verify the email isn't being used
                emailExists = DBManager.checkEmail(self, self.email.get())
                if not emailExists:

                    # Next verify the username isn't being used
                    usernameExists = DBManager.checkUsername(self, self.username.get())

                    if not usernameExists:
                        # Username and email aren't taken already; register user
                        register = DBManager.registerNewUser(self, self.email.get(), self.username.get(), hashPass, 'Visitor')

                        if register:
                            messagebox.showerror("Account Created", "Registration was a success!"
                                                                    "You can now login on the login page.")


                        else:
                            messagebox.showerror("Error", "Something went wrong")


                    else:
                        messagebox.showerror("Error", "Username is taken")

                else:
                    messagebox.showerror("Error", "Email is already associated with an account")
        


class visitorView(Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        Frame.__init__(self, parent)
        label = Label(self, text="Welcome Visitor", font =LARGE_FONT)
        label.grid(row=0, column=0)

        props = Label(self, text="All public, validated properties:")
        props.grid(row=1, column=0)

        frame = Frame(self)
        table = Treeview(frame, selectmode='browse')
        table.bind("<Button-1>", self.onClick)
        self.selectedVisitorprop = []
        self.frame = frame
        self.table = table
        table['columns'] = ('Name', 'Size', 'Commercial', 'Public', 'Street', 'City', 'ZIP', 'Type', 'Owner',
                            'visits', 'rating')

        table.column('#0', anchor='w', width=50)
        table.heading('#0', text='ID', anchor='w')

        table.column('Name', anchor='center', width=100)
        table.heading('Name', text='Name')

        table.column('Size', anchor='center', width=80)
        table.heading('Size', text='Size')

        table.column('Commercial', anchor='center', width=100)
        table.heading('Commercial', text='Commercial')

        table.column('Public', anchor='center', width=100)
        table.heading('Public', text='Public')

        table.column('Street', anchor='center', width=100)
        table.heading('Street', text='Street')

        table.column('City', anchor='center', width=100)
        table.heading('City', text='City')

        table.column('ZIP', anchor='center', width=80)
        table.heading('ZIP', text='ZIP')

        table.column('Type', anchor='center', width=100)
        table.heading('Type', text='Type')

        table.column('Owner', anchor='center', width=100)
        table.heading('Owner', text='Owner')

        table.heading('visits', text='Visits')
        table.column('visits', anchor='center', width = 100)

        table.heading('rating', text='Avg Rating')
        table.column('rating', anchor='center', width = 100)
        table.grid(sticky=(N,S,W,E))
        frame.treeview = self.table
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        frame.grid(sticky=(N,S,W,E))
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        
        #WORKING HERE

        #load data
        publicProps = DBManager.getPublicProperties(self)
        if publicProps is None:
            publicProps = []


        for prop in publicProps:
            id = prop[0]
            name = prop[1]
            size = prop[2]
            comm = prop[3]
            pub = prop[4]
            st = prop[5]
            city = prop[6]
            zip = prop[7]
            type = prop[8]
            owner = prop[9]
            

            # Change tinyint values into true/false for commercial and public
            if comm == 1:
                commercial = True
            else:
                commercial = False

            if pub == 1:
                public = True
            else:
                public = False


            newProp = [name, size, commercial, public, st, city, zip, type, owner]

            frame.treeview.insert('', 'end', text=id, values=newProp)

     
        types = {'Name', 'City', 'Type', 'Visits','Avg Rating'}
    
        search = StringVar()
        search.set(' ')
        self.search = search
        search_menu = OptionMenu(frame, search, 'Name', *types)
        search_menu.grid(row=3, column=0, sticky='w', padx=50, pady=10)
        self.term = Entry(self, text="Search Term")
        self.term.grid(row=3, column = 0, sticky='w', padx=50, pady=10)

        self.removed = []
        self.searchprop = Button(self, text="Search Properties", command=self.searchfunc)
        self.searchprop.grid(row=4, column=0, sticky='w', padx=50, pady=10)

        viewprop = Button(self, text="View Property", command= self.viewProperty)
        viewprop.grid(row=3, column=0, padx=50, pady=10)

        viewhist = Button(self, text="View Visit History", command=lambda: self.controller.show_frame(visitHistory))
        viewhist.grid(row=4, column=0, padx=50, pady=10)

        logout = Button(self, text="Log Out", command=lambda: self.controller.show_frame(loginPage))
        logout.grid(row=3, column=0, sticky='e', padx=50, pady=10)

    def searchfunc(self, item=''):
        children = self.frame.treeview.get_children(item)
        if(self.term.get() ==  ''):
            for i in range(len(self.removed)):
                self.frame.treeview.insert('', 'end', text=self.removed[i][0], values=(self.removed[i][1], self.removed[i][2], self.removed[i][3], self.removed[i][4], self.removed[i][5], self.removed[i][6], self.removed[i][7], self.removed[i][8], self.removed[i][9], self.removed[i][10]))
            self.removed = []
        else:
            index = 0
            if (self.search.get() == "Name"):
                index = 0
            elif (self.search.get() == "City"):
                index = 2
            elif (self.search.get() == "Type"):
                index = 5
            elif (self.search.get() == "Visits"):
                index = 9
            elif (self.search.get() == "Avg Rating"):
                index = 10

            for child in children:
                temp1 = []
                text = self.frame.treeview.item(child, 'text')
                temp1.append(text)
                for x in self.table.item(child, "values"):
                        temp1.append(x)
                #print(self.table.item(child, "values"))
                if (temp1[index] == self.term.get()):
                    self.frame.treeview.selection_set(child)
                else:
                    if ('-' in self.term.get()):
                        tempterm = self.term.get().split("-")
                        # print(float(temp1[index]))
                        # print(float(tempterm[0]))
                        if (float(temp1[index]) >= float(tempterm[0]) and float(temp1[index]) <= float(tempterm[1])):
                            self.frame.treeview.selection_set(child)
                        else:
                            res = self.searchfunc(child)
                    
                            self.removed.append(temp1)
                            self.frame.treeview.delete(child)
                            if res:
                                break

                    else:
                        res = self.searchfunc(child)
                    
                        self.removed.append(temp1)
                        self.frame.treeview.delete(child)
                        if res:
                            break

    def onClick(self, event):
        item = self.table.identify_column(event.x)
        self.element = self.table.identify_row(event.y)
        self.element = self.table.item(self.element, "text")
        if self.table.identify_region(event.x, event.y) == "heading" and item in ['#0', '#2', '#5', '#9', '#10']:

            children = self.frame.treeview.get_children('')
            temp = []
            for child in children:
                temp1 = []
                text = self.frame.treeview.item(child, 'text')
                temp1.append(text)
                for x in self.table.item(child, "values"):
                    temp1.append(x)
                temp.append(temp1)
                self.frame.treeview.delete(child)

            if item == '#0':
                #Name

                temp.sort(key=lambda x: x[0])
                for i in range(len(temp)):
                    self.frame.treeview.insert('', 'end', text=temp[i][0], values=(temp[i][1], temp[i][2], temp[i][3], temp[i][4], temp[i][5], temp[i][6], temp[i][7], temp[i][8], temp[i][9], temp[i][10]))


            if item == '#2':
                #City

                temp.sort(key=lambda x: x[2])
                for i in range(len(temp)):
                    self.frame.treeview.insert('', 'end', text=temp[i][0], values=(temp[i][1], temp[i][2], temp[i][3], temp[i][4], temp[i][5], temp[i][6], temp[i][7], temp[i][8], temp[i][9], temp[i][10]))

            if item == '#5':
                #Type

                temp.sort(key=lambda x: x[5])
                for i in range(len(temp)):
                    self.frame.treeview.insert('', 'end', text=temp[i][0], values=(temp[i][1], temp[i][2], temp[i][3], temp[i][4], temp[i][5], temp[i][6], temp[i][7], temp[i][8], temp[i][9], temp[i][10]))

            if item == '#9':
                #Visits

                temp.sort(key=lambda x: x[9])
                for i in range(len(temp)):
                    self.frame.treeview.insert('', 'end', text=temp[i][0], values=(temp[i][1], temp[i][2], temp[i][3], temp[i][4], temp[i][5], temp[i][6], temp[i][7], temp[i][8], temp[i][9], temp[i][10]))

            if item == '#10':
                #Avg Rating

                temp.sort(key=lambda x: x[10])
                for i in range(len(temp)):
                    self.frame.treeview.insert('', 'end', text=temp[i][0], values=(temp[i][1], temp[i][2], temp[i][3], temp[i][4], temp[i][5], temp[i][6], temp[i][7], temp[i][8], temp[i][9], temp[i][10]))

        # for x in self.table.item(item, "values"):
        #     i.append(x)
        # self.selectedVisitorprop = i
        # print(self.selectedVisitorprop)
    def viewProperty(self):
        global prop
       
        prop = DBManager.getPropertyDetails(self, propID = self.element)
       
        self.controller.show_frame(visitorPropertyPage)

class visitHistory(Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        Frame.__init__(self, parent)
        label = Label(self, text="Your Visit History", font=LARGE_FONT)
        label.grid(row=0, column=0, padx=50, pady=20)

        frame = Frame(self)

        table = Treeview(frame)
        self.table = table
        self.frame = frame

        # Get owners username
        self.controller = controller
        username = self.controller.username
        welcomemsg = 'Your Visit History'

        # Get a list with all of the owners properties
        propList = DBManager.getVisitHistory(self, username)
        if propList is None:
            propList = []


        self.table.bind("<Button-1>", self.onClick)
        table['columns'] = ('date', 'rating')

        self.table.heading('#0', text='Name', anchor='w')
        self.table.column('#0', anchor='w')
        self.table.heading('date', text='Date Logged')
        self.table.column('date', anchor='center', width = 100)
        self.table.heading('rating', text='Rating')
        self.table.column('rating', anchor='center', width = 100)

        self.table.grid(sticky=(N,S,W,E))
        self.frame.treeview = table
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        self.frame.grid(sticky=(N,S,W,E))
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)


        for prop in propList:
            
            name = prop[0]
            date = prop[1]
            rating = prop[2]

            newProp = [name, date, rating]

            frame.treeview.insert('', 'end', text=id, values=newProp)

        # loads temp data
        
        propdetails = Button(self, text="View Property Details", command=lambda: self.controller.show_frame(loginPage))
        propdetails.grid(row=2, column=0, pady=10)

        back = Button(self, text="Back", command=lambda: self.controller.show_frame(visitorView))
        back.grid(row=3, column=0, pady=10)

    def onClick(self, event):
        item = self.table.identify_column(event.x)

        if self.table.identify_region(event.x, event.y) == "heading" and item in ['#0', '#1', '#2']:

            children = self.frame.treeview.get_children('')
            temp = []
            for child in children:
                temp1 = []
                text = self.frame.treeview.item(child, 'text')
                temp1.append(text)
                for x in self.table.item(child, "values"):
                    temp1.append(x)
                temp.append(temp1)
                self.frame.treeview.delete(child)

            if item == '#0':
                #Name

                temp.sort(key=lambda x: x[0])
                for i in range(len(temp)):
                    self.frame.treeview.insert('', 'end', text=temp[i][0], values=(temp[i][1], temp[i][2]))


            if item == '#1':
                #Date

                temp.sort(key=lambda x: x[1])
                for i in range(len(temp)):
                    self.frame.treeview.insert('', 'end', text=temp[i][0], values=(temp[i][1], temp[i][2]))

            if item == '#2':
                #Rating

                temp.sort(key=lambda x: x[2])
                for i in range(len(temp)):
                    self.frame.treeview.insert('', 'end', text=temp[i][0], values=(temp[i][1], temp[i][2]))

class ownerRegistration(Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        Frame.__init__(self, parent)
        label = Label(self, text="New Owner Registration", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        frame = Frame(self)
        frame.pack(padx=5, pady=20, side=LEFT)
        self.frame = frame
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
        
        self.propTypeVar = StringVar()
        self.propTypeVar.set(' ')
        propType_menu = OptionMenu(frame, self.propTypeVar, "Farm", *types, command=self.func)
        propType_menu.grid(row=9, column=1, padx=20, pady=10)

        # Create crop label
        crop = Label(frame, text="Crop:* ")
        crop.grid(row=10, column=0, padx=20, pady=10)

        # Get list of approved, fruits, nuts, veggies, and flowers (since farm is default)
        fruits = DBManager.getApprovedFruits(self)
        nuts = DBManager.getApprovedNuts(self)
        veggies = DBManager.getApprovedVegetables(self)
        flowers = DBManager.getApprovedFlowers(self)
        crops = fruits + nuts + veggies + flowers

        # Get approved animals
        self.animal = Label(frame, text="Animal:* ")
        self.animal.grid(row=10, column=2, padx=20, pady=10)

        animals = DBManager.getApprovedAnimals(self)
        self.animalVar = StringVar()
        self.animalMenu = OptionMenu(frame, self.animalVar, *animals)
        self.animalMenu.grid(row=10, column=3, padx=20, pady=10)

        # Create option menu with the approved crops
        self.cropVar = StringVar()
        self.cropMenu = OptionMenu(frame, self.cropVar, *crops)
        self.cropMenu.grid(row=10, column=1, padx=20, pady=10)

        # Add yes/no drop down for isPublic
        yesno = ["Yes", "No"]
        public = Label(frame, text="Public:* ")
        public.grid(row=11, column=0, sticky='w')
        self.publicVar = StringVar()
        publicMenu = OptionMenu(frame, self.publicVar, "Yes", *yesno)
        publicMenu.grid(row=11, column=1, padx=20, pady=10)

        # Add yes/no drop down for isCommercial
        commercial = Label(frame, text="Commercial:* ")
        commercial.grid(row=12, column=0, sticky='w')
        self.commVar = StringVar()
        commMenu = OptionMenu(frame, self.commVar, "Yes", *yesno)
        commMenu.grid(row=12, column=1, padx=20, pady=10)

        # Buttons
        button1 = Button(frame, text="Cancel", command=lambda: self.controller.show_frame(loginPage))
        button1.grid(row=13, column=0, sticky='w')
        button2 = Button(frame, text="Register Owner", command=self.registerowner)
        button2.grid(row=13, column=1, sticky='w')

    def func(self, value):
        if value == 'Farm':
            # Farm GUI
            self.cropMenu.destroy()

            # Get list of approved, fruits, nuts, veggies, and flowers
            fruits = DBManager.getApprovedFruits(self)
            nuts = DBManager.getApprovedNuts(self)
            veggies = DBManager.getApprovedVegetables(self)
            flowers = DBManager.getApprovedFlowers(self)
            crops = fruits + nuts + veggies + flowers

            # Get approved animals
            self.animal = Label(self.frame, text="Animal:* ")
            self.animal.grid(row=10, column=2, padx=20, pady=10)

            animals = DBManager.getApprovedAnimals(self)
            self.animalVar = StringVar()
            self.animalMenu = OptionMenu(self.frame, self.animalVar, *animals)
            self.animalMenu.grid(row=10, column=3, padx=20, pady=10)

        elif value == 'Garden':
            # Garden
            self.cropMenu.destroy()
            self.animal.destroy()
            self.animalMenu.destroy()

            # Get approved vegetables and flowers from DB
            veggies = DBManager.getApprovedVegetables(self)
            flowers = DBManager.getApprovedFlowers(self)
            crops = veggies + flowers

        else:
            # Orchard
            self.cropMenu.destroy()
            self.animal.destroy()
            self.animalMenu.destroy()

            # Get approved vegetables and flowers from DB
            fruits = DBManager.getApprovedFruits(self)
            nuts = DBManager.getApprovedNuts(self)
            crops = fruits + nuts

        # Recreate drop down menu with new approved crops
        self.cropVar = StringVar()
        self.cropMenu = OptionMenu(self.frame, self.cropVar, *crops)
        self.cropMenu.grid(row=10, column=1, padx=20, pady=10)

        return value

    def registerowner(self):
        msg = StringVar()

        if len(self.password.get()) < 8:
            messagebox.showerror("Error", "Password must be at least 8 character")
        elif self.password.get() != self.confirmPassword.get():
            messagebox.showerror("Error", "Confirm password does not match")
        elif len(self.username.get()) == 0:
            messagebox.showerror("Error", "Must input Username")
        elif len(self.propName.get()) == 0:
            messagebox.showerror("Error", "Must input Property Name")
        elif len(self.propAddress.get()) == 0:
            messagebox.showerror("Error", "Must input Street Address")
        elif len(self.propCity.get()) == 0:
            messagebox.showerror("Error", "Must input City")
        elif len(self.propZip.get()) == 0:
            messagebox.showerror("Error", "Must input Zip")
        elif len(self.propAcres.get()) == 0:
            messagebox.showerror("Error", "Must input Acres")
        elif "@" not in self.email.get():
            messagebox.showerror("Error", "Invalid email")
        else:
            temp = self.email.get().split("@")
            if "." not in temp[1]:
                messagebox.showerror("Error", "Invalid email")
            else:
                hashfunc = hashlib.sha256()
                # Add the password string inputted into hash function
                hashfunc.update(str(self.password.get()).encode())
                # Get hashed password
                hashPass = hashfunc.digest()

                # First verify the email isn't being used
                emailExists = DBManager.checkEmail(self, self.email.get())
                if not emailExists:

                    # Next verify the username isn't being used
                    usernameExists = DBManager.checkUsername(self, self.username.get())
                    if not usernameExists:

                        # Verify property name isn't already taken
                        propNameExists = DBManager.checkPropertyName(self, self.propName.get())
                        if not propNameExists:
                            # Tests all passed, Add property and crop first

                            # Change public and commercial to 1 or 0
                            if self.publicVar.get() == 'Yes':
                                public = 1
                            else:
                                public = 0

                            if self.commVar.get() == 'Yes':
                                comm = 1
                            else:
                                comm = 0

                            # register user
                            register = DBManager.registerNewUser(self, self.email.get(),
                                                                self.username.get(), hashPass, 'Owner')

                            # Add the property
                            addProp = DBManager.addProperty(self, self.propName.get(), self.propAddress.get(),
                                                            self.propCity.get(), self.propZip.get(), public,
                                                            comm, self.propTypeVar.get(), self.username.get(),
                                                            self.propAcres.get())

                            # Get property ID for the new property
                            propID = DBManager.getPropertyID(self, self.propName.get())

                            # Add crop to Has table
                            crop = self.cropVar.get()
                            cropAdded = DBManager.addItem(self, propID, crop)

                            # If property is a farm then add animal also
                            if self.propTypeVar.get() == 'Farm':
                                animal = self.animalVar.get()
                                animalAdded = DBManager.addItem(self, propID, animal)

                                # Make sure everything was successful (including animal)
                                if register and addProp and cropAdded and animalAdded:
                                    # Now add user to User table
                                    messagebox.showerror("Account Created", "Registration was a success!"
                                                                            "You can now login on the login page.")
                                else:
                                    messagebox.showerror("Error", "Something went wrong")
                            else:
                                # Garden and orchard; Make sure everything was successful
                                if register and addProp and cropAdded:
                                    messagebox.showerror("Account Created", "Registration was a success!"
                                                                            "You can now login on the login page.")
                                else:
                                    messagebox.showerror("Error", "Something went wrong")
                        else:
                            messagebox.showerror("Error", "Property name is taken. Please choose a new name.")

                    else:
                        messagebox.showerror("Error", "Username is taken. Please choose a new username.")

                else:
                    messagebox.showerror("Error", "Email is already associated with an account")

class adminFunctions(Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        Frame.__init__(self, parent)
        label = Label(self, text="Admin Functionality", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        visListB = Button(self, text="View Visitor List", command=lambda: self.controller.show_frame(viewVisitorList))
        visListB.pack(fill = X)

        ownListB = Button(self, text="View Owner List", command=lambda: self.controller.show_frame(viewOwnerList))
        ownListB.pack(fill = X)

        conPropB = Button(self, text="View Confirmed Properties", command=lambda: self.controller.show_frame(confirmedProperties))
        conPropB.pack(fill = X)

        unconPropB = Button(self, text="View Unconfirmed Properties", command=lambda: self.controller.show_frame(unconfirmedProperties))
        unconPropB.pack(fill =X)

        approvedB = Button(self, text="View Approved Animals and Crops", command=lambda: self.controller.show_frame(approvedOrganisms))
        approvedB.pack(fill = X)

        pendingB = Button(self, text="View Pending Animals and Crops", command=lambda: self.controller.show_frame(pendingOrganisms))
        pendingB.pack(fill =X)

        logoutB = Button(self, text="Logout", command=lambda: self.controller.show_frame(loginPage))
        logoutB.pack(fill =X)

class viewVisitorList(Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        Frame.__init__(self, parent)
        label = Label(self, text="All Visitors in System", font =LARGE_FONT)
        label.grid(row=0, column=0)

        frame = Frame(self)


        #self.selectedVisitorprop = []
        self.frame = frame

        self.table = Treeview(frame,selectmode='browse')
        self.table['columns'] = ('Email', 'Logged Visits')
        self.table.heading('#0', text='Username', anchor='w')
        self.table.column('#0', anchor='w')
        
        self.table.heading('Email', text='Email')
        self.table.column('Email', anchor='center', width = 100)
        self.table.heading('Logged Visits', text='Logged Visits')
        self.table.column('Logged Visits', anchor='center', width = 100)
       
        self.table.grid(sticky=(N,S,W,E))
        self.table.bind("<Button-1>", self.onClick)
        frame.treeview = self.table
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        frame.grid(sticky=(N,S,W,E))
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)


        types = { 'Username', 'Email', 'Logged Visits'}
        
        search = StringVar()
        search.set(' ')
        self.search = search
        search_menu = OptionMenu(frame, search, 'Username', *types)
        search_menu.grid(row=3, column=0, sticky='w', padx=50, pady=10)

        self.term = Entry(self, text="Search Term")
        self.term.grid(row=3, column = 0, sticky='w', padx=50, pady=10)

        self.removed = []
        self.searchprop = Button(self, text="Search Visitors", command=self.searchfunc)
        self.searchprop.grid(row=4, column=0, sticky='w', padx=50, pady=10)

        deletevisitor = Button(self, text="Delete Visitor Account", command=lambda: self.controller.show_frame(adminFunctions))
        deletevisitor.grid(row=3, column=0, padx=50, pady=10)

        deletelog = Button(self, text="Delete Log History", command=lambda: self.controller.show_frame(adminFunctions))
        deletelog.grid(row=4, column=0, padx=50, pady=10)

        back = Button(self, text="Back", command=lambda: self.controller.show_frame(adminFunctions))
        back.grid(row=3, column=0, sticky='e', padx=50, pady=10)


    def searchfunc(self, item=''):
        children = self.frame.treeview.get_children(item)
        if(self.term.get() ==  ''):
            for i in range(len(self.removed)):
                self.frame.treeview.insert('', 'end', text=self.removed[i][0], values=(self.removed[i][1], self.removed[i][2]))
            self.removed = []
        else:
            index = 0
            if (self.search.get() == "Username"):
                index = 0
            elif (self.search.get() == "Email"):
                index = 1
            elif (self.search.get() == "Logged Visits"):
                index = 2


            for child in children:
                temp1 = []
                text = self.frame.treeview.item(child, 'text')
                temp1.append(text)
                for x in self.table.item(child, "values"):
                        temp1.append(x)

                if (temp1[index] == self.term.get()):
                    self.frame.treeview.selection_set(child)
                else:
                    res = self.searchfunc(child)

                    self.removed.append(temp1)
                    self.frame.treeview.delete(child)
                    if res:
                        break
    def onClick(self, event):
        item = self.table.identify_column(event.x)

        if self.table.identify_region(event.x, event.y) == "heading" and item in ['#0', '#1', '#2']:

            children = self.frame.treeview.get_children('')
            temp = []
            for child in children:
                temp1 = []
                text = self.frame.treeview.item(child, 'text')
                temp1.append(text)
                for x in self.table.item(child, "values"):
                    temp1.append(x)
                temp.append(temp1)
                self.frame.treeview.delete(child)

            if item == '#0':
                #Username
                print("Username")
                temp.sort(key=lambda x: x[0])
                for i in range(len(temp)):
                    self.frame.treeview.insert('', 'end', text=temp[i][0], values=(temp[i][1], temp[i][2]))


            if item == '#1':
                #Email
                print("Email")
                temp.sort(key=lambda x: x[1])
                for i in range(len(temp)):
                    self.frame.treeview.insert('', 'end', text=temp[i][0], values=(temp[i][1], temp[i][2]))
            if item == '#2':
                #Logged Visitss
                print("Logged Visits")
                temp.sort(key=lambda x: x[2])
                for i in range(len(temp)):
                    self.frame.treeview.insert('', 'end', text=temp[i][0], values=(temp[i][1], temp[i][2]))

class viewOwnerList(Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        Frame.__init__(self, parent)
        label = Label(self, text="All Owners in System", font =LARGE_FONT)
        label.grid(row=0, column=0)

        frame = Frame(self)


        table = Treeview(frame)
        self.table = table
        self.frame = frame
        self.table.bind("<Button-1>", self.onClick)
        self.table['columns'] = ('Email', 'Number of Properties')
        self.table.heading('#0', text='Username', anchor='w')
        self.table.column('#0', anchor='w')
        
        self.table.heading('Email', text='Email')
        self.table.column('Email', anchor='center', width = 100)
        self.table.heading('Number of Properties', text='Number of Properties')
        self.table.column('Number of Properties', anchor='center', width = 120)
       
        self.table.grid(sticky=(N,S,W,E))
        self.frame.treeview = table
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        self.frame.grid(sticky=(N,S,W,E))
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        types = { 'Username', 'Email', 'Number of Properties'}
        
        search = StringVar()
        search.set(' ')
        self.search = search
        search_menu = OptionMenu(frame, search, 'Username', *types)
        search_menu.grid(row=3, column=0, sticky='w', padx=50, pady=10)
        self.removed = []
        self.term = Entry(self, text="Search Term")
        self.term.grid(row=3, column = 0, sticky='w', padx=50, pady=10)

        searchowners = Button(self, text="Search Owners", command=self.searchfunc)
        searchowners.grid(row=4, column=0, sticky='w', padx=50, pady=10)

        deletelog = Button(self, text="Delete Owner Account", command=lambda: controller.show_frame(adminFunctions))
        deletelog.grid(row=4, column=0, padx=50, pady=10)

        back = Button(self, text="Back", command=lambda: self.controller.show_frame(adminFunctions))
        back.grid(row=3, column=0, sticky='e', padx=50, pady=10)


    def searchfunc(self, item=''):
        children = self.frame.treeview.get_children(item)
        if(self.term.get() ==  ''):
            for i in range(len(self.removed)):
                self.frame.treeview.insert('', 'end', text=self.removed[i][0], values=(self.removed[i][1], self.removed[i][2]))
            self.removed = []
        else:
            index = 0
            if (self.search.get() == "Username"):
                index = 0
            elif (self.search.get() == "Email"):
                index = 1
            elif (self.search.get() == "Number of Properties"):
                index = 2

            for child in children:
                temp1 = []
                text = self.frame.treeview.item(child, 'text')
                temp1.append(text)
                for x in self.table.item(child, "values"):
                        temp1.append(x)
                #print(self.table.item(child, "values"))
                if (temp1[index] == self.term.get()):
                    self.frame.treeview.selection_set(child)
                else:
                    res = self.searchfunc(child)

                    self.removed.append(temp1)
                    self.frame.treeview.delete(child)
                    if res:
                        break

    def onClick(self, event):
        item = self.table.identify_column(event.x)

        if self.table.identify_region(event.x, event.y) == "heading" and item in ['#0', '#1', '#2']:

            children = self.frame.treeview.get_children('')
            temp = []
            for child in children:
                temp1 = []
                text = self.frame.treeview.item(child, 'text')
                temp1.append(text)
                for x in self.table.item(child, "values"):
                    temp1.append(x)
                temp.append(temp1)
                self.frame.treeview.delete(child)

            if item == '#0':
                #Name

                temp.sort(key=lambda x: x[0])
                for i in range(len(temp)):
                    self.frame.treeview.insert('', 'end', text=temp[i][0], values=(temp[i][1], temp[i][2]))


            if item == '#1':
                #City

                temp.sort(key=lambda x: x[1])
                for i in range(len(temp)):
                    self.frame.treeview.insert('', 'end', text=temp[i][0], values=(temp[i][1], temp[i][2]))

            if item == '#2':
                #Type

                temp.sort(key=lambda x: x[2])
                for i in range(len(temp)):
                    self.frame.treeview.insert('', 'end', text=temp[i][0], values=(temp[i][1], temp[i][2]))


class approvedOrganisms(Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        Frame.__init__(self, parent)
        label = Label(self, text="Approved Owners/Crops", font =LARGE_FONT)
        label.grid(row=0, column=0)

        frame = Frame(self)
        self.frame = frame
        table = Treeview(frame,selectmode='browse')
        self.table = table
        table['columns'] = ('Type')
        table.heading('#0', text='Name', anchor='w')
        table.column('#0', anchor='w')
        table.heading('Type', text='Type')
        table.column('Type', anchor='center', width = 100)


        table.grid(sticky=(N,S,W,E))
        table.bind("<Button-1>", self.onClick)
        frame.treeview = self.table
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        frame.grid(sticky=(N,S,W,E))
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)


        types = {'Fruit', 'Vegetable', 'Nut', 'Flower', 'Animal'}
        
        search = StringVar()
        search.set(' ')
        self.search = search
        add = StringVar()
        add.set(' ')
        self.add = add

       
        searches = {'Type', 'Name'}
        search_menu = OptionMenu(frame, search, 'Name', *searches)
        search_menu.grid(row=3, column=1, sticky='w', padx=00, pady=10)

        type_menu = OptionMenu(frame, add, 'Fruit', *types)
        type_menu.grid(row=3, column=0, sticky='w', padx=00, pady=10)

        self.removed = []
        nameterm = Entry(self, text="Enter Name")
        nameterm.grid(row=4, column = 0, sticky='w', padx=00, pady=10)
        searchterm = Entry(self, text="Search Term")
        searchterm.grid(row=4, column = 1, sticky='w', padx=0, pady=10)

        self.nameterm = nameterm
        self.searchterm = searchterm
        searchB = Button(self, text="Search", command=self.searchfunc)
        searchB.grid(row=5, column=1, sticky='w', padx=0, pady=10)

        #TO DO- ADD TO PEDNING APPROVAL#
        #TO DO#
        addB = Button(self, text="Add to Approval List", command=lambda: controller.show_frame(adminFunctions))
        addB.grid(row=5, column=0, sticky='w', padx=00, pady=10)

        #TO DO- ADD TO DELETE SELECTION#
        #TO DO#
        deleteselection = Button(self, text="Delete Selection", command=lambda: self.controller.show_frame(adminFunctions))
        deleteselection.grid(row=6, column=0, padx=50, pady=10)


        back = Button(self, text="Back", command=lambda: self.controller.show_frame(adminFunctions))
        back.grid(row=6, column=0, sticky='e', padx=0, pady=10)
    def searchfunc(self, item=''):
        children = self.frame.treeview.get_children(item)
        if(self.searchterm.get() ==  ''):
            for i in range(len(self.removed)):
                self.frame.treeview.insert('', 'end', text=self.removed[i][0], values=(self.removed[i][1]))
            self.removed = []
        else:
            index = 0
            if (self.search.get() == "Name"):
                index = 0
            elif (self.search.get() == "Type"):
                index = 1

            for child in children:
                temp1 = []
                text = self.frame.treeview.item(child, 'text')
                temp1.append(text)
                for x in self.table.item(child, "values"):
                        temp1.append(x)

                if (temp1[index] == self.searchterm.get()):
                    self.frame.treeview.selection_set(child)
                else:
                    res = self.searchfunc(child)

                    self.removed.append(temp1)
                    self.frame.treeview.delete(child)
                    if res:
                        break

    def onClick(self, event):
        item = self.table.identify_column(event.x)
        if self.table.identify_region(event.x, event.y) == "heading" and item in ['#0', '#1']:

            children = self.frame.treeview.get_children('')
            temp = []
            for child in children:
                temp1 = []
                text = self.frame.treeview.item(child, 'text')
                temp1.append(text)
                for x in self.table.item(child, "values"):
                    temp1.append(x)
                temp.append(temp1)
                self.frame.treeview.delete(child)

            if item == '#0':
                #Name
                print("Name")
                temp.sort(key=lambda x: x[0])
                for i in range(len(temp)):
                    self.frame.treeview.insert('', 'end', text=temp[i][0], values=(temp[i][1]))
            if item == '#1':
                #Type
                print("Type")
                temp.sort(key=lambda x: x[1])
                for i in range(len(temp)):
                    self.frame.treeview.insert('', 'end', text=temp[i][0], values=(temp[i][1]))


class pendingOrganisms(Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        Frame.__init__(self, parent)
        label = Label(self, text="Pending Owners/Crops", font =LARGE_FONT)
        label.grid(row=0, column=0)

        frame = Frame(self)
        table = Treeview(frame)
        self.table = table
        self.removed = []
        self.frame = frame
        table['columns'] = ('Type')
        table.heading('#0', text='Name', anchor='w')
        table.column('#0', anchor='w')
        
        table.heading('Type', text='Type')
        table.column('Type', anchor='center', width = 100)
        
        table.grid(sticky=(N,S,W,E))
        table.bind("<Button-1>", self.onClick)
        frame.treeview = table
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        frame.grid(sticky=(N,S,W,E))
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

   
        approveB = Button(self, text="Approve Selection", command=lambda: controller.show_frame(adminFunctions))
        approveB.grid(row=4, column=0)

        deleteselection = Button(self, text="Delete Selection", command=lambda: self.controller.show_frame(adminFunctions))
        deleteselection.grid(row=5, column=0)

        back = Button(self, text="Back", command=lambda: self.controller.show_frame(adminFunctions))
        back.grid(row=6, column=0, sticky='e')

    def searchfunc(self, item=''):
        children = self.frame.treeview.get_children(item)
        if(self.searchterm.get() ==  ''):
            for i in range(len(self.removed)):
                self.frame.treeview.insert('', 'end', text=self.removed[i][0], values=(self.removed[i][1]))
            self.removed = []
        else:
            index = 0
            if (self.search.get() == "Name"):
                index = 0
            elif (self.search.get() == "Type"):
                index = 1

            for child in children:
                temp1 = []
                text = self.frame.treeview.item(child, 'text')
                temp1.append(text)
                for x in self.table.item(child, "values"):
                        temp1.append(x)

                if (temp1[index] == self.searchterm.get()):
                    self.frame.treeview.selection_set(child)
                else:
                    res = self.searchfunc(child)

                    self.removed.append(temp1)
                    self.frame.treeview.delete(child)
                    if res:
                        break

    def onClick(self, event):
        item = self.table.identify_column(event.x)
        if self.table.identify_region(event.x, event.y) == "heading" and item in ['#0', '#1']:

            children = self.frame.treeview.get_children('')
            temp = []
            for child in children:
                temp1 = []
                text = self.frame.treeview.item(child, 'text')
                temp1.append(text)
                for x in self.table.item(child, "values"):
                    temp1.append(x)
                temp.append(temp1)
                self.frame.treeview.delete(child)

            if item == '#0':
                #Name
                print("Name")
                temp.sort(key=lambda x: x[0])
                for i in range(len(temp)):
                    self.frame.treeview.insert('', 'end', text=temp[i][0], values=(temp[i][1]))
            if item == '#1':
                #Type
                print("Type")
                temp.sort(key=lambda x: x[1])
                for i in range(len(temp)):
                    self.frame.treeview.insert('', 'end', text=temp[i][0], values=(temp[i][1]))
class confirmedProperties(Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        Frame.__init__(self, parent)
        label = Label(self, text="Confirmed Properties:", font =LARGE_FONT)
        label.grid(row=0, column=0)

        frame = Frame(self)

        table = Treeview(frame)
        self.frame = frame
        self.table = table
        self.table.bind("<Button-1>", self.onClick)
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

        types = {'Name', 'Zip', 'Type', 'Verified By','Avg Rating'}
        
        search = StringVar()
        search.set(' ')
        search_menu = OptionMenu(frame, search, 'Name', *types)
        search_menu.grid(row=3, column=0, sticky='w', padx=50, pady=10)
        self.removed = []
        term = Entry(self, text="Search Term")
        term.grid(row=3, column = 0, sticky='w', padx=50, pady=10)

        searchprop = Button(self, text="Search Properties", command=self.searchfunc)
        searchprop.grid(row=4, column=0, sticky='w', padx=50, pady=10)
        self.search = search
        self.term = term
        mprop = Button(self, text="Manage Selected Property", command=lambda: self.controller.show_frame(loginPage))
        mprop.grid(row=3, column=0, padx=50, pady=10)

        back = Button(self, text="Back", command=lambda: self.controller.show_frame(adminFunctions))
        back.grid(row=3, column=0, sticky='e', padx=50, pady=10)

    def searchfunc(self, item=''):
        children = self.frame.treeview.get_children(item)
        if(self.term.get() ==  ''):
            for i in range(len(self.removed)):
                self.frame.treeview.insert('', 'end', text=self.removed[i][0], values=(self.removed[i][1], self.removed[i][2], self.removed[i][3], self.removed[i][4], self.removed[i][5], self.removed[i][6], self.removed[i][7], self.removed[i][8], self.removed[i][9], self.removed[i][10]))
            self.removed = []
        else:
            index = 0
            if (self.search.get() == "Name"):
                index = 0
            elif (self.search.get() == "City"):
                index = 2
            elif (self.search.get() == "Type"):
                index = 5
            elif (self.search.get() == "Verified By"):
                index = 9
            elif (self.search.get() == "Avg Rating"):
                index = 10

            for child in children:
                temp1 = []
                text = self.frame.treeview.item(child, 'text')
                temp1.append(text)
                for x in self.table.item(child, "values"):
                        temp1.append(x)
                #print(self.table.item(child, "values"))
                if (temp1[index] == self.term.get()):
                    self.frame.treeview.selection_set(child)
                else:
                    if ('-' in self.term.get()):
                        tempterm = self.term.get().split("-")
                        # print(float(temp1[index]))
                        # print(float(tempterm[0]))
                        if (float(temp1[index]) >= float(tempterm[0]) and float(temp1[index]) <= float(tempterm[1])):
                            self.frame.treeview.selection_set(child)
                        else:
                            res = self.searchfunc(child)

                            self.removed.append(temp1)
                            self.frame.treeview.delete(child)
                            if res:
                                break

                    else:
                        res = self.searchfunc(child)

                        self.removed.append(temp1)
                        self.frame.treeview.delete(child)
                        if res:
                            break

    def onClick(self, event):
        item = self.table.identify_column(event.x)

        if self.table.identify_region(event.x, event.y) == "heading" and item in ['#0', '#2', '#5', '#9', '#10']:

            children = self.frame.treeview.get_children('')
            temp = []
            for child in children:
                temp1 = []
                text = self.frame.treeview.item(child, 'text')
                temp1.append(text)
                for x in self.table.item(child, "values"):
                    temp1.append(x)
                temp.append(temp1)
                self.frame.treeview.delete(child)

            if item == '#0':
                #Name

                temp.sort(key=lambda x: x[0])
                for i in range(len(temp)):
                    self.frame.treeview.insert('', 'end', text=temp[i][0], values=(temp[i][1], temp[i][2], temp[i][3], temp[i][4], temp[i][5], temp[i][6], temp[i][7], temp[i][8], temp[i][9], temp[i][10]))


            if item == '#2':
                #City

                temp.sort(key=lambda x: x[2])
                for i in range(len(temp)):
                    self.frame.treeview.insert('', 'end', text=temp[i][0], values=(temp[i][1], temp[i][2], temp[i][3], temp[i][4], temp[i][5], temp[i][6], temp[i][7], temp[i][8], temp[i][9], temp[i][10]))

            if item == '#5':
                #Type

                temp.sort(key=lambda x: x[5])
                for i in range(len(temp)):
                    self.frame.treeview.insert('', 'end', text=temp[i][0], values=(temp[i][1], temp[i][2], temp[i][3], temp[i][4], temp[i][5], temp[i][6], temp[i][7], temp[i][8], temp[i][9], temp[i][10]))

            if item == '#9':
                #Visits

                temp.sort(key=lambda x: x[9])
                for i in range(len(temp)):
                    self.frame.treeview.insert('', 'end', text=temp[i][0], values=(temp[i][1], temp[i][2], temp[i][3], temp[i][4], temp[i][5], temp[i][6], temp[i][7], temp[i][8], temp[i][9], temp[i][10]))

            if item == '#10':
                #Avg Rating

                temp.sort(key=lambda x: x[10])
                for i in range(len(temp)):
                    self.frame.treeview.insert('', 'end', text=temp[i][0], values=(temp[i][1], temp[i][2], temp[i][3], temp[i][4], temp[i][5], temp[i][6], temp[i][7], temp[i][8], temp[i][9], temp[i][10]))


#### TO DO
class unconfirmedProperties(Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        Frame.__init__(self, parent)
        label = Label(self, text="Unconfirmed Properties:", font =LARGE_FONT)
        label.grid(row=0, column=0)

        frame = Frame(self)

        table = Treeview(frame)
        self.frame = frame
        self.table = table
        self.table.bind("<Button-1>", self.onClick)
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

   
        types = {'Name', 'Size', 'Owner'}
        
        search = StringVar()
        search.set(' ')
        search_menu = OptionMenu(frame, search, 'Name', *types)
        search_menu.grid(row=3, column=0, sticky='w', padx=50, pady=10)
        self.removed = []
        term = Entry(self, text="Search Term")
        term.grid(row=3, column = 0, sticky='w', padx=50, pady=10)
        self.search = search
        self.term = term
        searchprop = Button(self, text="Search Properties", command=self.searchfunc)
        searchprop.grid(row=4, column=0, sticky='w', padx=50, pady=10)

        mprop = Button(self, text="Manage Selected Property", command=lambda: self.controller.show_frame(loginPage))
        mprop.grid(row=3, column=0, padx=50, pady=10)

        back = Button(self, text="Back", command=lambda: self.controller.show_frame(adminFunctions))
        back.grid(row=3, column=0, sticky='e', padx=50, pady=10)

    def searchfunc(self, item=''):
        children = self.frame.treeview.get_children(item)
        if(self.term.get() ==  ''):
            for i in range(len(self.removed)):
                self.frame.treeview.insert('', 'end', text=self.removed[i][0], values=(self.removed[i][1], self.removed[i][2], self.removed[i][3], self.removed[i][4], self.removed[i][5], self.removed[i][6], self.removed[i][7], self.removed[i][8], self.removed[i][9]))
            self.removed = []
        else:
            index = 0
            if (self.search.get() == "Name"):
                index = 0
            elif (self.search.get() == "Size"):
                index = 4
            elif (self.search.get() == "Owner"):
                index = 9
            

            for child in children:
                temp1 = []
                text = self.frame.treeview.item(child, 'text')
                temp1.append(text)
                for x in self.table.item(child, "values"):
                        temp1.append(x)
                #print(self.table.item(child, "values"))
                if (temp1[index] == self.term.get()):
                    self.frame.treeview.selection_set(child)
                else:
                    if ('-' in self.term.get()):
                        tempterm = self.term.get().split("-")
                        # print(float(temp1[index]))
                        # print(float(tempterm[0]))
                        if (float(temp1[index]) >= float(tempterm[0]) and float(temp1[index]) <= float(tempterm[1])):
                            self.frame.treeview.selection_set(child)
                        else:
                            res = self.searchfunc(child)

                            self.removed.append(temp1)
                            self.frame.treeview.delete(child)
                            if res:
                                break

                    else:
                        res = self.searchfunc(child)

                        self.removed.append(temp1)
                        self.frame.treeview.delete(child)
                        if res:
                            break

    def onClick(self, event):
        item = self.table.identify_column(event.x)

        if self.table.identify_region(event.x, event.y) == "heading" and item in ['#0', '#4', '#9']:

            children = self.frame.treeview.get_children('')
            temp = []
            for child in children:
                temp1 = []
                text = self.frame.treeview.item(child, 'text')
                temp1.append(text)
                for x in self.table.item(child, "values"):
                    temp1.append(x)
                temp.append(temp1)
                self.frame.treeview.delete(child)

            if item == '#0':
                #Name

                temp.sort(key=lambda x: x[0])
                for i in range(len(temp)):
                    self.frame.treeview.insert('', 'end', text=temp[i][0], values=(temp[i][1], temp[i][2], temp[i][3], temp[i][4], temp[i][5], temp[i][6], temp[i][7], temp[i][8], temp[i][9]))


            if item == '#4':
                #City

                temp.sort(key=lambda x: x[4])
                for i in range(len(temp)):
                    self.frame.treeview.insert('', 'end', text=temp[i][0], values=(temp[i][1], temp[i][2], temp[i][3], temp[i][4], temp[i][5], temp[i][6], temp[i][7], temp[i][8], temp[i][9]))

            if item == '#9':
                #Type

                temp.sort(key=lambda x: x[9])
                for i in range(len(temp)):
                    self.frame.treeview.insert('', 'end', text=temp[i][0], values=(temp[i][1], temp[i][2], temp[i][3], temp[i][4], temp[i][5], temp[i][6], temp[i][7], temp[i][8], temp[i][9]))

            

class addNewProperty(Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        Frame.__init__(self, parent)
        label = Label(self, text="Add New Property:", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        frame = Frame(self)
        self.frame = frame
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
        zipcode.grid(row=3, column=0, sticky='w')
        self.zipcode = Entry(frame, background='white', width=24)
        self.zipcode.grid(row=3, column=1, sticky='w')
        self.zipcode.focus_set()

        acres = Label(frame, text="Acres:* ")
        acres.grid(row=4, column=0, sticky='w')
        self.acres = Entry(frame, background='white', width=24)
        self.acres.grid(row=4, column=1, sticky='w')
        self.acres.focus_set()

        propType = Label(frame, text="Property Type:* ")
        propType.grid(row=5, column=0, sticky='w')

        # Rest of GUI depends on property type selected
        types = {'Garden', 'Farm', 'Orchard'}  # Dictionary holding different prop types

        self.propTypeVar = StringVar()
        self.propTypeVar.set(' ')
        propType_menu = OptionMenu(frame, self.propTypeVar, "Farm", *types, command=self.propertyTypeChange)
        propType_menu.grid(row=5, column=1, padx=20, pady=10)

        # Create crop label
        crop = Label(frame, text="Crop:* ")
        crop.grid(row=6, column=0, padx=20, pady=10)

        # Get list of approved, fruits, nuts, veggies, and flowers (since farm is default)
        fruits = DBManager.getApprovedFruits(self)
        nuts = DBManager.getApprovedNuts(self)
        veggies = DBManager.getApprovedVegetables(self)
        flowers = DBManager.getApprovedFlowers(self)
        crops = fruits + nuts + veggies + flowers

        # Create option menu with the approved crops
        self.cropVar = StringVar()
        self.cropMenu = OptionMenu(frame, self.cropVar, *crops)
        self.cropMenu.grid(row=6, column=1, padx=20, pady=10)

        # Get approved animals
        self.animal = Label(frame, text="Animal:* ")
        self.animal.grid(row=6, column=2, padx=20, pady=10)

        animals = DBManager.getApprovedAnimals(self)
        self.animalVar = StringVar()
        self.animalMenu = OptionMenu(frame, self.animalVar, *animals)
        self.animalMenu.grid(row=6, column=3, padx=20, pady=10)

        # Add yes/no drop down for isPublic
        yesno = ["Yes", "No"]
        public = Label(frame, text="Public:* ")
        public.grid(row=7, column=0, sticky='w')
        self.publicVar = StringVar()
        publicMenu = OptionMenu(frame, self.publicVar, "Yes", *yesno)
        publicMenu.grid(row=7, column=1, padx=20, pady=10)

        # Add yes/no drop down for isCommercial
        commercial = Label(frame, text="Commercial:* ")
        commercial.grid(row=8, column=0, sticky='w')
        self.commVar = StringVar()
        commMenu = OptionMenu(frame, self.commVar, "Yes", *yesno)
        commMenu.grid(row=8, column=1, padx=20, pady=10)

        # Buttons
        button1 = Button(frame, text="Add Property", command=self.addPropertyOnClick)
        button1.grid(row=9, column=0, sticky='w')
        #TODO: REGISTER COMPLETE PAGE
        button2 = Button(frame, text="Cancel", command=lambda: self.controller.show_frame(ownerFunctionality))
        button2.grid(row=9, column=1, sticky='w')

    def addPropertyOnClick(self):
        msg = StringVar()

        # Make sure every field is filled in
        if len(self.name.get()) == 0 or len(self.street.get()) == 0 or len(self.city.get()) == 0 or len(self.zipcode.get()) == 0 or len(self.acres.get()) == 0:
            messagebox.showerror("Error", "All fields are required")
        else:
            # Make sure property name is unique
            propNameExists = DBManager.checkPropertyName(self, self.name.get())
            if not propNameExists:
                # Add property

                # Change public and commercial to 1 or 0
                if self.publicVar.get() == 'Yes':
                    public = 1
                else:
                    public = 0

                if self.commVar.get() == 'Yes':
                    comm = 1
                else:
                    comm = 0

                addProp = DBManager.addProperty(self, self.name.get(), self.street.get(), self.city.get(),
                                                self.zipcode.get(), public, comm, self.propTypeVar.get(),
                                                self.controller.username, self.acres.get())

                # Get property ID for the new property
                propID = DBManager.getPropertyID(self, self.name.get())

                # Add crop to Has table
                crop = self.cropVar.get()
                cropAdded = DBManager.addItem(self, propID, crop)

                # If property is a farm then add animal also
                if self.propTypeVar.get() == 'Farm':
                    animal = self.animalVar.get()
                    animalAdded = DBManager.addItem(self, propID, animal)

                    # Make sure everything was successful (including animal)
                    if addProp and cropAdded and animalAdded:
                        # Now add user to User table
                        messagebox.showerror("Property added", "Property was successfully added!")
                        self.controller.show_frame(ownerFunctionality)
                    else:
                        messagebox.showerror("Error", "Something went wrong")
                else:
                    # Make sure everything was successful
                    if addProp and cropAdded:
                        # Now add user to User table
                        messagebox.showerror("Property added", "Property was successfully added!")
                        self.controller.show_frame(ownerFunctionality)
                    else:
                        messagebox.showerror("Error", "Something went wrong")
            else:
                messagebox.showerror("Error", "All fields are required")


    def propertyTypeChange(self, value):
        if value == 'Farm':
            # Farm GUI
            self.cropMenu.destroy()

            # Get list of approved, fruits, nuts, veggies, and flowers
            fruits = DBManager.getApprovedFruits(self)
            nuts = DBManager.getApprovedNuts(self)
            veggies = DBManager.getApprovedVegetables(self)
            flowers = DBManager.getApprovedFlowers(self)
            crops = fruits + nuts + veggies + flowers

            # Get approved animals
            self.animal = Label(self.frame, text="Animal:* ")
            self.animal.grid(row=6, column=2, padx=20, pady=10)

            animals = DBManager.getApprovedAnimals(self)
            self.animalVar = StringVar()
            self.animalMenu = OptionMenu(self.frame, self.animalVar, *animals)
            self.animalMenu.grid(row=6, column=3, padx=20, pady=10)

        elif value == 'Garden':
            # Garden
            self.cropMenu.destroy()
            self.animal.destroy()
            self.animalMenu.destroy()

            # Get approved vegetables and flowers from DB
            veggies = DBManager.getApprovedVegetables(self)
            flowers = DBManager.getApprovedFlowers(self)
            crops = veggies + flowers

        else:
            # Orchard
            self.cropMenu.destroy()
            self.animal.destroy()
            self.animalMenu.destroy()

            # Get approved vegetables and flowers from DB
            fruits = DBManager.getApprovedFruits(self)
            nuts = DBManager.getApprovedNuts(self)
            crops = fruits + nuts

        # Recreate drop down menu with new approved crops
        self.cropVar = StringVar()
        self.cropMenu = OptionMenu(self.frame, self.cropVar, *crops)
        self.cropMenu.grid(row=6, column=1, padx=20, pady=10)

        return value


class visitorPropertyPage(Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        global prop
        print(prop)
        Frame.__init__(self, parent)

        #[(0, 'Atwood Street Garden', 1.0, 0, 1, 'Atwood Street SW', 'Atlanta', 30308, 'GARDEN', 'gardenowner', 'admin1')]
        
        label = Label(self, text=str(prop[0][1]), font =LARGE_FONT)
        label.pack()
        n= "Name: "+str(prop[0][1])
        name = Label(self, text=n)
        name.pack()
        o= "Owner: "+prop[0][9]
        owner = Label(self, text=o)
        owner.pack()
        o = "Owner Email: "
        ownerEmail = Label(self, text=o)
        ownerEmail.pack()
        v = "Visits: "
        visits = Label(self, text=v)
        visits.pack()
        a = "Address: "+prop[0][5]
        address = Label(self, text=a)
        address.pack()
        c = 'City: '+ prop[0][6]
        city = Label(self,text=c)
        city.pack()
        z = "Zip : "+str(prop[0][7])
        zipcode = Label(self, text=z)
        zipcode.pack()
        s = "Size (acres): " + str(prop[0][2])
        size = Label(self, text=s)
        size.pack()
        r = "Avg Rating: "
        rating = Label(self, text=r)
        rating.pack()
        tp = "Type: "+prop[0][8]
        typeProp = Label(self, text=tp)
        typeProp.pack()
        p = "Public: " + str(prop[0][4])
        public = Label(self, text=p)
        public.pack()
        c = "Commercial: "+ str(prop[0][3])
        commercial = Label(self, text=c)
        commercial.pack()
        i = "ID: "+ str(prop[0][0])
        idnum = Label(self, text="ID: ")
        idnum.pack()
        c = "Crops: "
        crops = Label(self, text=c)
        crops.pack()

        types = {'1', '2', '3', '4', '5'}
        search = StringVar()
        rating = OptionMenu(self, search, *types)
        rating.pack()

        logvisit = Button(self, text="Log Visit", command=lambda: messagebox.showinfo("Title", "Visit Logged!"))
        
        logvisit.pack()
        back = Button(self, text="Back", command=lambda: self.controller.show_frame(visitorView))
        back.pack()


class propertyDetails(Frame):
    def __init__(self, parent, controller):
        self.controller = controller
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
        back = Button(self, text="Back", command=lambda: self.controller.show_frame(visitorView))
        back.pack()

class otherOwnerProperties(Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        Frame.__init__(self, parent)
        label = Label(self, text="All Other Valid Properties", font =LARGE_FONT)
        label.grid(row=0, column=0)


        frame = Frame(self)

        table = Treeview(frame)
        self.frame = frame
        self.table = table
        self.table.bind("<Button-1>", self.onClick)

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
        
        types = {'Name', 'City', 'Public', 'Visits','Avg Rating'}
        
        search = StringVar()
        search.set(' ')
        search_menu = OptionMenu(frame, search, 'Name', *types)
        search_menu.grid(row=3, column=0, sticky='w', padx=50, pady=10)
        self.removed = []
        term = Entry(self, text="Search Term")
        term.grid(row=3, column = 0, sticky='w', padx=50, pady=10)

        self.term = term
        self.search = search
        searchprop = Button(self, text="Search Properties", command=self.searchfunc)
        searchprop.grid(row=4, column=0, sticky='w', padx=50, pady=10)

        viewprop = Button(self, text="View Property Details", command=lambda: self.controller.show_frame(propertyDetails))
        viewprop.grid(row=3, column=0, padx=50, pady=10)
        ## TO DO: BACK MUST GO TO THE RIGHT PAGE
        back = Button(self, text="Back", command=lambda: self.controller.show_frame(loginPage))
        back.grid(row=4, column=0, sticky='e', padx=50, pady=10)

    def searchfunc(self, item=''):
        children = self.frame.treeview.get_children(item)
        if(self.term.get() ==  ''):
            for i in range(len(self.removed)):
                self.frame.treeview.insert('', 'end', text=self.removed[i][0], values=(self.removed[i][1], self.removed[i][2], self.removed[i][3], self.removed[i][4], self.removed[i][5], self.removed[i][6], self.removed[i][7], self.removed[i][8], self.removed[i][9], self.removed[i][10]))
            self.removed = []
        else:
            index = 0
            if (self.search.get() == "Name"):
                index = 0
            elif (self.search.get() == "City"):
                index = 2
            elif (self.search.get() == "Public"):
                index = 5
            elif (self.search.get() == "Visits"):
                index = 9
            elif (self.search.get() == "Avg Rating"):
                index = 10

            for child in children:
                temp1 = []
                text = self.frame.treeview.item(child, 'text')
                temp1.append(text)
                for x in self.table.item(child, "values"):
                        temp1.append(x)
                #print(self.table.item(child, "values"))
                if (temp1[index] == self.term.get()):
                    self.frame.treeview.selection_set(child)
                else:
                    if ('-' in self.term.get()):
                        tempterm = self.term.get().split("-")
                        # print(float(temp1[index]))
                        # print(float(tempterm[0]))
                        if (float(temp1[index]) >= float(tempterm[0]) and float(temp1[index]) <= float(tempterm[1])):
                            self.frame.treeview.selection_set(child)
                        else:
                            res = self.searchfunc(child)

                            self.removed.append(temp1)
                            self.frame.treeview.delete(child)
                            if res:
                                break

                    else:
                        res = self.searchfunc(child)

                        self.removed.append(temp1)
                        self.frame.treeview.delete(child)
                        if res:
                            break

    def onClick(self, event):
        item = self.table.identify_column(event.x)

        if self.table.identify_region(event.x, event.y) == "heading" and item in ['#0', '#2', '#6', '#9', '#10']:

            children = self.frame.treeview.get_children('')
            temp = []
            for child in children:
                temp1 = []
                text = self.frame.treeview.item(child, 'text')
                temp1.append(text)
                for x in self.table.item(child, "values"):
                    temp1.append(x)
                temp.append(temp1)
                self.frame.treeview.delete(child)

            if item == '#0':
                #Name

                temp.sort(key=lambda x: x[0])
                for i in range(len(temp)):
                    self.frame.treeview.insert('', 'end', text=temp[i][0], values=(temp[i][1], temp[i][2], temp[i][3], temp[i][4], temp[i][5], temp[i][6], temp[i][7], temp[i][8], temp[i][9], temp[i][10]))


            if item == '#2':
                #City

                temp.sort(key=lambda x: x[2])
                for i in range(len(temp)):
                    self.frame.treeview.insert('', 'end', text=temp[i][0], values=(temp[i][1], temp[i][2], temp[i][3], temp[i][4], temp[i][5], temp[i][6], temp[i][7], temp[i][8], temp[i][9], temp[i][10]))

            if item == '#6':
                #Type

                temp.sort(key=lambda x: x[6])
                for i in range(len(temp)):
                    self.frame.treeview.insert('', 'end', text=temp[i][0], values=(temp[i][1], temp[i][2], temp[i][3], temp[i][4], temp[i][5], temp[i][6], temp[i][7], temp[i][8], temp[i][9], temp[i][10]))

            if item == '#9':
                #Visits

                temp.sort(key=lambda x: x[9])
                for i in range(len(temp)):
                    self.frame.treeview.insert('', 'end', text=temp[i][0], values=(temp[i][1], temp[i][2], temp[i][3], temp[i][4], temp[i][5], temp[i][6], temp[i][7], temp[i][8], temp[i][9], temp[i][10]))

            if item == '#10':
                #Avg Rating

                temp.sort(key=lambda x: x[10])
                for i in range(len(temp)):
                    self.frame.treeview.insert('', 'end', text=temp[i][0], values=(temp[i][1], temp[i][2], temp[i][3], temp[i][4], temp[i][5], temp[i][6], temp[i][7], temp[i][8], temp[i][9], temp[i][10]))

class ownerFunctionality(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        frame = Frame(self)

        # Get owners username
        self.controller = controller
        username = self.controller.username
        welcomemsg = "Welcome " + username

        # Get a list with all of the owners properties
        propList = DBManager.getOwnerProperties(self, username)
        if propList is None:
            propList = []

        label = Label(self, text=welcomemsg, font=LARGE_FONT)
        label.grid(row=0, column=0)

        props = Label(self, text="Your properties:")
        props.grid(row=1, column=0)

        # Create owner property tables
        table = Treeview(frame)
        self.frame = frame
        self.table = table
        self.table.bind("<Button-1>", self.onClick)
        table['columns'] = ('Name', 'Size', 'Commercial', 'Public', 'Street', 'City', 'ZIP', 'Type', 'Owner',
                            'Approved')

        table.column('#0', anchor='w')
        table.heading('#0', text='ID', anchor='w')

        table.column('Name', anchor='center', width=100)
        table.heading('Name', text='Name')

        table.column('Size', anchor='center', width=100)
        table.heading('Size', text='Size')

        table.column('Commercial', anchor='center', width=100)
        table.heading('Commercial', text='Commercial')

        table.column('Public', anchor='center', width=100)
        table.heading('Public', text='Public')

        table.column('Street', anchor='center', width=100)
        table.heading('Street', text='Street')

        table.column('City', anchor='center', width=100)
        table.heading('City', text='City')

        table.column('ZIP', anchor='center', width=100)
        table.heading('ZIP', text='ZIP')

        table.column('Type', anchor='center', width=100)
        table.heading('Type', text='Type')

        table.column('Owner', anchor='center', width=100)
        table.heading('Owner', text='Owner')

        table.column('Approved', anchor='center', width=100)
        table.heading('Approved', text='Approved')

        table.grid(sticky=(N,S,W,E))
        frame.treeview = table
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        frame.grid(sticky=(N,S,W,E))
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        for prop in propList:
            id = prop[0]
            name = prop[1]
            size = prop[2]
            comm = prop[3]
            pub = prop[4]
            st = prop[5]
            city = prop[6]
            zip = prop[7]
            type = prop[8]
            owner = prop[9]
            appr = prop[10]

            # Change tinyint values into true/false for commercial and public
            if comm == 1:
                commercial = True
            else:
                commercial = False

            if pub == 1:
                public = True
            else:
                public = False

            # Change approved value from null or 1 to true/false
            if appr is None:
                approved = False
            else:
                approved = True

            newProp = [name, size, commercial, public, st, city, zip, type, owner, approved]

            frame.treeview.insert('', 'end', text=id, values=newProp)

        types = {'Name', 'City', 'Type', 'Visits', 'Avg Rating'}
        
        search = StringVar()
        search.set(' ')
        search_menu = OptionMenu(frame, search, 'Name', *types)
        search_menu.grid(row=3, column=0, sticky='w', padx=50, pady=10)
        self.search = search
        self.removed = []
        term = Entry(self, text="Search Term")
        term.grid(row=3, column = 0, sticky='w', padx=50, pady=10)
        self.term = term

        searchprop = Button(self, text="Search Properties", command=self.searchfunc)
        searchprop.grid(row=4, column=0, sticky='w', padx=50, pady=10)

        manage = Button(self, text="Manage Property", command=self.manageProp)
        manage.grid(row=3, column=0, padx=50, pady=10)

        addP = Button(self, text="Add Property", command=lambda: self.controller.show_frame(addNewProperty))
        addP.grid(row=4, column=0, padx=50, pady=10)

        logout = Button(self, text="Log Out", command=lambda: self.controller.show_frame(loginPage))
        logout.grid(row=4, column=0, sticky='e', padx=50, pady=10)

        viewOthers = Button(self, text="View Other Properties", command=lambda: self.controller.show_frame(otherOwnerProperties))
        viewOthers.grid(row=3, column=0, sticky='e', padx=50, pady=10)

    def searchfunc(self, item=''):
        children = self.frame.treeview.get_children(item)
        if(self.term.get() ==  ''):
            for i in range(len(self.removed)):
                self.frame.treeview.insert('', 'end', text=self.removed[i][0], values=(self.removed[i][1], self.removed[i][2], self.removed[i][3], self.removed[i][4], self.removed[i][5], self.removed[i][6], self.removed[i][7], self.removed[i][8], self.removed[i][9], self.removed[i][10]))
            self.removed = []
        else:
            index = 0
            if (self.search.get() == "Name"):
                index = 0
            elif (self.search.get() == "City"):
                index = 2
            elif (self.search.get() == "Type"):
                index = 5
            elif (self.search.get() == "Visits"):
                index = 9
            elif (self.search.get() == "Avg Rating"):
                index = 10

            for child in children:
                temp1 = []
                text = self.frame.treeview.item(child, 'text')
                temp1.append(text)
                for x in self.table.item(child, "values"):
                        temp1.append(x)
                #print(self.table.item(child, "values"))
                if (temp1[index] == self.term.get()):
                    self.frame.treeview.selection_set(child)
                else:
                    if ('-' in self.term.get()):
                        tempterm = self.term.get().split("-")
                        # print(float(temp1[index]))
                        # print(float(tempterm[0]))
                        if (float(temp1[index]) >= float(tempterm[0]) and float(temp1[index]) <= float(tempterm[1])):
                            self.frame.treeview.selection_set(child)
                        else:
                            res = self.searchfunc(child)

                            self.removed.append(temp1)
                            self.frame.treeview.delete(child)
                            if res:
                                break

                    else:
                        res = self.searchfunc(child)

                        self.removed.append(temp1)
                        self.frame.treeview.delete(child)
                        if res:
                            break

    def onClick(self, event):
        item = self.table.identify_column(event.x)
        self.element = self.table.identify_row(event.y)
        self.element = self.table.item(self.element, "text")

        if self.table.identify_region(event.x, event.y) == "heading" and item in ['#0', '#2', '#5', '#9', '#10']:

            children = self.frame.treeview.get_children('')
            temp = []
            for child in children:
                temp1 = []
                text = self.frame.treeview.item(child, 'text')
                temp1.append(text)
                for x in self.table.item(child, "values"):
                    temp1.append(x)
                temp.append(temp1)
                self.frame.treeview.delete(child)

            if item == '#0':
                #Name

                temp.sort(key=lambda x: x[0])
                for i in range(len(temp)):
                    self.frame.treeview.insert('', 'end', text=temp[i][0], values=(temp[i][1], temp[i][2], temp[i][3], temp[i][4], temp[i][5], temp[i][6], temp[i][7], temp[i][8], temp[i][9], temp[i][10]))


            if item == '#2':
                #City

                temp.sort(key=lambda x: x[2])
                for i in range(len(temp)):
                    self.frame.treeview.insert('', 'end', text=temp[i][0], values=(temp[i][1], temp[i][2], temp[i][3], temp[i][4], temp[i][5], temp[i][6], temp[i][7], temp[i][8], temp[i][9], temp[i][10]))

            if item == '#5':
                #Type

                temp.sort(key=lambda x: x[5])
                for i in range(len(temp)):
                    self.frame.treeview.insert('', 'end', text=temp[i][0], values=(temp[i][1], temp[i][2], temp[i][3], temp[i][4], temp[i][5], temp[i][6], temp[i][7], temp[i][8], temp[i][9], temp[i][10]))

            if item == '#9':
                #Visits

                temp.sort(key=lambda x: x[9])
                for i in range(len(temp)):
                    self.frame.treeview.insert('', 'end', text=temp[i][0], values=(temp[i][1], temp[i][2], temp[i][3], temp[i][4], temp[i][5], temp[i][6], temp[i][7], temp[i][8], temp[i][9], temp[i][10]))

            if item == '#10':
                #Avg Rating

                temp.sort(key=lambda x: x[10])
                for i in range(len(temp)):
                    self.frame.treeview.insert('', 'end', text=temp[i][0], values=(temp[i][1], temp[i][2], temp[i][3], temp[i][4], temp[i][5], temp[i][6], temp[i][7], temp[i][8], temp[i][9], temp[i][10]))


    def manageProp(self):
        global prop
        
        prop = DBManager.getPropertyDetails(self, propID = self.element)
        #print("manageprop", self.prop)
        self.controller.show_frame(propertyManagement)

class propertyManagement(Frame):
    def __init__(self, parent, controller):
        #self.prop = prop
        #print(self.prop)
        global prop
        
        print(prop)
        self.controller = controller
        Frame.__init__(self, parent)
        
        label = Label(self, text="Manage", font =LARGE_FONT)
        label.pack(pady=10,padx=10)

        frame = Frame(self)
        frame.pack(padx=5, pady=20, side=LEFT)
        self.frame = frame

        name = Label(frame, text="Name: ")
        name.grid(row=0, column=0, sticky='w')
        self.name = Entry(frame, background='white', width=24)
        self.name.insert(0, prop[0][1])
        self.name.grid(row=0, column=1, sticky='w')
        self.name.focus_set()

        typ = Label(frame, text="Type: " + prop[0][8])
        typ.grid(row=0, column=2, sticky='w')
        
        street = Label(frame, text="Address: ")
        street.grid(row=1, column=0, sticky='w')
        self.street = Entry(frame, background='white', width=24)
        self.street.insert(0, prop[0][5])
        self.street.grid(row=1, column=1, sticky='w')
        self.street.focus_set()

        pub = Label(frame, text="Public: ")
        pub.grid(row=1, column=2, sticky='w')

        # Rest of GUI depends on property type selected
        pubtypes = {'True', 'False'}   # Dictionary holding different prop types
        
        pubTypeVar = StringVar()
        pubTypeVar.set('False')   # Set garden as the default prop type
        temp5 = 'False'
        if prop[0][4] == 1:
            temp5 = 'True'
        pubType_menu = OptionMenu(frame, pubTypeVar, temp5, *pubtypes)
        pubType_menu.grid(row=1, column=3, padx=5, pady=10)

        city = Label(frame, text="City: ")
        city.grid(row=2, column=0, sticky='w')
        self.city = Entry(frame, background='white', width=24)
        self.city.insert(0, prop[0][6])
        self.city.grid(row=2, column=1, sticky='w')
        self.city.focus_set()

        com = Label(frame, text="Commercial: ")
        com.grid(row=2, column=2, sticky='w')

        comtypes = {'True', 'False'}   # Dictionary holding different prop types
        temp6 = 'False'
        if prop[0][3] == 1:
            temp6 = 'True'
        comTypeVar = StringVar()
        comTypeVar.set('False')   # Set garden as the default prop type
        comType_menu = OptionMenu(frame, comTypeVar, temp6, *comtypes)
        comType_menu.grid(row=2, column=3, padx=5, pady=10)

        zipcode = Label(frame, text="Zip: ")
        zipcode.grid(row=3, column=0, sticky='w')
        self.zipcode = Entry(frame, background='white', width=24)
        self.zipcode.insert(0, prop[0][7])
        self.zipcode.grid(row=3, column=1, sticky='w')
        self.zipcode.focus_set()

        ID = Label(frame, text="ID: " + str(prop[0][0]))
        ID.grid(row=3, column=2, sticky='w')

        acres = Label(frame, text="Size(Acres): ")
        acres.grid(row=4, column=0, sticky='w')
        self.acres = Entry(frame, background='white', width=24)
        self.acres.insert(0, prop[0][2])
        self.acres.grid(row=4, column=1, sticky='w')
        self.acres.focus_set()

        cropType = Label(frame, text="Add new crop: ")
        cropType.grid(row=5, column=0, sticky='w')
        # Rest of GUI depends on property type selected
        croptypes = {'Fruit', 'Nut', 'Flower', 'Vegetable'}   # Dictionary holding different prop types
        
        self.cropTypeVar = StringVar()
        self.cropTypeVar.set(' ')   # Set garden as the default prop type

        cropType_menu = OptionMenu(frame, self.cropTypeVar, 'Fruit', *croptypes)
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

        newcrops = Label(self.frame, text="New crop type: ")
        newcrops.grid(row=7, column=2, sticky='w')

        newcropType = Label(frame, text="New crop type: ")
        newcropType.grid(row=7, column=2, sticky='w')
        # Rest of GUI depends on property type selected
        newcroptypes = {'Fruit', 'Nut', 'Flower', 'Vegetable'}   # Dictionary holding different prop types
        
        newcropTypeVar = StringVar()
        newcropTypeVar.set(' ')   # Set garden as the default prop type
        newcropType_menu = OptionMenu(frame, newcropTypeVar, 'Fruit', *newcroptypes)
        newcropType_menu.grid(row=7, column=3, padx=5, pady=10)
        self.newcropTypeVar = newcropTypeVar
        self.newcropstypes = set()
        button2 = Button(frame, text="Submit Request", command=lambda: self.controller.show_frame(loginPage))
        button2.grid(row=8, column=1, sticky='w')

        button3 = Button(frame, text="Save Changes", command=lambda: self.controller.show_frame(loginPage))
        button3.grid(row=9, column=1, sticky='w')

        button4 = Button(frame, text="Delete Property", command=lambda: self.controller.show_frame(loginPage))
        button4.grid(row=10, column=0, sticky='w')

        button5 = Button(frame, text="Back (Don't Save)", command=lambda: self.controller.show_frame(loginPage))
        button5.grid(row=10, column=1, sticky='w')

    def addCrop(self):
        # global buttonnum
        # buttonnum += 1
        # butts = []
        # label = "Button " + str(buttonnum)
        # for i in range(buttonnum):
        #     butts.append(Button(self.frame, text=str(self.cropTypeVar.get()) + ' [X]', command=lambda: butts[i].destroy()))
        #     butts[i].grid(row = buttonnum + 4, column = 4)
        # self.butts = butts
        # print(butts)
    
        # Rest of GUI depends on property type selected
       # Dictionary holding different prop types
        self.newcropstypes.add(self.cropTypeVar.get())
        newcropsTypeVar = StringVar()
        newcropsTypeVar.set(' ')   # Set garden as the default prop type
        newcropsType_menu = OptionMenu(self.frame, newcropsTypeVar, self.cropTypeVar.get(), *self.newcropstypes)
        newcropsType_menu.grid(row=5, column=4, padx=5, pady=10)


app = Atlanta()
app.mainloop()