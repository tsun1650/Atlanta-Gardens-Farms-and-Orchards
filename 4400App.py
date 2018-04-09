from tkinter import *


class visitorRegistration:
    def __init__(self, parent=None):

        self.parent = parent

        self.make_window()

    def make_window(self):
        Label(text='New Visitor Registration').grid(row = 0, padx = 10, pady = 10)

        email = Label(visitorRegistrationPage, text="Email*: ")
        email.grid(row = 1, column = 0, padx = 20, pady = 10)

        username = Label(visitorRegistrationPage, text="Username*: ")
        username.grid(row = 2, column = 0, padx = 20, pady = 10)

        password = Label(visitorRegistrationPage, text="Password*: ")
        password.grid(row = 3, column = 0, padx = 20, pady = 10)

        confirmPassword = Label(visitorRegistrationPage, text="Confirm Password*: ")
        confirmPassword.grid(row = 4, column = 0, padx = 20, pady = 10)

        email_text=StringVar()
        entry1 = Entry(visitorRegistrationPage, textvariable=email_text)
        entry1.grid(row = 1, column = 1, padx = 20, pady = 10)

        username_text=StringVar()
        entry2 = Entry(visitorRegistrationPage, textvariable=username_text)
        entry2.grid(row = 2, column = 1, padx = 20, pady = 10)

        password_text=StringVar()
        entry3 = Entry(visitorRegistrationPage, textvariable=password_text)
        entry3.grid(row = 3, column = 1, padx = 20, pady = 10)

        confirmPassword_text=StringVar()
        entry4 = Entry(visitorRegistrationPage, textvariable=confirmPassword_text)
        entry4.grid(row = 4, column = 1, padx = 20, pady = 10)

        b1 = Button(visitorRegistrationPage, text = "Register Visitor", width = 15)
        b1.grid(row = 5, column = 0, padx = 20, pady = 10)

        b2 = Button(visitorRegistrationPage, text = "Cancel", width = 15)
        b2.grid(row = 5, column = 1, padx = 20, pady = 10)


visitorRegistrationPage=Tk()
visitorRegistrationPage.title("New Visitor Registration")
visitorRegistration = visitorRegistration(visitorRegistrationPage)
visitorRegistrationPage.mainloop()


