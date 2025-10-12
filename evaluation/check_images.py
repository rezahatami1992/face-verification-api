import os

# Check CALFW
calfw_dir = r'C:\Users\reza.hatami\Desktop\datasets\calfw\aligned images'
print("CALFW structure:")
print(f"Directory exists: {os.path.exists(calfw_dir)}")

if os.path.exists(calfw_dir):
    contents = os.listdir(calfw_dir)
    print(f"Contents: {contents[:5]}")  # First 5 items
    
    # Check if images are directly in folder or in subfolders
    sample_file = "Carl_Reiner_0001.jpg"
    direct_path = os.path.join(calfw_dir, sample_file)
    print(f"\nDirect path exists: {os.path.exists(direct_path)}")
    
    # Check subfolders
    for item in contents[:3]:
        item_path = os.path.join(calfw_dir, item)
        if os.path.isdir(item_path):
            print(f"Subfolder '{item}': {os.listdir(item_path)[:3]}")

print("\n" + "="*50)

# Check CPLFW
cplfw_dir = r'C:\Users\reza.hatami\Desktop\datasets\cplfw\aligned images'
print("CPLFW structure:")
print(f"Directory exists: {os.path.exists(cplfw_dir)}")

if os.path.exists(cplfw_dir):
    contents = os.listdir(cplfw_dir)
    print(f"Contents: {contents[:5]}")
    
    sample_file = contents[0] if contents else None
    if sample_file:
        print(f"Sample file: {sample_file}")