# Documentación del Proyecto IPA27

Este directorio contiene toda la documentación metodológica, técnica y contractual del Índice de Prosperidad Andaluz.

## Estructura

```
docs/
├── methodology/                # Documentación metodológica
│   ├── methodology.tex         # Artículo LaTeX principal
│   ├── methodology.pdf         # PDF compilado del artículo
│   ├── notes/                  # Notas de trabajo
│   ├── 01_benchmark_analysis.pdf
│   ├── 02_governance_indicators.docx
│   ├── 03_normalization_methods.docx
│   ├── 04_technical_documentation.pdf
│   ├── 05_architecture.pdf
│   └── indicators_sources.xlsx
│
├── agreements/                 # Convenios y contratos
│   ├── contract_draft_v0.doc
│   ├── proposed_agreement.docx
│   └── technical_report.docx
│
└── infographics/               # Infografías
    └── indicators_infographic.png
```

---

## Documentos Metodológicos

### 📄 **methodology.pdf** (Documento Principal)
**Título**: *Arquitectura del Índice de Prosperidad Andaluz (IPA27): Un Enfoque Metodológico Basado en Normalización Sigmoide Robusta y Agregación Jerárquica para la Medición Multidimensional del Bienestar Regional*

**Destino**: Social Indicators Research (Springer)

**Contenido**:
1. **Introducción**: Justificación y objetivos del IPA27
2. **Marco Teórico**: Fundamentos de prosperidad multidimensional (Legatum, IDH, SPI)
3. **Fuentes de Datos**: Catálogo completo de 24 indicadores, métodos de extracción
4. **Preprocesamiento**:
   - Desestacionalización (STL)
   - Trimestralizacion (Chow-Lin, Denton, agregación)
   - Nowcasting (ARIMA)
5. **Normalización Sigmoide Robusta**: Función basada en mediana e IQR
6. **Agregación Jerárquica**: Media aritmética vs geométrica
7. **Resultados 2025Q3**: Análisis de brechas por dominios y pilares
8. **Discusión**: Implicaciones para políticas públicas, limitaciones
9. **Conclusiones**: Recomendaciones y direcciones futuras

**Archivo fuente**: `methodology.tex` (LaTeX)

---

### 📊 **01_benchmark_analysis.pdf**
**Título**: *Informe Benchmark Índice Prosperidad Andaluz*

**Contenido**:
- Comparación del IPA27 con otros índices:
  - Legatum Prosperity Index (global)
  - Índice de Desarrollo Humano (IDH) subnacional
  - Social Progress Index (SPI)
  - Regional Competitiveness Index (RCI) de la UE
  - OECD Better Life Index
- Ventajas y desventajas metodológicas
- Justificación de decisiones del IPA27

---

### 🏛️ **02_governance_indicators.docx**
**Título**: *Propuesta Metodológica de Indicadores de Gobernanza para Regiones Españolas*

**Contenido**:
- Marco teórico de gobernanza (transparencia, accountability, participación)
- Justificación de GOB_TRA y GOB_CON
- Análisis de sentimiento en redes sociales como proxy
- Validación con encuestas de opinión (CIS)
- Limitaciones y alternativas

---

### 📐 **03_normalization_methods.docx**
**Título**: *Normalización de Indicadores Compuestos de Prosperidad*

**Contenido**:
- Revisión de métodos de normalización:
  - Min-Max (Distance-to-Frontier)
  - Z-score (estandarización)
  - Ranking
  - Percentiles
  - Sigmoide / Logística
- Ventajas de la normalización sigmoide robusta
- Calibración de parámetros ($x_0$, $k$, $\rho$)
- Comparación empírica con min-max en series del IPA27
- Resistencia a outliers: ejemplos

---

### 🔧 **04_technical_documentation.pdf**
**Título**: *Documentación Técnica IPA27. Indicadores*

**Contenido**:
- Fichas técnicas de los 24 indicadores:
  - Definición conceptual
  - Fuente de datos y contacto
  - Método de extracción (API, manual, scraping)
  - Frecuencia original
  - Tratamientos aplicados (per cápita, STL, Chow-Lin, ARIMA)
  - Polaridad (mayor/menor es mejor)
  - Justificación teórica (literatura académica)
- Tabla de correspondencia indicador-pilar-dominio
- Historial de cambios en indicadores

---

### 🏗️ **05_architecture.pdf**
**Título**: *IPA27: Architecture of a Precision Instrument for Regional Prosperity Measurement*

