# AI Web Scraper with Crawl4AI  

### 👉 **[Learn How to Scrape and Build Lead Lists Easily with Crawl4AI!](https://dev.to/kaymen99/scrape-any-website-fast-and-cheap-with-crawl4ai-3fj1)**  

This project is an AI-powered web scraper built with [**Crawl4AI**](https://docs.crawl4ai.com/). It automates **lead generation** by extracting local business (Dentists, restaurents,...) names, addresses, phone numbers, and more from [**YellowPages**](https://www.yellowpages.ca/). With the help of LLMs like GPT-4o, Claude, and DeepSeek, it intelligently processes data and saves it in **CSV files**, making it ready for outreach or analysis!  

## Features  

- **Extract Business Information** – Scrape business names, contact details, and other key data.  
- **AI-Powered Data Processing** – Use LLMs to clean, format, and enhance the extracted data.  
- **Customizable Scraper** – Adapt it to different websites and data types.  
- **Flexible LLM Integration** – Choose from AI models like GPT-4, Claude, and DeepSeek.  

## Adaptability  

This scraper is designed for **YellowPages** but can be used on **any website**. You can change the target URL, modify the AI instructions to adjust how the data is processed, and define new data fields based on your needs.  

## Potential Use Cases  

- **Lead Generation** – Collect business emails, phone numbers, and addresses to build targeted outreach lists.  
- **Market Research** – Gather real-time industry data to analyze trends and customer behavior.  
- **Competitor Analysis** – Monitor pricing, services, and customer reviews to stay competitive.  
- **AI Data Enrichment** – Use LLMs to clean and categorize data for better insights.  
- **Research & Analysis** – Extract structured data from directories, reports, and other sources for business or academic studies.  

## Project Structure

```
.
├── main.py # Main entry point for the crawler
├── config.py # Contains configuration constants (LLM Models, Base URL, CSS selectors, etc.)
├── models
│ └── business.py # Defines the Local Business data model using Pydantic
├── src
│ ├── utils.py # Utility functions for processing and saving data
│ └── scraper.py # functions for configuring and running the crawler
└── requirements.txt # Python package dependencies
```

# How to Run
## Prerequisites
Ensure you have the following installed:
- Python 3.11+
- LLM provider API key (OpenAI, Gemini, Claude,...)
- Necessary Python libraries (listed in `requirements.txt`)

## Setup
### Clone the Repository
```bash
git clone https://github.com/kaymen99/llm-web-scraper
cd llm-web-scraper
```

### Create and Activate a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Install Required Packages
```bash
pip install -r requirements.txt
playwright install
```

### Set Up Environment Variables
Create a `.env` file in the root directory and add necessary credentials:

```ini
# API keys for LLMs providers, add key for every provider you want to use
OPENAI_API_KEY=""            # OpenAI API key for accessing OpenAI's models and services
GEMINI_API_KEY=""            # Google Cloud API key for accessing Google Cloud services
GROQ_API_KEY=""              # GROQ platform API key for using GROQ's services
```

## Running the scraper

To start the scraper, run:

```bash
python main.py
```

The script will crawl the specified website, extract data page by page, and save the complete venues to a `businesses_data.csv` file in the project directory. Additionally, usage statistics for the LLM strategy will be displayed after crawling.

## Configuration  

The `config.py` file contains key settings for controlling the scraper's behavior. You can modify these values to customize the scraping process:  

- **LLM_MODEL**: The AI model used for data extraction. Supports any LLM from **LiteLLM** (e.g., `gpt-4o`, `claude`, `deepseek-chat`, `gemini-2.0-flash`). 
- **BASE_URL**: The target website to scrape. By default, it extracts **dentists in Toronto** from Yellow Pages, but you can change this to any business category or location.  
- **CSS_SELECTOR**: The HTML selector used to pinpoint business details within the page.  
- **MAX_PAGES**: Limits the number of pages to crawl (default: `3`). Increase this value to scrape more data.  
- **SCRAPER_INSTRUCTIONS**: Custom LLM prompt defining what details to extract .

# Contributing
Contributions are welcome! Please open an issue or submit a pull request for any changes.

# Contact
If you have any questions or suggestions, feel free to contact me at `aymenMir1001@gmail.com`.
