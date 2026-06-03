# Documentación y Metodología del Proyecto IPA27

Este directorio contiene toda la documentación metodológica, técnica, de análisis y contractual del **Índice de Prosperidad Andaluz (IPA27)**.

## Estructura de Directorios

```
docs/
├── README.md                          # Este índice de documentación
│
├── convenios/                         # Convenios, contratos y memorias técnicas
│   ├── Memo-eco-EY-MHidalgo.xls       # Presupuesto e histórico
│   ├── Memoria.docx                   # Memoria descriptiva
│   ├── autorDpto-CÁMARAS-2º-MHidalgo* (pdf, docx, firmados) # Autorizaciones
│   ├── contract_draft_v0.doc          # Borrador de contrato de desarrollo
│   ├── proposed_agreement.docx        # Texto propuesto para el convenio
│   ├── technical_report.docx          # Memoria técnica para organismos
│   ├── 260318 Cont-EYEE rev EY.doc    # Contrato con EY
│   └── 260318 Cont-EYEE rev EY_signed.pdf # Contrato firmado con EY
│
├── infografias/                       # Elementos visuales y divulgativos
│   └── indicators_infographic.png     # Infografía del árbol de indicadores (3 dominios, 12 pilares, 24 variables)
│
└── metodologia/                       # Todo el material científico y metodológico del índice
    ├── 01_general/                    # Metodología global, benchmarks y Beamer
    │   ├── methodology.tex            # Artículo LaTeX principal del IPA27 (Social Indicators Research)
    │   ├── methodology.pdf            # PDF compilado del artículo principal
    │   ├── 01_benchmark_analysis.pdf  # Informe de comparación con otros índices (Legatum, SPI, IDH)
    │   ├── Informe Benchmark Índice Prosperidad Andaluz.docx # Fuente del benchmark
    │   ├── 02_governance_indicators.docx # Propuesta metodológica para Gobernanza
    │   ├── 03_normalization_methods.docx # Revisión de métodos de normalización y sigmoide
    │   ├── 05_architecture.pdf        # Documentación técnica de arquitectura del pipeline
    │   ├── indicators_sources.xlsx    # Excel de referencia de fuentes, polaridad y transformaciones
    │   ├── ideas_fuerza_resultados.md # 6 mensajes clave para la venta de resultados
    │   ├── ipa27_variables.tex        # Macros LaTeX generadas por el pipeline de exportación
    │   ├── presentacion_ipa27_v5.tex  # Código de la presentación Beamer (compilación automática)
    │   ├── presentacion_ipa27_v5.pdf  # PDF compilado de la presentación Beamer
    │   └── *.png                      # Gráficos de resultados (radar, brechas, evolución)
    │
    ├── 02_desafeccion/                # Indicador de Desconfianza Política (Desafección)
    │   ├── IPA27_Metodologia_Desafeccion.tex # Nota metodológica en LaTeX
    │   ├── IPA27_Metodologia_Desafeccion.pdf # PDF de la nota metodológica
    │   ├── Metodología de Indicador de Desconfianza Política_GEMINI.docx # Informe de diseño
    │   ├── Metodología de Indicador de Desconfianza Política_GEMINI.pdf # PDF del informe de diseño
    │   ├── paper_indice_desafeccion.tex # Paper académico sobre el índice
    │   ├── paper_indice_desafeccion.pdf # PDF del paper académico
    │   └── indice de desconfianza_Claude.txt # Notas de desarrollo
    │
    ├── 03_participacion_electoral/    # Indicador de Participación Electoral
    │   ├── IPA27_Metodologia_Electoral.tex # Nota metodológica en LaTeX
    │   └── IPA27_Metodologia_Electoral.pdf # PDF de la nota metodológica
    │
    └── notas_trabajo/                 # Notas de Claude y borradores de análisis
        ├── claude_notes.pdf           # Notas analíticas de validación y simulación
        ├── gob_sen_methodology.docx   # Nota de análisis de sentimiento
        └── methodology_notes.docx     # Notas sobre el cálculo y alternativas
```

---

## Compilación de LaTeX

### 1. Artículo Metodológico Principal
Para compilar el documento principal `docs/metodologia/01_general/methodology.tex`:
```bash
cd docs/metodologia/01_general
pdflatex methodology.tex
bibtex methodology
pdflatex methodology.tex
pdflatex methodology.tex
```

### 2. Presentación Beamer
La presentación Beamer `docs/metodologia/01_general/presentacion_ipa27_v5.tex` se compila **automáticamente** desde el notebook `02_3_exportacion.ipynb` al terminar la ejecución del pipeline. Para hacerlo de forma manual:
```bash
cd docs/metodologia/01_general
pdflatex presentacion_ipa27_v5.tex
pdflatex presentacion_ipa27_v5.tex
```

---
**Última actualización**: Junio 2026
**Versión de estructura**: v2.0 (Consolidada y Racionalizada)
