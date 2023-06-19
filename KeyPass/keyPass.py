from tkinter import *
from random import*
# Cryptage AES (Advanced Encryption Standard)
# Aussi appellé Rijndael
import RijndaelAlgorithm as RA
import webbrowser
import string
import time
import sys

alphabet = string.ascii_letters + string.digits + string.punctuation
separators = ['<s@,>[','<s@,>]'] #espace, retour à la ligne


langue = "Français"
langues = ["Français","English","Español"]
platforme = sys.platform
controlKey = "Control"
if platforme == "darwin":
    controlKey = "Command"

mdp = {}
mdp["emplacement"] = "motDePasses.txt"

mdp["messageInit"] = ['Bienvenu dans votre gestionnaire de mots de passe !\n\nUne fois un compte selectionné :\n    - '+controlKey+' + X pour copier le mot de passe\n    - '+controlKey+' + B pour copier le nom d\'utilisateur\n    - '+controlKey+' + U pour copier le lien du site web\n    - Touche \'Entrée\' pour ouvrir le lien\n    - Touche \'Supr\' pour effacer ou modifier le compte\n\nRecherchez un compte avec les lettres des touches du clavier si besoin. \nPressez deux fois la touche "d" pour vous déconnecter. ',
                      'Welcome to your password manager !\n\nOnce an account has been selected :\n    - '+controlKey+' + X to copy the password\n    - '+controlKey+' + B to copy the username\n    - '+controlKey+' + U to copy the website link\n    - Key \'Enter\' to open the website link\n    - Key \'Delete\' to delete or modify the account\n\nSearch for an account with keyboard letters if necessary. \nPress the "d" key twice to log out. ',
                      '¡Bienvenido a tu administrador de contraseñas!\n\nUna vez que has seleccionado una cuenta :\n    - '+controlKey+' + X para copiar la contraseña\n    - '+controlKey+' + B para copiar el nombre de usuario\n    - '+controlKey+' + U para copiar el enlace\n    - Tecla \'Enter\' para abrir el enlace\n    - Tecla \'Borrar\' para eliminar o modificar la cuenta\n\nBusqua una cuenta con letras del teclado si es necesario. \nPresione la tecla "d" dos veces para cerrar sesión. '][langues.index(langue)]
                      

def chargerInfos():
    try:
        mdp["fichier"] = open(mdp["emplacement"], 'r')
        mdp["contenu"] = mdp["fichier"].read()
        mdp["fichier"].close()
        mdp["contenu"] = mdp["contenu"].split(separators[1])
        mdp["comptes"] = {}
        mdp["message"] = ""
        mdp["signature"] = mdp["contenu"][0]
        for i in range(1,len(mdp["contenu"])):
            mdp["comptes"][mdp["contenu"][i].split(separators[0])[0]]=[mdp["contenu"][i].split(separators[0])[h] for h in range(1,5)]


    except FileNotFoundError:
        mdp["fichier"] = open(mdp["emplacement"], 'w')
        sign = signature((input(trad("Nouveau mot de passe : "))+"aaaa"*4)[:16])
        while sign != 0:
            sign = signature((input(trad("Nouveau mot de passe : ")+"(Not only a's)")+"aaaa"*4)[:16])
        print("Veillez à fermer cette fenêtre le plus rapidement possible")
        mdp["fichier"].write(str(sign))
        mdp["fichier"].close()
        mdp["comptes"] = {}
        mdp["signature"] = sign
        mdp["message"] = trad("Nouveau mot de passe bien défini")+ "\n"

def envoyerInfos():
    texte = mdp["signature"]
    mdp["fichier"] = open(mdp["emplacement"], 'r')
    mdp["contenu"] = mdp["fichier"].read()
    mdp["fichier"].close()
    mdp["fichier"] = open(mdp["emplacement"], 'w')
    for i in range(len(mdp["comptes"])):
        texte += separators[1] + list(mdp["comptes"])[i]
        for j in range(4):
            texte += separators[0] + mdp["comptes"][list(mdp["comptes"])[i]][j]
    mdp["fichier"].write(texte)
    mdp["fichier"].close()
    
        
