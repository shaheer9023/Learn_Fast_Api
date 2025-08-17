# main.py
import time
import requests
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

# ✅ Sample image URLs (module-level par rakho)
SAMPLE_IMAGE_URLS = [
    "https://picsum.photos/200/300",
    "https://picsum.photos/id/10/250/250",
    "https://picsum.photos/seed/demo/300/200",
    "https://placekitten.com/300/300",
    "https://placecats.com/300/200"
]

# ✅ Background task: images download karta hai
async def download_images(image_urls: list[str]):
    start = time.time()
    for idx, img_url in enumerate(image_urls, start=1):
        try:
            # filename banane ka simple tareeqa (last path part + index so duplicates na banein)
            last_part = (img_url.rstrip("/").split("/")[-1] or "image")
            img_name = f"{idx}_{last_part}.jpg"

            # image download
            response = requests.get(img_url, timeout=30)
            response.raise_for_status()

            # file save
            with open(img_name, "wb") as f:
                f.write(response.content)

            print(f"{img_name} downloaded ✅")

        except Exception as e:
            print(f"❌ Failed to download {img_url}: {e}")

    print(f"Total time taken: {time.time() - start:.2f}s")

# ✅ FastAPI endpoint
@app.post("/download", status_code=202)
async def download(image_urls: list[str], background_task: BackgroundTasks):
    background_task.add_task(download_images, image_urls)
    return {"message": "Images are being downloaded in the background"}

