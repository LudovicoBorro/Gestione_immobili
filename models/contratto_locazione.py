from models.immobile import Immobile
from models.conduttore import Conduttore

class Contratto:    # durata contratto è espressa in mesi
    def __init__(self, id_contratto: str, immobile: Immobile, lista_conduttori: list[Conduttore], durata_contratto: int, data_inizio: str, data_fine: str, canone_mensile: float):
        self._id_contratto = None
        self.id_contratto = id_contratto
        self._immobile = None
        self.immobile = immobile
        self._lista_conduttori = None
        self.lista_conduttori = lista_conduttori
        self._durata_contratto = None
        self.durata_contratto = durata_contratto
        self._data_inizio = None
        self.data_inizio = data_inizio
        self._data_fine = None
        self.data_fine = data_fine
        self._canone_mensile = None
        self.canone_mensile = canone_mensile

    @property
    def id_contratto(self):
        return self._id_contratto

    @id_contratto.setter    # è necessario un controllo su id_contratto, è nella forma CL1
    def id_contratto(self, id_contratto):
        parte_let = ""
        parte_num = -1
        for c in id_contratto:
            if c.isalpha():
                parte_let += c
            if c.isnumeric():
                parte_num += c
        if parte_let.lower() != "cl" or parte_num <= 0:
            raise ValueError("Id contratto non valido!!")
        self._id_contratto = id_contratto

    @property
    def immobile(self):
        return self._immobile

    @immobile.setter
    def immobile(self, immobile):
        self._immobile = immobile

    @property
    def lista_conduttori(self):
        return self._lista_conduttori

    @lista_conduttori.setter
    def lista_conduttori(self, lista_conduttori: list[Conduttore]):
        if len(lista_conduttori) == 0:
            raise ValueError("Assegna almeno un conduttore!!")
        self._lista_conduttori = lista_conduttori

    @property
    def durata_contratto(self):
        return self._durata_contratto

    @durata_contratto.setter
    def durata_contratto(self, durata_contratto):
        if durata_contratto <= 0:
            raise ValueError("Impossibile assegnare durata negativa!!")
        self._durata_contratto = durata_contratto

    @property
    def data_inizio(self):
        return self._data_inizio

    @data_inizio.setter
    def data_inizio(self, data_inizio):
        self._data_inizio = data_inizio

    @property
    def data_fine(self):
        return self._data_fine

    @data_fine.setter
    def data_fine(self, data_fine):
        self._data_fine = data_fine

    @property
    def canone_mensile(self):
        return self._canone_mensile

    @canone_mensile.setter
    def canone_mensile(self, canone_mensile):
        if canone_mensile <= 0:
            raise ValueError("Impossibile assegnare canone mensile negativo!!")
        self._canone_mensile = canone_mensile

