# IMPORTS
from pygame import *
from FichierAffichageBoutonRect import AffichageBoutonRect
from FichierBoutonRect import BoutonRect
from FichierAffichageTitre import AffichageTitre

class MenuABoutons:
    """
    Un menu a boutons rectangulaires customisable.
    """
    # CHAMPS
    fond:Surface
    texteBoutons:list
    nombreBoutons:int
    espaceEntreBoutons:int
    boutonTouchesClavier:list
    choixSorties:list
    affichageTitre:AffichageTitre
    titreTexte:str

    # METHODES
    def CreerBoutons(self, tailleFenetre:tuple) -> None:
        """
        [ Entree(s): tailleFenetre:tuple ]
        [ Sortie(s): N/A ]
        -> Cree tous les boutons du menu.
        """
        boutonPositionX:int
        hauteurBoutonsMoitie:int
        espaceTotalBoutonsMoitie:int
        boutonPositionY:int
        b:int
        boutonPosition:tuple

        self.boutons = []

        boutonPositionX = (tailleFenetre[0] - AffichageBoutonRect().taille[0]) // 2

        hauteurBoutonsMoitie = (self.nombreBoutons / 2) * AffichageBoutonRect().taille[1] # Espace a retirer pour la taille des boutons
        espaceTotalBoutonsMoitie = (self.nombreBoutons - 1) * self.espaceEntreBoutons / 2 # Espace a retirer pour l'espace entre les boutons
        boutonPositionY = tailleFenetre[1] / 2 - hauteurBoutonsMoitie - espaceTotalBoutonsMoitie
        for b in range(self.nombreBoutons):
            boutonPosition = (boutonPositionX, boutonPositionY)
            self.boutons.append(BoutonRect(boutonPosition, self.texteBoutons[b]))
            boutonPositionY += AffichageBoutonRect().taille[1] + self.espaceEntreBoutons
    
    def ChangerCouleurBoutons(self, couleur:list) -> None:
        """
        [ Entree(s): couleur:list ]
        [ Sortie(s): N/A ]
        -> Change les couleurs des boutons a celle desiree.
        """
        for bouton in self.boutons:
            bouton.affichage.texteCouleur = couleur

    def ChargerTitre(self, fenetre:display) -> None:
        """
        [ Entree(s): fenetre:display ]
        [ Sortie(s): N/A ]
        -> Charge le titre du menu.
        """
        police:font.Font
        texte:Surface
        textePosition:Rect

        police = font.Font(self.affichageTitre.policeNom, self.affichageTitre.policeTaille)
        texte = police.render(self.titreTexte, True, self.affichageTitre.texteCouleur)
        textePosition = texte.get_rect(center = self.affichageTitre.centre)
        fenetre.blit(texte, textePosition)

    def Charger(self, fenetre:display, positionSouris:tuple) -> None:
        """
        [ Entree(s): fenetre:display, positionSouris:tuple ]
        [ Sortie(s): N/A ]
        -> Charge le menu dans la fenetre 'fenetre' selon la position de la souris 'positionSouris'.
        """
        bouton:BoutonRect

        fenetre.blit(self.fond, (0, 0)) # Image de fond
        self.ChargerTitre(fenetre) 

        for bouton in self.boutons: 
            bouton.Charger(fenetre, positionSouris) # Boutons du menu
        display.update()
    
    def Jouer(self, fenetre:display, tailleFenetre:tuple) -> int:
        """
        [ Entree(s): fenetre:display, tailleFenetre:tuple ]
        [ Sortie(s): choixSortie:int ]
        -> Permet de jouer le menu.
        """
        fin:bool
        evenement:event
        positionSouris:tuple
        choixSortie:int

        # Creation des boutons
        self.CreerBoutons(tailleFenetre)
        
        # Deroulement 
        fin = False
        choixSortie = 0
        while not fin:
            positionSouris = mouse.get_pos()
            # Evenements
            for evenement in event.get():
                if evenement.type == QUIT: # Quitter le jeu avec la croix
                    choixSortie = 3
                    fin = True
                # Entrees au clavier
                elif evenement.type == KEYDOWN:
                    if evenement.key in self.boutonTouchesClavier[:self.nombreBoutons - 1]:
                        choixSortie = self.boutonTouchesClavier.index(evenement.key)
                    elif evenement.key == K_ESCAPE or evenement.key == K_0 or evenement.key == K_q: # Quitter le jeu
                        choixSortie = 3 
                    fin = True
                # Choix du bouton avec la souris
                elif evenement.type == MOUSEBUTTONUP:
                    for bouton in self.boutons:
                        if bouton.Interagit(positionSouris):
                            choixSortie = self.choixSorties[self.boutons.index(bouton)]
                    fin = True
            # Affichage
            self.Charger(fenetre, positionSouris)
        return choixSortie

    # CONSTRUCTEURS
    def __init__(self, texteBoutons:list, choixSorties:list, titreTexte:str):
        """
        [ Entree(s): texteBoutons:list, choixSorties:list, titreTexte:str ]
        [ Sortie(s): :MenuABoutons ]
        -> Un menu comprenant des boutons et des sorties choisies.
        """
        self.fond = image.load("fond.png")
        self.boutons = []
        self.texteBoutons = texteBoutons
        self.nombreBoutons = len(texteBoutons)
        self.espaceEntreBoutons = 50
        self.boutonTouchesClavier = [K_1, K_2, K_3, K_4, K_5, K_6, K_8, K_9][:self.nombreBoutons]
        self.choixSorties = choixSorties
        self.affichageTitre = AffichageTitre()
        self.titreTexte = titreTexte