import socket
import requests
from bs4 import BeautifulSoup
import csv
from geoip2.database import Reader


# Function to retrieve website content
def get_website(url):
    response = requests.get(url)
    return response.text

# Function to resolve IP address using DNS resolution
def resolve_ip_address(hostname):
    try:
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except Exception as e:
        print(f"Error gethostbyname : {str(e)}")
        return None

# Function to geolocate IP address and extract country information
def geolocate_ip(ip_address):
    reader = Reader('GeoLite2-City.mmdb')  # Path to the GeoIP2 database file
    try:
        response = reader.city(ip_address)
        country = response.country.name
        city = response.city.name
        return country, city
    except Exception as e:
        print(ip_address)
        print(f"Error geolocating IP address: {str(e)}")
        return None, None


# Function to process <li> elements
def process_list_items(html_content,output_file):
    soup = BeautifulSoup(html_content, 'html.parser')
    li_elements = soup.find_all('li', class_='ListItem')

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['TextDNS', 'IP Address', 'City', 'Country'])  # Write header row

        for li in li_elements:
            span = li.find('span')
            if span is not None:
                textdns = span.get_text()
                ip_address = resolve_ip_address(textdns)
                country, city = geolocate_ip(ip_address)
                writer.writerow([textdns, ip_address, city, country])

# Example usage
website_url = 'https://nordvpn.com/ovpn/'
html_content = get_website(website_url)
output_file = 'geolocation.csv'
process_list_items(html_content, output_file)

