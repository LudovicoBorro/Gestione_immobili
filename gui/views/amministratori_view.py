import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
from models.amministratore import Amministratore

BG_MAIN   = "#161b27"
BG_CARD   = "#1e2535"
BG_INPUT  = "#252d3d"
ACCENT    = "#3b82f6"
ACCENT_H  = "#2563eb"
DANGER    = "#ef4444"
SUCCESS   = "#10b981"
TEXT_P    = "#f1f5f9"
TEXT_M    = "#64748b"
BORDER    = "#2d3748"
ROW_EVEN  = "#1e2535"
ROW_ODD   = "#1a2030"
ROW_SEL   = "#1e3a5f"


class AmministratoriView(ctk.CTkFrame):
    def __init__(self, parent, portfolio, refresh_cb):
        super().__init__(parent, fg_color=BG_MAIN, corner_radius=0)
        self.portfolio  = portfolio
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
            placeholder_text="🔍  Cerca per nome, cognome...",
            width=280, height=36,
            fg_color=BG_CARD, border_color=BORDER,
            text_color=TEXT_P, font=ctk.CTkFont(size=13)
        ).pack(side="left")

        ctk.CTkButton(
            top, text="＋  Nuovo Amministratore", height=36,
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

        # Card riepilogo
        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(fill="x", pady=(0, 16))
        card = ctk.CTkFrame(row, fg_color=BG_CARD, corner_radius=10)
        card.pack(side="left", ipadx=16, ipady=10)
        self._total_label = ctk.CTkLabel(
            card, text=str(len(self.portfolio.amministratori)),
            font=ctk.CTkFont(size=22, weight="bold"), text_color=ACCENT
        )
        self._total_label.pack()
        ctk.CTkLabel(card, text="Totale amministratori",
                     font=ctk.CTkFont(size=11), text_color=TEXT_M).pack()

        self._build_table()
        self._refresh_table()

    def _build_table(self):
        wrapper = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=12)
        wrapper.pack(fill="both", expand=True)

        cols    = ["ID", "Nome", "Cognome", "Telefono", "Email", "Indirizzo ufficio", "Immobili gestiti"]
        weights = [1, 2, 2, 2, 3, 3, 2]

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
        self._total_label.configure(text=str(len(self.portfolio.amministratori)))

        for w in self.table_scroll.winfo_children():
            w.destroy()

        query = self.search_var.get().lower()
        items = list(self.portfolio.amministratori.values())
        if query:
            items = [a for a in items
                     if query in (a.nome or "").lower()
                     or query in (a.cognome or "").lower()]

        for idx, amm in enumerate(items):
            bg = ROW_SEL if amm.id_amministratore == self._selected_id else (ROW_EVEN if idx % 2 == 0 else ROW_ODD)
            row_frame = ctk.CTkFrame(self.table_scroll, fg_color=bg, corner_radius=0, height=40)
            row_frame.pack(fill="x")
            row_frame.pack_propagate(False)

            # Conta gli immobili gestiti da questo amministratore
            n_immobili = sum(
                1 for imm in self.portfolio.immobili.values()
                if imm.id_amministratore == amm.id_amministratore
            )
            gestiti = str(n_immobili) if n_immobili > 0 else "—"

            values = [
                (amm.id_amministratore,         TEXT_M),
                (amm.nome or "—",               TEXT_P),
                (amm.cognome or "—",            TEXT_P),
                (amm.contatto_tel or "—",       TEXT_P),
                (amm.email or "—",              TEXT_P),
                (amm.indirizzo_ufficio or "—",  TEXT_P),
                (gestiti,                        SUCCESS if n_immobili > 0 else TEXT_M),
            ]
            for i, (val, color) in enumerate(values):
                lbl = ctk.CTkLabel(
                    row_frame, text=val,
                    font=ctk.CTkFont(size=12), text_color=color, anchor="w"
                )
                lbl.grid(row=0, column=i, sticky="w", padx=12)
                lbl.bind("<Button-1>", lambda e, id=amm.id_amministratore: self._select(id))
                row_frame.columnconfigure(i, weight=self._col_weights[i])
            row_frame.bind("<Button-1>", lambda e, id=amm.id_amministratore: self._select(id))

    def _select(self, id_amm: str):
        self._selected_id = id_amm
        self._refresh_table()

    def _delete_selected(self):
        if not self._selected_id:
            messagebox.showwarning("Nessuna selezione", "Seleziona prima un amministratore.")
            return
        # Avvisa se ha immobili collegati (non blocca, l'associazione è opzionale)
        n = sum(1 for imm in self.portfolio.immobili.values()
                if imm.id_amministratore == self._selected_id)
        amm = self.portfolio.trova_amministratore_per_id(self._selected_id)
        msg = f"Eliminare l'amministratore '{amm.nome} {amm.cognome}'?"
        if n > 0:
            msg += f"\n\nAttenzione: gestisce {n} immobile{'i' if n > 1 else ''} che rimarranno senza amministratore."
        if messagebox.askyesno("Conferma", msg):
            del self.portfolio.amministratori[self._selected_id]
            # Scollega dagli immobili
            for imm in self.portfolio.immobili.values():
                if imm.id_amministratore == self._selected_id:
                    imm.id_amministratore = None
            self._selected_id = None
            self._refresh_table()
            self.refresh_cb()

    def _open_form_new(self):
        AmministratoreForm(self, self.portfolio, None, self._on_saved)

    def _open_form_edit(self):
        if not self._selected_id:
            messagebox.showwarning("Nessuna selezione", "Seleziona prima un amministratore.")
            return
        amm = self.portfolio.trova_amministratore_per_id(self._selected_id)
        AmministratoreForm(self, self.portfolio, amm, self._on_saved)

    def _on_saved(self):
        self._refresh_table()
        self.refresh_cb()


