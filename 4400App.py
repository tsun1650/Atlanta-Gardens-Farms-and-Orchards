
import tkinter as tk

LARGE_FONT= ("Verdana", 12)


class Atlanta(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (loginPage, visitorRegistration, ownerRegistration):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(loginPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class loginPage(tk.Frame):
     def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Login Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)


        f = tk.Frame(self)
        f.pack(padx=5, pady=20, side=tk.LEFT)
        
        email = tk.Label(f, text="Email: ")
        email.grid(row=0, column=0, sticky='w')
        email.focus_set()

        self.emailEntry = tk.Entry(f, background='white', width=24)
        self.emailEntry.grid(row=0, column=1, sticky='w')
        self.emailEntry.focus_set()

        password = tk.Label(f, text="Password: ")
        password.grid(row=1, column=0, sticky='w')
        password.focus_set()

        self.passwordEntry = tk.Entry(f, background='white', width=24)
        self.passwordEntry.grid(row=1, column=1, sticky='w')

        button0 = tk.Button(f, text="Login", command=lambda: controller.show_frame(loginPage))
        button0.grid(row=2, column=1, sticky='w')

        button1 = tk.Button(f, text="New Owner Registration", command=lambda: controller.show_frame(ownerRegistration))
        button1.grid(row=3, column=0, sticky='w')

        button2 = tk.Button(f, text="New Visitor Registration", command=lambda: controller.show_frame(visitorRegistration))
        button2.grid(row=3, column=1, sticky='w')

class visitorRegistration(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="New Visitor Registration", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        
        #email.grid(row = 1, column = 0, padx = 20, pady = 10)
        dialog_frame = tk.Frame(self)
        dialog_frame.pack(padx=5, pady=20, side=tk.LEFT)
        
        email = tk.Label(dialog_frame, text="Email*: ")
        email.grid(row=0, column=0, sticky='w')
        self.email = tk.Entry(dialog_frame, background='white', width=24)
        self.email.grid(row=0, column=1, sticky='w')
        self.email.focus_set()
        
        username = tk.Label(dialog_frame, text="Username:* ")
        username.grid(row=1, column=0, sticky='w')
        self.username = tk.Entry(dialog_frame, background='white', width=24)
        self.username.grid(row=1, column=1, sticky='w')
        self.username.focus_set()

        password = tk.Label(dialog_frame, text="Password:* ")
        password.grid(row=2, column=0, sticky='w')
        self.password = tk.Entry(dialog_frame, background='white', width=24)
        self.password.grid(row=2, column=1, sticky='w')
        self.password.focus_set()

        confirmPassword = tk.Label(dialog_frame, text="Confirm Password:* ")
        confirmPassword.grid(row=3, column=0, sticky='w')
        self.confirmPassword = tk.Entry(dialog_frame, background='white', width=24)
        self.confirmPassword.grid(row=3, column=1, sticky='w')
        self.confirmPassword.focus_set()

        
        button1 = tk.Button(dialog_frame, text="Cancel", command=lambda: controller.show_frame(loginPage))
        button1.grid(row=4, column=0, sticky='w')
        #TODO: REGISTER COMPLETE PAGE
        button2 = tk.Button(dialog_frame, text="Register Visitor", command=lambda: controller.show_frame(loginPage))
        button2.grid(row=4, column=1, sticky='w')

class ownerRegistration(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="New Owner Registration", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        frame = tk.Frame(self)
        frame.pack(padx=5, pady=20, side=tk.LEFT)
        
        email = tk.Label(frame, text="Email:* ")
        email.grid(row=0, column=0, sticky='w')
        self.email = tk.Entry(frame, background='white', width=24)
        self.email.grid(row=0, column=1, sticky='w')
        self.email.focus_set()
        
        username = tk.Label(frame, text="Username:* ")
        username.grid(row=1, column=0, sticky='w')
        self.username = tk.Entry(frame, background='white', width=24)
        self.username.grid(row=1, column=1, sticky='w')
        self.username.focus_set()

        password = tk.Label(frame, text="Password:* ")
        password.grid(row=2, column=0, sticky='w')
        self.password = tk.Entry(frame, background='white', width=24)
        self.password.grid(row=2, column=1, sticky='w')
        self.password.focus_set()

        confirmPassword = tk.Label(frame, text="Confirm Password:* ")
        confirmPassword.grid(row=3, column=0, sticky='w')
        self.confirmPassword = tk.Entry(frame, background='white', width=24)
        self.confirmPassword.grid(row=3, column=1, sticky='w')
        self.confirmPassword.focus_set()

        propName = tk.Label(frame, text="Property Name:* ")
        propName.grid(row=4, column=0, sticky='w')
        self.propName = tk.Entry(frame, background='white', width=24)
        self.propName.grid(row=4, column=1, sticky='w')
        self.propName.focus_set()
        
        propAddress = tk.Label(frame, text="Street Address:* ")
        propAddress.grid(row=5, column=0, sticky='w')
        self.propAddress = tk.Entry(frame, background='white', width=24)
        self.propAddress.grid(row=5, column=1, sticky='w')
        self.propAddress.focus_set()
       
        propCity = tk.Label(frame, text="City:* ")
        propCity.grid(row=6, column=0, sticky='w')
        self.propCity = tk.Entry(frame, background='white', width=24)
        self.propCity.grid(row=6, column=1, sticky='w')
        self.propCity.focus_set()

        propZip = tk.Label(frame, text="Zip:* ")
        propZip.grid(row=7, column=0, sticky='w')
        self.propZip = tk.Entry(frame, background='white', width=24)
        self.propZip.grid(row=7, column=1, sticky='w')
        self.propZip.focus_set()
        
        propAcres = tk.Label(frame, text="Acres:* ")
        propAcres.grid(row=8, column=0, sticky='w')
        self.propAcres = tk.Entry(frame, background='white', width=24)
        self.propAcres.grid(row=8, column=1, sticky='w')
        self.propAcres.focus_set()

        propType = tk.Label(frame, text="Property Type:* ")
        propType.grid(row=9, column=0, sticky='w')
        # Rest of GUI depends on property type selected
        types = {'Garden', 'Farm', 'Orchard'}   # Dictionary holding different prop types
        
        propTypeVar = tk.StringVar()
        propTypeVar.set('Garden')   # Set garden as the default prop type
        propType_menu = tk.OptionMenu(frame, propTypeVar, *types)
        propType_menu.grid(row=9, column=1, padx=20, pady=10)

        if propTypeVar.get() == 'Garden':
            # Garden GUI
            # TODO: create a dictionary with approved vegetables and flowers (from DB)
            crop = tk.Label(frame, text="Crop:* ")
            crop.grid(row=10, column=0, padx=20, pady=10)

            # TODO: replace entry box with drop down populated by crop dictionary
            cropTxt = tk.StringVar()
            entry10 = tk.Entry(frame, textvariable=cropTxt)
            entry10.grid(row=10, column=1, padx=20, pady=10)
        elif propTypeVar.get() == 'Farm':
            # Farm GUI
            # TODO: create a dictionary with approved fruits, nuts, vegetables, and flowers (from DB)
            crop = tk.Label(frame, text="Crop:* ")
            crop.grid(row=10, column=0, padx=20, pady=10)

            # TODO: replace entry box with drop down populated by crop dictionary
            cropTxt = tk.StringVar()
            entry10 = tk.Entry(frame, textvariable=cropTxt)
            entry10.grid(row=10, column=1, padx=20, pady=10)

            # TODO: Do same thing with animals as crops ^
            animal = tk.Label(frame, text="Animal:* ")
            animal.grid(row=11, column=0, padx=20, pady=10)
            animalTxt = tk.StringVar()
            entry11 = tk.Entry(frame, textvariable=animalTxt)
            entry11.grid(row=11, column=1, padx=20, pady=10)
        else:
            # Orchard GUI
            # TODO: create a dictionary with approved fruits and nuts (from DB)
            crop = tk.Label(frame, text="Crop:* ")
            crop.grid(row=10, column=0, padx=20, pady=10)

            # TODO: replace entry box with drop down populated by crop dictionary
            cropTxt = tk.StringVar()
            entry10 = tk.Entry(frame, textvariable=cropTxt)
            entry10.grid(row=10, column=1, padx=20, pady=10)

        # Buttons
        button1 = tk.Button(frame, text="Cancel", command=lambda: controller.show_frame(loginPage))
        button1.grid(row=11, column=0, sticky='w')
        #TODO: REGISTER COMPLETE PAGE
        button2 = tk.Button(frame, text="Register Owner", command=lambda: controller.show_frame(loginPage))
        button2.grid(row=11, column=1, sticky='w')









app = Atlanta()
app.mainloop()