import os
import requests
import tarfile
import zipfile
from tqdm import tqdm

class DatasetDownloader:
    """Download and extract face verification datasets"""
    
    def __init__(self, base_dir=r"C:\Users\reza.hatami\Desktop\datasets"):
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)
    
    def download_file(self, url, output_path):
        """Download file with progress bar"""
        try:
            print(f"📥 Downloading from: {url}")
            response = requests.get(url, stream=True, timeout=60)
            total_size = int(response.headers.get('content-length', 0))
            
            with open(output_path, 'wb') as f, tqdm(
                desc=os.path.basename(output_path),
                total=total_size,
                unit='iB',
                unit_scale=True
            ) as pbar:
                for chunk in response.iter_content(chunk_size=8192):
                    size = f.write(chunk)
                    pbar.update(size)
            
            print(f"✅ Downloaded: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Download failed: {e}")
            return False
    
    def extract_archive(self, archive_path, extract_to):
        """Extract tar.gz or zip archive"""
        try:
            print(f"📦 Extracting: {archive_path}")
            
            if archive_path.endswith('.tgz') or archive_path.endswith('.tar.gz'):
                with tarfile.open(archive_path, 'r:gz') as tar:
                    tar.extractall(path=extract_to)
            elif archive_path.endswith('.zip'):
                with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_to)
            
            print(f"✅ Extracted to: {extract_to}")
            return True
            
        except Exception as e:
            print(f"❌ Extraction failed: {e}")
            return False
    
    def download_lfw(self):
        """Download LFW dataset"""
        print("\n" + "="*50)
        print("📊 Downloading LFW Dataset")
        print("="*50)
        
        lfw_dir = os.path.join(self.base_dir, "lfw")
        os.makedirs(lfw_dir, exist_ok=True)
        
        # Alternative mirrors for LFW
        mirrors = [
            "http://vis-www.cs.umass.edu/lfw/lfw.tgz",
            "https://ndownloader.figshare.com/files/5976018",  # Alternative
        ]
        
        archive_path = os.path.join(self.base_dir, "lfw.tgz")
        
        # Try each mirror
        downloaded = False
        for url in mirrors:
            if self.download_file(url, archive_path):
                downloaded = True
                break
        
        if not downloaded:
            print("❌ All mirrors failed. Please download manually:")
            print("   1. Go to: http://vis-www.cs.umass.edu/lfw/")
            print("   2. Download lfw.tgz")
            print(f"   3. Place in: {self.base_dir}")
            return False
        
        # Extract
        if self.extract_archive(archive_path, self.base_dir):
            # Download pairs.txt
            pairs_url = "http://vis-www.cs.umass.edu/lfw/pairs.txt"
            pairs_path = os.path.join(lfw_dir, "pairs.txt")
            
            if self.download_file(pairs_url, pairs_path):
                print("✅ LFW dataset ready!")
                return True
        
        return False
    
    def download_lfw_from_kaggle(self):
        """Alternative: Use Kaggle dataset"""
        print("\n💡 Alternative: Download from Kaggle")
        print("="*50)
        print("1. Install Kaggle CLI:")
        print("   pip install kaggle")
        print("\n2. Setup Kaggle API:")
        print("   - Go to: https://www.kaggle.com/settings")
        print("   - Create API token (kaggle.json)")
        print("   - Place in: C:\\Users\\reza.hatami\\.kaggle\\")
        print("\n3. Download LFW:")
        print("   kaggle datasets download -d jessicali9530/lfw-dataset")
        print("="*50)
    
    def check_existing_datasets(self):
        """Check which datasets are already downloaded"""
        print("\n🔍 Checking existing datasets...")
        print("="*50)
        
        datasets = {
            'LFW': os.path.join(self.base_dir, 'lfw'),
            'CP-LFW': os.path.join(self.base_dir, 'cplfw'),
            'CA-LFW': os.path.join(self.base_dir, 'calfw'),
        }
        
        for name, path in datasets.items():
            if os.path.exists(path):
                num_files = sum([len(files) for r, d, files in os.walk(path)])
                print(f"✅ {name}: Found ({num_files} files)")
            else:
                print(f"❌ {name}: Not found")
        
        print("="*50)

def main():
    print("🎯 Face Verification Dataset Downloader")
    print("="*50)
    
    downloader = DatasetDownloader()
    
    # Check existing datasets
    downloader.check_existing_datasets()
    
    # Try to download LFW
    print("\n📥 Attempting to download LFW...")
    
    if not downloader.download_lfw():
        print("\n⚠️  Automatic download failed!")
        downloader.download_lfw_from_kaggle()
    
    print("\n" + "="*50)
    print("✅ Download process complete!")
    print("="*50)

if __name__ == "__main__":
    main()
