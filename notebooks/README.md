# Notebooks del Proyecto IPA27

Este directorio contiene los notebooks de Jupyter para la gestión, procesamiento y visualización del **Índice de Prosperidad Andaluz**. El sistema está diseñado en un flujo secuencial que transforma datos brutos en indicadores agregados y visualizaciones de alto nivel.

## 🔄 Flujo de Datos

El flujo de trabajo principal sigue esta secuencia:

1.  **Cálculo de Desafección**: `01_1_Índice de desafección_cis_v2.ipynb` procesa microdatos del CIS para generar la serie de desafección regional.
2.  **Extracción Global**: `01_extracción de datos_CCAA_v2.ipynb` descarga datos de APIs (INE, IECA, etc.) y consolida todos los indicadores (incluyendo desafección) en un Excel regional.
3.  **Procesamiento Final**: `02_procesamiento_IPA27.ipynb` aplica el pipeline estadístico (desestacionalización, nowcasting) para generar el índice IPA27 final.

## 📓 Descripción de los Notebooks

### 1. **01_1_Índice de desafección_cis_v2.ipynb**
**Propósito**: Generar el indicador de gobernanza basado en desafección política.
- **Entrada**: Microdatos del CIS en `data/raw/cis/barómetro/`.
- **Salida**: `data/processed/cis/barómetro/indice_desafeccion_ccaa_pivot.csv`.

### 2. **01_extracción de datos_CCAA_v2.ipynb**
**Propósito**: Punto de entrada de datos al sistema con cobertura para 17 CCAA + España.
- **Funcionalidad**:
    - Descarga automática: INE Tempus, IECA, Criminalidad, JAXI.
    - Procesamiento manual: CIS (Sanidad y Elecciones), INE TIC (Banda Ancha), DataInvex.
    - Integra la serie de desafección generada previamente.
- **Salida Principal**: `results/data/ipa27_raw_YYYYMMDD.xlsx`.

### 3. **02_procesamiento_IPA27.ipynb**
**Propósito**: Transformación estadística y cálculo del Índice.
- **Funcionalidad**: Pipeline estadístico completo (STL, Chow-Lin, Nowcasting ARIMA).
- **Salidas**: `results/data/IPA27_agregado.xlsx` y Dashboards de análisis.

### 4. **03_transparencia.ipynb** y **04_gobernanza_senado.ipynb**
Análisis complementarios de transparencia y sentimiento político para alimentar pilares específicos de gobernanza.

---

## 🚀 Cómo ejecutar

1.  Ejecute `01_1_Índice de desafección_cis_v2.ipynb` si necesita actualizar los datos del CIS.
2.  Ejecute `01_extracción de datos_CCAA_v2.ipynb` para consolidar el dataset bruto.
3.  Ejecute `02_procesamiento_IPA27.ipynb` para el cálculo final y visualizaciones.

---
**Última actualización**: 22 de enero de 2026
