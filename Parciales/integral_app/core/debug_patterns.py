#!/usr/bin/env python3
"""
Debug script to test integral pattern matching
"""
import re

def test_patterns():
    """Test integral pattern matching directly"""
    
    # Test patterns from the engine
    patterns = [
        r'\bint\b\s*\(([^)]+/[^)]+)\)\s*d\s*([a-zA-Z])', # int (x^2+1)/(x+1) dx
        r'\bintegral\b\s*\(([^)]+/[^)]+)\)\s*d\s*([a-zA-Z])', # integral (x^2+1)/(x+1) dx
        r'\bint\b\s+([^(]+?)\s*d\s*([a-zA-Z])', # int x dx
        r'\bintegral\b\s+([^(]+?)\s*d\s*([a-zA-Z])', # integral x dx
    ]
    
    test_cases = [
        "int (x^2+1)/(x+1) dx",
        "integral (x^2+1)/(x+1) dx",
        "int x^2/x dx",
        "integral x^2/x dx",
        "int x dx",
        "integral x dx",
    ]
    
    print("Testing pattern matching...")
    print("=" * 60)
    
    for test_case in test_cases:
        print(f"\nTesting: '{test_case}'")
        matched = False
        
        for i, pattern in enumerate(patterns):
            match = re.search(pattern, test_case)
            if match:
                print(f"  Pattern {i+1} MATCHED: {pattern}")
                print(f"  Groups: {match.groups()}")
                matched = True
                break
        
        if not matched:
            print(f"  NO PATTERNS MATCHED")
    
    print("\n" + "=" * 60)
    print("Debug completed!")

if __name__ == "__main__":
    test_patterns()
