# Patrón: ROTACIÓN VERTICAL EN PÁGINAS WEB (`.v-rotator`)

Componente reutilizable de una sola fila con **3 posiciones visibles** (izquierda · centro · derecha) y un
"paseo vertical" al cambiar de tarjeta: la que sale se eleva 40 px y se desvanece; la que entra sube desde
40 px por debajo y gana foco al llegar. CSS y JS vanilla, autocontenido en `index.html`; compatible con la CSP
`default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'` (sin CDN, sin `fetch`, sin `innerHTML`).

Implementado en `index.html` (secciones `#ecosistema` y `#proyectos`). Respaldo previo: `index.html.bak_20261114_vrotator`.

## 1. Estructura HTML

```html
<div class="v-rotator" role="group" aria-label="Carrusel de repositorios">
  <button class="v-rotator-btn prev" type="button" aria-label="Anterior">&#8249;</button>
  <div class="v-rotator-stage">
    <div class="box">…</div>      <!-- cada hijo directo del stage es una tarjeta -->
    <div class="box">…</div>
  </div>
  <button class="v-rotator-btn next" type="button" aria-label="Siguiente">&#8250;</button>
</div>
```

- Los hijos directos de `.v-rotator-stage` son las tarjetas; el controlador les añade `.v-rotator-item`.
- El indicador de posición (`1 / 8` + puntos accesibles) lo crea el controlador **debajo** del `.v-rotator`
  (`.v-rotator-meta`).
- Sin JS (o antes de que arranque) el stage se ve como una grilla normal: el CSS del rotador solo se activa con la
  clase `.is-ready`, que añade el controlador.
- Traducción: si la página usa un diccionario de i18n por texto, agrega `Anterior`/`Siguiente` y el `aria-label`
  del grupo. Las etiquetas de los puntos las genera el controlador según `document.documentElement.lang`
  (`es`/`en`; ajusta `L10N` para otros idiomas).

## 2. Contrato CSS

| Clase | Efecto |
|---|---|
| `.v-rotator` | `position: relative; display: flex; align-items: center; justify-content: center; overflow: hidden` |
| `.v-rotator-stage` | Escenario; con `.is-ready` pasa a `position: relative` y su `min-height` lo calcula el controlador (tarjeta más alta + 56 px) |
| `.v-rotator-item` | Tarjeta absoluta centrada (`top/left: 50%`), ancho `--vr-w` |
| `.is-center` | `scale(1)`, `blur(0)`, `opacity 1`, `z-index 3`, borde cian iluminado |
| `.is-left` / `.is-right` | `scale(.60)`, `blur(3.5px)`, `opacity .55`, `z-index 1`, `cursor: pointer` |
| `.is-exit` | Salida: `translateY(-40px)`, `scale(.5)`, `opacity 0` (conserva el `x` de su posición) |
| `.is-offstage` | Fuera de escena: `translateY(40px)`, `opacity 0`, `visibility: hidden` |
| `.no-anim` | Desactiva la transición para recolocar sin animar (uso interno) |
| `.v-rotator-btn.prev/.next` | Botones laterales cian (`border: 1px solid rgba(0,255,255,.4)`, fondo oscuro translúcido, glow en hover/focus) |

Variables (se redefinen en `.v-rotator.is-ready`):

| Variable | Valor | Uso |
|---|---|---|
| `--vr-w` | `min(400px, max(38%, 260px))`; móvil `80%` | Ancho de cada tarjeta |
| `--vr-x` | `92%`; móvil `80%` | Desplazamiento horizontal de las laterales (en % del ancho de la tarjeta) |
| `--vr-ms` / `--vr-ease` | `.65s` / `cubic-bezier(0.22, 1, 0.36, 1)` | Transición |

Cada tarjeta compone `transform: translate(calc(-50% + var(--x)), calc(-50% + var(--y))) scale(var(--s))`,
con `--x/--y/--s/--blur/--op` definidas por la clase de posición. Las reglas usan 4 clases de especificidad para
imponerse a `:hover` del tema de tarjetas.

Responsive (`<= 768px`): tarjeta central al 80 % del ancho a `scale(1)`, laterales a `scale(.60)` + `blur(3px)`
asomando por los bordes, botones de 36 px. `@media (prefers-reduced-motion: reduce)`: sin transiciones ni
desplazamientos verticales, y **sin auto-avance** (solo navegación manual).

## 3. Controlador JS (`VRotator`)

```js
var rot = VRotator(rootElement, {
  getItems: function () { … }     // opcional: subconjunto activo, en orden (por defecto: hijos no `hidden`)
});
rot.refresh();   // recalcula el subconjunto y reinicia en el índice 0 (sin animar)
rot.next(); rot.prev(); rot.goTo(i);
rot.index; rot.size;
```

