# IMPORTS
from FichierAffichageErreurs import AffichageErreurs
from pygame import display, draw, font

class Erreurs:
    # CHAMPS
    affichage:AffichageErreurs
    nbErreurs:int
    nbErreursMax:int
    police:font.Font
    titrePolice:font.Font

    # METHODES
    def Charger(self, fenetre:display) -> None:
        """
        Charge le nombre d'erreurs a l'ecran.
        """
        draw.circle(fenetre, self.affichage.couleur, self.affichage.centre, self.affichage.rayon)
        draw.circle(fenetre, self.affichage.bordCouleur, self.affichage.centre, self.affichage.rayon, self.affichage.bordEpaisseur)

        texte = self.police.render(f"{self.nbErreurs} / {self.nbErreursMax}", True, self.affichage.texteCouleur)
        textePosition = texte.get_rect(center=self.affichage.centre)
        fenetre.blit(texte, textePosition)
        texte = self.titrePolice.render("Erreurs", True, self.affichage.titreTexteCouleur)
        textePosition = texte.get_rect(center=self.affichage.centre)
        textePosition[1] -= self.affichage.policeTaille * 4 / 5
        fenetre.blit(texte, textePosition)

    def __init__(self, difficulte:int, nbErreurs = 0, affichage:AffichageErreurs = AffichageErreurs()) -> None:
        """
        Represente les erreurs faites dans une partie de sudoku.
        """
        self.affichage = affichage
        self.nbErreurs = nbErreurs
        self.nbErreursMax = 6 - difficulte
        self.police = font.Font(self.affichage.policeNom, self.affichage.policeTaille)
        self.titrePolice = font.Font(self.affichage.policeNom, self.affichage.titrePoliceTaille)