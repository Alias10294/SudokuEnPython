# IMPORTS
from FichierAffichageBoutonCirc import AffichageBoutonCirc
from pygame import image, display, draw, transform
from math import sqrt

class BoutonCirc:
    # CHAMPS
    centre:tuple
    affichage:AffichageBoutonCirc
    logo:image
    active:bool

    # METHODES
    def Interagit(self, positionSouris:tuple) -> bool:
        """
        Verifie si la souris de position 'positionSouris' se trouve sur le bouton.
        """
        distance:int

        distance = int(sqrt((self.centre[0] - positionSouris[0])**2 + (self.centre[1] - positionSouris[1])**2))
        return distance <= self.affichage.rayon

    def MettreAJourCoeffInteraction(self, positionSouris:tuple) -> float:
        """
        Met a jour le coeffcient de taille pour l'interaction selon la position de la souris 'positionSouris'.
        """
        return 1 + int(self.Interagit(positionSouris) or self.active) * self.affichage.coeffInteraction

    def Charger(self, fenetre:display, positionSouris:tuple) -> None:
        """
        Charge le bouton dans la fenetre 'fenetre', selon si la souris de position 'positionSouris' est sur le bouton.
        """
        coeffInteraction:float

        coeffInteraction = self.MettreAJourCoeffInteraction(positionSouris)
        rayon = self.affichage.rayon * coeffInteraction
        draw.circle(fenetre, self.affichage.couleur, self.centre, rayon)
        draw.circle(fenetre, self.affichage.bordCouleur, self.centre, rayon, self.affichage.bordEpaisseur)

        logo = transform.scale_by(self.logo, coeffInteraction)
        positionLogo = logo.get_rect(center = self.centre)
        fenetre.blit(logo, positionLogo)

    # CONSTRUCTEURS
    def __init__(self, centre:tuple, logo:image) -> None:
        """
        Un bouton circulaire.
        """
        self.centre = centre
        self.affichage = AffichageBoutonCirc()
        self.logo = logo
        self.active = False