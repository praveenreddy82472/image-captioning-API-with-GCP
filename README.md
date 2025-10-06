# 🧠 AI-Powered Image Captioning API — Google Cloud Run + Vertex AI + Firestore

## 🌟 Project Story

Every image tells a story — but what if we could teach AI to *describe it* automatically?

This project brings that idea to life.  
I built a **serverless Image Captioning API** on **Google Cloud Platform (GCP)** that generates intelligent, human-like captions for any uploaded image.  
It’s powered by **Google Vertex AI’s Gemini Vision model**, served through a **Cloud Run REST API**, and logs all results in **Firestore** — all seamlessly orchestrated with **Cloud Build** and **Artifact Registry**.

---

## 🧩 The Motivation

In many AI applications — from accessibility to e-commerce — there’s a need to automatically describe images:
- 🛍️ Product image tagging  
- 🌍 Accessibility (auto alt-text for visually impaired users)  
- 📰 Content moderation and media organization  
- 📸 Automated metadata generation  

Traditional approaches require complex on-prem pipelines.  
So, I designed a **fully managed, serverless solution** where everything runs on GCP — scalable, cost-efficient, and production-ready.

---

## 🏗️ Architecture Overview

![Architecture](https://github.com/praveenreddy82472/image-captioning-API-with-GCP/blob/main/image_cap_api.png)

### **Data Flow**
1. A user uploads an image via an HTTP POST request to the `/caption` endpoint.
2. The image is temporarily stored in **Cloud Storage**.
3. The API invokes **Vertex AI’s Gemini model** to generate a descriptive caption.
4. The generated caption and metadata are stored in **Firestore**.
5. A JSON response with the caption, image URI, and timestamp is returned to the user.

---

## ☁️ Tech Stack

| Service / Tool | Purpose |
|----------------|----------|
| **Cloud Run** | Hosts and scales the REST API |
| **Vertex AI (Gemini Vision)** | Generates image captions using multimodal AI |
| **Firestore** | Stores image metadata and captions |
| **Cloud Storage (GCS)** | Stores uploaded images |
| **Cloud Build** | Builds Docker images from source |
| **Artifact Registry** | Stores container images for deployment |
| **Python + Flask** | Implements the REST API |

---

## 🧠 Core Idea

At its core, the API accepts an image, uploads it to Cloud Storage, sends it to the Gemini model, and returns a **human-readable caption** — all within seconds.

Example:
> Input: 🖼️ A street photo  
> Output: *“A busy European street lined with parked cars and trees on a sunny afternoon.”*

---

# 🧪 API Usage

### **Request**
```bash
curl -X POST "https://caption-api-t4ktkkp2ca-uc.a.run.app/caption" ^
  -H "Content-Type: multipart/form-data" ^
  -F "file=@\"D:\path\to\test.jpg\""
```


# Response

{
  "filename": "28d0aa0b-e5bc-43af-95e9-d7c3519d47ff.jpg",
  "image_uri": "gs://image-caption-bucket/28d0aa0b-e5bc-43af-95e9-d7c3519d47ff.jpg",
  "caption": "A busy European street lined with parked cars and trees.",
  "timestamp": "2025-10-04T16:37:32.784244"
}

# 🌍 Real-World Applications

- 🛍️ Product image labeling for e-commerce
- ♿ Accessibility support (auto alt-text)
- 📸 Photo management & organization
- 📰 News and media classification