**Posiciones según el número de tarjetas activas (`n`):**

| `n` | Resultado |
|---|---|
| 0 | Escenario vacío, sin botones ni indicador (la página decide qué mensaje mostrar) |
| 1 | Una tarjeta al 100 % centrada; sin laterales ni flechas |
| 2 | Principal al centro y la otra al 60 % a la derecha; las flechas las alternan |
| ≥ 3 | Izquierda 60 % blur · centro 100 % · derecha 60 % blur, con rotación circular |

**Animación** (generada por cambio de posición, `layout(animate)`): visible→visible mueve por transición; el que
sale (`left` al avanzar) recibe `.is-exit` 650 ms y pasa a `.is-offstage`; el nuevo entra desde `.is-offstage`
(`translateY(40px)`) a su posición. Con `n = 3` la tarjeta que salta de lado a lado sale por arriba y reentra por
abajo en el lado opuesto.

**Interacción:** botones, clic en una tarjeta lateral (la centra sin activar sus enlaces/botones), puntos, flechas
del teclado dentro del rotador y deslizamiento táctil (> 50 px). Las tarjetas no centrales llevan
`aria-hidden="true"` y sus enlaces/botones `tabindex="-1"`.

**Temporización (auto-avance hacia la derecha):**

| Regla | Comportamiento |
|---|---|
| Intervalo adaptable | Escritorio (`> 768px`): **5000 ms**. Móvil (`<= 768px`): **7000 ms**. Se lee con `matchMedia("(max-width: 768px)")` y el temporizador se reinicia si cambia el ancho de ventana. Ya no se usa `data-vr-interval` |
| Reinicio manual | Flechas, puntos, tarjeta lateral, teclado o swipe reinician la cuenta desde cero |
| Hover | Pausa **solo** si el puntero está sobre la tarjeta central (`.is-center`, `pointerover`/`pointerout` delegados en el stage); el vacío y las laterales no pausan; no aplica a punteros táctiles |
| Botón de fijado | `.v-rotator-pin` junto al contador (`type="button"`, `aria-pressed`): `⏸ Fijar` / `▶ Auto` (ES) y `⏸ Pin` / `▶ Auto` (EN). Fijado detiene el ciclo hasta pulsarlo de nuevo |
| Táctil / teclado | Pausa mientras el dedo toca la tarjeta central (`touchstart`/`touchend`/`touchcancel`) y mientras hay foco de teclado dentro del rotador (`focusin` con `:focus-visible` / `focusout`) |
| Modales | Con `#projectModal` o `#skillsModal` abiertos (`.open` / `aria-hidden="false"`) el rotador queda 100 % estático; al cerrarse el ciclo se reanuda desde cero (salvo que esté fijado) |
| Pestaña / pantalla | Pausa con `document.hidden` (`visibilitychange`) y cuando el rotador no está en pantalla (`IntersectionObserver`) |
| Movimiento reducido | Con `prefers-reduced-motion: reduce` no hay auto-avance, ni botón de fijado; solo navegación manual |

Al salir de cualquier pausa (`sync()`), el temporizador se reinicia, así que nunca hay un salto inmediato al reanudar.

## 4. Integración con filtros (`#proyectos`)

El filtro existente marca `card.hidden`; el rotador solo debe recalcular su subconjunto después de cada filtro:

```js
var projRot = VRotator(projRoot, {
  getItems: function () { return [].filter.call(projRoot.querySelectorAll(".project-card"), function (c) { return !c.hidden; }); }
});
document.querySelectorAll(".filter-btn").forEach(function (b) {
  b.addEventListener("click", function () { projRot.refresh(); });   // registrar DESPUÉS del handler del filtro
});
```

## 5. Reutilizar en otro proyecto

1. Copiar el bloque CSS `ROTACIÓN VERTICAL EN PÁGINAS WEB (.v-rotator)` y la función `VRotator` (script al final del `<body>`).
2. Envolver las tarjetas en `.v-rotator > .v-rotator-stage` con los dos botones.
3. Llamar `VRotator(el)` (y, si hay filtros, `refresh()` tras cada uno).
4. Asegurarse de que las tarjetas tengan fondo propio (el desenfoque y la opacidad se aplican a la tarjeta completa).

## 6. Notas de verificación

- Probado con 8, 4, 3, 2, 1 y 0 tarjetas activas; botones, puntos, clic lateral, teclado y filtros.
- Intervalos medidos en local: ~5,1 s (1280 px) y ~7,1 s (491 px); hover central, fijado y modal abierto detienen el ciclo.
- `prefers-reduced-motion` se respeta en CSS y en JS (`matchMedia` se consulta en cada acción).
- Un panel de navegador oculto congela el reloj de animaciones CSS: para medir la animación hay que tener la
  pestaña visible.
