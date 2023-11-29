# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 20:42:16 2023

@author: pablo
"""

import tkinter as tk
from tkinter import messagebox
import sqlite3

class AplicacionCRUD:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicación CRUD")

        # Conexión a la base de datos SQLite (o cambia esto a tu base de datos preferida)
        self.conn = sqlite3.connect('crud_database.db')
        self.cursor = self.conn.cursor()

        # Crear la tabla si no existe
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS registros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                edad INTEGER NOT NULL
            )
        ''')
        self.conn.commit()

        # Interfaz gráfica
        self.crear_widgets()

    def crear_widgets(self):
        # Etiquetas y cuadros de entrada
        self.label_nombre = tk.Label(self.root, text="Nombre:")
        self.label_nombre.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.label_edad = tk.Label(self.root, text="Edad:")
        self.label_edad.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        self.entry_nombre = tk.Entry(self.root)
        self.entry_nombre.grid(row=0, column=1, padx=10, pady=10)

        self.entry_edad = tk.Entry(self.root)
        self.entry_edad.grid(row=1, column=1, padx=10, pady=10)

        # Botones en línea horizontal
        self.boton_crear = tk.Button(self.root, text="Crear", command=self.crear_registro)
        self.boton_crear.grid(row=2, column=0, pady=10, padx=5)

        self.boton_leer = tk.Button(self.root, text="Leer", command=self.leer_registros)
        self.boton_leer.grid(row=2, column=1, pady=10, padx=5)

        self.boton_actualizar = tk.Button(self.root, text="Actualizar", command=self.actualizar_registro)
        self.boton_actualizar.grid(row=2, column=2, pady=10, padx=5)

        self.boton_eliminar = tk.Button(self.root, text="Eliminar", command=self.eliminar_registro)
        self.boton_eliminar.grid(row=2, column=3, pady=10, padx=5)

    def crear_registro(self):
        nombre = self.entry_nombre.get()
        edad = self.entry_edad.get()

        if nombre and edad:
            self.cursor.execute('INSERT INTO registros (nombre, edad) VALUES (?, ?)', (nombre, edad))
            self.conn.commit()
            messagebox.showinfo("Éxito", "Registro creado con éxito.")
        else:
            messagebox.showerror("Error", "Por favor, completa todos los campos.")

    def leer_registros(self):
        self.cursor.execute('SELECT * FROM registros')
        registros = self.cursor.fetchall()

        if registros:
            resultado_texto = "Registros:\n"
            for registro in registros:
                resultado_texto += f"ID: {registro[0]}, Nombre: {registro[1]}, Edad: {registro[2]}\n"
        else:
            resultado_texto = "No hay registros en la base de datos."

        messagebox.showinfo("Registros", resultado_texto)

    def actualizar_registro(self):
        id_registro = simpledialog.askinteger("Actualizar Registro", "Ingrese el ID del registro a actualizar:")

        if id_registro is not None:
            self.cursor.execute('SELECT * FROM registros WHERE id=?', (id_registro,))
            registro = self.cursor.fetchone()

            if registro:
                # Mostrar el registro existente
                messagebox.showinfo("Registro Existente", f"ID: {registro[0]}, Nombre: {registro[1]}, Edad: {registro[2]}")

                # Obtener la nueva información del usuario
                nuevo_nombre = simpledialog.askstring("Actualizar Registro", "Nuevo Nombre:")
                nueva_edad = simpledialog.askinteger("Actualizar Registro", "Nueva Edad:")

                # Actualizar el registro en la base de datos
                self.cursor.execute('''
                    UPDATE registros
                    SET nombre=?, edad=?
                    WHERE id=?
                ''', (nuevo_nombre, nueva_edad, id_registro))
                self.conn.commit()

                messagebox.showinfo("Éxito", "Registro actualizado con éxito.")
            else:
                messagebox.showerror("Error", "ID de registro no encontrado.")
    
    def eliminar_registro(self):
        id_registro = simpledialog.askinteger("Eliminar Registro", "Ingrese el ID del registro a eliminar:")

        if id_registro is not None:
            self.cursor.execute('SELECT * FROM registros WHERE id=?', (id_registro,))
            registro = self.cursor.fetchone()

            if registro:
                # Mostrar el registro antes de la eliminación
                messagebox.showinfo("Registro a Eliminar", f"ID: {registro[0]}, Nombre: {registro[1]}, Edad: {registro[2]}")

                # Confirmar la eliminación
                confirmar = messagebox.askyesno("Confirmar Eliminación", "¿Está seguro de que desea eliminar este registro?")
                if confirmar:
                    # Eliminar el registro de la base de datos
                    self.cursor.execute('DELETE FROM registros WHERE id=?', (id_registro,))
                    self.conn.commit()

                    messagebox.showinfo("Éxito", "Registro eliminado con éxito.")
            else:
                messagebox.showerror("Error", "ID de registro no encontrado.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionCRUD(root)
    root.mainloop()
