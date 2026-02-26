from models import immobile, contratto_locazione, amministratore, conduttore
import os

lista_immobili: list[immobile.Immobile] = []
lista_contratti: list[contratto_locazione.Contratto] = []
lista_amministratori: list[amministratore.Amministratore] = []
lista_conduttori: list[conduttore.Conduttore] = []
inizio = True

def crea_immobile():
    os.system("cls")
    print("Ora ti verranno chiesti dei dati per registrare correttamente l'immobile")
    input("Premi invio per continuare...")
    imm = immobile.Immobile()
    check = True
    while check:
        try:
            imm.id_imm = "IMM" + str(len(lista_immobili)+1)
            imm.nome = input("Assegna un nome all'immobile: ").strip()
            imm.indirizzo = input("Indirizzo: ").strip()
            imm.citta = input("Città: ").strip()
            imm.data_acquisto = input("Data di acquisto nel formato gg/mm/aaaa: ").strip()
            imm.foglio_cat = int(input("Numero foglio catastale: ").strip())
            imm.numero_cat = int(input("Numero immobile catastale: ").strip())
            imm.sublocazione_cat = int(input("Numero sublocazione catastale: ").strip())
            imm.prezzo_acq = float(input("Prezzo di acquisto: ").strip())
            imm.num_locali = int(input("Numero locali: ").strip())
            imm.metratura = float(input("Metri quadri: ").strip())
            imm.spese_notarili = float(input("Costi notarili in €: ").strip())
            imm.spese_condominiali = float(input("Costi condominiali in €: ").strip())
            check = False
        except ValueError as e:
            print(e)
    check = True
    while check:
        tipo_in = input("Digita \"c\" se l'immobile sarà destinato ad uso commerciale, \"r\" per uso residenziale: ")
        if tipo_in.strip().lower() == "c":
            imm.tipo_immobile = "commerciale"
            check = False
        elif tipo_in.strip().lower() == "r":
            imm.tipo_immobile = "residenziale"
            check = False
        else:
            print("Inserisci un carattere valido!!")
    imm.stato_loc = "personale"
    lista_immobili.append(imm)
    print("Immobile salvato correttamente!")


def crea_contratto():
    pass

def stampa_immobili():
    pass

def stampa_contratti():
    pass

def menu():
    risp = -1
    while risp != 5:
        print("Scegli una voce dal menù:\n")
        print("1) Inserisci un nuovo immobile")  # durante l'inserimento dell'immobile ha senso inserire anche amministratore se necessario, non lo metto nel menu generale
        print("2) Inserisci un nuovo contratto di locazione")  # durante questo inserimento ha senso inserire anche i conduttori
        print("3) Mostra tutti gli immobili")
        print("4) Mostra tutti i contratto stipulati")
        print("5) Esci")
        risp = input("Digita qui il numero corrispondente: ")
        risp.strip()
        if risp == "1":  # inserimento di un nuovo immobile
            crea_immobile()
        elif risp == "2":
            crea_contratto()
        elif risp == "3":
            stampa_immobili()
        elif risp == "4":
            stampa_contratti()
        elif risp == "5":
            risp = 5
        else:
            print("Inserisci un numero valido!")

def main():
    print("Benvenuto! Questo programma ti aiuta a gestire il patrimonio immobiliare!\n")
    menu()

main()
# RICORDARSI DI STRIPPARE TUTTI I DATI PRIMA DI PASSARLI ALLE CLASSI
