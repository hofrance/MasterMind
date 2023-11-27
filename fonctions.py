import random
import datetime

# Fonctions auxiliaires pour la logique du jeu

def verifier_liste_unique(liste):
    """ Vérifie si tous les éléments de la liste sont uniques. """
    return len(liste) == len(set(liste))

def generer_nombre(n):
    """ Génère un nombre aléatoire avec des chiffres uniques. """
    chiffres = list(range(10))
    random.shuffle(chiffres)
    notreListe=chiffres[:n]
    return notreListe

# On interagit avec l'utilisateur ---> Richard

def demander_nombre_utilisateur(n):
    """ Demande à l'utilisateur de saisir un nombre. """
    while True:
        try:
            saisie = input("Devinez le nombre: ")
            if not saisie.isdigit() or len(saisie) != n or not verifier_liste_unique(list(saisie)) :
                print(f"L'expression {saisie} n'est pas correcte.")
                continue #on recommence au debut de la boucle

            lesChiffrerentrees=[int(chiffre) for chiffre in saisie]
            return lesChiffrerentrees
        except ValueError:
            print("Entrée non valide, réessayez.")

def afficher_indication(nombre_secret, tentative):
    """ Affiche des indications sur la tentative de l'utilisateur. """
    if nombre_secret == tentative:
        return "Gagné", True
    indication = ""
    for i, chiffre in enumerate(tentative):
        if chiffre in nombre_secret:  #si le chiffre est présent
            if nombre_secret[i] == chiffre: #si le chiffre est au bon endroit
                indication += "="
            else:
                indication +="-" #si le chiffre est au mauvais endroit
        else:
            indication += "*" #le chiffre n'est pas present
    return indication, False #on retourne un tulpe

# Gestion des scores

def lire_dernier_score():
    """ Lit le dernier score à partir d'un fichier. """
    try:
        with open("masterMind.txt", "r") as file:
            for last_line in file:
                pass
            return last_line.strip()
    except Exception:
        return None

def enregistrer_score(score,niveauDifficute,nomJoueur):
    heureExacteDuScore =   datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    """ Enregistre le score dans un fichier. """
    try:
        with open("masterMind.txt", "a") as file:
            file.write(f"Pseudo:{nomJoueur} | Niveau:{niveauDifficute} | Score:{score} | Date:{heureExacteDuScore}\n")

    except IOError as e:
        print("Erreur lors de l'enregistrement du score")

# Choix du niveau de difficulté

def choixDuNiveauDeDifficulte():
    """ Permet à l'utilisateur de choisir un niveau de difficulté. """
    difficulte_max = 9
    difficulte_min = 1
    while True:
        try:
            choix = input(f"Veuillez choisir un niveau de difficulté entre {difficulte_min} et {difficulte_max}: ")
            if not choix.isdigit():
                print(f"L'expression '{choix}' n'est pas un nombre valide.")
                continue
            decision = int(choix)
            if difficulte_min <= decision <= difficulte_max:
                return decision
            else:
                print(f"Le nombre doit être compris entre {difficulte_min} et {difficulte_max}.")
        except ValueError:
            print("Entrée non valide, réessayez.")

# Fonction pour demander si l'utilisateur veut rejouer

def rejouer():
    """ Demande à l'utilisateur s'il souhaite rejouer. """
    while True:
        try:
            choix = input("Voulez-vous rejouer ? (oui = 1 / non = 0): ")
            if not choix.isdigit() or len(choix) != 1:
                print(f"Veuillez saisir '1' pour oui ou '0' pour non.")
                continue
            decision = int(choix)
            if decision == 1:
                print("Vous avez décidé de relancer une partie.")
                return True
            elif decision == 0:
                print("Merci d'avoir joué, à la prochaine.")
                return False
        except ValueError:
            print("Entrée non valide, réessayez.")

# Fonction principale du jeu

def jouer():
    nomJoueur=input("saisir votre pseudo pour le game")
    niveau_difficulte=choixDuNiveauDeDifficulte()
    dernier_score = lire_dernier_score()
    if dernier_score:
        print(f"Le dernier score est: {dernier_score}")
    else:
        print("Aucun historique de score trouvé. Nouvelle partie.")

    nombre_secret = generer_nombre(niveau_difficulte)
    #print(nombre_secret) decommenté pour voir le chiffre mystère
    essais_max = 9

    for essai in range(essais_max):
        print(f"Tentative {essai + 1} sur {essais_max}")
        tentative = demander_nombre_utilisateur(niveau_difficulte)
        indication, gagne = afficher_indication(nombre_secret, tentative)
        print(indication)
        if gagne:
            print(f"Bravo ! Vous avez trouvé en {essai + 1} essais.")
            #petite logique  d'attribution du score
            score=(str((10-essai)*10))+"%"
            enregistrer_score(score,niveau_difficulte,nomJoueur)
            break
    else:
        print(f"Dommage ! Le nombre était {nombre_secret}.")



def afficher_bienvenue():
    print("""
==================================================
||     Richard et Sedra vous présente le jeu    ||
||           le Master Mind version             ||
||                                              ||
||    Devinez le nombre secret et gagnez !      ||
||                                              ||
==================================================
||      Règles du Jeu :                         ||
||      1. Choisissez un niveau de difficulté   ||
||      2. Devinez un nombre avec des chiffres  ||
||         uniques                              ||
||      3. Recevez des indices après chaque     ||
||         tentative :                          ||
||         "=" signifie bon chiffre et place,   ||
||         "-" signifie bon chiffre, mauvaise   ||
||         place, "*" signifie chiffre absent   ||
||      4. Vous avez 9 tentatives               ||
==================================================
||      Bonne chance !                          ||
==================================================
    """)
