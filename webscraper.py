import tkinter as tk
from tkinter import ttk, messagebox
import requests
from bs4 import BeautifulSoup
import json
import csv
import xml.etree.ElementTree as ET
import random
import time
import logging
import os
import sys
import re
import hashlib
from urllib.parse import urljoin
from urllib import robotparser

#### Configure logging ###########################
# Create a logging instance
logger = logging.getLogger("web_scraper")
logger.setLevel(logging.DEBUG)  # Set the minimum logging level

# Create a log formatter
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Create a log file handler
log_file = "scraper_log.txt"
log_file_handler = logging.FileHandler(log_file)
log_file_handler.setFormatter(log_formatter)
logger.addHandler(log_file_handler)

# Create a console handler for real-time logging
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_formatter)
logger.addHandler(console_handler))
#################################################

# Directory to store cached data
cache_directory = "cache"
if not os.path.exists(cache_directory):
    os.makedirs(cache_directory)

# List of user agent headers for rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    # Add more user agents here
]

# Rate limiting parameters
REQUEST_DELAY = 2  # Delay between requests in seconds

# Function to check robots.txt compliance
def is_allowed_by_robots(url):
    try:
        rp = robotparser.RobotFileParser()
        rp.set_url(urljoin(url, "/robots.txt"))
        rp.read()
        return rp.can_fetch(USER_AGENTS[0], url)
    except Exception as e:
        print(f"An error occurred while checking robots.txt compliance for {url}: {e}")
        return False

# Function to scrape and process a single page
def scrape_page(url, target_element, relevance_keywords, scraped_data, progress_var):
    cache_file = os.path.join(cache_directory, hashlib.md5(url.encode()).hexdigest() + '.cache')

    if os.path.exists(cache_file):
        with open(cache_file, 'r', encoding='utf-8') as cache:
            cached_data = json.load(cache)
            scraped_data.extend(cached_data)
            logger.info(f"Loaded data from cache for {url}")
    else:
        try:
            headers = {'User-Agent': random.choice(USER_AGENTS)}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            elements = soup.find_all(target_element)

            if elements:
                for element in elements:
                    text = element.text

                    # Check for relevance based on user-defined keywords
                    text_lower = text.lower()
                    relevant = any(keyword in text_lower for keyword in relevance_keywords)

                    # If relevant, store the content in the data list
                    if relevant:
                        scraped_data.append(text)

            # Log a successful scrape
            logger.info(f"Scraped data from {url}")

            # Cache the scraped data
            with open(cache_file, 'w', encoding='utf-8') as cache:
                json.dump(scraped_data, cache, ensure_ascii=False, indent=2)
        except requests.exceptions.RequestException as request_error:
            # Log a failed scrape
            logger.error(f"Failed to retrieve the web page '{url}'. Error: {request_error}")
        except Exception as error:
            # Log a general error, including traceback
            logger.error(f"An error occurred while scraping the page: {error}", exc_info=True)
        time.sleep(REQUEST_DELAY)

    progress_var.set(len(scraped_data))  # Update the progress vari

# Function to apply regular expressions to the scraped data
def apply_regular_expression(scraped_data, regex_pattern):
    filtered_data = []
    for item in scraped_data:
        matches = re.findall(regex_pattern, item)
        if matches:
            filtered_data.extend(matches)
    return filtered_data

