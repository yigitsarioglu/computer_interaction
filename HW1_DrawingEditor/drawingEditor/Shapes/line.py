from shape import Shape


class Line(Shape):
    def draw(self):
        """
        Draw a line shape.
        """
        self.shape = self.canvas.create_line(
            self.start_x, self.start_y, self.end_x, self.end_y, fill=self.color
        )