def trad(text):
    traducteur = {"Veillez à fermer cette fenêtre le plus rapidement possible":
                  ["Please, close that window as quick as possible",
                  "Porfavor, cierre esta ventana rapidamente"],
                  "Nouveau mot de passe bien défini":
                  ["New password well defined ",
                  "Nueva contraseña bien definida "],
                  "Nouveau mot de passe : ":
                  ["New password : ",
                  "Nueva contraseña : "],
                  "Entrez le mot de passe principal : ":["Please, enter the master password : ","Ingrese la contraseña maestra : "],
                  "Valider":["Check","Validar"],"":["",""],
                  "Le mot de passe est invalide.":["Invalid password.","La contraseña no es válida."],
                  "Connexion":["Connection","Conexión"],
                  "Mes comptes":["My accounts","Mis cuentas"],
                  "Copier le nom d'utilisateur":["Copy username","Copiar el nombre de usuario"],
                  "Copier le mot de passe":["Copy password","Copiar la contraseña"],
                  "Ouvrir le lien":["Open the link","Abrir el enlace"],
                  "Ajouter un compte":["Add an account","Añadir una cuenta"],
                  "Nouveau compte":["New account","Nueva cuenta"],"Modification du compte":["Edit account","Editar cuenta"],
                  "Nom du compte":["Account name","Nombre de la cuenta"],
                  "Nom de l'utilisateur":["Username","Nombre de usuario"],
                  "URL du site web":["Website Url","Enlace del sitio web"],
                  "Mot de passe":["Password","Contraseña"],
                  "Notes":["Notes","Notas"],"Lettres":["Letters","Letras"],
                  "Générer":["Generate","Generar"],"Chiffres":["Digits","Cifras"],
                  "Paramètres": ["Settings","Configuración"],"Longueur":["Length","Longitud"],
                  "Caractères spéciaux":["Special characters","Caracteres especiales"],
                  "Effacer":["Delete","Borrar"],"Oui":["Yes","Si"], "Non":["No"]*2,
                  "Modifier":["Edit","Modificar"],
                  "Aucun compte sélectionné":["No account selected","Ninguna cuenta seleccionada"]}
    if(langues.index(langue)==0):
        return text
    else:
        return traducteur[text][langues.index(langue)-1]

def passWordCreate(longueur, l = True, c = True, p = False):
    return "".join(choice(string.ascii_letters*int(l) + string.digits*int(c) + string.punctuation*int(p)) for i in range(longueur))

def signature(motDePasse):#On défini la signature d'un mot de passe comme la somme des index de chaquns de ses caractères
    return sum([alphabet.index(motDePasse[i]) for i in range(len(motDePasse))])

