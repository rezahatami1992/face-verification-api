import requests
import os

def test_pair(img1_path, img2_path, expected_label):
    """Test a single pair"""
    
    if not os.path.exists(img1_path):
        print(f"❌ Image 1 not found: {img1_path}")
        return
    
    if not os.path.exists(img2_path):
        print(f"❌ Image 2 not found: {img2_path}")
        return
    
    print(f"✅ Testing pair:")
    print(f"   Image 1: {os.path.basename(img1_path)}")
    print(f"   Image 2: {os.path.basename(img2_path)}")
    print(f"   Expected: {'Same person' if expected_label == 1 else 'Different person'}")
    
    with open(img1_path, 'rb') as f1, open(img2_path, 'rb') as f2:
        files = {
            'image1': ('img1.jpg', f1, 'image/jpeg'),
            'image2': ('img2.jpg', f2, 'image/jpeg')
        }
        
        response = requests.post('http://localhost:8000/verify_faces', files=files)
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n📊 API Response:")
            print(f"   Similarity: {result['similarity_score']}%")
            print(f"   Prediction: {'Same' if result['is_same_person'] else 'Different'}")
            print(f"   Confidence: {result['confidence']}")
        else:
            print(f"❌ Error: {response.status_code}")

# Test CALFW same person
base = r'C:\Users\reza.hatami\Desktop\datasets\calfw\aligned images'
print("="*50)
print("CALFW - Same Person Test")
print("="*50)
test_pair(
    os.path.join(base, 'Carl_Reiner_0001.jpg'),
    os.path.join(base, 'Carl_Reiner_0003.jpg'),
    expected_label=1
)

print("\n" + "="*50)
print("CALFW - Different Person Test")
print("="*50)
# Get two different person images from negative samples
test_pair(
    os.path.join(base, 'Jeffrey_Archer_0002.jpg'),
    os.path.join(base, 'Luis_Ernesto_Derbez_Bautista_0003.jpg'),
    expected_label=0
)