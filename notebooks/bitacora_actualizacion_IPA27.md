# 📓 Bitácora de Trazabilidad, Depuración y Limpieza del Pipeline IPA27

Este documento constituye el **registro vivo de trazabilidad y gobernanza del proyecto IPA27**. Su objetivo es registrar los archivos (notebooks, datasets, scripts) activamente utilizados en la pipeline de actualización, así como catalogar aquellos elementos **obsoletos, zombis o superfluos** identificados para su depuración o aislamiento.

---

## 🧟 1. Inventario de Elementos "Zombis" / Innecesarios / Obsoletos

Esta sección cataloga los recursos que **NO son consumidos por el modelo final del IPA27** o cuya lógica ha sido reemplazada por pipelines más eficientes.

| Recurso / Fichero | Tipo | Diagnóstico de Inactividad | Acción Recomendada |
| :--- | :--- | :--- | :--- |
| **`01_2_participacion_electoral_cis.ipynb`** | Notebook | Genera las series `serie_participacion_ccaa.csv` y `serie_participacion_espana.csv` a partir del CIS. En `01_extraccion_datos_CCAA.ipynb`, el código prioriza los datos reales del Ministerio del Interior (`PARTICIPACION_OFICIAL`) mediante `drop_duplicates`, descartando los datos del CIS. | **Marcar como Zombi / Opcional**. El IPA27 oficial utiliza `SOC_PAR_enlazado` derivado del Min. Interior + Chow-Lin/ARIMA. |
| **Variable `SOC_PAR` (bruta)** | Pestaña / Variable | En `02_1_procesamiento.ipynb` (celda `zombies`), se incluye explícitamente `SOC_PAR` en la lista `['GOB_COR', 'GOB_TRA', 'SAL_SAT', 'SOC_PAR']` y se elimina del sistema. | **Inactiva**. Solo se utiliza la versión `SOC_PAR_enlazado`. |
| **`02_procesamiento_IPA27_CCAA.ipynb`** | Notebook | Versión histórica unificada original anterior a la modularización en `02_1`, `02_2` y `02_3`. | **Archivado / Histórico**. No ejecutar en actualizaciones de producción. |
| **`03_playground_edad_media.ipynb`** | Notebook | Entorno de pruebas temporal para la interpolación municipal/regional de la edad media. | **Playground / Scratch**. No forma parte de la cadena crítica de producción. |

---

## 🛠️ 2. Arquitectura de la Pipeline Crítica (Elementos Activos)

### 🤖 Paso 1: Microdatos del CIS (Desafección Política)
- **Agente / Skill**: `agente_paso1_cis` (`.agents/skills/agente_paso1_cis/`)
- **Script**: `procesar_cis_incremental.py`
- **Output Principal**: `data/processed/cis/barómetro/indice_desafeccion_ccaa_pivot.csv`
- **Indicador Consumido**: `GOB_DES` (Índice de Desafección Política, 60% Menciones ajustadas + 40% Anclajes).

### 🌐 Paso 2: Portales Oficiales y Excel Consolidado Raw
- **Notebook**: `01_extraccion_datos_CCAA.ipynb`
- **Fuentes**: INE APIs (Tempus/JAXI), IECA, Ministerio del Interior (Criminalidad y Elecciones Generales), SS (Afiliados), DataInvex, CGPJ.
- **Output Principal**: `results/data/ipa27_raw_YYYYMMDD.xlsx`
- **Constante Crítica**: `PARTICIPACION_OFICIAL` (datos reales de Elecciones Generales 2016, 2019, 2023) para construir `SOC_PAR_enlazado`.

### 📊 Paso 3: Pipeline Estadístico y Modelación
1. **`02_1_procesamiento.ipynb`**:
   - Carga `ipa27_raw_YYYYMMDD.xlsx`.
   - Clasifica indicadores por frecuencia (Mensual, Trimestral, Anual).
   - Ejecuta filtro de seguridad contra variables zombis (`GOB_COR`, `GOB_TRA`, `SAL_SAT`, `SOC_PAR`).
   - Imputa fallbacks regionales si es necesario.
2. **`02_2_modelacion.ipynb`**:
   - Trimestralización (Chow-Lin / Denton spline) relacionando series anuales (ej. `SOC_PAR_enlazado`) con series de frecuencia superior (ej. `EMP_SOC`).
   - Extensiones ARIMA Nowcasting hasta el trimestre de cierre actual (ej. `2026Q1` / `2026Q2`).
3. **`02_3_exportacion_geometricas.ipynb`**:
   - Normalización 0-100 con techos y suelos robustos.
   - Agregación jerárquica por pilares y dimensiones del IPA27.
   - Exportación de `results/data/dashboard_data.json`, fichas PDF y macros Beamer/LaTeX.

---

## 📋 3. Registro de Cambios y Revisiones de la Bitácora

| Fecha | Autor | Modificación / Hito | Impacto |
| :--- | :--- | :--- | :--- |
| **2026-08-06** | Antigravity / Manuel | Creación inicial de la bitácora de trazabilidad. Diagnóstico de `01_2_participacion_electoral_cis.ipynb` y `SOC_PAR` como elementos Zombis. | Clarificación de la pipeline oficial y simplificación de dependencias. |
| **2026-08-06** | Antigravity / Manuel | Ejecución con éxito del Paso 2 (`01_extraccion_datos_CCAA.ipynb`). Generación del consolidado `results/data/ipa27_raw_20260806.xlsx`. | 10 indicadores actualizados vía API (INE/IECA). 24 indicadores manuales 100% inalterados y preservados. |
| **2026-08-20** | Antigravity / Manuel | Ejecución del Paso 2 (`01_extraccion_datos_CCAA.ipynb`) tras la incorporación manual de datos de la Seguridad Social (`SOC_ASO` y `CON_OCI`). Generación de `results/data/ipa27_raw_20260820.xlsx`. | Extensión de `SOC_ASO` y `CON_OCI` a 2026-M07. Descarga automática de APIs INE/IECA (IPC a 2026-M07, EPA a Q2, etc.). 22 indicadores manuales 100% inalterados. |
