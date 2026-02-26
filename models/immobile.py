from models.amministratore import Amministratore

class Immobile:
    def __init__(self):             #   id_immobile: str, nome: str, indirizzo: str, citta: str, data_acquisto: str, foglio_cat: int, numero_cat: int,
                                    #    sublocazione_cat: int, prezzo_acq: float, num_locali: int, metratura: float, spese_notarili: float, spese_condominiali: float
        self._id_immobile = None
        self._nome = None
        self._indirizzo = None
        self._citta = None
        self._data_acquisto = None
        self._foglio_cat = None
        self._numero_cat = None
        self._sublocazione_cat = None
        self._prezzo_acq = None
        self._num_locali = None
        self._metratura = None
        self._spese_notarili = None
        self._spese_condominiali = None
        self._amministratore = None
        self._tipo_immobile = None
        self._stato_loc = None

    @property
    def id_immobile(self):
        return self._id_immobile

    @id_immobile.setter     # è necessario un controllo su id_immobile perchè deve essere nella forma IMM1
    def id_immobile(self, id_immobile: str):
        parte_let = ""
        parte_num = -1
        for c in id_immobile:
            if c.isalpha():
                parte_let += c
            if c.isnumeric():
                parte_num += c
        if parte_let.lower() != "imm" or parte_num <= 0:
            raise ValueError("Id immobile errato!!")
        self._id_immobile = id_immobile

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome: str):
        self._nome = nome

    @property
    def indirizzo(self):
        return self._indirizzo

    @indirizzo.setter
    def indirizzo(self, indirizzo: str):
        self._indirizzo = indirizzo

    @property
    def citta(self):
        return self._citta

    @citta.setter
    def citta(self, citta: str):
        if citta.isalpha():
            self._citta = citta
        else:
            raise ValueError("Città non valida!!")

    @property
    def data_acquisto(self):
        return self._data_acquisto

    @data_acquisto.setter
    def data_acquisto(self, data_acquisto: str):
        self._data_acquisto = data_acquisto

    @property
    def foglio_cat(self):
        return self._foglio_cat

    @foglio_cat.setter
    def foglio_cat(self, foglio_cat: int):
        if foglio_cat < 0 or foglio_cat is not int:
            raise ValueError("Foglio catastale errato!!")
        self._foglio_cat = foglio_cat

    @property
    def numero_cat(self):
        return self._numero_cat

    @numero_cat.setter
    def numero_cat(self, numero_cat: int):
        if numero_cat < 0 or numero_cat is not int:
            raise ValueError("Numero catastale errato!!")
        self._numero_cat = numero_cat

    @property
    def sublocazione_cat(self):
        return self._sublocazione_cat

    @sublocazione_cat.setter
    def sublocazione_cat(self, sublocazione_cat: int):
        if sublocazione_cat < 0 or sublocazione_cat is not int:
            raise ValueError("Sublocazione catastale errata!!")

    @property
    def prezzo_acq(self):
        return self._prezzo_acq

    @prezzo_acq.setter
    def prezzo_acq(self, prezzo_acq: float):
        if prezzo_acq <= 0:
            raise ValueError("Prezzo acquisto errato!!")
        self._prezzo_acq = prezzo_acq

    @property
    def num_locali(self):
        return self._num_locali

    @num_locali.setter
    def num_locali(self, num_locali: int):
        if num_locali <= 0 or num_locali is not int:
            raise ValueError("Numero locali errato!!")
        self._num_locali = num_locali

    @property
    def metratura(self):
        return self._metratura

    @metratura.setter
    def metratura(self, metratura: float):
        if metratura <= 0:
            raise ValueError("Metratura errata!!")
        self._metratura = metratura

    @property
    def spese_notarili(self):
        return self._spese_notarili

    @spese_notarili.setter
    def spese_notarili(self, spese_notarili: float):
        if spese_notarili <= 0:
            raise ValueError("Spese notarili errate!!")
        self._spese_notarili = spese_notarili

    @property
    def spese_condominiali(self):
        return self._spese_condominiali

    @spese_condominiali.setter
    def spese_condominiali(self, spese_condominiali: float):
        if spese_condominiali < 0:          # le spese condominiali sono nulle se l'immobile è una villa o un negozio
            raise ValueError("Spese condominiali errate!!")
        self._spese_condominiali = spese_condominiali

    @property
    def amministratore(self):
        return self._amministratore

    @amministratore.setter
    def amministratore(self, amministratore: Amministratore):
        self._amministratore = amministratore

    @property
    def tipo_immobile(self):
        return self._tipo_immobile

    @tipo_immobile.setter
    def tipo_immobile(self, tipo_immobile: str):
        tipo = {"commerciale" , "residenziale"}     # commerciale se l'immobile è a uso commerciale, residenziale se è a uso abitativo
        if tipo_immobile in tipo:
            self._tipo_immobile = tipo_immobile
        else:
            raise ValueError("Tipo immobile non valido!!")

    @property
    def stato_loc(self):
        return self._stato_loc

    @stato_loc.setter
    def stato_loc(self, stato_loc: str):
        stati = {"locato", "libero", "personale"}     # locato se immobile è in locazione, libero se non lo è, personale se è per uso personale, abitativo o commerciale
        if stato_loc in stati:
            self._stato_loc = stato_loc
        else:
            raise ValueError("Stato immobile non valido!!")


