class Conduttore:
    def __init__(self, id_conduttore: str, nome: str, cognome: str, contatto_tel: str, email: str, sesso: str, data_nascita: str):
        self._id_conduttore = None
        self.id_conduttore = id_conduttore
        self._nome = None
        self.nome = nome
        self._cognome = None
        self.cognome = cognome
        self._contatto_tel = None
        self.contatto_tel = contatto_tel
        self._email = None
        self.email = email
        self._sesso = None
        self.sesso = sesso
        self._data_nascita = None
        self.data_nascita = data_nascita

    @property
    def id_conduttore(self):
        return self._id_conduttore

    @id_conduttore.setter       # id conduttore è nella forma CO1
    def id_conduttore(self, id_conduttore: str):
        parte_let = ""
        parte_num = -1
        for c in id_conduttore:
            if c.isalpha():
                parte_let += c
            if c.isnumeric():
                parte_num += c
        if parte_let.lower() != "co" or parte_num <= 0:
            raise ValueError("Id conduttore non valido!!")
        self._id_conduttore = id_conduttore

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome):
        if nome.isalpha():
            self._nome = nome
        else:
            raise ValueError("Attenzione, nome non valido!!")

    @property
    def cognome(self):
        return self._cognome

    @cognome.setter
    def cognome(self, cognome):
        if cognome.isalpha():
            self._cognome = cognome
        else:
            raise ValueError("Attenzione, cognome non valido!!")

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
    def sesso(self):
        return self._sesso

    @sesso.setter
    def sesso(self, sesso: str):
        if sesso.isalpha():
            self._sesso = sesso
        else:
            raise ValueError("Attenzione, sesso non valido!!")

    @property
    def data_nascita(self):
        return self._data_nascita

    @data_nascita.setter
    def data_nascita(self, data_nascita: str):
        self._data_nascita = data_nascita


