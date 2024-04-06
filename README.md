# G2
G2 - Hackathon, 2024

## Problem Statement 1 
G2 is the largest software marketplace in the world, with over 165,000 listed 
products and real reviews. Our mission is to help every software buyer make 
informed purchasing decisions. To achieve this, we want all B2B software products to 
be listed on G2 as soon as they become generally available. While this is common 
practice in North America, Asia, and some other countries, there are regions where 
G2 has low visibility and companies do not list their products with us. Therefore, we 
want to identify such products and get them listed on G2 proactively. As an aspiring 
Computer Science graduate, we would like you to develop a system that periodically 
identifies new GA products (daily, weekly, or monthly), checks their availability on G2 
using the API provided below, and provides a list of any products that are not yet 
listed on G2 (this could be in a database or a CSV file). 

## About the Script (G2.py)
This script retrieves emails from a Gmail inbox, extracts product names from Google Alerts emails, checks if these products are listed on G2, and saves the list of products not listed on G2 to a CSV file.

## Features

- Connects to a Gmail inbox using IMAP.
- Parses emails from Google Alerts to extract product names.
- Utilizes the G2 API to check if products are listed on G2.
- Saves products not listed on G2 to a CSV file.

## Prerequisites

- Python 3.x installed on your system.
- Required Python libraries installed: `imaplib`, `email`, `bs4`, `json`, `requests`, `csv`.

## Configuration

- IMAP_SERVER: IMAP server address (e.g., for Gmail, use 'imap.gmail.com').
- IMAP_PORT: Port number for IMAP server (e.g., for Gmail with SSL, use 993).
- EMAIL: Your email address.
- PASSWORD: Your email password.
- G2_API_TOKEN: Your G2 API token.
