from shape import Shape


class Square(Shape):
    def draw(self):
        """
        Draw a square shape.
        """
        size = min(abs(self.end_x - self.start_x), abs(self.end_y - self.start_y))
        if self.end_x < self.start_x:
            self.end_x = self.start_x - size
        else:
            self.end_x = self.start_x + size
        if self.end_y < self.start_y:
            self.end_y = self.start_y - size
        else:
            self.end_y = self.start_y + size
        self.shape = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.end_x, self.end_y, outline=self.color
        )
