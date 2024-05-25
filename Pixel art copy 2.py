import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel, Text
import numpy as np
import pickle

class PaintxelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Paintxel")
        self.pixel_size = 10
        self.min_pixel_size = 1
        self.max_pixel_size = 50
        self.grid_size = 50
        self.canvas_size = self.pixel_size * self.grid_size
        self.matrix = np.zeros((self.grid_size, self.grid_size), dtype=int)
        self.canvas = tk.Canvas(self.root, width=self.canvas_size, height=self.canvas_size, bg="white")
        self.canvas.pack()
        self.colors = [
            "#000000", "#FF0000", "#00FF00", "#0000FF",
            "#FFFF00", "#FF00FF", "#00FFFF", "#FFFFFF", "#808080", "#572364"
        ]
        self.ascii_chars = [' ','.', ':', '-', '=', '¡', '&', '$', '%', '@']
        self.current_color = 0  # Initialize to the first color (black)
        self.rectangles = {}
        self.draw_initial_grid()
        self.create_menu()
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<Button-1>", self.paint)

    def create_menu(self):
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Cargar imagen", command=self.load_image)
        filemenu.add_command(label="Guardar imagen", command=self.save_image)
        filemenu.add_command(label="Guardar con pickle", command=self.save_image_pickle)
        filemenu.add_command(label="Cargar con pickle", command=self.load_image_pickle)
        filemenu.add_command(label="Cerrar imagen", command=self.clear_image)
        filemenu.add_separator()
        filemenu.add_command(label="Salir", command=self.root.quit)
        menubar.add_cascade(label="Archivo", menu=filemenu)

        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label="Zoom in", command=self.zoom_in)
        editmenu.add_command(label="Zoom out", command=self.zoom_out)
        editmenu.add_command(label="Rotar derecha", command=self.rotate_right)
        editmenu.add_command(label="Rotar izquierda", command=self.rotate_left)
        editmenu.add_command(label="Reflejo horizontal", command=self.horizontal_reflection)
        editmenu.add_command(label="Reflejo vertical", command=self.vertical_reflection)
        editmenu.add_command(label="Alto contraste", command=self.high_contrast)
        editmenu.add_command(label="Negativo", command=self.negative)
        menubar.add_cascade(label="Editar", menu=editmenu)

        viewmenu = tk.Menu(menubar, tearoff=0)
        viewmenu.add_command(label="ASCII-Art", command=self.ascii_art)
        viewmenu.add_command(label="Ver matriz numérica", command=self.view_numeric_matrix)
        menubar.add_cascade(label="Ver", menu=viewmenu)

        colormenu = tk.Menu(menubar, tearoff=0)
        for i, color in enumerate(self.colors):
            colormenu.add_command(label=f"Color {i+1}", command=lambda c=i: self.set_color(c))
        menubar.add_cascade(label="Colores", menu=colormenu)

        self.root.config(menu=menubar)

    def draw_initial_grid(self):
        self.canvas.delete("all")
        self.rectangles.clear()
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                rect = self.canvas.create_rectangle(
                    x * self.pixel_size, y * self.pixel_size,
                    (x + 1) * self.pixel_size, (y + 1) * self.pixel_size,
                    fill=self.colors[self.matrix[y, x]], outline="gray"
                )
                self.rectangles[(x, y)] = rect

    def paint(self, event):
        x, y = event.x // self.pixel_size, event.y // self.pixel_size
        if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
            self.matrix[y, x] = self.current_color
            color = self.colors[self.current_color]
            self.canvas.itemconfig(self.rectangles[(x, y)], fill=color)

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    for y, line in enumerate(file):
                        self.matrix[y] = list(map(int, line.strip().split()))
                self.update_canvas()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    for row in self.matrix:
                        file.write(" ".join(map(str, row)) + "\n")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def save_image_pickle(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pkl")
        if file_path:
            try:
                with open(file_path, 'wb') as file:
                    pickle.dump(self.matrix, file)
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def load_image_pickle(self):
        file_path = filedialog.askopenfilename(filetypes=[("Pickle files", "*.pkl")])
        if file_path:
            try:
                with open(file_path, 'rb') as file:
                    self.matrix = pickle.load(file)
                self.update_canvas()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def clear_image(self):
        # Clear the matrix and update the canvas
        self.matrix = np.zeros((self.grid_size, self.grid_size), dtype=int)
        self.update_canvas()

    def update_canvas(self):
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                color = self.colors[self.matrix[y, x]]
                self.canvas.itemconfig(self.rectangles[(x, y)], fill=color)

    def set_color(self, color_index):
        self.current_color = color_index

    def zoom_in(self):
        if self.pixel_size < self.max_pixel_size:
            self.pixel_size += 10
            self.draw_initial_grid()

    def zoom_out(self):
        if self.pixel_size > self.min_pixel_size:
            self.pixel_size -= 10
            self.draw_initial_grid()

    def rotate_right(self):
        self.matrix = np.rot90(self.matrix, -1)
        self.update_canvas()

    def rotate_left(self):
        self.matrix = np.rot90(self.matrix)
        self.update_canvas()

    def horizontal_reflection(self):
        self.matrix = np.flip(self.matrix, axis=1)
        self.update_canvas()

    def vertical_reflection(self):
        self.matrix = np.flip(self.matrix, axis=0)
        self.update_canvas()

    def high_contrast(self):
        # Convert all values between 0 and 4 to 1, and values between 5 and 9 to 9
        self.matrix = np.where(self.matrix <= 4, 1, 9)
        self.update_canvas()

    def negative(self):
        # Invert the values in the matrix: 9 -> 0, 8 -> 1, ..., 1 -> 8, 0 -> 9
        self.matrix = 9 - self.matrix
        self.update_canvas()

    def ascii_art(self):
        ascii_window = Toplevel(self.root)
        ascii_window.title("ASCII Art")
        ascii_window.geometry("700x710")
        text_widget = Text(ascii_window, width=100, height=100, font=("Courier", 8))
        text_widget.pack(expand=True, fill=tk.BOTH)
        text_widget.config(state=tk.NORMAL)

        for row in self.matrix:
            ascii_row = ' '.join(self.ascii_chars[val] for val in row) + '\n'
            text_widget.insert(tk.END, ascii_row)

        text_widget.config(state=tk.DISABLED)

    def view_numeric_matrix(self):
        numeric_window = Toplevel(self.root)
        numeric_window.title("Matriz Numérica")
        numeric_window.geometry("700x710")
        text_widget = Text(numeric_window, width=100, height=100, font=("Courier", 8))
        text_widget.pack(expand=True, fill=tk.BOTH)
        text_widget.config(state=tk.NORMAL)

        for row in self.matrix:
            numeric_row = ' '.join(map(str, row)) + '\n'
            text_widget.insert(tk.END, numeric_row)

        text_widget.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = PaintxelApp(root)
    root.mainloop()
