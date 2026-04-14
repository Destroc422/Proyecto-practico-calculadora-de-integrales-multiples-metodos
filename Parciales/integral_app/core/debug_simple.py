#!/usr/bin/env python3
"""
Simple debug script to test individual pattern
"""
import re

def test_single_pattern():
    """Test a single pattern"""
    
    pattern = r'\bint\b\s*\(([^)]+/[^)]+)\)\s*dx'
    test_case = "int (x^2+1)/(x+1) dx"
    
    print(f"Testing pattern: {pattern}")
    print(f"Test case: '{test_case}'")
    
    match = re.search(pattern, test_case)
    if match:
        print(f"MATCHED! Groups: {match.groups()}")
    else:
        print("NO MATCH")
        
        # Let's break down the pattern
        print("\nBreaking down the pattern:")
        print(r"\bint\b - word boundary 'int'")
        print(r"\s* - zero or more spaces")
        print(r"\( - literal '('")
        print(r"([^)]+/[^)]+) - capture group: any chars except ')' followed by '/' followed by any chars except ')'")
        print(r"\) - literal ')'")
        print(r"\s* - zero or more spaces")
        print(r"d - literal 'd'")
        print(r"\s* - zero or more spaces")
        print(r"([a-zA-Z]) - capture group: single letter")
        
        # Test individual parts
        print(f"\nTesting parts:")
        print(f"Contains 'int': {'int' in test_case}")
        print(f"Has parentheses: '(' in test_case and ')' in test_case")
        print(f"Has '/': '/' in test_case")
        print(f"Has 'dx': {'dx' in test_case}")

if __name__ == "__main__":
    test_single_pattern()
