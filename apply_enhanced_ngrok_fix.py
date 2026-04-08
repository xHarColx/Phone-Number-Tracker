import os
import subprocess

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
            
        if "def _launch_ngrok_tunnel(self, port=8888, timeout=30):" in line:
            new_lines.append("    def _launch_ngrok_tunnel(self, port=8888, timeout=40):\n")
            new_lines.append("        \"\"\"Start ngrok in the background and return the public HTTPS URL.\"\"\"\n")
            new_lines.append("        import shutil\n")
            new_lines.append("        console.print(\"[cyan]  [NGROK] Initializing secure tunnel...[/cyan]\")\n")
            new_lines.append("        # Kill any existing ngrok processes to avoid port conflicts\n")
            new_lines.append("        try:\n")
            new_lines.append("            subprocess.run([\"taskkill\", \"/f\", \"/im\", \"ngrok.exe\"], \n")
            new_lines.append("                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, \n")
            new_lines.append("                           creationflags=0x08000000)\n")
            new_lines.append("            time.sleep(1)\n")
            new_lines.append("        except: pass\n\n")
            new_lines.append("        if shutil.which(\"ngrok\") is None:\n")
            new_lines.append("            if not os.path.exists(\"ngrok.exe\"):\n")
            new_lines.append("                console.print(\"[red]  [NGROK] Error: ngrok.exe not found in Path or local directory.[/red]\")\n")
            new_lines.append("                return None\n")
            new_lines.append("            ngrok_cmd = \"./ngrok.exe\"\n")
            new_lines.append("        else:\n")
            new_lines.append("            ngrok_cmd = \"ngrok\"\n\n")
            new_lines.append("        authtoken = os.environ.get(\"NGROK_AUTHTOKEN\")\n")
            new_lines.append("        if authtoken:\n")
            new_lines.append("            try:\n")
            new_lines.append("                subprocess.run([ngrok_cmd, \"config\", \"add-authtoken\", authtoken], \n")
            new_lines.append("                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,\n")
            new_lines.append("                               creationflags=0x08000000)\n")
            new_lines.append("            except: pass\n\n")
            new_lines.append("        try:\n")
            new_lines.append("            process = subprocess.Popen(\n")
            new_lines.append("                [ngrok_cmd, \"http\", str(port), \"--log=stdout\"],\n")
            new_lines.append("                stdout=subprocess.PIPE, \n")
            new_lines.append("                stderr=subprocess.PIPE,\n")
            new_lines.append("                text=True,\n")
            new_lines.append("                creationflags=0x08000000\n")
            new_lines.append("            )\n")
            new_lines.append("        except Exception as e:\n")
            new_lines.append("            console.print(f\"[red]  [NGROK] Failed to start: {e}[/red]\")\n")
            new_lines.append("            return None\n")
            
            # Skip old method body until 'start = time.time()'
            count = 0
            for j in range(i+1, len(lines)):
                count += 1
                if "start = time.time()" in lines[j]:
                    break
            skip_lines = count - 1
            continue
            
        new_lines.append(line)
        
    with open(filename, 'w', encoding='utf-8', newline='\n') as f:
        f.writelines(new_lines)
    print("Ngrok Enhanced Fix applied.")

if __name__ == "__main__":
    apply_fix()
