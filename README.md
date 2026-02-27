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

## Estructura del Proyecto

El repositorio del proyecto sigue una estructura limpia y optimizada para la separación de responsabilidades e investigación analítica:

```text
IPA27_project/
├── data/                        # Datos brutos y preprocesados (bases trimestrales y anuales)
├── docs/                        # Documentación complementaria, convenios e infografías
├── metodologia/                 # Documentos metodológicos, papers y ficheros LaTeX core:
│   └── metodologia_ipa27_actualizada.tex  # Documento técnico principal
├── notebooks/                   # Jupyter Notebooks principales de ejecución:
│   ├── 01_extraccion_datos_CCAA.ipynb
│   ├── 01_1_indice_desafeccion_cis.ipynb
│   ├── 01_2_participacion_electoral_cis.ipynb
│   ├── 02_procesamiento_IPA27_CCAA.ipynb
│   └── 03_scraping_REE_renovables.ipynb
├── results/                     # Resultados estadísticos:
│   ├── data/                    # Exportaciones CSV (techos, contribución y agregaciones)
│   └── figures/                 # Outputs gráficos y de reporting del pipeline
├── src/                         # Módulos Python fuente reutilizables:
│   ├── config.py                
│   ├── extractors.py            
│   ├── consolidator.py          
│   └── connectors.py            
├── README.md                    # Este archivo
└── requirements.txt             # Dependencias del entorno
```

## Instalación

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Dependencias Principales

- **pandas**: Manipulación de datos
- **numpy**: Operaciones numéricas
- **statsmodels**: Modelos estadísticos (ARIMA, desestacionalización STL)
- **matplotlib, seaborn**: Visualización
- **requests**: Peticiones HTTP a APIs

## Uso del Pipeline

### 1. Extracción de Datos (`01_extraccion_datos_CCAA.ipynb`)

Los datos se rescatan automáticamente desde las siguientes plataformas gubernamentales y privadas utilizando APIs y Scraping:
- **INE (Instituto Nacional de Estadística)**
- **IECA (Instituto de Estadística y Cartografía de Andalucía)**
- **Ministerio del Interior (Portal Estadístico de Criminalidad)**
- **Red Eléctrica de España**
- **CIS (Centro de Investigaciones Sociológicas)**

### 2. Procesamiento Metodológico (`02_procesamiento_IPA27_CCAA.ipynb`)

El procesamiento integral sigue estas fases:
1. **Desacumulación**: Series acumuladas anuales se tornan trimestrales absolutas.
2. **Desestacionalización (STL)**: Depuración de patrones estacionales que ensucian la economía y lo criminal.
3. **Trimestralización**: Agregaciones directas, modelos de interpolación por regresores de Chow-Lin y Denton.
4. **Nowcasting (ARIMA)**: Rellenado de ausencias (lags) de reporte público.
5. **Cálculo de Techos Fijos y Normalización**: Adaptación de los valores al baremo `0-120`.
6. **Agregación Geométrica**: Compresión a medias de equidad restrictiva (Pilares, Dominios, IPA27 Total).
7. **Análisis de Elasticidades Absolutas**: Reportes sobre dominios que obran como cuellos de botella mediante control de desequilibrios por varianza y deltas.

### 3. Ejecución de Entornos Relacionales

La compilación y visualización del índice de desafección, electorabilidad y scraping del clúster renovable, ocurre a través de los cuadernos de soporte correspondientes situados de igual manera en `notebooks/`.

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

## Documentación

La teoría que respalda la modernización del procesamiento de techos y cálculos matriciales se discute íntegramente en la carpeta `metodologia/`, junto a los reportes subversivos de las dimensiones de afección política. El fichero técnico madre del proyecto se puede compilar al abrir `metodologia/metodologia_ipa27_actualizada.tex`. 

## Licencia & Contacto

MIT License - Ver archivo fuente de metadatos.

**Equipo IPA27**
Instituto de Estudios Regionales, Sevilla, España
Email: ipa27@andalucia.es

**Última actualización**: Febrero 2026
**Versión del Índice**: IPA27 (Techos Fijos / Media Geométrica)
