with open(r'C:\Users\reza.hatami\Desktop\datasets\calfw\pairs_CALFW.txt', 'r') as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]

print("First 100 lines label distribution:")
labels = []
for i in range(100):
    parts = lines[i].split()
    label = int(parts[1])
    labels.append(label)

print(f"Label=1: {labels.count(1)}")
print(f"Label=0: {labels.count(0)}")

# Check pairs
print("\nFirst 10 pairs:")
for i in range(0, 20, 2):
    parts1 = lines[i].split()
    parts2 = lines[i+1].split()
    
    label1 = int(parts1[1])
    label2 = int(parts2[1])
    
    is_same = 1 if label1 == label2 else 0
    
    print(f"Pair {i//2}: label={label1},{label2} → {'SAME' if is_same else 'DIFF'}")