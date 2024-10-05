# IMPORTS

class Case:
    # CHAMPS
    numero:str
    vraiNumero:str
    brouillon:list
    estOrigine:bool

    # METHODES
    def Initialiser(self, numero:str = "0") -> None:
        """
        Initialise le numero et le vrai numero de la case.
        """
        self.numero = numero
        self.vraiNumero = numero
    
    def Vider(self) -> str:
        """
        Retire le numero de la case, et retourne le numero retire.
        """
        numeroRetire:str

        self.estOrigine = False
        numeroRetire = self.numero
        self.numero = "0"
        return numeroRetire

    # CONSTRUCTEURS
    def __init__(self, numero:str = "0") -> None:
        """
        Une case de grille de sudoku.
        """
        self.numero = numero
        self.vraiNumero = numero
        self.brouillon = []
        self.estOrigine = True