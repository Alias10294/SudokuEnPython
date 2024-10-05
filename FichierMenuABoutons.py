# IMPORTS
from pygame import *
from FichierAffichageBoutonRect import AffichageBoutonRect
from FichierBoutonRect import BoutonRect
from FichierAffichageTitre import AffichageTitre

class MenuABoutons:
    # CHAMPS
    fond:Surface
    affichageBouton:AffichageBoutonRect
    texteBoutons:list
    nombreBoutons:int
    espaceEntreBoutons:int
    boutonTouchesClavier:list
    choixSorties:list
    affichageTitre:AffichageTitre
    titreTexte:str

    # METHODES
    def CreerBoutons(self, tailleFenetre) -> None:
        """
        Cree tous les boutons du menu.
        """
        boutonPositionX:int
        hauteurBoutonsMoitie:int
        espaceTotalBoutonsMoitie:int
        boutonPositionY:int
        b:int
        boutonPosition:tuple

        self.boutons = []

        boutonPositionX = (tailleFenetre[0] - self.affichageBouton.taille[0]) // 2

        hauteurBoutonsMoitie = (self.nombreBoutons / 2) * self.affichageBouton.taille[1] # Espace a retirer pour la taille des boutons
        espaceTotalBoutonsMoitie = (self.nombreBoutons - 1) * self.espaceEntreBoutons / 2 # Espace a retirer pour l'espace entre les boutons
        boutonPositionY = tailleFenetre[1] / 2 - hauteurBoutonsMoitie - espaceTotalBoutonsMoitie
        for b in range(self.nombreBoutons):
            boutonPosition = (boutonPositionX, boutonPositionY)
            self.boutons.append(BoutonRect(boutonPosition, self.affichageBouton, self.texteBoutons[b]))
            boutonPositionY += self.affichageBouton.taille[1] + self.espaceEntreBoutons
    
    def ChargerTitre(self, fenetre:display) -> None:
        """
        Charge le titre du menu.
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
        Charger le menu dans la fenetre 'fenetre' selon la position de la souris 'positionSouris'.
        """
        bouton:BoutonRect

        fenetre.blit(self.fond, (0, 0)) # Image de fond
        self.ChargerTitre(fenetre) 

        for bouton in self.boutons: 
            bouton.Charger(fenetre, positionSouris) # Boutons du menu
        display.update()
    
    def Jouer(self, fenetre, tailleFenetre) -> int:
        """
        Permet de jouer le menu.
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
    def __init__(self, texteBoutons:list, choixSorties:list, titreTexte):
        """
        Un menu comprenant des boutons et des sorties choisies.
        """
        self.fond = image.load("fond.png")
        self.affichageBouton = AffichageBoutonRect()
        self.texteBoutons = texteBoutons
        self.nombreBoutons = len(texteBoutons)
        self.espaceEntreBoutons = 50
        self.boutonTouchesClavier = [K_1, K_2, K_3, K_4, K_5, K_6, K_8, K_9][:self.nombreBoutons]
        self.choixSorties = choixSorties
        self.affichageTitre = AffichageTitre()
        self.titreTexte = titreTexte