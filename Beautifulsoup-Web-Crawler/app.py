from flask import Flask
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


def extract_jobs(term):
    url = f"https://remoteok.com/remote-{term}-jobs"
    request = requests.get(url, headers={"User-Agent": "Kimchi"})
    results = []
    if request.status_code == 200:
        soup = BeautifulSoup(request.text, "html.parser")
        jobs = soup.find_all("tr", class_="job")
        for job in jobs:
            company = job.find("h3", itemprop="name")
            position = job.find("h2", itemprop="title")
            location = job.find("div", class_="location")
            if company:
                company = company.string.strip()
            if position:
                position = position.string.strip()
            if location:
                location = location.string.strip()
            if company and position and location:
                job = {
                    'company': company,
                    'position': position,
                    'location': location
                }
                results.append(job)
    else:
        print("Can't get jobs.")
    return results


jobs = extract_jobs("golang")
print(jobs)

if __name__ == '__main__':
    app.run()
