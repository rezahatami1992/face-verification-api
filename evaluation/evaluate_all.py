import requests
import os
import json
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score, roc_curve
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

class FaceVerificationEvaluator:
    """Evaluate face verification model on multiple datasets"""
    
    def __init__(self, api_url="http://localhost:8000/verify_faces"):
        self.api_url = api_url
        self.results = {}
        
    def load_pairs(self, pairs_file):
        """Load pairs from pairs text file"""
        pairs = []
        
        with open(pairs_file, 'r') as f:
            lines = f.readlines()
        
        # Remove empty lines
        lines = [line.strip() for line in lines if line.strip()]
        
        # Split into positive and negative samples
        positive_samples = []
        negative_samples = []
        
        for line in lines:
            parts = line.split()
            if len(parts) >= 2:
                img = parts[0]
                label = int(parts[1])
                
                if label == 1:
                    positive_samples.append(img)
                else:
                    negative_samples.append(img)
        
        # Create same-person pairs from positive samples (consecutive pairs)
        for i in range(0, len(positive_samples) - 1, 2):
            pairs.append({
                'img1': positive_samples[i],
                'img2': positive_samples[i + 1],
                'label': 1  # Same person
            })
        
        # Create different-person pairs from negative samples (consecutive pairs)
        for i in range(0, len(negative_samples) - 1, 2):
            pairs.append({
                'img1': negative_samples[i],
                'img2': negative_samples[i + 1],
                'label': 0  # Different person
            })
        
        return pairs
    
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
                    return None
                    
        except Exception as e:
            print(f"⚠️  Error: {e}")
            return None
    
    def find_optimal_threshold(self, y_true, y_scores):
        """Find optimal threshold using ROC curve"""
        fpr, tpr, thresholds = roc_curve(y_true, y_scores)
        
        # Find threshold that maximizes (TPR - FPR)
        optimal_idx = np.argmax(tpr - fpr)
        optimal_threshold = thresholds[optimal_idx]
        
        return optimal_threshold
    
    def evaluate_dataset(self, dataset_name, pairs_file, images_dir, max_pairs=None):
        """Evaluate model on a single dataset"""
        print(f"\n{'='*60}")
        print(f"📊 Evaluating {dataset_name}")
        print(f"{'='*60}")
        
        # Load pairs
        print("📥 Loading pairs...")
        pairs = self.load_pairs(pairs_file)
        
        # Apply max_pairs AFTER creating balanced dataset
        if max_pairs:
            # Take half from same-person, half from different-person
            same_pairs = [p for p in pairs if p['label'] == 1]
            diff_pairs = [p for p in pairs if p['label'] == 0]
            
            half = max_pairs // 2
            pairs = same_pairs[:half] + diff_pairs[:half]
        
        print(f"✅ Loaded {len(pairs)} pairs")
        
        # Count labels
        label_counts = {0: 0, 1: 0}
        for p in pairs:
            label_counts[p['label']] += 1
        print(f"   Same person: {label_counts[1]}, Different: {label_counts[0]}")
        
        y_true = []
        y_scores = []
        failed = 0
        
        print(f"🔄 Processing pairs...")
        for pair in tqdm(pairs, desc=f"{dataset_name}"):
            # Construct full paths
            img1_path = os.path.join(images_dir, pair['img1'])
            img2_path = os.path.join(images_dir, pair['img2'])
            
            # Check if images exist
            if not os.path.exists(img1_path):
                print(f"\n⚠️  Missing: {img1_path}")
                failed += 1
                continue
                
            if not os.path.exists(img2_path):
                print(f"\n⚠️  Missing: {img2_path}")
                failed += 1
                continue
            
            # Get similarity score
            score = self.verify_pair(img1_path, img2_path)
            
            if score is not None:
                y_true.append(pair['label'])
                y_scores.append(score / 100.0)  # Normalize to [0,1]
            else:
                failed += 1
        
        if len(y_true) == 0:
            print(f"❌ No valid pairs processed for {dataset_name}")
            return None
        
        # Find optimal threshold
        optimal_threshold = self.find_optimal_threshold(y_true, y_scores)
        optimal_threshold_percent = optimal_threshold * 100
        
        # Calculate predictions with optimal threshold
        y_pred_optimal = [1 if score >= optimal_threshold else 0 for score in y_scores]
        
        # Also calculate with default threshold (0.65)
        default_threshold = 0.65
        y_pred_default = [1 if score >= default_threshold else 0 for score in y_scores]
        
        # Calculate metrics for optimal threshold
        accuracy_optimal = accuracy_score(y_true, y_pred_optimal)
        precision_optimal = precision_score(y_true, y_pred_optimal, zero_division=0)
        recall_optimal = recall_score(y_true, y_pred_optimal, zero_division=0)
        
        # Calculate metrics for default threshold
        accuracy_default = accuracy_score(y_true, y_pred_default)
        precision_default = precision_score(y_true, y_pred_default, zero_division=0)
        recall_default = recall_score(y_true, y_pred_default, zero_division=0)
        
        # Calculate AUC
        try:
            auc = roc_auc_score(y_true, y_scores)
        except:
            auc = 0.0
        
        # Calculate True Acceptance Rate (TAR) and False Acceptance Rate (FAR)
        # For optimal threshold
        tp_opt = sum([1 for t, p in zip(y_true, y_pred_optimal) if t == 1 and p == 1])
        fp_opt = sum([1 for t, p in zip(y_true, y_pred_optimal) if t == 0 and p == 1])
        tn_opt = sum([1 for t, p in zip(y_true, y_pred_optimal) if t == 0 and p == 0])
        fn_opt = sum([1 for t, p in zip(y_true, y_pred_optimal) if t == 1 and p == 0])
        
        tar_opt = tp_opt / (tp_opt + fn_opt) if (tp_opt + fn_opt) > 0 else 0
        far_opt = fp_opt / (fp_opt + tn_opt) if (fp_opt + tn_opt) > 0 else 0
        
        # For default threshold
        tp_def = sum([1 for t, p in zip(y_true, y_pred_default) if t == 1 and p == 1])
        fp_def = sum([1 for t, p in zip(y_true, y_pred_default) if t == 0 and p == 1])
        tn_def = sum([1 for t, p in zip(y_true, y_pred_default) if t == 0 and p == 0])
        fn_def = sum([1 for t, p in zip(y_true, y_pred_default) if t == 1 and p == 0])
        
        tar_def = tp_def / (tp_def + fn_def) if (tp_def + fn_def) > 0 else 0
        far_def = fp_def / (fp_def + tn_def) if (fp_def + tn_def) > 0 else 0
        
        results = {
            'dataset': dataset_name,
            'total_pairs': len(pairs),
            'evaluated_pairs': len(y_true),
            'failed_pairs': failed,
            'auc': round(auc, 4),
            'optimal_threshold': {
                'threshold': round(optimal_threshold_percent, 2),
                'accuracy': round(accuracy_optimal * 100, 2),
                'precision': round(precision_optimal * 100, 2),
                'recall': round(recall_optimal * 100, 2),
                'tar': round(tar_opt * 100, 2),
                'far': round(far_opt * 100, 2),
                'tp': tp_opt, 'fp': fp_opt, 'tn': tn_opt, 'fn': fn_opt
            },
            'default_threshold': {
                'threshold': 65.0,
                'accuracy': round(accuracy_default * 100, 2),
                'precision': round(precision_default * 100, 2),
                'recall': round(recall_default * 100, 2),
                'tar': round(tar_def * 100, 2),
                'far': round(far_def * 100, 2),
                'tp': tp_def, 'fp': fp_def, 'tn': tn_def, 'fn': fn_def
            }
        }
        
        return results
    
    def print_results(self, results):
        """Print evaluation results"""
        print(f"\n{'='*60}")
        print(f"📈 Results for {results['dataset']}")
        print(f"{'='*60}")
        print(f"Total Pairs:       {results['total_pairs']}")
        print(f"Evaluated Pairs:   {results['evaluated_pairs']}")
        print(f"Failed Pairs:      {results['failed_pairs']}")
        print(f"AUC:               {results['auc']}")
        
        print(f"\n--- With Optimal Threshold ({results['optimal_threshold']['threshold']}%) ---")
        print(f"Accuracy:          {results['optimal_threshold']['accuracy']}%")
        print(f"Precision:         {results['optimal_threshold']['precision']}%")
        print(f"Recall:            {results['optimal_threshold']['recall']}%")
        print(f"TAR (True Accept): {results['optimal_threshold']['tar']}%")
        print(f"FAR (False Accept):{results['optimal_threshold']['far']}%")
        
        print(f"\n--- With Default Threshold (65%) ---")
        print(f"Accuracy:          {results['default_threshold']['accuracy']}%")
        print(f"Precision:         {results['default_threshold']['precision']}%")
        print(f"Recall:            {results['default_threshold']['recall']}%")
        print(f"TAR (True Accept): {results['default_threshold']['tar']}%")
        print(f"FAR (False Accept):{results['default_threshold']['far']}%")
        print(f"{'='*60}")
    
    def save_results(self, all_results, output_file='evaluation/results_all.json'):
        """Save all evaluation results to JSON file"""
        with open(output_file, 'w') as f:
            json.dump(all_results, f, indent=4)
        print(f"\n✅ Results saved to {output_file}")

