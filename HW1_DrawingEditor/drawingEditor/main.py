import tkinter as tk
from drawingEditor import DrawingEditor


root = tk.Tk()
editor = DrawingEditor(root)

shape_type_label = tk.Label(root, text="Select Shape:")
shape_type_label.pack()

editor.shape_type = tk.StringVar(root)
editor.shape_type.set("Rectangle")

shape_types = ["Rectangle", "Square", "Circle", "Line"]
shape_menu = tk.OptionMenu(root, editor.shape_type, *shape_types)
shape_menu.pack()

color_button = tk.Button(root, text="Pick Color", command=editor.pick_color)
color_button.pack()

delete_button = tk.Button(root, text="Clear", command=editor.delete_all)
delete_button.pack()

root.mainloop()
