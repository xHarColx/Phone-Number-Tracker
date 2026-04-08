import customtkinter as ctk
import subprocess
import threading
import sys
import os
import glob
import json
import datetime
import tkintermapview

ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Phone Tracker Pro v6.5 - Apex Predator")
        self.config_file = "config.json"
        self.geometry("1000x800")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Tracker Pro", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.phone_label = ctk.CTkLabel(self.sidebar_frame, text="Target Number:")
        self.phone_label.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.phone_container = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.phone_container.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.phone_container.grid_columnconfigure(1, weight=1)
        
        self.prefix_var = ctk.StringVar(value="+56")
        self.prefix_dropdown = ctk.CTkOptionMenu(self.phone_container, values=["+56", "+54", "+52", "+51", "+1", "+34", "+44", "+91"], variable=self.prefix_var, width=70)
        self.prefix_dropdown.grid(row=0, column=0, padx=(0, 5))
        
        self.phone_entry = ctk.CTkEntry(self.phone_container, placeholder_text="932977690")
        self.phone_entry.grid(row=0, column=1, sticky="ew")

        self.officer_label = ctk.CTkLabel(self.sidebar_frame, text="Officer / Webhook:")
        self.officer_label.grid(row=3, column=0, padx=20, pady=(10, 0), sticky="w")
        self.officer_entry = ctk.CTkEntry(self.sidebar_frame, placeholder_text="OPERATOR-1")
        self.officer_entry.grid(row=4, column=0, padx=20, pady=(0, 10), sticky="ew")

        self.case_label = ctk.CTkLabel(self.sidebar_frame, text="Case ID:")
        self.case_label.grid(row=5, column=0, padx=20, pady=(10, 0), sticky="nw")
        self.case_entry = ctk.CTkEntry(self.sidebar_frame, placeholder_text="CASE-XXXX")
        self.case_entry.grid(row=6, column=0, padx=20, pady=(0, 10), sticky="nw")

        self.grabber_var = ctk.BooleanVar(value=False)
        self.grabber_checkbox = ctk.CTkCheckBox(self.sidebar_frame, text="Enable IP Grabber", variable=self.grabber_var)
        self.grabber_checkbox.grid(row=7, column=0, padx=20, pady=(10, 10), sticky="w")

        self.quick_var = ctk.BooleanVar(value=False)
        self.quick_checkbox = ctk.CTkCheckBox(self.sidebar_frame, text="Quick Mode", variable=self.quick_var)
        self.quick_checkbox.grid(row=8, column=0, padx=20, pady=(10, 10), sticky="w")

        self.template_var = ctk.StringVar(value="Standard Offer")
        self.template_dropdown = ctk.CTkOptionMenu(self.sidebar_frame, 
                                                 values=["Standard Offer", "YouTube Video", "Google Drive", "Instagram", "WhatsApp", "Delivery Tracking", "Security Alert"], 
                                                 variable=self.template_var)
        self.template_dropdown.grid(row=9, column=0, padx=20, pady=(10, 10), sticky="ew")

        self.start_button = ctk.CTkButton(self.sidebar_frame, text="START SCAN", command=self.start_scan, fg_color="red", hover_color="darkred")
        self.start_button.grid(row=10, column=0, padx=20, pady=20, sticky="ew")

        self.stop_button = ctk.CTkButton(self.sidebar_frame, text="STOP", command=self.stop_scan, fg_color="gray", state="disabled")
        self.stop_button.grid(row=11, column=0, padx=20, pady=(0, 20), sticky="ew")

        # Main frame with Tabs
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        self.tabview.add("Dashboard")
        self.tabview.add("Live Map")
        self.tabview.add("Case History")
        self.tabview.add("Settings")

        # Dashboard Tab
        self.tabview.tab("Dashboard").grid_rowconfigure(1, weight=1)
        self.tabview.tab("Dashboard").grid_columnconfigure(0, weight=1)
        
        # Stat Cards
        self.stats_frame = ctk.CTkFrame(self.tabview.tab("Dashboard"), fg_color="transparent")
        self.stats_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        self.stats_frame.grid_columnconfigure((0,1,2), weight=1)
        
        self.stat_status = ctk.CTkLabel(self.stats_frame, text=" SYSTEM: OFFLINE", font=ctk.CTkFont(weight="bold", size=14), text_color="gray")
        self.stat_status.grid(row=0, column=0)
        
        self.stat_targets = ctk.CTkLabel(self.stats_frame, text=" TARGETS CAPTURED: 0", font=ctk.CTkFont(weight="bold", size=14), text_color="cyan")
        self.stat_targets.grid(row=0, column=1)
        
        self.stat_latest = ctk.CTkLabel(self.stats_frame, text=" LATEST: N/A", font=ctk.CTkFont(weight="bold", size=14), text_color="orange")
        self.stat_latest.grid(row=0, column=2)
        
        self.console_textbox = ctk.CTkTextbox(self.tabview.tab("Dashboard"), font=ctk.CTkFont(family="Consolas", size=12))
        self.console_textbox.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.console_textbox.insert("0.0", "Welcome to Phone Tracker Pro v5.0\nWaiting for commands...\n")
        self.console_textbox.configure(state="disabled")

        self.progress = ctk.CTkProgressBar(self.tabview.tab("Dashboard"), progress_color="red")
        self.progress.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))
        self.progress.set(0)

        # Tracking Link Row
        self.link_frame = ctk.CTkFrame(self.tabview.tab("Dashboard"), fg_color="transparent")
        
        self.warning_lbl = ctk.CTkLabel(self.tabview.tab("Dashboard"), 
                                        text="⚠️ MANTENGA ESTA VENTANA ABIERTA PARA RECIBIR DATOS", 
                                        text_color="orange", font=ctk.CTkFont(weight="bold"))
        self.warning_lbl.grid(row=4, column=0, pady=5)
        self.link_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 10))
        self.link_frame.grid_columnconfigure(1, weight=1)

        self.link_label = ctk.CTkLabel(self.link_frame, text="Tracking Link:", font=ctk.CTkFont(weight="bold"))
        self.link_label.grid(row=0, column=0, padx=(0, 10))

        self.link_entry = ctk.CTkEntry(self.link_frame, placeholder_text="Waiting for link...", height=35)
        self.link_entry.grid(row=0, column=1, sticky="ew")
        
        self.copy_btn = ctk.CTkButton(self.link_frame, text=" COPY ", width=60, height=35, command=self.copy_link, fg_color="#2244aa")
        self.copy_btn.grid(row=0, column=2, padx=(10, 0))

        # Live Map Tab
        self.tabview.tab("Live Map").grid_rowconfigure(1, weight=1)
        self.tabview.tab("Live Map").grid_columnconfigure(0, weight=1)

        map_controls = ctk.CTkFrame(self.tabview.tab("Live Map"), fg_color="transparent")
        map_controls.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        self.plot_all_btn = ctk.CTkButton(map_controls, text=" Plot All Cases", width=150, command=self.plot_all_cases, fg_color="#2244aa")
        self.plot_all_btn.pack(side="left", padx=5)
        self.clear_map_btn = ctk.CTkButton(map_controls, text=" Clear Map", width=120, command=self.clear_map, fg_color="#555")
        self.clear_map_btn.pack(side="left", padx=5)
        
        self.map_widget = tkintermapview.TkinterMapView(self.tabview.tab("Live Map"), corner_radius=0)
        self.map_widget.grid(row=1, column=0, sticky="nsew")
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        self.map_widget.set_position(0, 0)
        self.map_widget.set_zoom(2)

        # Case History Tab
        self.tabview.tab("Case History").grid_rowconfigure(1, weight=1)
        self.tabview.tab("Case History").grid_columnconfigure(0, weight=1)
        
        self.refresh_btn = ctk.CTkButton(self.tabview.tab("Case History"), text="Refresh History", command=self.load_history)
        self.refresh_btn.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.history_frame = ctk.CTkScrollableFrame(self.tabview.tab("Case History"))
        self.history_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # Settings Tab
        self.webhook_label = ctk.CTkLabel(self.tabview.tab("Settings"), text="Discord Webhook URL (For IP Grabber Alerts):", font=ctk.CTkFont(weight="bold"))
        self.webhook_label.pack(pady=(20, 5), padx=20, anchor="w")
        self.webhook_entry = ctk.CTkEntry(self.tabview.tab("Settings"), width=400, placeholder_text="https://discord.com/api/webhooks/...")
        self.webhook_entry.pack(pady=5, padx=20, anchor="w")
        
        self.sound_alert_var = ctk.BooleanVar(value=True)
        self.sound_alert_cb = ctk.CTkCheckBox(self.tabview.tab("Settings"), text="Play Sound on Target Capture", variable=self.sound_alert_var)
        self.sound_alert_cb.pack(pady=20, padx=20, anchor="w")

        self.snapcam_var = ctk.BooleanVar(value=False)
        self.snapcam_cb = ctk.CTkCheckBox(self.tabview.tab("Settings"), text=" Enable SnapCam (Request Front Camera Capture)", variable=self.snapcam_var, text_color="orange")
        self.snapcam_cb.pack(pady=10, padx=20, anchor="w")

        self.theme_var = ctk.StringVar(value="Standard Grey")
        self.theme_label = ctk.CTkLabel(self.tabview.tab("Settings"), text="Console Theme Engine:")
        self.theme_label.pack(pady=(20, 0), padx=20, anchor="w")
        self.theme_dropdown = ctk.CTkOptionMenu(self.tabview.tab("Settings"), values=["Standard Grey", "Matrix Green", "Crimson Red", "FBI Blue"], variable=self.theme_var, command=self.change_theme)
        self.theme_dropdown.pack(pady=5, padx=20, anchor="w")

        self.ngrok_label = ctk.CTkLabel(self.tabview.tab("Settings"), text="Ngrok Auth Token (Optional):", font=ctk.CTkFont(weight="bold"))
        self.ngrok_label.pack(pady=(20, 5), padx=20, anchor="w")
        self.ngrok_entry = ctk.CTkEntry(self.tabview.tab("Settings"), width=400, placeholder_text="Enter your authtoken...")
        self.ngrok_entry.pack(pady=5, padx=20, anchor="w")

        self.map_style_var = ctk.StringVar(value="Google Maps")
        self.map_style_label = ctk.CTkLabel(self.tabview.tab("Settings"), text="Map Style:")
        self.map_style_label.pack(pady=(20, 0), padx=20, anchor="w")
        self.map_style_dropdown = ctk.CTkOptionMenu(self.tabview.tab("Settings"), values=["Google Maps", "OpenStreetMap", "Satellite"], variable=self.map_style_var, command=self.change_map_style)
        self.map_style_dropdown.pack(pady=5, padx=20, anchor="w")

        self.auto_dossier_var = ctk.BooleanVar(value=True)
        self.auto_dossier_cb = ctk.CTkCheckBox(self.tabview.tab("Settings"), text="Auto-Open Dossier (after collection)", variable=self.auto_dossier_var)
        self.auto_dossier_cb.pack(pady=10, padx=20, anchor="w")

        self.save_settings_btn = ctk.CTkButton(self.tabview.tab("Settings"), text=" SAVE SETTINGS", fg_color="#228822", hover_color="#1a661a", command=self.manual_save)
        self.save_settings_btn.pack(pady=20, padx=20, anchor="w")

        self.process = None
        self.target_count = 0
        self.load_history()
        self.load_config()

    def load_config(self):
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(base_dir, self.config_file)
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                self.phone_entry.insert(0, config.get("phone", ""))
                self.prefix_var.set(config.get("prefix", "+56"))
                self.officer_entry.insert(0, config.get("officer", ""))
                self.case_entry.insert(0, config.get("case_id", ""))
                self.grabber_var.set(config.get("grabber", False))
                self.quick_var.set(config.get("quick", False))
                self.template_var.set(config.get("template", "Standard Offer"))
                self.webhook_entry.insert(0, config.get("webhook", ""))
                self.sound_alert_var.set(config.get("sound_alert", True))
                self.snapcam_var.set(config.get("snapcam", False))
                self.theme_var.set(config.get("theme", "Standard Grey"))
                self.ngrok_entry.insert(0, config.get("ngrok_token", ""))
                self.map_style_var.set(config.get("map_style", "Google Maps"))
                self.auto_dossier_var.set(config.get("auto_dossier", True))
                
                self.change_theme(self.theme_var.get())
                self.change_map_style(self.map_style_var.get())
                self.append_text("[CONFIG] Settings loaded from file.\n")
            except Exception as e:
                self.append_text(f"[CONFIG] Error loading: {e}\n")

    def save_config(self):
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(base_dir, self.config_file)
        config = {
            "phone": self.phone_entry.get(),
            "prefix": self.prefix_var.get(),
            "officer": self.officer_entry.get(),
            "case_id": self.case_entry.get(),
            "grabber": self.grabber_var.get(),
            "quick": self.quick_var.get(),
            "template": self.template_var.get(),
            "webhook": self.webhook_entry.get(),
            "sound_alert": self.sound_alert_var.get(),
            "snapcam": self.snapcam_var.get(),
            "theme": self.theme_var.get(),
            "ngrok_token": self.ngrok_entry.get(),
            "map_style": self.map_style_var.get(),
            "auto_dossier": self.auto_dossier_var.get()
        }
        try:
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            self.append_text(f"[CONFIG] Error saving: {e}\n")

    def manual_save(self):
        self.save_config()
        self.append_text("[CONFIG] Settings saved manually.\n")

    def change_theme(self, choice):
        colors = {"Standard Grey": "#ffffff", "Matrix Green": "#00ff00", "Crimson Red": "#ff3333", "FBI Blue": "#3399ff"}
        prog_colors = {"Standard Grey": "red", "Matrix Green": "#00aa00", "Crimson Red": "darkred", "FBI Blue": "navy"}
        self.console_textbox.configure(text_color=colors.get(choice, "white"))
        self.progress.configure(progress_color=prog_colors.get(choice, "red"))


    def change_map_style(self, choice):
        if choice == "Google Maps":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga")
        elif choice == "OpenStreetMap":
            self.map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
        elif choice == "Satellite":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga")
        self.append_text(f"[SYSTEM] Map style changed to: {choice}\n")

    def copy_link(self):
        link = self.link_entry.get()
        if link and "Waiting" not in link:
            self.clipboard_clear()
            self.clipboard_append(link)
            self.append_text("\n[SYSTEM] Link copied to clipboard!\n")
        else:
            self.append_text("\n[ERROR] No link available to copy.\n")

    def append_text(self, text):
        if not isinstance(text, str):
            try:
                text = str(text)
            except Exception:
                text = "[unprintable output]"
                
        # Smart Auto-Scroll: only jump to bottom if scrollbar is already at bottom
        yview = self.console_textbox._textbox.yview()
        is_at_bottom = yview[1] >= 0.99
                
        self.console_textbox.configure(state="normal")
        self.console_textbox.insert("end", text)
        if is_at_bottom:
            self.console_textbox.see("end")
        self.console_textbox.configure(state="disabled")
        
        # Ghost Intel Link-Capture (v6.3)
        if "https://" in text:
            import re
            # Strip ANSI color codes
            clean_text = re.sub(r'\x1b\[[0-9;]*[mK]', '', text)
            links = re.findall(r"(https?://\S+)", clean_text)
            for link in links:
                l = link.strip().strip("'").strip('"').strip(']').strip('[')
                if "is.gd" in l or "ngrok-free.dev" in l:
                    self.link_entry.configure(state="normal")
                    self.link_entry.delete(0, "end")
                    self.link_entry.insert(0, l)
        
        # Process events for Stat Cards
        if "TARGET CAPTURED" in text:
            self.target_count += 1
            self.stat_targets.configure(text=f" TARGETS CAPTURED: {self.target_count}")
            import datetime
            self.stat_latest.configure(text=f" LATEST: {datetime.datetime.now().strftime('%H:%M:%S')}")
        
        # Super basic progress heuristics
        if "PHASE 3" in text:
            self.progress.set(0.3)
        elif "OSINT" in text:
            self.progress.set(0.6)
        elif "GENERATING REPORTS" in text:
            self.progress.set(0.9)
        elif "Server running" in text or "collection complete" in text:
            self.progress.set(1.0)
            self.stat_status.configure(text=" SYSTEM: ONLINE", text_color="#00ff00")

    def view_case(self, case_path):
        import json
        from PIL import Image
        
        try:
            self.tabview.add("Case Viewer")
        except ValueError:
            pass # Tab already exists
            
        self.tabview.set("Case Viewer")
        tab = self.tabview.tab("Case Viewer")
        
        for widget in tab.winfo_children():
            widget.destroy()
            
        scroll_frame = ctk.CTkScrollableFrame(tab)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        title = ctk.CTkLabel(scroll_frame, text=" OSINT FORENSIC DOSSIER", font=ctk.CTkFont(size=20, weight="bold"), text_color="red")
        title.pack(pady=10)
        
        try:
            with open(case_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            captures = data.get("captures", [])
            disk_images = sorted(glob.glob(case_path.replace(".json", "_*.jpg")))

            def _show_img(parent, pil_img, label):
                try:
                    pil_img.thumbnail((300, 300))
                    ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=pil_img.size)
                    lbl = ctk.CTkLabel(parent, image=ctk_img, text="")
                    lbl._ref = ctk_img
                    lbl.pack(pady=5)
                    ctk.CTkLabel(parent, text=label, text_color="orange", font=ctk.CTkFont(weight="bold")).pack()
                except Exception:
                    pass

            # Snapcam Image
            img_pattern = case_path.replace(".json", "_*.jpg")
            images = glob.glob(img_pattern)
            if images:
                try:
                    img_data = Image.open(images[-1])
                    # resize to fit
                    img_data.thumbnail((300, 300))
                    ctk_img = ctk.CTkImage(light_image=img_data, dark_image=img_data, size=img_data.size)
                    img_lbl = ctk.CTkLabel(scroll_frame, image=ctk_img, text="")
                    img_lbl.pack(pady=10)
                    tag = ctk.CTkLabel(scroll_frame, text=" SNAPCAM CAPTURE", text_color="orange", font=ctk.CTkFont(weight="bold"))
                    tag.pack(pady=5)
                except Exception as e:
                    pass
            
            # Parse captures
            captures = data.get("captures", [])
            for i, c in enumerate(captures):
                card = ctk.CTkFrame(scroll_frame)
                card.pack(fill="x", pady=10, padx=10)
                
                header = ctk.CTkLabel(card, text=f" Capture #{i+1}    {c.get('captured_ip','Unknown')}", font=ctk.CTkFont(weight="bold", size=13))
                header.pack(anchor="w", padx=10, pady=5)

                # Try disk image first, then decode from JSON base64
                if i < len(disk_images):
                    try:
                        _show_img(card, Image.open(disk_images[i]), f" SnapCam #{i+1}")
                    except Exception:
                        pass
                elif c.get("base64_image"):
                    try:
                        import base64 as _b64, io as _io
                        raw = c["base64_image"]
                        if "," in raw:
                            raw = raw.split(",", 1)[1]
                        img_pil = Image.open(_io.BytesIO(_b64.b64decode(raw)))
                        save_path = case_path.replace(".json", f"_{i+1}.jpg")
                        img_pil.save(save_path, "JPEG", quality=85)
                        _show_img(card, img_pil, f" SnapCam #{i+1} (extracted from JSON  {save_path})")
                    except Exception:
                        pass
                
                info = f"Time: {c.get('capture_time', '')}\n"
                addr = c.get('street_address', '')
                if addr:
                    info += f" {addr}\n"
                info += f"Device: {c.get('platform', '')} | Battery: {c.get('battery', '')} | Network: {c.get('network', '')}\n"
                webgl = c.get('webgl_renderer', '')
                if webgl:
                    info += f"GPU: {webgl} | CPU: {c.get('cpu_cores','?')} cores | RAM: {c.get('ram_gb','?')}GB\n"
                gps_lat = c.get('gps_lat')
                gps_lon = c.get('gps_lon')
                if gps_lat and gps_lon:
                    info += f"GPS: {gps_lat}, {gps_lon} (Acc: {c.get('gps_accuracy','')}m)\n"
                    info += f"Maps: https://maps.google.com/?q={gps_lat},{gps_lon}\n"
                else:
                    info += "GPS: Not captured\n"
                info += f"Browser: {c.get('userAgent', '')[:80]}"
                
                txt = ctk.CTkTextbox(card, height=160)
                txt.pack(fill="x", padx=10, pady=5)
                txt.insert("0.0", info)
                txt.configure(state="disabled")

        except Exception as e:
            err = ctk.CTkLabel(scroll_frame, text=f"Error reading case: {e}")
            err.pack(pady=20)

        # Export button at bottom
        export_btn = ctk.CTkButton(scroll_frame, text=" Export Dossier HTML", fg_color="#aa4400",
                                   command=lambda: self.export_dossier(case_path))
        export_btn.pack(pady=15)


    def export_dossier(self, case_path):
        import json, base64, webbrowser
        try:
            with open(case_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            return
        
        captures = data.get("captures", [])
        img_html = ""
        img_pattern = case_path.replace(".json", "_*.jpg")
        images = glob.glob(img_pattern)
        if images:
            try:
                with open(images[-1], "rb") as imgf:
                    b64 = base64.b64encode(imgf.read()).decode()
                img_html = f'<img src="data:image/jpeg;base64,{b64}" style="max-width:300px;border-radius:8px;border:2px solid #ff4444;"/>'
            except Exception:
                pass

        rows = ""
        for i, c in enumerate(captures):
            addr = c.get('street_address', 'N/A')
            gmap = ""
            if c.get('gps_lat') and c.get('gps_lon'):
                gmap = f'<a href="https://maps.google.com/?q={c["gps_lat"]},{c["gps_lon"]}" target="_blank" style="color:#4af">Open in Google Maps</a>'
            rows += f"""
            <tr>
                <td>#{i+1}</td><td>{c.get('captured_ip','')}</td>
                <td>{addr}<br>{gmap}</td>
                <td>{c.get('battery','')} | Charging: {c.get('charging','')}</td>
                <td>{c.get('network','')}</td>
                <td>{c.get('webgl_renderer','')}<br>CPU: {c.get('cpu_cores','?')} | RAM: {c.get('ram_gb','?')}GB</td>
                <td>{c.get('capture_time','')}</td>
            </tr>"""
        
        html = f"""<!DOCTYPE html><html><head><meta charset='utf-8'>
        <title>Dossier - {os.path.basename(case_path)}</title>
        <style>
            body{{background:#0d0d0d;color:#e0e0e0;font-family:monospace;padding:20px;}}
            h1{{color:#ff4444;}} h2{{color:#aaffaa;border-bottom:1px solid #333;padding-bottom:5px;}}
            table{{width:100%;border-collapse:collapse;margin-top:10px;}}
            th{{background:#1a1a2e;color:#4af;padding:8px;text-align:left;}}
            td{{border:1px solid #333;padding:8px;vertical-align:top;font-size:12px;}}
            .snapcam{{text-align:center;padding:20px;border:1px solid #aa4400;margin:20px 0;border-radius:8px;}}
        </style></head><body>
        <h1> OSINT FORENSIC DOSSIER</h1>
        <p>Case File: <b>{os.path.basename(case_path)}</b> &nbsp;|&nbsp; Target: <b>{data.get('target','N/A')}</b></p>
        {'<div class="snapcam"><h2> SNAPCAM CAPTURE</h2>' + img_html + '</div>' if img_html else ''}
        <h2>Capture Records</h2>
        <table><tr><th>#</th><th>IP</th><th>Address / Map</th><th>Battery</th><th>Network</th><th>Hardware</th><th>Time</th></tr>
        {rows}</table>
        </body></html>"""

        out_path = case_path.replace(".json", "_dossier.html")
        with open(out_path, "w", encoding="utf-8") as fout:
            fout.write(html)
        webbrowser.open(out_path)


    def plot_all_cases(self):
        files = glob.glob("output/*.json")
        if not files:
            return
        self.map_widget.delete_all_marker()
        plotted = 0
        for f in files:
            try:
                with open(f, 'r', encoding='utf-8') as jf:
                    data = json.load(jf)
                for c in data.get("captures", []):
                    lat = c.get("gps_lat")
                    lon = c.get("gps_lon")
                    ip = c.get("captured_ip", "?")
                    has_snap = bool(c.get("base64_image"))
                    if lat and lon:
                        label = f" {ip}"  # Red = GPS confirmed
                    else:
                        ip_i = c.get("ip_info", {})
                        lat = ip_i.get("loc", ",").split(",")[0]
                        lon_v = ip_i.get("loc", ",").split(",")[1] if "," in ip_i.get("loc", ",") else None
                        if lat and lon_v:
                            lat, lon = float(lat), float(lon_v)
                            label = f" {ip}"  # Yellow = IP only
                        else:
                            continue
                    try:
                        self.map_widget.set_marker(float(lat), float(lon), text=label)
                        plotted += 1
                    except Exception:
                        pass
            except Exception:
                pass
        if plotted > 0:
            self.tabview.set("Live Map")
        self.append_text(f"\n[ MAP] Plotted {plotted} historical captures.\n")


    def clear_map(self):
        self.map_widget.delete_all_marker()
        self.map_widget.set_position(0, 0)
        self.map_widget.set_zoom(2)


    def load_history(self):
        for widget in self.history_frame.winfo_children():
            widget.destroy()
        
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(base_dir, "output")
            
        if not os.path.exists(output_dir):
            l = ctk.CTkLabel(self.history_frame, text="No cases found.")
            l.pack(pady=10)
            return
            
        files = glob.glob(os.path.join(output_dir, "*.json"))
        if not files:
            l = ctk.CTkLabel(self.history_frame, text="No scan reports found.")
            l.pack(pady=10)
            return
            
        for f in reversed(sorted(files, key=os.path.getmtime)):
            basename = os.path.basename(f)
            mtime = os.path.getmtime(f)
            dt_str = datetime.datetime.fromtimestamp(mtime).strftime('%d-%b-%Y %H:%M')
            
            frame = ctk.CTkFrame(self.history_frame)
            frame.pack(fill="x", pady=5, padx=5)
            lbl = ctk.CTkLabel(frame, text=f" {basename.replace('.json','')}  |   {dt_str}")
            lbl.pack(side="left", padx=10, fill="x")
            btn = ctk.CTkButton(frame, text="View Case", width=80, command=lambda x=f: self.view_case(x))
            btn.pack(side="right", padx=10, pady=5)

    def _scan_finished(self):
        self.append_text("\n[PROCESS TERMINATED]\n")
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.stat_status.configure(text=" SYSTEM: OFFLINE", text_color="gray")
        self.load_history()

    def start_scan(self):
        # combine prefix and phone
        prefix = self.prefix_var.get()
        phone = self.phone_entry.get().strip()
        
        if not phone:
            self.append_text("[ERROR] Please enter a target phone number.\n")
            return

        full_phone = prefix + phone
        
        # Save config on start
        self.save_config()

        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal", fg_color="red")
        self.console_textbox.configure(state="normal")
        self.console_textbox.delete("0.0", "end")
        self.console_textbox.configure(state="disabled")
        self.progress.set(0.1)

        self.append_text(f"Starting tracking for {full_phone}...\n")
        threading.Thread(target=self._run_internal, args=(full_phone,), daemon=True).start()

    def stop_scan(self):
        self.append_text("\n[STOPPING PROCESS...]\n")
        sys.exit(0)

    def update_map(self, lat, lon):
        def _do_update():
            try:
                self.map_widget.set_position(float(lat), float(lon))
                self.map_widget.set_zoom(12)
                self.map_widget.set_marker(float(lat), float(lon), text="Target")
            except:
                pass
        self.after(0, _do_update)

    def _run_internal(self, phone):
        import io
        import sys
        import phone_tracker
        from unittest.mock import patch
        import traceback
        
        # Immediate debug at start
        self.after(0, self.append_text, "[DEBUG 1] _run_internal started\n")
        
        class GUIStream(io.StringIO):
            def __init__(self, app):
                super().__init__()
                self.app = app
            def write(self, string):
                if string:
                    try:
                        self.app.after(0, self.app.append_text, string)
                    except:
                        pass
        
        stream = GUIStream(self)
        self.after(0, self.append_text, "[DEBUG 2] Stream created\n")
        
        try:
            self.after(0, self.append_text, f"[DEBUG 3] phone_tracker module loaded from: {phone_tracker.__file__}\n")
            
            argv = ["phone_tracker.py", phone]
            if self.officer_entry.get().strip():
                argv.extend(["--officer", self.officer_entry.get().strip()])
            if self.case_entry.get().strip():
                argv.extend(["--case", self.case_entry.get().strip()])
            if self.quick_var.get():
                argv.append("--quick")
            if self.grabber_var.get():
                argv.append("--grab")

            os.environ["TEMPLATE_CHOICE"] = self.template_var.get()
            os.environ["PLAY_SOUND"] = "1" if self.sound_alert_var.get() else "0"
            os.environ["ENABLE_SNAPCAM"] = "1" if self.snapcam_var.get() else "0"
            if self.ngrok_entry.get().strip():
                os.environ["NGROK_AUTHTOKEN"] = self.ngrok_entry.get().strip()

            self.after(0, self.append_text, f"[DEBUG 4] Setting up callbacks, argv={argv}\n")
            
            phone_tracker._gui_map_update = self.update_map
            if self.webhook_entry.get().strip():
                os.environ["DISCORD_WEBHOOK"] = self.webhook_entry.get().strip()
            
            self.after(0, self.append_text, "[DEBUG 5] About to call phone_tracker.main()\n")
            
            with patch("sys.stdout", stream), patch("sys.argv", argv):
                from rich.console import Console
                phone_tracker.console = Console(file=stream, force_terminal=False, color_system=None)
                phone_tracker.main()
            
            # Auto-Open Dossier Logic
            if self.auto_dossier_var.get():
                try:
                    import glob, webbrowser
                    # Look for the latest matching report in output/
                    clean_num = phone.replace("+", "")
                    reports = glob.glob(f"output/phone_intel_{clean_num}_*.html")
                    if reports:
                        latest_report = sorted(reports)[-1]
                        self.after(0, self.append_text, f"[SYSTEM] Auto-opening dossier: {latest_report}\n")
                        webbrowser.open(os.path.abspath(latest_report))
                except Exception as ex:
                    self.after(0, self.append_text, f"[WARN] Failed to auto-open report: {ex}\n")
                
            self.after(0, self.append_text, "[DEBUG 6] main() completed normally\n")
        except Exception as e:
            tb = traceback.format_exc()
            self.after(0, self.append_text, f"\n[EXCEPTION] {e}\n")
            self.after(0, self.append_text, f"[TRACE] {tb}\n")
        finally:
            self.after(0, self._scan_finished)

if __name__ == "__main__":
    app = App()
    app.mainloop()


