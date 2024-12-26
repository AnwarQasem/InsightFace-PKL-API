from fastapi import FastAPI, File, UploadFile, Path
from fastapi.responses import FileResponse
from typing import List
import insightface
import pickle
import cv2
import numpy as np
from pathlib import Path as PPath
import time

app = FastAPI()

TEMP_DIR = PPath("temp")
RESULTS_DIR = PPath("results")
TEMP_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)

model = insightface.app.FaceAnalysis()
model.prepare(ctx_id=0)

def clean_old_files(directory: PPath, max_age_seconds: int = 3600):
    current_time = time.time()
    for file in directory.iterdir():
        if file.is_file() and (current_time - file.stat().st_mtime > max_age_seconds):
            file.unlink()

@app.post("/create_pkl/{filename}")
async def create_pkl(filename: str, images: List[UploadFile] = File(...)):
    # Clean up old files
    clean_old_files(TEMP_DIR)
    clean_old_files(RESULTS_DIR)

    combined_embeddings = []
    for image in images:
        try:
            temp_file_path = TEMP_DIR / image.filename
            contents = await image.read()
            with temp_file_path.open("wb") as f:
                f.write(contents)

            img = cv2.imread(str(temp_file_path))
            if img is None:
                raise ValueError(f"Unable to load image: {image.filename}")

            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            faces = model.get(img)

            if faces:
                combined_embeddings.append(faces[0].embedding)
            else:
                print(f"No faces detected in {image.filename}")

        except Exception as e:
            print(f"Error processing {image.filename}: {e}")
            return {"status": False, "message": f"Error processing {image.filename}: {e}"}

        finally:
            if temp_file_path.exists():
                temp_file_path.unlink()

    if combined_embeddings:
        final_embedding = np.mean(combined_embeddings, axis=0)
        pkl_filename = RESULTS_DIR / f"{filename}.pkl"
        with pkl_filename.open('wb') as f:
            pickle.dump(final_embedding, f)
        return {"status": True, "file": str(pkl_filename)}
    else:
        return {"status": False, "message": "No faces detected in the uploaded images."}

@app.get("/results/{filename}.pkl")
async def download_pkl(filename: str):
    # Clean up old files
    clean_old_files(TEMP_DIR)
    clean_old_files(RESULTS_DIR)

    pkl_path = RESULTS_DIR / f"{filename}.pkl"
    if not pkl_path.exists():
        return {"status": False, "message": "File not found."}
    return FileResponse(str(pkl_path), media_type="application/octet-stream", filename=f"{filename}.pkl")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
