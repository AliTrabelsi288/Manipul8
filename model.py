import json

class Model:
    def __init__(self):
        self.org_data = {"model_name": "", "individuals": [], "positions": []}
        self.save_path = None
        self.model_name = ""
        self.view = None

    def set_view(self, view):
        self.view = view

    def load_data(self, data, filepath):
        """Load data from the file."""
        self.org_data = data
        self.save_path = filepath
        self.model_name = data.get("model_name", "Unnamed")

    def create_new(self, name, path):
        """Create a new model."""
        self.model_name = name
        self.save_path = path
        self.org_data = {
            "model_name": name,
            "individuals": [],
            "positions": []
        }
        self.save()

    def save(self):
        """Save the model data to the file."""
        with open(self.save_path, 'w') as file:
            json.dump(self.org_data, file, indent=4)

    def add_individual(self, person_data):
        """Add a new individual to the model."""
        self.org_data["individuals"].append(person_data)
        self.save()

    def get_all_profiles(self):
        """Get all the profiles from the model."""
        return self.org_data.get("individuals", [])

    def save_positions(self, positions):
        """Save the positions of the cards."""
        self.org_data["positions"] = positions
        self.save()

    def update_individual(self, old_profile, new_profile):
        """Update an existing individual's data."""
        profiles = self.org_data.get("individuals", [])
        for i, p in enumerate(profiles):
            if p == old_profile:
                profiles[i] = new_profile
                break
        self.org_data["individuals"] = profiles
        self.save()

    def delete_individual(self, profile):
        """Delete an individual from the model."""
        profiles = self.org_data.get("individuals", [])
        profiles = [p for p in profiles if p != profile]
        self.org_data["individuals"] = profiles
        self.save()

    def reload_model_data(self):
        """Reload model data from the file."""
        self.org_data = self.load_model_data_from_file()

    def load_model_data_from_file(self):
        """Helper to load data from file path."""
        with open(self.save_path, 'r') as file:
            return json.load(file)
