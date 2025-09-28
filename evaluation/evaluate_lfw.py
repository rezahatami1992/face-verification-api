import requests
import os
import json
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score
import numpy as np
from tqdm import tqdm

class LFWEvaluator:
    """Evaluate face verification model on LFW dataset"""
    
    def __init__(self, api_url="http://localhost:8000/verify_faces"):
        self.api_url = api_url
        self.results = []
        
    def load_lfw_pairs(self, pairs_file):
        """Load LFW pairs from pairs.txt file"""
        pairs = []
        
        with open(pairs_file, 'r') as f:
            lines = f.readlines()[1:]  # Skip header
            
            for line in lines:
                parts = line.strip().split('\t')
                
                if len(parts) == 3:  # Same person
                    person, img1_idx, img2_idx = parts
                    pairs.append({
                        'person1': person,
                        'img1': int(img1_idx),
                        'person2': person,
                        'img2': int(img2_idx),
                        'label': 1  # Same person
                    })
                elif len(parts) == 4:  # Different persons
                    person1, img1_idx, person2, img2_idx = parts
                    pairs.append({
                        'person1': person1,
                        'img1': int(img1_idx),
                        'person2': person2,
                        'img2': int(img2_idx),
                        'label': 0  # Different person
                    })
        
        return pairs
    
    def get_image_path(self, lfw_dir, person_name, img_idx):
        """Construct image path from LFW directory"""
        img_name = f"{person_name}_{img_idx:04d}.jpg"
        img_path = os.path.join(lfw_dir, person_name, img_name)
        return img_path
    
    def verify_pair(self, img1_path, img2_path):
        """Send pair to API and get similarity score"""
        try:
            with open(img1_path, 'rb') as f1, open(img2_path, 'rb') as f2:
                files = {
                    'image1': ('img1.jpg', f1, 'image/jpeg'),
                    'image2': ('img2.jpg', f2, 'image/jpeg')
                }
                
                response = requests.post(self.api_url, files=files, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                    return result['similarity_score']
                else:
                    print(f"Error: {response.status_code}")
                    return None
                    
        except Exception as e:
            print(f"Error processing pair: {e}")
            return None
    
    def evaluate(self, lfw_dir, pairs_file, max_pairs=None):
        """Run evaluation on LFW dataset"""
        print("🔍 Loading LFW pairs...")
        pairs = self.load_lfw_pairs(pairs_file)
        
        if max_pairs:
            pairs = pairs[:max_pairs]
        
        print(f"📊 Evaluating {len(pairs)} pairs...")
        
        y_true = []
        y_scores = []
        y_pred = []
        
        for pair in tqdm(pairs, desc="Processing"):
            img1_path = self.get_image_path(lfw_dir, pair['person1'], pair['img1'])
            img2_path = self.get_image_path(lfw_dir, pair['person2'], pair['img2'])
            
            # Check if images exist
            if not os.path.exists(img1_path) or not os.path.exists(img2_path):
                print(f"⚠️  Missing images: {img1_path} or {img2_path}")
                continue
            
            # Get similarity score
            score = self.verify_pair(img1_path, img2_path)
            
            if score is not None:
                y_true.append(pair['label'])
                y_scores.append(score / 100.0)  # Normalize to [0,1]
                y_pred.append(1 if score > 65.0 else 0)  # Threshold
        
        # Calculate metrics
        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred)
        recall = recall_score(y_true, y_pred)
        
        try:
            auc = roc_auc_score(y_true, y_scores)
        except:
            auc = 0.0
        
        results = {
            'dataset': 'LFW',
            'total_pairs': len(pairs),
            'evaluated_pairs': len(y_true),
            'accuracy': round(accuracy * 100, 2),
            'precision': round(precision * 100, 2),
            'recall': round(recall * 100, 2),
            'auc': round(auc, 4),
            'threshold': 65.0
        }
        
        return results
    
    def save_results(self, results, output_file='results.json'):
        """Save evaluation results to JSON file"""
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=4)
        print(f"✅ Results saved to {output_file}")

def main():
    # Configuration
    LFW_DIR = r"C:\Users\reza.hatami\Desktop\lfw"  # Change this path
    PAIRS_FILE = r"C:\Users\reza.hatami\Desktop\lfw\pairs.txt"  # Change this path
    
    print("=" * 50)
    print("🎯 Face Verification Model Evaluation")
    print("=" * 50)
    
    # Check if server is running
    try:
        response = requests.get("http://localhost:8000")
        if response.status_code != 200:
            print("❌ Server is not running! Start server first.")
            return
    except:
        print("❌ Cannot connect to server! Start server first.")
        return
    
    # Check if LFW dataset exists
    if not os.path.exists(LFW_DIR):
        print(f"❌ LFW dataset not found at: {LFW_DIR}")
        print("📥 Download LFW dataset from: http://vis-www.cs.umass.edu/lfw/")
        return
    
    # Run evaluation
    evaluator = LFWEvaluator()
    
    # Test with subset first (remove max_pairs for full evaluation)
    results = evaluator.evaluate(LFW_DIR, PAIRS_FILE, max_pairs=100)
    
    # Print results
    print("\n" + "=" * 50)
    print("📊 Evaluation Results:")
    print("=" * 50)
    print(f"Dataset: {results['dataset']}")
    print(f"Total Pairs: {results['total_pairs']}")
    print(f"Evaluated Pairs: {results['evaluated_pairs']}")
    print(f"Accuracy: {results['accuracy']}%")
    print(f"Precision: {results['precision']}%")
    print(f"Recall: {results['recall']}%")
    print(f"AUC: {results['auc']}")
    print(f"Threshold: {results['threshold']}%")
    print("=" * 50)
    
    # Save results
    evaluator.save_results(results, 'evaluation/results.json')

if __name__ == "__main__":
    main()
