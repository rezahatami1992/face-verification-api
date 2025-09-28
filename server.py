from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
from PIL import Image
import io
import uvicorn
import insightface
from insightface.app import FaceAnalysis

app = FastAPI(title="Face Verification API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize InsightFace model (global variable)
face_model = None

def load_face_model():
    """Load InsightFace model on startup"""
    global face_model
    try:
        face_model = FaceAnalysis(providers=['CPUExecutionProvider'])
        face_model.prepare(ctx_id=0, det_size=(640, 640))
        print("✅ InsightFace model loaded successfully")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        face_model = None

@app.on_event("startup")
async def startup_event():
    """Load model when server starts"""
    load_face_model()

def preprocess_image(image_bytes):
    """Convert uploaded image to OpenCV format"""
    try:
        image = Image.open(io.BytesIO(image_bytes))
        
        if image.mode != 'RGB':
            image = image.convert('RGB')
            
        img_array = np.array(image)
        img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        
        return img_bgr
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Image processing error: {str(e)}")

def calculate_similarity(img1, img2):
    """Calculate face similarity using InsightFace"""
    if face_model is None:
        raise HTTPException(status_code=500, detail="Face model not loaded")
    
    try:
        # Detect faces
        faces1 = face_model.get(img1)
        faces2 = face_model.get(img2)
        
        if len(faces1) == 0:
            raise HTTPException(status_code=400, detail="No face detected in image 1")
        if len(faces2) == 0:
            raise HTTPException(status_code=400, detail="No face detected in image 2")
        
        # Get embeddings (take first face if multiple detected)
        embedding1 = faces1[0].embedding
        embedding2 = faces2[0].embedding
        
        # Calculate cosine similarity
        similarity = np.dot(embedding1, embedding2) / (
            np.linalg.norm(embedding1) * np.linalg.norm(embedding2)
        )
        
        # Convert to percentage (0-100)
        similarity_percent = float((similarity + 1) * 50)  # Scale from [-1,1] to [0,100]
        
        return round(similarity_percent, 2)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Similarity calculation error: {str(e)}")

@app.get("/")
def read_root():
    model_status = "loaded" if face_model is not None else "not loaded"
    return {
        "message": "Face Verification API is running!",
        "model_status": model_status,
        "status": "active"
    }

@app.post("/verify_faces")
async def verify_faces(
    image1: UploadFile = File(...),
    image2: UploadFile = File(...)
):
    """Compare two face images and return similarity score"""
    
    try:
        # Read uploaded files
        img1_bytes = await image1.read()
        img2_bytes = await image2.read()
        
        # Preprocess images
        img1 = preprocess_image(img1_bytes)
        img2 = preprocess_image(img2_bytes)
        
        # Calculate similarity using InsightFace
        similarity_score = calculate_similarity(img1, img2)
        
        # Determine if same person (InsightFace threshold: typically 60-70%)
        is_same_person = similarity_score > 65.0
        
        if similarity_score > 75:
            confidence = "high"
        elif similarity_score > 60:
            confidence = "medium"
        else:
            confidence = "low"
        
        return {
            "similarity_score": similarity_score,
            "is_same_person": is_same_person,
            "confidence": confidence,
            "model": "InsightFace ArcFace",
            "status": "success"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "face_verification",
        "model_loaded": face_model is not None
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
