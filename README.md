# Índice de Prosperidad Andaluz (IPA27)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## Descripción

El **Índice de Prosperidad Andaluz (IPA27)** es un sistema de medición multidimensional del bienestar regional diseñado para el seguimiento trimestral de la prosperidad en Andalucía en comparación con España. Adaptando el marco conceptual del Legatum Prosperity Index a la realidad estadística y política de una región europea, el proyecto busca proveer un análisis métrico sólido.

### Estructura del Índice

El IPA27 se compone de:
- **3 Dominios**: Sociedades Inclusivas, Economías Abiertas, Personas Empoderadas
- **12 Pilares**: 4 pilares por dominio
- **24 Indicadores**: 2 indicadores por pilar

### Innovaciones Metodológicas (Actualización 2026)

1. **Nowcasting integrado**: Pipeline automatizado que combina métodos de Chow-Lin, splines de Denton y modelos ARIMA para unificar series de frecuencias mixtas (mensual, trimestral, anual).
2. **Normalización por Techos Fijos**: Función de transformación anclada en topes estructurales (calculados a partir del promedio del top 3 de los mejores rendimientos históricos y márgenes de proyección). Penaliza la falta de rendimientos y admite elasticidad superior con techos controlados hasta una puntuación de clímax de 120.
3. **Agregación por Media Geométrica Robusta**: A todos los niveles (indicadores a pilares, pilares a dominios y dominios a índice general) se usa una agregación mediante interpolación geométrica de potencias con acotaciones, penalizando la inequidad formativa (no poder compensar falencias graves en un pilar con saltos inmensos en otro).

---

## Estructura del Proyecto

El repositorio del proyecto sigue una estructura limpia y consolidada para la separación de responsabilidades:

```text
IPA27_project/
├── dashboard/                   # Cuadro de mando interactivo web (Vite + React)
│   ├── public/data/             # dashboard_data.json y series de datos para la web
│   └── src/                     # Código fuente de la interfaz de usuario
├── data/                        # Datos históricos y procesados del modelo
│   ├── raw/                     # Datos fuente (archivos de criminalidad, renta, etc.)
│   │   └── archive/             # Histórico de Excel consolidados archivados
│   └── processed/               # Resultados intermedios e indicadores preprocesados
├── docs/                        # Documentación complementaria, convenios e infografías
├── metodologia/                 # Documentos metodológicos y ficheros LaTeX core:
│   ├── 01_IPA27_General/        # Presentación Beamer y variables del modelo:
│   │   ├── presentacion_ipa27_v5.tex  # Código de la presentación Beamer
│   │   ├── ipa27_variables.tex        # Macros numéricas actualizadas por el notebook
│   │   └── ideas_fuerza_resultados.md # 6 mensajes clave para la venta de resultados
│   ├── 02_Indice_Desafeccion/   # Documentación del índice de desafección política
│   └── 03_Participacion_Electoral/ # Estudios de participación electoral
├── notebooks/                   # Jupyter Notebooks de ejecución (libres de carpetas data/results locales):
│   ├── 01_extraccion_datos_CCAA.ipynb       # Descarga e integración de APIs y scraping
│   ├── 01_1_indice_desafeccion_cis.ipynb    # Generación del indicador de desafección (CIS)
│   ├── 01_2_participacion_electoral_cis.ipynb # Procesamiento de microdatos electorales
│   ├── 02_procesamiento_IPA27_CCAA.ipynb    # Pipeline metodológico, ARIMA y compilación
│   └── 03_scraping_REE_renovables.ipynb     # Scraping de generación de energías renovables
├── results/                     # Resultados estadísticos y visuales del proyecto:
│   ├── data/                    # Exportaciones de series y coeficientes en Excel
│   │   └── archive/             # Versiones históricas de ficheros consolidados ipa27_raw
│   └── figures/                 # Outputs gráficos y de diagnóstico (reporting y dashboards)
├── src/                         # Módulos Python reutilizables (conectores y extractores):
│   ├── config.py                
│   ├── extractors.py            
│   ├── consolidator.py          
│   └── connectors.py            
├── README.md                    # Este archivo
└── requirements.txt             # Dependencias del entorno de Python
```

