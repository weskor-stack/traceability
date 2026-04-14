import tkinter as tk
from tkinter import ttk
import conexion

class FormularioProgramas:
    def __init__(self, root):
        self.root = root
        self.data = {}
        self.root.iconbitmap("favicon.ico")
        self.contador_id = 1
        self.root.title(" Gestión de Programas")
        # self.root.iconbitmap("favicon.ico") # Descomentar si tienes el archivo

        # ===== ESTILO =====
        style = ttk.Style()
        style.theme_use("default")

        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        style.configure("Treeview", rowheight=28, font=("Segoe UI", 10))
        style.map("Treeview", background=[("selected", "#757575")])

        # ===== BOTONES =====
        frame = tk.Frame(root)
        frame.pack(pady=10)

        tk.Button(frame, text=" Agregar", bg="#1D8A21", fg="white",
                  command=self.abrir_agregar).grid(row=0, column=0, padx=5)

        tk.Button(frame, text=" Actualizar", bg="#105FA0", fg="white",
                  command=self.abrir_actualizar).grid(row=0, column=1, padx=5)

        tk.Button(frame, text=" Eliminar", bg="#f44336", fg="white",
                  command=self.eliminar).grid(row=0, column=2, padx=5)

        # ===== TABLA =====
        self.tabla = ttk.Treeview(
            root,
            columns=("Nombre", "Descripcion"),
            show="headings"
        )

        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Descripcion", text="Descripción")
        self.tabla.pack(fill="both", expand=True, padx=10, pady=10)

        # Cargar datos
        self.cargar_datos()

        self.root.update_idletasks()
        self.root.geometry("")

    def cargar_datos(self):
        self.tabla.delete(*self.tabla.get_children())
        self.data.clear()

        registros = conexion.select_programs()
        print("Filas obtenidas:", registros)

        for registro in registros:
            item = self.tabla.insert("", "end", values=(registro[1], registro[2]))
            self.data[item] = {
            "Program_id": registro[0],
            "Name": registro[1],
            "Description": registro[2]
        }

            self.ajustar_columnas()
    def ajustar_columnas(self):
        for col in self.tabla["columns"]:
            max_len = len(col)
            for item in self.tabla.get_children():
                valor = str(self.tabla.item(item, "values")[self.tabla["columns"].index(col)])
                if len(valor) > max_len:
                    max_len = len(valor)
            ancho = (max_len + 2) * 8
            self.tabla.column(col, width=ancho)

    # ===== FUNCIONES =====
    def abrir_agregar(self):

        VentanaPrograma(self, "Agregar")
        self.root.update_idletasks()
        self.root.iconbitmap("favicon.ico")

    def abrir_actualizar(self):
        self.root.iconbitmap("favicon.ico")

        selected = self.tabla.focus()
        if not selected:
            return
        datos = self.data[selected]
        VentanaPrograma(self, "Actualizar", selected, datos)

    def agregar(self, datos):
        self.root.iconbitmap("favicon.ico")
        program_id = conexion.insert_program(
        datos["Name"],
        datos["Description"],
        datos["Create_registration"]
    )

        if program_id:
            datos["Program_id"] = program_id
            item = self.tabla.insert("", "end", values=(datos["Name"], datos["Description"]))
            self.data[item] = datos
            self.ajustar_columnas()
            print(f"Registro agregado con ID: {program_id}")
        else:
            print("Error: No se pudo obtener el ID de la base de datos")
    def actualizar(self, item, datos):
        program_id = self.data[item]["Program_id"]  
        conexion.update_program(program_id, datos["Name"], datos["Description"])
        self.tabla.item(item, values=(datos["Name"], datos["Description"]))
        datos["Program_id"] = program_id  # Reinyectarlo en el diccionario nuevo
        self.data[item] = datos
        self.ajustar_columnas()

    # --- AQUÍ ESTÁ EL MÉTODO ELIMINAR CORREGIDO ---
    def eliminar(self):
        selected = self.tabla.selection() 
        
        if not selected:
            print("No hay fila seleccionada")
            return # El return debe estar DENTRO del if

        item_id = selected[0] 
        
        if item_id not in self.data:
            print("No existe en self.data")
            return # El return debe estar DENTRO del if

        program_id = self.data[item_id].get("Program_id")

        if not program_id:
            print("No se encontró el Program_id")
            return

        try:
            conexion.delete_program(program_id)
            self.tabla.delete(item_id)
            del self.data[item_id]
            print(f"Programa {program_id} eliminado con éxito")
        except Exception as e:
            print(f"Error al eliminar: {e}")


class VentanaPrograma:
    def __init__(self, principal, modo, item=None, datos=None):
        self.principal = principal
        self.modo = modo
        self.item = item

        self.ventana = tk.Toplevel()
        self.ventana.title(f" {modo} Programa")

        self.name = tk.StringVar()
        if datos:
            self.name.set(datos["Name"])

        tk.Label(self.ventana, text="Nombre").pack(pady=5)
        tk.Entry(self.ventana, textvariable=self.name).pack()
        tk.Label(self.ventana, text="Descripción").pack(pady=5)

        self.desc_text = tk.Text(self.ventana, height=4, width=30)
        self.desc_text.pack()

        if datos:
            self.desc_text.insert("1.0", datos["Description"])

        tk.Button(self.ventana, text=" Guardar",
                  bg="#4CAF50", fg="white",
                  command=self.guardar).pack(pady=10)

        self.ventana.update_idletasks()
        self.ventana.geometry("400x300")

    def guardar(self):
        descripcion = self.desc_text.get("1.0", "end").strip()
        datos = {
        "Name": self.name.get(),
        "Description": descripcion,
        "Create_registration": "2026-01-01 00:00:00"
    }

        if self.modo == "Agregar":
            self.principal.agregar(datos)
        elif self.modo == "Actualizar":
            self.principal.actualizar(self.item, datos)

        self.ventana.destroy()

# ===== MAIN =====
if __name__ == "__main__":
    root = tk.Tk()
    app = FormularioProgramas(root)
    root.mainloop()