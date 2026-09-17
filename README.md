# Campus Asset Tracker

A real-time IoT asset-tracking dashboard for monitoring physical assets across a campus environment. The system is designed to track BLE-tagged assets through a multi-layer IoT pipeline and surface live location, status, and alert data through a web dashboard.

---

## What This Project Does

Campus Asset Tracker addresses the problem of physical asset loss, misuse, and unauthorised removal on large campuses. Each tracked asset carries a BLE beacon. A network of ESP32 gateways detects nearby beacons and forwards telemetry through LoRa to a central Raspberry Pi hub, which publishes data via MQTT to a FastAPI ingestion service. Firebase Realtime Database acts as the live data store, and a React web dashboard presents the data to administrators.

---

## Current Implementation Status

> **Stage 1 — Dashboard layer only.**
>
> The current repository contains the **React/Firebase web dashboard** only.
>
> The hardware layer (BLE, ESP32, LoRa), the Raspberry Pi hub, the MQTT broker, and the FastAPI ingestion service have **not yet been implemented**.
>
> All asset, gateway, and alert data shown in the dashboard is currently **static mock data** defined inline in the React hooks. No live IoT data flows into the system at this stage.

---

## Architecture

### Currently Implemented

```
React/Vite Dashboard  ──reads──  Firebase Realtime Database
```

The Firebase Realtime Database schema is defined and the hooks are wired to it behind a `useMock` flag. Switching `useMock` to `false` in any hook will make it read live data from Firebase.

### Planned Full Architecture

```
BLE Asset Tags
     │  (Bluetooth Low Energy advertisement)
     ▼
ESP32 Gateway (per zone)
     │  (LoRa radio packet)
     ▼
Raspberry Pi Hub
     │  (MQTT publish)
     ▼
MQTT Broker
     │
     ▼
FastAPI Ingestion Service
     │  (Firebase Admin SDK write)
     ▼
Firebase Realtime Database
     │  (Firebase SDK onValue listener)
     ▼
React / Vite Dashboard  ──served to──  Browser
```

The ingestion pipeline (everything above Firebase) is planned for Stage 2.

---

## Current Features

| Feature           | Status              | Notes                                                               |
|-------------------|---------------------|---------------------------------------------------------------------|
| Authentication    | ✅ Fully implemented | Firebase Auth (email/password). `AuthProvider` + `useAuth` hook.   |
| Live Map          | ✅ UI implemented   | Leaflet map with colour-coded asset markers. Mock lat/lng data.     |
| Asset Registry    | ✅ UI implemented   | Searchable/filterable table. Mock data. Firebase hook ready.        |
| Gateway Health    | ✅ UI implemented   | Card grid with RSSI bars. Mock data. Firebase hook ready.           |
| Alerts            | ✅ UI implemented   | Alert list with severity icons. Mock data. Firebase hook ready.     |
| Geofences         | ⚠️ UI only          | Zone list + map view. **No geometry, no breach logic, all static.** |
| Reports           | ⚠️ Static only      | Hardcoded incident table. CSV export works. No Firebase integration.|
| Map view modes    | ⚠️ UI only          | Heatmap/Floorplan tabs are rendered but do nothing.                 |
| Alert acknowledge | ⚠️ UI only          | Acknowledge button renders but has no handler.                      |
| Geofence draw     | ⚠️ UI only          | "+ New Zone" and "Edit" buttons render but have no handlers.        |
| Nearby tab        | ⚠️ UI only          | "Nearby" panel tab renders but shows the same list as "All".        |

---

## Technology Stack (Current)

| Layer         | Technology                                |
|---------------|-------------------------------------------|
| Frontend      | React 19, Vite 8                          |
| Routing       | React Router DOM v7                       |
| Styling       | Vanilla CSS (custom dark design system)   |
| Maps          | Leaflet 1.9 + React-Leaflet 5             |
| Charts        | Recharts 3 (imported but not yet used)    |
| Icons         | Lucide React                              |
| Auth          | Firebase Authentication (email/password)  |
| Database      | Firebase Realtime Database                |
| Linting       | ESLint 9 (flat config)                    |
| Build         | Vite (Rolldown bundler)                   |

