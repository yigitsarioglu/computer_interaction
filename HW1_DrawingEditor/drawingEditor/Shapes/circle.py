from shape import Shape


class Circle(Shape):
    def draw(self):
        """
        Draw a circle shape.
        """
        self.shape = self.canvas.create_oval(
            self.start_x, self.start_y, self.end_x, self.end_y, outline=self.color
        )
