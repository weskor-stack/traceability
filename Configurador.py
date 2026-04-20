import os
import glob 
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import conexion

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
    style.configure("Dark.TCombobox", fieldbackground=BG_ENTRY, background=BG_PANEL, 
                    foreground=FG_WHITE, selectbackground=ACCENT_DIM, selectforeground=FG_WHITE,
                    bordercolor=BORDER, arrowcolor=ACCENT, relief="flat", padding=6)
    style.map("Dark.TCombobox", fieldbackground=[("readonly", BG_ENTRY)], 
              foreground=[("readonly", FG_WHITE)], bordercolor=[("focus", ACCENT), ("!focus", BORDER)])

class ConfiguradorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Configurador")
        self.root.geometry("560x440") 
        self.root.configure(bg=BG_DARK)
        apply_dark_theme()
        self._build_ui()
        self.station["values"] = ["Station 10", "Station 20", "Station 30"]
        self.cargar()

    def _build_ui(self):
        try: self.root.iconbitmap("favicon.ico")
        except: pass
        
        # Header
        header = tk.Frame(self.root, bg=BG_DARK)
        header.pack(fill="x", padx=24, pady=(20, 0))
        tk.Label(header, text="⚙ CONFIGURADOR", font=FONT_HEAD, bg=BG_DARK, fg=FG_WHITE).pack(side="left")
        tk.Frame(self.root, bg=ACCENT, height=2).pack(fill="x", padx=24, pady=(8, 0))

        # Panel Principal 
        panel = tk.Frame(self.root, bg=BG_PANEL, highlightthickness=1, highlightbackground=BORDER)
        panel.pack(fill="x", padx=24, pady=16, expand=False)
        inner = tk.Frame(panel, bg=BG_PANEL)
        inner.pack(fill="x", padx=20, pady=16, expand=False)

        # STATION
        tk.Label(inner, text="STATION", bg=BG_PANEL, font=FONT_LABEL).grid(row=0, column=0, sticky="w")
        self.station = ttk.Combobox(inner, style="Dark.TCombobox", state="readonly")
        self.station.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        self.station.bind("<<ComboboxSelected>>", self._on_station_change)

        # SHOP ORDER
        self.lbl_shop = tk.Label(inner, text="SHOP ORDER", bg=BG_PANEL, font=FONT_LABEL)
        self.shop_order = tk.Entry(inner, bg=BG_ENTRY, relief="flat", font=FONT_MONO, highlightthickness=1, highlightbackground=BORDER)
        
        # PRODUCTS
        self.lbl_products = tk.Label(inner, text="PRODUCTS", bg=BG_PANEL, font=FONT_LABEL)
        self.products = tk.Entry(inner, bg=BG_ENTRY, relief="flat", font=FONT_MONO, highlightthickness=1, highlightbackground=BORDER)

        # MACHINE / OPERATOR
        tk.Label(inner, text="MACHINE NAME", bg=BG_PANEL, font=FONT_LABEL).grid(row=4, column=0, sticky="w")
        tk.Label(inner, text="ID OPERATOR", bg=BG_PANEL, font=FONT_LABEL).grid(row=4, column=1, sticky="w", padx=(16,0))
        
        self.machine = tk.Entry(inner, bg=BG_ENTRY, relief="flat", font=FONT_MONO, highlightthickness=1, highlightbackground=BORDER)
        self.machine.grid(row=5, column=0, sticky="ew", ipady=4, pady=(0, 10))
        
        self.operator = tk.Entry(inner, bg=BG_ENTRY, relief="flat", font=FONT_MONO, highlightthickness=1, highlightbackground=BORDER)
        self.operator.grid(row=5, column=1, sticky="ew", padx=(16, 0), ipady=4, pady=(0, 10))

        # PROCESS NAME
        tk.Label(inner, text="PROCESS NAME", bg=BG_PANEL, font=FONT_LABEL).grid(row=6, column=0, sticky="w")
        self.process = tk.Entry(inner, bg=BG_ENTRY, relief="flat", font=FONT_MONO, highlightthickness=1, highlightbackground=BORDER)
        self.process.grid(row=7, column=0, columnspan=2, sticky="ew", ipady=4)

        inner.columnconfigure(0, weight=1); inner.columnconfigure(1, weight=1)

        # Botones
        btn_frame = tk.Frame(panel, bg=BG_PANEL)
        btn_frame.pack(fill="x", padx=20, pady=(0, 12)) # Ajustado pady superior a 0
        tk.Button(btn_frame, text="▶ GUARDAR", command=self.guardar, bg=ACCENT, font=FONT_BTN, relief="flat", cursor="hand2").pack(side="left", ipadx=15)
        tk.Button(btn_frame, text="↺ LIMPIAR", command=self.limpiar, bg=BG_ENTRY, font=FONT_BTN, relief="flat", cursor="hand2").pack(side="left", padx=(10, 0), ipadx=15)

        # Barra de estado
        self.status_var = tk.StringVar(value="Listo")
        status_bar = tk.Label(self.root, textvariable=self.status_var, font=FONT_LABEL, bg=BG_DARK, fg=FG_MUTED)
        status_bar.pack(side="bottom", anchor="w", padx=24, pady=8)

    def _on_station_change(self, event):
        seleccion = self.station.get()    
        self.lbl_shop.grid_forget()
        self.shop_order.grid_forget()
        self.lbl_products.grid_forget()
        self.products.grid_forget()

        if seleccion == "Station 10":
            self.lbl_shop.grid(row=2, column=0, sticky="w")
            self.shop_order.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 10), ipady=4)
            self._rellenar_ultimo_shop_order()
        
        elif seleccion in ["Station 20", "Station 30"]:
            self.lbl_products.grid(row=2, column=0, sticky="w")
            self.products.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 10), ipady=4)

        self._auto_rellenar()

    def _rellenar_ultimo_shop_order(self):
        self.shop_order.delete(0, tk.END)
        archivos = glob.glob("shop_order_*_enabled.txt")
        if archivos:
            ultimo = max(archivos, key=os.path.getmtime)
            nombre = ultimo.replace("shop_order_", "").replace("_enabled.txt", "")
            self.shop_order.insert(0, nombre)

    def guardar(self):
        m, p, o, s = self.machine.get().strip(), self.process.get().strip(), self.operator.get().strip(), self.station.get()
        shop = self.shop_order.get().strip()

        if not all([m, p, o, s]):
            messagebox.showwarning("Error", "Faltan campos obligatorios.")
            return

        if s == "Station 10":
            if not shop:
                messagebox.showwarning("Error", "Shop Order es requerido para Estación 10.")
                return
            try:
                viejos = glob.glob("shop_order_*_enabled.txt")
                for v in viejos: os.remove(v)
                filename = f"shop_order_{shop}_enabled.txt"
                with open(filename, "w") as f:
                    f.write(f"Registro: {datetime.now()}")
            except Exception as e:
                messagebox.showerror("Error archivo", str(e)); return

        try:
            conexion.insert_configurador(m, p, o, s, "")
            messagebox.showinfo("Éxito", "Configuración guardada correctamente.")
            self.root.destroy()
        except Exception as e:
            messagebox.showerror("Error DB", str(e))

    def limpiar(self):
        for w in (self.machine, self.operator, self.process, self.shop_order, self.products):
            w.delete(0, tk.END)
        self.station.set("")
        self.lbl_shop.grid_forget()
        self.shop_order.grid_forget()
        self.lbl_products.grid_forget()
        self.products.grid_forget()
        self.status_var.set("Campos limpiados")

    def _auto_rellenar(self):
        try:
            datos = conexion.obtener_datos_fila_unica()
            if datos:
                self.machine.delete(0, tk.END); self.machine.insert(0, str(datos[0]))
                self.process.delete(0, tk.END); self.process.insert(0, str(datos[1]))
                self.operator.delete(0, tk.END); self.operator.insert(0, str(datos[2]))
        except: pass

    def cargar(self):
        try:
            data = conexion.obtener_datos_fila_unica()
            if data:
                self.station.set(data[3])
                self._on_station_change(None)
        except: pass

if __name__ == "__main__":
    root = tk.Tk()
    app = ConfiguradorUI(root)
    root.mainloop()