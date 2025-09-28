import requests
import json
import os

def test_basic_connection():
    """Test if server is running"""
    url = "http://localhost:8000"
    
    try:
        response = requests.get(url)
        print(f"✅ Server Status: {response.status_code}")
        print(f"✅ Response: {response.json()}")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running!")
        return False

def test_face_verification(image1_path, image2_path):
    """Test face verification with two images"""
    url = "http://localhost:8000/verify_faces"
    
    try:
        # Check if files exist
        if not os.path.exists(image1_path):
            print(f"❌ Image 1 not found: {image1_path}")
            return
            
        if not os.path.exists(image2_path):
            print(f"❌ Image 2 not found: {image2_path}")
            return
        
        # Open and send images
        with open(image1_path, 'rb') as f1, open(image2_path, 'rb') as f2:
            files = {
                'image1': ('image1.jpg', f1, 'image/jpeg'),
                'image2': ('image2.jpg', f2, 'image/jpeg')
            }
            
            print("🚀 Sending images to server...")
            response = requests.post(url, files=files)
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Face Verification Results:")
                print(f"   Similarity Score: {result['similarity_score']}%")
                print(f"   Same Person: {result['is_same_person']}")
                print(f"   Confidence: {result['confidence']}")
            else:
                print(f"❌ Error {response.status_code}: {response.text}")
                
    except Exception as e:
        print(f"❌ Error: {e}")

def create_sample_images():
    """Create sample image paths for testing"""
    # You'll need to add your own image files
    image1 = "C:/Users/reza.hatami/Desktop/ryan reynolds.jpg"  # Add your image path
    image2 = "C:/Users/reza.hatami/Desktop/ryan gosling.jpg"  # Add your image path
    
    return image1, image2

if __name__ == "__main__":
    print("🔍 Face Verification Client")
    print("=" * 30)
    
    # Test server connection
    if test_basic_connection():
        print("\n" + "=" * 30)
        
        # Test with sample images
        img1, img2 = create_sample_images()
        
        print(f"📸 Testing with images:")
        print(f"   Image 1: {img1}")
        print(f"   Image 2: {img2}")
        
        test_face_verification(img1, img2)
