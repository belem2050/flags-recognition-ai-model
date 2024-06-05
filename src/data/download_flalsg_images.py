from google_images_download import google_images_download

def download_flags(query, limit=10):
    response = google_images_download.googleimagesdownload()
    args = {
        "keywords": query,
        "limit": limit,
        "print_urls": True,
        "format": "jpg",
        "output_directory": "data/raw",
        "image_directory": query.replace(" ", "_"),
        "safe_search": True
    }

    try:
        response.download(args)
    except:
        print("Error while trying to download")


if __name__ =="__main__":
    
    countries = ["Burkina Faso", "Ivoiry Coast", "Mali", "Niger", "Nigeria"]

    for country in countries:
        print(f"Downloading images for {country} flag")
        query = country + " flag"
        download_flags(query)