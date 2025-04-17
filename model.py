import json
import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
from urllib.parse import urljoin


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

    def clean_text(self, text):
        """Remove unnecessary whitespace and clean the text."""
        return re.sub(r'\s+', ' ', text).strip()

    def extract_with_patterns(self, pattern, text, limit=5):
        """Extract all matches of a given pattern from the text."""
        return list(set(re.findall(pattern, text)))[:limit]

    def extract_name(self, text, soup):
        """Extract full name using regex and contextual analysis."""
        name_candidates = re.findall(r'\b[A-Z][a-z]+\s[A-Z][a-z]+\b', text)
        blacklist = {
            'Computer Science', 'Cyber Security', 'Data Science', 'Machine Learning',
            'Artificial Intelligence', 'Software Engineering', 'Information Technology',
            'Secure Software', 'Internet Systems', 'Informatics', 'Threat Intelligence',
            'Security Engineering', 'Digital Forensics', 'Human Factors', 'Information Systems'
        }
        name_candidates = [n for n in name_candidates if n not in blacklist]

        contextual_name = None
        for label in ['Name', 'Full Name', 'Profile Name', 'Principal Lecturer', 'Professor']:
            match = re.search(rf'{label}[:\s\-]*([A-Z][a-z]+(?:\s[A-Z][a-z]+)+)', text)
            if match:
                contextual_name = match.group(1)
                break

        if not contextual_name:
            title_tag = soup.find('title')
            h1_tag = soup.find('h1')
            potential = (title_tag.get_text() if title_tag else '') + " " + (h1_tag.get_text() if h1_tag else '')
            contextual_match = re.findall(r'\b[A-Z][a-z]+\s[A-Z][a-z]+\b', potential)
            contextual_match = [n for n in contextual_match if n not in blacklist]
            contextual_name = contextual_match[0] if contextual_match else None

        if not contextual_name and name_candidates:
            name_freq = Counter(name_candidates)
            contextual_name = name_freq.most_common(1)[0][0]

        return contextual_name if contextual_name else "Not found"

    def extract_social_links(self, soup, base_url):
        """Extract social media links like LinkedIn, GitHub, etc."""
        links = [a['href'] for a in soup.find_all('a', href=True)]
        full_links = [urljoin(base_url, link) for link in links]
        social_domains = ['linkedin.com', 'github.com', 'twitter.com', 'facebook.com', 'researchgate.net']
        return [link for link in full_links if any(domain in link.lower() for domain in social_domains)]

    def get_structured_data(self, soup):
        """Extract JSON-LD structured data."""
        json_data = []
        for tag in soup.find_all('script', type='application/ld+json'):
            try:
                data = json.loads(tag.string)
                if isinstance(data, dict) and data.get('@type') == 'Person':
                    json_data.append(data)
                elif isinstance(data, list):
                    json_data.extend(data)
            except Exception:
                continue
        return json_data

    def web_scraper(self, url):
        """Main web scraper to extract personal profile data."""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")
            text = self.clean_text(soup.get_text(separator=' ', strip=True))

            email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
            phone_pattern = r'\+?\d[\d\s\-()]{7,}\d'
            dob_pattern = r'\b(?:\d{1,2}[/-]){2}\d{2,4}\b'

            full_name = self.extract_name(text, soup)
            dobs = self.extract_with_patterns(dob_pattern, text)
            emails = self.extract_with_patterns(email_pattern, text)
            phones = self.extract_with_patterns(phone_pattern, text)

            job_keywords = ['Engineer', 'Developer', 'Manager', 'Designer', 'Analyst', 'Consultant', 'Lecturer']
            jobs = [match for job in job_keywords for match in re.findall(rf'\b\w+\s{job}\b', text)]

            edu_keywords = ['University', 'College', 'School', 'Institute']
            education = [match for word in edu_keywords for match in re.findall(rf'\b(?:{word})\s(?:of\s)?[A-Z][a-z]+(?:\s[A-Z][a-z]+)*\b', text)]

            social_links = self.extract_social_links(soup, url)
            json_ld_data = self.get_structured_data(soup)

            # Compile the extracted data
            extracted = {
                "Full Name": full_name,
                "DOBs": dobs[:2] or ["Not found"],
                "Emails": emails[:3] or ["Not found"],
                "Phones": phones[:3] or ["Not found"],
                "Jobs": list(set(jobs))[:3] or ["Not found"],
                "Education": list(set(education))[:3] or ["Not found"],
                "Social Profiles": social_links[:5] or ["Not found"],
                "Structured Data": json_ld_data[:1] or ["No JSON-LD found"]
            }

            # Format the output for easy reading
            result = "\n\n".join(
                f"{key}:\n  - " + "\n  - ".join(
                    [json.dumps(v, indent=2) if isinstance(v, (dict, list)) else str(v)
                     for v in (val if isinstance(val, list) else [val])]
                )
                for key, val in extracted.items()
            )

            return result

        except Exception as e:
            print(f"Scraping error: {e}")
            return None
