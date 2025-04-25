from tkinter import Frame, Label, Toplevel, Entry, Button, Canvas, Scrollbar, BOTH, LEFT, RIGHT, Y, VERTICAL, END, messagebox, FLAT, NORMAL, DISABLED, Text, WORD
from tkinter import ttk
from tkinter import filedialog
import os

class View(Frame):
    def __init__(self, parent, os):
        super().__init__(parent, width=1100, height=700, bg="#1e1e2f")
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

        style.configure("MiniRed.TButton",
                    font=("Segoe UI", 12, "bold"),
                    background="#D32F2F",
                    foreground="white",
                    padding=10)
        style.map("MiniRed.TButton", background=[('active', '#B71C1C')])

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
        self.build_simulation_open_file_screen()

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
        for widget in self.winfo_children():
            widget.destroy()

        # Main container
        main_container = Frame(self, bg="#1e1e2f")
        main_container.pack(fill="both", expand=True)

        # Sidebar (Navigation Bar)
        sidebar = Frame(main_container, bg="#2b2b40", width=150)
        sidebar.pack(side="left", fill="y")

        Label(
            sidebar,
            text=f"Model: {model_name}",
            font=("Segoe UI", 14, "bold"),
            fg="white",
            bg="#2b2b40",
            wraplength=180,
            justify="center"
        ).pack(pady=(20, 30))

        # Navigation buttons
        ttk.Button(
            sidebar,
            text="Add Individual",
            style="Blue.TButton",
            command=self.open_add_individual_form
        ).pack(pady=10, padx=10, fill="x")

        ttk.Button(
            sidebar,
            text="Save Positions",
            style="Blue.TButton",
            command=self.save_card_positions
        ).pack(pady=10, padx=10, fill="x")

        ttk.Button(
            sidebar,
            text="Web Scraper",
            style="Blue.TButton",
            command=self.web_scaper
        ).pack(pady=10, padx=10, fill="x")

        ttk.Button(
            sidebar,
            text="Back to Home",
            style="Blue.TButton",
            command=self.go_back_to_home
        ).pack(pady=(300, 10), padx=10, fill="x")

        # Main content area for profile cards
        content_area = Frame(main_container, bg="#1e1e2f")
        content_area.pack(side="left", fill="both", expand=True)

        self.profile_list_frame = Frame(content_area, bg="#1e1e2f")
        self.profile_list_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.refresh_profile_list()

    def open_add_individual_form(self):
        form = Toplevel(self)
        form.title("Add Individual")
        form.geometry("400x600")
        form.configure(bg="#1e1e2f")

        container = Frame(form, bg="#1e1e2f")
        container.pack(fill=BOTH, expand=True)

        canvas = Canvas(container, bg="#1e1e2f", highlightthickness=0)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = Scrollbar(container, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        canvas.configure(yscrollcommand=scrollbar.set)

        form_frame = Frame(canvas, bg="#1e1e2f")
        canvas.create_window((0, 0), window=form_frame, anchor="nw")

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        form_frame.bind("<Configure>", on_frame_configure)

        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)

        Label(
            form_frame,
            text="➕ Add New Individual",
            font=("Segoe UI", 18, "bold"),
            fg="white",
            bg="#1e1e2f"
        ).pack(pady=(20, 10), padx=20, anchor="w")

        Label(
            form_frame,
            text="New Field Name",
            font=("Segoe UI", 11, "bold"),
            fg="#cccccc",
            bg="#1e1e2f"
        ).pack(pady=(10, 0), padx=20, anchor="w")

        field_name_entry = Entry(
            form_frame,
            font=("Segoe UI", 11),
            width=28,
            relief=FLAT,
            highlightthickness=1,
            highlightbackground="#3c3c4e",
            bg="white",
            fg="black",
            insertbackground="black"
        )
        field_name_entry.pack(pady=(5, 10), padx=20, anchor="w")

        fields = []
        entries = {}

        def add_field():
            field_name = field_name_entry.get().strip()
            if field_name and field_name not in fields:
                fields.append(field_name)
                Label(
                    form_frame,
                    text=field_name,
                    font=("Segoe UI", 11),
                    fg="white",
                    bg="#1e1e2f"
                ).pack(anchor="w", padx=20, pady=(10, 0))
                entry = Entry(
                    form_frame,
                    font=("Segoe UI", 11),
                    width=28,
                    relief=FLAT,
                    highlightthickness=1,
                    highlightbackground="#3c3c4e",
                    bg="white",
                    fg="black",
                    insertbackground="black"
                )
                entry.pack(padx=20, pady=(0, 10), anchor="w")
                entries[field_name] = entry
                field_name_entry.delete(0, END)

        ttk.Button(
            form_frame,
            text="➕ Add Field",
            style="MiniBlue.TButton",
            command=add_field
        ).pack(padx=20, pady=(0, 20), anchor="w")

        def save_individual():
            person_data = {field: entries[field].get() for field in fields}
            self.controller.add_individual_to_model(person_data)
            form.destroy()
            self.refresh_profile_list()

        ttk.Button(
            form_frame,
            text="💾 Save Individual",
            style="MiniBlue.TButton",
            command=save_individual
        ).pack(pady=30, padx=20, anchor="center")

        form.after(100, lambda: canvas.configure(scrollregion=canvas.bbox("all")))


    def refresh_profile_list(self):
        # Clear the current profile list from the frame
        for widget in self.profile_list_frame.winfo_children():
            widget.destroy()

          # Retrieve the updated list of profiles
        profiles = self.controller.get_all_profiles()

        # If no profiles exist, show a message
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
        # Store card references for later use 
        self.card_refs = []

        for idx, profile in enumerate(profiles):
            # Only use non-position fields for preview text
            preview_fields = [(k, v) for k, v in profile.items() if k != "position"][:2]
            preview_text = "\n".join(f"{k}: {v}" for k, v in preview_fields)

            # Use saved position or default grid position
            position = profile.get("position", [20 + (idx % 3) * 270, 20 + (idx // 3) * 120])
            x, y = position

            # Create the profile card frame
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

            # Add profile preview text
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

            # Add a button to view the profile details
            btn = ttk.Button(
                card,
                text="View Details",
                command=lambda p=profile: self.show_more_info(p),
                style="MiniBlue.TButton",
                width=15
            )
            btn.pack(pady=5)

            # Make the profile card draggable
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
        detail_win.geometry("400x600")
        detail_win.configure(bg="#1e1e2f")

        # Header
        Label(
            detail_win,
            text="👤 Profile Details",
            font=("Segoe UI", 18, "bold"),
            fg="white",
            bg="#1e1e2f"
        ).pack(pady=(20, 10), anchor="center")

        if not profile:
            Label(
                detail_win,
                text="No Data Found.",
                font=("Segoe UI", 12),
                fg="white",
                bg="#1e1e2f"
            ).pack(pady=10)
            return

        # Profile data
        for key, value in profile.items():
            if key == "position":
                continue

            frame = Frame(detail_win, bg="#1e1e2f")
            frame.pack(padx=20, pady=(6, 6), anchor="w", fill="x")

            Label(
                frame,
                text=f"{key}",
                font=("Segoe UI", 11, "bold"),
                fg="#bbbbbb",
                bg="#1e1e2f"
            ).pack(anchor="w")

            Label(
                frame,
                text=value,
                font=("Segoe UI", 11),
                fg="white",
                bg="#2e2e3e",
                padx=10,
                pady=5,
                relief="flat",
                anchor="w",
                width=30,
            ).pack(anchor="w", pady=(2, 0))

        # Separator
        Frame(detail_win, height=2, bd=0, relief="sunken", bg="#3c3c4e").pack(fill="x", padx=20, pady=20)

        # Action buttons
        btn_frame = Frame(detail_win, bg="#1e1e2f")
        btn_frame.pack(pady=10)

        ttk.Button(
            btn_frame,
            text="✏️ Update Profile",
            style="MiniBlue.TButton",
            command=lambda: [detail_win.destroy(), self.open_update_individual_form(profile)],
        ).pack(pady=5, ipadx=10, anchor="center")

        ttk.Button(
            btn_frame,
            text="🗑️ Delete Profile",
            style="MiniRed.TButton",
            command=lambda: [detail_win.destroy(), self.delete_individual(profile)],
        ).pack(pady=5, ipadx=10, anchor="center")

    def save_card_positions(self):
        """Save the positions of all cards along with profile data and model name to the JSON file."""
        profiles = self.controller.get_all_profiles()
    
        # Update profile data with current card positions
        for idx, card in enumerate(self.card_refs):
            x, y = card.winfo_x(), card.winfo_y()
            profiles[idx]["position"] = [x, y]  

        # Include the model name and profiles
        model_data = {
            "model_name": self.controller.get_model_name(),  # Get the model name
            "individuals": profiles  # Include all profiles with the updated positions
        }

        # Save the updated model data
        self.controller.save_model_data(model_data)
        messagebox.showinfo("Saved", "Card Positions and Model Data Saved Successfully.")
    
    def open_update_individual_form(self, profile):
        form = Toplevel(self)
        form.title("Update Individual")
        form.geometry("400x600")
        form.configure(bg="#1e1e2f")

        container = Frame(form, bg="#1e1e2f")
        container.pack(fill=BOTH, expand=True)

        canvas = Canvas(container, bg="#1e1e2f", highlightthickness=0)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = Scrollbar(container, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        canvas.configure(yscrollcommand=scrollbar.set)

        form_frame = Frame(canvas, bg="#1e1e2f")
        canvas.create_window((0, 0), window=form_frame, anchor="nw")

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        form_frame.bind("<Configure>", on_frame_configure)

        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)

        Label(
            form_frame,
            text="✏️ Update Individual",
            font=("Segoe UI", 18, "bold"),
            fg="white",
            bg="#1e1e2f"
        ).pack(pady=(20, 10), anchor="w", padx=20)

        fields = [k for k in profile.keys() if k != "position"]
        entries = {}

        for field in fields:
            Label(form_frame, text=field, font=("Segoe UI", 11), fg="white", bg="#1e1e2f").pack(anchor="w", padx=20, pady=(10, 0))
            entry = Entry(form_frame, font=("Segoe UI", 11), width=28, relief=FLAT, highlightthickness=1, highlightbackground="#3c3c4e", bg="white", fg="black", insertbackground="black")
            entry.insert(0, profile[field])
            entry.pack(padx=20, pady=(0, 10), anchor="w")
            entries[field] = entry

        Label(form_frame, text="Add New Field:", font=("Segoe UI", 11), fg="#cccccc", bg="#1e1e2f").pack(anchor="w", padx=20, pady=(15, 0))

        new_field_entry = Entry(form_frame, font=("Segoe UI", 11), width=28, relief=FLAT, highlightthickness=1, highlightbackground="#3c3c4e", bg="white", fg="black", insertbackground="black")
        new_field_entry.pack(padx=20, pady=(5, 10), anchor="w")

        def add_field():
            new_field = new_field_entry.get().strip()
            if new_field and new_field not in entries:
                Label(form_frame, text=new_field, font=("Segoe UI", 11), fg="white", bg="#1e1e2f").pack(anchor="w", padx=20, pady=(10, 0))
                entry = Entry(form_frame, font=("Segoe UI", 11), width=28, relief=FLAT, highlightthickness=1, highlightbackground="#3c3c4e", bg="white", fg="black", insertbackground="black")
                entry.pack(padx=20, pady=(0, 10), anchor="w")
                entries[new_field] = entry
                new_field_entry.delete(0, END)

        ttk.Button(form_frame, text="➕ Add Field", style="MiniBlue.TButton", command=add_field).pack(padx=20, pady=10, anchor="w")

        def save_updated_profile():
            updated_data = {field: entries[field].get() for field in entries}
            updated_data["position"] = profile.get("position", [20, 20])
            self.controller.update_individual(profile, updated_data)
            form.destroy()
            self.refresh_profile_list()

        ttk.Button(form_frame, text="💾 Save", style="MiniBlue.TButton", command=save_updated_profile).pack(padx=20, pady=30, anchor="center")

        form.after(100, lambda: canvas.configure(scrollregion=canvas.bbox("all")))

    def delete_individual(self, profile):
        confirm = messagebox.askyesno("Confirm Delete", "Are you Sure you Want to Delete This Profile?")
        if confirm:
            self.controller.delete_individual_from_model(profile)

            self.card_refs = [card for card in self.card_refs if card not in profile]

            self.refresh_profile_list()

            messagebox.showinfo("Deleted", "Profile Deleted Successfully.")

    def web_scaper(self):
        form = Toplevel(self)
        form.title("Web Scraper")
        form.geometry("650x550")
        form.configure(bg="#1e1e2f")

        container = Frame(form, bg="#1e1e2f")
        container.pack(fill=BOTH, expand=True)

        canvas = Canvas(container, bg="#1e1e2f", highlightthickness=0)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = Scrollbar(container, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        canvas.configure(yscrollcommand=scrollbar.set)

        form_frame = Frame(canvas, bg="#1e1e2f")
        canvas.create_window((0, 0), window=form_frame, anchor="nw")

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        form_frame.bind("<Configure>", on_frame_configure)

        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)

        Label(form_frame, text="🌐 Web Scraper", font=("Segoe UI", 18, "bold"),
            fg="white", bg="#1e1e2f").pack(pady=(20, 10), anchor="center")

        Label(form_frame, text="Enter a URL to Scrape Data From:",
            font=("Segoe UI", 13), fg="#bbbbbb", bg="#1e1e2f").pack(pady=(5, 5), anchor="w", padx=20)

        self.url_entry = Entry(form_frame, font=("Segoe UI", 12), width=45,
                           bg="#2c2c3c", fg="white", insertbackground="white", relief=FLAT)
        self.url_entry.pack(pady=(5, 10), padx=20)

        Label(form_frame,
          text="⚠️ Please Ensure you Have Permission to Scrape this Site. We Respect robots.txt.",
          font=("Segoe UI", 10, "italic"),
          fg="#ff6666", bg="#1e1e2f", wraplength=440, justify=LEFT).pack(pady=(0, 15), padx=20, anchor="w")

        go_button = ttk.Button(form_frame, text="🔍 Go", style="MiniBlue.TButton", command=self.scrape_data)
        go_button.pack(pady=(0, 20), padx=20)

        Label(form_frame, text="Scraped Data:", font=("Segoe UI", 13, "bold"),
          fg="white", bg="#1e1e2f").pack(pady=(5, 5), anchor="w", padx=20)

        result_container = Frame(form_frame, bg="#1e1e2f")
        result_container.pack(padx=20, pady=10, fill=BOTH, expand=True)

        self.result_text = Text(result_container,
                            font=("Segoe UI", 11),
                            wrap=WORD,
                            bg="#2a2a3d",
                            fg="white",
                            insertbackground="white",
                            relief=FLAT,
                            height=15)
        self.result_text.pack(side=LEFT, fill=BOTH, expand=True)

        result_scroll = Scrollbar(result_container, command=self.result_text.yview)
        result_scroll.pack(side=RIGHT, fill=Y)
        self.result_text.config(yscrollcommand=result_scroll.set)

        self.result_text.insert(END, "Results Will Appear Here After Scraping.")
        self.result_text.config(state=DISABLED)

    def scrape_data(self):
        url = self.url_entry.get().strip()

        if not url:
            messagebox.showerror("Error", "Please Enter a Valid URL!")
            return

        scraped_data = self.controller.web_scraper(url)

        if scraped_data:
            self.display_data(scraped_data)
        else:
            self.display_data("❌ Failed to Scrape the Page or No Data Found.")


    def display_data(self, data):
        self.result_text.config(state=NORMAL)
        self.result_text.delete(1.0, END)

        self.result_text.insert(END, f"✅ What We Extracted:\n\n{data}")
        self.result_text.config(state=DISABLED)

    def build_simulation_open_file_screen(self):
        open_model_window = Toplevel(self)
        open_model_window.title("Open Existing Model")
        open_model_window.geometry("500x150")
        open_model_window.configure(bg="#1e1e2f")

        Label(
            open_model_window,
            text="Open Existing Model to Begin Simulation",
            font=("Segoe UI", 20, "bold"),
            fg="white",
            bg="#1e1e2f"
        ).pack(pady=(20, 10))

        def browse_and_load_model():
            filename = filedialog.askopenfilename(filetypes=(("JSON Files", "*.json"),))
            if filename and self.controller:
                self.controller.load_existing_model(filename)
                open_model_window.destroy()
                self.show_simulation_screen(filename)

        button_frame = Frame(open_model_window, bg="#1e1e2f")
        button_frame.pack(pady=20)

        ttk.Button(button_frame, text="Browse", style="MiniBlue.TButton", command=browse_and_load_model, width=18).pack(side="left", padx=10)
        ttk.Button(button_frame, text="Cancel", style="MiniBlue.TButton", command=open_model_window.destroy, width=10).pack(side="left", padx=10)


    def show_simulation_screen(self, model_path):
        # Clear existing widgets
        for widget in self.winfo_children():
            widget.destroy()

        model_name = os.path.basename(model_path)

        # Main container
        main_container = Frame(self, bg="#1e1e2f")
        main_container.pack(fill="both", expand=True)

        # Sidebar
        sidebar = Frame(main_container, bg="#2b2b40", width=250)
        sidebar.pack(side="left", fill="y", padx=15, pady=15)

        Label(
            sidebar,
            text=f"Simulation: {model_name}",
            font=("Segoe UI", 18, "bold"),
            fg="white",
            bg="#2b2b40",
            wraplength=180,
            justify="center"
        ).pack(pady=(30, 40))

        ttk.Button(
            sidebar,
            text="Back to Home",
            style="Blue.TButton",
            command=self.go_back_to_home
        ).pack(side="bottom", pady=(10, 5), padx=15, fill="x")

        ttk.Button(
            sidebar,
            text="Send Email",
            style="Blue.TButton",
            command=self.send_email
        ).pack(side="bottom", pady=(5, 10), padx=15, fill="x")

        # Main simulation area
        simulation_area = Frame(main_container, bg="#1e1e2f")
        simulation_area.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        # Left section for available individuals
        left_section = Frame(simulation_area, bg="#1e1e2f", width=350)
        left_section.pack(side="left", fill="y", padx=15, pady=15)

        Label(left_section, text="Available Individuals", fg="white", bg="#1e1e2f", font=("Segoe UI", 14, "bold")).pack(pady=15)

        scroll_container = Frame(left_section, bg="#1e1e2f")
        scroll_container.pack(fill="both", expand=True)

        canvas = Canvas(scroll_container, bg="#1e1e2f", highlightthickness=0, width=320)
        scrollbar = ttk.Scrollbar(scroll_container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        scrollable_frame = Frame(canvas, bg="#1e1e2f")
        self.all_profiles_frame = scrollable_frame

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        self.render_simulation_profile_cards(self.all_profiles_frame, self.controller.get_all_profiles())

        # Right section for selected attackers & results
        right_section = Frame(simulation_area, bg="#1e1e2f", width=450)
        right_section.pack(side="left", fill="y", padx=15, pady=15)  

        # Recommendation Engine section
        selected_attackers_frame = Frame(right_section, bg="#1e1e2f")
        selected_attackers_frame.pack(fill="x", pady=(10, 5))

        Label(selected_attackers_frame, text="Recommendation Engine", fg="white", bg="#1e1e2f", font=("Segoe UI", 14, "bold")).pack(pady=15)

        self.selected_attackers_frame = selected_attackers_frame

        # Results Frame for generated email
        self.results_frame = Frame(right_section, bg="#1e1e2f", height=300) 
        self.results_frame.pack(fill="both", expand=False, pady=(5, 15))  

        Label(self.results_frame, text="Generate Attack", fg="white", bg="#1e1e2f", font=("Segoe UI", 14, "bold")).pack(pady=15)

        self.email_textbox = Text(
            self.results_frame,
            bg="#2a2a3c",
            fg="white",
            wrap="word",
            font=("Segoe UI", 12),
            width=50,
            height=20,
            padx=10,
            pady=10,
            bd=0,
            state="disabled"  
        )
        self.email_textbox.pack(fill="both", padx=10, pady=15)

    def render_simulation_profile_cards(self, parent_frame, profiles):
        for widget in parent_frame.winfo_children():
            if isinstance(widget, Frame):
                widget.destroy()

        for idx, profile in enumerate(profiles):
            preview_fields = [(k, v) for k, v in profile.items() if k != "position"][:2]
            preview_text = "\n".join(f"{k}: {v}" for k, v in preview_fields)

            card = Frame(
                parent_frame,
                bg="#2a2a3c",
                bd=1,
                relief="solid",
                padx=12,
                pady=15
            )
            card.pack(pady=12, padx=12, fill="x")

            Label(
                card,
                text=preview_text or "No Data",
                font=("Segoe UI", 11),
                fg="white",
                bg="#2a2a3c",
                justify="left",
                anchor="w",
                wraplength=240
            ).pack(pady=8, fill="x")

            ttk.Button(
                card,
                text="Attack",
                command=lambda p=profile: self.select_for_attack(p),
                style="MiniBlue.TButton",
                width=18
            ).pack(pady=8)

    def select_for_attack(self, profile):
        preview_fields = [(k, v) for k, v in profile.items() if k != "position"][:2]
        preview_text = "\n".join(f"{k}: {v}" for k, v in preview_fields)

        card = Frame(
            self.selected_attackers_frame,
            bg="#3a3a50",
            bd=1,
            relief="solid",
            padx=12,
            pady=10,
            height=150,  
            width=420  
        )
        card.pack(pady=12, padx=12, fill="x")
        card.pack_propagate(False) 

        canvas = Canvas(card, bg="#3a3a50", bd=0, highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(card, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        content_frame = Frame(canvas, bg="#3a3a50")
        canvas.create_window((0, 0), window=content_frame, anchor="nw")

        content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        Label(
            content_frame,
            text=preview_text,
            font=("Segoe UI", 9),  
            fg="white",
            bg="#3a3a50",
            justify="left",
            anchor="w",
            wraplength=240
        ).pack(pady=(5, 2), fill="x")

        recommended_vectors = self.controller.recommend_vectors(profile)

        if recommended_vectors:
            Label(
                content_frame,
                text="Top Vectors:",
                font=("Segoe UI", 9, "bold"),
                fg="#b0b0ff",
                bg="#3a3a50",
                anchor="w"
            ).pack(pady=(5, 2), fill="x", padx=5)
            
            for vector in recommended_vectors[:5]:  
                Label(
                    content_frame,
                    text=f"• {vector}",
                    font=("Segoe UI", 8), 
                    fg="white",
                    bg="#3a3a50",
                    anchor="w",
                    wraplength=240,
                    justify="left"
                ).pack(fill="x", padx=12, pady=2)

        ttk.Button(
            content_frame,
            text="Remove",
            command=card.destroy,
            style="MiniRed.TButton",
            width=16 
        ).pack(pady=5, fill="x")

        ttk.Button(
            content_frame,
            text="Attack Profile",
            command=lambda rv=recommended_vectors, p=profile: self.attack_profile(rv, p),
            style="MiniBlue.TButton",
            width=16 
        ).pack(pady=5, fill="x")


    def attack_profile(self, recommended_vectors, profile):
        selected_vector = recommended_vectors[0] if recommended_vectors else None

        self.email_textbox.config(state="normal")  
        self.email_textbox.delete("1.0", "end")   
        self.email_textbox.insert("1.0", "Generating Phishing Email... Please Wait.")
        self.email_textbox.config(state="disabled") 

        self.controller.start_email_generation_in_background(profile, selected_vector, self.display_generated_email)

    def display_generated_email(self, cleaned_email):

        self.email_textbox.config(state="normal")  
        self.email_textbox.delete(1.0, "end")  
        self.email_textbox.insert("1.0", cleaned_email)  
        self.email_textbox.config(state="disabled") 

    def send_email(self):   
        open_email_window = Toplevel(self)
        open_email_window.title("Send Generated Email to Victim")
        open_email_window.geometry("520x720")  
        open_email_window.configure(bg="#1e1e2f")

        Label(
            open_email_window,
            text="Please Enter Your Gmail and Password, and Fill Out Other Fields:",
            font=("Segoe UI", 16, "bold"),
            fg="white",
            bg="#1e1e2f"
        ).pack(pady=(20, 10))

        Label(
            open_email_window,
            text="Your Email",
            font=("Segoe UI", 12),
            fg="white",
            bg="#1e1e2f"
        ).pack(pady=(10, 5))
        user_email_entry = Entry(open_email_window, width=40, font=("Segoe UI", 12))
        user_email_entry.pack(pady=(5, 10))

        Label(
            open_email_window,
            text="Your Password",
            font=("Segoe UI", 12),
            fg="white",
            bg="#1e1e2f"
        ).pack(pady=(10, 5))
        user_password_entry = Entry(open_email_window, width=40, show="*", font=("Segoe UI", 12))
        user_password_entry.pack(pady=(5, 10))

        Label(
            open_email_window,
            text="Recipient's Email",
            font=("Segoe UI", 12),
            fg="white",
            bg="#1e1e2f"
        ).pack(pady=(10, 5))
        recipient_email_entry = Entry(open_email_window, width=40, font=("Segoe UI", 12))
        recipient_email_entry.pack(pady=(5, 10))

        Label(
            open_email_window,
            text="Subject",
            font=("Segoe UI", 12),
            fg="white",
            bg="#1e1e2f"
        ).pack(pady=(10, 5))
        subject_entry = Entry(open_email_window, width=40, font=("Segoe UI", 12))
        subject_entry.pack(pady=(5, 10))

        Label(
            open_email_window,
            text="Message",
            font=("Segoe UI", 12),
            fg="white",
            bg="#1e1e2f"
        ).pack(pady=(10, 5))

        message_text = Text(open_email_window, width=40, height=8, font=("Segoe UI", 12), wrap="word")
        message_text.pack(pady=(5, 10))

        message_scrollbar = Scrollbar(open_email_window, command=message_text.yview)
        message_scrollbar.pack(side="right", fill="y")
        message_text.config(yscrollcommand=message_scrollbar.set)

        def on_send():
            user_email = user_email_entry.get()
            user_password = user_password_entry.get()
            recipient_email = recipient_email_entry.get()
            subject = subject_entry.get()
            message = message_text.get("1.0", "end-1c")

            if not (user_email and user_password and recipient_email and subject and message):
                messagebox.showwarning("Input Error", "All Fields Must be Filled Out.")
                return

            response = self.controller.send_email(user_email, user_password, recipient_email, subject, message)

            messagebox.showinfo("Email Status", response)

        ttk.Button(
            open_email_window,
            text="Send Email",
            style="MiniBlue.TButton",
            command=on_send
        ).pack(pady=20)

        ttk.Button(
            open_email_window,
            text="Close",
            style="MiniRed.TButton",
            command=open_email_window.destroy
        ).pack(pady=20)

    def go_back_to_home(self):
        """Handle the back navigation to home screen."""
        self.build_home_screen()
