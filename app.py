from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
import pyshorteners

# Load environment variables from .env file
load_dotenv()

# Read configuration from environment variables
upload_folder = os.getenv("UPLOAD_FOLDER", "uploads")  # Set default folder

# Flask app setup
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = upload_folder
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'gif'}

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Function to shorten URL
def shorten_url(url):
    s = pyshorteners.Shortener()
    return s.tinyurl.short(url)

# Endpoint
@app.route('/upload_article', methods=['POST'])
def upload_article():
    # Step 1: Get the data from the form (caption and article URL)
    caption = request.form.get('caption')
    article_url = request.form.get('article_url')

    if not caption or not article_url:
        return jsonify({"error": "Caption and article URL are required"}), 400

    # Step 2: Shorten the article URL
    short_url = shorten_url(article_url)
    full_caption = f"{caption} Read more here: {short_url}"

    # Step 3: Check if an image was included in the request
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        file.save(filepath)

        # try:
        #     image = Image.open(filepath)
        #     image = image.convert("RGB")
        #     image.save(filepath)
        # except Exception as e:
        #     return jsonify({"error": f"Error processing image: {str(e)}"}), 500

        # Return the success response with image URL and caption
        return jsonify({
            "message": "Post created successfully",
            "caption": full_caption,
            "image_url": f"/uploads/{filename}"  # Image URL can use in frontend
        }), 201

    return jsonify({"error": "Invalid file format. Allowed formats are jpg, jpeg, png, gif"}), 400

if __name__ == "__main__":
    # Make sure the upload folder exists
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    app.run(debug=True)