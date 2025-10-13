with open(r'C:\Users\reza.hatami\Desktop\datasets\calfw\pairs_CALFW.txt', 'r') as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]

print("First 20 lines with labels:")
for i in range(20):
    parts = lines[i].split()
    img = parts[0]
    label = parts[1]
    name = '_'.join(img.split('_')[:2])
    print(f"{i:2d}: {name:30s} | label={label}")

print("\n" + "="*50)
print("Lines 6000-6020 (transition point):")
for i in range(5998, 6020):
    if i < len(lines):
        parts = lines[i].split()
        img = parts[0]
        label = parts[1]
        name = '_'.join(img.split('_')[:2])
        print(f"{i:4d}: {name:30s} | label={label}")