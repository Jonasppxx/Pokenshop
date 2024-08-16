import requests
from urllib.parse import urlparse, unquote
from bs4 import BeautifulSoup
import os
import time
import json

def fetch_url_content(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad status codes
    return response.text

def parse_url(url):
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.split('/')
    # Assuming the URL structure is consistent
    set_name = path_parts[2] if len(path_parts) > 2 else 'Unknown'
    name = path_parts[3] if len(path_parts) > 3 else 'Unknown'
    return unquote(name), unquote(set_name)

def extract_price(html):
    soup = BeautifulSoup(html, 'html.parser')
    price_element = soup.find('td', id='used_price').find('span', class_='price js-price')
    if price_element:
        price = price_element.text.strip().replace('$', '')
        return float(price)
    return None

def extract_images(name):
    image_dir = f"C:/Users/jonas/OneDrive/Desktop/GITHUB/Pokemonshop/images/{name}"
    images = []
    if os.path.exists(image_dir):
        for file_name in os.listdir(image_dir):
            if file_name.lower().endswith('.jpg'):
                images.append(os.path.join('images', name, file_name).replace('\\', '/'))
    image = images[0] if len(images) > 0 else None
    hover_image = images[1] if len(images) > 1 else None
    return image, hover_image

def load_existing_products(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return {"products": []}

def save_products(file_path, products):
    with open(file_path, 'w') as file:
        json.dump(products, file, indent=4)

def main():
    urls_file = 'urls.txt'
    products_file = 'products.json'
    results = []

    with open(urls_file, 'r') as file:
        urls = file.readlines()

    total_urls = len(urls)
    processed_count = 0

    existing_products = load_existing_products(products_file)
    existing_product_names = {product['name']: product for product in existing_products['products']}

    for url in urls:
        url = url.strip()
        if not url:
            continue
        try:
            name, set_name = parse_url(url)
            html_content = fetch_url_content(url)
            price = extract_price(html_content)
            image, hover_image = extract_images(name)
            
            # Create directory for the product images if it doesn't exist
            image_dir = f"C:/Users/jonas/OneDrive/Desktop/GITHUB/Pokemonshop/images/{name}"
            if not os.path.exists(image_dir):
                os.makedirs(image_dir)
            
            product = {
                'name': name,
                'set': set_name,
                'price': price,
                'image': image,
                'hoverImage': hover_image
            }
            existing_product_names[name] = product
            processed_count += 1
            print(f"Processed {processed_count} of {total_urls}")
            time.sleep(1)  # Wait for 1 second after processing each product
        except Exception as e:
            print(f"Error processing URL {url}: {e}")

    # Update the products list
    existing_products['products'] = list(existing_product_names.values())
    save_products(products_file, existing_products)

    # Output results
    for result in existing_products['products']:
        print(f"Name: {result['name']}, Set: {result['set']}, Price: {result['price']}, Image: {result['image']}, HoverImage: {result['hoverImage']}")

if __name__ == '__main__':
    main()