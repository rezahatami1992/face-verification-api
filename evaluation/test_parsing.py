def test_load_pairs(pairs_file):
    with open(pairs_file, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    
    # Split by label
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
    
    print(f"Positive samples (label=1): {len(positive_samples)}")
    print(f"Negative samples (label=0): {len(negative_samples)}")
    
    # Create pairs
    pairs = []
    
    # Same-person pairs
    for i in range(0, min(10, len(positive_samples) - 1), 2):
        pairs.append({
            'img1': positive_samples[i],
            'img2': positive_samples[i + 1],
            'label': 1
        })
    
    # Different-person pairs  
    for i in range(0, min(10, len(negative_samples) - 1), 2):
        pairs.append({
            'img1': negative_samples[i],
            'img2': negative_samples[i + 1],
            'label': 0
        })
    
    print(f"\nTotal pairs created: {len(pairs)}")
    print(f"\nFirst 10 pairs:")
    for i, pair in enumerate(pairs[:10]):
        print(f"  {i}: {pair['img1']} + {pair['img2']} = label {pair['label']}")
    
    # Count labels
    label_1 = sum([1 for p in pairs if p['label'] == 1])
    label_0 = sum([1 for p in pairs if p['label'] == 0])
    print(f"\nLabel distribution:")
    print(f"  Same person (1): {label_1}")
    print(f"  Different (0): {label_0}")

test_load_pairs(r'C:\Users\reza.hatami\Desktop\datasets\calfw\pairs_CALFW.txt')