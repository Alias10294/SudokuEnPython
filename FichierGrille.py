# IMPORTS
from FichierCase import Case
from random import shuffle
from math import sqrt

class Grille:
    # CHAMPS
    sousTaille:int
    taille:int
    cases:list
    numeros:list

    # METHODES
    def NumeroPossibleLigne(self, numero:str, i:int) -> bool:
        """
        Retourne True si le numero 'numero' peut etre entre dans la ligne 'i', sinon False.
        """
        case:Case
        resultat:bool

        resultat = True
        for case in self.cases[i]:
            if case.numero == numero:
                resultat = False
                break
        return resultat

    def NumeroPossibleColonne(self, numero:str, j:int) -> bool:
        """
        Retourne True si le numero 'numero' peut etre entre dans la colonne 'j', sinon False.
        """
        i:int
        resultat:bool

        resultat = True
        for i in range(self.taille):
            if self.cases[i][j].numero == numero:
                resultat = False
                break
        return resultat

    def NumeroPossibleSousGrille(self, numero:str, i:int, j:int) -> bool:
        """
        Retourne True si le numero 'numero' peut etre entre dans la sous-grille de la case de coordonnees 'i' et 'j', sinon False.
        """
        resultat:bool
        ligneDebut:int
        colonneDebut:int
        i2:int
        j2:int

        # On trouve d'abord le coin en haut à gauche de la sous-grille 
        resultat = True
        ligneDebut = self.sousTaille * (i // self.sousTaille)
        colonneDebut = self.sousTaille * (j // self.sousTaille)
        
        for i2 in range(ligneDebut, ligneDebut + self.sousTaille):
            for j2 in range(colonneDebut, colonneDebut + self.sousTaille):
                if self.cases[i2][j2].numero == numero:
                    resultat = False
                    break
        return resultat

    def NumeroPossible(self, numero:str, i:int, j:int) -> bool:
        """
        Retourne True si le numero 'numero' peut etre entre dans la case de coordonnees 'i' et 'j', sinon False.
        """
        resultatLigne:bool
        resultatColonne:bool
        resultatSousGrille:bool
        resultat:bool

        resultatLigne = self.NumeroPossibleLigne(numero, i)
        resultatColonne = self.NumeroPossibleColonne(numero, j)
        resultatSousGrille = self.NumeroPossibleSousGrille(numero, i, j)
        resultat = resultatLigne and resultatColonne and  resultatSousGrille
        return resultat
    
    def TrouverCoordonneesCaseVide(self) -> list:
        """
        Retourne les coordonnees 'i' et 'j' de la premiere case sans numero dans le tableau, sinon None.
        """
        i:int
        j:int
        resultat:tuple

        resultat = []
        for i in range(self.taille):
            for j in range(self.taille):
                if self.cases[i][j].numero == "0":
                    resultat = [i, j]
        return resultat

    def SeRemplir(self) -> bool:
        """
        Remplit les cases selon les regles du sudoku.
        """
        resultat:bool
        coordonneesCase:list
        i:int
        j:int
        numeros:list
        numero:int

        resultat = False
        coordonneesCase = self.TrouverCoordonneesCaseVide()
        if coordonneesCase == []:
            resultat = True
        else:
            i = coordonneesCase[0]
            j = coordonneesCase[1]
            numeros = self.numeros.copy()
            shuffle(numeros)
            
            for numero in numeros:
                if self.NumeroPossible(numero, i, j):
                    self.cases[i][j].Initialiser(numero)
                    if self.SeRemplir():
                        resultat = True
                        break
                    else:
                        self.cases[i][j].Initialiser("0")
        return resultat
    
    def AfficherConsole(self) -> None:
        """
        Affiche les numeros des cases dans la console.
        """
        ligneHorizontale:str
        i:int
        j:int

        ligneHorizontale = "-" * (2 * self.sousTaille + 1) + "-" * (2 * self.taille)
        for i in range(self.taille):
            if (i % self.sousTaille) == 0:
                print(ligneHorizontale)
            for j in range(self.taille): 
                if (j % self.sousTaille) == 0: 
                    print("| ", end = "")
                numero = self.cases[i][j].numero
                if numero != "0": # N'affiche que les numeros des cases pleines
                    print(f"{numero} ", end = "")
                else:
                    print("  ", end = "")
            print("|")
        print(ligneHorizontale)
    
    def NombreSolutions(self) -> int:
        """
        Retourne le nombre de solutions differentes à la grille.
        """
        resultat:int
        coordonneesCase:list
        i:int
        j:int
        numeros:list
        numero:str

        resultat = 0
        coordonneesCase = self.TrouverCoordonneesCaseVide()
        if coordonneesCase == []:
            resultat += 1
        else:
            i = coordonneesCase[0]
            j = coordonneesCase[1]
            numeros = self.numeros.copy()
            shuffle(numeros)

            for numero in numeros:
                if self.NumeroPossible(numero, i, j):
                    self.cases[i][j].numero = numero
                    resultat += self.NombreSolutions()
                    self.cases[i][j].numero = "0"
        return resultat
    
    def EstUnique(self) -> bool:
        """
        Retourne True si il n'y a qu'une seule solution à la grille de sudoku actuelle, sinon False.
        """
        return self.NombreSolutions() == 1

    def NombresARetirer(self, difficulte:int) -> int:
        """
        Retourne le nombre de chiffres a retirer selon la difficulte 'difficulte' et la taille de la grille.
        """
        nombreARetirer:int

        nombreARetirer = 1 # Au cas ou
        match self.sousTaille:
            case 2:
                nombreARetirer = 16
            case 3:
                listeNombreARetirer = [32, 42, 52]
                nombreARetirer = listeNombreARetirer[difficulte - 1]
            case 4:
                listeNombreARetirer = [90, 100, 110, 120]
                nombreARetirer = listeNombreARetirer[difficulte - 1]
        return nombreARetirer
    
    def RetirerNombres(self, difficulte:int) -> None:
        """
        Vide des numeros des cases, en gardant la solution de la grille unique et selon la difficulte 'difficulte'.
        """
        coordonnees:list
        i:int
        j:int
        nombreRetire:int
        coordonnee:tuple
        numeroRetire:str

        coordonnees = []
        for i in range(self.taille):
            for j in range(self.taille):
                coordonnees.append((i, j))
        shuffle(coordonnees)

        nombreRetire = 0
        nombreARetirer = self.NombresARetirer(difficulte)
        for coordonnee in coordonnees:
            i = coordonnee[0]
            j = coordonnee[1]
            numeroRetire = self.cases[i][j].Vider()
            if not self.EstUnique():
                self.cases[i][j].numero = numeroRetire
                self.cases[i][j].estOrigine = True
            else:
                nombreRetire += 1
            if nombreRetire == nombreARetirer:
                break

    # CONSTRUCTEURS
    def __init__(self, identifiant:str) -> None:
        """
        Une grille de sudoku, avec une taille de sous-grille 'sousTaille' variable (taille de la grille: 'sousTaille' * 'sousTaille').

        """
        i:int
        j:int

        self.sousTaille = int(identifiant[1]) + 1
        self.taille = self.sousTaille * self.sousTaille
        self.cases = [[Case(identifiant[8:][self.taille * i + j]) for j in range(self.taille)] for i in range(self.taille)]
        self.numeros = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G"][: self.taille]
        match identifiant[0]:
            case "1":
                self.SeRemplir()
                self.RetirerNombres(int(identifiant[2]))
            case "2":
                pass
