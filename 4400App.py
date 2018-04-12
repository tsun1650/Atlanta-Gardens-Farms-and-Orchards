
#import tkinter as tk
from tkinter import *
LARGE_FONT= ("Verdana", 12)


class Atlanta(Tk):

    def __init__(self, *args, **kwargs):
        
        Tk.__init__(self, *args, **kwargs)
        container = Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (loginPage, visitorRegistration, ownerRegistration, adminFunctions):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(loginPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class loginPage(Frame):
     def __init__(self, parent, controller):
        Frame.__init__(self,parent)
        label = Label(self, text="Login Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)


        f = Frame(self)
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

        button0 = Button(f, text="Login", command=lambda: controller.show_frame(loginPage))
        button0.grid(row=2, column=1, sticky='w')
        #button1 = Button(f, text="New Owner Registration", command=lambda: controller.show_frame(ownerFunctions))
        #button1.grid(row=3, column=0, sticky='w')
        button1 = Button(f, text="New Owner Registration", command=lambda: controller.show_frame(adminFunctions))
        button1.grid(row=3, column=0, sticky='w')

        button2 = Button(f, text="New Visitor Registration", command=lambda: controller.show_frame(visitorRegistration))
        button2.grid(row=3, column=1, sticky='w')

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
        button2 = Button(dialog_frame, text="Register Visitor", command=lambda: controller.show_frame(loginPage))
        button2.grid(row=4, column=1, sticky='w')

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
        button2 = Button(frame, text="Register Owner", command=lambda: controller.show_frame(loginPage))
        button2.grid(row=11, column=1, sticky='w')


class adminFunctions(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Admin Functionality", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        visListB = Button(self, text="View Visitor List", command=lambda: controller.show_frame(loginPage))
        visListB.pack(fill = X)

        ownListB = Button(self, text="View Owner List", command=lambda: controller.show_frame(loginPage))
        ownListB.pack(fill = X)

        conPropB = Button(self, text="View Confirmed Properties", command=lambda: controller.show_frame(loginPage))       
        conPropB.pack(fill = X)

        unconPropB = Button(self, text="View Unconfirmed Properties", command=lambda: controller.show_frame(loginPage))
        unconPropB.pack(fill =X)

        approvedB = Button(self, text="View Approved Animals and Crops", command=lambda: controller.show_frame(loginPage))
        approvedB.pack(fill = X)

        pendingB = Button(self, text="View Pending Animals and Crops", command=lambda: controller.show_frame(loginPage))
        pendingB.pack(fill =X)

        logoutB = Button(self, text="Logout", command=lambda: controller.show_frame(loginPage))
        logoutB.pack(fill =X)








app = Atlanta()
app.mainloop()