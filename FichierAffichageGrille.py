# IMPORTS
from pygame import font

class AffichageGrille:
    # CHAMPS
    position:tuple
    taille:int = 748
    bordCouleur:tuple = (200, 200, 200)
    bordEpaisseur:int = 2
    caseTaille:int
    police:font.Font
    policeCouleur:tuple = (150, 150, 150)
    policeCouleurBon:tuple = (50, 200, 50)
    policeCouleurFaux:tuple = (200, 50, 50)
    policeTaille:int 
    brouillonPolice:font.Font
    brouillonPoliceCouleur:tuple = (50, 50, 200)
    brouillonPoliceTaille:int