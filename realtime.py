from bs4 import BeautifulSoup
import requests

# Add headers to mimic a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

url = 'https://internshala.com/internships/python%2Fdjango-internship/'

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for bad status codes
    
    soup = BeautifulSoup(response.text, 'lxml')
    
    # Use a more general class name
    jobs = soup.find_all('div', class_='individual_internship')
    
    if jobs:
        print(f"Found {len(jobs)} job listings.")
        for job in jobs:
            # Print out the raw HTML of the job listing for debugging
            #print("Job HTML:", job.prettify())
            
            title = job.find('h3', class_='job-internship-name')
            company = job.find('p', class_='company-name')
            
            # Print debug information about what was found
            if title:
                print(f"Title found: {title.text.strip()}")
            else:
                print("Title not found")
                
            if company:
                print(f"Company found: {company.text.strip()}")
            else:
                print("Company not found")
            
            if title and company:
                print(f"Title: {title.text.strip()}")
                print(f"Company: {company.text.strip()}")
                print("---")
            else:
                print("One of title or company not found, skipping this job listing.")
    else:
        print("No job listings found. The page structure might have changed.")
    
except requests.RequestException as e:
    print(f"An error occurred: {e}")
