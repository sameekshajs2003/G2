import imaplib
import email
from email.header import decode_header
from bs4 import BeautifulSoup
import json
import requests
import csv

# IMAP settings
IMAP_SERVER = 'imap.gmail.com'
IMAP_PORT = 993
EMAIL = 'xyz@gmail.com'
PASSWORD = '**** **** **** ****'

# Decode Subject of the email
def decode_subject(subject):
    decoded_subject = []
    for part, encoding in decode_header(subject):
        if isinstance(part, bytes):
            decoded_subject.append(part.decode(encoding or 'utf-8'))
        else:
            decoded_subject.append(part)
    return ''.join(decoded_subject)

# Function to check if a product is listed on G2
def check_product_on_g2(product_name, api_token):
    # Construct the API request URL
    api_url = "https://data.g2.com/api/v1/products"
    
    # Set up the headers with the authorization token
    headers = {
        "Authorization": f"Token token={api_token}",
        "Content-Type": "application/vnd.api+json"
    }

    # Set up the query parameters
    params = {
        "filter[name]": product_name
    }

    try:
        # Send the API request
        response = requests.get(api_url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the JSON response
        data = response.json()

        # Check if any products are returned
        if data["meta"]["record_count"] > 0:
            return True  # Product is listed on G2
        else:
            return False  # Product is not listed on G2

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None  # Return None if an error occurs


# Connect to IMAP server
mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)

# Login to email account
mail.login(EMAIL, PASSWORD)

# Select the mailbox (inbox)
mail.select('inbox')

# Search for emails from Google Alerts
status, email_ids = mail.search(None, '(FROM "Google Alerts")', '(SUBJECT "Google Alert - software product")')

# Fetch the latest email
latest_email_id = email_ids[0].split()[-1]
status, email_data = mail.fetch(latest_email_id, "(RFC822)")

# Parse the email data
raw_email = email_data[0][1]
email_message = email.message_from_bytes(raw_email)

# Extract relevant information (such as body) from the email
products = []

# Iterate through the parts of the email
for part in email_message.walk():
    # Check if the part is HTML
    if part.get_content_type() == "text/html":
        html_content = part.get_payload(decode=True).decode(part.get_content_charset())
        soup = BeautifulSoup(html_content, 'html.parser')
        script_tag = soup.find('script', {'data-scope': 'inboxmarkup'})
        json_data = json.loads(script_tag.string)

        # Extract titles from updates
        for snippet in json_data['updates']['snippets']:
            products.append(snippet['message'])

products_not_listed_on_g2 = []
# Check if the products are listed on G2
for product_name in products:
    # Replace 'API_TOKEN' with the provided secret token
    api_token = 'API_TOKEN'

    # Check if the product is listed on G2
    is_listed_on_g2 = check_product_on_g2(product_name, api_token)

    if is_listed_on_g2 is True:
        print(f"{product_name} is listed on G2.")
    elif is_listed_on_g2 is False:
        print(f"{product_name} is not listed on G2.")
        products_not_listed_on_g2.append(product_name)
    else:
        print("An error occurred while checking the product on G2.")

# Function to write products not listed on G2 to a CSV file
def write_to_csv(products_not_listed):
    with open('products_not_listed_on_g2.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Product Name'])
        for product_name in products_not_listed:
            writer.writerow([product_name])

if products_not_listed_on_g2:
    write_to_csv(products_not_listed_on_g2)
    print("Products not listed on G2 have been saved to 'products_not_listed_on_g2.csv'.")

# Close the connection
mail.close()
mail.logout()
