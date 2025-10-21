"""
Download and setup InsightFace models locally
This script downloads required models to the project directory
"""

import os
import sys
from pathlib import Path
import insightface
from insightface.app import FaceAnalysis

def download_models():
    """Download InsightFace models to local models directory"""
    
    # Create models directory
    models_dir = Path(__file__).parent / "models"
    models_dir.mkdir(exist_ok=True)
    
    print("="*60)
    print("📦 Downloading InsightFace Models")
    print("="*60)
    print(f"Target directory: {models_dir.absolute()}")
    
    try:
        # Initialize FaceAnalysis - this will download models
        print("\n🔄 Downloading models (this may take a few minutes)...")
        print("   Model size: ~100MB")
        
        app = FaceAnalysis(
            name='buffalo_l',
            root=str(models_dir),
            providers=['CPUExecutionProvider']
        )
        app.prepare(ctx_id=0, det_size=(640, 640))
        
        print("\n✅ Models downloaded successfully!")
        print(f"📁 Models location: {models_dir.absolute()}")
        
        # List downloaded files
        print("\n📋 Downloaded files:")
        for root, dirs, files in os.walk(models_dir):
            level = root.replace(str(models_dir), '').count(os.sep)
            indent = ' ' * 2 * level
            print(f'{indent}{os.path.basename(root)}/')
            sub_indent = ' ' * 2 * (level + 1)
            for file in files:
                file_size = os.path.getsize(os.path.join(root, file)) / (1024*1024)
                print(f'{sub_indent}{file} ({file_size:.1f} MB)')
        
        print("\n" + "="*60)
        print("✅ Setup complete! You can now run the server.")
        print("="*60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error downloading models: {e}")
        print("\nTroubleshooting:")
        print("1. Check your internet connection")
        print("2. Try running: pip install --upgrade insightface onnxruntime")
        print("3. Check firewall settings")
        return False

def check_models_exist():
    """Check if models are already downloaded"""
    models_dir = Path(__file__).parent / "models"
    
    if not models_dir.exists():
        return False
    
    # Check for key model files
    buffalo_dir = models_dir / "buffalo_l"
    if buffalo_dir.exists():
        model_files = list(buffalo_dir.glob("*.onnx"))
        return len(model_files) > 0
    
    return False

def main():
    print("\n🎯 InsightFace Model Setup")
    print("="*60)
    
    # Check if models already exist
    if check_models_exist():
        print("✅ Models already downloaded!")
        models_dir = Path(__file__).parent / "models"
        print(f"📁 Location: {models_dir.absolute()}")
        
        response = input("\n🔄 Re-download models? (y/N): ").lower()
        if response != 'y':
            print("✅ Skipping download. Models are ready to use.")
            return
    
    # Download models
    success = download_models()
    
    if success:
        print("\n✨ Next steps:")
        print("   1. Run: python server.py")
        print("   2. Test with: python client.py")
    else:
        print("\n⚠️  Setup failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
