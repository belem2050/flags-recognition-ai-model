import os
import requests
from bs4 import BeautifulSoup

def download_images(query : str, num_pages=1, limit_per_page=20, output_dir="data/raw"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    image_urls = set()
    for page in range(num_pages):
        start_index = page * limit_per_page
        search_url = f"https://www.google.com/search?q={query}&tbm=isch&start={start_index}"
        try:
            response = requests.get(search_url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            soup = BeautifulSoup(response.text, "html.parser")
            for img in soup.find_all("img"):
                img_url = img.get("src")
                if img_url and img_url.startswith("http"):
                    image_urls.add(img_url)
        except Exception as e:
            print(f"Error fetching image URLs from page {page + 1}: {e}")
    
    # Download images
    count = 0
    for img_url in image_urls:
        try:
            print(f"Downloading image from: {img_url}")
            response = requests.get(img_url)
            image_name = query.replace(" ", "_")
            if response.status_code == 200:
                img_data = response.content
                with open(os.path.join(output_dir, f"{image_name}_{count+1}.jpg"), "wb") as f:
                    f.write(img_data)
                print(f"Downloaded image {count+1}")
                count += 1
                if count >= limit_per_page:
                    break
            else:
                print(f"Failed to download image. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error downloading image: {e}")

# Example usage
if __name__ =="__main__":
    countries =["Burkina Faso", "Ivory coast", "France"]

    for country in countries:
        query = country + " flag"
        download_images(query, num_pages=5, limit_per_page=5, output_dir=os.path.join("data", "raw", country.replace(" ", "_")))
