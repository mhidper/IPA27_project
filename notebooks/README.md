# Notebooks del Proyecto IPA27

Este directorio contiene los notebooks de Jupyter para la extracción, procesamiento estadístico, modelación y exportación de resultados del **Índice de Prosperidad Andaluz**. El pipeline se ha modularizado para mejorar la escalabilidad y facilitar el mantenimiento del código.

## 🔄 Flujo de Trabajo y Ejecución Secuencial

Para realizar una actualización completa de resultados, ejecute los notebooks en el siguiente orden:

1.  **Fase 1: Preparativos de Indicadores del CIS**
    *   `01_1_indice_desafeccion_cis.ipynb`: Procesa microdatos del CIS para generar el indicador de desconfianza política (`GOB_DES`).
    *   `01_2_participacion_electoral_cis.ipynb`: Procesa microdatos del CIS para el pilar de Capital Social (`SOC_PAR`).
2.  **Fase 2: Extracción Global y Consolidación**
    *   `01_extraccion_datos_CCAA.ipynb`: Conecta con APIs oficiales (INE, IECA), realiza web scraping y consolida el dataset bruto, generando el archivo Excel consolidado de salida (`results/data/ipa27_raw_YYYYMMDD.xlsx`).
3.  **Fase 3: Pipeline Estadístico y Modelación**
    *   `02_1_procesamiento.ipynb`: Carga y prepara las series temporales por frecuencias, realiza imputaciones de datos, calcula variables de escala y exporta los ficheros CSV preparados. Genera el registro inicial de trazabilidad (`AUDIT_REGISTRY`).
    *   `02_2_modelacion.ipynb`: Aplica desestacionalización STL, trimestralización Chow-Lin/Denton y extensiones ARIMA para nowcasting en el trimestre de cierre actual.
    *   `02_3_exportacion.ipynb`: Calcula los techos objetivos, normaliza los indicadores en el baremo de score (0-100), calcula las agregaciones jerárquicas del índice y exporta:
        *   Los datos del Cuadro de mando (`dashboard_data.json`).
        *   Las Fichas de Auditoría analíticas de trazabilidad en formato PDF (`docs/metodologia/01_general/`).
        *   El archivo macro LaTeX (`ipa27_variables.tex`) y compila la presentación de resultados Beamer (`presentacion_ipa27_v5.tex`).

## 📓 Notebooks Auxiliares y Adicionales

*   `03_scraping_REE_renovables.ipynb`: Capturador de datos históricos de generación renovable de Red Eléctrica de España.
*   `03_playground_edad_media.ipynb`: Entorno de pruebas para la interpolación de edades medias a nivel municipal y regional.
*   `02_procesamiento_IPA27_CCAA.ipynb`: Versión histórica unificada original (mantenida únicamente como referencia histórica).

---
**Última actualización**: Junio 2026
