import os

def apply_fix():
    filename = "phone_tracker.py"
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    skip_lines = 0
    
    for i, line in enumerate(lines):
        if skip_lines > 0:
            skip_lines -= 1
            continue
            
        if "if os.path.exists(\"ngrok.exe\"):" in line and "conf.get_default().ngrok_path" in lines[i+2]:
            new_lines.append(line)
            new_lines.append("            try:\n")
            new_lines.append("                c = conf.get_default()\n")
            new_lines.append("                c.ngrok_path = os.path.abspath(\"ngrok.exe\")\n")
            new_lines.append("                if os.name == 'nt':\n")
            new_lines.append("                    import subprocess\n")
            new_lines.append("                    startupinfo = subprocess.STARTUPINFO()\n")
            new_lines.append("                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW\n")
            new_lines.append("                    startupinfo.wShowWindow = subprocess.SW_HIDE\n")
            new_lines.append("                    c.startupinfo = startupinfo\n")
            new_lines.append("            except: pass\n")
            skip_lines = 3
            continue
            
        new_lines.append(line)
        
    with open(filename, 'w', encoding='utf-8', newline='\n') as f:
        f.writelines(new_lines)
    print("Silent Migration applied.")

if __name__ == "__main__":
    apply_fix()
