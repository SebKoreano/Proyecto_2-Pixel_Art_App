import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np

class PaintxelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Paintxel")
        self.pixel_size = 5
        self.grid_size = 100
        self.canvas_size = 500
        self.matrix = np.zeros((self.grid_size, self.grid_size), dtype=int)
        self.canvas = tk.Canvas(self.root, width=self.canvas_size, height=self.canvas_size, bg="white")
        self.canvas.pack()
        self.create_menu()
        self.current_color = 1
        self.rectangles = {}
        self.draw_initial_grid()
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<Button-1>", self.paint)

    def create_menu(self):
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Cargar imagen", command=self.load_image)
        filemenu.add_command(label="Guardar imagen", command=self.save_image)
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
        editmenu.add_command(label="ASCII-Art", command=self.ascii_art)
        menubar.add_cascade(label="Editar", menu=editmenu)

        self.root.config(menu=menubar)

    def draw_initial_grid(self):
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                rect = self.canvas.create_rectangle(
                    x * self.pixel_size, y * self.pixel_size,
                    (x + 1) * self.pixel_size, (y + 1) * self.pixel_size,
                    fill="white", outline="gray"
                )
                self.rectangles[(x, y)] = rect

    def paint(self, event):
        x, y = event.x // self.pixel_size, event.y // self.pixel_size
        if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
            self.matrix[y, x] = self.current_color
            color = f'#{self.current_color * 255 // 9:02x}{self.current_color * 255 // 9:02x}{self.current_color * 255 // 9:02x}'
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

    def update_canvas(self):
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                color = f'#{self.matrix[y, x] * 255 // 9:02x}{self.matrix[y, x] * 255 // 9:02x}{self.matrix[y, x] * 255 // 9:02x}'
                self.canvas.itemconfig(self.rectangles[(x, y)], fill=color)

    def zoom_in(self):
        pass  # Implementar funcionalidad de zoom

    def zoom_out(self):
        pass  # Implementar funcionalidad de zoom

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
        self.matrix = np.where(self.matrix < 5, 1, 9)
        self.update_canvas()

    def negative(self):
        self.matrix = 9 - self.matrix
        self.update_canvas()

    def ascii_art(self):
        ascii_chars = ' .:-=+*%@'
        result = ""
        for row in self.matrix:
            result += ''.join(ascii_chars[val] for val in row) + '\n'
        messagebox.showinfo("ASCII Art", result)

if __name__ == "__main__":
    root = tk.Tk()
    app = PaintxelApp(root)
    root.mainloop()
