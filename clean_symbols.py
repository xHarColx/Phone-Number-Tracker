import sys
import os

def sanitize_file(filepath):
    # Mapping of broken Unicode patterns to clean ASCII/Text
    # Including new patterns identified: fôï, fîì, fôè
    replacements = {
        '­ƒôï': '[CDR]',
        '­ƒîì': '[GEO]',
        '­ƒôè': '[SUM]',
        '­ƒöì': '[SCAN]',
        '­ƒîƒ': '[*]',
        '­ƒÄ»': '[GRAB]',
        '­ƒƒó': '[OPEN]',
        '­ƒƒí': '[RESTR]',
        '­ƒö┤': '[ALERT]',
        '­ƒÜ¿': '[SIREN]',
        '­ƒƒï': '[AUDIT]',
        '­ƒôæ': '[CASE]',
        '­ƒô▓': '[TRACK]',
        '­ƒô╖': '[SNAP]',
        '­ƒö¬': '[FORENSIC]',
        '­ƒôë': '[GRAPH]',
        'Ô£ô': '[OK]',
        'ÔÇö': '-',
        'Ôöü': '-',
        'ÔÜá': '[!]',
        'ÔåÆ': '->',
        'ÔöÇ': '-',
        'Ôöé': '|',
        'Ôòê': '=',
        'ÔòÉ': '=',
        'Ôòù': '=',
        'Ôòö': '=',
        'Ôö£': '+',
        'ÔöÉ': '+',
        'Ôòæ': '|',
    }
    
    try:
        with open(filepath, 'rb') as f:
            content = f.read().decode('utf-8', errors='ignore')
        
        original_content = content
        for broken, fixed in replacements.items():
            content = content.replace(broken, fixed)
            
        if content != original_content:
            # Write with consistent LF to avoid double newline issues
            with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
                f.write(content)
            print(f"Successfully sanitized {filepath}")
        else:
            print(f"No changes needed for {filepath}")
            
    except Exception as e:
        print(f"Error sanitizing {filepath}: {e}")

if __name__ == "__main__":
    sanitize_file("phone_tracker.py")