---

## Instalación y Configuración

### Requisitos Previos
- Python 3.8 o superior
- Node.js & npm (para ejecutar el dashboard localmente)

### Instalar Dependencias de Python
```bash
pip install -r requirements.txt
```

### Configurar e Iniciar el Dashboard Web
1. Dirígete a la carpeta del dashboard:
   ```bash
   cd dashboard
   ```
2. Instala las dependencias de Node:
   ```bash
   npm install
   ```
3. Lanza el servidor de desarrollo:
   ```bash
   npm run dev
   ```

---

## Uso del Pipeline

### 1. Extracción de Datos (`01_extraccion_datos_CCAA.ipynb`)
Los datos se rescatan automáticamente desde las siguientes plataformas gubernamentales y privadas utilizando APIs y Scraping:
- **INE (Instituto Nacional de Estadística)**
- **IECA (Instituto de Estadística y Cartografía de Andalucía)**
- **Ministerio del Interior (Portal Estadístico de Criminalidad)**
- **Red Eléctrica de España**
- **CIS (Centro de Investigaciones Sociológicas)**

El output consolidado se guarda automáticamente como `results/data/ipa27_raw_YYYYMMDD.xlsx`.

### 2. Procesamiento Metodológico (`02_procesamiento_IPA27_CCAA.ipynb`)
El procesamiento principal sigue las siguientes fases lógicas:
1. **Desestacionalización (STL)**: Depuración de patrones estacionales que ensucian las series de frecuencia mensual o trimestral.
2. **Trimestralización**: Modelos de interpolación por regresores de Chow-Lin y Denton para homogeneizar series de frecuencia mixta (anuales/mensuales).
3. **Nowcasting (ARIMA)**: Rellenado predictivo de retardos de reporte público para el trimestre de cierre actual.
4. **Normalización por Techos Fijos**: Ajuste de los valores al baremo estándar `0-120`.
5. **Agregación Geométrica**: Cálculo del índice de los Pilares, Dominios e IPA27 General mediante medias geométricas.
6. **Exportación de Datos y LaTeX**:
   - Genera y actualiza `dashboard/public/data/dashboard_data.json` para alimentar la interfaz React.
   - Genera y escribe el archivo macro de LaTeX `metodologia/01_IPA27_General/ipa27_variables.tex` y compila la presentación `presentacion_ipa27_v5.tex` a PDF de manera automática.

---

## Indicadores del IPA27

### Dominio 1: Sociedades Inclusivas
- **Pilar 1: Seguridad** (Tasa de Criminalidad Total, Balance de Hurtos y Robos)
- **Pilar 2: Libertad** (Delitos de Odio, Delitos de Libertad Sexual)
- **Pilar 3: Gobernanza** (Índice de Transparencia, Confianza en Gobierno)
- **Pilar 4: Capital Social** (Participación Electoral, Actividad Asociativa)

### Dominio 2: Economías Abiertas
- **Pilar 5: Inversión** (IED, Hipotecas sobre Fincas Urbanas)
- **Pilar 6: Empresas** (Natalidad Empresarial, Constitución Sociedades Mercantiles)
- **Pilar 7: Infraestructura** (Banda Ancha, Transporte de Viajeros)
- **Pilar 8: Calidad Económica** (PIB Trimestral, PIB per Cápita proxy de Rentas Brutas)

### Dominio 3: Personas Empoderadas
- **Pilar 9: Vida** (Tasa AROPE, Tasa de Paro EPA)
- **Pilar 10: Salud** (Esperanza de Vida, Satisfacción Sistema Sanitario)
- **Pilar 11: Educación** (Abandono Escolar Temprano, Educación Superior)
- **Pilar 12: Conocimiento** (Gasto I+D % PIB, Ocupaciones en Sectores de Conocimiento)

---

## Licencia & Actualización

**Última actualización**: Junio 2026 (Datos de cierre hasta **2026Q1**)  
**Versión del Índice**: IPA27 (Techos Fijos / Media Geométrica)
