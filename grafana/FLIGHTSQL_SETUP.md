# Grafana Datenquelle Konfiguration für InfluxDB 3.0

## ⚠️ Wichtig: InfluxDB 3.0 hat KEINE native InfluxQL-Unterstützung!

Die einzige zuverlässige Lösung ist der **Flight SQL** Connector.

## 🔧 Schritt-für-Schritt Einrichtung

### 1. Flight SQL Plugin installieren

In Grafana:
1. **Configuration** → **Plugins**
2. Suche nach **"Flight SQL"**
3. Klicke **Install**

### 2. Datenquelle erstellen

1. **Configuration** → **Data Sources**
2. **Add data source**
3. Wähle **"Flight SQL"** (nicht "InfluxDB"!)

### 3. Konfiguration

| Feld | Wert |
|------|------|
| **Name** | InfluxDB3-FlightSQL |
| **Host:Port** | localhost:8181 |
| **Database** | openclaw_metrics |
| **Username** | (leer lassen) |
| **Token** | apiv3_mmadkJ8rv4SQN5NIqjHp99_C4PIZuzLWbWjldnPK1vinqBRVVF6o6aB0NO1rREDWacNswd9w0IRWj1r5K5Ja2Q |

### 4. Test & Save

Klicke **"Save & Test"**

---

## 🎯 Alternative: Einfacher Python Viewer

Falls Flight SQL nicht funktioniert, habe ich ein Python-Script erstellt:

```bash
cd /Users/sen01/.openclaw/workspace/INFLUXGRAFANA
python3 viewer.py
```

Öffnet einen Browser unter http://localhost:8050

---

## 📊 Dashboard Import

NACH der FlightSQL-Einrichtung:

1. **+** → **Import**
2. Lade `dashboard_flightsql.json`
3. Wähle Datenquelle **"InfluxDB3-FlightSQL"**
4. **Import**

---

## 🚨 Fallback: InfluxDB 2.x

Falls nichts funktioniert:

```bash
brew uninstall influxdb influxdb-cli
brew install influxdb@2
```

InfluxDB 2.x hat perfekten Grafana-Support.