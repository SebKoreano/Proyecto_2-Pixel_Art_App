import pygame
import numpy as np

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
screen_size = 600
pixel_size = 6
grid_size = screen_size // pixel_size
screen = pygame.display.set_mode((screen_size + 200, screen_size))  # Añadimos espacio para los botones
pygame.display.set_caption("Pixel Art Editor")

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [BLACK, WHITE]  # Puedes agregar más colores aquí

# Matriz de imagen (100x100)
image_matrix = np.zeros((grid_size, grid_size), dtype=int)

# Función para dibujar la cuadrícula
def draw_grid():
    for x in range(0, screen_size, pixel_size):
        for y in range(0, screen_size, pixel_size):
            rect = pygame.Rect(x, y, pixel_size, pixel_size)
            pygame.draw.rect(screen, COLORS[image_matrix[y // pixel_size][x // pixel_size]], rect)
            pygame.draw.rect(screen, BLACK, rect, 1)

# Funciones de edición
def zoom_in():
    global pixel_size
    pixel_size *= 2

def zoom_out():
    global pixel_size
    if pixel_size > 1:
        pixel_size //= 2

def rotate_right():
    global image_matrix
    image_matrix = np.rot90(image_matrix, -1)

def rotate_left():
    global image_matrix
    image_matrix = np.rot90(image_matrix, 1)

def horizontal_flip():
    global image_matrix
    image_matrix = np.fliplr(image_matrix)

def vertical_flip():
    global image_matrix
    image_matrix = np.flipud(image_matrix)

def high_contrast():
    global image_matrix
    image_matrix = np.where(image_matrix <= 4, 1, 9)

def negative():
    global image_matrix
    image_matrix = 9 - image_matrix

def ascii_art():
    ascii_chars = ['.', ':', '-', '=', '¡', '&', '$', '%', '@']
    ascii_image = []
    for row in image_matrix:
        ascii_row = [ascii_chars[pixel] for pixel in row]
        ascii_image.append(''.join(ascii_row))
    for line in ascii_image:
        print(line)

# Funciones de manejo de archivos
def save_image(filename):
    np.savetxt(filename, image_matrix, fmt='%d')

def load_image(filename):
    global image_matrix
    image_matrix = np.loadtxt(filename, dtype=int)

# Clase para botones
class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (200, 200, 200)
        self.text = text
        self.action = action

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.SysFont(None, 24)
        text_surf = font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def click(self):
        self.action()

# Crear botones
buttons = [
    Button(screen_size + 20, 20, 160, 40, 'Zoom In', zoom_in),
    Button(screen_size + 20, 70, 160, 40, 'Zoom Out', zoom_out),
    Button(screen_size + 20, 120, 160, 40, 'Rotate Right', rotate_right),
    Button(screen_size + 20, 170, 160, 40, 'Rotate Left', rotate_left),
    Button(screen_size + 20, 220, 160, 40, 'Flip Horizontal', horizontal_flip),
    Button(screen_size + 20, 270, 160, 40, 'Flip Vertical', vertical_flip),
    Button(screen_size + 20, 320, 160, 40, 'High Contrast', high_contrast),
    Button(screen_size + 20, 370, 160, 40, 'Negative', negative),
    Button(screen_size + 20, 420, 160, 40, 'ASCII Art', ascii_art),
    Button(screen_size + 20, 470, 160, 40, 'Save Image', lambda: save_image('saved_image.txt')),
    Button(screen_size + 20, 520, 160, 40, 'Load Image', lambda: load_image('saved_image.txt')),
]

# Loop principal con funcionalidades añadidas
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if x < screen_size:
                grid_x, grid_y = x // pixel_size, y // pixel_size
                image_matrix[grid_y][grid_x] = (image_matrix[grid_y][grid_x] + 1) % len(COLORS)
            else:
                for button in buttons:
                    if button.rect.collidepoint(x, y):
                        button.click()

    screen.fill(WHITE)
    draw_grid()
    for button in buttons:
        button.draw()
    pygame.display.flip()

pygame.quit()