**Contenido**:
- Arquitectura técnica del sistema IPA27
- Diagrama de flujo completo (extracción → procesamiento → agregación)
- Conectores API implementados (INE, IECA, DataInvex)
- Pipeline de preprocesamiento
- Algoritmos de normalización y agregación
- Stack tecnológico (Python, pandas, statsmodels)
- Escalabilidad y extensibilidad del sistema

---

### 📋 **indicators_sources.xlsx**
**Tabla de referencia rápida**

**Hojas del Excel**:
1. **Catálogo**: Código, nombre, fuente, frecuencia, método de extracción
2. **Fuentes**: URLs, APIs, contactos de cada fuente oficial
3. **Tratamientos**: Matriz indicador × tratamiento (STL, Chow-Lin, ARIMA, etc.)
4. **Polaridad**: Dirección de cada indicador (+1 / -1)
5. **Ponderaciones**: Pesos actuales (todos iguales, pero preparado para cambios)

---

## Notas de Trabajo (`methodology/notes/`)

### 📝 **claude_notes.pdf**
Notas de análisis generadas durante el desarrollo del proyecto:
- Exploraciones metodológicas
- Validaciones estadísticas
- Decisiones de diseño y justificaciones

### 📝 **methodology_notes.docx**
Notas metodológicas complementarias:
- Cálculos intermedios
- Alternativas consideradas y descartadas
- Observaciones sobre fuentes de datos

### 📝 **gob_sen_methodology.docx**
Metodología específica para indicadores de sentimiento gubernamental (GOB_SEN):
- Análisis de sentimiento en Twitter/X
- Procesamiento de texto con NLP
- Validación con encuestas CIS
- Construcción de series temporales

---

## Convenios y Contratos (`agreements/`)

### ⚖️ **contract_draft_v0.doc**
Borrador inicial del contrato de desarrollo del IPA27:
- Partes involucradas
- Objeto del contrato
- Obligaciones y entregables
- Plazos y condiciones económicas

### 📑 **proposed_agreement.docx**
Texto propuesto para el convenio de colaboración:
- Instituto de Estudios Regionales
- Junta de Andalucía
- Objetivos del convenio
- Compromisos de las partes
- Propiedad intelectual y difusión

### 📊 **technical_report.docx**
Memoria técnica del IPA27 para organismos financiadores:
- Resumen ejecutivo
- Justificación del proyecto
- Metodología en lenguaje no técnico
- Resultados esperados
- Aplicaciones prácticas para políticas públicas
- Presupuesto y recursos

---

## Infografías (`infographics/`)

### 🎨 **indicators_infographic.png**
Infografía visual de la estructura del IPA27:
- Jerarquía de 3 dominios, 12 pilares, 24 indicadores
- Codificación por colores:
  - Azul: Sociedades Inclusivas
  - Verde: Economías Abiertas
  - Naranja: Personas Empoderadas
- Iconos representativos de cada pilar
- Fuentes de datos principales
- Útil para presentaciones y comunicación pública

---

## Cómo Citar

### Artículo Principal

```bibtex
@article{ipa27_2025,
  title={Arquitectura del Índice de Prosperidad Andaluz (IPA27): Un Enfoque Metodológico Basado en Normalización Sigmoide Robusta y Agregación Jerárquica},
  author={Equipo IPA27},
  journal={Social Indicators Research},
  year={2025},
  publisher={Springer},
  note={Documento en revisión}
}
```

### Documentos Técnicos

```bibtex
@techreport{ipa27_technical_2025,
  title={Documentación Técnica IPA27: Indicadores y Métodos},
  author={Equipo IPA27},
  institution={Instituto de Estudios Regionales, Sevilla},
  year={2025},
  type={Informe Técnico}
}
```

---

## Actualización de Documentación

La documentación se actualiza:
- **Metodología**: Cuando hay cambios en indicadores o métodos de procesamiento
- **Resultados**: Trimestralmente tras publicación de nuevos datos
- **Notas técnicas**: Continuamente durante el desarrollo

---

## Compilación de LaTeX

Para compilar el documento principal `methodology.tex`:

```bash
cd docs/methodology
pdflatex methodology.tex
bibtex methodology
pdflatex methodology.tex
pdflatex methodology.tex
```

O usando latexmk (recomendado):

```bash
latexmk -pdf methodology.tex
```

---

## Contacto para Documentación

**Equipo IPA27**
Instituto de Estudios Regionales
Sevilla, España

Email: ipa27@andalucia.es

---

**Última actualización**: Enero 2026
**Versión metodología**: v1.0 (2025Q3)
