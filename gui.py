# libraries
import tkinter.filedialog
import tkinter as tk
from tkinter import ttk

# processing fns
import util

# app width height
app_width = 1440
app_height = 900

# image width, height
target_image_size = (656, 410)
# 163px represents 100m
image_params = (163, 100)


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        def update_raw_callback():
            new_image = util.load_image(self._image, True, target_image_size)
            new_image = util.image_for_gui(new_image)

            self.raw_image_label.config(image=new_image)
            self.raw_image_label.image = new_image

        def update_processed_image():
            new_image = util.load_image(self._image, True, target_image_size)
            processed = util.process_image(new_image)
            processed = util.image_for_gui(processed)

            self.processed_image_label.config(image=processed)
            self.processed_image_label.image = processed

        def open_filedialog():
            selected_file = tk.filedialog.askopenfilename(
                initialdir="images",
                title="Choose map image...",
            )

            if selected_file:
                self._image = selected_file
                # update image on GUI
                update_raw_callback()
                update_processed_image()

        def update_slider(*_):
            # greenlh
            util.mask_green_l = (
                int(self.greenlh_slider.get()),
                util.mask_green_l[1],
                util.mask_green_l[2],
            )
            self.greenlh_label.config(text="Lower Hue: %d" % util.mask_green_l[0])
            # greenuh
            util.mask_green_u = (
                int(self.greenuh_slider.get()),
                util.mask_green_u[1],
                util.mask_green_u[2],
            )
            self.greenuh_label.config(text="Upper Hue: %d" % util.mask_green_u[0])

            # brownlh
            util.mask_brown_l = (
                int(self.brownlh_slider.get()),
                util.mask_brown_l[1],
                util.mask_brown_l[2],
            )
            self.brownlh_label.config(text="Lower Hue: %d" % util.mask_brown_l[0])
            # brownuh
            util.mask_brown_u = (
                int(self.brownuh_slider.get()),
                util.mask_brown_u[1],
                util.mask_brown_u[2],
            )
            self.brownuh_label.config(text="Upper Hue: %d" % util.mask_brown_u[0])

            # graylh
            util.mask_gray_l = (
                int(self.graylh_slider.get()),
                util.mask_gray_l[1],
                util.mask_gray_l[2],
            )
            self.graylh_label.config(text="Lower Hue: %d" % util.mask_gray_l[0])
            # grayuh
            util.mask_gray_u = (
                int(self.grayuh_slider.get()),
                util.mask_gray_u[1],
                util.mask_gray_u[2],
            )
            self.grayuh_label.config(text="Upper Hue: %d" % util.mask_gray_u[0])

            update_processed_image()

        self.title("Land Classification")
        self.geometry("{}x{}".format(app_width, app_height))
        self.resizable(False, False)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        # images frame
        self.images_frame = tk.Frame(
            self,
            width=(app_width / 2),
            height=app_height,
            padx=16,
            pady=16,
        )
        self.images_frame.grid_rowconfigure(1, weight=1)
        self.images_frame.grid(row=0, column=0)

        # program starts with image_1 loaded
        self._image = "images/image_1.png"

        self.raw_image = util.load_image(self._image)
        self.scaled_image = util.load_image(self._image, True, target_image_size)
        self.raw_gui_image = util.image_for_gui(self.scaled_image)
        self.processed_gui_image = util.image_for_gui(
            util.process_image(self.scaled_image)
        )

        self.raw_image_label = tk.Label(self.images_frame, image=self.raw_gui_image)
        self.raw_image_label.grid(row=0, column=0, pady=(0, 8))

        self.processed_image_label = tk.Label(
            self.images_frame, image=self.processed_gui_image
        )
        self.processed_image_label.grid(row=1, column=0, pady=(8, 0))

        # controls and output frames
        self.controls_frame = tk.Frame(
            self,
            width=(app_width / 2),
            height=app_height,
            padx=16,
            pady=16,
        )
        self.controls_frame.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.controls_frame.grid(row=0, column=1)

        # open filedialog
        self.open_filedialog = tk.Frame(
            self.controls_frame,
            width=(app_width / 2),
            height=(app_height / 4),
            padx=16,
            pady=16,
        )
        self.open_filedialog.grid_rowconfigure((0, 1), weight=1)
        self.open_filedialog.grid_columnconfigure((0, 1), weight=1)
        self.open_filedialog.grid(row=0, column=0)

        self.open_filedialog_label = ttk.Label(
            self.open_filedialog, text="Select new image for processing:", font="bold"
        )
        self.open_filedialog_btn = ttk.Button(
            self.open_filedialog,
            text="Choose file",
            command=open_filedialog,
        )
        self.open_filedialog_label.grid(
            row=0, column=0, columnspan=2, sticky="nesw", padx=16
        )
        self.open_filedialog_btn.grid(
            row=1, column=0, columnspan=2, sticky="nesw", padx=16, pady=16, ipady=4
        )

        # green controls
        self.green_controls = tk.Frame(
            self.controls_frame,
            width=(app_width / 2),
            height=(app_height / 4),
        )
        self.green_controls.grid_rowconfigure((0, 1, 2), weight=1)
        self.green_controls.grid_columnconfigure(1, weight=1)
        self.green_controls.grid(row=1, pady=(0, 16))

        # green
        self.green_label = ttk.Label(
            self.green_controls, text="Green mask:", font="bold"
        )
        # greenlh
        self.greenlh_slider = ttk.Scale(
            self.green_controls,
            from_=0,
            to=90,
            length=(4 * 90),
            orient="horizontal",
            variable=util.mask_green_l[0],
            value=util.mask_green_l[0],
            command=update_slider,
        )
        self.greenlh_label = ttk.Label(
            self.green_controls,
            text="Lower Hue: %d" % util.mask_green_l[0],
            width=16,
        )
        # greenuh
        self.greenuh_slider = ttk.Scale(
            self.green_controls,
            from_=90,
            to=180,
            length=(4 * 90),
            orient="horizontal",
            variable=util.mask_green_u[0],
            value=util.mask_green_u[0],
            command=update_slider,
        )
        self.greenuh_label = ttk.Label(
            self.green_controls, text="Upper Hue: %d" % util.mask_green_u[0], width=16
        )

        self.green_label.grid(row=0, column=0, columnspan=2, sticky="nesw")
        self.greenlh_label.grid(row=1, column=0, sticky="nesw")
        self.greenlh_slider.grid(row=1, column=1, padx=16)
        self.greenuh_label.grid(row=2, column=0, sticky="nesw")
        self.greenuh_slider.grid(row=2, column=1, padx=16)

        # brown controls
        self.brown_controls = tk.Frame(
            self.controls_frame,
            width=(app_width / 2),
            height=(app_height / 4),
        )
        self.brown_controls.grid_rowconfigure(3, weight=1)
        self.brown_controls.grid_columnconfigure(1, weight=1)
        self.brown_controls.grid(row=2, pady=(16, 16))

        # brown
        self.brown_label = ttk.Label(
            self.brown_controls, text="Brown mask:", font="bold"
        )
        # brownlh
        self.brownlh_slider = ttk.Scale(
            self.brown_controls,
            from_=0,
            to=90,
            length=(4 * 90),
            orient="horizontal",
            variable=util.mask_brown_l[0],
            value=util.mask_brown_l[0],
            command=update_slider,
        )
        self.brownlh_label = ttk.Label(
            self.brown_controls, text="Lower Hue: %d" % util.mask_brown_l[0], width=16
        )

        # brownuh
        self.brownuh_slider = ttk.Scale(
            self.brown_controls,
            from_=90,
            to=180,
            length=(4 * 90),
            orient="horizontal",
            variable=util.mask_brown_u[0],
            value=util.mask_brown_u[0],
            command=update_slider,
        )
        self.brownuh_label = ttk.Label(
            self.brown_controls, text="Upper Hue: %d" % util.mask_brown_u[0], width=16
        )

        self.brown_label.grid(row=0, column=0, columnspan=2, sticky="nesw")
        self.brownlh_label.grid(row=1, column=0, sticky="nesw")
        self.brownlh_slider.grid(row=1, column=1, padx=16)
        self.brownuh_label.grid(row=2, column=0, sticky="nesw")
        self.brownuh_slider.grid(row=2, column=1, padx=16)

        # gray controls
        self.gray_controls = tk.Frame(
            self.controls_frame,
            width=(app_width / 2),
            height=(app_height / 4),
        )
        self.gray_controls.grid_rowconfigure(3, weight=1)
        self.gray_controls.grid_columnconfigure(1, weight=1)
        self.gray_controls.grid(row=3, pady=(16, 0))

        # gray
        self.gray_label = ttk.Label(self.gray_controls, text="Gray mask:", font="bold")
        # graylh
        self.graylh_slider = ttk.Scale(
            self.gray_controls,
            from_=0,
            to=90,
            length=(4 * 90),
            orient="horizontal",
            variable=util.mask_gray_l[0],
            value=util.mask_gray_l[0],
            command=update_slider,
        )
        self.graylh_label = ttk.Label(
            self.gray_controls, text="Lower Hue: %d" % util.mask_gray_l[0], width=16
        )
        # grayuh
        self.grayuh_slider = ttk.Scale(
            self.gray_controls,
            from_=90,
            to=180,
            length=(4 * 90),
            orient="horizontal",
            variable=util.mask_gray_u[0],
            value=util.mask_gray_u[0],
            command=update_slider,
        )
        self.grayuh_label = ttk.Label(
            self.gray_controls, text="Upper Hue: %d" % util.mask_gray_u[0], width=16
        )

        self.gray_label.grid(row=0, column=0, columnspan=2, sticky="nesw")
        self.graylh_label.grid(row=1, column=0, sticky="nesw")
        self.graylh_slider.grid(row=1, column=1, padx=16)
        self.grayuh_label.grid(row=2, column=0, sticky="nesw")
        self.grayuh_slider.grid(row=2, column=1, padx=16)

        # data display
        self.data_display = tk.Frame(
            self.controls_frame,
            width=(app_width / 2),
            height=(app_height / 4),
        )
        self.data_display.grid_rowconfigure(3, weight=1)
        self.data_display.grid_columnconfigure(1, weight=1)
        self.data_display.grid(row=4, pady=(16, 0))

        self.data_area_value = 0.49
        self.data_green_value = 0.21
        self.data_build_value = 0.18

        self.data_label = ttk.Label(
            self.data_display, text="Classification results:", font="bold"
        )
        self.data_area = ttk.Label(
            self.data_display,
            text="Area: %.2f km\u00b2" % self.data_area_value,
            font="bold",
        )
        self.data_green = ttk.Label(
            self.data_display,
            text="Greenery: %.2f km\u00b2" % self.data_green_value,
            font="bold",
        )
        self.data_build = ttk.Label(
            self.data_display,
            text="Buildings: %.2f km\u00b2" % self.data_build_value,
            font="bold",
        )

        self.data_label.grid(row=0, sticky="w")
        self.data_area.grid(row=1, columnspan=2, sticky="w")
        self.data_green.grid(row=2, columnspan=2, sticky="w")
        self.data_build.grid(row=3, columnspan=2, sticky="w")

        # Keyboard functions
        # Exit app with <Esc>
        self.bind("<Escape>", lambda *_: self.quit())
        # Open file dialog with o
        self.bind("<o>", lambda *_: open_filedialog())


if __name__ == "__main__":
    app = App()
    app.mainloop()
