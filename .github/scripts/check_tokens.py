#!/usr/bin/env python3
"""
Script to check token lengths of documentation files using HuggingFace tokenizers.
"""

import os
import glob
import subprocess
import sys
from tabulate import tabulate

def install_dependencies():
    """Install required dependencies if not present."""
    try:
        import tokenizers
        import tabulate
    except ImportError:
        print("📦 Installing required dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "tokenizers", "tabulate"])
        print("✅ Dependencies installed successfully.")

def count_tokens(file_path):
    """Count tokens in a file using HuggingFace tokenizers."""
    from tokenizers import Tokenizer
    from tokenizers.models import BPE
    
    # Load GPT-2 tokenizer (commonly used baseline for many models)
    tokenizer = Tokenizer.from_pretrained("gpt2")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    encoded = tokenizer.encode(content)
    return len(encoded.ids)

def format_file_path(file_path):
    """Format file path to be more readable."""
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    relative_path = os.path.relpath(file_path, base_dir)
    return relative_path

def main():
    """Check token lengths of README.md and docs/*.md files."""
    install_dependencies()
    
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    files_to_check = [
        os.path.join(base_dir, "README.md"),
    ]
    
    # Add all markdown files in docs directory
    docs_pattern = os.path.join(base_dir, "docs", "**", "*.md")
    files_to_check.extend(glob.glob(docs_pattern, recursive=True))
    
    results = []
    total_tokens = 0
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            token_count = count_tokens(file_path)
            total_tokens += token_count
            results.append([format_file_path(file_path), token_count])
    
    # Add total row
    results.append(["TOTAL", total_tokens])
    
    # Print results as a table
    print("\n📊 Token Count Summary:")
    print(tabulate(results, headers=["File", "Token Count"], tablefmt="grid"))
    print("\nNote: Token counts are based on the GPT-2 tokenizer and may vary for different models.")

if __name__ == "__main__":
    main()