# Function to save data to various file formats
def save_data(scraped_data, file_format):
    try:
        if file_format == 'json':
            with open('scraped_data.json', 'w') as json_file:
                json.dump(scraped_data, json_file, indent=2)
            logging.info("Data saved to 'scraped_data.json'.")
        elif file_format == 'csv':
            with open('scraped_data.csv', 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerows([[item] for item in scraped_data])
            logging.info("Data saved to 'scraped_data.csv'.")
        elif file_format == 'xml':
            root = ET.Element('data')
            for item in scraped_data:
                element = ET.SubElement(root, 'item')
                element.text = item
            tree = ET.ElementTree(root)
            tree.write('scraped_data.xml')
            logging.info("Data saved to 'scraped_data.xml'.")
        elif file_format == 'txt':
            with open('scraped_data.txt', 'w') as txt_file:
                for item in scraped_data:
                    txt_file.write(item + '\n')
            logging.info("Data saved to 'scraped_data.txt'.")
    except Exception as error:
        # Log an error while saving
        logging.error(f"An error occurred while saving data: {error}")

# Function to search and filter data
def search_and_filter_data(scraped_data):
    filtered_data = []
    
    try:
        search_query = search_entry.get().lower()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return

    try:
        if search_query:
            filtered_data = [item for item in scraped_data if search_query in item.lower()]
            if not filtered_data:
                messagebox.showinfo("Filter Results", "No matching data found")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while filtering: {e}")

    try:
        result_text.delete(1.0, tk.END)
        for idx, item in enumerate(filtered_data, start=1):
            result_text.insert(tk.END, f"{idx}: {item}\n")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while displaying results: {e}")

# Function to start the scraping process
def start_scraping(progress_var):
    try:
        url = url_entry.get()
        target_element = element_entry.get()
        relevance_keywords = keyword_entry.get().split(',')
        max_pages = int(pages_entry.get())
        file_format = format_var.get()

        scraped_data = scrape_with_pagination(url, target_element, relevance_keywords, max_pages, progress_var)

        save_data(scraped_data, file_format)
        messagebox.showinfo("Scraping Complete", "Scraping and data saving complete.")
    except Exception as error:
        messagebox.showerror("Error", f"An error occurred: {error}")

# Function to scrape data with pagination
def scrape_with_pagination(url, target_element, relevance_keywords, max_pages):
    scraped_data = []

    try:
        for page in range(1, max_pages + 1):
            page_url = f"{url}?page={page}"  # Adjust the URL for pagination
            scrape_page(page_url, target_element, relevance_keywords, scraped_data)
    except Exception as e:
        print(f"An error occurred while scraping page {page}: {e}")

    return scraped_data

# Function to implement throttling
def set_request_delay():
    global request_delay
    try:
        new_delay = float(request_delay_entry.get())
        if new_delay >= 0:
            request_delay = new_delay
            messagebox.showinfo("Request Delay Set", f"Request delay set to {request_delay} seconds.")
        else:
            messagebox.showerror("Invalid Input", "Please enter a non-negative delay value.")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid numeric value for the delay.")


# Create and place widgets in the GUI
# Create the main application window ##################################
root = tk.Tk()
root.title("Web Scraper")
root.geometry("600x400")
root.configure(bg="#333")

# Define dark-themed style
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", foreground="white", background="#444")
style.configure("TLabel", foreground="white", background="#333")
style.configure("TEntry", background="#444", foreground="white")
######################################################################

url_label = ttk.Label(root, text="URL:")
url_entry = ttk.Entry(root, width=40)
element_label = ttk.Label(root, text="HTML Element:")
element_entry = ttk.Entry(root)
keyword_label = ttk.Label(root, text="Relevance Keywords (comma-separated):")
keyword_entry = ttk.Entry(root)
pages_label = ttk.Label(root, text="Maximum Pages:")
pages_entry = ttk.Entry(root, width=5)
format_label = ttk.Label(root, text="Storage Format:")
format_var = tk.StringVar(value="json")
format_options = ttk.Combobox(root, textvariable=format_var, values=["json", "csv", "xml", "txt"])
start_button = ttk.Button(root, text="Start Scraping", command=start_scraping)

search_label = ttk.Label(root, text="Search Data:")
search_entry = ttk.Entry(root, width=40)
search_button = ttk.Button(root, text="Search and Filter", command=search_and_filter_data)
result_text = tk.Text(root, wrap=tk.WORD, width=40, height=10)

request_delay_label = ttk.Label(root, text="Request Delay (seconds):")
request_delay_entry = ttk.Entry(root)
set_delay_button = ttk.Button(root, text="Set Request Delay", command=set_request_delay)

url_label.grid(row=0, column=0, pady=10)
url_entry.grid(row=0, column=1, padx=10, pady=10)
element_label.grid(row=1, column=0, pady=10)
element_entry.grid(row=1, column=1, padx=10, pady=10)
keyword_label.grid(row=2, column=0, pady=10)
keyword_entry.grid(row=2, column=1, padx=10, pady=10)
pages_label.grid(row=3, column=0, pady=10)
pages_entry.grid(row=3, column=1, padx=10, pady=10)
format_label.grid(row=4, column=0, pady=10)
format_options.grid(row=4, column=1, padx=10, pady=10)
start_button.grid(row=5, column=0, columnspan=2, pady=20)

search_label.grid(row=6, column=0, pady=10)
search_entry.grid(row=6, column=1, padx=10, pady=10)
search_button.grid(row=7, column=0, columnspan=2, pady=10)
result_text.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

request_delay_label.grid(row=9, column=0, pady=10)
request_delay_entry.grid(row=9, column=1, padx=10, pady=10)
set_delay_button.grid(row=10, column=0, columnspan=2, pady=10)

# Create a progress bar to monitor scraping progress
progress_label = ttk.Label(root, text="Scraping Progress:")
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
progress_label.grid(row=11, column=0, pady=10)
progress_bar.grid(row=11, column=1, padx=10, pady=10)

root.mainloop()
