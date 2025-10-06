from flask import Flask, request, jsonify
from google.cloud import firestore, storage
from google import genai
from google.genai import types
from datetime import datetime
import os
import uuid

app = Flask(__name__)

PROJECT_ID = "image-captioning-api"
REGION = "us-central1"
BUCKET_NAME = "image-caption-bucket"   # Reuse same bucket

# Firestore client
db = firestore.Client(project=PROJECT_ID)

# Storage client
storage_client = storage.Client(project=PROJECT_ID)

# GenAI client
client = genai.Client(vertexai=True, project=PROJECT_ID, location="global")

MODEL_NAME = "gemini-2.5-flash-lite-preview-09-2025"


@app.route("/caption", methods=["POST"])
def caption_image():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    filename = f"{uuid.uuid4()}.jpg"

    # Upload to GCS bucket
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(filename)
    blob.upload_from_file(file, content_type="image/jpeg")
    gcs_uri = f"gs://{BUCKET_NAME}/{filename}"

    # Generate caption using Gemini
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[
            "What is shown in this image?",
            types.Part.from_uri(file_uri=gcs_uri, mime_type="image/jpeg"),
        ],
    )

    caption = response.text
    timestamp = datetime.utcnow()

    # Log in Firestore
    doc_ref = db.collection("image_captions").document(filename)
    doc_ref.set({
        "image_uri": gcs_uri,
        "caption": caption,
        "timestamp": timestamp
    })

    return jsonify({
        "filename": filename,
        "image_uri": gcs_uri,
        "caption": caption,
        "timestamp": timestamp.isoformat()
    })


# Required for Cloud Run
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
