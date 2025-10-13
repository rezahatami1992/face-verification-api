def check_pairs(pairs_file):
    with open(pairs_file, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    
    # Parse
    all_samples = []
    for line in lines:
        parts = line.split()
        if len(parts) >= 2:
            img = parts[0]
            label = int(parts[1])
            all_samples.append({'img': img, 'label': label})
    
    # Create pairs
    pairs = []
    for i in range(0, len(all_samples) - 1, 2):
        sample1 = all_samples[i]
        sample2 = all_samples[i + 1]
        
        is_same_person = 1 if sample1['label'] == sample2['label'] else 0
        
        pairs.append({
            'img1': sample1['img'],
            'img2': sample2['img'],
            'label': is_same_person
        })
    
    # Count
    same = sum([1 for p in pairs if p['label'] == 1])
    diff = sum([1 for p in pairs if p['label'] == 0])
    
    print(f"Total pairs: {len(pairs)}")
    print(f"Same person: {same}")
    print(f"Different: {diff}")
    
    # Show first different pair
    for i, p in enumerate(pairs):
        if p['label'] == 0:
            print(f"\nFirst different pair at index {i}:")
            print(f"  {p['img1']}")
            print(f"  {p['img2']}")
            break

print("CALFW:")
check_pairs(r'C:\Users\reza.hatami\Desktop\datasets\calfw\pairs_CALFW.txt')

print("\n" + "="*50)
print("CPLFW:")
check_pairs(r'C:\Users\reza.hatami\Desktop\datasets\cplfw\pairs_CPLFW.txt')