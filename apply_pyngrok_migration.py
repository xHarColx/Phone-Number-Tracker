import os

def apply_fix():
    filename = "phone_tracker.py"
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    in_method = False
    skip_lines = 0
    
    for i, line in enumerate(lines):
        if skip_lines > 0:
            skip_lines -= 1
            continue
            
        if "def _launch_ngrok_tunnel(self, port=8888, timeout=40):" in line:
            in_method = True
            new_lines.append("    def _launch_ngrok_tunnel(self, port=8888, timeout=40):\n")
            new_lines.append("        \"\"\"Start ngrok in the background using pyngrok and return the public HTTPS URL.\"\"\"\n")
            new_lines.append("        if ngrok is None:\n")
            new_lines.append("            console.print(\"[red]  [NGROK] Error: pyngrok library not found.[/red]\")\n")
            new_lines.append("            return None\n\n")
            new_lines.append("        console.print(\"[cyan]  [NGROK] Initializing secure tunnel via pyngrok...[/cyan]\")\n\n")
            new_lines.append("        authtoken = os.environ.get(\"NGROK_AUTHTOKEN\")\n")
            new_lines.append("        if authtoken:\n")
            new_lines.append("            try:\n")
            new_lines.append("                ngrok.set_auth_token(authtoken)\n")
            new_lines.append("            except Exception as e:\n")
            new_lines.append("                console.print(f\"[yellow]  [NGROK] Warning during token config: {e}[/yellow]\")\n\n")
            new_lines.append("        if os.path.exists(\"ngrok.exe\"):\n")
            new_lines.append("            try:\n")
            new_lines.append("                conf.get_default().ngrok_path = os.path.abspath(\"ngrok.exe\")\n")
            new_lines.append("            except: pass\n\n")
            new_lines.append("        try:\n")
            new_lines.append("            public_url = ngrok.connect(port, \"http\").public_url\n")
            new_lines.append("            return {\"process\": \"pyngrok_managed\", \"url\": public_url}\n")
            new_lines.append("        except Exception as e:\n")
            new_lines.append("            console.print(f\"[red]  [NGROK] Failed to establish tunnel: {e}[/red]\")\n")
            new_lines.append("            if \"authtoken\" in str(e).lower():\n")
            new_lines.append("                console.print(\"[yellow]  [TIP] Check your Ngrok Auth Token in Settings.[/yellow]\")\n")
            new_lines.append("            return None\n")
            
            # Skip old method body (until next def)
            count = 0
            for j in range(i+1, len(lines)):
                if "def _build_tracking_page(" in lines[j]:
                    break
                count += 1
            skip_lines = count
            continue
            
        new_lines.append(line)
        
    with open(filename, 'w', encoding='utf-8', newline='\n') as f:
        f.writelines(new_lines)
    print("Pyngrok Migration applied.")

if __name__ == "__main__":
    apply_fix()