def coder(textOrList):
    if textOrList.__class__ == str:
        texte = textOrList
        if texte == "":
            return ""
        texte += " " * (len(masterPassword)-len(texte) % len(masterPassword))
        decoupage = [texte[16*(i):16*(i+1)] for i in range(len(texte)//16)]
        code = ""
        for i in range(len(decoupage)):
            code += key.encrypt(decoupage[i])
        code = code.replace("\r","</r@,>")
        return code
    elif textOrList.__class__ == list:
        liste = textOrList
        code = []
        for i in range(len(liste)):
            code.append(coder(liste[i]))
        return code

def decoder(textOrList):
    if textOrList.__class__ == str:
        texte = textOrList
        if texte == "":
            return ""
        texte = texte.replace("</r@,>","\r")
        decoupage = [texte[16*(i):16*(i+1)] for i in range(len(texte)//16)]
        decode = ""
        for i in range(len(decoupage)):
            decode += key.decrypt(decoupage[i])
        while(decode[-1]==" "):
            decode = decode[0:len(decode)-1]
            if decode == "":
                return ""
        return decode
    elif textOrList.__class__ == list:
        liste = textOrList
        decode = []
        for i in range(len(liste)):
            decode.append(decoder(liste[i]))
        return decode

def ajouterMdp(compte, utilisateur, motdepasse, URL, notes = ""):
    mdp["comptes"][coder(compte)] = coder([utilisateur, motdepasse, URL, notes])
    envoyerInfos()

def effacerMdp(compte):
    try:
        del mdp["comptes"][compte]
    except KeyError:
        del mdp["comptes"][coder(compte)]
    envoyerInfos()
        
def connexion():
    def validation(e=None):
        global masterPassword
        if(signature(entreMdp.get()) == int(mdp["signature"])):#Si le mot de passe a la bonne signature
            masterPassword = (entreMdp.get()+"aaaa"*4)[:16]
            master.destroy()
            gerantMdp()
        else:
            message.set(mdp["message"]+trad("Le mot de passe est invalide."))
        #En essayant un mot de passe au hasard, il y a une chance sur 5,7 10^26 d'avoir le bon code et une chance sur 2700 d'obtenir la même signature et de passer cette étape,
        # dans ce cas, les mots de passe donnés seront éronnés
    
    global masterPassword
    
    master = Tk()
    message = StringVar(master)
    master.title(trad("Connexion"))
    master.geometry("480x360")
    master.minsize(400,300)
    master.maxsize(1080,720)
    if(platforme!="darwin"):
        master.iconbitmap("key-icon.ico")

    frame = Frame(master)
    
    texteMaster = Label(frame,text=trad("Entrez le mot de passe principal : "), font = ("Courrier", 14))#bg et fg
    texteMaster.pack()

    entreMdp = Entry(frame,show = "*",text = "Master password...",font = ("Courrier", 14))
    entreMdp.pack()
    
    sousTexteMaster = Label(frame,textvariable=message, font = ("Courrier", 14), fg = "red")#bg et fg
    sousTexteMaster.pack()
    message.set(mdp["message"])

    buttonValider = Button(frame, text = trad("Valider"), command=validation)
    buttonValider.pack()

    frame.pack(expand = YES)

    master.bind("<Return>", validation)   
    
    master.mainloop()
    

def deconnexion(e=None, root = None):
    global masterPassword
    del masterPassword
    if (root != None):
        root.destroy()
    else:
        e.widget.destroy()
    connexion()

def refresh(e=None):
    listCon.set(tuple([sorted(decoder(list(mdp["comptes"])))[i] for i in range(len(mdp["comptes"]))]))

    
def modifCompte(_list):
    global eyeLogo,eyeBarLogo
    eyeLogo = PhotoImage(file="eye.gif")
    eyeBarLogo = PhotoImage(file="eyeBar.gif")
    ancienCompte = sorted(decoder(list(mdp["comptes"])))[(_list.curselection()+(-1,))[0]]
    def validation():
        effacerMdp(ancienCompte)
        nvCompte = entreCompte.get()[0].upper()+entreCompte.get()[1:len(entreCompte.get())]
        nvUser = entreUser.get()
        nvMDP = entreMDP.get()
        nvURL = entreURL.get()
        nvNotes = entreNotes.get("1.0","end")
        nvCompteNum, i = nvCompte, 0
        while nvCompteNum in decoder(list(mdp["comptes"])):
            i = i+1
            nvCompteNum = nvCompte + str(i)
        ajouterMdp(nvCompteNum, nvUser , nvMDP, nvURL, nvNotes)
        refresh()
        modifButt.destroy()
    def showHide():
        if entreMDP["show"] == "*":
            entreMDP["show"] = ""
            eyeButton["image"] = eyeBarLogo
        else:
            entreMDP["show"] = "*"
            eyeButton["image"] = eyeLogo

    def param():
        global paramW
        paramW = Toplevel()
        paramW.title(trad("Paramètres"))
        paramW.geometry("178x144")
        Checkbutton(paramW,text = trad("Lettres"), variable = lettresMDP).pack()
        Checkbutton(paramW,text = trad("Chiffres"), variable = chiffresMDP).pack()
        Checkbutton(paramW,text = "Caractères spéciaux", variable = caracMDP).pack()
        Scale(paramW, orient='horizontal', from_=0, to=32,
      resolution=1, tickinterval=8, length=150,
      label=trad('Longueur')+ " : ", variable = lenMDP).pack(fill = BOTH)

    def generer():
        if(not bool(lettresMDP.get()+chiffresMDP.get()+caracMDP.get())):
            paramButton.flash()
        else:
            motDePasse.set(passWordCreate(lenMDP.get(), l = bool(lettresMDP.get()), c = bool(chiffresMDP.get()), p = bool(caracMDP.get())))

    def adapter(e):
        entreNotes["height"] = (modifButt.winfo_height()-validBut.winfo_height()-430)//17
        
    modifButt = Toplevel()
    modifButt.title(trad("Modification du compte"))
    modifButt.geometry("300x572")
    modifButt.minsize(170,100)
    if(platforme!="darwin"):
        modifButt.iconbitmap("new.ico")

    Label(modifButt).pack(side=TOP) ### separation ###
    
    Label(modifButt,text = trad("Nom du compte")+" : ", font = ("Courrier", 14), justify = "left").pack(side=TOP)

    entreCompteVar = StringVar()
    entreCompte = Entry(modifButt,font = ("Courrier", 14), textvariable = entreCompteVar) # entree compte
    entreCompte.pack(side=TOP,fill = X)
    entreCompteVar.set(ancienCompte)
    
    Label(modifButt).pack(side=TOP) ### separation ###
    
    Label(modifButt,text = trad("Nom de l'utilisateur")+" : ", font = ("Courrier", 14)).pack(side=TOP)
    
    entreUserVar = StringVar()
    entreUser = Entry(modifButt,font = ("Courrier", 14), textvariable = entreUserVar) # entree Utilisateur
    entreUser.pack(side=TOP,fill = X)
    entreUserVar.set(decoder(mdp["comptes"][coder(ancienCompte)][0]))
    
    Label(modifButt).pack(side=TOP) ### separation ###
    
    Label(modifButt,text = trad("URL du site web")+" : ", font = ("Courrier", 14)).pack(side=TOP)

    entreURLVar = StringVar()
    entreURL = Entry(modifButt,font = ("Courrier", 14), textvariable = entreURLVar) # entree url
    entreURL.pack(side=TOP, fill =X)
    entreURLVar.set(decoder(mdp["comptes"][coder(ancienCompte)][2]))
    
    Label(modifButt).pack(side=TOP) ### separation ###
    
    frameMDP = Frame(modifButt) # partie mot de passe
    view = IntVar()
    Label(frameMDP,text = trad("Mot de passe")+" : ", font = ("Courrier", 14)).pack(side=TOP)
    motDePasse = StringVar()
    entreMDP = Entry(frameMDP,show="*",textvariable = motDePasse,font = ("Courrier", 14))
    entreMDP.pack(side=TOP,fill = X)
    motDePasse.set(decoder(mdp["comptes"][coder(ancienCompte)][1]))
    Button(frameMDP, text = trad("Générer"), command = generer).pack(side=LEFT)
    paramButton = Button(frameMDP, text = trad("Paramètres"), command = param)
    paramButton.pack(side=LEFT)
    eyeButton = Button(frameMDP, image = eyeLogo, command = showHide)
    eyeButton.pack(side= RIGHT)
    frameMDP.pack(side=TOP,fill = BOTH)
    
    Label(modifButt).pack(side=TOP) ### separation ###
    
    Label(modifButt,text = trad("Notes")+" : ", font = ("Courrier", 14)).pack(side=TOP)
    
    entreNotes = Text(modifButt,font = ("Courrier", 14),wrap='word', height = 7, undo = True, highlightthickness = 0, bd = 1, relief = "solid") # entree notes
    entreNotes.pack(side=TOP,fill=BOTH)
    entreNotes.insert("1.0",decoder(mdp["comptes"][coder(ancienCompte)][3]))
    
    Label(modifButt).pack(side=TOP) ### separation ###

    validBut = Button(modifButt,text = trad("Valider"),font = ("Courrier", 14), command = validation)
    validBut.pack(side = RIGHT)

    modifButt.bind("<Configure>", adapter)


def ajoutCompte():
    global eyeLogo,eyeBarLogo
    eyeLogo = PhotoImage(file="eye.gif")
    eyeBarLogo = PhotoImage(file="eyeBar.gif")
    
    def validation():
        nvCompte = entreCompte.get()[0].upper()+entreCompte.get()[1:len(entreCompte.get())]
        nvUser = entreUser.get()
        nvMDP = entreMDP.get()
        nvURL = entreURL.get()
        nvNotes = entreNotes.get("1.0","end")
        nvCompteNum, i = nvCompte, 1
        while nvCompteNum in decoder(list(mdp["comptes"])):
            i = i+1
            nvCompteNum = nvCompte + str(i)
        ajouterMdp(nvCompteNum, nvUser , nvMDP, nvURL, nvNotes)
        refresh()
        addButt.destroy()
    def showHide():
        if entreMDP["show"] == "*":
            entreMDP["show"] = ""
            eyeButton["image"] = eyeBarLogo
        else:
            entreMDP["show"] = "*"
            eyeButton["image"] = eyeLogo

    def param():
        global paramW
        paramW = Toplevel()
        paramW.title(trad("Paramètres"))
        paramW.geometry("178x144")
        Checkbutton(paramW,text = trad("Lettres"), variable = lettresMDP).pack()
        Checkbutton(paramW,text = trad("Chiffres"), variable = chiffresMDP).pack()
        Checkbutton(paramW,text = trad("Caractères spéciaux"), variable = caracMDP).pack()
        Scale(paramW, orient='horizontal', from_=0, to=32,
      resolution=1, tickinterval=8, length=150,
      label=trad('Longueur')+ " : ", variable = lenMDP).pack(fill = BOTH)

    def generer():
        if(not bool(lettresMDP.get()+chiffresMDP.get()+caracMDP.get())):
            paramButton.flash()
        else:
            motDePasse.set(passWordCreate(lenMDP.get(), l = bool(lettresMDP.get()), c = bool(chiffresMDP.get()), p = bool(caracMDP.get())))

    def adapter(e):
        entreNotes["height"] = (addButt.winfo_height()-validBut.winfo_height()-430)//17
        
    addButt = Toplevel()
    addButt.title(trad("Nouveau compte"))
    addButt.geometry("300x572")
    addButt.minsize(170,100)
    if(platforme!="darwin"):
        addButt.iconbitmap("new.ico")

    Label(addButt).pack(side=TOP) ### separation ###
    
    Label(addButt,text = trad("Nom du compte")+" : ", font = ("Courrier", 14), justify = "left").pack(side=TOP)

    entreCompte = Entry(addButt,font = ("Courrier", 14)) # entree compte
    entreCompte.pack(side=TOP,fill = X)
    
    Label(addButt).pack(side=TOP) ### separation ###
    
    Label(addButt,text = trad("Nom de l'utilisateur")+" : ", font = ("Courrier", 14)).pack(side=TOP)

    entreUser = Entry(addButt,font = ("Courrier", 14)) # entree Utilisateur
    entreUser.pack(side=TOP,fill = X)
    
    Label(addButt).pack(side=TOP) ### separation ###
    
    Label(addButt,text = trad("URL du site web")+" : ", font = ("Courrier", 14)).pack(side=TOP)

    entreURL = Entry(addButt,font = ("Courrier", 14)) # entree url
    entreURL.pack(side=TOP, fill =X)
    
    Label(addButt).pack(side=TOP) ### separation ###
    
    frameMDP = Frame(addButt) # partie mot de passe
    view = IntVar()
    Label(frameMDP,text = trad("Mot de passe")+" : ", font = ("Courrier", 14)).pack(side=TOP)
    motDePasse = StringVar()
    entreMDP = Entry(frameMDP,show="*",textvariable = motDePasse,font = ("Courrier", 14))
    entreMDP.pack(side=TOP,fill = X)
    Button(frameMDP, text = trad("Générer"), command = generer).pack(side=LEFT)
    paramButton = Button(frameMDP, text = trad("Paramètres"), command = param)
    paramButton.pack(side=LEFT)
    eyeButton = Button(frameMDP, image = eyeLogo, command = showHide)
    eyeButton.pack(side= RIGHT)
    frameMDP.pack(side=TOP,fill = BOTH)
    
    Label(addButt).pack(side=TOP) ### separation ###
    
    Label(addButt,text = trad("Notes")+" : ", font = ("Courrier", 14)).pack(side=TOP)
    
    entreNotes = Text(addButt,font = ("Courrier", 14), wrap='word', height = 7, undo = True, highlightthickness = 0, bd = 1, relief = "solid") # entree notes
    entreNotes.pack(side=TOP,fill=BOTH)
    
    Label(addButt).pack(side=TOP) ### separation ###

    validBut = Button(addButt,text = trad("Valider"),font = ("Courrier", 14), command = validation)
    validBut.pack(side = RIGHT)

    addButt.bind("<Configure>", adapter)

        
def gerantMdp():
    global _listFrames, key, motDePasse,listCon,lettresMDP, chiffresMDP, caracMDP, lenMDP, logoLeave
    mdp["autoriser"] = True
    
    def copierMdp(compte):
        root.clipboard_clear()
        root.clipboard_append(decoder(mdp["comptes"][coder(compte)][1]))
        print("Le mot de passe a bien été copié dans le presse papiers.")
        mdp["autoriser"] = False
    def copierMdpEvent(Event):
        copierMdp(sorted(decoder(list(mdp["comptes"])))[(_list.curselection()+(-1,))[0]])
        
    def copierUser(compte):
        root.clipboard_clear()
        root.clipboard_append(decoder(mdp["comptes"][coder(compte)][0]))
        print("Le nom d'utilisateur a bien été copié dans le presse papiers.")
        mdp["autoriser"] = False
    def copierUserEvent(Event):
        copierUser(sorted(decoder(list(mdp["comptes"])))[(_list.curselection()+(-1,))[0]])
    
        
    def copierURL(compte):
        root.clipboard_clear()
        root.clipboard_append(decoder(mdp["comptes"][coder(compte)][2]))
        print("Le lien a bien été copié dans le presse papiers.")
        mdp["autoriser"] = False
    def copierURLEvent(Event):
        copierURL(sorted(decoder(list(mdp["comptes"])))[(_list.curselection()+(-1,))[0]])

    def openURL(compte):
        URL = decoder(mdp["comptes"][coder(compte)][2])
        webbrowser.open(URL)
        mdp["autoriser"] = False
    def openURLEvent(Event):
        index = (_list.curselection()+(-1,))[0]
        if index != -1:
            openURL(sorted(decoder(list(mdp["comptes"])))[index])

    def deleteEvent(Event):
        def yes():
            effacerMdp(compte)
            refresh()
            verif.destroy()
        def modif():
            modifCompte(Event.widget)
            verif.destroy()
        verif = Toplevel()
        verif.title(trad("Effacer"))
        compte = sorted(decoder(list(mdp["comptes"])))[(_list.curselection()+(-1,))[0]]
        Label(verif, text = trad("Effacer")+ " " + compte+ " ?").pack(side = TOP)
        Button(verif,text=trad("Oui"),command = yes).pack(side = RIGHT)
        Button(verif,text=trad("Modifier"),command = modif).pack(side = RIGHT)
        Button(verif, text=trad("Non"), command = verif.destroy).pack(side = LEFT)

    def adapt_all(Event): # à compléter avec le canevas
        _list["height"] = (listFrame.winfo_height()-addButton.winfo_height()-22)//18
        leave.place(x=root.winfo_width()-38,y=10)
        
    def changeFocusWithLetter(Event):
        if mdp["autoriser"] == True:
            if Event.keysym in string.ascii_letters :
                if _list.curselection() != ():
                    _list.selection_clear(_list.curselection())
                index = sorted(decoder(list(mdp["comptes"]))+[Event.keysym.upper()]).index(Event.keysym.upper())
                if index == len(mdp["comptes"]):
                    index -= 1
                _list.activate(index)
                _list.index(index)
                _list.see(index)
                _list.selection_set(index)
        mdp["autoriser"]  = True

    def scrollY(Event):
        _list.xview_scroll(Event.delta, "units")

    def modTCompte(e=None):
        compte = (sorted(decoder(list(mdp["comptes"])))+[trad("Aucun compte sélectionné")])[(_list.curselection()+(-1,))[0]]
        titreCompteVar.set(compte)
        notesCompte["state"] = "normal"
        notesCompte.delete("1.0","end")
        if compte == trad("Aucun compte sélectionné"):
            notesCompte.insert("1.0",mdp["messageInit"])             
        else:
            modifier["state"] = "normal"
            notesCompte.insert("1.0",decoder(mdp["comptes"][coder(compte)][3]))
        notesCompte["state"] = "disabled"

    def deco(e=None):
        deconnexion(root = root)


    key = RA.Rijndael(masterPassword, block_size = len(masterPassword))
    root = Tk()
    root.title(trad("Mes comptes"))
    root.geometry("930x480")
    root.minsize(500,250)
    root.maxsize(1080,720)
    if(platforme!="darwin"):
        root.iconbitmap("key-icon.ico")
        
    lettresMDP, chiffresMDP, caracMDP, lenMDP = IntVar(), IntVar(), IntVar(), IntVar()
    lettresMDP.set(1)
    chiffresMDP.set(1)
    caracMDP.set(0)
    lenMDP.set(10)
        
    listFrame = LabelFrame(root, text = trad("Mes comptes"))
    listCon = StringVar()
    _list = Listbox(listFrame, width = 30, height = 30, font = ("Courrier", 14), bd= 0 , listvariable = listCon)#selectmode = SINGLE)
    _list.pack()
    listFrame.pack(side = RIGHT, fill= BOTH)
    
    refresh()


    titreCompteVar = StringVar()
    titreCompte = Label(root, textvariable = titreCompteVar, font = ("Courrier", 22), cursor = "hand2",pady=10)
    titreCompte.pack(side = TOP)

    notesCompte = Text(root,font = ("Courrier", 14), wrap='word', height = 15, undo = True, highlightthickness = 0) # entree notes
    notesCompte.pack(side=TOP,fill=BOTH)
    logoLeave = PhotoImage(file="logoLeave.png")
    leave = Button(root,image=logoLeave ,command = lambda: deconnexion(root = root))
    leave.place(x=892,y=10)

    modifier = Button(root, font = ("Courrier", 14), text="Modifier", state = "disabled",command = lambda:  modifCompte(_list))
    modifier.pack(side=BOTTOM)
    
    modTCompte()
    
    #root.bind("<Any-Motion>",test) pour le temps avant déconnexion, prbl : il est bcp trop actif
    
    root.bind("<Double-d>",deco)
    _list.bind("<Double-t>",deco)
    root.bind("<Double-r>",refresh)
    root.bind("<Configure>",adapt_all)
    _list.bind("<Any-Key>",changeFocusWithLetter)
    _list.bind("<Any-KeyRelease>",modTCompte)
    _list.bind("<Any-ButtonRelease>",modTCompte)
    _list.bind("<BackSpace>", deleteEvent)
    _list.bind("<Delete>", deleteEvent)
    _list.bind("<Any-MouseWheel>",scrollY)
    _list.bind("<"+controlKey+"-x>", copierMdpEvent)       #copy password with cmd + X or crtl + X
    _list.bind("<"+controlKey+"-b>", copierUserEvent)      #copy username with cmd + B or crtl + B
    _list.bind("<"+controlKey+"-u>", copierURLEvent)      #copy URL with cmd + U or crtl + U
    _list.bind("<Return>", openURLEvent)                #open URL with enter
    _list.bind("<Double-Button-1>", openURLEvent)       #open URL with double click
    titreCompte.bind("<Button-1>",openURLEvent)         #open URL with click on the title

    addButton = Button(listFrame,text = trad("Ajouter un compte"), command = ajoutCompte)
    addButton.pack(side = BOTTOM)

    
chargerInfos()
connexion()


