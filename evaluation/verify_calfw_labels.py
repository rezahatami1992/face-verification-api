import os

calfw_dir = r'C:\Users\reza.hatami\Desktop\datasets\calfw\aligned images'

# Check label=1 pairs (should be same person?)
print("Label=1 examples:")
pairs_label_1 = [
    ('Carl_Reiner_0001.jpg', 'Carl_Reiner_0003.jpg'),
    ('Bernard_Law_0001.jpg', 'Bernard_Law_0004.jpg'),
    ('Ian_Smith_0001.jpg', 'Ian_Smith_0004.jpg')
]

for img1, img2 in pairs_label_1:
    name1 = img1.split('_')[0] + '_' + img1.split('_')[1]
    name2 = img2.split('_')[0] + '_' + img2.split('_')[1]
    print(f"  {name1} vs {name2} → {'SAME' if name1 == name2 else 'DIFFERENT'}")

# Check label=0 pairs (should be different person?)
print("\nLabel=0 examples:")
with open(r'C:\Users\reza.hatami\Desktop\datasets\calfw\pairs_CALFW.txt', 'r') as f:
    lines = [l.strip() for l in f.readlines() if l.strip()]
    # Get label=0 lines
    label_0_lines = [l for l in lines if l.endswith(' 0')][:3]
    
for line in label_0_lines:
    img = line.split()[0]
    name = '_'.join(img.split('_')[:2])
    print(f"  {img} → {name}")