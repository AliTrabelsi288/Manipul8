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
        
        # Ensure individuals and positions are loaded
        self.individuals = self.org_data.get("individuals", [])
        self.positions = self.org_data.get("positions", [])

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
        if "individuals" not in self.org_data:
            self.org_data["individuals"] = []
        self.org_data["individuals"].append(person_data)
        self.save()  # Save after adding a new individual

    def get_all_profiles(self):
        """Get all the profiles from the model."""
        return self.org_data.get("individuals", [])

    def save_positions(self, positions):
        """Save the positions of the cards."""
        self.org_data["positions"] = positions
        self.save()  # Save after saving positions
