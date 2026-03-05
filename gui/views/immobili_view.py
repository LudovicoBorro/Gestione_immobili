import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
from models.immobile import Immobile

BG_MAIN   = "#161b27"
BG_CARD   = "#1e2535"
BG_INPUT  = "#252d3d"
ACCENT    = "#3b82f6"
ACCENT_H  = "#2563eb"
DANGER    = "#ef4444"
DANGER_H  = "#dc2626"
SUCCESS   = "#10b981"
TEXT_P    = "#f1f5f9"
TEXT_M    = "#64748b"
BORDER    = "#2d3748"
ROW_EVEN  = "#1e2535"
ROW_ODD   = "#1a2030"
ROW_SEL   = "#1e3a5f"


class ImmobiliView(ctk.CTkFrame):
    def __init__(self, parent, portfolio, refresh_cb):
        super().__init__(parent, fg_color=BG_MAIN, corner_radius=0)
        self.portfolio = portfolio
        self.refresh_cb = refresh_cb
        self._selected_id = None

        self._build()

    # ── Layout ──────────────────────────────────────────

    def _build(self):
        # Top bar: search + buttons
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", pady=(0, 16))

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self._refresh_table())
        ctk.CTkEntry(
            top, textvariable=self.search_var,
            placeholder_text="🔍  Cerca per nome, città...",
            width=280, height=36,
            fg_color=BG_CARD, border_color=BORDER,
            text_color=TEXT_P, font=ctk.CTkFont(size=13)
        ).pack(side="left")

        ctk.CTkButton(
            top, text="＋  Nuovo Immobile", height=36,
            fg_color=ACCENT, hover_color=ACCENT_H,
            font=ctk.CTkFont(size=13), corner_radius=8,
            command=self._open_form_new
        ).pack(side="right")

        ctk.CTkButton(
            top, text="✏  Modifica", height=36, width=110,
            fg_color=BG_CARD, hover_color=BG_INPUT,
            border_width=1, border_color=BORDER,
            font=ctk.CTkFont(size=13), corner_radius=8,
            command=self._open_form_edit
        ).pack(side="right", padx=(0, 8))

        ctk.CTkButton(
            top, text="🗑  Elimina", height=36, width=100,
            fg_color=BG_CARD, hover_color="#2d1515",
            border_width=1, border_color=DANGER,
            text_color=DANGER,
            font=ctk.CTkFont(size=13), corner_radius=8,
            command=self._delete_selected
        ).pack(side="right", padx=(0, 8))

        # Summary cards row
        self._build_summary_cards()

        # Table
        self._build_table()
        self._refresh_table()

    def _build_summary_cards(self):
        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(fill="x", pady=(0, 16))

        cards = [
            ("Totale",    lambda: len(self.portfolio.immobili),                 "#3b82f6"),
            ("Locati",    lambda: len(self.portfolio.immobili_locati()),         SUCCESS),
            ("Liberi",    lambda: len(self.portfolio.immobili_liberi()),         "#f59e0b"),
            ("Personali", lambda: len(self.portfolio.immobili_personali()),      TEXT_M),
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

        # Header row
        cols = ["ID", "Nome", "Città", "Tipo", "Stato", "Canone €/mese", "Metratura m²"]
        weights = [1, 2, 2, 1, 1, 2, 1]
        header = ctk.CTkFrame(wrapper, fg_color="#131929", corner_radius=0)
        header.pack(fill="x")
        for i, (col, w) in enumerate(zip(cols, weights)):
            header.columnconfigure(i, weight=w)
        for i, col in enumerate(cols):
            ctk.CTkLabel(
                header, text=col.upper(),
                font=ctk.CTkFont(size=10, weight="bold"),
                text_color=TEXT_M
            ).grid(row=0, column=i, sticky="w", padx=12, pady=10)

        # Scrollable rows
        self.table_scroll = ctk.CTkScrollableFrame(
            wrapper, fg_color="transparent", corner_radius=0
        )
        self.table_scroll.pack(fill="both", expand=True)
        self._col_weights = weights
        self._cols = cols

    def _refresh_table(self, *_):
        # Update cards
        for label, (lbl, fn) in self._card_labels.items():
            lbl.configure(text=str(fn()))

        # Clear rows
        for widget in self.table_scroll.winfo_children():
            widget.destroy()
        self._row_frames = {}

        query = self.search_var.get().lower()
        items = list(self.portfolio.immobili.values())
        if query:
            items = [i for i in items if query in i.nome.lower() or query in (i.citta or "").lower()]

        for idx, imm in enumerate(items):
            bg = ROW_SEL if imm.id_immobile == self._selected_id else (ROW_EVEN if idx % 2 == 0 else ROW_ODD)
            row_frame = ctk.CTkFrame(self.table_scroll, fg_color=bg, corner_radius=0, height=40)
            row_frame.pack(fill="x")
            row_frame.pack_propagate(False)

            # Find canone from active contract
            canone = "—"
            for c in self.portfolio.contratti.values():
                if c.id_immobile == imm.id_immobile and c.stato == "attivo":
                    canone = f"€ {c.canone_mensile:,.0f}"
                    break

            stato_color = {
                "locato": SUCCESS, "libero": "#f59e0b", "personale": TEXT_M
            }.get(imm.stato_loc, TEXT_P)

            values = [
                (imm.id_immobile, TEXT_M),
                (imm.nome or "—", TEXT_P),
                (imm.citta or "—", TEXT_P),
                (imm.tipo_immobile or "—", TEXT_P),
                (imm.stato_loc or "—", stato_color),
                (canone, SUCCESS if canone != "—" else TEXT_M),
                (f"{imm.metratura} m²" if imm.metratura else "—", TEXT_P),
            ]
            for i, (val, color) in enumerate(values):
                lbl = ctk.CTkLabel(
                    row_frame, text=val,
                    font=ctk.CTkFont(size=12), text_color=color, anchor="w"
                )
                lbl.grid(row=0, column=i, sticky="w", padx=12)
                lbl.bind("<Button-1>", lambda e, id=imm.id_immobile: self._select(id))
                row_frame.columnconfigure(i, weight=self._col_weights[i])
            row_frame.bind("<Button-1>", lambda e, id=imm.id_immobile: self._select(id))
            self._row_frames[imm.id_immobile] = row_frame

    def _select(self, id_imm: str):
        self._selected_id = id_imm
        self._refresh_table()

    # ── Delete ────────────────────────────────────────────

    def _delete_selected(self):
        if not self._selected_id:
            messagebox.showwarning("Nessuna selezione", "Seleziona prima un immobile.")
            return
        imm = self.portfolio.trova_immobile_per_id(self._selected_id)
        if imm and imm.stato_loc == "locato":
            messagebox.showerror("Errore", "Non puoi eliminare un immobile locato. Chiudi prima il contratto.")
            return
        if messagebox.askyesno("Conferma", f"Eliminare l'immobile '{imm.nome}'?"):
            del self.portfolio.immobili[self._selected_id]
            self._selected_id = None
            self._refresh_table()
            self.refresh_cb()

    # ── Form: nuovo / modifica ────────────────────────────

    def _open_form_new(self):
        ImmobileForm(self, self.portfolio, None, self._on_form_saved)

    def _open_form_edit(self):
        if not self._selected_id:
            messagebox.showwarning("Nessuna selezione", "Seleziona prima un immobile.")
            return
        imm = self.portfolio.trova_immobile_per_id(self._selected_id)
        ImmobileForm(self, self.portfolio, imm, self._on_form_saved)

    def _on_form_saved(self):
        self._refresh_table()
        self.refresh_cb()


# ── Immobile Form Dialog ──────────────────────────────────────────────────────

class ImmobileForm(ctk.CTkToplevel):
    def __init__(self, parent, portfolio, immobile: Immobile | None, on_save_cb):
        super().__init__(parent)
        self.portfolio = portfolio
        self.immobile = immobile
        self.on_save_cb = on_save_cb
        self.is_edit = immobile is not None

        self.title("Modifica Immobile" if self.is_edit else "Nuovo Immobile")
        self.geometry("560x680")
        self.resizable(False, False)
        self.configure(fg_color=BG_MAIN)
        self.grab_set()

        self._build()
        if self.is_edit:
            self._populate()

    def _build(self):
        ctk.CTkLabel(
            self, text="Modifica Immobile" if self.is_edit else "Nuovo Immobile",
            font=ctk.CTkFont(family="Georgia", size=17, weight="bold"),
            text_color=TEXT_P
        ).pack(pady=(20, 4), padx=24, anchor="w")

        ctk.CTkLabel(self, text="Compila i dati dell'immobile",
                     font=ctk.CTkFont(size=12), text_color=TEXT_M
                     ).pack(padx=24, anchor="w", pady=(0, 16))

        scroll = ctk.CTkScrollableFrame(self, fg_color=BG_CARD, corner_radius=12)
        scroll.pack(fill="both", expand=True, padx=16, pady=(0, 12))

        self._entries = {}

        fields = [
            ("nome",              "Nome immobile *",        "text"),
            ("indirizzo",         "Indirizzo *",            "text"),
            ("citta",             "Città *",                "text"),
            ("data_acquisto",     "Data acquisto (gg/mm/aaaa)", "text"),
            ("foglio_cat",        "Foglio catastale",       "int"),
            ("numero_cat",        "Numero catastale",       "int"),
            ("sublocazione_cat",  "Sublocazione catastale", "int"),
            ("prezzo_acq",        "Prezzo acquisto (€) *",  "float"),
            ("num_locali",        "Numero locali *",        "int"),
            ("metratura",         "Metratura (m²) *",       "float"),
            ("spese_notarili",    "Spese notarili (€)",     "float"),
            ("spese_condominiali","Spese condominiali (€)", "float"),
        ]

        for key, label, _ in fields:
            self._field_row(scroll, key, label)

        # Dropdowns
        self._tipo_var = tk.StringVar(value="residenziale")
        self._stato_var = tk.StringVar(value="libero")

        self._dropdown_row(scroll, "Tipo immobile", self._tipo_var, ["residenziale", "commerciale"])
        self._dropdown_row(scroll, "Stato locazione", self._stato_var, ["libero", "locato", "personale"])

        # Amministratore (optional)
        self._field_row(scroll, "id_amministratore", "ID Amministratore (opz.)")

        # Buttons
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
            btn_frame, text="Salva immobile", height=38,
            fg_color=ACCENT, hover_color=ACCENT_H,
            font=ctk.CTkFont(size=13), corner_radius=8,
            command=self._save
        ).pack(side="right")

    def _field_row(self, parent, key, label):
        ctk.CTkLabel(parent, text=label, font=ctk.CTkFont(size=12),
                     text_color=TEXT_M).pack(anchor="w", padx=12, pady=(10, 2))
        entry = ctk.CTkEntry(parent, height=36, fg_color=BG_INPUT,
                             border_color=BORDER, text_color=TEXT_P,
                             font=ctk.CTkFont(size=13))
        entry.pack(fill="x", padx=12, pady=(0, 2))
        self._entries[key] = entry

    def _dropdown_row(self, parent, label, var, values):
        ctk.CTkLabel(parent, text=label, font=ctk.CTkFont(size=12),
                     text_color=TEXT_M).pack(anchor="w", padx=12, pady=(10, 2))
        ctk.CTkOptionMenu(parent, variable=var, values=values,
                          fg_color=BG_INPUT, button_color=ACCENT,
                          text_color=TEXT_P, font=ctk.CTkFont(size=13),
                          height=36).pack(fill="x", padx=12, pady=(0, 2))

    def _populate(self):
        imm = self.immobile
        mapping = {
            "nome": imm.nome, "indirizzo": imm.indirizzo, "citta": imm.citta,
            "data_acquisto": imm.data_acquisto,
            "foglio_cat": imm.foglio_cat, "numero_cat": imm.numero_cat,
            "sublocazione_cat": imm.sublocazione_cat,
            "prezzo_acq": imm.prezzo_acq, "num_locali": imm.num_locali,
            "metratura": imm.metratura, "spese_notarili": imm.spese_notarili,
            "spese_condominiali": imm.spese_condominiali,
            "id_amministratore": imm.id_amministratore,
        }
        for key, val in mapping.items():
            if key in self._entries and val is not None:
                self._entries[key].insert(0, str(val))
        if imm.tipo_immobile:
            self._tipo_var.set(imm.tipo_immobile)
        if imm.stato_loc:
            self._stato_var.set(imm.stato_loc)

    def _save(self):
        def get(key): return self._entries[key].get().strip()
        def get_float(key, default=0.0):
            v = get(key)
            return float(v) if v else default
        def get_int(key, default=0):
            v = get(key)
            return int(v) if v else default

        try:
            if self.is_edit:
                imm = self.immobile
                imm.nome             = get("nome")
                imm.indirizzo        = get("indirizzo")
                imm.citta            = get("citta")
                imm.data_acquisto    = get("data_acquisto")
                imm.foglio_cat       = get_int("foglio_cat")
                imm.numero_cat       = get_int("numero_cat")
                imm.sublocazione_cat = get_int("sublocazione_cat")
                imm.prezzo_acq       = get_float("prezzo_acq")
                imm.num_locali       = get_int("num_locali")
                imm.metratura        = get_float("metratura")
                imm.spese_notarili   = get_float("spese_notarili")
                imm.spese_condominiali = get_float("spese_condominiali")
                imm.tipo_immobile    = self._tipo_var.get()
                imm.stato_loc        = self._stato_var.get()
                id_amm = get("id_amministratore")
                imm.id_amministratore = id_amm if id_amm else None
            else:
                id_amm = get("id_amministratore") or None
                self.portfolio.crea_immobile(
                    nome=get("nome"),
                    indirizzo=get("indirizzo"),
                    citta=get("citta"),
                    data_acquisto=get("data_acquisto"),
                    foglio_cat=get_int("foglio_cat"),
                    numero_cat=get_int("numero_cat"),
                    sublocazione_cat=get_int("sublocazione_cat"),
                    prezzo_acq=get_float("prezzo_acq"),
                    num_locali=get_int("num_locali"),
                    metratura=get_float("metratura"),
                    spese_notarili=get_float("spese_notarili"),
                    spese_condominiali=get_float("spese_condominiali"),
                    tipo_immobile=self._tipo_var.get(),
                    stato_loc=self._stato_var.get(),
                    id_amministratore=id_amm
                )
            self.on_save_cb()
            self.destroy()
        except ValueError as e:
            messagebox.showerror("Errore di validazione", str(e), parent=self)
        except Exception as e:
            messagebox.showerror("Errore", str(e), parent=self)
