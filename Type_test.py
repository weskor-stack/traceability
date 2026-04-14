import tkinter as tk
from tkinter import ttk
import conexion
from datetime import datetime

class TypeTestCRUD:
    def __init__(self, root):

        self.root = root
        self.root.title("Tipo de Prueba")
        self.root.geometry("600x400")
        self.root.iconbitmap("favicon.ico")
        self.data = {}
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        style.configure("Treeview", rowheight=28, font=("Segoe UI", 10))
        style.map("Treeview", background=[("selected", "#757575")])
        frame = tk.Frame(root)
        frame.pack(pady=10)

        tk.Button(frame, text="Agregar", bg="#1D8A21", fg="white",
                  command=self.abrir_agregar).grid(row=0, column=0, padx=5)

        tk.Button(frame, text="Actualizar", bg="#105FA0", fg="white",
                  command=self.abrir_actualizar).grid(row=0, column=1, padx=5)

        self.tabla = ttk.Treeview(
            root,
            columns=("Nombre", "Status"),
            show="headings"
        )
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Status", text="Status")
        self.tabla.column("Nombre", width=300)
        self.tabla.column("Status", width=100, anchor="center")
        self.tabla.pack(fill="both", expand=True, padx=10, pady=10)

        # Cargar datos al final cuando tabla y data ya existen
        self.cargar_datos()
    def status_texto(self, status_id):
        return "Enabled" if status_id == 1 else "Not enabled"
    
    # ====== CARGAR DATOS ======

    def cargar_datos(self):
        self.tabla.delete(*self.tabla.get_children())
        self.data.clear()
        registros = conexion.select_type_test()

        for registro in registros:
            item = self.tabla.insert("", "end", values=(registro[1], self.status_texto(registro[2])))
            self.data[item] = {
                
            "test_type_id": registro[0],  
            "nombre":       registro[1],
            "status":       registro[2]

        }
   
    # ===== AGREGAR =====
    def abrir_agregar(self):
        VentanaAgregar(self)
        self.root.iconbitmap("favicon.ico")

    def agregar(self, nombre):
    # Todos a 2 en BD y en UI
        for item in self.tabla.get_children():
            test_type_id = self.data[item]["test_type_id"]  # corregido
        conexion.update_type_test(test_type_id, self.data[item]["nombre"], 2)
        valores = list(self.tabla.item(item, "values"))

        valores[1] = self.status_texto(2)
        self.tabla.item(item, values=(nombre, self.status_texto(2)))
        self.data[item]["status"] = 2

    # Insertar nuevo con status 1
        test_type_id = conexion.insert_type_test(
        nombre,
        1,
        1,  # user_id, ajusta según tu lógica
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

        item = self.tabla.insert("", "end", values=(nombre, 1))
        self.data[item] = {
        "test_type_id": test_type_id,
        "nombre":       nombre,
        "status":       1
    }

    # ===== ACTUALIZAR =====
    def abrir_actualizar(self):
        selected = self.tabla.selection()
        if not selected:
            return
        selected = selected[0]
        datos = self.data[selected]
        VentanaActualizar(self, selected, datos)

    def actualizar(self, item, nombre, status):
        if status == 1:
            for i in self.tabla.get_children():
                if i != item:
                    test_type_id = self.data[i]["test_type_id"]
                    conexion.update_type_test(test_type_id, self.data[i]["nombre"], 2)  # <-- adentro del if
                    valores = list(self.tabla.item(i, "values"))
                    valores[1] = self.status_texto(2)
                    self.tabla.item(i, values=valores)
                    self.data[i]["status"] = 2

        test_type_id = self.data[item]["test_type_id"]
        conexion.update_type_test(test_type_id, nombre, status)
        self.tabla.item(item, values=(nombre, self.status_texto(status)))
        self.data[item] = {
        "test_type_id": test_type_id,
        "nombre":       nombre,
        "status":       status
    }

# ===== VENTANA AGREGAR =====
class VentanaAgregar:
    def __init__(self, principal):
        self.principal = principal
        self.ventana = tk.Toplevel()
        self.ventana.title("Agregar")
        self.ventana.geometry("250x150")
        self.ventana.iconbitmap("favicon.ico")
        self.nombre = tk.StringVar()

        tk.Label(self.ventana, text="Nombre").pack(pady=5)
        tk.Entry(self.ventana, textvariable=self.nombre).pack()
        tk.Button(self.ventana, text="Guardar",
                  bg="#1D8A21", fg="white",
                  command=self.guardar).pack(pady=10)

    def guardar(self):
        if self.nombre.get():
            self.principal.agregar(self.nombre.get())
        self.ventana.destroy()

# ===== VENTANA ACTUALIZAR =====
class VentanaActualizar:
    def __init__(self, principal, item, datos):
        self.principal = principal
        self.item = item
        self.ventana = tk.Toplevel()
        self.ventana.title("Actualizar")
        self.ventana.geometry("250x200")
        self.ventana.iconbitmap("favicon.ico")
        self.nombre = tk.StringVar(value=datos["nombre"])
        self.status = tk.IntVar(value=datos["status"])

        tk.Label(self.ventana, text="Nombre").pack()
        tk.Entry(self.ventana, textvariable=self.nombre).pack()
        tk.Label(self.ventana, text="Status").pack()
        tk.Radiobutton(self.ventana, text="Enabled", variable=self.status, value=1).pack()
        tk.Radiobutton(self.ventana, text="Not Enabled", variable=self.status, value=2).pack()  # 0 -> 2
        tk.Button(self.ventana, text="Guardar",
                  bg="#4CAF50", fg="white",
                  command=self.guardar).pack(pady=10)

    def guardar(self):
        self.principal.actualizar(
            self.item,
            self.nombre.get(),
            self.status.get()
        )
        self.ventana.destroy()

# ===== MAIN =====
root = tk.Tk()
app = TypeTestCRUD(root)
root.mainloop()