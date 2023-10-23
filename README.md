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
- [License](#license)

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

 Feel free to contribute to this project by opening issues or pull requests on the [GitHub repository](https://github.com/Ashhar-Azim/Web-Scraper-using-Python-Libraries).

## License

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

1. The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

2. Users of the Software are responsible for complying with the rules and terms of use set by the respective websites, services, or platforms where the Software is applied. It is the user's responsibility to ensure that the use of the Software aligns with the website's rules and internet ethics.

3. The Software is provided "as is," without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and noninfringement. In no event shall the authors or copyright holders be liable for any claim, damages, or other liability, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the Software or the use or other dealings in the Software.

By using this software, you agree to abide by the terms and conditions of this license.

For more details, refer to the full text of the [MIT License](https://opensource.org/licenses/MIT)


