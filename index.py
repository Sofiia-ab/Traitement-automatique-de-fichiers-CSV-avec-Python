#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, re, sys

donnees = {} 
colonnes_finales = ["","HAI724I", "HAI726I", "HAI723I", "ingrédients", "difficulté"] #[, = "nom étudiant"]

def parcours (repertoire) : 
    liste = os.listdir(repertoire) 
    for fichier in liste :
        if os.path.isdir(repertoire +"/"+ fichier) : 
            parcours(repertoire +"/"+ fichier) # explorer le sous dossier (resursivement)
        else :
            data = fichier.split(".") 
            if len(data) > 1 and data [-1] == "csv" :
                lire(repertoire +"/"+ fichier) 
                print(fichier)

def lire(fichier): 
    fd = open(fichier, 'r') 

    lignes = fd.readlines() # La commande fd.readlines() lit toutes les lignes du fichier.+ stocke ttes les lignes du fichier dans une LISTE
    nombre_de_lignes = len(lignes)  

    #Extraction des noms de colonnes 
    entetes = lignes[0] # entêtes
    entetes = entetes.strip() 
    entetes = entetes.replace(";" ,",") 
    entetes = re.sub(" +,", ",", entetes) 
    entetes = re.sub(", +", ",", entetes)
    noms_de_colonnes = entetes.split(",") 

    #Traitement des lignes restantes
    for i in range(1, nombre_de_lignes):
        ligne_valeurs = lignes[i] # Récupère la ligne correspondant à l'indice i 
        valeurs = ligne_valeurs.strip().replace(";" ,",").split(",")
         
        valeur_premiere_colonne = " ".join(sorted(valeurs[0].strip().lower().split())) #création d'une clé unique à partir de la deuxieme ligne du fichier 
        if valeur_premiere_colonne not in donnees: 
            donnees_pour_valeur = {} 
            for j in range(len(noms_de_colonnes)): 
                donnees_pour_valeur[noms_de_colonnes[j]] = valeurs[j] 
            donnees[valeur_premiere_colonne] = donnees_pour_valeur 
        else: 
            donnees_pour_valeur = donnees[valeur_premiere_colonne] # recupere le sous-dict associé à cette clé pour le compléter
            for j in range(len(noms_de_colonnes)):
                if noms_de_colonnes[j] not in donnees_pour_valeur:
                    donnees_pour_valeur[noms_de_colonnes[j]] = valeurs[j]
     
    for i in range(1, len(noms_de_colonnes)): 
        if noms_de_colonnes[i] not in colonnes_finales:  
            colonnes_finales.append(noms_de_colonnes[i])

    for ligne in fd.readlines(): # ligne = "12;15;14"
        data = ligne.strip().replace(";" ,",").split(",") 
        if len(data) > 0:  # Vérifie si la ligne contient des données
            donnees.append(data)  

    fd.close() 
    return donnees 

def affiche(donnees): 
    for clef in donnees:
        print("'", clef, "': ", donnees[clef], sep ="")

def resultat(fichier_sortie, donnees, colonnes_finales) :
    fd = open(fichier_sortie, 'w') 
    fd.write(",".join(colonnes_finales) + "\n")  

    for clef, valeurs in donnees.items(): 
        ligne = [clef]  # Ajouter la clé unique (étudiant ou dessert)
        for colonne in colonnes_finales [1:]: 
            ligne.append(valeurs.get(colonne, "")) #ici on récupere chaque valeur de la colonne d'entête et si la valeur n'existe pas, on va mettre rien c'est a dire vide.
        fd.write(",".join(ligne) + "\n") 
    fd.close() 

if len(sys.argv) > 2: 
    parcours(sys.argv[1]) 
    affiche(donnees)
    fichier_sortie = sys.argv[2] 
    resultat(fichier_sortie, donnees,colonnes_finales)
    print(f"Fichier {fichier_sortie} créé avec succès.")
else :
    print(f"Erreur : Aucun fichier n'a été créé.")
