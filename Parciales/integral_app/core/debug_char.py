#!/usr/bin/env python3
"""
Debug character by character
"""
import re

def test_chars():
    """Test character by character"""
    
    test_case = "int (x^2+1)/(x+1) dx"
    pattern = r'\bint\b\s*\(([^)]+/[^)]+)\)\s*dx'
    
    print(f"Test case: '{test_case}'")
    print(f"Pattern: {pattern}")
    print(f"Length: {len(test_case)}")
    
    # Print each character with index
    for i, char in enumerate(test_case):
        print(f"{i}: '{char}'")
    
    # Test with a simpler pattern first
    simple_pattern = r'int.*dx'
    match = re.search(simple_pattern, test_case)
    print(f"\nSimple pattern '{simple_pattern}' matches: {match}")
    
    # Test step by step
    patterns = [
        r'int',
        r'int\s*',
        r'int\s*\(',
        r'int\s*\([^)]+',
        r'int\s*\([^)]+/',
        r'int\s*\([^)]+/[^)]+',
        r'int\s*\([^)]+/[^)]+\)',
        r'int\s*\([^)]+/[^)]+\)\s*',
        r'int\s*\([^)]+/[^)]+)\)\s*d',
        r'int\s*\([^)]+/[^)]+)\)\s*dx',
    ]
    
    print(f"\nStep by step:")
    for i, pat in enumerate(patterns):
        match = re.search(pat, test_case)
        print(f"{i+1}. '{pat}' -> {match}")

if __name__ == "__main__":
    test_chars()
