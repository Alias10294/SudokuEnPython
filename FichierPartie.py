# IMPORTS
from pygame import *
from FichierGrille import Grille
from FichierCase import Case
from FichierAffichageGrille import AffichageGrille
from FichierBoutonCirc import BoutonCirc
from FichierHorloge import Horloge
from FichierErreurs import Erreurs

class Partie:
    # CHAMPS
    fond:image
    grille:Grille
    affichageGrille:AffichageGrille
    coordonneesCaseEditee:tuple
    boutonsEdition:list
    modeEdition:bool # True pour Edition, False pour Brouillon
    horloge:Horloge
    erreurs:Erreurs

    # METHODES
    def ModifierCouleur(self, couleur:tuple):
        bouton:BoutonCirc

        self.affichageGrille.policeCouleur = couleur

    def sourisSurGrille(self, positionSouris:tuple) -> bool:
        """
        Verifie si la souris de position 'positionSouris' se trouve sur la grille de sudoku.
        """ 
        sourisApresDebutGrilleX:bool
        sourisApresDebutGrilleY:bool
        sourisDepasseGrilleX:bool
        sourisDepasseGrilleY:bool
        sourisSurGrilleX:bool
        sourisSurGrilleY:bool

        sourisApresDebutGrilleX = positionSouris[0] > self.affichageGrille.position[0] + 2
        sourisApresDebutGrilleY = positionSouris[1] > self.affichageGrille.position[1] + 2
        sourisDepasseGrilleX = positionSouris[0] < self.affichageGrille.position[0] + self.affichageGrille.taille - 2
        sourisDepasseGrilleY = positionSouris[1] < self.affichageGrille.position[1] + self.affichageGrille.taille - 2
        sourisSurGrilleX = sourisApresDebutGrilleX and sourisDepasseGrilleX
        sourisSurGrilleY = sourisApresDebutGrilleY and sourisDepasseGrilleY
        return sourisSurGrilleX and sourisSurGrilleY

    def choisirCase(self, positionSouris:tuple) -> None:
        """
        Determine la case ou la souris de position 'positionSouris' se trouve.
        """
        i:int
        j:int

        j = 0
        while positionSouris[0] > self.trouverPositionCase((0, j + 1))[0]:
            j += 1
        i = 0
        while positionSouris[1] > self.trouverPositionCase((i + 1, 0))[1]:
            i += 1
        if self.grille.cases[i][j].numero != self.grille.cases[i][j].vraiNumero:
            self.coordonneesCaseEditee = (i, j)

    def trouverPositionCase(self, caseCoordonnee:tuple) -> tuple:
        """
        Trouve la position de la case en pixels.
        """
        caseDebutPositionX:int
        casePositionX:int
        caseDebutPositionY:int
        casePositionY:int

        caseDebutPositionX = self.affichageGrille.position[0] + 2
        casePositionX = caseDebutPositionX + caseCoordonnee[1] * (self.affichageGrille.caseTaille - 2) + 2 * (caseCoordonnee[1] // self.grille.sousTaille)
        caseDebutPositionY = self.affichageGrille.position[1] + 2
        casePositionY = caseDebutPositionY + caseCoordonnee[0] * (self.affichageGrille.caseTaille - 2) + 2 * (caseCoordonnee[0] // self.grille.sousTaille)
        return (casePositionX, casePositionY)
    
    def ChargerChiffre(self, fenetre:display, caseCoordonnee:tuple) -> None:
        """
        Charge les chiffres de la case.
        """
        chiffre:Case
        casePosition:tuple
        chiffreRenduCouleur:tuple
        chiffreRendu:font.Font
        chiffreRenduPosition:Rect
        i:int
        brouillonRendu:font.Font
        brouillonRenduPositionX:int
        brouillonRenduPositionY:int
        brouillonRenduPosition:Rect

        chiffre = self.grille.cases[caseCoordonnee[0]][caseCoordonnee[1]]
        casePosition = self.trouverPositionCase(caseCoordonnee)

        # Si un chiffre est entré dans la case
        if chiffre.numero != "0":
            if chiffre.estOrigine:
                chiffreRenduCouleur = self.affichageGrille.policeCouleur
            elif chiffre.numero != chiffre.vraiNumero:
                chiffreRenduCouleur = self.affichageGrille.policeCouleurFaux
            else:
                chiffreRenduCouleur = self.affichageGrille.policeCouleurBon
            chiffreRendu = self.affichageGrille.police.render(chiffre.numero, True, chiffreRenduCouleur)
            chiffreRenduCentre = (casePosition[0] + int(self.affichageGrille.caseTaille / 2), casePosition[1] + int(self.affichageGrille.caseTaille / 2))
            chiffreRenduPosition = chiffreRendu.get_rect(center = chiffreRenduCentre)
            fenetre.blit(chiffreRendu, chiffreRenduPosition)
        # Sinon on affiche les chiffres en brouillon
        else:
            for i in range(len(chiffre.brouillon)):
                brouillonRendu = self.affichageGrille.brouillonPolice.render(chiffre.brouillon[i], True, self.affichageGrille.brouillonPoliceCouleur)
                brouillonRenduPositionX = casePosition[0] + int((0.5 + i % self.grille.sousTaille) * self.affichageGrille.caseTaille / self.grille.sousTaille)
                brouillonRenduPositionY = casePosition[1] + int((0.5 + i // self.grille.sousTaille) * self.affichageGrille.caseTaille / self.grille.sousTaille)
                brouillonRenduPosition = brouillonRendu.get_rect(center = (brouillonRenduPositionX, brouillonRenduPositionY))
                fenetre.blit(brouillonRendu, brouillonRenduPosition)

    def chargerCase(self, fenetre:display, caseCoordonnee:tuple) -> None:
        """
        Charge une case de la grille de sudoku.
        """
        casePosition:tuple
        rectCase:Rect
        caseCouleur:tuple

        casePosition = self.trouverPositionCase(caseCoordonnee)
        rectCase = Rect(casePosition, (self.affichageGrille.caseTaille, self.affichageGrille.caseTaille))
        if caseCoordonnee != self.coordonneesCaseEditee:
            caseCouleur = (255, 255, 255)
        else:
            caseCouleur = (240, 240, 255)
        draw.rect(fenetre, caseCouleur, rectCase)
        draw.rect(fenetre, self.affichageGrille.bordCouleur, rectCase, self.affichageGrille.bordEpaisseur)

        self.ChargerChiffre(fenetre, caseCoordonnee)

    def ChargerGrille(self, fenetre:display, tailleFenetre:tuple) -> None:
        """
        Charge la grille de sudoku.
        """
        rectGrille:Rect
        i:int
        j:int

        self.affichageGrille.position = ((tailleFenetre[0] - self.affichageGrille.taille) / 2, (tailleFenetre[1] - self.affichageGrille.taille) / 2)
        rectGrille = Rect(self.affichageGrille.position, (self.affichageGrille.taille, self.affichageGrille.taille))
        draw.rect(fenetre, self.affichageGrille.bordCouleur, rectGrille, self.affichageGrille.bordEpaisseur)
        # Affiche les cases une par une
        for i in range(self.grille.taille):
            for j in range(self.grille.taille):
                self.chargerCase(fenetre, (i, j))

    def CreerBoutonsEdition(self) -> None:
        """
        Cree les boutons des modes d'edition et de brouillon.
        """
        self.boutonsEdition = []
        centreEdition = (197, 357)
        logoEdition = image.load("logoModeEdition.png")
        self.boutonsEdition.append(BoutonCirc(centreEdition, logoEdition))
        centreBrouillon = (197, 507)
        logoBrouillon = image.load("logoModeBrouillon.png")
        self.boutonsEdition.append(BoutonCirc(centreBrouillon, logoBrouillon))
        self.boutonsEdition[1].active = True

    def ChargerBoutonsEdition(self, fenetre:display, positionSouris:tuple) -> None:
        """
        Charge les boutons des modes d'edition et de brouillon.
        """
        bouton:BoutonCirc

        for bouton in self.boutonsEdition:
            bouton.Charger(fenetre, positionSouris)

    def Charger(self, fenetre:display, tailleFenetre:tuple, positionSouris:tuple):
        fenetre.blit(self.fond, (0, 0))
        self.ChargerGrille(fenetre, tailleFenetre)
        self.ChargerBoutonsEdition(fenetre, positionSouris)
        self.horloge.Charger(fenetre)
        self.erreurs.Charger(fenetre)
        display.update()

    def Jouer(self, fenetre, tailleFenetre) -> int:
        """
        Joue une partie de jeu.
        """
        # Deroulement
        fin = False
        touchesClavierPossibles = [K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_a, K_b, K_c, K_d, K_e, K_f, K_g][: self.grille.taille]
        while not fin: 
            positionSouris = mouse.get_pos()
            # Evenements
            for evenement in event.get():
                if evenement.type == QUIT: # Quitter le jeu avec la croix
                    fin = True
                    choixSortie = 3
                if evenement.type == KEYDOWN: 
                    if evenement.key == K_ESCAPE: # Quitter le jeu avec Echap
                        fin = True
                        choixSortie = 3
                    if evenement.key in touchesClavierPossibles: # Entrer un chiffre
                        numeroEntre = self.grille.numeros[touchesClavierPossibles.index(evenement.key)]
                        if self.modeEdition:
                            case = self.grille.cases[self.coordonneesCaseEditee[0]][self.coordonneesCaseEditee[1]]
                            if numeroEntre != case.numero:
                                self.grille.cases[self.coordonneesCaseEditee[0]][self.coordonneesCaseEditee[1]].numero = numeroEntre
                                if case.numero != case.vraiNumero:
                                    self.erreurs.nbErreurs += 1
                        else:
                            if numeroEntre in self.grille.cases[self.coordonneesCaseEditee[0]][self.coordonneesCaseEditee[1]].brouillon:
                                self.grille.cases[self.coordonneesCaseEditee[0]][self.coordonneesCaseEditee[1]].brouillon.remove(numeroEntre)
                            else:
                                self.grille.cases[self.coordonneesCaseEditee[0]][self.coordonneesCaseEditee[1]].brouillon.append(numeroEntre)
                                self.grille.cases[self.coordonneesCaseEditee[0]][self.coordonneesCaseEditee[1]].brouillon.sort()
                    if evenement.key == K_BACKSPACE:
                        if self.modeEdition:
                            self.grille.cases[self.coordonneesCaseEditee[0]][self.coordonneesCaseEditee[1]].numero = "0"
                        else:
                            self.grille.cases[self.coordonneesCaseEditee[0]][self.coordonneesCaseEditee[1]].brouillon.pop(-1)
                if evenement.type == MOUSEBUTTONUP:
                    if self.sourisSurGrille(positionSouris):
                        self.choisirCase(positionSouris)
                    elif self.boutonsEdition[0].Interagit(positionSouris):
                        self.boutonsEdition[0].active = True
                        self.boutonsEdition[1].active = False
                        self.modeEdition = True
                    elif self.boutonsEdition[1].Interagit(positionSouris):
                        self.boutonsEdition[1].active = True
                        self.boutonsEdition[0].active = False
                        self.modeEdition = False
            # Affichage
            self.Charger(fenetre, tailleFenetre, positionSouris)
            # Choix de sortie:
            if self.grille.TrouverCoordonneesCaseVide() == []:
                fin = True
                choixSortie = 51
            elif self.erreurs.nbErreurs >= self.erreurs.nbErreursMax:
                fin = True
                choixSortie = 52
        return choixSortie 

    # CONSTRUCTEURS
    def __init__(self, identifiant:str) -> None:
        """
        Une partie de jeu de sudoku, generee par un identifiant 'identifiant' comprennant la taille et difficulte de la grille a jouer.
        """
        departHorloge:float

        self.fond = image.load("fond.png")

        self.grille = Grille(identifiant)
        self.affichageGrille = AffichageGrille()
        match self.grille.sousTaille:
            case 2:
                self.affichageGrille.caseTaille = 187
                self.affichageGrille.policeTaille = 130
                self.affichageGrille.brouillonPoliceTaille = 40
            case 3:
                self.affichageGrille.caseTaille = 84
                self.affichageGrille.policeTaille = 60
                self.affichageGrille.brouillonPoliceTaille = 15
            case 4:
                self.affichageGrille.caseTaille = 48
                self.affichageGrille.policeTaille = 30
                self.affichageGrille.brouillonPoliceTaille = 7
        self.affichageGrille.police = font.Font("good times rg.otf", self.affichageGrille.policeTaille)
        self.affichageGrille.brouillonPolice = font.Font("good times rg.otf", self.affichageGrille.brouillonPoliceTaille)
        self.coordonneesCaseEditee = tuple(self.grille.TrouverCoordonneesCaseVide())

        self.modeEdition = False
        self.CreerBoutonsEdition()

        departHorloge = float(identifiant[3:6]) / 1000
        self.horloge = Horloge(departHorloge)

        self.erreurs = Erreurs(int(identifiant[2]), int(identifiant[8]))