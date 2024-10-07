# IMPORTS
from pygame import *
from FichierMenuABoutons import MenuABoutons
from FichierPartie import Partie

class Jeu:
    """
     Un jeu de sudoku genial !
    """
    # CHAMPS
    fenetre:display
    tailleFenetre:tuple
    menuDepart:MenuABoutons
    menuTailleGrille:MenuABoutons
    menuDifficulte3x3:MenuABoutons
    menuDifficulte4x4:MenuABoutons
    partie:Partie
    menuRejouer:MenuABoutons
    couleurActuelle:tuple

    # METHODES
    def CreerIdentifiant(self, choixJeu:int) -> str:
        """
        [ Entree(s): choixJeu:int ]
        [ Sortie(s): :str ]
        -> Retourne un identifiant qui permet de generer une partie de sudoku selon les parametres encryptes dans 'choixJeu'.
.        """
        return str(choixJeu) + ("0" * 4) + "0" + ("0" * ((choixJeu % 100 // 10 + 1) ** 4))

    def ModifierCouleur(self, couleur:tuple) -> None:
        """
        [ Entree(s): couleur:tuple ]
        [ Sortie(s): N/A ]
        -> Modifie la couleur des textes dans le jeu a la couleur desiree.
        """
        self.couleurActuelle = couleur
        self.menuDepart.affichageBouton.texteCouleur = couleur
        self.menuTailleGrille.affichageBouton.texteCouleur = couleur
        self.menuDifficulte3x3.affichageBouton.texteCouleur = couleur
        self.menuDifficulte4x4.affichageBouton.texteCouleur = couleur
        self.menuRejouer.affichageBouton.texteCouleur = couleur
        self.menuCharger.affichageBouton.texteCouleur = couleur
        self.menuOptions.affichageBouton.texteCouleur = couleur
        self.menuCouleur.affichageBouton.texteCouleur = couleur

    def Jouer(self) -> None:
        """
        [ Entree(s): N/A ]
        [ Sortie(s): N/A ]
        -> Fonction principale, qui permet de jouer au jeu.
        """
        choixJeu:int
        identifiantPartie:str

        init()
        font.init()
        choixJeu = 0
        while choixJeu >= 0:
            match choixJeu:
                case 0: # Menu de depart
                    choixJeu = self.menuDepart.Jouer(self.fenetre, self.tailleFenetre)
                case 1: # Nouvelle partie, choix de difficulte
                    choixJeu = self.menuTailleGrille.Jouer(self.fenetre, self.tailleFenetre)
                case 11: # Choix de taille de grille, taille 2x2
                    choixJeu = 113
                case 12: # Choix de taille de grille, taille 3x3
                    choixJeu = self.menuDifficulte3x3.Jouer(self.fenetre, self.tailleFenetre)
                case 13: # Choix de taille de grille, taille 4x4
                    choixJeu = self.menuDifficulte4x4.Jouer(self.fenetre, self.tailleFenetre)
                case 2: # Charger une partie, choisir la partie
                    choixJeu = self.menuOptions.Jouer(self.fenetre, self.tailleFenetre)
                case 21: # Choisir la couleur
                    choixJeu = self.menuCouleur.Jouer(self.fenetre, self.tailleFenetre)
                case 211: # Couleur bleue
                    self.ModifierCouleur((150, 150, 150))
                    choixJeu = 2
                case 212: # Couleur verte
                    self.ModifierCouleur((71, 153, 31))
                    choixJeu = 2
                case 213: # Couleur jaune
                    self.ModifierCouleur((230, 191, 0))
                    choixJeu = 2
                case 214: # Couleur orange
                    self.ModifierCouleur((217, 108, 0))
                    choixJeu = 2
                case 215: # Couleur violette
                    self.ModifierCouleur((91, 17, 166))
                    choixJeu = 2
                case 3: # Quitter le jeu
                    choixJeu = -1
                case 51: # Finir une partie gagnée
                    self.menuRejouer.titreTexte = "PARTIE GAGNEE"
                    choixJeu = self.menuRejouer.Jouer(self.fenetre, self.tailleFenetre)
                case 52: # Finir une partie perdue
                    self.menuRejouer.titreTexte = "PARTIE PERDUE"
                    choixJeu = self.menuRejouer.Jouer(self.fenetre, self.tailleFenetre)
            if (choixJeu // 100) == 1:
                # Indices dans l'identifiant:
                # [0]: mode de generation (1: cree, 2: charge)
                # [1]: taille
                # [2]: difficulte
                # [3:6]: temps de depart en millisecondes
                # [7]: nombre d'erreurs actuel
                # [8:]: numeros de la grille
                identifiantPartie = self.CreerIdentifiant(choixJeu)
                self.partie = Partie(identifiantPartie)
                self.partie.ModifierCouleur(self.couleurActuelle)
                choixJeu = self.partie.Jouer(self.fenetre, self.tailleFenetre)
        quit()
        font.quit()

    # CONSTRUCTEURS
    def __init__(self):
        """
        [ Entree(s): N/A ]
        [ Sortie(s): :Jeu ]
        -> Un jeu de sudoku.
        """
        self.tailleFenetre = (1536, 864)
        self.fenetre = display.set_mode(self.tailleFenetre)
        self.menuDepart = MenuABoutons(["JOUER", "OPTIONS", "QUITTER"], [1, 2, 3, ], "SUDOKU")
        self.menuTailleGrille = MenuABoutons(["2 X 2", "3 X 3", "4 X 4"], [11, 12, 13], "")
        self.menuDifficulte3x3 = MenuABoutons(["FACILE", "MOYEN", "DIFFICILE"], [121, 122, 123], "")
        self.menuDifficulte4x4 = MenuABoutons(["FACILE", "MOYEN", "DIFFICILE", "EXPERT"], [131, 132, 133, 134], "")
        self.menuRejouer = MenuABoutons(["REJOUER", "DEPART", "QUITTER"], [1, 0, 4], "")
        self.menuCharger = MenuABoutons([""], [4], "CHARGER")
        self.menuOptions = MenuABoutons(["COULEUR", "DEPART"], [21, 0], "OPTIONS")
        self.menuCouleur = MenuABoutons(["GRIS", "VERT", "JAUNE", "ORANGE", "VIOLET"], [211, 212, 213, 214, 215], "COULEURS")
        self.couleurActuelle = (200, 200, 200)