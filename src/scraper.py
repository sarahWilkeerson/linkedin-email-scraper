thonimport requests
from bs4 import BeautifulSoup
import csv
import time

class LinkedInScraper:
    def __init__(self, keywords, location, country, email_type, output_file):
        self.keywords = keywords
        self.location = location
        self.country = country
        self.email_type = email_type
        self.output_file = output_file

    def scrape_profiles(self):
        search_query = self.build_search_query()
        profiles = self.search_linkedin(search_query)
        email_data = self.extract_emails(profiles)
        self.save_to_csv(email_data)

    def build_search_query(self):
        query = f"site:linkedin.com/in {self.keywords} {self.location} {self.country}"
        if self.email_type:
            query += f" {self.email_type}"
        return query

    def search_linkedin(self, query):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        url = f"https://www.google.com/search?q={query}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        profiles = [a['href'] for a in soup.find_all('a', href=True) if "linkedin.com/in" in a['href']]
        return profiles

    def extract_emails(self, profiles):
        email_data = []
        for profile in profiles:
            response = requests.get(profile)
            soup = BeautifulSoup(response.text, 'html.parser')
            email = self.find_email(soup)
            if email:
                name = soup.find('title').get_text()
                location = soup.find('span', class_='location').get_text() if soup.find('span', class_='location') else 'Unknown'
                email_data.append({'email': email, 'profileUrl': profile, 'name': name, 'location': location, 'domainType': self.email_type})
        return email_data

    def find_email(self, soup):
        email = None
        email_elements = soup.find_all('a', href=True)
        for elem in email_elements:
            if "mailto:" in elem['href']:
                email = elem['href'].replace("mailto:", "")
                break
        return email

    def save_to_csv(self, email_data):
        with open(self.output_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["email", "profileUrl", "name", "location", "domainType"])
            writer.writeheader()
            writer.writerows(email_data)

if __name__ == "__main__":
    keywords = "Software Engineer"
    location = "New York"
    country = "USA"
    email_type = "gmail"
    output_file = "scraped_emails.csv"
    
    scraper = LinkedInScraper(keywords, location, country, email_type, output_file)
    scraper.scrape_profiles()