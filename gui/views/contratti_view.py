import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk

BG_MAIN   = "#161b27"
BG_CARD   = "#1e2535"
BG_INPUT  = "#252d3d"
ACCENT    = "#3b82f6"
ACCENT_H  = "#2563eb"
DANGER    = "#ef4444"
SUCCESS   = "#10b981"
WARNING   = "#f59e0b"
TEXT_P    = "#f1f5f9"
TEXT_M    = "#64748b"
BORDER    = "#2d3748"
ROW_EVEN  = "#1e2535"
ROW_ODD   = "#1a2030"
ROW_SEL   = "#1e3a5f"


class ContrattiView(ctk.CTkFrame):
    def __init__(self, parent, portfolio, refresh_cb):
        super().__init__(parent, fg_color=BG_MAIN, corner_radius=0)
        self.portfolio = portfolio
        self.refresh_cb = refresh_cb
        self._selected_id = None

        self._build()

    def _build(self):
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", pady=(0, 16))

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self._refresh_table())
        ctk.CTkEntry(
            top, textvariable=self.search_var,
            placeholder_text="🔍  Cerca per ID immobile, conduttore...",
            width=300, height=36,
            fg_color=BG_CARD, border_color=BORDER,
            text_color=TEXT_P, font=ctk.CTkFont(size=13)
        ).pack(side="left")

        ctk.CTkButton(
            top, text="＋  Nuovo Contratto", height=36,
            fg_color=ACCENT, hover_color=ACCENT_H,
            font=ctk.CTkFont(size=13), corner_radius=8,
            command=self._open_form_new
        ).pack(side="right")

        ctk.CTkButton(
            top, text="🔒  Chiudi contratto", height=36, width=150,
            fg_color=BG_CARD, hover_color="#2d1515",
            border_width=1, border_color=DANGER,
            text_color=DANGER,
            font=ctk.CTkFont(size=13), corner_radius=8,
            command=self._close_selected
        ).pack(side="right", padx=(0, 8))

        self._build_cards()
        self._build_table()
        self._refresh_table()

    def _build_cards(self):
        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(fill="x", pady=(0, 16))

        def n_attivi():
            return sum(1 for c in self.portfolio.contratti.values() if c.stato == "attivo")
        def n_chiusi():
            return sum(1 for c in self.portfolio.contratti.values() if c.stato == "chiuso")

        cards = [
            ("Totale", lambda: len(self.portfolio.contratti),                          ACCENT),
            ("Attivi", n_attivi,                                                        SUCCESS),
            ("Chiusi", n_chiusi,                                                        TEXT_M),
            ("€/mese", lambda: f"€ {self.portfolio.totale_canoni_mensili():,.0f}",     WARNING),
        ]
        self._card_labels = {}
        for label, fn, color in cards:
            card = ctk.CTkFrame(row, fg_color=BG_CARD, corner_radius=10)
            card.pack(side="left", padx=(0, 12), ipadx=16, ipady=10)
            val_lbl = ctk.CTkLabel(card, text=str(fn()),
                                   font=ctk.CTkFont(size=22, weight="bold"),
                                   text_color=color)
            val_lbl.pack()
            ctk.CTkLabel(card, text=label,
                         font=ctk.CTkFont(size=11), text_color=TEXT_M).pack()
            self._card_labels[label] = (val_lbl, fn)

    def _build_table(self):
        wrapper = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=12)
        wrapper.pack(fill="both", expand=True)

        cols    = ["ID Contratto", "Immobile", "Conduttori", "Inizio", "Fine", "Canone €/mese", "Stato"]
        weights = [1, 1, 2, 1, 1, 1, 1]

        header = ctk.CTkFrame(wrapper, fg_color="#131929", corner_radius=0)
        header.pack(fill="x")
        for i, w in enumerate(weights):
            header.columnconfigure(i, weight=w)
        for i, col in enumerate(cols):
            ctk.CTkLabel(
                header, text=col.upper(),
                font=ctk.CTkFont(size=10, weight="bold"), text_color=TEXT_M
            ).grid(row=0, column=i, sticky="w", padx=12, pady=10)

        self.table_scroll = ctk.CTkScrollableFrame(wrapper, fg_color="transparent", corner_radius=0)
        self.table_scroll.pack(fill="both", expand=True)
        self._col_weights = weights

    def _refresh_table(self, *_):
        for label, (lbl, fn) in self._card_labels.items():
            lbl.configure(text=str(fn()))

        for w in self.table_scroll.winfo_children():
            w.destroy()

        query = self.search_var.get().lower()
        items = list(self.portfolio.contratti.values())
        if query:
            items = [c for c in items if
                     query in c.id_immobile.lower() or
                     query in c.id_contratto.lower() or
                     any(query in cid.lower() for cid in c.lista_id_conduttori)]

        for idx, cont in enumerate(items):
            bg = ROW_SEL if cont.id_contratto == self._selected_id else (ROW_EVEN if idx % 2 == 0 else ROW_ODD)
            row_frame = ctk.CTkFrame(self.table_scroll, fg_color=bg, corner_radius=0, height=40)
            row_frame.pack(fill="x")
            row_frame.pack_propagate(False)

            cond_str    = ", ".join(cont.lista_id_conduttori) if cont.lista_id_conduttori else "—"
            stato_color = SUCCESS if cont.stato == "attivo" else TEXT_M
            stato_text  = "✔ Attivo" if cont.stato == "attivo" else "✖ Chiuso"

            # FIX #5: mostra ID + nome immobile per chiarezza
            imm = self.portfolio.trova_immobile_per_id(cont.id_immobile)
            imm_label = f"{cont.id_immobile}" + (f" – {imm.nome}" if imm and imm.nome else "")

            values = [
                (cont.id_contratto,                    TEXT_M),
                (imm_label,                            TEXT_P),
                (cond_str,                             TEXT_P),
                (cont.data_inizio or "—",              TEXT_P),
                (cont.data_fine or "—",                TEXT_P),
                (f"€ {cont.canone_mensile:,.0f}",      SUCCESS),
                (stato_text,                           stato_color),
            ]
            for i, (val, color) in enumerate(values):
                lbl = ctk.CTkLabel(
                    row_frame, text=val,
                    font=ctk.CTkFont(size=12), text_color=color, anchor="w"
                )
                lbl.grid(row=0, column=i, sticky="w", padx=12)
                lbl.bind("<Button-1>", lambda e, id=cont.id_contratto: self._select(id))
                row_frame.columnconfigure(i, weight=self._col_weights[i])
            row_frame.bind("<Button-1>", lambda e, id=cont.id_contratto: self._select(id))

    def _select(self, id_cont: str):
        self._selected_id = id_cont
        self._refresh_table()

    def _close_selected(self):
        if not self._selected_id:
            messagebox.showwarning("Nessuna selezione", "Seleziona prima un contratto.")
            return
        cont = self.portfolio.trova_contratto_per_id(self._selected_id)
        if cont and cont.stato == "chiuso":
            messagebox.showinfo("Info", "Questo contratto è già chiuso.")
            return
        if messagebox.askyesno("Conferma", f"Chiudere il contratto '{self._selected_id}'?\nL'immobile verrà segnato come libero."):
            try:
                self.portfolio.chiudi_contratto(self._selected_id)
                self._refresh_table()
                self.refresh_cb()
            except ValueError as e:
                messagebox.showerror("Errore", str(e))

    def _open_form_new(self):
        ContrattoForm(self, self.portfolio, self._on_form_saved)

    def _on_form_saved(self):
        self._refresh_table()
        self.refresh_cb()


