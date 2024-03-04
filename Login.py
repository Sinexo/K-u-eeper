from tkinter import Canvas, Entry, Button, PhotoImage, Label, Frame,filedialog,simpledialog,Toplevel,ttk
import sqlite3
import customtkinter as ctk

class Login_page(ctk.CTkFrame):
    def __init__(self, master=None, app_instance=None,chest=None, **kwargs):
        super().__init__(master, **kwargs)
        # ctk.set_appearance_mode('Dark')#c'est sensé être un dark mode, mais ca ne fonctionne pas correctement, ça remplace le fond blanc qui apparait brievement pendant un changement de page par unfond noir, c'est tout de même mieux
        # ctk.set_default_color_theme("dark-blue")
        self.app_instance = app_instance  #pour appeler les fonction de MainApp, l'héritage ne fonctionnais pas comme je le souhaitais
        self.create_widgets()


    def create_widgets(self):
        self.canvas = ctk.CTkCanvas(
            self,
            bg="#FFFFFF",
            height=768,
            width=1366,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        self.image_image_1 = PhotoImage(
			file="./assets/frame0/image_1.png")
        self.image_1 = self.canvas.create_image(
			683.0,
			384.0,
			image=self.image_image_1
		)
        self.image_image_2 = PhotoImage(
			file="./assets/frame0/image_2.png")
        self.image_2 = self.canvas.create_image(
			325.0,
			309.0,
			image=self.image_image_2
		)

        self.entry_image_1 = PhotoImage(
			file="./assets/frame0/entry_1.png")
        entry_bg_1 = self.canvas.create_image(
			288.5,
			338.0,
			image=self.entry_image_1
		)
        self.entry_1 = ctk.CTkEntry(#Je pensais que customtkinter pourrait géré la transparence,mais je n'y arrive pas, cependant je trouve CTkEntry plus jolie que celui de tkinter donc je garde 
            self,
			# bd=0,
			# bg="#FFFFFF",
			# fg="#000716",
			bg_color='transparent',
			text_color='black',
			fg_color='pink',
			placeholder_text='Entrer votre mot de passe',
			show='*',
			width=385.0,
			height=34.0
		)
        self.entry_1.place(
			x=96.0,
			y=320.0,

		)

        self.button_new_image = PhotoImage(
			file="./assets/frame0/button_new.png")
        self.button_new = Button(
			image=self.button_new_image,
			borderwidth=0,
			highlightthickness=0,
			command=self.app_instance.create_and_change,
			relief="flat"
		)
        self.button_new.place(
			x=312.0,
			y=255.0,
			width=179.0,
			height=31.0
		)

        self.button_image_1 = PhotoImage(
			file="./assets/frame0/button_1.png")
        self.button_1 = Button(
			image=self.button_image_1,
			borderwidth=0,
			highlightthickness=0,
			command=self.open,

			relief="flat"
		)
        self.button_1.place(
			x=87.0,
			y=364.0,
			width=404.0,
			height=32.0
		)
        self.entry_1.bind('<Return>', lambda event=None: self.open())
        self.canvas.create_text(
			86.0,
			299.0,
			anchor="nw",
			text="Mot de passe",
			fill="#000000",
			font=("Poppins Medium", 14 * -1)
		)
        
        
        self.button_image_2 = PhotoImage(
			file="./assets/frame0/button_2.png")
        self.button_2 = Button(
			image=self.button_image_2,
			borderwidth=0,
			highlightthickness=0,
			command=self.app_instance.select_file,
			relief="flat"
		)
        self.button_2.place(
			x=87.0,
			y=255.0,
			width=179.0,
			height=31.0
		)
        
        self.image_image_3 = PhotoImage(
			file="./assets/frame0/image_3.png")
        self.image_3 = self.canvas.create_image(
			246.0,
			270.0,
			image=self.image_image_3
		)
        
        self.button_image_3 = PhotoImage(
			file="./assets/frame0/button_3.png")
        button_3 = Button(
			image=self.button_image_3,
			borderwidth=0,
			highlightthickness=0,
			command=lambda: print("button_3 clicked"),
			relief="flat"
		)
        button_3.place(
			x=1261.0,
			y=15.0,
			width=41.0,
			height=14.0
		)
        
        self.button_image_4 = PhotoImage(
			file="./assets/frame0/button_4.png")
        button_4 = Button(
			image=self.button_image_4,
			borderwidth=0,
			highlightthickness=0,
			command=self.app_instance.close,
			relief="flat"
		)
        button_4.place(
			x=1323.0,
			y=7.0,
			width=33.6,
			height=30.0
		)
    def open(self):
        self.app_instance.open_chest(self.entry_1.get())