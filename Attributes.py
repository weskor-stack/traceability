import tkinter as tk
from tkinter import ttk
import conexion
import importlib
importlib.reload(conexion)
from datetime import datetime

class FormularioPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Attributes")
        self.root.geometry("900x500")
        self.root.iconbitmap("favicon.ico")
        self.data = {}

        # ====== ESTILO TABLA ======
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), relief="flat")
        style.configure("Treeview", rowheight=30, font=("Segoe UI", 10), borderwidth=1, relief="solid")
        style.map("Treeview", background=[("selected", "#757575")])

        # ====== BOTONES ======
        frame_botones = tk.Frame(root)
        frame_botones.pack(pady=10)

        tk.Button(frame_botones, text="Agregar", font=("Segoe UI Emoji", 10),
                  bg="#1D8A21", fg="white", width=12,
                  command=self.abrir_agregar).grid(row=0, column=0, padx=5)

        tk.Button(frame_botones, text="Actualizar", font=("Segoe UI Emoji", 10),
                  bg="#105FA0", fg="white", width=12,
                  command=self.abrir_actualizar).grid(row=0, column=1, padx=5)

        tk.Button(frame_botones, text="Eliminar", font=("Segoe UI Emoji", 10),
                  bg="#f44336", fg="white", width=12,
                  command=self.eliminar).grid(row=0, column=2, padx=5)

        # ====== TABLA ======
        self.tabla = ttk.Treeview(
            root,
            columns=("Nombre", "Lower", "Upper", "Value"),
            show="headings",
            selectmode="browse"
        )

        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Lower", text="Lower-limit")
        self.tabla.heading("Upper", text="Upper-limit")
        self.tabla.heading("Value", text="Value_expected")
        self.tabla.column("Nombre", width=180)
        self.tabla.column("Lower", width=120, anchor="center")
        self.tabla.column("Upper", width=120, anchor="center")
        self.tabla.column("Value", width=150, anchor="center")
        self.tabla.pack(fill="both", expand=True, padx=10, pady=10)

        self.tabla.tag_configure("par", background="#f9f9f9")
        self.tabla.tag_configure("impar", background="#ffffff")

        self.cargar_datos()

    # ====== CARGAR DATOS ======
    def cargar_datos(self):
        self.tabla.delete(*self.tabla.get_children())
        self.data.clear()

        registros = conexion.select_attributes()

        for i, registro in enumerate(registros):
            tag = "par" if i % 2 == 0 else "impar"
            item = self.tabla.insert("", "end", values=(
                registro[1],  # name
                registro[4],  # lower_limit
                registro[3],  # upper_limit
                registro[5],  # value_expected
            ), tags=(tag,))

            self.data[item] = {
                "attribute_id":        registro[0],
                "name":                registro[1],
                "unit":                registro[2],
                "upper_limit":         registro[3],
                "lower_limit":         registro[4],
                "value_expected":      registro[5],
                "create_registration": registro[7],
            }

    # ====== FUNCIONES ======
    def abrir_agregar(self):
        VentanaFormulario(self, "Agregar")
        self.root.iconbitmap("favicon.ico")

    def abrir_actualizar(self):
        selected = self.tabla.selection()
        if not selected:
            return
        selected = selected[0]
        datos = self.data[selected]
        VentanaFormulario(self, "Actualizar", selected, datos)

    def agregar_datos(self, datos):
        attribute_id = conexion.insert_attribute(
            datos["name"],
            datos["unit"],
            datos["upper_limit"],
            datos["lower_limit"],
            datos["value_expected"],
            datos["create_registration"]
        )

        datos["attribute_id"] = attribute_id

        count = len(self.tabla.get_children())
        tag = "par" if count % 2 == 0 else "impar"

        item = self.tabla.insert("", "end", values=(
            datos["name"],
            datos["lower_limit"],
            datos["upper_limit"],
            datos["value_expected"],
        ), tags=(tag,))

        self.data[item] = datos

    def actualizar_datos(self, item, datos):
        attribute_id = self.data[item]["attribute_id"]

        conexion.update_attribute(
            attribute_id,
            datos["name"],
            datos["unit"],
            datos["upper_limit"],
            datos["lower_limit"],
            datos["value_expected"],
        )

        self.tabla.item(item, values=(
            datos["name"],
            datos["lower_limit"],
            datos["upper_limit"],
            datos["value_expected"],
        ))

        datos["attribute_id"] = attribute_id
        self.data[item] = datos

    def eliminar(self):
        selected = self.tabla.selection()
        if not selected:
            print("No hay fila seleccionada")
            return

        selected = selected[0]

        if selected not in self.data:
            print("No existe en self.data")
            return

        attribute_id = self.data[selected].get("attribute_id")
        if not attribute_id:
            print("No se encontró el attribute_id")
            return

        conexion.delete_attribute(attribute_id)
        self.tabla.delete(selected)
        del self.data[selected]


class VentanaFormulario:
    def __init__(self, principal, modo, item=None, datos=None):
        self.principal = principal
        self.modo = modo
        self.item = item
        self.ventana = tk.Toplevel()
        self.ventana.title(f" {modo} Registro")
        self.ventana.geometry("350x320")
        self.ventana.iconbitmap("favicon.ico")

        # Variables
        self.nombre = tk.StringVar()
        self.unit = tk.StringVar()
        self.lower = tk.StringVar()
        self.upper = tk.StringVar()
        self.value = tk.StringVar()

        # Cargar datos si es actualizar
        if datos:
            self.nombre.set(datos["name"])
            self.unit.set(datos["unit"])
            self.lower.set(datos["lower_limit"])
            self.upper.set(datos["upper_limit"])
            self.value.set(datos["value_expected"])

        # Campos
        tk.Label(self.ventana, text="Nombre").pack(pady=2)
        tk.Entry(self.ventana, textvariable=self.nombre).pack()
        tk.Label(self.ventana, text="Unit").pack(pady=2)
        tk.Entry(self.ventana, textvariable=self.unit).pack()
        tk.Label(self.ventana, text="Lower-limit").pack(pady=2)
        tk.Entry(self.ventana, textvariable=self.lower).pack()
        tk.Label(self.ventana, text="Upper-limit").pack(pady=2)
        tk.Entry(self.ventana, textvariable=self.upper).pack()
        tk.Label(self.ventana, text="Value_expected").pack(pady=2)
        tk.Entry(self.ventana, textvariable=self.value).pack()

        tk.Button(self.ventana, text=" Guardar", font=("Segoe UI Emoji", 10),
                  bg="#228F26", fg="white", width=15,
                  command=self.guardar).pack(pady=15)

    def guardar(self):
        datos = {
            "name":                self.nombre.get(),
            "unit":                self.unit.get(),
            "upper_limit":         self.upper.get(),
            "lower_limit":         self.lower.get(),
            "value_expected":      self.value.get(),
            "create_registration": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        if self.modo == "Agregar":
            self.principal.agregar_datos(datos)
        else:
            self.principal.actualizar_datos(self.item, datos)

        self.ventana.destroy()


# ===== MAIN =====
if __name__ == "__main__":
    root = tk.Tk()
    app = FormularioPrincipal(root)
    root.mainloop()