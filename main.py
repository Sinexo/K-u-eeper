#import explicite parceque c'est chiant d'écrire nom.fonction
from tkinter import Canvas, Entry, Button, PhotoImage, Label, Frame,filedialog,simpledialog,Toplevel,ttk
import sqlite3
import customtkinter as ctk # pas sûr de le garder si j'arrive pas a faire ce que je veux avec/ on peut faire des interface arroundi (bouton etc..) mais ça nécessite un fond de couleur uni car on change la couleur des bords, ce qui fonctionne pas très bien avec mon design 
import pyperclip # pour copier dans le presse papier
from hashlib import sha256, sha3_256
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Random.random import choice,shuffle
from Login import *
from Chest import *
from pathlib import Path
import string


class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1366x768")
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")
        # self.configure(bg="#FFFFFF")
        self.current_page = "main"
        self.main_page = Login_page(self, app_instance=self)
        self.main_page.pack(fill='both', expand=True)
        self.coffre = "NULL"

		#Stock les clef dans la ram
        self.login=""
        self.primary_key=""#On stock le hash sha3 ddu mdp maître pour pouvoir déchiffrer la clef primaire


    def select_file(self):
        file_path = filedialog.askopenfilename()
        #On pourrait juste utiliser endswith, mais vu que j'utilise pathlib pour supprimer des fichier plus tard dans le code, autant utiliser pthlib ici aussi
        if Path(file_path).suffix.lower()=='.db':
            self.coffre= file_path
        else:
            self.error()
            return


    def open_chest(self,entry):
        conn = sqlite3.connect(self.coffre)
        cursor = conn.cursor()
        cursor.execute("SELECT KEY FROM security")
        self.login = cursor.fetchone()
        # print(self.login)
        if sha256(entry.encode()).digest()==self.login[0]:
            conn.close()
            self.primary_key=sha3_256(entry.encode()).digest()
            self.change_page()
        else:
            self.error()

    def error(self):
        popup = ctk.CTkToplevel(self)
        ctk.set_appearance_mode("Dark")
        popup.title("ERREUR !")

        label_nom_db = Label(popup, text="Une erreur est survenu.")
        label_nom_db.pack(pady=(10, 0))
        label_mot_de_passe = Label(popup, text="Veuillez réessayer.")
        label_mot_de_passe.pack(pady=(10, 0))

        submit_button = Button(popup, text="Ok", command=lambda:popup.destroy())
        submit_button.pack(pady=20)

        popup.grab_set()
        self.wait_window(popup)

    #Fonction créeant un popup qui demande la saisie du mdp maître et du nom du coffre, à voir si jepeux la mettre dans un fichier à part parceque ça rallonge vraiment le mainapp
    def get_user_input(self):
        def submit():
            user_inputs[0] = entry_nom_db.get()
            user_inputs[1] = entry_mot_de_passe.get()
            for input in user_inputs:
                if input=="":
                    self.error()
                    return
            popup.destroy()

        user_inputs = ["", ""]
        popup = Toplevel(self)
        popup.geometry("220x180")
        popup.resizable(False,False)
        popup.bind('<Return>', lambda event=None: submit())
        popup.title("Nouveau coffre")

        label_nom_db = Label(popup, text="Nom de la base de données:")
        label_nom_db.place(x=30, y=10)

        entry_nom_db = Entry(popup)
        entry_nom_db.place(x=30, y=40)

        label_mot_de_passe = Label(popup, text="Mot de passe maître:")
        label_mot_de_passe.place(x=30, y=70)

        entry_mot_de_passe = Entry(popup, show='*')
        entry_mot_de_passe.place(x=30, y=100)

        submit_button = Button(popup, text="Soumettre", command=submit)
        submit_button.place(x=30, y=130)

        popup.grab_set()
        self.wait_window(popup)

        self.coffre = user_inputs[0]+'.db'
        return user_inputs[0]+'.db', user_inputs[1]


    def get_user_input_add_pass(self):
        # les fonctions sont définie à l'interieur d'un autre, c'est moche en effet, mais c'est bien plus pratique pour l'accès aux variable local à cet fonctions et rend le code un peu plus compréhensible à mon avis 
        def gen_password():
            alphabet = string.ascii_letters + string.digits + string.punctuation #concatenation des caractère
            p=''
            for i in range(18):
                p +=choice(alphabet)
            #print(p)
            entry_mot_de_passe.delete(0, 'end')
            entry_mot_de_passe.insert(0, p)

        def submit():
            user_inputs[0] = entry_site.get()
            user_inputs[1] = entry_user.get()
            user_inputs[2] = entry_mot_de_passe.get()
            for input in user_inputs:
                if input=="":
                    self.error()
                    return
            popup.destroy()

        user_inputs=[1,2,3]
        popup = Toplevel(self)
        popup.geometry("168x250")
        popup.resizable(False,False)
        popup.bind('<Return>', lambda event=None: submit())
        popup.title("Ajout d'un nouveau compte")

        label_site = Label(popup, text="Site:")
        label_site.place(x=10, y=10)

        entry_site = Entry(popup)
        entry_site.place(x=10, y=40)

        label_user = Label(popup, text="Identifiants:")
        label_user.place(x=10, y=70)

        entry_user = Entry(popup)
        entry_user.place(x=10, y=100)

        label_mot_de_passe = Label(popup, text="Mot de passe:")
        label_mot_de_passe.place(x=10, y=130)

        entry_mot_de_passe = Entry(popup, show='*')
        entry_mot_de_passe.place(x=10, y=160)

        gen_button = Button(popup, text="Genérer Mot de passe", command=gen_password)
        gen_button.place(x=17, y=190)

        submit_button = Button(popup, text="Ajouter", command=submit)
        submit_button.place(x=55, y=220)


        popup.grab_set()
        self.wait_window(popup)

        return user_inputs[0], user_inputs[1], user_inputs[2] #site/user/mdp


    def change_page(self):
        if self.current_page == "main":
            self.main_page.destroy()
            self.new_page = Chest_page(self, app_instance=self,chest=self.coffre)
            self.new_page.pack(fill='both', expand=True)
            self.current_page = "new"
            self.title("K(u)eeper Vault")
        else:
            self.new_page.destroy()
            self.main_page = Login_page(self, app_instance=self)
            self.main_page.pack(fill='both', expand=True)
            self.current_page = "main"
            self.title("K(u)eeper Login")

    def create_newDB(self):
        nom,mdp = self.get_user_input()
        #print(mdp)
        conn = sqlite3.connect(nom)
        cursor = conn.cursor()
        # print("oe")
        cursor.execute('''CREATE TABLE IF NOT EXISTS kueeper (id INTEGER PRIMARY KEY, site TEXT NOT NULL, user TEXT NOT NULL, password TEXT NOT NULL)''')
        # print("oe2")
        cursor.execute('''CREATE TABLE IF NOT EXISTS security (KEY BLOB, PRIMARY_KEY BLOB)''')
        # print("oe3")
        hash_mdp = sha256(mdp.encode()).digest()
        # cursor.execute("INSERT INTO security (KEY) VALUES (?)",(hash_mdp,))
        cursor.execute("INSERT INTO security (KEY, PRIMARY_KEY) VALUES (?, ?)", (hash_mdp, self.gen_primary_key(mdp)))
        # cursor.execute("INSERT INTO security (PRIMARY_KEY) VALUES (?)",(self.gen_primary_key(mdp),))
        # print("oe4")
        conn.commit()
        conn.close()
        # print("oe5")

    def gen_primary_key(self,mdp):
        iv = get_random_bytes(16)
        cipher=AES.new(sha3_256(mdp.encode()).digest(),AES.MODE_OFB,iv)
        p_key = cipher.encrypt(get_random_bytes(32))
        return p_key + iv#concatenation de la clef primaire + l'iv généré aléatoirement

    def decrypt_p_key(self):
        conn = sqlite3.connect(self.coffre)
        cursor = conn.cursor()
        cursor.execute("SELECT PRIMARY_KEY FROM security")
        liste = cursor.fetchone()

        p_key_cipher = liste[0]
        p_key = p_key_cipher[:-16]# la clef = les 32 premier octets
        iv = p_key_cipher[-16:]

        # key = sha3_256(mdp.encode()).digest() pas besoin le hash est stocké dans la mémoire pendant l'exécution
        cipher = AES.new(p_key, AES.MODE_OFB, iv)
        # clef = cipher.decrypt(p_key)

        return cipher.decrypt(p_key)

    def create_and_change(self):
        self.create_newDB()
        if(self.coffre==".db"):
            path = Path(".")
            for file in path.glob("*"):
                if file.name ==('.db'):
                    file.unlink()
            return
        self.change_page()

    def close(self):
        self.destroy()

app = MainApp()
app.title("K(u)eeper Login")
# app.wm_overrideredirect(True)
app.mainloop()
