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

### B. Afiliados Seguridad Social (CON_OCI / SOC_ASO)
1.  **Descarga**: Ve al portal de estadísticas de la Seguridad Social (Series de Afiliación por CNAE a 2 dígitos). [Enlace a Estadísticas SS](https://www.seg-social.es/wps/portal/wss/internet/EstadisticasPresupuestosEstudios/Estadisticas/EST8/EST10/EST305/c43ad8ea-fe79-4329-ac8e-e5758f3c4d7a/f83fe4aa-2dee-49c5-8317-98d105813796)
2.  **Extracción**: Descarga los datos de afiliados para las secciones **S (94)** para Asociacionismo (`SOC_ASO`) y **J + M** para Conocimiento Intensivo (`CON_OCI`).
3.  **Ubicación**: Actualiza el archivo `data/raw/other/ss_afiliados ccaas.csv`.
4.  **Nota Técnica (CNAE-2025)**: En enero de 2026 se ha cambiado a la clasificación **CNAE-2025**. Los datos de enero 2026 a abril 2026 son los extraídos directamente de la web de la Seguridad Social. Para los datos anteriores, se ha realizado un enlace de series aplicando un crecimiento del **0,2% mensual** entre diciembre de 2025 y enero de 2026 de forma uniforme para todos los sectores.

### C. Inversión Extranjera (INV_IED)
1.  **Portal**: [DataInvex - Inversión Extranjera](https://datainvex.comercio.es/principal_invex.aspx)
2.  **Criterios de Selección**:
    *   **Operaciones**: "OPERACIONES NO ETVE" en "Flujos Inversión Bruta en miles de euros".
    *   **Sector**: Todos los sectores.
    *   **País Último / Inmediato**: Todos los países.
    *   **Periodo**: Seleccionar todos los trimestres desde el 1º TRIMESTRE 2016 hasta el más reciente disponible (ej. 2025 o 2026).
    *   **Comunidad Autónoma**: Seleccionar "Todas las comunidades" y cada una de las 17 CCAAs + Ceuta y Melilla individualmente.
    *   **Tipo de Inversión**: Inversión Total (Capital+Financiación).
3.  **Ubicación**: Guardar como `data/raw/other/consulta_datainvex_ccaa.xls`.

### D. Otros Archivos Externos
| Indicador | Fuente | Web de Descarga | Fichero Destino |
| :--- | :--- | :--- | :--- |
| **LIB_ODI** | Min. Interior | [Delitos de Odio](https://oficinanacional-delitosdeodio.ses.mir.es/publico/ONDOD/publicaciones.html) | `data/raw/other/mir_odio CCAA.xls` Se toma el primero de los desplegables Descarga ficheros Informacion tabla Hechos conocidos por causa de delitos de odio desglosado por tipo hecho|
| **GOB_COR / EFF** | CGPJ | Scraper Automático | Ejecutar `scrape_cgpj_corruption.py` (Genera `data/raw/cgpj_corrupcion_procesado.csv`) |
| **INV_IED** | DataInvex | [Inversión Extranjera](https://datainvex.comercio.es/principal_invex.aspx) | `data/raw/other/consulta_datainvex_ccaa.xls` |
| **INF_BAN** | INE | [TIC en Hogares](https://www.ine.es/) | `data/raw/tic_hogares/` (microdatos .tab) |
| **AUX_EDA** | INE | [Padrón Municipal](https://www.ine.es/) | `data/raw/other/edad_media.csv` |
| **ECO_RBH** | INE | [Renta de los Hogares](https://www.ine.es/) | `data/raw/renta_ine/rentahogd25.xlsx` |

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