# ── Amministratore Form Dialog ────────────────────────────────────────────────

class AmministratoreForm(ctk.CTkToplevel):
    def __init__(self, parent, portfolio, amministratore: Amministratore | None, on_save_cb):
        super().__init__(parent)
        self.portfolio      = portfolio
        self.amministratore = amministratore
        self.on_save_cb     = on_save_cb
        self.is_edit        = amministratore is not None

        self.title("Modifica Amministratore" if self.is_edit else "Nuovo Amministratore")
        self.geometry("440x480")
        self.resizable(False, False)
        self.configure(fg_color=BG_MAIN)
        self.grab_set()

        self._build()
        if self.is_edit:
            self._populate()

    def _build(self):
        ctk.CTkLabel(
            self, text="Modifica Amministratore" if self.is_edit else "Nuovo Amministratore",
            font=ctk.CTkFont(family="Georgia", size=17, weight="bold"),
            text_color=TEXT_P
        ).pack(pady=(20, 4), padx=24, anchor="w")
        ctk.CTkLabel(self, text="Dati dell'amministratore condominiale",
                     font=ctk.CTkFont(size=12), text_color=TEXT_M
                     ).pack(padx=24, anchor="w", pady=(0, 16))

        scroll = ctk.CTkScrollableFrame(self, fg_color=BG_CARD, corner_radius=12)
        scroll.pack(fill="both", expand=True, padx=16, pady=(0, 12))

        self._entries = {}
        fields = [
            ("nome",              "Nome *"),
            ("cognome",           "Cognome *"),
            ("contatto_tel",      "Telefono (10 cifre) *"),
            ("email",             "Email"),
            ("indirizzo_ufficio", "Indirizzo ufficio"),
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
            btn_frame, text="Salva amministratore", height=38,
            fg_color=ACCENT, hover_color=ACCENT_H,
            font=ctk.CTkFont(size=13), corner_radius=8,
            command=self._save
        ).pack(side="right")

    def _populate(self):
        a = self.amministratore
        for key, val in {
            "nome": a.nome, "cognome": a.cognome,
            "contatto_tel": a.contatto_tel, "email": a.email,
            "indirizzo_ufficio": a.indirizzo_ufficio
        }.items():
            if val is not None:
                self._entries[key].insert(0, str(val))

    def _save(self):
        def get(k): return self._entries[k].get().strip()
        try:
            if self.is_edit:
                a = self.amministratore
                a.nome              = get("nome")
                a.cognome           = get("cognome")
                a.contatto_tel      = get("contatto_tel")
                a.email             = get("email")
                a.indirizzo_ufficio = get("indirizzo_ufficio")
            else:
                self.portfolio.crea_amministratore(
                    nome=get("nome"),
                    cognome=get("cognome"),
                    contatto_tel=get("contatto_tel"),
                    email=get("email"),
                    indirizzo_ufficio=get("indirizzo_ufficio")
                )
            self.on_save_cb()
            self.destroy()
        except ValueError as e:
            messagebox.showerror("Errore di validazione", str(e), parent=self)
        except Exception as e:
            messagebox.showerror("Errore", str(e), parent=self)