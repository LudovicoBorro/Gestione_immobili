import json
import os
from models.immobile import Immobile
from models.contratto_locazione import Contratto
from models.conduttore import Conduttore
from models.amministratore import Amministratore
from services.portfolio_manager import Portfolio


FILE_PATH = "services/database.json"
TEMP_PATH = "services/database.json.tmp"
BACKUP_PATH = "services/database.json.bak"


# =========================
# SALVATAGGIO CRASH-SAFE
# =========================
def salva_portfolio(portfolio: Portfolio):
    data = portfolio.to_dict()

    # 1️⃣ Scrittura su file temporaneo
    with open(TEMP_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
        f.flush()
        os.fsync(f.fileno())

    # 2️⃣ Backup del file esistente
    if os.path.exists(FILE_PATH):
        if os.path.exists(BACKUP_PATH):
            os.remove(BACKUP_PATH)
        os.replace(FILE_PATH, BACKUP_PATH)

    # 3️⃣ Rename atomico
    os.replace(TEMP_PATH, FILE_PATH)


# =========================
# CARICAMENTO CON RECOVERY
# =========================
def carica_portfolio() -> Portfolio:
    portfolio = Portfolio()

    # Se non esiste nulla → portfolio vuoto
    if not os.path.exists(FILE_PATH):
        return portfolio

    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

    except json.JSONDecodeError:
        print("⚠ File principale corrotto. Tentativo di ripristino dal backup...")

        if os.path.exists(BACKUP_PATH):
            try:
                with open(BACKUP_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Ripristina il file principale
                os.replace(BACKUP_PATH, FILE_PATH)
                print("✔ Ripristino completato dal backup.")

            except Exception:
                print("❌ Anche il backup è corrotto.")
                return portfolio
        else:
            print("❌ Nessun backup disponibile.")
            return portfolio

    # =========================
    # RICOSTRUZIONE OGGETTI
    # =========================

    # 1️⃣ Amministratori
    for amm_data in data.get("amministratori", []):
        amm = Amministratore.from_dict(amm_data)
        portfolio.amministratori[amm.id_amministratore] = amm

    # 2️⃣ Conduttori
    for cond_data in data.get("conduttori", []):
        cond = Conduttore.from_dict(cond_data)
        portfolio.conduttori[cond.id_conduttore] = cond

    # 3️⃣ Immobili
    for imm_data in data.get("immobili", []):
        imm = Immobile.from_dict(imm_data)
        portfolio.immobili[imm.id_immobile] = imm

    # 4️⃣ Contratti
    for cont_data in data.get("contratti", []):
        cont = Contratto.from_dict(cont_data)
        portfolio.contratti[cont.id_contratto] = cont

    return portfolio