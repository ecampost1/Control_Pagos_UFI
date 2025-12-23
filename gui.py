import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from estudiantes import (insertar_estudiante, actualizar_estudiante, 
                        listar_estudiantes, buscar_estudiantes, 
                        obtener_estudiante, eliminar_estudiante)
from pagos import (registrar_matricula, registrar_pago, 
                  listar_matriculas_estudiante, listar_pagos_estudiante,
                  obtener_estado_financiero, listar_alertas_morosidad,
                  generar_alertas, generar_alertas_prueba, resolver_alerta, 
                  listar_estados_financieros)

class ControlPagosGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Control de Pagos - Universidad Fidélitas")
        self.root.geometry("1100x700")
        
        # Variables para almacenar el estudiante seleccionado
        self.estudiante_seleccionado = None
        
        # Crear el notebook con las pestañas
        self.tabControl = ttk.Notebook(root)
        
        self.tab_matricula = ttk.Frame(self.tabControl)
        self.tab_busqueda = ttk.Frame(self.tabControl)
        self.tab_pagos = ttk.Frame(self.tabControl)
        self.tab_estados = ttk.Frame(self.tabControl)
        self.tab_alertas = ttk.Frame(self.tabControl)
        
        self.tabControl.add(self.tab_matricula, text=" Matrícula Estudiantes")
        self.tabControl.add(self.tab_busqueda, text=" Gestión Estudiantes")
        self.tabControl.add(self.tab_pagos, text=" Pagos y Matrículas")
        self.tabControl.add(self.tab_estados, text=" Estados Financieros")
        self.tabControl.add(self.tab_alertas, text=" Alertas de Morosidad")
        self.tabControl.pack(expand=1, fill="both", padx=10, pady=10)
        
        # Configurar las pestañas
        self.configurar_tab_matricula()
        self.configurar_tab_busqueda()
        self.configurar_tab_pagos()
        self.configurar_tab_estados()
        self.configurar_tab_alertas()
    
    
    # ==================== TAB MATRÍCULA ====================
    def configurar_tab_matricula(self):
        frame = ttk.LabelFrame(self.tab_matricula, text="Registrar Nuevo Estudiante", padding=20)
        frame.pack(padx=20, pady=20, fill="both", expand=True)
        
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
        
        ttk.Button(btn_frame, text=" Registrar Estudiante", 
                  command=self.guardar_estudiante).pack(side="left", padx=5)
        ttk.Button(btn_frame, text=" Limpiar", 
                  command=self.limpiar_matricula).pack(side="left", padx=5)
    
    
    # ==================== TAB BÚSQUEDA ====================
    def configurar_tab_busqueda(self):
        # Frame superior: Búsqueda
        frame_busqueda = ttk.LabelFrame(self.tab_busqueda, text="Buscar Estudiante", padding=15)
        frame_busqueda.pack(padx=20, pady=10, fill="x")
        
        ttk.Label(frame_busqueda, text="Buscar:").grid(row=0, column=0, padx=5, pady=5)
        self.ent_busqueda = ttk.Entry(frame_busqueda, width=30)
        self.ent_busqueda.grid(row=0, column=1, padx=5, pady=5)
        self.ent_busqueda.bind('<KeyRelease>', lambda e: self.buscar_estudiante())
        
        ttk.Button(frame_busqueda, text=" Buscar", 
                  command=self.buscar_estudiante).grid(row=0, column=2, padx=5)
        ttk.Button(frame_busqueda, text=" Ver Todos", 
                  command=self.cargar_todos_estudiantes).grid(row=0, column=3, padx=5)
        
        # Frame medio: Lista de resultados
        frame_resultados = ttk.LabelFrame(self.tab_busqueda, text="Resultados", padding=10)
        frame_resultados.pack(padx=20, pady=10, fill="both", expand=True)
        
        columns = ("ID", "Nombre", "Apellido", "Identificación", "Correo")
        self.tree_estudiantes = ttk.Treeview(frame_resultados, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.tree_estudiantes.heading(col, text=col)
        
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
        
        # Frame inferior: Acciones
        frame_acciones = ttk.LabelFrame(self.tab_busqueda, text="Acciones", padding=15)
        frame_acciones.pack(padx=20, pady=10, fill="x")
        
        self.lbl_seleccionado = ttk.Label(frame_acciones, text="No hay estudiante seleccionado", 
                                         foreground="gray", font=("Arial", 10, "italic"))
        self.lbl_seleccionado.pack(pady=5)
        
        btn_frame = ttk.Frame(frame_acciones)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text=" Actualizar Datos", 
                  command=self.abrir_ventana_actualizar).pack(side="left", padx=5)
        ttk.Button(btn_frame, text=" Eliminar Estudiante", 
                  command=self.eliminar_estudiante_seleccionado).pack(side="left", padx=5)
        
        self.cargar_todos_estudiantes()
    
    
    # ==================== TAB PAGOS Y MATRÍCULAS ====================
    def configurar_tab_pagos(self):
        # Frame superior: Búsqueda de estudiante
        frame_busqueda = ttk.LabelFrame(self.tab_pagos, text="Seleccionar Estudiante", padding=15)
        frame_busqueda.pack(padx=20, pady=10, fill="x")
        
        ttk.Label(frame_busqueda, text="Buscar:").grid(row=0, column=0, padx=5, pady=5)
        self.ent_busqueda_pago = ttk.Entry(frame_busqueda, width=30)
        self.ent_busqueda_pago.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(frame_busqueda, text=" Buscar", 
                  command=self.buscar_estudiante_pagos).grid(row=0, column=2, padx=5)
        
        self.lbl_estudiante_pago = ttk.Label(frame_busqueda, text="Ningún estudiante seleccionado", 
                                            foreground="gray")
        self.lbl_estudiante_pago.grid(row=1, column=0, columnspan=3, pady=5)
        
        # Notebook interno para Matrículas y Pagos
        self.notebook_pagos = ttk.Notebook(self.tab_pagos)
        self.notebook_pagos.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Sub-tab: Registrar Matrícula
        tab_reg_matricula = ttk.Frame(self.notebook_pagos)
        self.notebook_pagos.add(tab_reg_matricula, text="📚 Registrar Matrícula")
        
        frame_mat = ttk.LabelFrame(tab_reg_matricula, text="Nueva Matrícula", padding=20)
        frame_mat.pack(padx=20, pady=20)
        
        ttk.Label(frame_mat, text="Año:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.ent_anio = ttk.Entry(frame_mat, width=20)
        self.ent_anio.insert(0, str(datetime.now().year))
        self.ent_anio.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(frame_mat, text="Cuatrimestre:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.cmb_cuatrimestre = ttk.Combobox(frame_mat, values=[1, 2, 3], width=18, state="readonly")
        self.cmb_cuatrimestre.current(0)
        self.cmb_cuatrimestre.grid(row=1, column=1, padx=10, pady=10)
        
        ttk.Label(frame_mat, text="Monto Total:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.ent_monto_matricula = ttk.Entry(frame_mat, width=20)
        self.ent_monto_matricula.grid(row=2, column=1, padx=10, pady=10)
        
        ttk.Button(frame_mat, text=" Registrar Matrícula", 
                  command=self.registrar_nueva_matricula).grid(row=3, column=0, columnspan=2, pady=15)
        
        # Sub-tab: Registrar Pago
        tab_reg_pago = ttk.Frame(self.notebook_pagos)
        self.notebook_pagos.add(tab_reg_pago, text=" Registrar Pago")
        
        frame_pago = ttk.LabelFrame(tab_reg_pago, text="Nuevo Pago", padding=20)
        frame_pago.pack(padx=20, pady=20)
        
        ttk.Label(frame_pago, text="Monto:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.ent_monto_pago = ttk.Entry(frame_pago, width=20)
        self.ent_monto_pago.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(frame_pago, text="Método de Pago:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.cmb_metodo_pago = ttk.Combobox(frame_pago, 
                                           values=["Tarjeta", "Transferencia", "Efectivo", "Cheque"], 
                                           width=18, state="readonly")
        self.cmb_metodo_pago.current(0)
        self.cmb_metodo_pago.grid(row=1, column=1, padx=10, pady=10)
        
        ttk.Button(frame_pago, text=" Registrar Pago", 
                  command=self.registrar_nuevo_pago).grid(row=2, column=0, columnspan=2, pady=15)
        
        # Sub-tab: Historial
        tab_historial = ttk.Frame(self.notebook_pagos)
        self.notebook_pagos.add(tab_historial, text=" Historial")
        
        # Matrículas
        frame_hist_mat = ttk.LabelFrame(tab_historial, text="Matrículas", padding=10)
        frame_hist_mat.pack(padx=20, pady=10, fill="both", expand=True)
        
        columns_mat = ("ID", "Año", "Cuatrimestre", "Monto")
        self.tree_matriculas = ttk.Treeview(frame_hist_mat, columns=columns_mat, show="headings", height=5)
        
        for col in columns_mat:
            self.tree_matriculas.heading(col, text=col)
            self.tree_matriculas.column(col, width=100)
        
        self.tree_matriculas.pack(fill="both", expand=True)
        
        ttk.Button(frame_hist_mat, text="🔄 Actualizar", 
                  command=self.actualizar_historial_matriculas).pack(pady=5)
        
        # Pagos
        frame_hist_pag = ttk.LabelFrame(tab_historial, text="Pagos Realizados", padding=10)
        frame_hist_pag.pack(padx=20, pady=10, fill="both", expand=True)
        
        columns_pag = ("ID", "Fecha", "Monto", "Método", "Estado")
        self.tree_pagos = ttk.Treeview(frame_hist_pag, columns=columns_pag, show="headings", height=5)
        
        for col in columns_pag:
            self.tree_pagos.heading(col, text=col)
            self.tree_pagos.column(col, width=100)
        
        self.tree_pagos.pack(fill="both", expand=True)
        
        ttk.Button(frame_hist_pag, text="🔄 Actualizar", 
                  command=self.actualizar_historial_pagos).pack(pady=5)
    
    
    # ==================== TAB ESTADOS FINANCIEROS ====================
    def configurar_tab_estados(self):
        frame_titulo = ttk.Frame(self.tab_estados)
        frame_titulo.pack(padx=20, pady=10, fill="x")
        
        ttk.Label(frame_titulo, text="Estados Financieros de Estudiantes", 
                 font=("Arial", 14, "bold")).pack(side="left")
        ttk.Button(frame_titulo, text=" Actualizar", 
                  command=self.cargar_estados_financieros).pack(side="right")
        
        # Tabla de estados
        frame_tabla = ttk.Frame(self.tab_estados)
        frame_tabla.pack(padx=20, pady=10, fill="both", expand=True)
        
        columns = ("ID", "Estudiante", "Identificación", "Saldo", "Última Act.", "Estado")
        self.tree_estados = ttk.Treeview(frame_tabla, columns=columns, show="headings", height=20)
        
        self.tree_estados.heading("ID", text="ID")
        self.tree_estados.heading("Estudiante", text="Estudiante")
        self.tree_estados.heading("Identificación", text="Identificación")
        self.tree_estados.heading("Saldo", text="Saldo Actual")
        self.tree_estados.heading("Última Act.", text="Última Actualización")
        self.tree_estados.heading("Estado", text="Estado")
        
        self.tree_estados.column("ID", width=50)
        self.tree_estados.column("Estudiante", width=200)
        self.tree_estados.column("Identificación", width=120)
        self.tree_estados.column("Saldo", width=120)
        self.tree_estados.column("Última Act.", width=150)
        self.tree_estados.column("Estado", width=100)
        
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree_estados.yview)
        self.tree_estados.configure(yscrollcommand=scrollbar.set)
        
        self.tree_estados.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.cargar_estados_financieros()
    
    
    # ==================== TAB ALERTAS ====================
    def configurar_tab_alertas(self):
        frame_titulo = ttk.Frame(self.tab_alertas)
        frame_titulo.pack(padx=20, pady=10, fill="x")
        
        ttk.Label(frame_titulo, text="Alertas de Morosidad", 
                 font=("Arial", 14, "bold")).pack(side="left")
        
        btn_frame = ttk.Frame(frame_titulo)
        btn_frame.pack(side="right")
        
        ttk.Button(btn_frame, text=" Generar Alertas", 
                  command=self.generar_alertas_manual).pack(side="left", padx=5)
        
        ttk.Button(btn_frame, text=" Actualizar", 
                  command=self.cargar_alertas).pack(side="left", padx=5)
        
        # Tabla de alertas
        frame_tabla = ttk.Frame(self.tab_alertas)
        frame_tabla.pack(padx=20, pady=10, fill="both", expand=True)
        
        columns = ("ID", "Estudiante", "Identificación", "Correo", "Días Mora", "Saldo", "Fecha", "Estado")
        self.tree_alertas = ttk.Treeview(frame_tabla, columns=columns, show="headings", height=20)
        
        for col in columns:
            self.tree_alertas.heading(col, text=col)
        
        self.tree_alertas.column("ID", width=50)
        self.tree_alertas.column("Estudiante", width=200)
        self.tree_alertas.column("Identificación", width=120)
        self.tree_alertas.column("Correo", width=200)
        self.tree_alertas.column("Días Mora", width=80)
        self.tree_alertas.column("Saldo", width=100)
        self.tree_alertas.column("Fecha", width=120)
        self.tree_alertas.column("Estado", width=100)
        
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree_alertas.yview)
        self.tree_alertas.configure(yscrollcommand=scrollbar.set)
        
        self.tree_alertas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botón para resolver alerta
        ttk.Button(self.tab_alertas, text=" Resolver Alerta Seleccionada", 
                  command=self.resolver_alerta_seleccionada).pack(pady=10)
        
        self.cargar_alertas()
    
    
    # ==================== FUNCIONES DE MATRÍCULA ====================
    def guardar_estudiante(self):
        nombre = self.ent_nombre.get().strip()
        apellido = self.ent_apellido.get().strip()
        identificacion = self.ent_identificacion.get().strip()
        correo = self.ent_correo.get().strip()
        
        if not all([nombre, apellido, identificacion, correo]):
            messagebox.showwarning("Campos vacíos", "Por favor complete todos los campos")
            return
        
        if insertar_estudiante(nombre, apellido, identificacion, correo):
            messagebox.showinfo("Éxito", " Estudiante registrado correctamente")
            self.limpiar_matricula()
            self.cargar_todos_estudiantes()
        else:
            messagebox.showerror("Error", "No se pudo registrar el estudiante")
    
    def limpiar_matricula(self):
        self.ent_nombre.delete(0, tk.END)
        self.ent_apellido.delete(0, tk.END)
        self.ent_identificacion.delete(0, tk.END)
        self.ent_correo.delete(0, tk.END)
    
    
    # ==================== FUNCIONES DE BÚSQUEDA ====================
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
                est['id'], est['nombre'], est['apellido'],
                est['identificacion'], est['correo']
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
    
    def abrir_ventana_actualizar(self):
        if not self.estudiante_seleccionado:
            messagebox.showwarning("Selección requerida", "Debe seleccionar un estudiante primero")
            return
        
        ventana = tk.Toplevel(self.root)
        ventana.title("Actualizar Datos del Estudiante")
        ventana.geometry("450x350")
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
            if actualizar_estudiante(
                self.estudiante_seleccionado['id'],
                ent_nombre.get().strip(),
                ent_apellido.get().strip(),
                ent_identificacion.get().strip(),
                ent_correo.get().strip()
            ):
                messagebox.showinfo("Éxito", "Datos actualizados correctamente")
                ventana.destroy()
                self.cargar_todos_estudiantes()
            else:
                messagebox.showerror("Error", "No se pudo actualizar")
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text=" Guardar", command=guardar_cambios).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=ventana.destroy).pack(side="left", padx=5)
    
    def eliminar_estudiante_seleccionado(self):
        if not self.estudiante_seleccionado:
            messagebox.showwarning("Selección requerida", "Debe seleccionar un estudiante primero")
            return
        
        respuesta = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Está seguro que desea eliminar a:\n\n{self.estudiante_seleccionado['nombre']} {self.estudiante_seleccionado['apellido']}\n\nEsta acción no se puede deshacer."
        )
        
        if respuesta:
            if eliminar_estudiante(self.estudiante_seleccionado['id']):
                messagebox.showinfo("Éxito", " Estudiante eliminado correctamente")
                self.estudiante_seleccionado = None
                self.cargar_todos_estudiantes()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el estudiante")
    
    
    # ==================== FUNCIONES DE PAGOS ====================
    def buscar_estudiante_pagos(self):
        termino = self.ent_busqueda_pago.get().strip()
        if not termino:
            messagebox.showwarning("Campo vacío", "Ingrese un término de búsqueda")
            return
        
        estudiantes = buscar_estudiantes(termino)
        if not estudiantes:
            messagebox.showinfo("Sin resultados", "No se encontraron estudiantes")
            return
        
        if len(estudiantes) == 1:
            self.seleccionar_estudiante_pago(estudiantes[0])
        else:
            self.mostrar_seleccion_estudiantes(estudiantes)
    
    def mostrar_seleccion_estudiantes(self, estudiantes):
        ventana = tk.Toplevel(self.root)
        ventana.title("Seleccionar Estudiante")
        ventana.geometry("600x400")
        ventana.grab_set()
        
        ttk.Label(ventana, text="Seleccione un estudiante:", font=("Arial", 11, "bold")).pack(pady=10)
        
        frame = ttk.Frame(ventana)
        frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        columns = ("ID", "Nombre", "Apellido", "Identificación")
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        
        for col in columns:
            tree.heading(col, text=col)
        
        for est in estudiantes:
            tree.insert("", "end", values=(est['id'], est['nombre'], est['apellido'], est['identificacion']))
        
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        def seleccionar():
            seleccion = tree.selection()
            if seleccion:
                item = tree.item(seleccion[0])
                valores = item['values']
                est_sel = next((e for e in estudiantes if e['id'] == valores[0]), None)
                if est_sel:
                    self.seleccionar_estudiante_pago(est_sel)
                    ventana.destroy()
        
        ttk.Button(ventana, text="Seleccionar", command=seleccionar).pack(pady=10)
    
    def seleccionar_estudiante_pago(self, estudiante):
        self.estudiante_pago = estudiante
        self.lbl_estudiante_pago.config(
            text=f"Seleccionado: {estudiante['nombre']} {estudiante['apellido']} (ID: {estudiante['id']})",
            foreground="blue"
        )
        self.actualizar_historial_matriculas()
        self.actualizar_historial_pagos()
    
    def registrar_nueva_matricula(self):
        if not hasattr(self, 'estudiante_pago'):
            messagebox.showwarning("Estudiante requerido", "Primero busque y seleccione un estudiante")
            return
        
        try:
            anio = int(self.ent_anio.get())
            cuatrimestre = int(self.cmb_cuatrimestre.get())
            monto = float(self.ent_monto_matricula.get())
            
            if monto <= 0:
                messagebox.showwarning("Monto inválido", "El monto debe ser mayor a 0")
                return
            
            if registrar_matricula(self.estudiante_pago['id'], anio, cuatrimestre, monto):
                messagebox.showinfo("Éxito", f" Matrícula registrada por ${monto}")
                self.ent_monto_matricula.delete(0, tk.END)
                self.actualizar_historial_matriculas()
                self.cargar_estados_financieros()
            else:
                messagebox.showerror("Error", "No se pudo registrar la matrícula")
                
        except ValueError:
            messagebox.showerror("Error", "Ingrese valores válidos")
    
    def registrar_nuevo_pago(self):
        if not hasattr(self, 'estudiante_pago'):
            messagebox.showwarning("Estudiante requerido", "Primero busque y seleccione un estudiante")
            return
        
        try:
            monto = float(self.ent_monto_pago.get())
            metodo = self.cmb_metodo_pago.get()
            
            if monto <= 0:
                messagebox.showwarning("Monto inválido", "El monto debe ser mayor a 0")
                return
            
            if registrar_pago(self.estudiante_pago['id'], monto, metodo):
                messagebox.showinfo("Éxito", f"💰 Pago de ${monto} registrado correctamente")
                self.ent_monto_pago.delete(0, tk.END)
                self.actualizar_historial_pagos()
                self.cargar_estados_financieros()
                self.cargar_alertas()
            else:
                messagebox.showerror("Error", "No se pudo registrar el pago")
                
        except ValueError:
            messagebox.showerror("Error", "Ingrese un monto válido")
    
    def actualizar_historial_matriculas(self):
        if not hasattr(self, 'estudiante_pago'):
            return
        
        for item in self.tree_matriculas.get_children():
            self.tree_matriculas.delete(item)
        
        matriculas = listar_matriculas_estudiante(self.estudiante_pago['id'])
        for mat in matriculas:
            self.tree_matriculas.insert("", "end", values=(
                mat['id_matricula'],
                mat['anio'],
                mat['cuatrimestre'],
                f"${mat['monto_total']:.2f}"
            ))
    
    def actualizar_historial_pagos(self):
        if not hasattr(self, 'estudiante_pago'):
            return
        
        for item in self.tree_pagos.get_children():
            self.tree_pagos.delete(item)
        
        pagos = listar_pagos_estudiante(self.estudiante_pago['id'])
        for pago in pagos:
            fecha = pago['fecha_pago'].strftime('%Y-%m-%d') if hasattr(pago['fecha_pago'], 'strftime') else str(pago['fecha_pago'])
            self.tree_pagos.insert("", "end", values=(
                pago['id_pago'],
                fecha,
                f"${pago['monto']:.2f}",
                pago['metodo_pago'],
                pago['estado']
            ))
    
    
    # ==================== FUNCIONES DE ESTADOS FINANCIEROS ====================
    def cargar_estados_financieros(self):
        for item in self.tree_estados.get_children():
            self.tree_estados.delete(item)
        
        estados = listar_estados_financieros()
        for est in estados:
            fecha = est['ultima_actualizacion'].strftime('%Y-%m-%d') if hasattr(est['ultima_actualizacion'], 'strftime') else str(est['ultima_actualizacion'])
            
            # Color según el estado
            tags = ()
            if est['estado'] == 'Debe':
                tags = ('debe',)
            elif est['estado'] == 'Al Día':
                tags = ('aldia',)
            
            self.tree_estados.insert("", "end", values=(
                est['id_estudiante'],
                est['nombre_completo'],
                est['identificacion'],
                f"${est['saldo_actual']:.2f}",
                fecha,
                est['estado']
            ), tags=tags)
        
        # Configurar colores
        self.tree_estados.tag_configure('debe', foreground='red')
        self.tree_estados.tag_configure('aldia', foreground='green')
    
    
    # ==================== FUNCIONES DE ALERTAS ====================
    def cargar_alertas(self):
        for item in self.tree_alertas.get_children():
            self.tree_alertas.delete(item)
        
        alertas = listar_alertas_morosidad()
        for alerta in alertas:
            fecha = alerta['fecha_alerta'].strftime('%Y-%m-%d') if hasattr(alerta['fecha_alerta'], 'strftime') else str(alerta['fecha_alerta'])
            
            self.tree_alertas.insert("", "end", values=(
                alerta['id_alerta'],
                alerta['nombre_completo'],
                alerta['identificacion'],
                alerta['correo'],
                alerta['dias_mora'],
                f"${alerta['saldo_actual']:.2f}",
                fecha,
                alerta['estado_alerta']
            ), tags=('alerta',))
        
        self.tree_alertas.tag_configure('alerta', foreground='red', font=('Arial', 9, 'bold'))
    
    def generar_alertas_manual(self):
        respuesta = messagebox.askyesno(
            "Generar Alertas",
            "Genera alertas para estudiantes con MATRÍCULAS VENCIDAS y saldo pendiente.\n\n¿Continuar?"
        )
        
        if respuesta:
            if generar_alertas():
                messagebox.showinfo("Éxito", "Alertas generadas correctamente")
                self.cargar_alertas()
            else:
                messagebox.showerror("Error", "No se pudieron generar las alertas")
    
    def generar_alertas_prueba(self):
        respuesta = messagebox.askyesno(
            "Generar Alertas de Prueba",
            "Genera alertas para TODOS los estudiantes con saldo pendiente (sin importar vencimiento).\n\nÚtil para pruebas.\n\n¿Continuar?"
        )
        
        if respuesta:
            if generar_alertas_prueba():
                messagebox.showinfo("Éxito", " Alertas de prueba generadas")
                self.cargar_alertas()
            else:
                messagebox.showerror("Error", "No se pudieron generar las alertas")
    
    def resolver_alerta_seleccionada(self):
        seleccion = self.tree_alertas.selection()
        if not seleccion:
            messagebox.showwarning("Selección requerida", "Debe seleccionar una alerta")
            return
        
        item = self.tree_alertas.item(seleccion[0])
        id_alerta = item['values'][0]
        
        respuesta = messagebox.askyesno(
            "Resolver Alerta",
            "¿Marcar esta alerta como resuelta?"
        )
        
        if respuesta:
            if resolver_alerta(id_alerta):
                messagebox.showinfo("Éxito", " Alerta resuelta")
                self.cargar_alertas()
            else:
                messagebox.showerror("Error", "No se pudo resolver la alerta")


if __name__ == "__main__":
    root = tk.Tk()
    app = ControlPagosGUI(root)
    root.mainloop()