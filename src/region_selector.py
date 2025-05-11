# region_selector.py
import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path

class RegionSelector:
    def __init__(self, image_paths):
        self.image_paths = image_paths
        self.index = 0
        self.capture_boxes = []  # list of dicts: {"name": str, "coords": tuple, "radio": tk.Radiobutton, "entry": tk.Entry}
        self.current_box_index = None

        self.start_x = None
        self.start_y = None

        self.root = tk.Toplevel()
        self.root.title("Select OCR Regions")

        self.btn_prev = tk.Button(self.root, text="<", command=self.show_prev_image)
        self.btn_prev.grid(row=0, column=0, sticky="w")

        self.btn_ok = tk.Button(self.root, text="OK", command=self.confirm_selection)
        self.btn_ok.grid(row=0, column=1)

        self.btn_next = tk.Button(self.root, text=">", command=self.show_next_image)
        self.btn_next.grid(row=0, column=2, sticky="e")

        self.add_box_button = tk.Button(self.root, text="+ Add Capture Box", command=self.add_capture_box)
        self.add_box_button.grid(row=0, column=3, padx=5)
        self.selected_box_index = tk.IntVar(value=0)

        self.attr_frame = tk.Frame(self.root)
        self.attr_frame.grid(row=1, column=0, columnspan=4, sticky="ew")

        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.grid(row=2, column=0, columnspan=4, sticky="nsew")
        self.root.rowconfigure(2, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(self.canvas_frame, bg="gray")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.h_scroll = tk.Scrollbar(self.canvas_frame, orient="horizontal", command=self.canvas.xview)
        self.v_scroll = tk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=self.h_scroll.set, yscrollcommand=self.v_scroll.set)
        self.v_scroll.grid(row=0, column=1, sticky="ns")
        self.h_scroll.grid(row=1, column=0, sticky="ew")
        self.canvas_frame.rowconfigure(0, weight=1)
        self.canvas_frame.columnconfigure(0, weight=1)

        self.load_image()
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        self.root.wait_window()

    def add_capture_box(self):
        idx = len(self.capture_boxes)
        box = {"name": tk.StringVar(), "coords": None}

        frame = tk.Frame(self.attr_frame)
        radio = tk.Radiobutton(
            frame,
            variable=self.selected_box_index,  # ✅ shared across all radios
            value=idx,
            command=lambda i=idx: self.set_current_box(i)
        )
        entry = tk.Entry(frame, textvariable=box["name"], width=15)
        coord_label = tk.Label(frame, text="(0,0,0,0)")

        frame.grid(row=idx, column=0, sticky="w")
        radio.pack(side="left")
        entry.pack(side="left", padx=(5, 5))
        coord_label.pack(side="left")

        box.update({"radio": radio, "entry": entry, "label": coord_label})
        self.capture_boxes.append(box)
        self.set_current_box(idx)

    def set_current_box(self, index=None):
        if index is not None:
            self.selected_box_index.set(index)
        self.current_box_index = self.selected_box_index.get()

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
        self.tk_img = ImageTk.PhotoImage(self.img)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        for box in self.capture_boxes:
            if box["coords"]:
                self.canvas.create_rectangle(*box["coords"], outline='red')

    def on_click(self, event):
        if self.current_box_index is None:
            return
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)

    def on_drag(self, event):
        if self.current_box_index is None:
            return
        end_x = self.canvas.canvasx(event.x)
        end_y = self.canvas.canvasy(event.y)
        coords = (int(self.start_x), int(self.start_y), int(end_x), int(end_y))
        self.capture_boxes[self.current_box_index]["coords"] = coords
        self.capture_boxes[self.current_box_index]["label"].config(text=str(coords))
        self.load_image()

    def on_release(self, event):
        pass

    def confirm_selection(self):
        self.root.destroy()

    def get_capture_data(self):
        return [(box["name"].get(), box["coords"]) for box in self.capture_boxes if box["coords"]]
