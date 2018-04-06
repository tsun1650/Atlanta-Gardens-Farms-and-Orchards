from tkinter import *

class visitorRegistration:
	def __init__(self, parent = None):
		
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