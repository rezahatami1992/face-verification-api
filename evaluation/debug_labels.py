def check_pairs_format(pairs_file):
    with open(pairs_file, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    
    print(f"Total lines: {len(lines)}")
    print("\nFirst 10 lines:")
    for i, line in enumerate(lines[:10]):
        print(f"{i}: {line}")
    
    # Test parsing
    print("\n--- Testing pair parsing ---")
    for i in range(0, min(10, len(lines)-1), 2):
        line1 = lines[i].split()
        line2 = lines[i+1].split()
        
        img1, label1 = line1[0], int(line1[1])
        img2, label2 = line2[0], int(line2[1])
        
        is_same = 1 if label1 == label2 else 0
        
        print(f"\nPair {i//2}:")
        print(f"  {img1} (label={label1})")
        print(f"  {img2} (label={label2})")
        print(f"  Same person: {is_same}")

# Run
check_pairs_format(r'C:\Users\reza.hatami\Desktop\datasets\calfw\pairs_CALFW.txt')