# ── Contratto Form Dialog ─────────────────────────────────────────────────────

class ContrattoForm(ctk.CTkToplevel):
    def __init__(self, parent, portfolio, on_save_cb):
        super().__init__(parent)
        self.portfolio  = portfolio
        self.on_save_cb = on_save_cb

        self.title("Nuovo Contratto")
        self.geometry("520x600")
        self.resizable(False, False)
        self.configure(fg_color=BG_MAIN)
        self.grab_set()

        self._build()

    def _build(self):
        ctk.CTkLabel(
            self, text="Nuovo Contratto",
            font=ctk.CTkFont(family="Georgia", size=17, weight="bold"),
            text_color=TEXT_P
        ).pack(pady=(20, 4), padx=24, anchor="w")
        ctk.CTkLabel(self, text="Compila i dati del contratto di locazione",
                     font=ctk.CTkFont(size=12), text_color=TEXT_M
                     ).pack(padx=24, anchor="w", pady=(0, 16))

        scroll = ctk.CTkScrollableFrame(self, fg_color=BG_CARD, corner_radius=12)
        scroll.pack(fill="both", expand=True, padx=16, pady=(0, 12))

        self._entries = {}

        # FIX #5: dropdown mostra "ID – Nome" per leggibilità
        immobili_liberi = self.portfolio.immobili_liberi()
        opzioni = [
            f"{imm.id_immobile} – {imm.nome or '?'}"
            for imm in immobili_liberi
        ]
        self._imm_var = tk.StringVar(value=opzioni[0] if opzioni else "")

        ctk.CTkLabel(scroll, text="Immobile (liberi disponibili) *",
                     font=ctk.CTkFont(size=12), text_color=TEXT_M
                     ).pack(anchor="w", padx=12, pady=(10, 2))
        if opzioni:
            ctk.CTkOptionMenu(scroll, variable=self._imm_var, values=opzioni,
                              fg_color=BG_INPUT, button_color=ACCENT,
                              text_color=TEXT_P, font=ctk.CTkFont(size=13), height=36
                              ).pack(fill="x", padx=12, pady=(0, 2))
        else:
            ctk.CTkLabel(scroll, text="Nessun immobile libero disponibile",
                         font=ctk.CTkFont(size=12), text_color=DANGER
                         ).pack(anchor="w", padx=12)

        # Conduttori
        ctk.CTkLabel(scroll, text="ID Conduttori (separati da virgola) *",
                     font=ctk.CTkFont(size=12), text_color=TEXT_M
                     ).pack(anchor="w", padx=12, pady=(10, 2))
        cond_entry = ctk.CTkEntry(scroll, height=36, fg_color=BG_INPUT,
                                  border_color=BORDER, text_color=TEXT_P,
                                  placeholder_text="es. CO0001, CO0002",
                                  font=ctk.CTkFont(size=13))
        cond_entry.pack(fill="x", padx=12, pady=(0, 2))
        self._entries["conduttori"] = cond_entry

        if self.portfolio.conduttori:
            hint = "Conduttori: " + ", ".join(
                f"{c.id_conduttore} ({c.cognome})"
                for c in list(self.portfolio.conduttori.values())[:5]
            )
            ctk.CTkLabel(scroll, text=hint, font=ctk.CTkFont(size=10),
                         text_color=TEXT_M, wraplength=430
                         ).pack(anchor="w", padx=12, pady=(0, 4))

        fields = [
            ("durata_contratto", "Durata (mesi) *"),
            ("data_inizio",      "Data inizio (gg/mm/aaaa) *"),
            ("data_fine",        "Data fine prevista (gg/mm/aaaa)"),
            ("canone_mensile",   "Canone mensile (€) *"),
        ]
        for key, label in fields:
            ctk.CTkLabel(scroll, text=label, font=ctk.CTkFont(size=12),
                         text_color=TEXT_M).pack(anchor="w", padx=12, pady=(10, 2))
            entry = ctk.CTkEntry(scroll, height=36, fg_color=BG_INPUT,
                                 border_color=BORDER, text_color=TEXT_P,
                                 font=ctk.CTkFont(size=13))
            entry.pack(fill="x", padx=12, pady=(0, 2))
            self._entries[key] = entry

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=16, pady=(0, 16))

        ctk.CTkButton(
            btn_frame, text="Annulla", width=120, height=38,
            fg_color=BG_CARD, hover_color=BG_INPUT,
            border_width=1, border_color=BORDER,
            font=ctk.CTkFont(size=13), corner_radius=8,
            command=self.destroy
        ).pack(side="left")

        ctk.CTkButton(
            btn_frame, text="Crea contratto", height=38,
            fg_color=ACCENT, hover_color=ACCENT_H,
            font=ctk.CTkFont(size=13), corner_radius=8,
            command=self._save
        ).pack(side="right")

    def _save(self):
        def get(k): return self._entries[k].get().strip()
        try:
            raw_opzione = self._imm_var.get()
            if not raw_opzione:
                raise ValueError("Nessun immobile libero selezionato.")

            # FIX #5: estrae solo l'ID dalla stringa "ID – Nome"
            id_imm = raw_opzione.split(" – ")[0].strip()

            raw_cond  = get("conduttori")
            lista_cond = [c.strip() for c in raw_cond.split(",") if c.strip()]
            if not lista_cond:
                raise ValueError("Inserisci almeno un ID conduttore.")

            durata = int(get("durata_contratto"))
            canone = float(get("canone_mensile"))

            self.portfolio.crea_contratto(
                id_immobile=id_imm,
                lista_id_conduttori=lista_cond,
                durata_contratto=durata,
                data_inizio=get("data_inizio"),
                data_fine=get("data_fine") or None,
                canone_mensile=canone
            )
            self.on_save_cb()
            self.destroy()
        except ValueError as e:
            messagebox.showerror("Errore di validazione", str(e), parent=self)
        except Exception as e:
            messagebox.showerror("Errore", str(e), parent=self)
