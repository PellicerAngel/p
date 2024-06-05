import tkinter as tk

from tkinter import messagebox, ttk

from pymongo import MongoClient

import time

from datetime import datetime



# Conectar a MongoDB

client = MongoClient('mongodb://localhost:27017/')

db = client['fitdiary']

usuarios_collection = db['usuarios']

registros_collection = db['registros']



# Función para verificar la conexión con MongoDB

def check_mongodb_connection():

    try:

        client.server_info()

        return True

    except Exception as e:

        return False



# Esperar hasta que se establezca la conexión con MongoDB o hasta que se agote el tiempo

def wait_for_mongodb_connection():

    timeout = 30  # segundos

    start_time = time.time()

    while time.time() - start_time < timeout:

        if check_mongodb_connection():

            return True

        time.sleep(1)

    return False



class Aplicacion:

    def __init__(self, root):

        self.root = root

        self.root.title("Aplicación de Usuario")

        self.root.geometry("400x400")

        

        self.crear_inicio_frame()

    

    def crear_inicio_frame(self):

        self.inicio_frame = tk.Frame(self.root)

        self.inicio_frame.pack(pady=20)

        

        # Titulo

        tk.Label(self.inicio_frame, text="FitDiary", font=("Helvetica", 16, "bold")).pack(pady=5)

        

        # Usuario

        tk.Label(self.inicio_frame, text="Usuario").pack(pady=5)

        self.usuario_entry_inicio = tk.Entry(self.inicio_frame)

        self.usuario_entry_inicio.pack(pady=5)

        

        # Contraseña

        tk.Label(self.inicio_frame, text="Contraseña").pack(pady=5)

        self.contrasena_entry_inicio = tk.Entry(self.inicio_frame, show="*")

        self.contrasena_entry_inicio.pack(pady=5)

        

        # Botón de Iniciar Sesión

        self.iniciar_sesion_button = tk.Button(self.inicio_frame, text="Iniciar Sesión", command=self.iniciar_sesion, bg="#4CAF50", fg="white")

        self.iniciar_sesion_button.pack(pady=10)

        

        # Botón de Crear Usuario

        self.crear_usuario_button = tk.Button(self.inicio_frame, text="Crear Usuario", command=self.mostrar_registro_frame, bg="#2196F3", fg="white")

        self.crear_usuario_button.pack(pady=5)

    

    def iniciar_sesion(self):

        if not wait_for_mongodb_connection():

            messagebox.showerror("Error", "No se pudo establecer conexión con la base de datos.")

            return

        

        usuario = self.usuario_entry_inicio.get()

        contrasena = self.contrasena_entry_inicio.get()

        

        user = usuarios_collection.find_one({"usuario": usuario, "contrasena": contrasena})

        

        if user:

            self.usuario_actual = user

            self.mostrar_bienvenida_frame()

        else:

            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    

    def mostrar_registro_frame(self):

        self.limpiar_frames()

        

        self.registro_frame = tk.Frame(self.root)

        self.registro_frame.pack(pady=20)

        

        tk.Label(self.registro_frame, text="Registro de Usuario", font=("Helvetica", 16, "bold")).pack(pady=5)

        

        tk.Label(self.registro_frame, text="Usuario").pack(pady=5)

        self.usuario_entry_registro = tk.Entry(self.registro_frame)

        self.usuario_entry_registro.pack(pady=5)

        

        tk.Label(self.registro_frame, text="Contraseña").pack(pady=5)

        self.contrasena_entry_registro = tk.Entry(self.registro_frame, show="*")

        self.contrasena_entry_registro.pack(pady=5)



        tk.Label(self.registro_frame, text="DNI").pack(pady=5)

        self.dni_entry_registro = tk.Entry(self.registro_frame)

        self.dni_entry_registro.pack(pady=5)

        

        tk.Label(self.registro_frame, text="Edad").pack(pady=5)

        self.edad_entry_registro = tk.Entry(self.registro_frame)

        self.edad_entry_registro.pack(pady=5)

        

        tk.Label(self.registro_frame, text="Género").pack(pady=5)

        self.genero_entry_registro = ttk.Combobox(self.registro_frame, values=["Masculino", "Femenino"])

        self.genero_entry_registro.pack(pady=5)

        

        tk.Label(self.registro_frame, text="Peso").pack(pady=5)

        self.peso_entry_registro = tk.Entry(self.registro_frame)

        self.peso_entry_registro.pack(pady=5)

        

        tk.Label(self.registro_frame, text="Grasa corporal (%)").pack(pady=5)

        self.grasa_entry_registro = tk.Entry(self.registro_frame)

        self.grasa_entry_registro.pack(pady=5)

        

        tk.Button(self.registro_frame, text="Registrar", command=self.registrar_usuario, bg="#4CAF50", fg="white").pack(pady=10)

        tk.Button(self.registro_frame, text="Cancelar", command=self.mostrar_inicio_frame, bg="#F44336", fg="white").pack(pady=5)

    

    def mostrar_bienvenida_frame(self):

        self.limpiar_frames()

        

        self.bienvenida_frame = tk.Frame(self.root)

        self.bienvenida_frame.pack(pady=20)

        

        tk.Label(self.bienvenida_frame, text=f"Bienvenido, {self.usuario_actual['usuario']}", font=("Helvetica", 16, "bold")).pack(pady=5)

        

        tk.Button(self.bienvenida_frame, text="Crear registro de entrenamiento", command=self.mostrar_crear_registro_frame, bg="#4CAF50", fg="white").pack(pady=10)

        tk.Button(self.bienvenida_frame, text="Ver registros", command=self.mostrar_registros_frame, bg="#2196F3", fg="white").pack(pady=5)

        tk.Button(self.bienvenida_frame, text="Modificar datos personales", command=self.mostrar_modificar_datos_frame, bg="#FFC107", fg="black").pack(pady=5)

        tk.Button(self.bienvenida_frame, text="Cerrar sesión", command=self.mostrar_inicio_frame, bg="#F44336", fg="white").pack(pady=5)

    

    def mostrar_crear_registro_frame(self):

        self.limpiar_frames()

        

        self.crear_registro_frame = tk.Frame(self.root)

        self.crear_registro_frame.pack(pady=20)

        

        tk.Label(self.crear_registro_frame, text="Crear Registro de Entrenamiento", font=("Helvetica", 16, "bold")).pack(pady=5)

        

        tk.Label(self.crear_registro_frame, text="Duración (min)").pack(pady=5)

        self.duracion_entry = tk.Entry(self.crear_registro_frame)

        self.duracion_entry.pack(pady=5)

        

        tk.Label(self.crear_registro_frame, text="Tipo de entrenamiento").pack(pady=5)

        self.tipo_entrenamiento = ttk.Combobox(self.crear_registro_frame, values=["Fuerza", "Cardio", "Flexibilidad", "Otros"])

        self.tipo_entrenamiento.pack(pady=5)

        

        tk.Button(self.crear_registro_frame, text="Guardar registro", command=self.guardar_registro, bg="#4CAF50", fg="white").pack(pady=10)

        tk.Button(self.crear_registro_frame, text="Cancelar", command=self.mostrar_bienvenida_frame, bg="#F44336", fg="white").pack(pady=5)

    

    def guardar_registro(self):

        duracion = self.duracion_entry.get()

        tipo = self.tipo_entrenamiento.get()

        

        if not duracion or not tipo:

            messagebox.showerror("Error", "Todos los campos son obligatorios.")

            return

        

        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        usuario_id = self.usuario_actual['_id']

        

        registros_collection.insert_one({

            "usuario_id": usuario_id,

            "fecha": fecha,

            "duracion": duracion,

            "tipo": tipo

        })

        

        messagebox.showinfo("Éxito", "Registro guardado exitosamente.")

        self.mostrar_bienvenida_frame()

    

    def mostrar_registros_frame(self):

        self.limpiar_frames()

        

        self.registros_frame = tk.Frame(self.root)

        self.registros_frame.pack(pady=20)

        

        tk.Label(self.registros_frame, text="Registros de Entrenamiento", font=("Helvetica", 16, "bold")).pack(pady=5)

        

        columnas = ["ID", "Fecha", "Duración (min)", "Tipo de entrenamiento"]

        self.treeview = ttk.Treeview(self.registros_frame, columns=columnas, show="headings")

        

        for col in columnas:

            self.treeview.heading(col, text=col)

        

        self.treeview.pack(pady=10)

        

        usuario_id = self.usuario_actual['_id']

        registros = list(registros_collection.find({"usuario_id": usuario_id}))

        

        for i, registro in enumerate(registros, start=1):

            self.treeview.insert("", "end", values=(i, registro["fecha"], registro["duracion"], registro["tipo"]))

        

        tk.Button(self.registros_frame, text="Salir", command=self.mostrar_bienvenida_frame, bg="#F44336", fg="white").pack(pady=5)

    

    def mostrar_modificar_datos_frame(self):

        self.limpiar_frames()

        

        self.modificar_datos_frame = tk.Frame(self.root)

        self.modificar_datos_frame.pack(pady=20)

        

        tk.Label(self.modificar_datos_frame, text="Modificar Datos Personales", font=("Helvetica", 16, "bold")).pack(pady=5)

        

        tk.Label(self.modificar_datos_frame, text="DNI").pack(pady=5)

        self.dni_entry_modificar = tk.Entry(self.modificar_datos_frame)

        self.dni_entry_modificar.pack(pady=5)

        

        tk.Label(self.modificar_datos_frame, text="Edad").pack(pady=5)

        self.edad_entry_modificar = tk.Entry(self.modificar_datos_frame)

        self.edad_entry_modificar.pack(pady=5)

        

        tk.Label(self.modificar_datos_frame, text="Género").pack(pady=5)

        self.genero_entry_modificar = ttk.Combobox(self.modificar_datos_frame, values=["Masculino", "Femenino"])

        self.genero_entry_modificar.pack(pady=5)

        

        tk.Label(self.modificar_datos_frame, text="Peso").pack(pady=5)

        self.peso_entry_modificar = tk.Entry(self.modificar_datos_frame)

        self.peso_entry_modificar.pack(pady=5)

        

        tk.Label(self.modificar_datos_frame, text="Grasa corporal (%)").pack(pady=5)

        self.grasa_entry_modificar = tk.Entry(self.modificar_datos_frame)

        self.grasa_entry_modificar.pack(pady=5)

        

        tk.Button(self.modificar_datos_frame, text="Guardar cambios", command=self.guardar_datos_modificados, bg="#4CAF50", fg="white").pack(pady=10)

        tk.Button(self.modificar_datos_frame, text="Cancelar", command=self.mostrar_bienvenida_frame, bg="#F44336", fg="white").pack(pady=5)

    

    def guardar_datos_modificados(self):

        dni = self.dni_entry_modificar.get()

        edad = self.edad_entry_modificar.get()

        genero = self.genero_entry_modificar.get()

        peso = self.peso_entry_modificar.get()

        grasa = self.grasa_entry_modificar.get()

        

        usuarios_collection.update_one(

            {"_id": self.usuario_actual["_id"]},

            {"$set": {

                "dni": dni,

                "edad": edad,

                "genero": genero,

                "peso": peso,

                "grasa": grasa

            }}

        )

        

        messagebox.showinfo("Éxito", "Datos personales modificados exitosamente.")

        self.mostrar_bienvenida_frame()

    

    def registrar_usuario(self):

        usuario = self.usuario_entry_registro.get()

        contrasena = self.contrasena_entry_registro.get()

        dni = self.dni_entry_registro.get()

        edad = self.edad_entry_registro.get()

        genero = self.genero_entry_registro.get()

        peso = self.peso_entry_registro.get()

        grasa = self.grasa_entry_registro.get()

        

        if not usuario or not contrasena or not dni or not edad or not genero or not peso or not grasa:

            messagebox.showerror("Error", "Todos los campos son obligatorios.")

            return

        

        if usuarios_collection.find_one({"usuario": usuario}):

            messagebox.showerror("Error", "El nombre de usuario ya existe.")

            return

        

        usuarios_collection.insert_one({

            "usuario": usuario,

            "contrasena": contrasena,

            "dni": dni,

            "edad": edad,

            "genero": genero,

            "peso": peso,

            "grasa": grasa

        })

        

        messagebox.showinfo("Éxito", "Usuario registrado exitosamente.")

        self.mostrar_inicio_frame()

    

    def limpiar_frames(self):

        for widget in self.root.winfo_children():

            widget.destroy()



    def mostrar_inicio_frame(self):

        self.limpiar_frames()

        self.crear_inicio_frame()



if __name__ == "__main__":

    root = tk.Tk()

    app = Aplicacion(root)

    root.mainloop()

