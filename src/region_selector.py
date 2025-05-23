# region_selector.py (updated with fuzzy match dropdown)
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from pathlib import Path

FUZZY_OPTIONS = ["No Fuzzy Matching", "Pokemon Name", "YuGiOh Card Name", "MTG Card Name"]

class RegionSelector:
    def __init__(self, image_paths):
        self.image_paths = image_paths
        self.index = 0
        self.capture_boxes = []
        self.current_box_index = None
        self.selected_box_index = tk.IntVar(value=0)

        self.start_x = None
        self.start_y = None
        self.zoom = 1.0

        self.root = tk.Toplevel()
        self.root.title("Select OCR Regions")
        self.root.geometry("800x600")

        # Layout: top bar
        nav_frame = tk.Frame(self.root)
        nav_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.btn_prev = tk.Button(nav_frame, text="<", command=self.show_prev_image)
        self.btn_prev.pack(side="left")
        self.btn_next = tk.Button(nav_frame, text=">", command=self.show_next_image)
        self.btn_next.pack(side="left")

        # Canvas area
        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.grid(row=1, column=0, sticky="nsew")
        self.canvas = tk.Canvas(self.canvas_frame, bg="gray")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.h_scroll = tk.Scrollbar(self.canvas_frame, orient="horizontal", command=self.canvas.xview)
        self.v_scroll = tk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=self.h_scroll.set, yscrollcommand=self.v_scroll.set)
        self.v_scroll.grid(row=0, column=1, sticky="ns")
        self.h_scroll.grid(row=1, column=0, sticky="ew")
        self.canvas_frame.rowconfigure(0, weight=1)
        self.canvas_frame.columnconfigure(0, weight=1)

        # Capture box panel
        self.attr_frame = tk.Frame(self.root)
        self.attr_frame.grid(row=1, column=1, sticky="nsew")
        self.attr_frame.columnconfigure(0, weight=1)

        self.add_box_button = tk.Button(self.attr_frame, text="+ Add Capture Box", command=self.add_capture_box)
        self.add_box_button.pack(pady=(5, 10))

        self.instructions = tk.Label(self.attr_frame, justify="left", anchor="w", text=(
            "Mouse Controls:\n"
            "- Scroll: vertical scroll\n"
            "- Shift + Scroll: horizontal scroll\n"
            "- Ctrl + Scroll: zoom in/out\n\n"
            "Note: First capture box is used for file name"
        ))
        self.instructions.pack(pady=(10, 5), padx=5, anchor="w")

        self.confirm_button = tk.Button(self.root, text="OK", command=self.confirm_selection)
        self.confirm_button.grid(row=2, column=1, sticky="e", pady=10, padx=10)

        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=3)
        self.root.columnconfigure(1, weight=1)

        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)

        self.load_image()
        self.root.wait_window()

    def add_capture_box(self):
        idx = len(self.capture_boxes)
        box = {"name": tk.StringVar(), "coords": None, "fuzzy_type": tk.StringVar(value=FUZZY_OPTIONS[0])}

        frame = tk.Frame(self.attr_frame)
        radio = tk.Radiobutton(frame, variable=self.selected_box_index, value=idx, command=lambda i=idx: self.set_current_box(i))
        name_hint = " (used for filename)" if idx == 0 else ""
        entry = tk.Entry(frame, textvariable=box["name"], width=15)
        coord_label = tk.Label(frame, text="[x:0 y:0 w:0 h:0]", anchor="w")
        fuzzy_dropdown = ttk.Combobox(frame, values=FUZZY_OPTIONS, textvariable=box["fuzzy_type"], state="readonly", width=20)

        frame.pack(fill="x", pady=2, padx=5, anchor="w")
        radio.pack(side="left")
        entry.insert(0, f"Attribute {idx+1}{name_hint}")
        entry.pack(side="left", padx=(5, 5))
        coord_label.pack(side="left")
        fuzzy_dropdown.pack(side="left", padx=5)

        box.update({"radio": radio, "entry": entry, "label": coord_label, "dropdown": fuzzy_dropdown})
        self.capture_boxes.append(box)
        self.set_current_box(idx)

    def set_current_box(self, index=None):
        if index is not None:
            self.selected_box_index.set(index)
        self.current_box_index = self.selected_box_index.get()
        self.load_image()

    def show_prev_image(self):
        if self.index > 0:
            self.index -= 1
            self.load_image()

    def show_next_image(self):
        if self.index < len(self.image_paths) - 1:
            self.index += 1
            self.load_image()

    def load_image(self):
        image_path = self.image_paths[self.index]
        self.img = Image.open(image_path)
        self.zoomed_img = self.img.resize((int(self.img.width * self.zoom), int(self.img.height * self.zoom)))
        self.tk_img = ImageTk.PhotoImage(self.zoomed_img)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        for i, box in enumerate(self.capture_boxes):
            if box["coords"]:
                x1, y1, x2, y2 = [int(c * self.zoom) for c in box["coords"]]
                color = 'blue' if i == self.selected_box_index.get() else 'red'
                self.canvas.create_rectangle(x1, y1, x2, y2, outline=color, width=2 if color == 'blue' else 1)

    def on_click(self, event):
        if self.current_box_index is None:
            return
        self.start_x = self.canvas.canvasx(event.x) / self.zoom
        self.start_y = self.canvas.canvasy(event.y) / self.zoom

    def on_drag(self, event):
        if self.current_box_index is None:
            return
        end_x = self.canvas.canvasx(event.x) / self.zoom
        end_y = self.canvas.canvasy(event.y) / self.zoom
        x1, y1 = int(self.start_x), int(self.start_y)
        x2, y2 = int(end_x), int(end_y)
        coords = (x1, y1, x2, y2)
        w, h = abs(x2 - x1), abs(y2 - y1)
        self.capture_boxes[self.current_box_index]["coords"] = coords
        self.capture_boxes[self.current_box_index]["label"].config(text=f"[x:{x1} y:{y1} w:{w} h:{h}]")
        self.load_image()

    def on_release(self, event):
        pass

    def on_mouse_wheel(self, event):
        if event.state & 0x0004:  # Ctrl = zoom
            if event.delta > 0:
                self.zoom = min(3.0, self.zoom * 1.1)
            else:
                self.zoom = max(0.3, self.zoom / 1.1)
            self.load_image()
        elif event.state & 0x0001:  # Shift = horizontal scroll
            self.canvas.xview_scroll(-1 * (event.delta // 120), "units")
        else:  # Normal = vertical scroll
            self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def confirm_selection(self):
        self.root.destroy()

    def get_capture_data(self):
        return [
            (box["name"].get(), box["coords"], box["fuzzy_type"].get())
            for box in self.capture_boxes if box["coords"]
        ]
