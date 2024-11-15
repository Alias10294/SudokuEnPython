# IMPORTS
from pygame import Surface, draw, display, Rect, font
from FichierAffichageBoutonRect import AffichageBoutonRect

class BoutonRect:
    # CHAMPS
    position:list
    texte:str
    affichage:AffichageBoutonRect

    # METHODES
    def ChangerCouleur(self, couleur:list) -> None:
        self.affichage.texteCouleur = couleur

    def Interagit(self, positionSouris:tuple) -> bool:
        """
        [ Entree(s): positionSouris:tuple ]
        [ Sortie(s): :bool ]
        -> Gere l'interaction avec le bouton.
        Retourne True si la souris est sur le bouton, False sinon.
        """
        interactionX = positionSouris[0] > self.position[0] and positionSouris[0] < self.position[0] + self.affichage.taille[0]
        interactionY = positionSouris[1] > self.position[1] and positionSouris[1] < self.position[1] + self.affichage.taille[1]
        return interactionX and interactionY

    def MettreAJourCoeffInteraction(self, positionSouris:tuple) -> float:
        """
        [ Entree(s): positionSouris:tuple ]
        [ Sortie(s): :float ]
        -> Le bouton est agrandi lorsque la souris passe dessus.
        Retourne le coefficient a appliquer a la taille du bouton pour l'interaction.
        """
        return 1 + int(self.Interagit(positionSouris)) * self.affichage.coeffInteraction

    def Charger(self, fenetre:display, positionSouris:tuple) -> None:
        """
        [ Entree(s): fenetre:display, positionSouris:tuple ]
        [ Sortie(s): N/A ]
        -> Charge le bouton a l'ecran, en prenant en compte la position de la souris pour l'interaction.
        """
        coeffInteraction:float
        positionX:int
        positionY:int
        position:tuple
        tailleX:int
        tailleY:int
        taille:tuple
        policeBouton:font.Font
        texteBouton:Surface
        texteBoutonPosition:Rect

        # Affiche la forme du bouton
        coeffInteraction = self.MettreAJourCoeffInteraction(positionSouris)
        positionX = self.position[0] - (coeffInteraction - 1) * self.affichage.taille[0] / 2
        positionY = self.position[1] - (coeffInteraction - 1) * self.affichage.taille[1] / 2
        position = (positionX, positionY)
        tailleX = self.affichage.taille[0] * coeffInteraction
        tailleY = self.affichage.taille[1] * coeffInteraction
        taille = (tailleX, tailleY)
        draw.rect(fenetre, self.affichage.couleur, Rect(position, taille))
        draw.rect(fenetre, self.affichage.bordCouleur, Rect(position, taille), int(self.affichage.bordEpaisseur * coeffInteraction))

        # Affiche le texte du bouton
        policeBouton = font.Font(self.affichage.policeNom, int(self.affichage.policeTaille * coeffInteraction))
        texteBouton = policeBouton.render(self.texte, True, self.affichage.texteCouleur)
        texteBoutonPosition = texteBouton.get_rect(center = (positionX + tailleX / 2, positionY + tailleY / 2))
        fenetre.blit(texteBouton, texteBoutonPosition)

    # CONSTRUCTEURS
    def __init__(self, position:tuple, texte:str):
        """
        [ Entree(s): position:tuple, texte:str ]
        [ Sortie(s): :BoutonRect ]
        -> Un bouton rectangulaire, avec une position centrale et un texte inscrit.
        """
        self.position = position
        self.affichage = AffichageBoutonRect()
        self.texte = texte