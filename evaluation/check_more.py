def analyze_full_file(pairs_file):
    with open(pairs_file, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    
    print(f"Total lines: {len(lines)}")
    print(f"Total pairs: {len(lines) // 2}")
    
    # Parse all pairs
    same_count = 0
    diff_count = 0
    
    for i in range(0, len(lines)-1, 2):
        line1 = lines[i].split()
        line2 = lines[i+1].split()
        
        label1 = int(line1[1])
        label2 = int(line2[1])
        
        if label1 == label2:
            same_count += 1
        else:
            diff_count += 1
    
    print(f"\nSame person pairs: {same_count}")
    print(f"Different person pairs: {diff_count}")
    
    # Show middle section
    print("\n--- Lines 6000-6010 (middle section) ---")
    for i in range(6000, min(6010, len(lines))):
        print(f"{i}: {lines[i]}")

analyze_full_file(r'C:\Users\reza.hatami\Desktop\datasets\calfw\pairs_CALFW.txt')
