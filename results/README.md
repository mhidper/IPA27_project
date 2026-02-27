# Resultados del IPA27

Este directorio contiene todos los resultados finales del Índice de Prosperidad Andaluz: datos consolidados y visualizaciones.

## Estructura

```
results/
├── data/                       # Datos finales del índice
│   ├── ipa27_raw.xlsx
│   ├── ipa27_quarterly.xlsx
│   ├── ipa27_normalized.xlsx
│   └── ipa27_aggregated.xlsx
│
└── figures/                    # Visualizaciones
    ├── indicators/             # Gráficos por indicador (27 imágenes)
    └── analysis/               # Dashboards y análisis (10 imágenes)
```

---

## Datos Finales (`data/`)

### 1. `ipa27_raw.xlsx`
**Datos brutos antes de normalización**

- **Contenido**: Valores originales de los 24 indicadores en sus unidades naturales
- **Hojas del Excel**:
  - `Indicadores`: Todos los indicadores en unidades originales
  - `Metadatos`: Descripción de cada indicador, fuentes, unidades
- **Uso**: Verificar datos fuente antes de transformaciones

### 2. `ipa27_quarterly.xlsx`
**Series trimestrales unificadas**

- **Contenido**: Todos los indicadores en frecuencia trimestral
- **Transformaciones aplicadas**:
  - Mensual → Trimestral (agregación)
  - Anual → Trimestral (Chow-Lin, Denton)
  - Nowcasting (ARIMA) para valores faltantes
  - Desestacionalización (STL) donde aplique
- **Hojas del Excel**:
  - Por dominio: `Sociedades_Inclusivas`, `Economias_Abiertas`, `Personas_Empoderadas`
  - `Completo`: Todos los indicadores juntos
  - `Metadatos`: Información de procesamiento

### 3. `ipa27_normalized.xlsx`
**Indicadores normalizados (escala 0-100)**

- **Contenido**: Todos los indicadores normalizados mediante función sigmoide robusta
- **Método de normalización**:
  - Función sigmoide: $S(x) = \frac{\rho \cdot 100}{1 + \exp(-k \cdot (x - x_0))}$
  - Punto de inflexión $x_0$: Mediana de la distribución histórica conjunta (AND+ESP)
  - Sensibilidad $k$: Calibrada inversamente al IQR (Rango Intercuartílico)
  - Polaridad $\rho$: +1 (mayor es mejor) o -1 (menor es mejor)
- **Interpretación**: Valores cercanos a 50 = mediana histórica
- **Ventajas**: Resistente a outliers, interpretabilidad percentílica

### 4. `ipa27_aggregated.xlsx`
**Índice agregado final (IPA27)**

- **Contenido**: Resultados consolidados del IPA27
- **Hojas del Excel**:
  - `Pilares`: Puntuaciones de los 12 pilares (0-100)
  - `Dominios`: Puntuaciones de los 3 dominios (0-100)
  - `IPA27_Total`: Índice global (0-100)
  - `Brechas`: Diferencias Andalucía - España
  - `Ranking_Temporal`: Evolución trimestral
  - `Resumen_2025Q3`: Snapshot del último trimestre

**Método de agregación**:
- Indicadores → Pilares: **Media aritmética** (sustituibilidad perfecta)
- Pilares → Dominios: **Media geométrica** (penalización de desequilibrios)
- Dominios → IPA27: **Media geométrica**

**Ejemplo de cálculo**:
```
Pilar Seguridad = (SEG_CRI + SEG_BAL) / 2              [Media aritmética]
Dominio SI = (Seg * Lib * Gob * CS)^(1/4)              [Media geométrica]
IPA27 = (SI * EA * PE)^(1/3)                            [Media geométrica]
```

---

## Visualizaciones (`figures/`)

### Indicadores (`figures/indicators/`)

Contiene **27 gráficos** (24 indicadores + 3 auxiliares):

- **Formato**: PNG (alta resolución)
- **Contenido por gráfico**:
  - Serie temporal completa (2016Q1 - 2025Q3)
  - Líneas separadas para Andalucía (azul) y España (naranja)
  - Marcadores trimestrales
  - Grid para facilitar lectura
  - Título descriptivo con código del indicador

**Ejemplos de archivos**:
- `AUX_IPC_Andalucía_España.png`
- `SEG_CRI_Andalucía_España.png`
- `ECO_PIBpc_Andalucía_España.png`
- `EDU_SUP_Andalucía_España_enlazado.png` (series enlazadas)

### Análisis (`figures/analysis/`)

Contiene **10 visualizaciones principales**:

#### 1. `ipa27_dashboard.png`
**Dashboard completo del IPA27**
- Panel superior izquierdo: Evolución temporal del índice total (2016-2025)
- Panel superior derecho: Radar de 12 pilares (AND vs ESP)
- Panel inferior izquierdo: Barras de 3 dominios (AND vs ESP)
- Panel inferior derecho: Brechas horizontales por pilar

#### 2. `ipa27_dominios.png`
**Comparación de los 3 dominios**
- Gráfico de barras agrupadas
- Andalucía vs España
- Colores diferenciados por dominio

