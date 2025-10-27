"""
Test script to verify the AI Legal Aid Chatbot setup
Run this to check if all dependencies are installed correctly
"""

import sys
import importlib

def test_imports():
    """Test if all required packages are installed"""
    
    required_packages = {
        'streamlit': 'Streamlit',
        'pypdf': 'PyPDF',
        'chromadb': 'ChromaDB',
        'sentence_transformers': 'Sentence Transformers',
        'transformers': 'Transformers',
        'torch': 'PyTorch',
        'numpy': 'NumPy',
        'pandas': 'Pandas'
    }
    
    print("=" * 60)
    print("AI Legal Aid Chatbot - Setup Verification")
    print("=" * 60)
    print()
    
    all_passed = True
    
    for package, name in required_packages.items():
        try:
            importlib.import_module(package)
            print(f"✅ {name:25s} - Installed")
        except ImportError:
            print(f"❌ {name:25s} - NOT FOUND")
            all_passed = False
    
    print()
    print("=" * 60)
    
    if all_passed:
        print("✅ All dependencies are installed correctly!")
        print()
        print("Next steps:")
        print("1. Ensure PDFs are in the 'data/' directory")
        print("2. Run: streamlit run app.py")
        print("3. Open http://localhost:8501 in your browser")
    else:
        print("❌ Some dependencies are missing!")
        print()
        print("Please run: pip install -r requirements.txt")
    
    print("=" * 60)
    
    return all_passed


def test_project_structure():
    """Test if project structure is correct"""
    
    from pathlib import Path
    
    print()
    print("Checking project structure...")
    print()
    
    required_files = [
        'app.py',
        'rag_pipeline.py',
        'prompts.py',
        'requirements.txt',
        'README.md'
    ]
    
    required_dirs = [
        'data',
        'db'
    ]
    
    all_passed = True
    
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - NOT FOUND")
            all_passed = False
    
    for dir in required_dirs:
        if Path(dir).exists():
            print(f"✅ {dir}/")
        else:
            print(f"❌ {dir}/ - NOT FOUND")
            all_passed = False
    
    # Check for PDFs
    data_dir = Path('data')
    if data_dir.exists():
        pdf_files = list(data_dir.glob('*.pdf'))
        print()
        print(f"📄 Found {len(pdf_files)} PDF file(s) in data/:")
        for pdf in pdf_files:
            print(f"   - {pdf.name}")
    
    return all_passed


def test_models():
    """Test if models can be loaded"""
    
    print()
    print("=" * 60)
    print("Testing model loading (this may take a moment)...")
    print("=" * 60)
    print()
    
    try:
        print("Loading embedding model...")
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        print("✅ Embedding model loaded successfully")
        
        print()
        print("Loading LLM model...")
        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
        tokenizer = AutoTokenizer.from_pretrained('google/flan-t5-small')
        llm = AutoModelForSeq2SeqLM.from_pretrained('google/flan-t5-small')
        print("✅ LLM model loaded successfully")
        
        print()
        print("✅ All models loaded successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error loading models: {e}")
        return False


if __name__ == "__main__":
    print()
    
    # Test imports
    imports_ok = test_imports()
    
    if not imports_ok:
        print()
        print("Please install missing dependencies before proceeding.")
        sys.exit(1)
    
    # Test project structure
    structure_ok = test_project_structure()
    
    if not structure_ok:
        print()
        print("⚠️  Some files or directories are missing!")
        print("Please ensure all required files are present.")
    
    # Ask if user wants to test models
    print()
    print("=" * 60)
    response = input("Do you want to test model loading? (y/n): ").strip().lower()
    
    if response == 'y':
        models_ok = test_models()
        
        if models_ok:
            print()
            print("=" * 60)
            print("🎉 Setup verification complete! Everything looks good!")
            print("=" * 60)
            print()
            print("You can now run the application:")
            print("  streamlit run app.py")
            print()
            print("Or use the quick start script:")
            print("  run.bat  (Windows)")
            print("=" * 60)
    else:
        print()
        print("Skipping model loading test.")
        print("Run 'python test_setup.py' again when ready to test models.")
    
    print()
