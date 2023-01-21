# Libraries
import tkinter as tk
from PIL import Image, ImageTk

# Project files
import util

app_width = 1440
app_height = 900

# width, height
target_image_size = (656, 410)

# 163px represents 100m
image_params = (163, 100)


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Land Classification")
        self.geometry(f"{app_width}x{app_height}")
        self.resizable(False, False)

        self.raw_image = util.load_image("images/image_1.png")

        self.raw_gui_image = util.load_image(
            "images/image_1.png", True, target_image_size
        )
        self.raw_image_label = tk.Label(self, image=self.raw_gui_image)
        self.raw_image_label.grid(row=0, column=0, columnspan=1, padx=16, pady=16)

        # Keyboard functions
        # Exit app with <Esc>
        self.bind("<Escape>", lambda evt: close_app_callback())
        # Open file dialog with o
        self.bind("<o>", lambda evt: select_file_callback())

        def close_app_callback():
            self.quit()

        def select_file_callback():
            file = tk.filedialog.askopenfilename(
                initialdir="images",
                title="Choose map image...",
            )

            new_image = util.load_image(file, True, target_image_size)
            self.raw_image_label.configure(image=new_image)
            self.raw_image_label.image = new_image


if __name__ == "__main__":
    app = App()
    app.mainloop()
