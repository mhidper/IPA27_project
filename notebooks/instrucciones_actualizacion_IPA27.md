# Guía de Actualización de Fuentes Estadísticas - IPA27

Este documento detalla el procedimiento para actualizar todos los indicadores del **Índice de Prosperidad Andaluz (IPA27)**. El sistema combina captadores automáticos mediante APIs y procesamiento manual de microdatos o archivos externos.

## 📊 Resumen de Fuentes por Método de Actualización

| Método | Tipo | Fuentes Principales | Esfuerzo |
| :--- | :--- | :--- | :--- |
| **Automático** | API / Scraping | INE (Tempus/JAXI), IECA, Min. Interior (Criminalidad) | Bajo (Ejecutar Notebook) |
| **Manual** | Descarga Web | CIS Barómetro, SS Afiliados, CGPJ Corrupción, DataInvex | Medio (Descarga + Ejecución) |
| **Local** | Archivo Excel | INE Renta Hogares | Bajo (Actualizar fichero) |

---

## 🚀 Paso 1: Actualización Automática
La mayoría de los indicadores se actualizan automáticamente conectando con las APIs oficiales.

1.  Abre el notebook `01_extraccion_datos_CCAA.ipynb`.
2.  Ejecuta la **Celda 0** (Configuración) y **Celda 4** (Motor de descarga).
3.  Llama a la función `descargar_todos()` para actualizar los siguientes indicadores:
    *   **INE (Tempus/JAXI)**: Hipotecas, Sociedades, Transporte, AROPE, Paro, Educación, I+D.
    *   **IECA**: PIB Trimestral de Andalucía (Auxiliar).
    *   **Ministerio del Interior**: Balances de Criminalidad (Tasa total, Hurtos/Robos, Libertad Sexual).
    *   **Red Eléctrica (REE)**: Generación Renovable (mediante notebook `03_scraping_REE_renovables.ipynb`).

---

## 📥 Paso 2: Actualización Manual (Requiere Acción Previa)
Para estos indicadores, debes descargar los datos brutos antes de ejecutar el procesamiento.

### A. Microdatos del CIS (Desafección y Participación)
1.  **Descarga**: Visita el [Portal del CIS](https://www.cis.es/) y descarga el último barómetro mensual (Microdatos en formato CSV o SAV).
2.  **Ubicación**: Guarda el archivo en `data/raw/cis/barómetro/`.
3.  **Procesamiento**:
    *   Ejecuta `01_1_indice_desafeccion_cis.ipynb` para generar la serie de desafección (`GOB_DES`).
    *   Ejecuta `01_2_participacion_electoral_cis.ipynb` para actualizar la probabilidad de voto.

### B. Estadísticas de Seguridad Social (Asociacionismo y Conocimiento)
1.  **Descarga**: Ve al portal de estadísticas de la Seguridad Social (Series de Afiliación por CNAE a 2 dígitos).
2.  **Extracción**: Descarga los datos de afiliados para las secciones **S (94)** para Asociacionismo (`SOC_ASO`) y **J + M** para Conocimiento Intensivo (`CON_OCI`).
3.  **Ubicación**: Actualiza el archivo `data/raw/other/ss_afiliados.csv`.

### C. Otros Archivos Externos
| Indicador | Fuente | Web de Descarga | Fichero Destino |
| :--- | :--- | :--- | :--- |
| **LIB_ODI** | Min. Interior | [Delitos de Odio](https://oficinanacional-delitosdeodio.ses.mir.es/publico/ONDOD/publicaciones.html) | `data/raw/other/mir_odio.xls` |
| **GOB_COR / EFF** | CGPJ | [Corrupción Judicial](https://www.poderjudicial.es/cgpj/es/Temas/Estadistica-Judicial/Estadistica-Judicial-Anual/Estadistica-Judicial-Anual/Estadistica-de-la-Corrupcion/) | `data/raw/other/mir_corrupcion.xls` |
| **INV_IED** | DataInvex | [Inversión Extranjera](https://datainvex.comercio.es/principal_invex.aspx) | `data/raw/other/consulta_datainvex.xls` |
| **INF_BAN** | INE | [TIC en Hogares](https://www.ine.es/) | `data/raw/tic_hogares/` (microdatos .tab) |
| **AUX_EDA** | INE | [Padrón Municipal](https://www.ine.es/) | `data/raw/other/edad_media.csv` |
| **ECO_RBH** | INE | [Renta de los Hogares](https://www.ine.es/) | `data/raw/renta_ine/rentahogd25.xlsx` |
| **SOC_ASO / CON_OCI** | Seg. Social | [Estadísticas SS](https://www.seg-social.es/) | `data/raw/other/ss_afiliados.csv` |

---

## 🛠️ Paso 3: Consolidación y Procesamiento Final
Una vez actualizadas todas las fuentes (automáticas y manuales):

1.  **Consolidar**: En `01_extraccion_datos_CCAA.ipynb`, ejecuta la última celda para generar el fichero `results/data/ipa27_raw_YYYYMMDD.xlsx`.
2.  **Calcular Índice**: Abre `02_procesamiento_IPA27_CCAA.ipynb` y ejecútalo íntegramente. Este notebook realiza:
    *   Desestacionalización de series.
    *   Nowcasting (predicción de los últimos meses).
    *   Agregación por pilares y dominios.
    *   Generación de los gráficos finales del Dashboard.

---

## 📌 Checklist de Verificación
- [ ] ¿Se han descargado los últimos archivos del CIS y Seguridad Social?
- [ ] ¿Se ha ejecutado `01_1_indice_desafeccion_cis.ipynb`?
- [ ] ¿El reporte de `descargar_todos()` muestra éxito en los conectores del INE?
- [ ] ¿Se ha generado el archivo `.xlsx` en `results/data/` con la fecha de hoy?
