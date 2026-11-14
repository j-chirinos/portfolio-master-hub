# Portfolio Master Hub

Portafolio central de **Senior Data Analyst & Process Automation Lead** (JW-Solutions). Reúne en una sola landing page la trayectoria en banca y seguros, las métricas de impacto y el ecosistema de repositorios open source.

## Propósito

- Presentar de forma ejecutiva los hitos profesionales: BI, SSoT, ETL y automatización de procesos.
- Servir de puerta de entrada a los repositorios técnicos del ecosistema.
- Demostrar resultados medibles, no solo herramientas.

## Contenido

| Sección | Descripción |
|---|---|
| Métricas de Impacto Global | ROI operativo, reducción de errores y automatización de procesos |
| Proyectos y Trayectoria | Tarjetas `project-card` con filtros interactivos por sector y tipo de solución |
| Ecosistema de Repositorios | `segubot-ocr-agent`, `v15-sports-predictor`, `ssot-data-normalizer` |

## Hitos documentados

- **Banesco Seguros Panamá:** Tableros de Gestión Comercial y Automatización de Referimientos.
- **Mercantil Seguros:** Tablero Comercial de Cotizaciones con actualización automática.
- **Banesco Banco Universal:** −95% en reclamaciones rechazadas mediante SSoT y modelos de datos.
- **Consultoría Freelance:** ETL de siniestralidad en Python/Excel, segmentación a demanda y monitoreo de tasas con IA Generativa.

## Stack y diseño

- HTML5 + CSS3 + JavaScript vanilla; sin dependencias ni CDN externos.
- Paleta: fondo `#0f172a`, tarjetas `#1e293b`, acentos `#38bdf8` y `#4ade80`.
- Seguridad: Content-Security-Policy restrictiva por `<meta>`, sin `innerHTML` ni recursos de terceros.
- Accesibilidad: filtros con `aria-pressed`, foco visible, `prefers-reduced-motion`, diseño responsivo.

## Vista previa local

```powershell
cd portfolio-master-hub
python -m http.server 8080
```

Abrir <http://localhost:8080>. También funciona abriendo `index.html` directamente.

## Pendiente

- Completar las métricas de ROI operativo con cifras reales verificadas por el autor (hoy se muestran de forma cualitativa).

## Idioma (ES / EN)

Selector ES/EN en la barra de navegación. El HTML queda en español (respaldo sin JS) y el inglés se aplica con JavaScript vanilla por coincidencia exacta de texto. Orden de preferencia: `?lang=en|es` en la URL, luego la última elección (localStorage) y, por defecto, el idioma del navegador (inglés si no es español).

---

## English

Central portfolio of a **Senior Data Analyst & Process Automation Lead** (JW-Solutions): a single landing page with banking/insurance experience, impact metrics and the open-source repository ecosystem.

- **Content:** impact metrics, filterable project cards (by sector and solution type), and the repository ecosystem.
- **Stack:** HTML5 + CSS3 + vanilla JavaScript; no dependencies or external CDNs.
- **Security:** restrictive Content-Security-Policy via `<meta>`, no `innerHTML`, no third-party resources.
- **Accessibility:** `aria-pressed` filters, visible focus, `prefers-reduced-motion`, responsive layout.
- **Run locally:** `python -m http.server 8080` inside the folder, then open <http://localhost:8080> (or open `index.html` directly).
- **Language:** ES/EN toggle in the top bar (vanilla JS, no dependencies). Preference order: `?lang=en|es` URL parameter, last choice (localStorage), then browser language (English unless Spanish).
- **Pending:** replace qualitative ROI metrics with author-verified figures.
