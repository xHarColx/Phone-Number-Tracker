import os

def apply_fix():
    filename = "gui.py"
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    
    # 1. Add get_base_dir helper after imports if not present
    # 2. Update config and history paths
    
    for i, line in enumerate(lines):
        if "def load_config(self):" in line:
            new_lines.append(line)
            new_lines.append("        if getattr(sys, 'frozen', False):\n")
            new_lines.append("            base_dir = os.path.dirname(sys.executable)\n")
            new_lines.append("        else:\n")
            new_lines.append("            base_dir = os.path.dirname(os.path.abspath(__file__))\n")
            new_lines.append("        config_path = os.path.join(base_dir, self.config_file)\n")
            # Skip until 'if os.path.exists(config_path):'
            skip = 0
            for j in range(i+1, len(lines)):
                skip += 1
                if "if os.path.exists(config_path):" in lines[j]:
                    break
            # Just let it proceed, but skip the old config_path line
            continue

        if "def save_config(self):" in line:
            new_lines.append(line)
            new_lines.append("        if getattr(sys, 'frozen', False):\n")
            new_lines.append("            base_dir = os.path.dirname(sys.executable)\n")
            new_lines.append("        else:\n")
            new_lines.append("            base_dir = os.path.dirname(os.path.abspath(__file__))\n")
            new_lines.append("        config_path = os.path.join(base_dir, self.config_file)\n")
            continue

        if "def load_history(self):" in line:
            new_lines.append(line)
            new_lines.append("        if getattr(sys, 'frozen', False):\n")
            new_lines.append("            base_dir = os.path.dirname(sys.executable)\n")
            new_lines.append("        else:\n")
            new_lines.append("            base_dir = os.path.dirname(os.path.abspath(__file__))\n")
            new_lines.append("        output_dir = os.path.join(base_dir, \"output\")\n")
            new_lines.append("        for widget in self.history_frame.winfo_children():\n")
            new_lines.append("            widget.destroy()\n")
            new_lines.append("        \n")
            new_lines.append("        if not os.path.exists(output_dir):\n")
            new_lines.append("            l = ctk.CTkLabel(self.history_frame, text=\"No cases found.\")\n")
            new_lines.append("            l.pack(pady=10)\n")
            new_lines.append("            return\n")
            new_lines.append("            \n")
            new_lines.append("        files = glob.glob(os.path.join(output_dir, \"*.json\"))\n")
            # Skip old load_history body until the loop
            count = 0
            for j in range(i+1, len(lines)):
                if "for f in reversed(sorted(files" in lines[j]:
                    break
                count += 1
            # We already added the frame cleaning and if-blocks, so skip those
            # The next line in new_lines will be the loop
            skip_count = count
            for j in range(i+1, i+1+skip_count):
                pass
            
            # This logic is a bit complex for a simple script, I'll just replace the whole body
            continue

        new_lines.append(line)
        
    # Actually, I'll just use replace_file_content for the specific blocks.
    # It failed before because I was replacing too much or the line numbers were off.
    
if __name__ == "__main__":
    # Skipping this script, will use replace_file_content with smaller chunks
    pass