**Not yet in repository:** FastAPI, MQTT, Paho, ESP32 firmware, LoRa driver, Raspberry Pi services, Docker, Python simulator.

---

## Firebase Realtime Database Schema

The frontend hooks expect the following schema. Future ingestion services must write data in this structure.

### `/assets/{assetId}`

```json
{
  "name":     "Laptop #L-22",
  "category": "Electronics",
  "location": "Eng Block",
  "status":   "online",
  "battery":  87,
  "lat":      11.0168,
  "lng":      76.9558
}
```

**Valid `status` values:** `online` | `alert` | `breach` | `idle`

### `/gateways/{gatewayId}`

```json
{
  "name":     "GW-01 Eng. Block",
  "status":   "online",
  "rssi":     -42,
  "lastPing": "5s ago",
  "zone":     "Eng Block"
}
```

**Valid `status` values:** `online` | `warning` | `offline`

### `/alerts/{alertId}`

```json
{
  "type":         "critical",
  "title":        "Asset left campus",
  "detail":       "MacBook #MB-04 · Admin gate",
  "time":         "2m ago",
  "acknowledged": false
}
```

**Valid `type` values:** `critical` | `warning` | `info`

Only alerts where `acknowledged === false` are shown in the dashboard.

### `/geofences` (schema not yet wired to Firebase)

Geofences are currently hardcoded static data inside `Geofences.jsx`. No Firebase path is consumed. The expected future schema is TBD.

---

## Running Locally

### Prerequisites

- Node.js 18+
- A Firebase project with **Email/Password Authentication** and **Realtime Database** enabled

### Setup

```bash
# 1. Install dependencies
npm install

# 2. Create your environment file
cp .env .env.local
# Then edit .env.local with your real Firebase credentials
```

### Environment Variables

Create `.env.local` (never commit this file — it is in `.gitignore` via `*.local`):

```env
VITE_FIREBASE_API_KEY=your_api_key
VITE_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
VITE_FIREBASE_DATABASE_URL=https://your_project-default-rtdb.firebaseio.com
VITE_FIREBASE_PROJECT_ID=your_project_id
VITE_FIREBASE_STORAGE_BUCKET=your_project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
VITE_FIREBASE_APP_ID=your_app_id
```

### Development Server

```bash
npm run dev
# Opens at http://localhost:5173
```

### Production Build

```bash
npm run build
# Output in dist/
```

### Lint

```bash
npm run lint
```

---

## Switching from Mock to Live Firebase Data

Each hook has a `useMock` parameter (default `true`). To connect a hook to Firebase:

```js
// In the relevant page, change:
const { assets } = useAssets()        // → uses mock data
const { assets } = useAssets(false)   // → reads from Firebase /assets
```

The same pattern applies to `useGateways(false)` and `useAlerts(false)`.

---

## Project Status

| Stage   | Description                                          | Status      |
|---------|------------------------------------------------------|-------------|
| Stage 1 | React/Firebase dashboard — inspection & stabilisation | ✅ Complete |
| Stage 2 | Python simulator producing Firebase-compatible data   | 🔜 Planned  |
| Stage 3 | FastAPI + MQTT ingestion service                      | 🔜 Planned  |
| Stage 4 | ESP32 gateway firmware                                | 🔜 Planned  |
| Stage 5 | Raspberry Pi LoRa hub                                 | 🔜 Planned  |
| Stage 6 | Full end-to-end BLE → dashboard integration           | 🔜 Planned  |

---

## Important Gaps (Known Before Stage 2)

- **Geofence logic is entirely absent.** The frontend has no polygon geometry, no containment check, and no breach detection. This must be implemented in the ingestion layer and reflected in asset `status: "breach"` in Firebase.
- **Reports are fully static.** The incident log is hardcoded. No Firebase path is read or written for reports.
- **Alert acknowledgement is a no-op.** The Acknowledge button has no Firebase write.
- **Heatmap and Floorplan views are stubs.** Only the "Map" tile layer is rendered.
- **No route protection.** The `ProtectedLayout` does not redirect unauthenticated users to `/login`. Auth guard will need to be added before any production deployment.
- **No geofence schema in Firebase.** This must be designed and agreed before Stage 3.
- **`recharts` is installed but unused.** Reserved for future analytics/reporting charts.
