import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
from models.conduttore import Conduttore

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


class ConduttoriView(ctk.CTkFrame):
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
            top, text="＋  Nuovo Conduttore", height=36,
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
            card, text=str(len(self.portfolio.conduttori)),
            font=ctk.CTkFont(size=22, weight="bold"), text_color=ACCENT
        )
        self._total_label.pack()
        ctk.CTkLabel(card, text="Totale conduttori",
                     font=ctk.CTkFont(size=11), text_color=TEXT_M).pack()

        self._build_table()
        self._refresh_table()

    def _build_table(self):
        wrapper = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=12)
        wrapper.pack(fill="both", expand=True)

        cols    = ["ID", "Nome", "Cognome", "Telefono", "Email", "Data nascita", "Sesso"]
        weights = [1, 2, 2, 2, 3, 2, 1]

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
        self._total_label.configure(text=str(len(self.portfolio.conduttori)))

        for w in self.table_scroll.winfo_children():
            w.destroy()

        query = self.search_var.get().lower()
        items = list(self.portfolio.conduttori.values())
        if query:
            items = [c for c in items
                     if query in (c.nome or "").lower()
                     or query in (c.cognome or "").lower()]

        for idx, cond in enumerate(items):
            bg = ROW_SEL if cond.id_conduttore == self._selected_id else (ROW_EVEN if idx % 2 == 0 else ROW_ODD)
            row_frame = ctk.CTkFrame(self.table_scroll, fg_color=bg, corner_radius=0, height=40)
            row_frame.pack(fill="x")
            row_frame.pack_propagate(False)

            values = [
                (cond.id_conduttore,          TEXT_M),
                (cond.nome or "—",            TEXT_P),
                (cond.cognome or "—",         TEXT_P),
                (cond.contatto_tel or "—",    TEXT_P),
                (cond.email or "—",           TEXT_P),
                (cond.data_nascita or "—",    TEXT_P),
                (cond.sesso or "—",           TEXT_P),
            ]
            for i, (val, color) in enumerate(values):
                lbl = ctk.CTkLabel(
                    row_frame, text=val,
                    font=ctk.CTkFont(size=12), text_color=color, anchor="w"
                )
                lbl.grid(row=0, column=i, sticky="w", padx=12)
                lbl.bind("<Button-1>", lambda e, id=cond.id_conduttore: self._select(id))
                row_frame.columnconfigure(i, weight=self._col_weights[i])
            row_frame.bind("<Button-1>", lambda e, id=cond.id_conduttore: self._select(id))

    def _select(self, id_cond: str):
        self._selected_id = id_cond
        self._refresh_table()

    def _delete_selected(self):
        if not self._selected_id:
            messagebox.showwarning("Nessuna selezione", "Seleziona prima un conduttore.")
            return
        # Blocca se il conduttore è in un contratto attivo
        for cont in self.portfolio.contratti.values():
            if cont.stato == "attivo" and self._selected_id in cont.lista_id_conduttori:
                messagebox.showerror(
                    "Errore",
                    f"Il conduttore è associato al contratto attivo '{cont.id_contratto}'.\nChiudi prima il contratto."
                )
                return
        cond = self.portfolio.trova_conduttore_per_id(self._selected_id)
        if messagebox.askyesno("Conferma", f"Eliminare il conduttore '{cond.nome} {cond.cognome}'?"):
            del self.portfolio.conduttori[self._selected_id]
            self._selected_id = None
            self._refresh_table()
            self.refresh_cb()

    def _open_form_new(self):
        ConduttoreForm(self, self.portfolio, None, self._on_saved)

    def _open_form_edit(self):
        if not self._selected_id:
            messagebox.showwarning("Nessuna selezione", "Seleziona prima un conduttore.")
            return
        cond = self.portfolio.trova_conduttore_per_id(self._selected_id)
        ConduttoreForm(self, self.portfolio, cond, self._on_saved)

    def _on_saved(self):
        self._refresh_table()
        self.refresh_cb()


# ── Conduttore Form Dialog ────────────────────────────────────────────────────

