from tkinter import messagebox
import json
import threading

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.model.set_view(view)
        self.view.setController(self)
        self.view.build_home_screen()
        self.json_path = ""

    def load_existing_model(self, filepath):
        try:
            self.json_path = filepath
            with open(filepath, 'r') as file:
                data = json.load(file)
            self.model.load_data(data, filepath)
            self.view.show_model_editor(self.model.model_name)
            self.view.refresh_profile_list()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to Load Model:\n{str(e)}")

    def create_new_model(self, model_name, save_path):
        try:
            self.json_path = save_path
            self.model.create_new(model_name, save_path)
            self.view.show_model_editor(self.model.model_name)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to Create Model:\n{str(e)}")

    def add_individual_to_model(self, person_data):
        self.model.add_individual(person_data)
        self.view.refresh_profile_list()

    def get_all_profiles(self):
        return self.model.get_all_profiles()

    def get_model_name(self):
        return self.model.model_name

    def update_individual(self, old_profile, new_profile):
        self.model.update_individual(old_profile, new_profile)
        self.view.refresh_profile_list()

    def delete_individual_from_model(self, profile):
        self.model.delete_individual(profile)
        self.view.refresh_profile_list()

    def save_model_data(self, model_data):
        """Save the complete model data."""
        self.model.org_data = model_data
        self.model.save()

    def web_scraper(self, url):
        # Call the model's web_scraper method to scrape the data
        scraped_data = self.model.web_scraper(url)

        if scraped_data:
            # If scraping is successful, return the data to the view
            return scraped_data
        else:
            return "Failed to Scrape the Page or No Data Found."

    def handle_simulate_button(self):
        messagebox.showinfo("Simulation", "Simulation functionality not implemented yet.")

    def recommend_vectors(self, profile):
        try:
            return self.model.recommend_social_engineering_vectors(profile)
        except Exception as e:
            print(f"Recommendation Error: {e}")
            return []
        
    def start_email_generation_in_background(self, profile, vector, callback):
        threading.Thread(target=self.generate_email, args=(profile, vector, callback)).start()

    def generate_email(self, profile, selected_vector, callback):
        try:
            generated_email = self.model.generate_phishing_email(profile, selected_vector)
            callback(generated_email)
        except Exception as e:
            callback("An Error Occured Generating Email, Please Try Again Layer.")

    def send_email(self, user_email, user_password, recipient_email, subject, message):
        result = self.model.send_email(user_email, user_password, recipient_email, subject, message)
        return result