class OwnerRegistration:
    def __init__(self, parent=None):
        self.parent = parent
        self.make_window()

    @staticmethod
    def make_window(self):
        Label(text='New Owner Registration').grid(row=0, padx=10, pady=10)

        # Define textbox labels
        email = Label(ownerRegistrationPage, text="Email:* ")
        email.grid(row=1, column=0, padx=20, pady=10)

        username = Label(ownerRegistrationPage, text="Username:* ")
        username.grid(row=2, column=0, padx=20, pady=10)

        password = Label(ownerRegistrationPage, text="Password:* ")
        password.grid(row=3, column=0, padx=20, pady=10)

        confirmPassword = Label(ownerRegistrationPage, text="Confirm Password:* ")
        confirmPassword.grid(row=4, column=0, padx=20, pady=10)

        propName = Label(ownerRegistrationPage, text="Property Name:* ")
        propName.grid(row=5, column=0, padx=20, pady=10)

        propAddress = Label(ownerRegistrationPage, text="Street Address:* ")
        propAddress.grid(row=6, column=0, padx=20, pady=10)

        propCity = Label(ownerRegistrationPage, text="City:* ")
        propCity.grid(row=7, column=0, padx=20, pady=10)

        propZip = Label(ownerRegistrationPage, text="Zip:* ")
        propZip.grid(row=8, column=0, padx=20, pady=10)

        propAcres = Label(ownerRegistrationPage, text="Acres:* ")
        propAcres.grid(row=9, column=0, padx=20, pady=10)

        propType = Label(ownerRegistrationPage, text="Property Type:* ")
        propType.grid(row=10, column=0, padx=20, pady=10)

        # User input section
        email_text = StringVar()
        entry1 = Entry(ownerRegistrationPage, textvariable=email_text)
        entry1.grid(row=1, column=1, padx=20, pady=10)

        username_text = StringVar()
        entry2 = Entry(ownerRegistrationPage, textvariable=username_text)
        entry2.grid(row=2, column=1, padx=20, pady=10)

        password_text = StringVar()
        entry3 = Entry(ownerRegistrationPage, textvariable=password_text)
        entry3.grid(row=3, column=1, padx=20, pady=10)

        confirmPassword_text = StringVar()
        entry4 = Entry(ownerRegistrationPage, textvariable=confirmPassword_text)
        entry4.grid(row=4, column=1, padx=20, pady=10)

        propName_text = StringVar()
        entry5 = Entry(ownerRegistrationPage, textvariable=propName_text)
        entry5.grid(row=5, column=1, padx=20, pady=10)

        propAddress_text = StringVar()
        entry6 = Entry(ownerRegistrationPage, textvariable=propAddress_text)
        entry6.grid(row=6, column=1, padx=20, pady=10)

        propCity_text = StringVar()
        entry7 = Entry(ownerRegistrationPage, textvariable=propCity_text)
        entry7.grid(row=7, column=1, padx=20, pady=10)

        propZip_text = StringVar()
        entry8 = Entry(ownerRegistrationPage, textvariable=propZip_text)
        entry8.grid(row=8, column=1, padx=20, pady=10)

        propAcres_text = StringVar()
        entry9 = Entry(ownerRegistrationPage, textvariable=propAcres_text)
        entry9.grid(row=9, column=1, padx=20, pady=10)

        # Rest of GUI depends on property type selected
        types = {'Garden', 'Farm', 'Orchard'}   # Dictionary holding different prop types

        propTypeVar = StringVar()
        propTypeVar.set('Garden')   # Set garden as the default prop type
        propType_menu = OptionMenu(ownerRegistrationPage, propTypeVar, *types)
        propType_menu.grid(row=10, column=1, padx=20, pady=10)

        if propTypeVar.get() == 'Garden':
            # Garden GUI
            # TODO: create a dictionary with approved vegetables and flowers (from DB)
            crop = Label(ownerRegistrationPage, text="Crop:* ")
            crop.grid(row=11, column=0, padx=20, pady=10)

            # TODO: replace entry box with drop down populated by crop dictionary
            cropTxt = StringVar()
            entry10 = Entry(ownerRegistrationPage, textvariable=cropTxt)
            entry10.grid(row=11, column=1, padx=20, pady=10)
        elif propTypeVar.get() == 'Farm':
            # Farm GUI
            # TODO: create a dictionary with approved fruits, nuts, vegetables, and flowers (from DB)
            crop = Label(ownerRegistrationPage, text="Crop:* ")
            crop.grid(row=11, column=0, padx=20, pady=10)

            # TODO: replace entry box with drop down populated by crop dictionary
            cropTxt = StringVar()
            entry10 = Entry(ownerRegistrationPage, textvariable=cropTxt)
            entry10.grid(row=11, column=1, padx=20, pady=10)

            # TODO: Do same thing with animals as crops ^
            animal = Label(ownerRegistrationPage, text="Animal:* ")
            animal.grid(row=12, column=0, padx=20, pady=10)
            animalTxt = StringVar()
            entry11 = Entry(ownerRegistrationPage, textvariable=animalTxt)
            entry11.grid(row=11, column=1, padx=20, pady=10)
        else:
            # Orchard GUI
            # TODO: create a dictionary with approved fruits and nuts (from DB)
            crop = Label(ownerRegistrationPage, text="Crop:* ")
            crop.grid(row=11, column=0, padx=20, pady=10)

            # TODO: replace entry box with drop down populated by crop dictionary
            cropTxt = StringVar()
            entry10 = Entry(ownerRegistrationPage, textvariable=cropTxt)
            entry10.grid(row=11, column=1, padx=20, pady=10)

        # Buttons
        registerBtn = Button(ownerRegistrationPage, text="Register Owner", width=15)
        registerBtn.grid(row=13, column=0, padx=20, pady=10)

        cancelBtn = Button(ownerRegistrationPage, text="Cancel", width=15)
        cancelBtn.grid(row=13, column=10, padx=20, pady=10)


ownerRegistrationPage = Tk()
ownerRegistrationPage.title("New Owner Registration")
ownerRegistration = OwnerRegistration(ownerRegistrationPage)
ownerRegistrationPage.mainloop()