#### 3. `ipa27_pilares.png`
**Radar plot de los 12 pilares**
- Visualización tipo araña
- Dos polígonos superpuestos (AND, ESP)
- Facilita identificación visual de fortalezas/debilidades

#### 4. `ipa27_brecha_dominios.png`
**Brechas entre Andalucía y España por dominio**
- Barras horizontales
- Verde: Ventaja andaluza (+)
- Naranja: Desventaja andaluza (-)
- Ordenadas por magnitud de brecha

#### 5. `ipa27_brecha_pilares.png`
**Brechas entre Andalucía y España por pilar**
- Similar a brecha_dominios, pero con 12 pilares
- Identifica los 3 pilares con mayor brecha:
  - Educación: -26.7 puntos
  - Vida: -26.3 puntos
  - Conocimiento: -22.3 puntos

#### 6. `ipa27_indicadores.png`
**Grid de 24 mini-gráficos**
- Un gráfico pequeño por cada indicador
- Permite visión global de todas las series
- Código y tendencia visible en cada panel

#### 7. `ipa27_indicadores_trimestrales.png`
**Series trimestrales tras procesamiento**
- Visualiza el resultado de la trimestralizacion
- Muestra interpolaciones y proyecciones
- Útil para validar métodos de Chow-Lin/Denton

#### 8. `ipa27_desestacionalizacion.png`
**Efecto de la desestacionalización STL**
- Panel superior: Serie original vs desestacionalizada
- Panel inferior: Componente estacional extraído
- Muestra 6 indicadores con patrones estacionales significativos

#### 9. `ipa27_trimestralizacion.png`
**Desagregación anual → trimestral (Chow-Lin)**
- Línea punteada: Valores anuales originales
- Línea continua: Serie trimestral desagregada
- Áreas sombreadas: Trimestres interpolados
- Validación del método de Chow-Lin con regresores

#### 10. `ipa27_nowcasting.png`
**Extensión de series mediante ARIMA**
- Línea azul sólida: Valores observados
- Línea naranja: Proyecciones ARIMA
- Banda gris: Intervalo de confianza al 95%
- Muestra 7 indicadores con publication lag

---

## Interpretación de Resultados

### Escala de Puntuaciones (0-100)

| Rango | Interpretación |
|-------|----------------|
| 75-100 | Excelente - Por encima del percentil 75 histórico |
| 60-75 | Bueno - Por encima de la mediana histórica |
| 50-60 | Moderado - Ligeramente por encima de la mediana |
| 40-50 | Mediocre - Ligeramente por debajo de la mediana |
| 25-40 | Bajo - Por debajo del percentil 25 histórico |
| 0-25 | Muy bajo - Extremo inferior de la distribución |

**Nota**: 50 puntos = Mediana histórica de la distribución conjunta Andalucía + España (2016-2025)

### Brechas (Andalucía - España)

| Brecha | Significado |
|--------|-------------|
| +10 o más | Ventaja andaluza fuerte |
| +5 a +10 | Ventaja andaluza moderada |
| -5 a +5 | Paridad (sin diferencia significativa) |
| -10 a -5 | Desventaja andaluza moderada |
| -10 o menos | Desventaja andaluza fuerte |

### Resultados Destacados (2025Q3)

**IPA27 Total**:
- Andalucía: **46.3**
- España: **50.9**
- Brecha: **-4.7** (desventaja moderada)

**Dominio con mayor ventaja**:
- Sociedades Inclusivas: **+3.3** (fortaleza en capital social y seguridad)

**Dominio con mayor brecha**:
- Personas Empoderadas: **-22.8** (retos en educación, empleo, I+D)

**Pilares críticos** (requieren atención prioritaria):
1. Educación (EDU): -26.7
2. Vida (VID): -26.3
3. Conocimiento (CON): -22.3

---

## Uso de Resultados

### Para Investigadores
- Analizar evolución temporal del IPA27
- Identificar factores determinantes de brechas
- Comparar metodología con otros índices compuestos
- Validar métodos de normalización y agregación

### Para Policymakers
- Diagnosticar áreas prioritarias de intervención
- Evaluar impacto de políticas públicas
- Diseñar estrategias regionales basadas en evidencia
- Monitorear convergencia/divergencia con media nacional

### Para Comunicación
- Dashboards y visualizaciones listas para presentaciones
- Datos en Excel para análisis personalizados
- Interpretación clara de puntuaciones y brechas

---

## Actualización

Los resultados se actualizan trimestralmente tras:
1. Publicación de nuevas estadísticas oficiales
2. Ejecución del pipeline de procesamiento
3. Validación de coherencia de las series
4. Regeneración de visualizaciones

**Próxima actualización esperada**: Abril 2026 (datos 2025Q4)

---

## Referencias

Para más detalles metodológicos, consultar:
- `docs/methodology/methodology.pdf`: Artículo completo
- `docs/methodology/04_technical_documentation.pdf`: Documentación técnica

---

**Última actualización**: Enero 2026
**Trimestre actual**: 2025Q3
**Fecha de cálculo**: 2026-01-08
