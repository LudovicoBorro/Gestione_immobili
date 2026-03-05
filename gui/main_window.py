import customtkinter as ctk
from gui.views.immobili_view import ImmobiliView
from gui.views.contratti_view import ContrattiView

# ── Palette ──────────────────────────────────────────────
BG_SIDEBAR   = "#0f1117"
BG_MAIN      = "#161b27"
BG_CARD      = "#1e2535"
ACCENT       = "#3b82f6"       # blue-500
ACCENT_HOVER = "#2563eb"       # blue-600
TEXT_PRIMARY = "#f1f5f9"
TEXT_MUTED   = "#64748b"
BORDER       = "#2d3748"
SUCCESS      = "#10b981"
WARNING      = "#f59e0b"


class MainWindow:
    def __init__(self, root: ctk.CTk, portfolio):
        self.root = root
        self.portfolio = portfolio
        self._active_btn = None
        self._views: dict[str, ctk.CTkFrame] = {}

        self._build_layout()
        self._build_sidebar()
        self._build_header()
        self._show_view("immobili")

    # ── Layout skeleton ──────────────────────────────────

    def _build_layout(self):
        self.root.configure(fg_color=BG_MAIN)

        # Sidebar
        self.sidebar = ctk.CTkFrame(
            self.root, width=220, corner_radius=0,
            fg_color=BG_SIDEBAR, border_width=0
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Right column
        right = ctk.CTkFrame(self.root, fg_color=BG_MAIN, corner_radius=0)
        right.pack(side="left", fill="both", expand=True)

        # Header bar
        self.header = ctk.CTkFrame(right, height=60, fg_color=BG_SIDEBAR, corner_radius=0)
        self.header.pack(fill="x")
        self.header.pack_propagate(False)

        # Content area
        self.content = ctk.CTkFrame(right, fg_color=BG_MAIN, corner_radius=0)
        self.content.pack(fill="both", expand=True, padx=24, pady=20)

    # ── Sidebar ──────────────────────────────────────────

    def _build_sidebar(self):
        # Logo / brand
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.pack(fill="x", padx=20, pady=(28, 32))

        ctk.CTkLabel(
            logo_frame, text="🏢", font=ctk.CTkFont(size=28)
        ).pack(anchor="w")
        ctk.CTkLabel(
            logo_frame, text="GestImm",
            font=ctk.CTkFont(family="Georgia", size=18, weight="bold"),
            text_color=TEXT_PRIMARY
        ).pack(anchor="w")
        ctk.CTkLabel(
            logo_frame, text="Portfolio Manager",
            font=ctk.CTkFont(size=11),
            text_color=TEXT_MUTED
        ).pack(anchor="w")

        # Separator
        ctk.CTkFrame(self.sidebar, height=1, fg_color=BORDER).pack(fill="x", padx=16, pady=(0, 20))

        # Nav label
        ctk.CTkLabel(
            self.sidebar, text="NAVIGAZIONE",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=TEXT_MUTED
        ).pack(anchor="w", padx=20, pady=(0, 8))

        # Nav buttons
        nav_items = [
            ("immobili",  "🏠  Immobili"),
            ("contratti", "📄  Contratti"),
        ]
        for key, label in nav_items:
            self._nav_button(key, label)

        # Bottom: stats summary
        self._build_sidebar_stats()

    def _nav_button(self, key: str, label: str):
        btn = ctk.CTkButton(
            self.sidebar, text=label,
            anchor="w", height=42,
            font=ctk.CTkFont(size=13),
            fg_color="transparent",
            text_color=TEXT_MUTED,
            hover_color="#1e2535",
            corner_radius=8,
            command=lambda k=key: self._show_view(k)
        )
        btn.pack(fill="x", padx=12, pady=2)
        btn._key = key
        # store for active highlight
        if not hasattr(self, "_nav_btns"):
            self._nav_btns = {}
        self._nav_btns[key] = btn

    def _build_sidebar_stats(self):
        ctk.CTkFrame(self.sidebar, height=1, fg_color=BORDER).pack(
            fill="x", padx=16, side="bottom", pady=(0, 16)
        )
        stats_frame = ctk.CTkFrame(self.sidebar, fg_color=BG_CARD, corner_radius=10)
        stats_frame.pack(fill="x", padx=12, pady=8, side="bottom")

        ctk.CTkLabel(
            stats_frame, text="Riepilogo",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=TEXT_MUTED
        ).pack(anchor="w", padx=12, pady=(10, 4))

        self.stat_immobili = ctk.CTkLabel(
            stats_frame, text=f"Immobili: {len(self.portfolio.immobili)}",
            font=ctk.CTkFont(size=12), text_color=TEXT_PRIMARY
        )
        self.stat_immobili.pack(anchor="w", padx=12, pady=1)

        self.stat_contratti = ctk.CTkLabel(
            stats_frame, text=f"Contratti attivi: {sum(1 for c in self.portfolio.contratti.values() if c.stato == 'attivo')}",
            font=ctk.CTkFont(size=12), text_color=TEXT_PRIMARY
        )
        self.stat_contratti.pack(anchor="w", padx=12, pady=1)

        self.stat_canoni = ctk.CTkLabel(
            stats_frame, text=f"Canoni/mese: €{self.portfolio.totale_canoni_mensili():,.0f}",
            font=ctk.CTkFont(size=12), text_color=SUCCESS
        )
        self.stat_canoni.pack(anchor="w", padx=12, pady=(1, 10))

    # ── Header ───────────────────────────────────────────

    def _build_header(self):
        self.header_title = ctk.CTkLabel(
            self.header, text="",
            font=ctk.CTkFont(family="Georgia", size=16, weight="bold"),
            text_color=TEXT_PRIMARY
        )
        self.header_title.pack(side="left", padx=24)

        # Save button
        ctk.CTkButton(
            self.header, text="💾  Salva",
            width=100, height=34,
            font=ctk.CTkFont(size=12),
            fg_color=ACCENT, hover_color=ACCENT_HOVER,
            corner_radius=8,
            command=self._save
        ).pack(side="right", padx=16, pady=13)

    # ── View switching ────────────────────────────────────

    def _show_view(self, key: str):
        # Highlight active nav button
        for k, btn in self._nav_btns.items():
            if k == key:
                btn.configure(fg_color=ACCENT, text_color=TEXT_PRIMARY)
            else:
                btn.configure(fg_color="transparent", text_color=TEXT_MUTED)

        titles = {"immobili": "🏠  Gestione Immobili", "contratti": "📄  Gestione Contratti"}
        self.header_title.configure(text=titles.get(key, ""))

        # Hide all frames
        for frame in self._views.values():
            frame.pack_forget()

        # Create view lazily
        if key not in self._views:
            if key == "immobili":
                frame = ImmobiliView(self.content, self.portfolio, self._refresh_stats)
            elif key == "contratti":
                frame = ContrattiView(self.content, self.portfolio, self._refresh_stats)
            else:
                return
            self._views[key] = frame

        self._views[key].pack(fill="both", expand=True)

    # ── Helpers ───────────────────────────────────────────

    def _refresh_stats(self):
        self.stat_immobili.configure(text=f"Immobili: {len(self.portfolio.immobili)}")
        self.stat_contratti.configure(
            text=f"Contratti attivi: {sum(1 for c in self.portfolio.contratti.values() if c.stato == 'attivo')}"
        )
        self.stat_canoni.configure(
            text=f"Canoni/mese: €{self.portfolio.totale_canoni_mensili():,.0f}"
        )

    def _save(self):
        from services.persistence import salva_portfolio
        salva_portfolio(self.portfolio)
        self._show_toast("✔  Dati salvati correttamente")

    def _show_toast(self, msg: str):
        toast = ctk.CTkLabel(
            self.root, text=msg,
            fg_color=SUCCESS, text_color="white",
            corner_radius=8, font=ctk.CTkFont(size=12),
            padx=16, pady=8
        )
        toast.place(relx=0.5, rely=0.95, anchor="center")
        self.root.after(2500, toast.destroy)
