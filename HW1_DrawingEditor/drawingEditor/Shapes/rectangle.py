from shape import Shape


class Rectangle(Shape):
    def draw(self):
        """
        Draw a rectangle shape.
        """
        self.shape = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.end_x, self.end_y, outline=self.color
        )
