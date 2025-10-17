import os
import uuid
import shutil
from fastapi import UploadFile, HTTPException

# Set your Cloudinary credentials
# ==============================
from dotenv import load_dotenv
load_dotenv()

# Import the Cloudinary libraries
# ==============================
import cloudinary
import cloudinary.uploader

# Set configuration parameter: return "https" URLs by setting secure=True  
# ==============================
config = cloudinary.config(secure=True)

# Log the configuration
# ==============================
print("****1. Set up and configure the SDK:****\nCredentials: ", config.cloud_name, config.api_key, "\n")


ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

def is_image_file(filename: str) -> bool:
    _, ext = os.path.splitext(filename.lower())
    return ext in ALLOWED_EXTENSIONS

async def save_upload_file(upload_file: UploadFile, dir: str) -> str:
    if not is_image_file(upload_file.filename):
        raise HTTPException(status_code=400, detail="Only image files are allowed (.jpg, .jpeg, .png, .webp)")

    unique_filename = uuid.uuid4().hex
    folder_path = dir.strip("/")  # remove leading/trailing slashes if any

    try:
        file_bytes = await upload_file.read()
        await upload_file.close()

        result = cloudinary.uploader.upload(
            file_bytes,
            folder=folder_path,
            public_id=unique_filename,
            resource_type="image",
            overwrite=True,
        )

        secure_url = result.get("secure_url")
        if not secure_url:
            raise HTTPException(status_code=500, detail="Upload succeeded but no secure URL returned.")

        return secure_url

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


def delete_file_if_exists(secure_url: str):
    """
    Accepts a Cloudinary secure_url and extracts the public_id to delete the image.
    Example input:
    https://res.cloudinary.com/<cloud_name>/image/upload/v1234567890/folder/filename.jpg
    Extracts: folder/filename (without version and extension)
    """
    try:
        # Split after /upload/ to get the path: v1234567890/folder/filename.jpg
        path_part = secure_url.split("/upload/")[-1]

        # Remove version number: v1234567890/folder/filename.jpg → folder/filename.jpg
        parts = path_part.split("/", 1)
        if len(parts) != 2:
            raise ValueError("Invalid Cloudinary URL format.")

        _, public_path = parts
        # Remove the extension: folder/filename.jpg → folder/filename
        public_id = public_path.rsplit(".", 1)[0]

        # Delete from Cloudinary
        cloudinary.uploader.destroy(public_id, resource_type="image")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")














# def uploadImage():

#   # Upload the image and get its URL
#   # ==============================

#   # Upload the image.
#   # Set the asset's public ID and allow overwriting the asset with new versions
#   cloudinary.uploader.upload("https://cloudinary-devs.github.io/cld-docs-assets/assets/images/butterfly.jpeg", public_id="quickstart_butterfly", unique_filename = False, overwrite=True)

#   # Build the URL for the image and save it in the variable 'srcURL'
#   srcURL = CloudinaryImage("quickstart_butterfly").build_url()

#   # Log the image URL to the console. 
#   # Copy this URL in a browser tab to generate the image on the fly.
#   print("****2. Upload an image****\nDelivery URL: ", srcURL, "\n")

#   def getAssetInfo():

#   # Get and use details of the image
#   # ==============================

#   # Get image details and save it in the variable 'image_info'.
#   image_info=cloudinary.api.resource("quickstart_butterfly")
#   print("****3. Get and use details of the image****\nUpload response:\n", json.dumps(image_info,indent=2), "\n")

#   # Assign tags to the uploaded image based on its width. Save the response to the update in the variable 'update_resp'.
#   if image_info["width"]>900:
#     update_resp=cloudinary.api.update("quickstart_butterfly", tags = "large")
#   elif image_info["width"]>500:
#     update_resp=cloudinary.api.update("quickstart_butterfly", tags = "medium")
#   else:
#     update_resp=cloudinary.api.update("quickstart_butterfly", tags = "small")

#   # Log the new tag to the console.
#   print("New tag: ", update_resp["tags"], "\n")


# old_code

# BASE_RESOURCE_PATH = "resource"
# ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

# def is_image_file(filename: str) -> bool:
#     _, ext = os.path.splitext(filename.lower())
#     return ext in ALLOWED_EXTENSIONS

# async def save_upload_file(upload_file: UploadFile, dir: str) -> str:
#     if not is_image_file(upload_file.filename):
#         raise HTTPException(status_code=400, detail="Only image files are allowed (.jpg, .jpeg, .png, .webp)")

#     save_dir = os.path.join(BASE_RESOURCE_PATH, dir)
#     os.makedirs(save_dir, exist_ok=True)

#     _, ext = os.path.splitext(upload_file.filename)
#     filename = f"{uuid.uuid4().hex}{ext}"
#     file_path = os.path.join(save_dir, filename)

#     try:
#         contents = await upload_file.read()
#         with open(file_path, "wb") as f:
#             f.write(contents)
#     finally:
#         await upload_file.close()

#     return f"/resource/{dir}/{filename}"

# async def delete_file_if_exists(path: str):
#     full_path = os.path.join(BASE_RESOURCE_PATH, *path.replace("/resource/", "").split("/"))
#     if os.path.exists(full_path):
#         os.remove(full_path)
