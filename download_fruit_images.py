import requests
import re
import os

# Map of product name to Wikimedia Commons File Page
IMAGE_SOURCES = {
    'banana': 'https://commons.wikimedia.org/wiki/File:Banana.png',
    'mango': 'https://commons.wikimedia.org/wiki/File:Mango_inner.png',
    'pineapple': 'https://commons.wikimedia.org/wiki/File:Pineapple_Icon.png',
    'coconut': 'https://commons.wikimedia.org/wiki/File:Coconut.png',
    'strawberry': 'https://commons.wikimedia.org/wiki/File:Strawberry_(transparent_background).png',
    'watermelon': 'https://commons.wikimedia.org/wiki/File:Piece_of_watermelon.png'
}

OUTPUT_DIR = 'static/images'

def get_image_url(page_url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(page_url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch page: {page_url}")
            return None
        
        # Look for the "Original file" link or the main image display
        # Pattern: <a href="https://upload.wikimedia.org/wikipedia/commons/..." class="internal"
        match = re.search(r'href="(https://upload\.wikimedia\.org/wikipedia/commons/[^"]+)" class="internal"', response.text)
        if match:
            return match.group(1)
        
        # Fallback: look for the main image tag
        # <div class="fullImageLink" id="file"><a href="//upload.wikimedia.org/..."
        match = re.search(r'<div class="fullImageLink" id="file"><a href="(//upload\.wikimedia\.org/[^"]+)"', response.text)
        if match:
            return "https:" + match.group(1)
            
        return None
    except Exception as e:
        print(f"Error scraping {page_url}: {e}")
        return None

def download_image(url, filename):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded: {filename}")
            return True
        else:
            print(f"Failed to download image from {url}")
            return False
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    for name, page_url in IMAGE_SOURCES.items():
        print(f"Processing {name}...")
        image_url = get_image_url(page_url)
        if image_url:
            print(f"  Found URL: {image_url}")
            filename = os.path.join(OUTPUT_DIR, f"{name}.png")
            download_image(image_url, filename)
        else:
            print(f"  Could not find image URL for {name}")

if __name__ == '__main__':
    main()