class ConduttoreForm(ctk.CTkToplevel):
    def __init__(self, parent, portfolio, conduttore: Conduttore | None, on_save_cb):
        super().__init__(parent)
        self.portfolio  = portfolio
        self.conduttore = conduttore
        self.on_save_cb = on_save_cb
        self.is_edit    = conduttore is not None

        self.title("Modifica Conduttore" if self.is_edit else "Nuovo Conduttore")
        self.geometry("440x520")
        self.resizable(False, False)
        self.configure(fg_color=BG_MAIN)
        self.grab_set()

        self._build()
        if self.is_edit:
            self._populate()

    def _build(self):
        ctk.CTkLabel(
            self, text="Modifica Conduttore" if self.is_edit else "Nuovo Conduttore",
            font=ctk.CTkFont(family="Georgia", size=17, weight="bold"),
            text_color=TEXT_P
        ).pack(pady=(20, 4), padx=24, anchor="w")
        ctk.CTkLabel(self, text="Dati anagrafici del conduttore",
                     font=ctk.CTkFont(size=12), text_color=TEXT_M
                     ).pack(padx=24, anchor="w", pady=(0, 16))

        scroll = ctk.CTkScrollableFrame(self, fg_color=BG_CARD, corner_radius=12)
        scroll.pack(fill="both", expand=True, padx=16, pady=(0, 12))

        self._entries = {}
        fields = [
            ("nome",         "Nome *"),
            ("cognome",      "Cognome *"),
            ("contatto_tel", "Telefono (10 cifre) *"),
            ("email",        "Email"),
            ("data_nascita", "Data di nascita (gg/mm/aaaa)"),
        ]
        for key, label in fields:
            ctk.CTkLabel(scroll, text=label, font=ctk.CTkFont(size=12),
                         text_color=TEXT_M).pack(anchor="w", padx=12, pady=(10, 2))
            entry = ctk.CTkEntry(scroll, height=36, fg_color=BG_INPUT,
                                 border_color=BORDER, text_color=TEXT_P,
                                 font=ctk.CTkFont(size=13))
            entry.pack(fill="x", padx=12, pady=(0, 2))
            self._entries[key] = entry

        ctk.CTkLabel(scroll, text="Sesso", font=ctk.CTkFont(size=12),
                     text_color=TEXT_M).pack(anchor="w", padx=12, pady=(10, 2))
        self._sesso_var = tk.StringVar(value="M")
        ctk.CTkOptionMenu(scroll, variable=self._sesso_var, values=["M", "F"],
                          fg_color=BG_INPUT, button_color=ACCENT,
                          text_color=TEXT_P, font=ctk.CTkFont(size=13),
                          height=36).pack(fill="x", padx=12, pady=(0, 2))

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
            btn_frame, text="Salva conduttore", height=38,
            fg_color=ACCENT, hover_color=ACCENT_H,
            font=ctk.CTkFont(size=13), corner_radius=8,
            command=self._save
        ).pack(side="right")

    def _populate(self):
        c = self.conduttore
        for key, val in {
            "nome": c.nome, "cognome": c.cognome,
            "contatto_tel": c.contatto_tel, "email": c.email,
            "data_nascita": c.data_nascita
        }.items():
            if val is not None:
                self._entries[key].insert(0, str(val))
        if c.sesso:
            self._sesso_var.set(c.sesso)

    def _save(self):
        def get(k): return self._entries[k].get().strip()
        try:
            if self.is_edit:
                c = self.conduttore
                c.nome         = get("nome")
                c.cognome      = get("cognome")
                c.contatto_tel = get("contatto_tel")
                c.email        = get("email")
                c.data_nascita = get("data_nascita")
                c.sesso        = self._sesso_var.get()
            else:
                self.portfolio.crea_conduttore(
                    nome=get("nome"),
                    cognome=get("cognome"),
                    contatto_tel=get("contatto_tel"),
                    email=get("email"),
                    sesso=self._sesso_var.get(),
                    data_nascita=get("data_nascita")
                )
            self.on_save_cb()
            self.destroy()
        except ValueError as e:
            messagebox.showerror("Errore di validazione", str(e), parent=self)
        except Exception as e:
            messagebox.showerror("Errore", str(e), parent=self)