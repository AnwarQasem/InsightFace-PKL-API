# InsightFace PKL API

This project provides a FastAPI-based service for processing images, generating facial embeddings using InsightFace, and storing them in a single `.pkl` file. The API includes functionality for uploading images, cleaning temporary files, and downloading generated `.pkl` files.

## Features

- Accepts multiple image uploads.
- Combines facial embeddings from multiple images into a single `.pkl` file.
- Automatically cleans temporary files and results older than one hour.
- Provides download access to the generated `.pkl` files.

## Requirements

- Python 3.8 or higher
- Dependencies (install via `pip`):
  - `fastapi`
  - `uvicorn`
  - `opencv-python-headless`
  - `insightface`
  - `numpy`

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/AnwarQasem/InsightFace-PKL-API.git
   cd InsightFace-PKL-API
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Start the API Server

Run the following command to start the server:
```bash
uvicorn app:app --host 0.0.0.0 --port 8001
```

### API Endpoints

#### 1. Create PKL File
- **URL:** `/create_pkl/{filename}`
- **Method:** `POST`
- **Description:** Upload multiple images to generate a single `.pkl` file representing one person.
- **Request Parameters:**
  - `filename`: Name of the `.pkl` file to be generated.
- **Request Body:** List of image files.
- **Response:**
  - `status: true` and the path of the generated `.pkl` file on success.
  - `status: false` and an error message on failure.

#### 2. Download PKL File
- **URL:** `/results/{filename}.pkl`
- **Method:** `GET`
- **Description:** Download a generated `.pkl` file.
- **Request Parameters:**
  - `filename`: Name of the `.pkl` file to download.
- **Response:** The requested file or an error message if the file does not exist.

## File Management

The application manages the following directories:

- **`temp/`**: Temporary storage for uploaded files. Files older than 1 hour are deleted automatically.
- **`results/`**: Stores generated `.pkl` files. Files older than 1 hour are deleted automatically.

## Example Usage

### Create a PKL File
Use `curl` or any HTTP client to upload images:
```bash
curl -X POST "http://localhost:8001/create_pkl/person1" \
     -F "images=@image1.jpg" \
     -F "images=@image2.jpg"
```

### Download a PKL File
```bash
curl -O "http://localhost:8001/results/person1.pkl"
```

## Notes

- Ensure the `temp/` and `results/` directories are writable by the application.
- InsightFace must be properly installed and configured to work with your environment.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

