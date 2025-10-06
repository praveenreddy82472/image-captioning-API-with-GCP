import functions_framework
from google.cloud import storage
from google.cloud import firestore
from google import genai
from google.genai import types
from datetime import datetime

PROJECT_ID = "image-captioning-api"
REGION = "us-central1"
IMAGE_BUCKET = "image-caption-bucket"

# Initialize Firestore client outside the function for reuse
db = firestore.Client(project=PROJECT_ID)

@functions_framework.cloud_event
def image_upload_trigger(cloudevent):
    bucket_name = cloudevent.data["bucket"]
    file_name = cloudevent.data["name"]
    gcs_uri = f"gs://{bucket_name}/{file_name}"
    timestamp = datetime.utcnow()
    print(f"New file uploaded: {file_name} in bucket: {bucket_name}")
    print(f"GCS URI: {gcs_uri}")

    # Initialize GenAI client
    client = genai.Client(vertexai=True, project=PROJECT_ID, location="global")

    # Generate caption using Gemini
    model_name = "gemini-2.5-flash-lite-preview-09-2025"
    response = client.models.generate_content(
        model=model_name,
        contents=[
            "What is shown in this image?",
            types.Part.from_uri(
                file_uri=gcs_uri,
                mime_type="image/jpeg"  # use jpg/png as appropriate
            ),
        ],
    )

    caption = response.text
    print("Generated Caption:", caption)
    # Save to Firestore
    doc_ref = db.collection("image_captions").document(file_name)
    doc_ref.set({
        "image_uri": gcs_uri,
        "caption": caption,
        "timestamp": timestamp
    })

    print(f"Caption logged in Firestore for image: {file_name}")