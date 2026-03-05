from models.amministratore import Amministratore
from models.immobile import Immobile
from models.contratto_locazione import Contratto
from models.conduttore import Conduttore
from datetime import datetime

# Questa classe gestisce la logica del programma. I vari modelli non devono avere altri oggetti come attributi, ma solo id, dato che nei json
# non è possibile salvare oggetti. In questa classe devo inserire anche funzioni utili, come calcolo rendimenti ecc. Per salvare dati uso
# dizionari per complessità computazionale minore durante la ricerca: O(1).

class Portfolio:
    def __init__(self):
        self.immobili: dict[str, Immobile] = {}
        self.contratti: dict[str, Contratto] = {}
        self.conduttori: dict[str, Conduttore] = {}
        self.amministratori: dict[str, Amministratore] = {}

    def aggiungi_immobile(self, immobile: Immobile):
        if immobile.id_immobile in self.immobili:
            raise ValueError("Immobile già esistente")

        # if immobile.id_amministratore not in self.amministratori: Non tutti gli immobili hanno degli amministratori
            # raise ValueError("Amministratore non esistente")

        self.immobili[immobile.id_immobile] = immobile

    def aggiungi_contratto(self, contratto: Contratto):

        if contratto.id_contratto in self.contratti:
            raise ValueError("Contratto già esistente")

        if contratto.id_immobile not in self.immobili:
            raise ValueError("Immobile non esistente")

        for id_cond in contratto.lista_id_conduttori:
            if id_cond not in self.conduttori:
                raise ValueError(f"Conduttore {id_cond} non esistente")

        # Controllo immobile non già locato
        immobile = self.immobili[contratto.id_immobile]
        if immobile.stato_loc == "locato":
            raise ValueError("Immobile già locato")

        self.contratti[contratto.id_contratto] = contratto
        immobile.stato_loc = "locato"

    def trova_immobile_per_id(self, id_imm: str):
        im = self.immobili.get(id_imm)
        if im is not None:
            return im
        return None

    def trova_contratto_per_id(self, id_cont: str):
        cont = self.contratti.get(id_cont)
        if cont is not None:
            return cont
        return None

    def trova_conduttore_per_id(self, id_cond: str):
        cond = self.conduttori.get(id_cond)
        if cond is not None:
            return cond
        return None

    def trova_amministratore_per_id(self, id_amm: str):
        am = self.amministratori.get(id_amm)
        if am is not None:
            return am
        return None

    def to_dict(self):
        return {
            "immobili": [i.to_dict() for i in self.immobili.values()],
            "contratti": [c.to_dict() for c in self.contratti.values()],
            "conduttori": [c.to_dict() for c in self.conduttori.values()],
            "amministratori": [a.to_dict() for a in self.amministratori.values()],
        }

    # Funzione per calcolare il totale dei canoni mensili da tutti gli immobili locati attualmente (contratti attivi)
    def totale_canoni_mensili(self):
        totale = 0
        for c in self.contratti.values():
            if c.stato == "attivo":
                totale += c.canone_mensile
        return totale

    # Funzione che ritorna Immobili liberi (non locati)
    def immobili_liberi(self):
        immobili: list[Immobile] = []
        for imm in self.immobili.values():
            if imm.stato_loc == "libero":
                immobili.append(imm)
        return immobili

    # Funzione che ritorna Immobili locati
    def immobili_locati(self):
        immobili: list[Immobile] = []
        for imm in self.immobili.values():
            if imm.stato_loc == "locato":
                immobili.append(imm)
        return immobili

    # Funzione che ritorna Immobili a uso personale (non locati, non liberi)
    def immobili_personali(self):
        immobili: list[Immobile] = []
        for imm in self.immobili.values():
            if imm.stato_loc == "personale":
                immobili.append(imm)
        return immobili

    # Funzione che ritorna i conduttori di un dato Contratto, attraverso id
    def conduttori_immobile_per_id(self, id_cont: str):
        contr = self.trova_contratto_per_id(id_cont)
        if contr is None:
            raise ValueError(f"Contratto {id_cont} non esistente!!")
        conduttori = []
        for id_cond in contr.lista_id_conduttori:
            conduttore = self.trova_conduttore_per_id(id_cond)
            if conduttore is not None:
                conduttori.append(conduttore)
        return conduttori

    # Funzione per creare un immobile e salvarlo
    def crea_immobile(self, nome: str, indirizzo: str, citta: str, data_acquisto: str, foglio_cat: int, numero_cat: int,
                      sublocazione_cat: int, prezzo_acq: float, num_locali: int, metratura: float, spese_notarili: float, spese_condominiali: float, tipo_immobile: str, stato_loc: str, id_amministratore: str):
        try:
            imm = Immobile()
            imm.id_immobile = self.genera_id(self.immobili, "IMM")
            imm.nome = nome
            imm.indirizzo = indirizzo
            imm.citta = citta
            imm.data_acquisto = data_acquisto
            imm.foglio_cat = foglio_cat
            imm.numero_cat = numero_cat
            imm.sublocazione_cat = sublocazione_cat
            imm.prezzo_acq = prezzo_acq
            imm.num_locali = num_locali
            imm.metratura = metratura
            imm.spese_notarili = spese_notarili
            imm.spese_condominiali = spese_condominiali
            imm.tipo_immobile = tipo_immobile           # Il controllo sugli input lo faccio nel main non qui, quindi il controllo locato, personale, libero ecc
            imm.stato_loc = stato_loc
            imm.id_amministratore = id_amministratore   # La scelta dell'amministratore la gestisco negli input, quindi l'utente dovrà poter scegliere tra amm vecchi o crearne uno nuovo
            self.immobili[imm.id_immobile] = imm
            return imm
        except ValueError as ve:
            raise ValueError(f"Errore nella creazione dell'immobile: {ve}")

    # Funzione per creare contratto e salvarlo
    def crea_contratto(self, id_immobile: str, lista_id_conduttori: list[str], durata_contratto: int, data_inizio: str, data_fine: str, canone_mensile: float):
        immobile = self.trova_immobile_per_id(id_immobile)

        if immobile is None:
            raise ValueError(f"Immobile {id_immobile} non esistente!!")
        if immobile.stato_loc == "locato":
            raise ValueError(f"Immobile {id_immobile} è già stato locato!")
        for id_cond in lista_id_conduttori:
            if id_cond not in self.conduttori:
                raise ValueError(f"Conduttore {id_cond} non esistente!!")

        try:
            cont = Contratto()
            cont.id_contratto = self.genera_id(self.contratti, "CL")
            cont.id_immobile = id_immobile
            cont.lista_id_conduttori = lista_id_conduttori
            cont.durata_contratto = durata_contratto
            cont.data_inizio = data_inizio
            cont.data_fine = data_fine
            cont.canone_mensile = canone_mensile
            self.contratti[cont.id_contratto] = cont
            immobile.stato_loc = "locato"
            return cont
        except ValueError as ve:
            raise ValueError(f"Errore nella creazione del contratto: {ve}")

    # Funzione per creare conduttore e salvarlo
    def crea_conduttore(self, nome: str, cognome: str, contatto_tel: str, email: str, sesso: str, data_nascita: str):
        try:
            cond = Conduttore()
            cond.id_conduttore = self.genera_id(self.conduttori, "CO")
            cond.nome = nome
            cond.cognome = cognome
            cond.contatto_tel = contatto_tel
            cond.email = email
            cond.sesso = sesso
            cond.data_nascita = data_nascita
            self.conduttori[cond.id_conduttore] = cond
            return cond
        except ValueError as ve:
            raise ValueError(f"Errore nella creazione del conduttore: {ve}")

    # Funzione per creare amministratore e salvarlo
    def crea_amministratore(self, nome: str, cognome: str, contatto_tel: str, email: str, indirizzo_ufficio: str):
        try:
            amm = Amministratore()
            amm.id_amministratore = self.genera_id(self.amministratori, "AMM")
            amm.nome = nome
            amm.cognome = cognome
            amm.contatto_tel = contatto_tel
            amm.email = email
            amm.indirizzo_ufficio = indirizzo_ufficio
            self.amministratori[amm.id_amministratore] = amm
            return amm
        except ValueError as ve:
            raise ValueError(f"Errore nella creazione dell' amministratore: {ve}")

    # Funzione per chiudere un contratto cambiando stato_loc in immobile
    def chiudi_contratto(self, id_contratto: str):

        contratto = self.trova_contratto_per_id(id_contratto)
        if contratto is None:
            raise ValueError(f"Contratto {id_contratto} non esistente!!")
        if contratto.stato == "chiuso":
            raise ValueError("Il contratto è già chiuso!!")

        immobile = self.trova_immobile_per_id(contratto.id_immobile)
        if immobile is None:
            raise ValueError(f"Immobile {contratto.id_immobile} non esistente!!")
        if immobile.stato_loc != "locato":
            raise ValueError("L'immobile non risulta attualmente locato!!")

        contratto.data_fine_effettiva = datetime.now().strftime("%d/%m/%Y")
        contratto.stato = "chiuso"
        immobile.stato_loc = "libero"

    # FUNZIONE PER GENERAZIONE ID
    @classmethod
    def genera_id(cls, dizionario: dict, prefisso: str) -> str:

        if not dizionario:
            return f"{prefisso}0001"

        numeri = [
            int(id_elem[len(prefisso):])
            for id_elem in dizionario.keys()
        ]

        prossimo_numero = max(numeri) + 1
        return f"{prefisso}{prossimo_numero:04d}"