def main():
    # Dataset configurations
    DATASETS = {
        'CALFW': {
            'pairs_file': r'C:\Users\reza.hatami\Desktop\datasets\calfw\pairs_CALFW.txt',
            'images_dir': r'C:\Users\reza.hatami\Desktop\datasets\calfw\aligned images'
        },
        'CPLFW': {
            'pairs_file': r'C:\Users\reza.hatami\Desktop\datasets\cplfw\pairs_CPLFW.txt',
            'images_dir': r'C:\Users\reza.hatami\Desktop\datasets\cplfw\aligned images'
        }
    }
    
    print("="*60)
    print("🎯 Face Verification Model - Multi-Dataset Evaluation")
    print("="*60)
    
    # Check if server is running
    try:
        response = requests.get("http://localhost:8000")
        if response.status_code != 200:
            print("❌ Server is not running! Start server first:")
            print("   python server.py")
            return
        print("✅ Server is running")
    except:
        print("❌ Cannot connect to server! Start server first:")
        print("   python server.py")
        return
    
    # Initialize evaluator
    evaluator = FaceVerificationEvaluator()
    all_results = {}
    
    # Evaluate each dataset
    for dataset_name, config in DATASETS.items():
        # Check if dataset exists
        if not os.path.exists(config['pairs_file']):
            print(f"\n⚠️  {dataset_name} pairs file not found: {config['pairs_file']}")
            continue
        
        if not os.path.exists(config['images_dir']):
            print(f"\n⚠️  {dataset_name} images directory not found: {config['images_dir']}")
            continue
        
        # Run evaluation (remove max_pairs for full evaluation)
        results = evaluator.evaluate_dataset(
            dataset_name,
            config['pairs_file'],
            config['images_dir'],
            max_pairs=None  # Full evaluation - 6000 pairs
        )
        
        if results:
            evaluator.print_results(results)
            all_results[dataset_name] = results
    
    # Save all results
    if all_results:
        evaluator.save_results(all_results)
        
        print("\n" + "="*60)
        print("🎉 Evaluation Complete!")
        print("="*60)
        print("\n📊 Summary:")
        for dataset_name, results in all_results.items():
            opt_acc = results['optimal_threshold']['accuracy']
            def_acc = results['default_threshold']['accuracy']
            print(f"{dataset_name:10s} - Optimal: {opt_acc}% | Default: {def_acc}% | AUC: {results['auc']}")
    else:
        print("\n❌ No datasets were evaluated successfully")

if __name__ == "__main__":
    main()