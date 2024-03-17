import tkinter as tk
import tkinter.colorchooser as colorchooser
from Shapes.rectangle import Rectangle
from Shapes.line import Line
from Shapes.square import Square
from Shapes.circle import Circle


class DrawingEditor:
    def __init__(self, master):
        self.master = master
        self.master.title("Drawing Editor")

        self.canvas = tk.Canvas(master, width=800, height=600, bg="white")
        self.canvas.pack(expand=True, fill=tk.BOTH)

        self.shapes = []  # List to store drawn shapes
        self.current_shape = None  # Variable to hold the currently drawn shape
        self.start_x = None  # Variable to store initial x coordinate of drawing
        self.start_y = None  # Variable to store initial y coordinate of drawing
        self.color = "black"  # Default color

        # Binding mouse events to canvas
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.end_draw)
        self.canvas.bind("<Button-2>", self.delete_shape)
        self.canvas.bind("<Button-3>", self.start_move)
        self.canvas.bind("<B3-Motion>", self.move_shape)
        self.canvas.bind("<ButtonRelease-3>", self.end_move)

    def start_draw(self, event):
        """
        Start drawing a shape.
        """
        self.start_x = event.x
        self.start_y = event.y

    def draw(self, event):
        """
        Draw the shape based on mouse motion.
        """
        if self.current_shape:
            self.canvas.delete(self.current_shape.shape)

        x, y = event.x, event.y
        if self.start_x is not None and self.start_y is not None:
            if self.shape_type.get() == "Rectangle":
                self.current_shape = Rectangle(self.canvas, self.start_x, self.start_y, x, y, color=self.color)
            elif self.shape_type.get() == "Square":
                self.current_shape = Square(self.canvas, self.start_x, self.start_y, x, y, color=self.color)
            elif self.shape_type.get() == "Circle":
                self.current_shape = Circle(self.canvas, self.start_x, self.start_y, x, y, color=self.color)
            elif self.shape_type.get() == "Line":
                self.current_shape = Line(self.canvas, self.start_x, self.start_y, x, y, color=self.color)
            self.current_shape.draw()

    def end_draw(self, event):
        """
        Finish drawing a shape and add it to the list of shapes.
        """
        if self.current_shape:
            self.shapes.append(self.current_shape)
            self.current_shape = None
            self.start_x = None
            self.start_y = None

    def delete_shape(self, event):
        """
        Delete a shape.
        """
        shape = self.canvas.find_closest(event.x, event.y)
        if shape:
            self.canvas.delete(shape[0])

    def delete_all(self):
        """
        Delete all shapes.
        """
        for shape in self.canvas.find_all():
            self.canvas.delete(shape)

    def start_move(self, event):
        """
        Start moving a shape.
        """
        self.start_x = event.x
        self.start_y = event.y
        shape = self.canvas.find_closest(event.x, event.y)
        if shape:
            for s in self.shapes:
                if s.shape == shape[0]:
                    self.current_shape = s
                    break

    def move_shape(self, event):
        """
        Move a shape.
        """
        if self.current_shape:
            dx = event.x - self.start_x
            dy = event.y - self.start_y
            self.current_shape.move(dx, dy)
            self.start_x = event.x
            self.start_y = event.y

    def end_move(self, event):
        """
        End moving a shape.
        """
        self.current_shape = None

    def pick_color(self):
        """
        Open a colorpicker and set a color.
        """
        color = colorchooser.askcolor()
        if color[1]:
            self.color = color[1]

