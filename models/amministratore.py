class Amministratore:
    def __init__(self, id_amministratore: str, nome: str, cognome: str, contatto_tel: str, email: str, indirizzo_ufficio: str):
        self._id_amministratore = None
        self.id_amministratore = id_amministratore
        self._nome = None
        self.nome = nome
        self._cognome = None
        self.cognome = cognome
        self._contatto_tel = None
        self.contatto_tel = contatto_tel
        self._email = None
        self.email = email
        self._indirizzo_ufficio = None
        self.indirizzo_ufficio = indirizzo_ufficio

    @property
    def id_amministratore(self):
        return self._id_amministratore

    @id_amministratore.setter   # id amministratore deve essere nella forma AMM1
    def id_amministratore(self, id_amministratore: str):
        parte_let = ""
        parte_num = -1
        for c in id_amministratore:
            if c.isalpha():
                parte_let += c
            if c.isnumeric():
                parte_num += c
        if parte_let.lower() != "amm" or parte_num <= 0:
            raise ValueError("Id amministratore non valido!!")
        self._id_amministratore = id_amministratore

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome: str):
        if nome.isalpha():
            self._nome = nome
        else:
            raise ValueError("Attenzione nome non valido!!")

    @property
    def cognome(self):
        return self._cognome

    @cognome.setter
    def cognome(self, cognome: str):
        if cognome.isalpha():
            self._cognome = cognome
        else:
            raise ValueError("Attenzione cognome non valido!!")

    @property
    def contatto_tel(self):
        return self._contatto_tel

    @contatto_tel.setter
    def contatto_tel(self, contatto_tel: str):
        if contatto_tel.isnumeric() and len(contatto_tel) == 10:
            self._contatto_tel = contatto_tel
        else:
            raise ValueError("Attenzione contatto_tel non valido!!")

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email: str):
        self._email = email

    @property
    def indirizzo_ufficio(self):
        return self._indirizzo_ufficio

    @indirizzo_ufficio.setter
    def indirizzo_ufficio(self, indirizzo_ufficio: str):
        self._indirizzo_ufficio = indirizzo_ufficio