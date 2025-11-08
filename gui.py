import tkinter as tk
from tkinter import ttk, messagebox
from estudiantes import (insertar_estudiante, actualizar_estudiante, 
                        listar_estudiantes, buscar_estudiantes, 
                        obtener_estudiante, eliminar_estudiante)
from pagos import registrar_pago

class ControlPagosGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Control de Pagos - Universidad Fidélitas")
        self.root.geometry("900x600")
        
        
        self.estudiante_seleccionado = None
        
        
        self.tabControl = ttk.Notebook(root)
        
        self.tab_matricula = ttk.Frame(self.tabControl)
        self.tab_busqueda = ttk.Frame(self.tabControl)
        
        self.tabControl.add(self.tab_matricula, text=" Matrícula")
        self.tabControl.add(self.tab_busqueda, text=" Búsqueda y Gestión")
        self.tabControl.pack(expand=1, fill="both", padx=10, pady=10)
        
        
        self.configurar_tab_matricula()
        self.configurar_tab_busqueda()
    
    
    
    def configurar_tab_matricula(self):
        frame = ttk.LabelFrame(self.tab_matricula, text="Registrar Nuevo Estudiante", padding=20)
        frame.pack(padx=20, pady=20, fill="both", expand=True)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        ttk.Label(frame, text="Nombre:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.ent_nombre = ttk.Entry(frame, width=30)
        self.ent_nombre.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(frame, text="Apellido:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.ent_apellido = ttk.Entry(frame, width=30)
        self.ent_apellido.grid(row=1, column=1, padx=10, pady=10)
        
        ttk.Label(frame, text="Identificación:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.ent_identificacion = ttk.Entry(frame, width=30)
        self.ent_identificacion.grid(row=2, column=1, padx=10, pady=10)
        
        ttk.Label(frame, text="Correo:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.ent_correo = ttk.Entry(frame, width=30)
        self.ent_correo.grid(row=3, column=1, padx=10, pady=10)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text=" Realizar Matrícula", 
                  command=self.guardar_estudiante).pack(side="left", padx=5)
        ttk.Button(btn_frame, text=" Limpiar Datos", 
                  command=self.limpiar_matricula).pack(side="left", padx=5)
    
    
    
    def configurar_tab_busqueda(self):
        
        frame_busqueda = ttk.LabelFrame(self.tab_busqueda, text="Buscar Estudiante", padding=15)
        frame_busqueda.pack(padx=20, pady=10, fill="x")
        
       
        ttk.Label(frame_busqueda, text="Buscar por:").grid(row=0, column=0, padx=5, pady=5)
        
        self.tipo_busqueda = tk.StringVar(value="nombre")
        ttk.Radiobutton(frame_busqueda, text="Nombre/Apellido", 
                       variable=self.tipo_busqueda, value="nombre").grid(row=0, column=1, padx=5)
        ttk.Radiobutton(frame_busqueda, text="Identificación", 
                       variable=self.tipo_busqueda, value="identificacion").grid(row=0, column=2, padx=5)
        
      
        ttk.Label(frame_busqueda, text="Término:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.ent_busqueda = ttk.Entry(frame_busqueda, width=30)
        self.ent_busqueda.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
        self.ent_busqueda.bind('<KeyRelease>', lambda e: self.buscar_estudiante())
        
        ttk.Button(frame_busqueda, text=" Buscar", 
                  command=self.buscar_estudiante).grid(row=1, column=3, padx=5, pady=5)
        ttk.Button(frame_busqueda, text="Ver Todos", 
                  command=self.cargar_todos_estudiantes).grid(row=1, column=4, padx=5, pady=5)
        
        
        frame_resultados = ttk.LabelFrame(self.tab_busqueda, text="Resultados", padding=10)
        frame_resultados.pack(padx=20, pady=10, fill="both", expand=True)
        
       
        columns = ("ID", "Nombre", "Apellido", "Identificación", "Correo")
        self.tree_estudiantes = ttk.Treeview(frame_resultados, columns=columns, show="headings", height=8)
        
        self.tree_estudiantes.heading("ID", text="ID")
        self.tree_estudiantes.heading("Nombre", text="Nombre")
        self.tree_estudiantes.heading("Apellido", text="Apellido")
        self.tree_estudiantes.heading("Identificación", text="Identificación")
        self.tree_estudiantes.heading("Correo", text="Correo")
        
        self.tree_estudiantes.column("ID", width=50)
        self.tree_estudiantes.column("Nombre", width=150)
        self.tree_estudiantes.column("Apellido", width=150)
        self.tree_estudiantes.column("Identificación", width=120)
        self.tree_estudiantes.column("Correo", width=200)
        
        
        
        scrollbar = ttk.Scrollbar(frame_resultados, orient="vertical", command=self.tree_estudiantes.yview)
        self.tree_estudiantes.configure(yscrollcommand=scrollbar.set)
        
        self.tree_estudiantes.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        
        self.tree_estudiantes.bind('<<TreeviewSelect>>', self.seleccionar_estudiante)
        
        
        frame_acciones = ttk.LabelFrame(self.tab_busqueda, text="Acciones sobre Estudiante Seleccionado", padding=15)
        frame_acciones.pack(padx=20, pady=10, fill="x")
        
   
        self.lbl_seleccionado = ttk.Label(frame_acciones, text="No hay estudiante seleccionado", 
                                         foreground="gray", font=("Arial", 10, "italic"))
        self.lbl_seleccionado.pack(pady=5)
        
       
        btn_frame = ttk.Frame(frame_acciones)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Registrar Pago", 
                  command=self.abrir_ventana_pago).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Actualizar Datos", 
                  command=self.abrir_ventana_actualizar).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Eliminar Estudiante", 
                  command=self.eliminar_estudiante_seleccionado).pack(side="left", padx=5)
        
        
        self.cargar_todos_estudiantes()
    
    
   
    def guardar_estudiante(self):
        nombre = self.ent_nombre.get().strip()
        apellido = self.ent_apellido.get().strip()
        identificacion = self.ent_identificacion.get().strip()
        correo = self.ent_correo.get().strip()
        
        if not all([nombre, apellido, identificacion, correo]):
            messagebox.showwarning("Campos vacíos", "Por favor complete todos los campos")
            return
        
        if insertar_estudiante(nombre, apellido, identificacion, correo):
            messagebox.showinfo("Éxito", " Estudiante matriculado correctamente")
            self.limpiar_matricula()
            self.cargar_todos_estudiantes()  
        else:
            messagebox.showerror("Error", "No se pudo matricular el estudiante")
    
    def limpiar_matricula(self):
        self.ent_nombre.delete(0, tk.END)
        self.ent_apellido.delete(0, tk.END)
        self.ent_identificacion.delete(0, tk.END)
        self.ent_correo.delete(0, tk.END)

    def buscar_estudiante(self):
        termino = self.ent_busqueda.get().strip()
        
        if not termino:
            self.cargar_todos_estudiantes()
            return
        
        estudiantes = buscar_estudiantes(termino)
        self.actualizar_tabla(estudiantes)
    
    def cargar_todos_estudiantes(self):
        estudiantes = listar_estudiantes()
        self.actualizar_tabla(estudiantes)
    
    def actualizar_tabla(self, estudiantes):
        
        for item in self.tree_estudiantes.get_children():
            self.tree_estudiantes.delete(item)
        
        
        for est in estudiantes:
            self.tree_estudiantes.insert("", "end", values=(
                est['id'],
                est['nombre'],
                est['apellido'],
                est['identificacion'],
                est['correo']
            ))
    
    def seleccionar_estudiante(self, event):
        seleccion = self.tree_estudiantes.selection()
        if seleccion:
            item = self.tree_estudiantes.item(seleccion[0])
            valores = item['values']
            
            self.estudiante_seleccionado = {
                'id': valores[0],
                'nombre': valores[1],
                'apellido': valores[2],
                'identificacion': valores[3],
                'correo': valores[4]
            }
            
            self.lbl_seleccionado.config(
                text=f"Seleccionado: {valores[1]} {valores[2]} (ID: {valores[0]})",
                foreground="blue"
            )
        else:
            self.estudiante_seleccionado = None
            self.lbl_seleccionado.config(
                text="No hay estudiante seleccionado",
                foreground="gray"
            )
    
    
    
    def abrir_ventana_pago(self):
        if not self.estudiante_seleccionado:
            messagebox.showwarning("Selección requerida", "Debe seleccionar un estudiante primero")
            return
        
        ventana = tk.Toplevel(self.root)
        ventana.title("Registrar Pago")
        ventana.geometry("400x300")
        ventana.resizable(False, False)
        ventana.grab_set()
        
        frame = ttk.Frame(ventana, padding=20)
        frame.pack(fill="both", expand=True)
        
       
        ttk.Label(frame, text=f"Estudiante: {self.estudiante_seleccionado['nombre']} {self.estudiante_seleccionado['apellido']}", 
                 font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        ttk.Label(frame, text=f"ID: {self.estudiante_seleccionado['id']}", 
                 foreground="gray").grid(row=1, column=0, columnspan=2, pady=5)
        
        ttk.Separator(frame, orient="horizontal").grid(row=2, column=0, columnspan=2, sticky="ew", pady=15)
        
        
        ttk.Label(frame, text="Monto:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        ent_monto = ttk.Entry(frame, width=20)
        ent_monto.grid(row=3, column=1, padx=10, pady=10)
        
        ttk.Label(frame, text="Método de pago:").grid(row=4, column=0, padx=10, pady=10, sticky="e")
        cmb_metodo = ttk.Combobox(frame, values=["Tarjeta", "Transferencia", "Efectivo"], width=18, state="readonly")
        cmb_metodo.grid(row=4, column=1, padx=10, pady=10)
        cmb_metodo.current(0)
        
        def realizar_pago():
            try:
                monto = float(ent_monto.get())
                metodo = cmb_metodo.get()
                
                if monto <= 0:
                    messagebox.showwarning("Monto inválido", "El monto debe ser mayor a 0")
                    return
                
                registrar_pago(self.estudiante_seleccionado['id'], monto, metodo)
                messagebox.showinfo("Éxito", f" Pago de ${monto:.2f} registrado correctamente")
                ventana.destroy()
                
            except ValueError:
                messagebox.showerror("Error", "Ingrese un monto válido")
            except Exception as e:
                messagebox.showerror("Error", f"Error al registrar pago: {str(e)}")
        
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text=" Registrar Pago", command=realizar_pago).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=ventana.destroy).pack(side="left", padx=5)
    
    
    def abrir_ventana_actualizar(self):
        if not self.estudiante_seleccionado:
            messagebox.showwarning("Selección requerida", "Debe seleccionar un estudiante primero")
            return
        
        ventana = tk.Toplevel(self.root)
        ventana.title("Actualizar Datos del Estudiante")
        ventana.geometry("450x400")
        ventana.resizable(False, False)
        ventana.grab_set()
        
        frame = ttk.Frame(ventana, padding=20)
        frame.pack(fill="both", expand=True)
        
        ttk.Label(frame, text="Actualizar Información", font=("Arial", 12, "bold")).pack(pady=10)
        
        form_frame = ttk.Frame(frame)
        form_frame.pack(pady=10)
        
       
        ttk.Label(form_frame, text="Nombre:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        ent_nombre = ttk.Entry(form_frame, width=30)
        ent_nombre.insert(0, self.estudiante_seleccionado['nombre'])
        ent_nombre.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(form_frame, text="Apellido:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        ent_apellido = ttk.Entry(form_frame, width=30)
        ent_apellido.insert(0, self.estudiante_seleccionado['apellido'])
        ent_apellido.grid(row=1, column=1, padx=10, pady=10)
        
        ttk.Label(form_frame, text="Identificación:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        ent_identificacion = ttk.Entry(form_frame, width=30)
        ent_identificacion.insert(0, self.estudiante_seleccionado['identificacion'])
        ent_identificacion.grid(row=2, column=1, padx=10, pady=10)
        
        ttk.Label(form_frame, text="Correo:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        ent_correo = ttk.Entry(form_frame, width=30)
        ent_correo.insert(0, self.estudiante_seleccionado['correo'])
        ent_correo.grid(row=3, column=1, padx=10, pady=10)
        
        def guardar_cambios():
            try:
                nombre = ent_nombre.get().strip()
                apellido = ent_apellido.get().strip()
                identificacion = ent_identificacion.get().strip()
                correo = ent_correo.get().strip()
                
                if not all([nombre, apellido, identificacion, correo]):
                    messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios")
                    return
                
                if actualizar_estudiante(
                    self.estudiante_seleccionado['id'],
                    nombre, apellido, identificacion, correo
                ):
                    messagebox.showinfo("Éxito", " Datos actualizados correctamente")
                    ventana.destroy()
                    self.cargar_todos_estudiantes()
                else:
                    messagebox.showerror("Error", "No se pudo actualizar el estudiante")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error al actualizar: {str(e)}")
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text=" Guardar Cambios", command=guardar_cambios).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=ventana.destroy).pack(side="left", padx=5)
    
    
    def eliminar_estudiante_seleccionado(self):
        if not self.estudiante_seleccionado:
            messagebox.showwarning("Selección requerida", "Debe seleccionar un estudiante primero")
            return
        
        respuesta = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Está seguro que desea eliminar a:\n\n{self.estudiante_seleccionado['nombre']} {self.estudiante_seleccionado['apellido']}\nID: {self.estudiante_seleccionado['id']}\n\nEsta acción no se puede deshacer."
        )
        
        if respuesta:
            if eliminar_estudiante(self.estudiante_seleccionado['id']):
                messagebox.showinfo("Éxito", " Estudiante eliminado correctamente")
                self.estudiante_seleccionado = None
                self.cargar_todos_estudiantes()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el estudiante")


if __name__ == "__main__":
    root = tk.Tk()
    app = ControlPagosGUI(root)
    root.mainloop()