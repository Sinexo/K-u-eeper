#import explicite parceque c'est chiant d'écrire nom.fonction
from tkinter import Canvas, Entry, Button, PhotoImage, Label, Frame,filedialog,simpledialog,Toplevel,ttk
import sqlite3
import customtkinter as ctk # pas sûr de le garder si j'arrive pas a faire ce que je veux avec/ on peut faire des interface arroundi (bouton etc..) mais ça nécessite un fond de couleur uni car on change la couleur des bords, ce qui fonctionne pas très bien avec mon design 
import pyperclip # pour copier dans le presse papier
from hashlib import sha256, sha3_256
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Random.random import choice,shuffle
from pathlib import Path
import string

class Chest_page(Frame):
    def __init__(self, master=None, app_instance=None,chest=None, **kwargs):
        super().__init__(master, **kwargs)
        self.coffre=chest
        self.app_instance = app_instance
        self.initialize_widgets()  # j'ai changé le nom car j'avais des problèmes de superposition des boutons, normalement c'est pas en lien mais dans le doute pour éviter les conflits
    def initialize_widgets(self):
        self.conn = sqlite3.connect(self.coffre)
        #self.cursor=self.conn j'ai des problème avec cette ligne j'ai donc choisi de la réécrire à chauqe fois que j'ai besoin de la bdd
        self.canvas = Canvas(
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
			file="./assets/frame1/image_1.png")
        self.image_1 = self.canvas.create_image(
			683.0,
			384.0,
			image=self.image_image_1
		)
        self.image_image_2 = PhotoImage(
			file="./assets/frame1/image_2.png")
        self.image_2 = self.canvas.create_image(
			823.0,
			397.0,
			image=self.image_image_2
		)
        self.image_image_3 = PhotoImage(
			file="./assets/frame1/image_3.png")
        image_3 = self.canvas.create_image(
			163.0,
			268.0,
			image=self.image_image_3
		)

		#Bouton pour supprimer une entrée dans la BDD
        self.button_image_1 = PhotoImage(
			file="./assets/frame1/button_1.png")
        self.button_1 = Button(
			image=self.button_image_1,
			borderwidth=0,
			highlightthickness=0,
			command=lambda:self.delete_pass(),
			relief="flat"
		)
        self.button_1.place(
			x=65.0,
			y=131.0,
			width=98.0,
			height=22.0
		)

        #Bouton pour ajouter une entrée dans la BDD
        self.button_image_2 = PhotoImage(
			file="./assets/frame1/button_2.png")
        self.button_add_pass = Button(
			image=self.button_image_2,
			borderwidth=0,
			highlightthickness=0,
			command=lambda:self.add_pass(self.conn),
			relief="flat"
		)
        self.button_add_pass.place(
			x=65.0,
			y=91.0,
			width=98.0,
			height=22.0
		)


		#Bouton qui ferme l'accès au coffre(retour au menu de connexion)
        self.button_image_3 = PhotoImage(
			file="./assets/frame1/button_3.png")
        self.button_3 = Button(
			image=self.button_image_3,
			borderwidth=0,
			highlightthickness=0,
			command=self.app_instance.change_page,
			relief="flat"
		)
        self.button_3.place(
			x=65.0,
			y=397.0,
			width=130.0,
			height=37.0
		)


		#Bouton qui modifie unentrée dans la BDD
        self.button_image_4 = PhotoImage(
			file="./assets/frame1/button_4.png")
        self.button_4 = Button(
			image=self.button_image_4,
			borderwidth=0,
			highlightthickness=0,
			command=lambda: self.modify_pass(),
			relief="flat"
		)
        self.button_4.place(
			x=65.0,
			y=174.0,
			width=98.0,
			height=21
		)

        #Bouton qui exporte la bdd mais dcp un peu inutile finalement, a delete ou remplacer 
        # self.button_image_5 = PhotoImage(
		# 	file="./assets/frame1/button_5.png")
        # self.button_5 = Button(
		# 	image=self.button_image_5,
		# 	borderwidth=0,
		# 	highlightthickness=0,
		# 	command=lambda: print("button_5 clicked"),
		# 	relief="flat"
		# )
        # self.button_5.place(
		# 	x=65.0,
		# 	y=216.0,
		# 	width=98.0,
		# 	height=22.0
		# )
        self.image_image_4 = PhotoImage(
			file="./assets/frame1/image_4.png")
        self.image_4 = self.canvas.create_image(
			813.0,
			346.0,
			image=self.image_image_4
		)


        self.button_image_6 = PhotoImage(
			file="./assets/frame1/button_6.png")
        self.button_6 = Button(
			image=self.button_image_6,
			borderwidth=0,
			highlightthickness=0,
			command=lambda: print("button_6 clicked"),
			relief="flat"
		)
        self.button_6.place(
			x=1254.0,
			y=19.0,
			width=41.0,
			height=14.0
		)

        #Bouton close, je ne saispa si wm.override sera gardé dans l version final, mais c'était pour pouvoir fermer la fenêtre
        self.button_image_close = PhotoImage(
			file="./assets/frame1/button_7.png")
        self.button_close = Button(
			image=self.button_image_close,
			borderwidth=0,
			highlightthickness=0,
			command=self.app_instance.close,
			relief="flat"
		)
        self.button_close.place(
			x=1313.0,
			y=11.0,
			width=33.6,
			height=30.0
		)

        self.image_image_5 = PhotoImage(
			file="./assets/frame1/image_5.png")
        self.image_5 = self.canvas.create_image(
			152.0,
			310.0,
			image=self.image_image_5
		)

        #Treeview pour afficher la base de données
        self.tree = ttk.Treeview(self)
        self.tree["columns"] = ("Site", "Utilisateur", "Password","ID")#Nom des colonnes (pas celle de la bdd)
        self.tree.column("#0", width=0, stretch=False) # Colonne fantôme pour avoir des ID
        self.tree.column("Site", anchor='w', width=150)
        self.tree.column("Utilisateur", anchor='w', width=150)
        self.tree.column("Password", anchor='w', width=150)
        self.tree.column("ID",width=0,stretch=False)

        self.tree.heading("#0", text="", anchor='w')
        self.tree.heading("Site", text="Site", anchor='w')
        self.tree.heading("Utilisateur", text="Utilisateur", anchor='w')
        self.tree.heading("Password", text="Mot de passe", anchor='w')
        self.tree.heading("ID", text="", anchor='w')

        self.tree.place(x=400, y=100, width=850, height=600)

        self.load_data(self.conn)
        self.tree.bind("<Double-1>", self.copy)
        self.tree_scroll = ttk.Scrollbar(self)
        self.tree_scroll.place(x=1250, y=100, height=600)
        self.tree.configure(yscrollcommand=self.tree_scroll.set)
        self.tree_scroll.configure(command=self.tree.yview)

    def encrypt(self,champ):
        iv = get_random_bytes(16)
        cipher=AES.new(self.app_instance.decrypt_p_key(),AES.MODE_OFB,iv)
        cipher_champ= cipher.encrypt(champ.encode())
        return cipher_champ + iv#concatenation de la clef primaire + l'iv généré aléatoirement

    def decrypt(self,champ):
        iv = champ[-16:]
        cipher_champ= champ[:-16]#vu que les données déchiffré ne seront pas tous de la même longueur on ne peut pas écrire de manière brut comme dans les fonctions de clefs primaires écrite en dessous 
        decipher=AES.new(self.app_instance.decrypt_p_key(),AES.MODE_OFB,iv)
        res = decipher.decrypt(cipher_champ).decode('UTF-8')
        return res


    def load_data(self,conn):#On charge la bdd dans le treeview pour l'afficher
        try:
            # conn = sqlite3.connect('bdd.db')
            cursor = self.conn.cursor()
            cursor.execute("SELECT id, site, user, password FROM kueeper")
            rows = cursor.fetchall()
            for row in rows:
                mdp = row[3]
                cache = '*' * len(mdp)
                self.tree.insert("", 'end', values=(self.decrypt(row[1]),self.decrypt(row[2]),cache,row[0]))
                # conn.close()
        except Exception:
            self.app_instance.error()
            self.app_instance.change_page()

    def copy(self,event):
        item = self.tree.selection()[0]
        values = self.tree.item(item, "values")
        # Colonne 
        col = self.tree.identify_column(event.x)
        if col == "#1": #Site
            pyperclip.copy(values[0])
        elif col == "#2":  # User
            pyperclip.copy(values[1])
        elif col == "#3":  #MDP
            cursor = self.conn.cursor()
            cursor.execute("SELECT password FROM kueeper WHERE id=?", (values[3],))
            mdp = cursor.fetchone()
            pyperclip.copy(self.decrypt(mdp[0])) # ça renvoie un tuple même c'est fetchone etpas all
            

    #Fonction de d'opération basique dans la base de données
    def add_pass(self,conn):
        try:
            # conn = sqlite3.connect('bdd.db')
            site,user,password=self.app_instance.get_user_input_add_pass()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO kueeper (site, user, password) VALUES (?, ?, ?)", (self.encrypt(site), self.encrypt(user), self.encrypt(password)))
            conn.commit()
            cache= '*' * len(password)
            self.tree.insert("", 'end', values=(site, user, cache,cursor.lastrowid))
        except Exception as error:
            print(f"Erreur lors de l'ajout du mot de passe : {error}")

    def delete_pass(self):
        selected_item = self.tree.selection()[0]
        values = self.tree.item(selected_item, 'values')
        conn = sqlite3.connect(self.coffre)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM kueeper WHERE id=?", (values[3],))
        conn.commit()
        conn.close()
        self.tree.delete(selected_item)


    def modify_pass(self):
        site,user,password=self.app_instance.get_user_input_add_pass()
        selected_item = self.tree.selection()[0]
        values = self.tree.item(selected_item, 'values')
        conn = sqlite3.connect(self.coffre)
        cursor = conn.cursor()
        cursor.execute("UPDATE kueeper SET site=?, user=?, password=? WHERE id=?", (self.encrypt(site), self.encrypt(user), self.encrypt(password), values[3]))
        conn.commit()
        cache= '*' * len(password)
        self.tree.item(selected_item, values=(site, user, cache,values[3],))