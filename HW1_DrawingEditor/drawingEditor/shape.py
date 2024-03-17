
class Shape:
    def __init__(self, canvas, start_x, start_y, end_x, end_y, color="black"):
        """
        Initialize a shape.
        """
        self.canvas = canvas
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.color = color
        self.shape = None

    def draw(self):
        pass

    def move(self, dx, dy):
        """
        Move the shape.
        """
        self.canvas.move(self.shape, dx, dy)
        self.start_x += dx
        self.start_y += dy
        self.end_x += dx
        self.end_y += dy

    def delete(self):
        """
        Delete the shape.
        """
        self.canvas.delete(self.shape)
