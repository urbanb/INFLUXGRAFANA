#!/usr/bin/env python3
"""
OpenClaw Metrics Sender für Telegraf
Sendet Metriken an den Telegraf HTTP Listener
"""

import requests
import json
import time
from datetime import datetime, timezone

TELEGRAF_URL = "http://localhost:8180/telegraf"

def send_metric(measurement, tags, fields):
    """
    Sendet eine Metrik an Telegraf (InfluxDB Line Protocol)
    """
    # Line Protocol Format: measurement,tag1=value1 field1=value1 timestamp
    tag_str = ",".join([f"{k}={v}" for k, v in tags.items()]) if tags else ""
    field_str = ",".join([f"{k}={v}" if isinstance(v, (int, float)) else f'{k}="{v}"' for k, v in fields.items()])
    
    if tag_str:
        line = f"{measurement},{tag_str} {field_str}"
    else:
        line = f"{measurement} {field_str}"
    
    try:
        response = requests.post(TELEGRAF_URL, data=line, timeout=5)
        if response.status_code == 204:
            print(f"✅ Sent: {measurement}")
            return True
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Failed to send: {e}")
        return False

def log_session_start():
    """Loggt Session Start"""
    return send_metric(
        "session_event",
        {"agent": "nyx", "event_type": "start"},
        {"value": 1}
    )

def log_session_end(duration_min, total_tokens, tools_used):
    """Loggt Session Ende"""
    return send_metric(
        "session_summary",
        {"agent": "nyx"},
        {
            "duration_min": float(duration_min),
            "total_tokens": int(total_tokens),
            "tools_used": int(tools_used)
        }
    )

def log_tool_usage(tool_name, success=True):
    """Loggt Tool-Nutzung"""
    return send_metric(
        "tool_usage",
        {"tool": tool_name, "success": str(success).lower()},
        {"count": 1}
    )

def log_message_sent(message_type="text"):
    """Loggt gesendete Nachricht"""
    return send_metric(
        "message_activity",
        {"type": message_type},
        {"count": 1}
    )

def log_custom_event(event_name, value=1):
    """Loggt beliebiges Event"""
    return send_metric(
        "custom_event",
        {"event": event_name},
        {"value": value}
    )

# Test
if __name__ == "__main__":
    print("🧪 Testing Telegraf connection...")
    print(f"Sending to: {TELEGRAF_URL}")
    
    # Test Metriken
    log_session_start()
    log_tool_usage("browser", success=True)
    log_tool_usage("web_search", success=True)
    log_message_sent("text")
    
    print("\n✅ Test complete!")
    print("Check InfluxDB for data: influxdb3 query 'SELECT * FROM session_event'")