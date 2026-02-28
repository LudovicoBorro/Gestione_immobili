from services.persistence import salva_portfolio, carica_portfolio

def main():
    portfolio = carica_portfolio()

    print("Portfolio caricato.")
    print(f"Immobili: {len(portfolio.immobili)}")
    print(f"Contratti: {len(portfolio.contratti)}")
    print(f"Conduttori: {len(portfolio.conduttori)}")
    print(f"Amministratori: {len(portfolio.amministratori)}")

    try:
        # Qui in futuro metterai menu, logica ecc.
        pass
    finally:
        # Questo viene eseguito anche se c'è un errore
        salva_portfolio(portfolio)
        print("Dati salvati correttamente.")

if __name__ == "__main__":
    main()