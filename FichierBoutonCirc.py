# IMPORTS
from FichierAffichageBoutonCirc import AffichageBoutonCirc
from pygame import image, display, draw, transform
from math import sqrt

class BoutonCirc:
    """
    Un bouton circulaire.
    """
    # CHAMPS
    centre:tuple
    affichage:AffichageBoutonCirc
    logo:image
    active:bool

    # METHODES
    def Interagit(self, positionSouris:tuple) -> bool:
        """
        [ Entree(s): positionSouris:tuple ]
        [ Sortie(s): :bool ]
        -> Gere l'interaction avec le bouton.
        Retourne True si la souris est sur le bouton, False sinon.
        """
        distance:int

        distance = int(sqrt((self.centre[0] - positionSouris[0])**2 + (self.centre[1] - positionSouris[1])**2))
        return distance <= self.affichage.rayon

    def MettreAJourCoeffInteraction(self, positionSouris:tuple) -> float:
        """
        [ Entree(s): positionSouris:tuple ]
        [ Sortie(s): :float ]
        -> Le bouton est agrandi lorsque la souris passe dessus.
        Retourne le coefficient a appliquer a la taille du bouton pour l'interaction.
        """
        return 1 + int(self.Interagit(positionSouris) or self.active) * self.affichage.coeffInteraction

    def Charger(self, fenetre:display, positionSouris:tuple) -> None:
        """
        [ Entree(s): fenetre:display, positionSouris:tuple ]
        [ Sortie(s): N/A ]
        -> Charge le bouton a l'ecran, en prenant en compte la position de la souris pour l'interaction.
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
    def __init__(self, centre:tuple, logo:image):
        """
        [ Entree(s): centre:tuple, logo:image ]
        [ Sortie(s): :BoutonCirc ]
        -> Un bouton circulaire, avec une position centrale et un logo donne.
        """
        self.centre = centre
        self.affichage = AffichageBoutonCirc()
        self.logo = logo
        self.active = False