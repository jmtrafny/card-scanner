# region_selector.py
import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path

class RegionSelector:
    def __init__(self, image_paths):
        self.image_paths = image_paths
        self.index = 0
        self.coords = None
        self.start_x = None
        self.start_y = None
        self.rect_coords = None  # Store rectangle coordinates explicitly
        self.dragging_handle = None
        self.dragging_box = False

        self.root = tk.Toplevel()
        self.root.title("Select Card Name Region")

        self.canvas = tk.Canvas(self.root)
        self.canvas.grid(row=0, column=0, columnspan=3)

        self.btn_prev = tk.Button(self.root, text="<", command=self.show_prev_image)
        self.btn_prev.grid(row=1, column=0, sticky="w")

        self.btn_ok = tk.Button(self.root, text="OK", command=self.confirm_selection)
        self.btn_ok.grid(row=1, column=1)

        self.btn_next = tk.Button(self.root, text=">", command=self.show_next_image)
        self.btn_next.grid(row=1, column=2, sticky="e")

        self.rect = None
        self.handles = []

        self.load_image()
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        self.root.wait_window()

    def load_image(self):
        image_path = self.image_paths[self.index]
        self.img = Image.open(image_path)
        self.tk_img = ImageTk.PhotoImage(self.img)
        self.canvas.delete("all")  # Clear everything on canvas
        self.canvas.config(width=self.tk_img.width(), height=self.tk_img.height())
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)

        # Recreate the bounding box if previously defined
        if self.rect_coords:
            x1, y1, x2, y2 = self.rect_coords
            self.rect = self.canvas.create_rectangle(x1, y1, x2, y2, outline='red')
            self.draw_handles(x1, y1, x2, y2)

        self.update_buttons()

    def show_prev_image(self):
        if self.index > 0:
            self.index -= 1
            self.load_image()

    def show_next_image(self):
        if self.index < len(self.image_paths) - 1:
            self.index += 1
            self.load_image()

    def update_buttons(self):
        self.btn_prev.config(state="normal" if self.index > 0 else "disabled")
        self.btn_next.config(state="normal" if self.index < len(self.image_paths) - 1 else "disabled")

    def on_click(self, event):
        if event.widget != self.canvas:
            return
        self.start_x, self.start_y = event.x, event.y

        # Check if clicking on a handle
        for idx, handle in enumerate(self.handles):
            x1, y1, x2, y2 = self.canvas.coords(handle)
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                self.dragging_handle = idx
                return

        # Check if clicking inside the box
        if self.rect_coords:
            x1, y1, x2, y2 = self.rect_coords
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                self.dragging_box = True
                return

        # Start drawing a new box
        if self.rect:
            self.canvas.delete(self.rect)
            for handle in self.handles:
                self.canvas.delete(handle)
            self.handles.clear()
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red')

    def on_drag(self, event):
        if event.widget != self.canvas:
            return

        if self.dragging_handle is not None and self.rect_coords:
            coords = list(self.rect_coords)
            if self.dragging_handle == 0:
                coords[0], coords[1] = event.x, event.y  # Top-left
            elif self.dragging_handle == 1:
                coords[2], coords[1] = event.x, event.y  # Top-right
            elif self.dragging_handle == 2:
                coords[2], coords[3] = event.x, event.y  # Bottom-right
            elif self.dragging_handle == 3:
                coords[0], coords[3] = event.x, event.y  # Bottom-left

            self.rect_coords = tuple(coords)
            self.canvas.coords(self.rect, *coords)
            for handle in self.handles:
                self.canvas.delete(handle)
            self.draw_handles(*coords)
            return

        if self.dragging_box and self.rect_coords:
            dx = event.x - self.start_x
            dy = event.y - self.start_y
            self.start_x, self.start_y = event.x, event.y

            x1, y1, x2, y2 = self.rect_coords
            self.rect_coords = (x1 + dx, y1 + dy, x2 + dx, y2 + dy)
            self.canvas.coords(self.rect, *self.rect_coords)
            for handle in self.handles:
                self.canvas.delete(handle)
            self.draw_handles(*self.rect_coords)
            return

        if self.rect:
            self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)
            self.rect_coords = (int(self.start_x), int(self.start_y), int(event.x), int(event.y))
            for handle in self.handles:
                self.canvas.delete(handle)
            self.draw_handles(self.start_x, self.start_y, event.x, event.y)

    def on_release(self, event):
        self.dragging_handle = None
        self.dragging_box = False

    def draw_handles(self, x1, y1, x2, y2):
        size = 3  # Smaller handles
        corners = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]
        self.handles.clear()
        for x, y in corners:
            handle = self.canvas.create_oval(x - size, y - size, x + size, y + size, fill='blue')
            self.handles.append(handle)

    def confirm_selection(self):
        if self.rect_coords:
            self.coords = self.rect_coords
        self.root.destroy()
