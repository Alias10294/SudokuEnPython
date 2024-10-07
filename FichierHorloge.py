# IMPORTS
import time
from pygame import display, draw, Rect, image, font, Surface
from FichierAffichageHorloge import AffichageHorloge

class Horloge:
    """
    Une horloge de jeu de sudoku.
    """
    # CHAMPS
    depart:float
    debut:float
    actuel:float
    affichage:AffichageHorloge

    # METHODES
    def MettreAJourTemps(self) -> None:
        """
        [ Entree(s): N/A ]
        [ Sortie(s): N/A ]
        -> Met à jour le temps actuel de l'horloge.
        """
        self.actuel = self.depart + time.time() - self.debut
    
    def ChargerCircs(self, fenetre:display) -> None:
        """
        [ Entree(s): fenetre:display ]
        [ Sortie(s): N/A ]
        -> Charge les bords circulaires de l'affichage de l'horloge.
        """
        centreCercleY:int
        centreCercleX:int

        centreCercleY = self.affichage.centre[1]
        # Cercle gauche
        centreCercleX = self.affichage.centre[0] - self.affichage.taille[0] / 2 + self.affichage.taille[1] / 2
        draw.circle(fenetre, self.affichage.couleur, [centreCercleX, centreCercleY], self.affichage.taille[1] / 2)
        draw.circle(fenetre, self.affichage.bordCouleur, [centreCercleX, centreCercleY], self.affichage.taille[1] / 2, self.affichage.bordEpaisseur)
        # Cercle droit
        centreCercleX = self.affichage.centre[0] + self.affichage.taille[0] / 2 - self.affichage.taille[1] / 2
        draw.circle(fenetre, self.affichage.couleur, [centreCercleX, centreCercleY], self.affichage.taille[1] / 2)
        draw.circle(fenetre, self.affichage.bordCouleur, [centreCercleX, centreCercleY], self.affichage.taille[1] / 2, self.affichage.bordEpaisseur)
    
    def ChargerRect(self, fenetre:display) -> None:
        """
        [ Entree(s): fenetre:display ]
        [ Sortie(s): N/A ]
        Charge le rectangle central de l'affichage de l'horloge.
        """
        positionX:int
        positionY:int
        position:list
        tailleX:int
        taille:list
        positionFinX:int
        positionFin:list

        # Fond du rectangle
        positionX = self.affichage.centre[0] - self.affichage.taille[0] / 2 + self.affichage.taille[1] / 2
        positionY = self.affichage.centre[1] - self.affichage.taille[1] / 2 + self.affichage.bordEpaisseur / 2 - 1
        position = [positionX, positionY]
        tailleX = self.affichage.taille[0] - self.affichage.taille[1]
        taille = [tailleX, self.affichage.taille[1] - self.affichage.bordEpaisseur]
        draw.rect(fenetre, self.affichage.couleur, Rect(position, taille))
        # Ligne du haut
        positionFinX = self.affichage.centre[0] + self.affichage.taille[0] / 2 - self.affichage.taille[1] / 2 
        positionFin = [positionFinX, positionY]
        draw.line(fenetre, self.affichage.bordCouleur, position, positionFin, self.affichage.bordEpaisseur)
        # Ligne du bas
        position[1] += self.affichage.taille[1] - self.affichage.bordEpaisseur
        positionFin[1] += self.affichage.taille[1] - self.affichage.bordEpaisseur
        draw.line(fenetre, self.affichage.bordCouleur, position, positionFin, self.affichage.bordEpaisseur)
    
    def ChargerLogo(self, fenetre:display) -> None:
        """
        [ Entree(s): fenetre:display ]
        [ Sortie(s): N/A ]
        Charge le logo de l'affichage de l'horloge.
        """
        logo:Surface
        centreLogoX:int
        centreLogo:tuple
        positionLogo:Rect

        logo = image.load(self.affichage.logo)
        centreLogoX = self.affichage.centre[0] - self.affichage.taille[0] / 2 + self.affichage.taille[1] / 2
        centreLogo = (centreLogoX, self.affichage.centre[1])
        positionLogo = logo.get_rect(center = centreLogo)
        fenetre.blit(logo, positionLogo)
    
    def ChargerTemps(self, fenetre:display) -> None:
        """
        [ Entree(s): fenetre:display ]
        [ Sortie(s): N/A ]
        Charge le temps à afficher.
        """
        temps:float
        minutes:int
        secondes:float
        police:font.Font
        texte:Surface
        textePositionX:int
        textePositionY:int
        textePosition:tuple

        temps = round(self.actuel, 3)
        minutes = temps // 60
        secondes = temps % 60
        police = font.Font("good times rg.otf", 30)
        texte = police.render(f"{int(minutes)}:{secondes}"[:7], True, (0, 0, 0))
        textePositionX = self.affichage.centre[0] - 70
        textePositionY = self.affichage.centre[1] - 18
        textePosition = (textePositionX, textePositionY)
        fenetre.blit(texte, textePosition)
        
    def Charger(self, fenetre:display) -> None:
        """
        [ Entree(s): fenetre:display ]
        [ Sortie(s): N/A ]
        Charge l'horloge sur la fenetre.
        """
        self.ChargerCircs(fenetre)
        self.ChargerRect(fenetre)
        self.ChargerLogo(fenetre)
        self.MettreAJourTemps()
        self.ChargerTemps(fenetre)
        
    # CONSTRUCTEURS
    def __init__(self, depart:float = 0., affichageHorloge:AffichageHorloge = AffichageHorloge()):
        """
        [ Entree(s): depart:float = 0., affichageHorloge:AffichageHorloge = AffichageHorloge() ]
        [ Sortie(s): :Horloge ]
        -> Une horloge avec un temps de depart et des donnees d'affichage.
        """
        self.depart = depart
        self.debut = time.time()
        self.actuel = self.depart + time.time() - self.debut
        self.affichage = affichageHorloge
