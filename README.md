# LLM-Powered Web Scraper with Crawl4AI  

This project is an AI-enhanced web scraper built with **Crawl4AI**. It leverages **large language models (LLMs)** like OpenAI's GPT, Claude, and DeepSeek to intelligently extract **local business data** from YellowPages. All collected data is saved in structured **CSV files** for easy analysis.  

## 🌟 Features  

✅ **Extract Business Information** – Automatically scrape business names, contact details, and more.  
✅ **AI Data Extraction & Processing** – Use LLMs to collect, clean, format, and enhance extracted data.  
✅ **Customizable Scraper** – Easily adapt it to different websites and data types.  
✅ **Flexible LLM Integration** – Choose from multiple AI providers (GPT-4, Claude, DeepSeek, etc.).  

## 🔧 Adaptability  

While designed for **YellowPages**, this scraper can be adapted to **any website**. Simply switch the URL to your target site, modify the **LLM scraping instructions** to adjust how the AI processes and extracts relevant information, and define new **data models** to specify the exact fields you want to collect. With these changes, you can scrape **any structured data** with ease! 🚀

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
- LLM provider (OpenAI, Gemini, Claude,...)
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
If you have any questions or suggestions, feel free to contact me at aymenMir1001@gmail.com.
