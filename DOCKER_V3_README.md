# Docker Setup für InfluxDB 3.x + Grafana

## ⚠️ WICHTIGE HINWEISE

### InfluxDB 3.x Status
- **Noch nicht produktionsreif** (Alpha/Beta Status)
- **Kein offizielles Docker Image** verfügbar
- **Keine eingebaute Web-UI** (nur API)
- **Eingeschränkte Grafana-Unterstützung** (nur über Flight SQL Plugin)

### Empfohlene Alternative
**InfluxDB 2.7** ist stabil und hat volle Grafana-Unterstützung:
```bash
docker-compose -f docker-compose.yml up -d  # Nutzt 2.7
```

---

## 🚀 InfluxDB 3.x Setup (Experimentell)

### 1. Voraussetzungen
Docker Desktop muss laufen.

### 2. Starten
```bash
cd /Users/sen01/.openclaw/workspace/INFLUXGRAFANA
docker-compose -f docker-compose-v3.yml up -d --build
```

**Hinweis:** Das erste Mal wird das InfluxDB 3.x Image gebaut (kann 5-10 Minuten dauern).

### 3. Zugriff

| Service | URL | Hinweis |
|---------|-----|---------|
| **InfluxDB 3.x API** | http://localhost:8181 | Nur API, keine UI |
| **Grafana** | http://localhost:3000 | Login: admin/admin |

---

## 🔧 Grafana Konfiguration für InfluxDB 3.x

### Schritt 1: Flight SQL Plugin installieren
1. Grafana öffnen: http://localhost:3000
2. **Configuration** → **Plugins**
3. Suche **"Flight SQL"** und installiere es

### Schritt 2: Datenquelle einrichten
1. **Configuration** → **Data Sources**
2. **Add data source** → Wähle **"Flight SQL"**
3. Einstellungen:
   - **Host**: `influxdb3:8181`
   - **Database**: `openclaw_metrics`
   - **Token**: (leer lassen oder `admin`)

### Schritt 3: Dashboard importieren
Das Dashboard muss angepasst werden für Flight SQL/SQL Syntax!

---

## 🐳 Images

| Service | Image/Basis | Größe |
|---------|-------------|-------|
| **InfluxDB 3.x** | Custom Build (Ubuntu + Binary) | ~150 MB |
| **Grafana** | `grafana/grafana:latest` | ~150 MB |
| **Telegraf** | `telegraf:latest` | ~100 MB |

---

## 🛠️ Befehle

```bash
# Starten (mit Build)
docker-compose -f docker-compose-v3.yml up -d --build

# Stoppen
docker-compose -f docker-compose-v3.yml down

# Logs
docker-compose -f docker-compose-v3.yml logs -f

# Vollständiges Löschen
docker-compose -f docker-compose-v3.yml down -v
```

---

## ❓ Warum ist 3.x so kompliziert?

| Feature | InfluxDB 2.7 | InfluxDB 3.x |
|---------|--------------|--------------|
| Offizielles Docker Image | ✅ Ja | ❌ Nein |
| Web UI | ✅ Ja | ❌ Nein |
| Grafana InfluxQL | ✅ Ja | ❌ Nein |
| Grafana Flight SQL | ❌ Nein | ✅ Ja (Plugin) |
| Stabilität | ✅ Produktion | ⚠️ Alpha/Beta |

**Empfehlung:** Nutze `docker-compose.yml` (v2.7) für Produktion!

---

## 🔗 Links

- InfluxDB 3.x: https://github.com/influxdata/influxdb
- Flight SQL Plugin: https://grafana.com/grafana/plugins/influxdata-flightsql-datasource/