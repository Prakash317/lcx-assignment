try:
    import feedparser
    import pyshorteners
    import requests
    from PIL import Image
    from io import BytesIO
    import os
    from requests.auth import HTTPBasicAuth
    from dotenv import load_dotenv

except ImportError as e:
    print(f"Error importing module: {e}")

# Load environment variables from .env file
load_dotenv()

# Read configuration from .env
rss_url = os.getenv("RSS_URL")
pexels_api_key = os.getenv("PEXELS_API_KEY")
api_url = os.getenv("API_URL")
per_page = int(os.getenv("PER_PAGE", 5))

# Function to fetch the latest article from the RSS feed
def fetch_latest_article():
    response = feedparser.parse(rss_url)
    if response.status != 200:
        print(f"Error fetching news: {response.status}")
        return None

    # Get the first entry (latest article)
    latest_entry = response.entries[0]

    data = {
        "title": latest_entry.title,
        "summary": latest_entry.summary,
        "url": latest_entry.link,
        "published": latest_entry.published
    }
    return data

# Function to shorten URL using TinyURL (or you can use any URL shortening service)
def shorten_url(url):
    s = pyshorteners.Shortener()
    return s.tinyurl.short(url)

# Function to fetch an image related to the article from Pexels API
def fetch_image(query):
    url = f'https://api.pexels.com/v1/search?query={query}&per_page={per_page}'
    headers = {'Authorization': pexels_api_key}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data['photos']:
            image_url = data['photos'][0]['src']['original']
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                img_name = "article_image.jpg"
                image = Image.open(BytesIO(image_response.content))
                image.save(img_name)
                print(f"Image downloaded and saved as '{img_name}'")
                return img_name
            else:
                print("Failed to fetch the image.")
                return None
        else:
            print("No images found.")
            return None
    else:
        print(f"Failed to fetch photos from Pexels. Status code: {response.status_code}")
        return None

# Function to upload image and create a post on the Flask API
def upload(image_path, caption, article_url):
    url = api_url + '/upload_article'
    files = {'file': open(image_path, 'rb')}
    data = {'caption': caption, 'article_url': article_url}

    response = requests.post(url, files=files, data=data)

    if response.status_code == 201:
        print("Post created successfully on Flask app.")
        print(response.json())
    else:
        print("Failed to create post.")
        print(response.text)

# Main function to run the entire automation process
def main():
    # Step 1: Fetch the latest article from the RSS feed
    article_data = fetch_latest_article()
    if not article_data:
        print("No new article found.")
        return

    # Step 2: Generate caption
    caption = f"{article_data['title']}: {article_data['summary']}"
    short_url = shorten_url(article_data['url'])
    full_caption = f"{caption} Read more here: {short_url}"

    # Step 3: Fetch an image related to the article title
    image_path = fetch_image(article_data['title'])
    if not image_path:
        print("No image found or failed to fetch image.")
        return

    # Step 4: Upload the image and create the post on your Flask API
    upload(image_path, full_caption, article_data['url'])

if __name__ == "__main__":
    main()