def check_nltk():
    try:
        import nltk
        print(f"NLTK version: {nltk.__version__}")
        print("NLTK successfully imported.")
        
        if hasattr(nltk, 'download'):
            print("NLTK download function is available.")
        else:
            print("NLTK download function is not available. This is unexpected.")
        
    except ImportError as e:
        print(f"Error importing NLTK: {e}")
        print("NLTK might not be installed correctly.")

if __name__ == "__main__":
    check_nltk()