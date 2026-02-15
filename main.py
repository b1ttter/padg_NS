from tkinter import Tk
from padg_lib.view import MapView
from padg_lib.controller import MapController


if __name__ == "__main__":
    root = Tk()
    view = MapView(root)
    controller = MapController(root, view)
    root.mainloop()