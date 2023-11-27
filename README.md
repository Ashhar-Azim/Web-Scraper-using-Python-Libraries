# Web Scraper

This is a web scraping tool that allows you to extract and store data from web pages. You can specify a URL, HTML element, and relevance keywords to scrape data. The scraped data can be saved in various formats, and you can also search and filter the collected data.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Scraping Process](#scraping-process)
- [Filtering Data](#filtering-data)
- [Throttling](#throttling)
- [Contributing](#contributing)

## Requirements

- Python 3.x
- Required Python packages: `tkinter`, `requests`, `bs4 (Beautiful Soup)`, `json`, `csv`, `xml.etree.ElementTree`, `random`, `time`, `logging`, `os`, `sys`, `re`, `hashlib`, `urllib.parse`, `urllib.robotparser`, `threading`

## Installation

1. Clone this repository or download the source code.
2. Install the required Python packages using `pip`:

```pip install requests beautifulsoup4```


Run the script:

```python main.py```

## Usage 

1. Provide the following information in the GUI:

 - URL: Enter the URL of the web page you want to scrape.
 - HTML Element: Specify the HTML element you want to scrape (e.g., "p", "h1", "div").
 - Relevance Keywords (comma-separated): Enter keywords to filter relevant data.
 - Maximum Pages: Set the number of pages to scrape (for pagination).
 - Storage Format: Choose the format to save the scraped data (JSON, CSV, XML, or TXT).
 - Request Delay (seconds): Set the delay between requests.

2. Click the "Start Scraping" button to initiate the scraping process. You can monitor the progress using the progress bar.

3. After scraping is complete, you can search and filter the collected data by entering search terms in the "Search Data" field and clicking "Search and Filter."

4. The filtered results will be displayed in the text area below.

## Configuration

The script can be configured with user agents, rate limiting parameters, and cache settings in the source code.

## Scraping Process

 The script starts by checking if the page is allowed by the robots.txt file using user agents.
 Cached data is loaded if available to reduce redundant requests.
 The specified web page is scraped, and data is collected based on the HTML element and relevance keywords.
 Scraped data is cached to avoid repetitive requests.
 The data can be saved in various formats (JSON, CSV, XML, TXT).

## Filtering Data

 After scraping, you can search and filter the data by entering search terms and clicking "Search and Filter."
 Filtered results are displayed in the text area.

## Throttling

 You can set the request delay in seconds to control the rate of scraping. Use the "Set Request Delay" button to adjust this value.

## Contributing

 Feel free to contribute to this project by opening issues or pull requests



