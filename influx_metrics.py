#!/usr/bin/env python3
"""
OpenClaw Metrics Writer für InfluxDB 3
Schreibt Session-Metriken in die lokale InfluxDB
"""

import requests
import json
import time
import os
from datetime import datetime, timezone

# === KONFIGURATION ===
INFLUX_URL = "http://localhost:8181"
DATABASE = "openclaw_metrics"
TOKEN = "apiv3_mmadkJ8rv4SQN5NIqjHp99_C4PIZuzLWbWjldnPK1vinqBRVVF6o6aB0NO1rREDWacNswd9w0IRWj1r5K5Ja2Q"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def write_metric(measurement, tags, fields):
    """
    Schreibt einen einzelnen Metrik-Punkt in InfluxDB
    
    Args:
        measurement: Name der Messung (z.B. "session_usage")
        tags: Dict mit Tags (z.B. {"agent": "nyx", "session": "main"})
        fields: Dict mit Feldern (z.B. {"duration_min": 30, "tokens": 1500})
    """
    timestamp = datetime.now(timezone.utc).isoformat()
    
    # InfluxDB 3 Line Protocol (vereinfacht)
    line = f"{measurement}"
    
    # Tags hinzufügen
    if tags:
        tag_str = ",".join([f"{k}={v}" for k, v in tags.items()])
        line += f",{tag_str}"
    
    # Fields hinzufügen
    field_str = ",".join([f"{k}={v}" if isinstance(v, (int, float)) else f'{k}="{v}"' for k, v in fields.items()])
    line += f" {field_str} {int(time.time() * 1_000_000_000)}"
    
    # An InfluxDB senden
    url = f"{INFLUX_URL}/api/v3/write_lp?db={DATABASE}"
    response = requests.post(url, headers=HEADERS, data=line)
    
    if response.status_code == 204:
        print(f"✅ Metric geschrieben: {measurement}")
    else:
        print(f"❌ Fehler: {response.status_code} - {response.text}")
    
    return response.status_code == 204

def log_session_start():
    """Loggt den Start einer neuen Session"""
    write_metric(
        "session_event",
        {"event_type": "start", "agent": "nyx"},
        {"value": 1}
    )

def log_session_end(duration_min, total_tokens, tools_used):
    """Loggt das Ende einer Session mit Metriken"""
    write_metric(
        "session_summary",
        {"agent": "nyx"},
        {
            "duration_min": duration_min,
            "total_tokens": total_tokens,
            "tools_used": tools_used
        }
    )

def log_tool_usage(tool_name, success=True):
    """Loggt die Nutzung eines Tools"""
    write_metric(
        "tool_usage",
        {"tool": tool_name, "success": str(success).lower()},
        {"count": 1}
    )

def log_message_sent(message_type="text"):
    """Loggt eine gesendete Nachricht"""
    write_metric(
        "message_activity",
        {"type": message_type},
        {"count": 1}
    )

# === TEST ===
if __name__ == "__main__":
    print("🧪 Teste InfluxDB Connection...")
    
    # Test-Metriken schreiben
    log_session_start()
    log_tool_usage("web_search", success=True)
    log_tool_usage("browser", success=True)
    log_message_sent("text")
    
    print("\n✅ Test abgeschlossen!")
    print(f"   URL: {INFLUX_URL}")
    print(f"   Database: {DATABASE}")
    print("\nDaten können jetzt in der InfluxDB UI angezeigt werden:")
    print(f"   http://localhost:8181")