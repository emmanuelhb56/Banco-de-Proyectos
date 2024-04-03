import os
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
from ttkthemes import ThemedTk

class AplicacionIdentificador:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Identificador de Colores Rojos")
        self.ventana.configure(bg="#000000")
        self.ventana.resizable(False, False)

        self.imagenes = []
        self.resultados = []
        self.indice_actual = 0

        self.configurar_interfaz()

    def configurar_interfaz(self):
        self.frame_principal = tk.Frame(self.ventana, bg="#000000")
        self.frame_principal.pack(fill=tk.BOTH, expand=True)

        self.configurar_menu()
        self.crear_seccion_vista_previa()
        self.crear_seccion_navegacion()
        self.crear_barra_estado()

    def configurar_menu(self):
        self.menu_principal = tk.Menu(self.ventana)
        self.ventana.config(menu=self.menu_principal)

        # Menú Archivo
        self.menu_archivo = tk.Menu(self.menu_principal, tearoff=0)
        self.menu_principal.add_cascade(label="Archivo", menu=self.menu_archivo)
        self.menu_archivo.add_command(label="Cargar Imagen", command=self.seleccionar_imagen)
        self.menu_archivo.add_command(label="Cargar Carpeta", command=self.seleccionar_carpeta)
        self.menu_archivo.add_command(label="Guardar", command=self.guardar_resultado)
        self.menu_archivo.add_separator()
        self.menu_archivo.add_command(label="Salir", command=self.ventana.quit)

        # Menú Herramientas
        self.menu_herramientas = tk.Menu(self.menu_principal, tearoff=0)
        self.menu_principal.add_cascade(label="Herramientas", menu=self.menu_herramientas)
        self.menu_herramientas.add_command(label="Búsqueda de color rojo", command=self.identificar_rojo)
        self.menu_herramientas.add_command(label="Mostrar Original", command=self.mostrar_original)

    def crear_seccion_vista_previa(self):
        self.frame_vista_previa = tk.Frame(self.frame_principal, bg="#000000")
        self.frame_vista_previa.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.canvas_resultado = tk.Canvas(self.frame_vista_previa, bg="#000000", width=600, height=400)
        self.canvas_resultado.pack(padx=20, pady=(10, 20), fill=tk.BOTH, expand=True)

        self.nombre_imagen_label = tk.Label(self.frame_vista_previa, bg="#000000", fg="#FFFFFF", text="", anchor=tk.CENTER)
        self.nombre_imagen_label.pack(padx=20, pady=(0, 5), fill=tk.X)

        self.numero_imagen_label = tk.Label(self.frame_vista_previa, bg="#000000", fg="#FFFFFF", text="", anchor=tk.CENTER)
        self.numero_imagen_label.pack(padx=20, pady=(0, 10), fill=tk.X)

    def crear_seccion_navegacion(self):
        self.frame_navegacion = tk.Frame(self.ventana, bg="#000000")
        self.frame_navegacion.pack(side=tk.BOTTOM, fill=tk.X)

        self.boton_anterior = tk.Button(self.frame_navegacion, text="Anterior", command=self.anterior_imagen, state=tk.DISABLED, bg="#333333", fg="#FFFFFF", bd=0, padx=10, pady=5)
        self.boton_anterior.pack(side=tk.LEFT, padx=10, pady=10)

        self.boton_siguiente = tk.Button(self.frame_navegacion, text="Siguiente", command=self.siguiente_imagen, state=tk.DISABLED, bg="#333333", fg="#FFFFFF", bd=0, padx=10, pady=5)
        self.boton_siguiente.pack(side=tk.RIGHT, padx=10, pady=10)

    def crear_barra_estado(self):
        self.barra_estado = tk.Label(self.ventana, text="", bd=1, relief=tk.SUNKEN, anchor=tk.CENTER, bg="#333333", fg="#FFFFFF")
        self.barra_estado.pack(side=tk.BOTTOM, fill=tk.X)

    def actualizar_barra_estado(self, mensaje):
        self.barra_estado.config(text=mensaje)

    def seleccionar_imagen(self):
        ruta_imagen = filedialog.askopenfilename()
        if ruta_imagen:
            if ruta_imagen.lower().endswith(('jpg', 'jpeg', 'png', 'gif', 'bmp')):
                self.imagenes = [ruta_imagen]
                self.indice_actual = 0
                self.cargar_imagen()
                self.actualizar_barra_estado("Imagen cargada correctamente.")
            else:
                self.actualizar_barra_estado("Error: El archivo seleccionado no es una imagen válida.")

    def seleccionar_carpeta(self):
        ruta_carpeta = filedialog.askdirectory()
        if ruta_carpeta:
            imagenes_en_carpeta = [imagen for imagen in os.listdir(ruta_carpeta) if imagen.endswith(('jpg', 'jpeg', 'png', 'gif', 'bmp'))]
            if not imagenes_en_carpeta:
                self.actualizar_barra_estado("Carpeta vacía: La carpeta seleccionada no contiene imágenes válidas.")
                return
            self.imagenes = sorted([os.path.join(ruta_carpeta, imagen) for imagen in imagenes_en_carpeta])
            self.indice_actual = 0
            self.cargar_imagen()
            self.actualizar_barra_estado("Carpeta cargada correctamente.")

    def cargar_imagen(self):
        if self.imagenes:
            self.resultados = []
            nombre_imagen = os.path.basename(self.imagenes[self.indice_actual])
            self.nombre_imagen_label.config(text=f"Imagen seleccionada: {nombre_imagen}")
            self.numero_imagen_label.config(text=f"Número de imagen: {self.indice_actual + 1} de {len(self.imagenes)}")
            imagen = Image.open(self.imagenes[self.indice_actual])
            imagen = imagen.resize((600, 400))  # Ajustar el tamaño de la imagen
            self.imagen_tk = ImageTk.PhotoImage(imagen)
            self.canvas_resultado.config(width=imagen.width, height=imagen.height)  # Ajustar el tamaño del Canvas
            self.canvas_resultado.create_image(0, 0, anchor=tk.NW, image=self.imagen_tk)
            self.canvas_resultado.image = self.imagen_tk

            # Actualizar estados de los botones siguiente y anterior
            self.boton_siguiente.config(state=tk.NORMAL if self.indice_actual < len(self.imagenes) - 1 else tk.DISABLED)
            self.boton_anterior.config(state=tk.NORMAL if self.indice_actual > 0 else tk.DISABLED)

    def anterior_imagen(self):
        if self.indice_actual > 0:
            self.indice_actual -= 1
            self.cargar_imagen()

    def siguiente_imagen(self):
        if self.indice_actual < len(self.imagenes) - 1:
            self.indice_actual += 1
            self.cargar_imagen()

    def identificar_rojo(self):
        if self.imagenes:
            self.resultados = []
            for ruta_imagen in self.imagenes:
                imagen = cv2.imread(ruta_imagen)
                if imagen is not None:
                    hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
                    # Rango de color rojo ajustado
                    rojo_bajo1 = np.array([0, 100, 100])
                    rojo_alto1 = np.array([10, 255, 255])
                    rojo_bajo2 = np.array([160, 100, 100])
                    rojo_alto2 = np.array([179, 255, 255])
                    mascara1 = cv2.inRange(hsv, rojo_bajo1, rojo_alto1)
                    mascara2 = cv2.inRange(hsv, rojo_bajo2, rojo_alto2)
                    mascara_rojo = cv2.bitwise_or(mascara1, mascara2)
                    resultado = cv2.bitwise_and(imagen, imagen, mask=mascara_rojo)
                    resultado[np.where((resultado == [0, 0, 0]).all(axis=2))] = [255, 255, 255]
                    self.resultados.append(resultado)
            self.mostrar_resultado()
            self.actualizar_barra_estado("Búsqueda de color rojo completada.")

    def mostrar_resultado(self):
        self.canvas_resultado.delete("all")
        if self.resultados and len(self.resultados) > self.indice_actual:
            resultado_procesado = self.resultados[self.indice_actual]
            imagen_procesada = cv2.cvtColor(resultado_procesado, cv2.COLOR_BGR2RGB)
            imagen_procesada = Image.fromarray(imagen_procesada)
            
            # Redimensionar la imagen procesada para que coincida con las dimensiones de la imagen original
            imagen_original = Image.open(self.imagenes[self.indice_actual])
            imagen_original = imagen_original.resize((600, 400))
            imagen_procesada = imagen_procesada.resize(imagen_original.size)
            
            imagen_tk = ImageTk.PhotoImage(imagen_procesada)
            self.canvas_resultado.create_image(0, 0, anchor=tk.NW, image=imagen_tk)
            self.canvas_resultado.image = imagen_tk

            self.boton_siguiente.config(state=tk.DISABLED)
            self.boton_anterior.config(state=tk.DISABLED)

    def mostrar_original(self):
        if self.imagenes:
            nombre_imagen = os.path.basename(self.imagenes[self.indice_actual])
            self.nombre_imagen_label.config(text=f"Imagen original: {nombre_imagen}")
            imagen_original = Image.open(self.imagenes[self.indice_actual])
            imagen_original = imagen_original.resize((600, 400))
            imagen_tk = ImageTk.PhotoImage(imagen_original)
            self.canvas_resultado.create_image(0, 0, anchor=tk.NW, image=imagen_tk)
            self.canvas_resultado.image = imagen_tk
            self.actualizar_barra_estado("Se ha regresado la imágen a su estado original.")

    def guardar_resultado(self):
        if self.resultados:
            ruta_guardar = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("Archivo JPEG", "*.jpg"), ("Todos los archivos", "*.*")])
            if ruta_guardar:
                cv2.imwrite(ruta_guardar, self.resultados[self.indice_actual])
                self.actualizar_barra_estado("Resultado guardado exitosamente.")

def main():
    ventana = ThemedTk(theme="equilux")
    aplicacion = AplicacionIdentificador(ventana)
    ventana.mainloop()

if __name__ == "__main__":
    main()