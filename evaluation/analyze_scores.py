import json

# Load results
with open('evaluation/results_all.json', 'r') as f:
    results = json.load(f)

for dataset, data in results.items():
    print(f"\n{'='*50}")
    print(f"{dataset}")
    print(f"{'='*50}")
    print(f"Accuracy: {data['accuracy']}%")
    print(f"AUC: {data['auc']}")
    print(f"Optimal Threshold: {data['optimal_threshold']}%")
    print(f"\nConfusion Matrix:")
    print(f"  TP: {data['true_positives']:4d}  |  FP: {data['false_positives']:4d}")
    print(f"  FN: {data['false_negatives']:4d}  |  TN: {data['true_negatives']:4d}")
    
    # Analysis
    if data['auc'] < 0.5:
        print(f"\n⚠️  WARNING: AUC < 0.5 suggests label inversion!")
        print(f"   Try inverting predictions or check label parsing")