# Fast Prompting en Acción: POC — Generador de Briefs de Viaje

Este repositorio contiene una **prueba de concepto (POC)** para aplicar técnicas de **Fast Prompting** en un flujo real de AI de **turismo**: transformar respuestas de un cliente en un **brief ejecutable** con
- Itinerario resumido (7 días),
- Mensaje de cotización para WhatsApp,
- Filtros de búsqueda para HotelDO (ciudades, fechas, presupuesto, distribución, etc.).

> **Problema**: La pre‑venta turística requiere mucho tiempo “manual” para interpretar las necesidades del cliente y redactar primero un brief, luego una cotización y por último un mensaje claro. Esto escala mal y consume recursos.
>
> **Solución (POC)**: Orquestar *prompts rápidos* (FAST) con plantillas y *checks* de validación, evaluando variantes para **mejorar calidad** y **reducir costo** (menos llamadas a la API y menos tokens).

---

## 🧭 Estructura

```
fast-prompting-poc/
├─ README.md
├─ notebooks/
│  └─ fast_prompting_poc.ipynb
├─ src/
│  └─ prompting.py
├─ data/
│  └─ sample_requests.json
└─ LICENSE
```

---

## 🎯 Objetivos

1. **Demostrar** comprensión y uso práctico de **Fast Prompting**.
2. **Experimentar** con configuraciones de *prompts* (plantillas y *self-checks*).
3. **Mostrar** una demo efectiva en **Jupyter Notebook**.
4. **Analizar** si las nuevas técnicas **mejoran** la propuesta planteada en la preentrega 1 (menor costo, más coherencia, menos iteraciones).

---

## 🧪 Metodología (resumen)

- Definimos un **dataset mínimo** (JSON) con requerimientos reales de clientes (ver `data/sample_requests.json`).
- Implementamos 3 variantes:
  - **V0 (baseline)**: prompt directo sin estructura.
  - **V1 (FAST)**: rol + objetivo + restricciones + estilo + *salida en JSON* + checklist.
  - **V2 (FAST+Few‑Shot)**: V1 + 2 ejemplos de alta calidad y *crítica breve* auto‑guiada.
- Ejecutamos y **medimos** (heursticas): cobertura de campos clave, longitud, estimación de tokens y costo.
- **Comparamos** resultados y seleccionamos la mejor configuración.

---

## 🛠️ Herramientas y tecnologías

- Python 3.10+
- Jupyter Notebook
- (Opcional) `openai` o API equivalente. La notebook **detecta** si no hay API key y usa un **modelo *mock*** para la demo.
- Técnicas de prompting: Rol, Objetivo, Restricciones, JSON‑Schema, Few‑Shot, Auto‑checklist, *Guardrails* por regex.

> **Imagen**: Si necesitás generación de imagen (banner del viaje), podés integrar DALLE/Imagen, pero como ya no es gratuito para todos, se deja **opcional** y documentado cómo conectarlo, o usar servicios sin costo como **NightCafe** manualmente.

---

## 🚀 Cómo correr la demo

1. Crear entorno (opcional)
   ```bash
   python -m venv .venv && source .venv/bin/activate  # Linux/Mac
   # en Windows: .venv\Scripts\activate
   ```
2. Instalar dependencias mínimas
   ```bash
   pip install nbformat pandas
   # Opcional si vas a llamar un modelo real:
   pip install openai tiktoken
   ```
3. (Opcional) Exportar tu API key
   ```bash
   export OPENAI_API_KEY="sk-..."
   ```
4. Abrir la notebook: `notebooks/fast_prompting_poc.ipynb` y ejecutar.

---

## 💸 Costos y viabilidad

- La notebook calcula **tokens aproximados** y **costo estimado** por variante.
- Se minimizan llamadas (batch por caso de prueba cuando el proveedor lo permite).
- Se fuerza salida **JSON** para parsear sin re‑intentar, reduciendo *loops*.

---

## 📄 Licencia

MIT — Usar y adaptar libremente citando este repo.
