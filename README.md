# Face Verification API

A high-performance face verification REST API built with FastAPI and InsightFace for robust facial recognition and similarity comparison.

## 🎯 Features

- **State-of-the-art Face Recognition**: Powered by InsightFace ArcFace model
- **REST API**: Simple HTTP endpoints for easy integration
- **High Accuracy**: Evaluated on academic benchmarks (LFW, CP-LFW, CA-LFW)
- **Fast Processing**: Optimized for real-time face comparison
- **Easy Deployment**: Minimal dependencies and straightforward setup

## 📋 Requirements

- Python 3.8+
- Windows/Linux/MacOS
- 4GB RAM minimum
- Internet connection (first run only, for model download)

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/face-verification-api.git
cd face-verification-api
```

### 2. Create Virtual Environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Start Server

```bash
python server.py
```

Server will start at `http://localhost:8000`

On first run, InsightFace model (~100MB) will be downloaded automatically.

## 📖 API Usage

### Verify Two Faces

**Endpoint:** `POST /verify_faces`

**Request:**
```python
import requests

url = "http://localhost:8000/verify_faces"

with open("image1.jpg", "rb") as f1, open("image2.jpg", "rb") as f2:
    files = {
        'image1': ('img1.jpg', f1, 'image/jpeg'),
        'image2': ('img2.jpg', f2, 'image/jpeg')
    }
    response = requests.post(url, files=files)
    print(response.json())
```

**Response:**
```json
{
    "similarity_score": 85.42,
    "is_same_person": true,
    "confidence": "high",
    "model": "InsightFace ArcFace",
    "status": "success"
}
```

### Health Check

**Endpoint:** `GET /health`

```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
    "status": "healthy",
    "service": "face_verification",
    "model_loaded": true
}
```

## 🧪 Testing with Client

Run the included test client:

```bash
python client.py
```

**Note:** Update image paths in `client.py` before running.

## 📊 Model Evaluation

Evaluate model accuracy on academic datasets:

```bash
python evaluation/evaluate_lfw.py
```

## 📊 Benchmark Results

| Dataset | Accuracy | AUC | Description |
|---------|----------|-----|-------------|
| CPLFW | 95.73% | 0.97 | Celebrity pairs - excellent performance |
| CALFW | 58.13% | 0.74 | Cross-age - challenging for current model |

### Supported Datasets

- **LFW** (Labeled Faces in the Wild)
- **CP-LFW** (Celebrity-Pairs)
- **CA-LFW** (Cross-Age)

### Evaluation Metrics

- Accuracy
- Precision
- Recall
- AUC (Area Under Curve)

**Note:** Download datasets separately from official sources.

## 🏗️ Project Structure

```
face-verification-api/
├── server.py              # FastAPI server
├── client.py              # Test client
├── evaluation/
│   ├── evaluate_lfw.py    # LFW dataset evaluator
│   └── results.json       # Evaluation results
├── requirements.txt       # Python dependencies
└── README.md             # Documentation
```

## ⚙️ Configuration

### Similarity Threshold

Default threshold for face matching: **65%**

Modify in `server.py`:
```python
is_same_person = similarity_score > 65.0  # Adjust threshold
```

### Server Port

Change port in `server.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8000)  # Change port
```

## 🔧 Technical Details

### Model Architecture

- **Face Detection**: RetinaFace
- **Face Recognition**: ArcFace (ResNet-100)
- **Embedding Size**: 512 dimensions
- **Similarity Metric**: Cosine similarity

### API Framework

- **Backend**: FastAPI
- **Server**: Uvicorn ASGI
- **Image Processing**: OpenCV + PIL

## 📈 Performance

- **Inference Time**: ~200-300ms per pair (CPU)
- **Memory Usage**: ~500MB (model loaded)
- **Throughput**: ~3-5 requests/second (single worker)

## 🐛 Troubleshooting

### Model Download Issues

If model fails to download:
```bash
# Manual cache clear
rm -rf ~/.insightface/models/
python server.py  # Retry download
```

### ONNX Runtime Errors

```bash
pip install onnxruntime --upgrade
```

### Image Format Issues

Supported formats: JPG, PNG, BMP
Recommended: RGB images, resolution > 112x112

## 📝 API Documentation

Interactive API documentation available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- [InsightFace](https://github.com/deepinsight/insightface) for the face recognition model
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
- [LFW Dataset](http://vis-www.cs.umass.edu/lfw/) for evaluation benchmarks

## 📧 Contact

For questions or issues, please open an issue on GitHub.

---

**Built with ❤️ using InsightFace and FastAPI**
