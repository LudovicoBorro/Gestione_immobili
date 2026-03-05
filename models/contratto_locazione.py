from datetime import datetime

class Contratto:    # durata contratto è espressa in mesi
    def __init__(self):
        self._id_contratto = None
        self._id_immobile = None
        self._lista_id_conduttori = None
        self._durata_contratto = None
        self._data_inizio = None
        self._data_fine = None
        self._data_fine_effettiva = None
        self._canone_mensile = None
        self._stato = "attivo"

    @property
    def id_contratto(self):
        return self._id_contratto

    @id_contratto.setter    # è necessario un controllo su id_contratto, è nella forma CL0001
    def id_contratto(self, id_contratto):
        parte_let = ""
        parte_num = ""
        for c in id_contratto:
            if c.isalpha():
                parte_let += c
            if c.isnumeric():
                parte_num += c
        parte_num = int(parte_num)
        if parte_let.lower() != "cl" or parte_num <= 0:
            raise ValueError("Id contratto non valido!!")
        self._id_contratto = id_contratto

    @property
    def id_immobile(self):
        return self._id_immobile

    @id_immobile.setter
    def id_immobile(self, id_immobile):
        self._id_immobile = id_immobile

    @property
    def lista_id_conduttori(self):
        return self._lista_id_conduttori

    @lista_id_conduttori.setter
    def lista_id_conduttori(self, lista_id_conduttori: list[str]):
        if len(lista_id_conduttori) == 0:
            raise ValueError("Assegna almeno un conduttore!!")
        self._lista_id_conduttori = lista_id_conduttori

    @property
    def durata_contratto(self):
        return self._durata_contratto

    @durata_contratto.setter
    def durata_contratto(self, durata_contratto: int):
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

    @property
    def stato(self):
        return self._stato

    @stato.setter
    def stato(self, stato: str):
        if stato.lower().strip() in {"chiuso", "attivo"}:
            self._stato = stato
        else:
            raise ValueError(f"Stato {stato} non valido!!")

    @property
    def data_fine_effettiva(self):
        return self._data_fine_effettiva

    @data_fine_effettiva.setter
    def data_fine_effettiva(self, data_fine_effettiva: str):
        self._data_fine_effettiva = data_fine_effettiva

    def calcola_durata_effettiva(self):
        if self.data_fine_effettiva is None:
            raise ValueError("Il contratto non è ancora chiuso!!")

        data_inizio = datetime.strptime(self.data_inizio, "%d/%m/%Y")
        data_fine_effettiva = datetime.strptime(self.data_fine_effettiva, "%d/%m/%Y")

        if data_fine_effettiva < data_inizio:
            raise ValueError("La data di fine è precedente alla data di inizio!!")

        mesi = (data_fine_effettiva.year - data_inizio.year) * 12 + \
               (data_fine_effettiva.month - data_inizio.month)

        # Se il giorno finale è minore del giorno iniziale,
        # l'ultimo mese non è completo
        if data_fine_effettiva.day < data_inizio.day:
            mesi -= 1

        return mesi

    def to_dict(self):
        return {
            "id_contratto": self.id_contratto,
            "id_immobile": self.id_immobile,
            "lista_id_conduttori": self.lista_id_conduttori,
            "durata_contratto": self.durata_contratto,
            "data_inizio": self.data_inizio,
            "data_fine": self.data_fine,
            "canone_mensile": self.canone_mensile,
            "stato": self.stato,
            "data_fine_effettiva": self.data_fine_effettiva
        }

    @staticmethod
    def from_dict(data: dict):
        con = Contratto()
        con.id_contratto = data.get("id_contratto")
        con.id_immobile = data.get("id_immobile")
        con.lista_id_conduttori = data.get("lista_id_conduttori")
        con.durata_contratto = data.get("durata_contratto")
        con.data_inizio = data.get("data_inizio")
        con.data_fine = data.get("data_fine")
        con.canone_mensile = data.get("canone_mensile")
        con.stato = data.get("stato", "attivo")
        con.data_fine_effettiva = data.get("data_fine_effettiva")
        return con

