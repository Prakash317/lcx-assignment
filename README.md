# lcx-assignment
news-feeder

1. Clone Repo:
https://github.com/Prakash317/lcx-assignment.git

2. Install required dependencies

pip install -r requirements.txt
Flask
feedparser
requests
pyshorteners
Pillow
APScheduler

3. Configuration
Need to configure the application by setting up a .env file in the root directory with the following values.

4. How It Works
Flask API (app.py):
Image Upload & Post Creation: The Flask app provides an endpoint (/upload_article) that accepts a POST request with an article's caption, URL, and an image file.
Shortening URLs: The article URL is shortened using the pyshorteners library.
Image Handling: The image is saved locally after being processed, and it’s returned in the response along with the caption and shortened URL.

Main Script (news_feeder.py):
Fetch Latest Article: It fetches the latest article from the provided RSS feed using feedparser.
Generate Caption: It generates a short caption for the article and shortens its URL.
Fetch Related Image: It uses the Pexels API to fetch an image related to the article title.
Upload Image & Create Post: It sends the image, caption, and URL to the Flask API for processing and post creation.

5. Running the Application
1. Start the Flask API Server (app.py)
To start the Flask app, run the following command in the terminal:
    python app.py
    
This will start the Flask server, which will listen for requests on http://127.0.0.1:5000/. The server will handle image uploads and post creation requests

5. Scheduling Automation
Automating news_feeder.py with Cron 
You can use cron to automate the execution of news_feeder.py at regular intervals (e.g., every hour).