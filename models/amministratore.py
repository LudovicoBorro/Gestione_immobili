class Amministratore:
    def __init__(self):
        self._id_amministratore = None
        self._nome = None
        self._cognome = None
        self._contatto_tel = None
        self._email = None
        self._indirizzo_ufficio = None

    @property
    def id_amministratore(self):
        return self._id_amministratore

    @id_amministratore.setter   # id amministratore deve essere nella forma AMM0001
    def id_amministratore(self, id_amministratore: str):
        parte_let = ""
        parte_num = ""
        for c in id_amministratore:
            if c.isalpha():
                parte_let += c
            if c.isnumeric():
                parte_num += c
        parte_num = int(parte_num)
        if parte_let.lower() != "amm" or parte_num <= 0:
            raise ValueError("Id amministratore non valido!!")
        self._id_amministratore = id_amministratore

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome: str):
        self._nome = nome

    @property
    def cognome(self):
        return self._cognome

    @cognome.setter
    def cognome(self, cognome: str):
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
    def indirizzo_ufficio(self):
        return self._indirizzo_ufficio

    @indirizzo_ufficio.setter
    def indirizzo_ufficio(self, indirizzo_ufficio: str):
        self._indirizzo_ufficio = indirizzo_ufficio

    def to_dict(self):
        return {
            "id_amministratore": self._id_amministratore,
            "nome": self._nome,
            "cognome": self._cognome,
            "contatto_tel": self._contatto_tel,
            "email": self._email,
            "indirizzo_ufficio": self._indirizzo_ufficio
        }

    @staticmethod
    def from_dict(data: dict):
        amm = Amministratore()
        amm.id_amministratore = data.get("id_amministratore")
        amm.nome = data.get("nome")
        amm.cognome = data.get("cognome")
        amm.contatto_tel = data.get("contatto_tel")
        amm.email = data.get("email")
        amm.indirizzo_ufficio = data.get("indirizzo_ufficio")
        return amm