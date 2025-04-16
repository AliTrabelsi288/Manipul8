import json
from tkinter import messagebox

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.model.set_view(view)
        self.view.setController(self)
        self.view.build_home_screen()
        self.json_path = ""

    def load_existing_model(self, filepath):
        """Load the model from the file."""
        try:
            self.json_path = filepath
            with open(filepath, 'r') as file:
                data = json.load(file)
            self.model.load_data(data, filepath)
            self.view.show_model_editor(self.model.model_name)
            self.view.refresh_profile_list()  # Make sure to refresh the profile list after loading
        except Exception as e:
            messagebox.showerror("Error", f"Failed to Load Model:\n{str(e)}")


    def create_new_model(self, model_name, save_path):
        """Create a new model and save it."""
        try:
            self.json_path = save_path
            self.model.create_new(model_name, save_path)
            self.view.show_model_editor(self.model.model_name)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to Create Model:\n{str(e)}")

    def add_individual_to_model(self, person_data):
        """Add an individual to the model."""
        self.model.add_individual(person_data)
        self.model.save()  # Save the model data after adding the individual
        self.view.refresh_profile_list()  # Refresh the profile list after adding individual

    def get_all_profiles(self):
        """Get all profiles."""
        return self.model.get_all_profiles()

    def save_model_data(self, model_data):
        """Save the model data to the JSON file."""
        try:
            with open(self.json_path, 'w') as file:
                json.dump(model_data, file, indent=4)
            messagebox.showinfo("Saved", "Model data has been successfully saved.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to Save Model:\n{str(e)}")

    def get_model_name(self):
        """Get the current model's name."""
        return self.model.model_name

    def handle_simulate_button(self):
        """Handle the simulate button."""
        messagebox.showinfo("Simulation", "Simulation functionality not implemented yet.")
