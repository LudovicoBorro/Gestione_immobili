import customtkinter as ctk
from gui.main_window import MainWindow
from services.persistence import carica_portfolio, salva_portfolio

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def main():
    portfolio = carica_portfolio()

    app = ctk.CTk()
    app.title("Gestione Immobili")
    app.geometry("1200x750")
    app.minsize(1000, 650)

    window = MainWindow(app, portfolio)

    def on_close():
        salva_portfolio(portfolio)
        app.destroy()

    app.protocol("WM_DELETE_WINDOW", on_close)
    app.mainloop()

if __name__ == "__main__":
    main()
