import json
from tkinter import Frame, Label, Toplevel, Entry, Button, Canvas, Scrollbar, BOTH, LEFT, RIGHT, Y, VERTICAL, END, messagebox
from tkinter import ttk
from tkinter import filedialog

class View(Frame):
    def __init__(self, parent, os):
        super().__init__(parent, width=800, height=600, bg="#1e1e2f")
        self.controller = None
        self.os = os
        self.pack_propagate(False)
        self.card_refs = []
        self.build_home_screen()

    def setController(self, controller):
        self.controller = controller

    def apply_button_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Blue.TButton",
                        font=("Segoe UI", 16, "bold"),
                        background="#1976D2",
                        foreground="white",
                        padding=15)
        style.map("Blue.TButton", background=[('active', '#1565C0')])
        style.configure("MiniBlue.TButton",
                        font=("Segoe UI", 12, "bold"),
                        background="#1976D2",
                        foreground="white",
                        padding=10)
        style.map("MiniBlue.TButton", background=[('active', '#1565C0')])

    def build_home_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.apply_button_styles()

        Label(
            self,
            text="Welcome to Manipul8",
            font=("Segoe UI", 28, "bold"),
            fg="white",
            bg="#1e1e2f"
        ).pack(pady=(40, 60))

        button_frame = Frame(self, bg="#1e1e2f")
        button_frame.pack(pady=(20, 0))

        def make_button_with_desc(parent, text, desc, command):
            container = Frame(parent, bg="#1e1e2f")
            container.pack(side="top", padx=60, pady=20)
            ttk.Button(container, text=text, style="Blue.TButton", command=command, width=15).pack()
            Label(
                container,
                text=desc,
                font=("Segoe UI", 14),
                fg="white",
                bg="#1e1e2f",
                wraplength=240,
                justify="center"
            ).pack(pady=(16, 0))

        make_button_with_desc(button_frame, "Model", "Model and Visualise an Organisations Hierarchy.", self.on_model_click)
        make_button_with_desc(button_frame, "Simulate", "Run a Social Engineering Attack Simulation.", self.on_simulate_click)

    def on_model_click(self):
        self.build_model_options_screen()

    def on_simulate_click(self):
        if self.controller:
            self.controller.handle_simulate_button()

    def build_model_options_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.apply_button_styles()

        Label(
            self,
            text="Model Options",
            font=("Segoe UI", 28, "bold"),
            fg="white",
            bg="#1e1e2f"
        ).pack(pady=(40, 20))

        model_frame = Frame(self, bg="#1e1e2f")
        model_frame.pack(pady=20, expand=True)

        def make_option_button(parent, text, desc, command):
            container = Frame(parent, bg="#1e1e2f")
            container.pack(side="top", pady=20)
            ttk.Button(container, text=text, style="Blue.TButton", command=command, width=20).pack()
            Label(
                container,
                text=desc,
                font=("Segoe UI", 14),
                fg="white",
                bg="#1e1e2f",
                wraplength=240,
                justify="center"
            ).pack(pady=(12, 0))

        make_option_button(model_frame, "Load Model", "Load a Previously Saved Model.", self.on_load_model_click)
        make_option_button(model_frame, "Create New Model", "Create a New Organisation Hierarchy Model.", self.on_create_new_model_click)
        make_option_button(model_frame, "Back to Home", "Return to Home Screen.", self.on_back_to_home_click)

    def on_load_model_click(self):
        filename = filedialog.askopenfilename(filetypes=(("JSON Files", "*.json"),))
        if filename and self.controller:
            self.controller.load_existing_model(filename)

    def on_create_new_model_click(self):
        new_model_window = Toplevel(self)
        new_model_window.title("Create New Model")
        new_model_window.geometry("500x300")
        new_model_window.configure(bg="#1e1e2f")

        Label(
            new_model_window,
            text="Create New Model",
            font=("Segoe UI", 20, "bold"),
            fg="white",
            bg="#1e1e2f"
        ).pack(pady=(20, 10))

        Label(
            new_model_window,
            text="Model Name:",
            font=("Segoe UI", 14),
            fg="white",
            bg="#1e1e2f"
        ).pack(pady=(10, 0))

        model_name_entry = Entry(new_model_window, font=("Segoe UI", 14), width=30)
        model_name_entry.pack(pady=10)

        def choose_save_location_and_create():
            model_name = model_name_entry.get()
            if model_name:
                save_path = filedialog.asksaveasfilename(
                    defaultextension=".json",
                    filetypes=[("JSON files", "*.json")],
                    initialfile=model_name
                )
                if save_path:
                    self.controller.create_new_model(model_name, save_path)
                    new_model_window.destroy()

        button_frame = Frame(new_model_window, bg="#1e1e2f")
        button_frame.pack(pady=20)

        ttk.Button(button_frame, text="Create Model", style="MiniBlue.TButton", command=choose_save_location_and_create, width=18).pack(side="left", padx=10)
        ttk.Button(button_frame, text="Cancel", style="MiniBlue.TButton", command=new_model_window.destroy, width=10).pack(side="left", padx=10)

    def on_back_to_home_click(self):
        self.build_home_screen()

    def show_model_editor(self, model_name):
        """Show UI for editing an existing model or creating a new one."""
        # Clear the current screen
        for widget in self.winfo_children():
            widget.destroy()

        # Display the title depending on whether we are editing or creating a model
        title_text = f"Editing Model: {model_name}"
        Label(
            self,
            text=title_text,
            font=("Segoe UI", 24, "bold"),
            fg="white",
            bg="#1e1e2f"
        ).pack(pady=(20, 10))

        # Button to add a new individual
        ttk.Button(
            self,
            text="Add Individual",
            style="Blue.TButton",
            command=self.open_add_individual_form
        ).pack(pady=10)

        ttk.Button(
            self,
            text="Save Positions",
            style="Blue.TButton",
            command=self.save_card_positions
        ).pack(pady=10)

        # Frame to display the list of profiles
        self.profile_list_frame = Frame(self, bg="#1e1e2f")
        self.profile_list_frame.pack(pady=10, fill="both", expand=True)

        # Button to go back to the home page
        ttk.Button(
            self,
            text="Back to Home",
            style="Blue.TButton",
            command=self.go_back_to_home
        ).pack(pady=10)

        # Refresh the profile list
        self.refresh_profile_list()

    def open_add_individual_form(self):
        """Form to add a new person to the model."""
        form = Toplevel(self)
        form.title("Add Individual")
        form.geometry("320x600")
        form.configure(bg="#1e1e2f")

        # Scrollable canvas setup
        container = Frame(form, bg="#1e1e2f")
        container.pack(fill=BOTH, expand=True)

        canvas = Canvas(container, bg="#1e1e2f", highlightthickness=0)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = Scrollbar(container, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        canvas.configure(yscrollcommand=scrollbar.set)

        form_frame = Frame(canvas, bg="#1e1e2f")
        canvas.create_window((0, 0), window=form_frame, anchor="nw")

        # Scroll update function
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        form_frame.bind("<Configure>", on_frame_configure)

        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", on_mousewheel)

        # Title
        Label(form_frame, text="Add New Individual", font=("Segoe UI", 16, "bold"), fg="white", bg="#1e1e2f").pack(pady=(15, 5), anchor="w", padx=20)

        fields = []
        entries = {}

        # Add field function
        def add_field():
            field_name = field_name_entry.get().strip()
            if field_name and field_name not in fields:
                fields.append(field_name)
                Label(form_frame, text=field_name, font=("Segoe UI", 11), fg="white", bg="#1e1e2f").pack(anchor="w", padx=20, pady=(10, 0))
                entry = Entry(form_frame, font=("Segoe UI", 11), width=28)
                entry.pack(padx=20, pady=(0, 10), anchor="w")
                entries[field_name] = entry
                field_name_entry.delete(0, END)

        # Field name entry
        Label(form_frame, text="Field Name:", font=("Segoe UI", 11), fg="white", bg="#1e1e2f").pack(anchor="w", padx=20, pady=(10, 0))
        field_name_entry = Entry(form_frame, font=("Segoe UI", 11), width=28)
        field_name_entry.pack(padx=20, pady=5, anchor="w")

        ttk.Button(form_frame, text="Add Field", style="MiniBlue.TButton", command=add_field).pack(padx=20, pady=10, anchor="w")

        # Save individual
        def save_individual():
            person_data = {field: entries[field].get() for field in fields}
            self.controller.add_individual_to_model(person_data)
            form.destroy()
            self.refresh_profile_list()

        ttk.Button(form_frame, text="Save", style="MiniBlue.TButton", command=save_individual).pack(padx=20, pady=20, anchor="w")

        form.after(100, lambda: canvas.configure(scrollregion=canvas.bbox("all")))

    def refresh_profile_list(self):
        for widget in self.profile_list_frame.winfo_children():
            widget.destroy()

        profiles = self.controller.get_all_profiles()

        if not profiles:
            Label(
                self.profile_list_frame,
                text="No Profiles Yet.",
                fg="white",
                bg="#1e1e2f"
            ).pack()
            return

        self.render_draggable_profile_cards(profiles)

    def render_draggable_profile_cards(self, profiles):
        self.card_refs = []

        for idx, profile in enumerate(profiles):
            # Only use non-position fields for preview text
            preview_fields = [(k, v) for k, v in profile.items() if k != "position"][:2]
            preview_text = "\n".join(f"{k}: {v}" for k, v in preview_fields)

            # Use saved position if valid, else fall back to default grid position
            position = profile.get("position")
            if isinstance(position, list) and len(position) == 2:
                x, y = position
            else:
                x, y = 20 + (idx % 3) * 270, 20 + (idx // 3) * 120

            card = Frame(
                self.profile_list_frame,
                bg="#2a2a3c",
                bd=1,
                relief="solid",
                padx=10,
                pady=10,
                width=250,
                height=100
            )
            card.place(x=x, y=y)
            self.card_refs.append(card)

            label = Label(
                card,
                text=preview_text or "No Data Available.",
                font=("Segoe UI", 11),
                fg="white",
                bg="#2a2a3c",
                justify="left",
                anchor="w",
                wraplength=220
            )
            label.pack(pady=5, fill="x")

            btn = ttk.Button(
                card,
                text="View Details",
                command=lambda p=profile: self.show_more_info(p),
                style="MiniBlue.TButton",
                width=15
            )
            btn.pack(pady=5)

            self.make_draggable(card)


    def make_draggable(self, widget):
        def on_start_drag(event):
            widget.start_x = event.x
            widget.start_y = event.y

        def on_drag(event):
            dx = event.x - widget.start_x
            dy = event.y - widget.start_y
            x = widget.winfo_x() + dx
            y = widget.winfo_y() + dy
            widget.place(x=x, y=y)

        widget.bind("<Button-1>", on_start_drag)
        widget.bind("<B1-Motion>", on_drag)

    def show_more_info(self, profile):
        detail_win = Toplevel(self)
        detail_win.title("Profile Details")
        detail_win.geometry("400x500")
        detail_win.configure(bg="#1e1e2f")

        Label(
            detail_win,
            text="Profile Details",
            font=("Segoe UI", 16, "bold"),
            fg="white",
            bg="#1e1e2f"
        ).pack(pady=20)

        if not profile:
            Label(
                detail_win,
                text="No Data Found.",
                font=("Segoe UI", 12),
                fg="white",
                bg="#1e1e2f"
            ).pack(pady=10)
            return

        for key, value in profile.items():
            if key == "position":
                continue  # Skip displaying the position field

            Label(
                detail_win,
                text=f"{key}: {value}",
                font=("Segoe UI", 12),
                fg="white",
                bg="#1e1e2f"
            ).pack(pady=5)

    def save_card_positions(self):
        """Save the positions of all cards along with profile data and model name to the JSON file."""
        profiles = self.controller.get_all_profiles()
    
        # Update profile data with current card positions
        for idx, card in enumerate(self.card_refs):
            x, y = card.winfo_x(), card.winfo_y()
            profiles[idx]["position"] = [x, y]  # Always overwrite with new position

        # Include the model name and profiles
        model_data = {
            "model_name": self.controller.get_model_name(),  # Get the model name
            "individuals": profiles  # Include all profiles with the updated positions
        }

        # Save the updated model data
        self.controller.save_model_data(model_data)
        messagebox.showinfo("Saved", "Card Positions and Model Data Saved Successfully.")

    def go_back_to_home(self):
        """Handle the back navigation to home screen."""
        self.build_home_screen()
