from operator import add
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import conexion
import darkdetect

BG_DARK    = "#FFFFFF"
BG_PANEL   = "#F3F3F3"
BG_ENTRY   = "#DBCDCD"
ACCENT     = "#B6B6BD"       
ACCENT_DIM = "#9B9B9B"
FG_WHITE   = "#000000"
FG_MUTED   = "#000000"
BORDER     = "#3A3A45"
SUCCESS    = "#088135"
FONT_MONO  = ("Consolas", 10)
FONT_HEAD  = ("Consolas", 20, "bold")
FONT_LABEL = ("Consolas", 9)
FONT_BTN   = ("Consolas", 10, "bold")

def apply_dark_theme():
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Dark.TCombobox",
        fieldbackground=BG_ENTRY,
        background=BG_PANEL,
        foreground=FG_WHITE,
        selectbackground=ACCENT_DIM,
        selectforeground=FG_WHITE,
        bordercolor=BORDER,
        arrowcolor=ACCENT,
        relief="flat",
        padding=6,
    )
    style.map("Dark.TCombobox",
        fieldbackground=[("readonly", BG_ENTRY)],
        foreground=[("readonly", FG_WHITE)],
        bordercolor=[("focus", ACCENT), ("!focus", BORDER)],
    )

class ConfiguradorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Configurador")
        self.root.geometry("560x520") # Aumenté un poco el alto para el botón
        self.root.configure(bg=BG_DARK)
        self.root.iconbitmap("favicon.ico")
        apply_dark_theme()
        self._build_ui()
        self.cargar_combobox()
        self.cargar()

    def _entry(self, parent, **kwargs):
        return tk.Entry(
            parent,
            bg=BG_ENTRY,
            fg=FG_WHITE,
            insertbackground=ACCENT,
            relief="flat",
            font=FONT_MONO,
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=ACCENT,
            **kwargs,
        )

    def _label(self, parent, text, small=False, **kwargs):
        color = FG_MUTED if small else FG_WHITE
        font  = FONT_LABEL if small else FONT_MONO
        return tk.Label(parent, text=text, bg=parent["bg"], fg=color, font=font, **kwargs)

    def abrir_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Agregar nuevo")
        popup.geometry("300x340")
        popup.resizable(False, False)
        popup.configure(bg=BG_DARK)
        
        # Campos del Popup
        tk.Label(popup, text="Machine", bg=BG_DARK, font=FONT_LABEL).pack(pady=(10, 0))
        machine_e = tk.Entry(popup); machine_e.pack(pady=5)

        tk.Label(popup, text="Operator", bg=BG_DARK, font=FONT_LABEL).pack(pady=(5, 0))
        operator_e = tk.Entry(popup); operator_e.pack(pady=5)

        tk.Label(popup, text="Process", bg=BG_DARK, font=FONT_LABEL).pack(pady=(5, 0))
        process_e = tk.Entry(popup); process_e.pack(pady=5)

        tk.Label(popup, text="Station", bg=BG_DARK, font=FONT_LABEL).pack(pady=(5, 0))
        station_e = ttk.Combobox(popup, values=["Estación 10", "Estación 20", "Estación 30"], state="readonly")
        station_e.pack(pady=5)

        def guardar_nuevo():
            m, o, p, s = machine_e.get().strip(), operator_e.get().strip(), process_e.get().strip(), station_e.get()
            if not all([m, o, p, s]):
                messagebox.showwarning("Campos incompletos", "Completa todos los campos.")
                return
            try:
                conexion.insert_simple(m, o, p, s)
                messagebox.showinfo("Éxito", "Datos guardados.")
                self.cargar_combobox()
                popup.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        btn_save = tk.Button(popup, text="Guardar", command=guardar_nuevo, bg=SUCCESS, fg="white", font=FONT_BTN, relief="flat")
        btn_save.pack(pady=20)

    def cargar_combobox(self):
        try:
            self.process["values"] = conexion.select_distinct("process_name")
        except Exception as e:
            print(f"Error al cargar Process Name: {e}")

    def _auto_rellenar(self, event):
        proceso = self.process.get()
        if not proceso: return
        try:
            datos = conexion.obtener_datos_por_proceso(proceso)
            if datos:
                for widget, value in zip([self.machine, self.operator, self.station], datos):
                    widget.delete(0, tk.END)
                    widget.insert(0, str(value) if value is not None else "")
                self.status_var.set(f"✔ Datos cargados para: {proceso}")
        except Exception as e:
            print(f"Error al auto-rellenar: {e}")

    def _build_ui(self):
        # --- Header ---
        header = tk.Frame(self.root, bg=BG_DARK)
        header.pack(fill="x", padx=24, pady=(20, 0))
        tk.Label(header, text="⚙ CONFIGURADOR", font=FONT_HEAD, bg=BG_DARK, fg=FG_WHITE).pack(side="left")
        tk.Frame(self.root, bg=ACCENT, height=2).pack(fill="x", padx=24, pady=(8, 0))

        # --- Panel principal ---
        panel = tk.Frame(self.root, bg=BG_PANEL, highlightthickness=1, highlightbackground=BORDER)
        panel.pack(fill="both", padx=24, pady=16)
        inner = tk.Frame(panel, bg=BG_PANEL)
        inner.pack(fill="both", expand=True, padx=20, pady=16)

        # STATION (Entry)
        self._label(inner, "STATION", small=True).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 2))
        self.station = self._entry(inner)
        self.station.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 14), ipady=4)

        # MACHINE / OPERATOR (Entries)
        self._label(inner, "MACHINE NAME", small=True).grid(row=2, column=0, sticky="w", pady=(0, 2))
        self._label(inner, "ID OPERATOR", small=True).grid(row=2, column=1, sticky="w", padx=(16, 0), pady=(0, 2))

        self.machine = self._entry(inner)
        self.machine.grid(row=3, column=0, sticky="ew", ipady=4, pady=(0, 14))

        self.operator = self._entry(inner)
        self.operator.grid(row=3, column=1, sticky="ew", padx=(16, 0), ipady=4, pady=(0, 14))

        # PROCESS NAME (Combobox)
        self._label(inner, "PROCESS NAME", small=True).grid(row=4, column=0, columnspan=2, sticky="w", pady=(0, 2))
        self.process = ttk.Combobox(inner, style="Dark.TCombobox", state="readonly")
        self.process.grid(row=5, column=0, columnspan=2, sticky="ew", ipady=6)
        self.process.bind("<<ComboboxSelected>>", self._auto_rellenar)

        # BOTÓN AGREGAR NUEVO (Restaurado)
        add_btn = self._btn_secondary(inner, "+ Agregar nuevo", self.abrir_popup)
        add_btn.grid(row=6, column=0, columnspan=2, pady=(10, 0))

        inner.columnconfigure(0, weight=1)
        inner.columnconfigure(1, weight=1)

        # --- Botones Inferiores ---
        btn_frame = tk.Frame(panel, bg=BG_PANEL)
        btn_frame.pack(fill="x", padx=20, pady=12)

        self._btn_primary(btn_frame, "▶  GUARDAR", self.guardar).pack(side="left", ipady=6, ipadx=16)
        self._btn_secondary(btn_frame, "↺  LIMPIAR", self.limpiar).pack(side="left", padx=(10, 0), ipady=6, ipadx=16)

        # --- Status bar ---
        self.status_var = tk.StringVar(value="Listo")
        status_bar = tk.Frame(self.root, bg=BG_DARK)
        status_bar.pack(fill="x", side="bottom", padx=24, pady=(0, 8))
        tk.Label(status_bar, textvariable=self.status_var, font=FONT_LABEL, bg=BG_DARK, fg=FG_MUTED).pack(side="left")

    def _btn_primary(self, parent, text, cmd):
        return tk.Button(parent, text=text, command=cmd, bg=ACCENT, fg="#0A0A0A", relief="flat", font=FONT_BTN, cursor="hand2", bd=0)

    def _btn_secondary(self, parent, text, cmd):
        return tk.Button(parent, text=text, command=cmd, bg=BG_ENTRY, fg=FG_WHITE, relief="flat", font=FONT_BTN, cursor="hand2", bd=0)

    def guardar(self):
        datos = {
            "m": self.machine.get().strip(),
            "p": self.process.get().strip(),
            "o": self.operator.get().strip(),
            "s": self.station.get().strip(),
            "f": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        if not all([datos["m"], datos["p"], datos["o"], datos["s"]]):
            messagebox.showwarning("Campos incompletos", "Completa todo antes de guardar.")
            return
        try:
            conexion.insert_configurador(datos["m"], datos["p"], datos["o"], datos["s"], datos["f"])
            self.status_var.set(f"✔ Guardado — {datos['f']}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def limpiar(self):
        for w in (self.machine, self.operator, self.station): w.delete(0, tk.END)
        self.process.set("")
        self.status_var.set("Campos limpiados")

    def cargar(self):
        try:
            data = conexion.select_configurador()
            if data:
                self.machine.insert(0, data[1]); self.process.set(data[2])
                self.operator.insert(0, data[3]); self.station.insert(0, data[4])
                self.status_var.set("Configuración cargada")
        except: self.status_var.set("Sin datos previos")

if __name__ == "__main__":
    root = tk.Tk()
    app = ConfiguradorUI(root)
    root.mainloop()