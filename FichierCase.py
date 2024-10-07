# IMPORTS

class Case:
    """
    Une case de jeu de sudoku.
    """
    # CHAMPS
    numero:str
    vraiNumero:str
    brouillon:list
    estOrigine:bool

    # METHODES
    def Initialiser(self, numero:str = "0") -> None:
        """
        [ Entree(s): numero:str = "0"]
        [ Sortie(s): N/A ] 
        -> Initialise le numero et le vrai numero de la case.
        """
        self.numero = numero
        self.vraiNumero = numero
    
    def Vider(self) -> str:
        """
        [ Entree(s): N/A ]
        [ Sortie(s): numeroRetire:str ]
        -> Retire le numero de la case.
        Retourne le numero retire.
        """
        numeroRetire:str

        self.estOrigine = False
        numeroRetire = self.numero
        self.numero = "0"
        return numeroRetire

    # CONSTRUCTEURS
    def __init__(self, numero:str = "0"):
        """
        [ Entree(s): numero:str = "0" ]
        [ Sortie(s): :Case ]
        -> Une case de grille de sudoku, avec 0 en numero par defaut.
        """
        self.numero = numero
        self.vraiNumero = numero
        self.brouillon = []
        self.estOrigine = True