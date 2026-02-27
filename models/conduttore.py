class Conduttore:
    def __init__(self):
        self._id_conduttore = None
        self._nome = None
        self._cognome = None
        self._contatto_tel = None
        self._email = None
        self._sesso = None
        self._data_nascita = None

    @property
    def id_conduttore(self):
        return self._id_conduttore

    @id_conduttore.setter       # id conduttore è nella forma CO1
    def id_conduttore(self, id_conduttore: str):
        parte_let = ""
        parte_num = ""
        for c in id_conduttore:
            if c.isalpha():
                parte_let += c
            if c.isnumeric():
                parte_num += c
        parte_num = int(parte_num)
        if parte_let.lower() != "co" or parte_num <= 0:
            raise ValueError("Id conduttore non valido!!")
        self._id_conduttore = id_conduttore

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome):
        self._nome = nome

    @property
    def cognome(self):
        return self._cognome

    @cognome.setter
    def cognome(self, cognome):
        self._cognome = cognome

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

    def to_dict(self):
        return {
            "id_conduttore": self._id_conduttore,
            "nome": self._nome,
            "cognome": self._cognome,
            "contatto_tel": self._contatto_tel,
            "email": self._email,
            "sesso": self._sesso,
            "data_nascita": self._data_nascita
        }

    @staticmethod
    def from_dict(data: dict):
        cond = Conduttore()
        cond.id_conduttore = data.get("id_conduttore")
        cond.nome = data.get("nome")
        cond.cognome = data.get("cognome")
        cond.contatto_tel = data.get("contatto_tel")
        cond.email = data.get("email")
        cond.sesso = data.get("sesso")
        cond.data_nascita = data.get("data_nascita")
        return cond
