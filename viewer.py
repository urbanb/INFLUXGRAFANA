#!/usr/bin/env python3
"""
OpenClaw Metrics Viewer
Einfaches Web-Dashboard für InfluxDB 3.0
Keine Grafana-Konfiguration nötig!
"""

import http.server
import socketserver
import json
import requests
from datetime import datetime, timedelta
import webbrowser
from threading import Timer

# Konfiguration
INFLUX_URL = "http://localhost:8181"
DATABASE = "openclaw_metrics"
TOKEN = "apiv3_mmadkJ8rv4SQN5NIqjHp99_C4PIZuzLWbWjldnPK1vinqBRVVF6o6aB0NO1rREDWacNswd9w0IRWj1r5K5Ja2Q"
PORT = 8050

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def query_influx(sql):
    """Führt SQL Query aus"""
    url = f"{INFLUX_URL}/api/v3/query_sql?db={DATABASE}"
    try:
        response = requests.post(url, headers=HEADERS, json={"query": sql}, timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def get_latest_metrics():
    """Holt aktuelle Metriken"""
    metrics = {}
    
    # CPU
    result = query_influx("SELECT time, 100.0 - usage_idle as cpu_usage FROM cpu WHERE cpu = 'cpu-total' ORDER BY time DESC LIMIT 1")
    if result and 'results' in result:
        metrics['cpu'] = result['results'][0]['cpu_usage'] if result['results'] else 0
    else:
        metrics['cpu'] = 0
    
    # Memory
    result = query_influx("SELECT used_percent, available FROM mem ORDER BY time DESC LIMIT 1")
    if result and 'results' in result:
        metrics['mem_percent'] = result['results'][0]['used_percent'] if result['results'] else 0
        metrics['mem_available'] = result['results'][0]['available'] if result['results'] else 0
    else:
        metrics['mem_percent'] = 0
        metrics['mem_available'] = 0
    
    # Tool Usage
    result = query_influx("SELECT COUNT(*) as total FROM tool_usage WHERE time >= now() - INTERVAL '1 hour'")
    if result and 'results' in result:
        metrics['tool_calls'] = result['results'][0]['total'] if result['results'] else 0
    else:
        metrics['tool_calls'] = 0
    
    # Recent tools
    result = query_influx("SELECT time, tool, success FROM tool_usage ORDER BY time DESC LIMIT 10")
    if result and 'results' in result:
        metrics['recent_tools'] = result['results']
    else:
        metrics['recent_tools'] = []
    
    return metrics

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>OpenClaw Metrics Dashboard</title>
    <meta http-equiv="refresh" content="10">
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 20px; background: #f5f5f5; }
        h1 { color: #333; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-top: 20px; }
        .card { background: white; border-radius: 8px; padding: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .card h2 { margin-top: 0; color: #555; font-size: 14px; text-transform: uppercase; }
        .big-number { font-size: 48px; font-weight: bold; color: #333; }
        .unit { font-size: 18px; color: #666; }
        .gauge { width: 100%; height: 20px; background: #e0e0e0; border-radius: 10px; overflow: hidden; margin-top: 10px; }
        .gauge-fill { height: 100%; border-radius: 10px; transition: width 0.3s; }
        .green { background: #4caf50; }
        .yellow { background: #ff9800; }
        .red { background: #f44336; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th, td { text-align: left; padding: 8px; border-bottom: 1px solid #ddd; }
        th { color: #666; font-weight: 600; }
        .success { color: #4caf50; }
        .error { color: #f44336; }
        .timestamp { color: #999; font-size: 12px; }
        .status { display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 12px; }
        .status-ok { background: #e8f5e9; color: #2e7d32; }
        .status-error { background: #ffebee; color: #c62828; }
    </style>
</head>
<body>
    <h1>🔍 OpenClaw Metrics Dashboard</h1>
    <p class="timestamp">Letzte Aktualisierung: {timestamp}</p>
    
    <div class="grid">
        <div class="card">
            <h2>CPU Usage</h2>
            <div class="big-number">{cpu:.1f}<span class="unit">%</span></div>
            <div class="gauge">
                <div class="gauge-fill {cpu_color}" style="width: {cpu}%"></div>
            </div>
        </div>
        
        <div class="card">
            <h2>Memory Usage</h2>
            <div class="big-number">{mem_percent:.1f}<span class="unit">%</span></div>
            <div class="gauge">
                <div class="gauge-fill {mem_color}" style="width: {mem_percent}%"></div>
            </div>
            <p style="margin-top: 10px; color: #666;">
                {mem_available_gb:.1f} GB verfügbar
            </p>
        </div>
        
        <div class="card">
            <h2>Tool Calls (1h)</h2>
            <div class="big-number">{tool_calls}</div>
            <p style="color: #666;">API Aufrufe in der letzten Stunde</p>
        </div>
        
        <div class="card" style="grid-column: 1 / -1;">
            <h2>Recent Tool Usage</h2>
            <table>
                <tr>
                    <th>Zeit</th>
                    <th>Tool</th>
                    <th>Status</th>
                </tr>
                {tool_rows}
            </table>
        </div>
    </div>
</body>
</html>
"""

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            metrics = get_latest_metrics()
            
            # Farben bestimmen
            cpu_color = 'green' if metrics['cpu'] < 70 else 'yellow' if metrics['cpu'] < 90 else 'red'
            mem_color = 'green' if metrics['mem_percent'] < 70 else 'yellow' if metrics['mem_percent'] < 90 else 'red'
            
            # Tool-Rows generieren
            tool_rows = ""
            for tool in metrics['recent_tools']:
                time_str = tool.get('time', 'N/A')[:19] if 'time' in tool else 'N/A'
                tool_name = tool.get('tool', 'unknown')
                success = tool.get('success', 'true')
                status_class = 'success' if success == 'true' else 'error'
                status_text = '✅ Erfolg' if success == 'true' else '❌ Fehler'
                
                tool_rows += f"<tr><td>{time_str}</td><td>{tool_name}</td><td class='{status_class}'>{status_text}</td></tr>"
            
            if not tool_rows:
                tool_rows = "<tr><td colspan='3'>Keine Daten</td></tr>"
            
            html = HTML_TEMPLATE.format(
                timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                cpu=metrics['cpu'],
                cpu_color=cpu_color,
                mem_percent=metrics['mem_percent'],
                mem_color=mem_color,
                mem_available_gb=metrics['mem_available'] / (1024**3),
                tool_calls=int(metrics['tool_calls']),
                tool_rows=tool_rows
            )
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode())
        elif self.path == '/api/metrics':
            metrics = get_latest_metrics()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(metrics).encode())
        else:
            self.send_error(404)
    
    def log_message(self, format, *args):
        pass  # Logging deaktivieren

def open_browser():
    webbrowser.open(f'http://localhost:{PORT}')

if __name__ == '__main__':
    print(f"🚀 Starte OpenClaw Metrics Viewer...")
    print(f"📊 Dashboard: http://localhost:{PORT}")
    print(f"🔧 API: http://localhost:{PORT}/api/metrics")
    print(f"\nDrücke Ctrl+C zum Beenden")
    
    # Browser nach 1 Sekunde öffnen
    Timer(1, open_browser).start()
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Beendet")
