from models.amministratore import Amministratore
from models.immobile import Immobile
from models.contratto_locazione import Contratto
from models.conduttore import Conduttore

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
            raise ValueError("Amministratore non esistente")

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