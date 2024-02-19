import tkinter as tk
from PIL import ImageGrab
from tkinter.simpledialog import askinteger

class MatrixNavigator:
    def __init__(self, master, rows, cols, cell_size):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.pointer_pos = [rows - 1, 0]  # Posición inicial en la esquina inferior izquierda
        self.direction = "up"  # Dirección inicial hacia arriba
        self.path = set()
        self.points = []  # Lista para almacenar los puntos adicionales
        self.cell_size = cell_size
        self.create_canvas()
        self.create_widgets()  # Se llama a un nuevo método para crear widgets
        self.bind_keys()
        self.blink_pointer()
        self.update_title()

    def create_canvas(self):
        self.canvas = tk.Canvas(self.master, width=self.cols*self.cell_size, height=self.rows*self.cell_size, bg="#D9D9D9")
        self.canvas.pack()

    def create_widgets(self):
        # Se crea el botón "+" y se asocia a la función add_point
        self.add_button = tk.Button(self.master, text="+", command=self.add_point)
        self.add_button.pack(side=tk.LEFT)  # Se coloca a la izquierda

        # Se crea el botón "Photo" y se asocia a la función save_screenshot
        self.photo_button = tk.Button(self.master, text="Photo", command=self.save_screenshot)
        self.photo_button.pack(side=tk.LEFT)  # Se coloca a la izquierda

    def update_pointer(self):
        self.canvas.delete("all")
        for i in range(self.rows):
            for j in range(self.cols):
                x0, y0 = j * self.cell_size, i * self.cell_size
                x1, y1 = x0 + self.cell_size, y0 + self.cell_size
                if (i, j) in self.path:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="#0094FF", outline="")
                elif i == self.pointer_pos[0] and j == self.pointer_pos[1]:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="#C60000", outline="")
                    self.path.add((i, j))
        for point in self.points:  # Graficar puntos adicionales
            x, y = point
            x0, y0 = x * self.cell_size, y * self.cell_size
            x1, y1 = x0 + self.cell_size, y0 + self.cell_size
            self.canvas.create_rectangle(x0, y0, x1, y1, fill="#4BC12A", outline="")

    def move_pointer_forward(self):
        next_pos = self.get_next_position_forward()
        if self.is_valid_position(next_pos):
            self.pointer_pos = next_pos
            self.update_pointer()
            self.update_title()

    def move_pointer_backward(self):
        next_pos = self.get_next_position_backward()
        if self.is_valid_position(next_pos):
            self.pointer_pos = next_pos
            self.update_pointer()
            self.update_title()

    def get_next_position_forward(self):
        if self.direction == "up":
            return [self.pointer_pos[0] - 1, self.pointer_pos[1]]
        elif self.direction == "down":
            return [self.pointer_pos[0] + 1, self.pointer_pos[1]]
        elif self.direction == "left":
            return [self.pointer_pos[0], self.pointer_pos[1] - 1]
        elif self.direction == "right":
            return [self.pointer_pos[0], self.pointer_pos[1] + 1]

    def get_next_position_backward(self):
        if self.direction == "up":
            return [self.pointer_pos[0] + 1, self.pointer_pos[1]]
        elif self.direction == "down":
            return [self.pointer_pos[0] - 1, self.pointer_pos[1]]
        elif self.direction == "left":
            return [self.pointer_pos[0], self.pointer_pos[1] + 1]
        elif self.direction == "right":
            return [self.pointer_pos[0], self.pointer_pos[1] - 1]

    def is_valid_position(self, pos):
        return 0 <= pos[0] < self.rows and 0 <= pos[1] < self.cols

    def turn_right(self):
        if self.direction == "up":
            self.direction = "right"
        elif self.direction == "right":
            self.direction = "down"
        elif self.direction == "down":
            self.direction = "left"
        elif self.direction == "left":
            self.direction = "up"
        self.update_title()

    def turn_left(self):
        if self.direction == "up":
            self.direction = "left"
        elif self.direction == "left":
            self.direction = "down"
        elif self.direction == "down":
            self.direction = "right"
        elif self.direction == "right":
            self.direction = "up"
        self.update_title()

    def blink_pointer(self):
        current_color = "#C60000" if (self.pointer_pos[0], self.pointer_pos[1]) not in self.path else "#D9D9D9"
        self.update_pointer()
        self.master.after(500, self.blink_pointer)

    def bind_keys(self):
        self.master.bind("<Up>", lambda event: self.move_pointer_forward())
        self.master.bind("<Down>", lambda event: self.move_pointer_backward())
        self.master.bind("<Right>", lambda event: self.turn_right())
        self.master.bind("<Left>", lambda event: self.turn_left())
        self.master.bind("<Control-asterisk>", self.save_screenshot)  # Bind Control + * key to save screenshot

    def save_screenshot(self, event=None):
        x0 = self.master.winfo_rootx()
        y0 = self.master.winfo_rooty()
        x1 = x0 + self.master.winfo_width()
        y1 = y0 + self.master.winfo_height()
        ImageGrab.grab().crop((x0, y0, x1, y1)).save("screenshot.png")
        print("Se guardó una captura de pantalla con el nombre: screenshot.png")

    def update_title(self):
        direction_symbol = {"up": "↑", "down": "↓", "right": "→", "left": "←"}
        direction_text = direction_symbol[self.direction]
        self.master.title("Mapa del recorrido realizado: Posición X: {} Y: {} Dirección: {}".format(self.pointer_pos[1], self.pointer_pos[0], direction_text))

    def add_point(self, event=None):
        x = askinteger("Coordenada X", "Ingrese la coordenada X del punto:")
        y = askinteger("Coordenada Y", "Ingrese la coordenada Y del punto:")
        if x is not None and y is not None:
            self.points.append([x, y])
            self.update_pointer()

def main():
    root = tk.Tk()
    root.geometry("1200x800")  # Tamaño de la ventana
    navigator = MatrixNavigator(root, 80, 120, 9)  # Tamaño de la celda
    root.mainloop()

if __name__ == "__main__":
    main()
