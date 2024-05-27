import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel, Text
import numpy as np
import pickle

"""Esta clase contiene los atributos de la ventana paint y las acciones del menu"""
class PaintApp:

    #En esta funcion se definen todos los parametros de la clase
    def __init__(self, root,username,estado):
        self.root = root
        self.root.title("PaintApp")
        self.pixelSize = 15
        self.minPixelSize = 15
        self.maxPixelSize = 50
        self.gridSize = 50
        self.canvaSize = self.pixelSize * self.gridSize
        self.matrix = np.zeros((self.gridSize, self.gridSize), dtype=int) #np zeros crea una matriz llena de ceros con el grid size
        self.canvas = tk.Canvas(self.root, width=self.canvaSize, height=self.canvaSize, bg="white")
        self.canvas.pack()
        self.colors = [
            "#000000", "#FF0000", "#00FF00", "#0000FF", "#FFFF00", 
            "#FF00FF", "#00FFFF", "#FFFFFF", "#808080", "#572364"
        ]
        self.asciiSimbols = [' ','.', ':', '-', '=', '¡', '&', '$', '%', '@']
        self.colorActual = 7 #Inicia con el color en blanco
        self.cuadros = {}
        self.username = username
        self.estado = estado
        self.gridInicial()
        self.creaMenu()
        self.formaActual = None
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<Button-1>", self.paint)
        self.canvas.bind("<Button-3>", self.right_click)

    def creaMenu(self):
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Guardar", command=self.guardaImagenPickle)
        filemenu.add_command(label="Cargar", command=self.cargaImagenPickle)
        filemenu.add_command(label="Cerrar imagen", command=self.cerrarImagen)
        menubar.add_cascade(label="Archivo", menu=filemenu)

        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label="Zoom in", command=self.zoomIn)
        editmenu.add_command(label="Zoom out", command=self.zoomOut)
        editmenu.add_command(label="Rotar derecha", command=self.rotarDerecha)
        editmenu.add_command(label="Rotar izquierda", command=self.rotarIzquierda)
        editmenu.add_command(label="Reflejo horizontal", command=self.reflejoHorizontal)
        editmenu.add_command(label="Reflejo vertical", command=self.reflejoVertical)
        editmenu.add_command(label="Alto contraste", command=self.altoContraste)
        editmenu.add_command(label="Negativo", command=self.negativo)
        menubar.add_cascade(label="Editar", menu=editmenu)

        viewmenu = tk.Menu(menubar, tearoff=0)
        viewmenu.add_command(label="ASCII-Art", command=self.asciiArt)
        viewmenu.add_command(label="Ver matriz numérica", command=self.verMatrix)
        viewmenu.add_command(label="Info", command=self.verInfo)
        menubar.add_cascade(label="Ver", menu=viewmenu)

        colormenu = tk.Menu(menubar, tearoff=0)
        #Esto crea un boton para cada color de la lista de colores
        for i in range(len(self.colors)):
            colorLabel = f"Color {i+1}"
            colormenu.add_command(label=colorLabel, command=lambda c=i: self.setColor(c))
        menubar.add_cascade(label="Colores", menu=colormenu)

        formsmenu = tk.Menu(menubar, tearoff=0)
        formsmenu.add_command(label="Cuadrado", command=lambda: self.setForma("cuadrado"))
        formsmenu.add_command(label="Círculo", command=lambda: self.setForma("circulo"))
        menubar.add_cascade(label="Formas", menu=formsmenu)
        
        self.root.config(menu=menubar)

    #Esta funcion dibuja el grid cuando se inicia la partida
    def gridInicial(self):
        self.canvas.delete("all") #Me aseguro que el canvas y los cuadros esten limpios
        self.cuadros.clear()
        for y in range(self.gridSize): #Filas del grid
            for x in range(self.gridSize): #Colunmas
                rect = self.canvas.create_rectangle(
                    x * self.pixelSize, y * self.pixelSize, #coordenadas x0 y y0
                    (x + 1) * self.pixelSize, (y + 1) * self.pixelSize, #coordenadas x1 y y1
                    fill=self.colors[self.matrix[y, x]] #le pone color segun el numero de la matrix
                )
                self.cuadros[(x, y)] = rect #utiliza (x,y) para guardar el cuadro en el diccionario

    #Esta funcion maneja el cambio de colores
    def paint(self, event):
        x, y = event.x // self.pixelSize, event.y // self.pixelSize #agarra las coordenadas del click y las reduce al size de los pixeles, algo asi como un mapeo
        if 0 <= x < self.gridSize and 0 <= y < self.gridSize: #verifica que el click este dentro del grid
            self.matrix[y, x] = self.colorActual #modifica la matriz con el numero nuevo de color
            color = self.colors[self.colorActual] #agarra el color de la lista de colores
            self.canvas.itemconfig(self.cuadros[(x, y)], fill=color) #configura el cuadro correspondiente con el color
            self.estado = "en proceso"

    #esta funcion guarda los archivos con pickle
    def guardaImagenPickle(self):
        rutaArchivo = filedialog.asksaveasfilename(defaultextension=".pkl") #abre un dialogo que le pregunta al usuario donde y con que nombre lo quiere guardar
        if rutaArchivo: #revisa si la ruta no esta vacia
            try:
                with open(rutaArchivo, 'wb') as file: #abre el archivo con wb(modo binario)
                    pickle.dump(self.matrix, file) #guarda la matriz con .dump en el la ruta 
                self.estado = "terminado"
            except Exception as e:
                messagebox.showerror("Error", str(e)) #ventana de error

    #esta funcion lee los archivos con pickle, es casi igual que la de guardar, lo unico que cambia es el modo de leer la ruta
    def cargaImagenPickle(self):
        rutaArchivo = filedialog.askopenfilename(filetypes=[("Pickle files", "*.pkl")])
        if rutaArchivo:
            try:
                with open(rutaArchivo, 'rb') as file: #aqui lee la ruta como binario (rb)
                    self.matrix = pickle.load(file) #carga el archivo
                self.updateCanvas() #actualiza el canvas con la matrix del archivo
            except Exception as e:
                messagebox.showerror("Error", str(e))

    #esta funcion resetea el dibujo
    def cerrarImagen(self):
        self.matrix = np.zeros((self.gridSize, self.gridSize), dtype=int) #reestablece la matrix con todos ceros
        self.updateCanvas()

    #esta funcion actualiza los colores del canvas
    def updateCanvas(self):
        for y in range(self.gridSize):
            for x in range(self.gridSize):
                color = self.colors[self.matrix[y, x]] #agarra el numero de la matriz y lo busca en la lista de colores
                self.canvas.itemconfig(self.cuadros[(x, y)], fill=color) #aplica el color al cuadro correspondiente

    #esta funcion cambia el color con el que pintas
    def setColor(self, color):
        self.colorActual = color

    #esta funcion aumenta el size de los pixeles para hacer un zooIn
    def zoomIn(self):
        if self.pixelSize < self.maxPixelSize: #verifica el size limite
            self.pixelSize += 10
            self.gridInicial() #vuelve a hacer el grid con el nuevo size de pixeles

    #esta funcion reduce el size de los pixeles para hacer un zooOut
    def zoomOut(self):
        if self.pixelSize > self.minPixelSize: #verifica el size limite
            self.pixelSize -= 10
            self.gridInicial() #vuelve a hacer el grid con el nuevo size de pixeles

    #esta funcion usa una funcion de numpy para rotar la matriz
    def rotarDerecha(self):
        self.matrix = np.rot90(self.matrix, -1) #el -1 es para que rote en sentido de las agujas del reloj
        self.updateCanvas()

    #esta es lo mismo que la anterior pero en sentido contrario de las agujas del reloj
    def rotarIzquierda(self):
        self.matrix = np.rot90(self.matrix) 
        self.updateCanvas()

    #esta funcion le da vuelta al dibujo
    def reflejoHorizontal(self):
        self.matrix = np.flip(self.matrix, axis=1) #axis=1 es que es en sentido horizontal
        self.updateCanvas()

    #esta funcion le da vuelta al dibujo de manera vertical
    def reflejoVertical(self):
        self.matrix = np.flip(self.matrix, axis=0) #axis=0 es que es en sentido vertical
        self.updateCanvas()

    #esta funcion convierte los valores entre 0 y 4 en 1, y los valores entre 5 y 9 en 9
    def altoContraste(self):
        self.matrix = np.where(self.matrix <= 4, 1, 9) #where es una condición que verifica si cada elemento de la matriz es menor o igual a 4, si es true los convierte en 1 y si es false en 9
        self.updateCanvas()

    #esta funcion invierte los valores de la matri: 9 -> 0, 8 -> 1, ..., 1 -> 8, 0 -> 9
    def negativo(self):
        self.matrix = 9 - self.matrix #invierte los valores con una resta
        self.updateCanvas()

    #esta funcion muestra en una nueva ventana la matriz con caracteres
    def asciiArt(self):
        ventanaASCII = Toplevel(self.root)
        ventanaASCII.title("ASCII Art")
        ventanaASCII.geometry("700x710")
        texto = Text(ventanaASCII, width=100, height=100, font=("Courier", 8)) #crea un widget de texto dentro de la ventana secundaria
        texto.pack(expand=True, fill=tk.BOTH) #esto empaqueta el texto con la opcion de que se expanda
        texto.config(state=tk.NORMAL) #permite la edición del widget de texto para poder insertar el arte ASCII

        for row in self.matrix: #itera por cada fila de la matriz
            textoASCII = ' '.join(self.asciiSimbols[val] for val in row) + '\n' #crea una fila de caracteres usando la lista de simbolos mediante iteracion
            texto.insert(tk.END, textoASCII) #inserta el texto en el widget

        texto.config(state=tk.DISABLED) #deshabilita la edicion del widget para que quede de solo lectura

    #esta funcion se encarga de mostrar la matriz
    def verMatrix(self):
        ventanaMatriz = Toplevel(self.root)
        ventanaMatriz.title("Matriz Numérica")
        ventanaMatriz.geometry("700x710")
        texto = Text(ventanaMatriz, width=100, height=100, font=("Courier", 8)) #crea el widget de texto
        texto.pack(expand=True, fill=tk.BOTH)
        texto.config(state=tk.NORMAL)

        for row in self.matrix: #itera sobre las filas de la matriz
            textoMatriz = ' '.join(map(str, row)) + '\n' #esta linea mapea cada elemento de la matriz y lo convierte en str, para despues añadirlo a la variable
            texto.insert(tk.END, textoMatriz)

        texto.config(state=tk.DISABLED) #deshabilita la edicion del widget
        
    def verInfo(self):
        infoWindow = Toplevel(self.root)
        infoWindow.title("Info")
        infoWindow.geometry("200x100")
        tk.Label(infoWindow, text=f"Nombre: {self.username}").pack(padx=10, pady=10)
        tk.Label(infoWindow, text=f"Estado: {self.estado}").pack(padx=10, pady=10)
        
    def setForma(self, forma):
        self.formaActual = forma

    def right_click(self, event):
        if self.formaActual == "cuadrado":
            self.dibujarCuadrado(event.x, event.y)
        elif self.formaActual == "circulo":
            self.dibujarCirculo(event.x, event.y)

    def dibujarCuadrado(self, x, y):
        center_x, center_y = x // self.pixelSize, y // self.pixelSize
        size = self.gridSize // 12  
        color_num = self.colorActual
        for dy in range(-size, size):
            for dx in range(-size, size):
                nx, ny = center_x + dx, center_y + dy
                if 0 <= nx < self.gridSize and 0 <= ny < self.gridSize:
                    self.matrix[ny, nx] = color_num
        self.updateCanvas()

    def dibujarCirculo(self, x, y):
        center_x, center_y = x // self.pixelSize, y // self.pixelSize
        radius = self.gridSize // 12  
        color_num = self.colorActual
        for ny in range(self.gridSize):
            for nx in range(self.gridSize):
                if (nx - center_x) ** 2 + (ny - center_y) ** 2 <= radius ** 2:
                    self.matrix[ny, nx] = color_num
        self.updateCanvas()

def empezar(user, previa):
    username = user
    estado = "creado"
    previa.destroy()
        
    root = tk.Tk()
    app = PaintApp(root,username,estado)
    root.mainloop()
    
previa = tk.Tk()
previa.title("Enter your name")
tk.Label(previa, text="Name:").pack(padx=10, pady=10)
entry = tk.Entry(previa)
entry.pack(padx=10, pady=10)
tk.Button(previa, text="Aceptar", command=lambda: empezar(entry.get(), previa)).pack(pady=10)
previa.mainloop()
