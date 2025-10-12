# Check CALFW pairs
print("CALFW pairs.txt:")
with open(r'C:\Users\reza.hatami\Desktop\datasets\calfw\pairs_CALFW.txt', 'r') as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]
    print(f"First 5: {lines[:5]}")

print("\n" + "="*50)

# Check CPLFW pairs  
print("CPLFW pairs.txt:")
with open(r'C:\Users\reza.hatami\Desktop\datasets\cplfw\pairs_CPLFW.txt', 'r') as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]
    print(f"First 5: {lines[:5]}")