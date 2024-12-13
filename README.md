# README: Job Scraper API

## Overview
The Job Scraper API is a web application built with FastAPI that allows users to scrape job listings from Indeed.com based on a given job title and location. It extracts relevant job details such as the title, company name, location, salary, job description, and more, then processes the data for local storage in a CSV file and uploads it to a Supabase database for further use.

## Features

### Scraping Functionality:
- Scrapes job listings from Indeed.com based on user input (job title and location).
- Collects details like job title, company name, location, salary, benefits, and job descriptions.

### Data Export:
- Saves extracted data locally as a CSV file.
- Uploads the data to a Supabase table for database storage.

### API Endpoints:
- A root endpoint to confirm service availability.
- An endpoint to initiate the scraping process.

### Modular Design:
- The project is divided into reusable modules for scraping, processing, and database operations.

## Project Structure
```
job_scraper/
│
├── main.py              # Entry point for the FastAPI application
├── scraping.py          # Handles web scraping logic
├── supabase_utils.py    # Manages Supabase database interactions
├── requirements.txt     # List of dependencies
└── README.md            # Documentation for the project
```

## Technologies Used
- **Backend Framework:** FastAPI
- **Web Scraping:** Selenium, BeautifulSoup
- **Data Processing:** Pandas
- **Database:** Supabase
- **Other Tools:** WebDriver Manager, Uvicorn

## Prerequisites
- Python 3.10+
- Google Chrome and ChromeDriver (managed automatically by WebDriver Manager)
- A Supabase account with a database table set up:
  - **Table Name:** Job_listing
  - **Columns:**
    - POSITION
    - COMPANY NAME
    - LOCATION
    - SALARY
    - JOB LINK
    - BENEFITS
    - DESCRIPTION
    - EMPLOYMENT TYPE

## Setup and Installation

### Clone the Repository:
```bash
git clone https://github.com/your-repo/job_scraper.git
cd job_scraper
```

### Install Dependencies:
```bash
pip install -r requirements.txt
```

### Configure Supabase:
1. Open `supabase_utils.py`.
2. Replace `url` and `key` with your Supabase URL and API key.

### Run the API:
```bash
uvicorn main:app --reload
```

### Access the API:
Open your browser and go to:
```
http://127.0.0.1:8000/docs
```

## API Endpoints

### Root Endpoint
- **URL:** `/`
- **Method:** `GET`
- **Description:** Confirms the service is running.
- **Response:**
```json
{
  "message": "Welcome to the Job Scraper API"
}
```

### Scrape Endpoint
- **URL:** `/scrape/`
- **Method:** `POST`
- **Parameters:**
  - `job_title` (string, required): The title of the job to search for (e.g., "Data Analyst").
  - `location` (string, required): The location of the job (e.g., "Remote").
- **Description:** Scrapes job listings, saves data locally as a CSV, and uploads it to Supabase.
- **Response:**
```json
{
  "message": "Job data scraped and saved successfully!",
  "csv_path": "output.csv"
}
```

## Example Usage

### Request:
```bash
curl -X POST "http://127.0.0.1:8000/scrape/" -d "job_title=Data Analyst" -d "location=Remote"
```

### Response:
```json
{
    "message": "Job data scraped and saved successfully!",
    "csv_path": "output.csv"
}
```

## CSV Output
The job data is saved locally as `output.csv` with the following structure:
```
POSITION        COMPANY NAME    LOCATION        SALARY      JOB LINK        BENEFITS        DESCRIPTION     EMPLOYMENT TYPE
Data Analyst    TechCorp        Remote, USA     $80,000     https://job-link.com/1  Health, 401k    Job details     Full-time
Junior Analyst  BizSolutions    New York, USA   $50,000     https://job-link.com/2  None            Job details     Part-time
```

## Error Handling
- If no job links are found, the API returns:
```json
{
  "detail": "No job links found."
}
```
- If scraping fails or data extraction is incomplete:
```json
{
  "detail": "No job data could be extracted."
}
```

## Deployment

### Local Deployment:
Run the app locally with Uvicorn:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Docker Deployment:
Create a Dockerfile with the following content:
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run the Docker image:
```bash
docker build -t job_scraper .
docker run -p 8000:8000 job_scraper
```

## Future Improvements
- Add support for other job boards (e.g., LinkedIn, Glassdoor).
- Implement user authentication for secure access.
- Schedule automated scraping tasks using a job scheduler like Celery.
- Optimize scraping logic to handle large-scale data efficiently.

## Author
[Your Name] - [Your Email]

## License
This project is licensed under the MIT License.
