# Datos del Proyecto IPA27

Este directorio contiene todos los datos utilizados en el Índice de Prosperidad Andaluz.

## Estructura

```
data/
├── raw/                    # Datos originales (INMUTABLES - NO MODIFICAR)
│   ├── criminalidad/       # Datos de criminalidad del Ministerio del Interior
│   ├── tic_hogares/        # Encuesta TIC en Hogares (INE)
│   ├── cis/                # Microdatos CIS (sanidad, electoral)
│   ├── transparencia/      # Resoluciones y reclamaciones
│   └── other/              # Otros datos manuales (IED, SS, GOB_SEN)
│
└── processed/              # Datos procesados y transformados
    ├── criminalidad/       # Series de criminalidad procesadas
    └── indicadores/        # 24 indicadores finales del IPA27
```

---

## Datos Raw (Originales)

### ⚠️ IMPORTANTE: NO MODIFICAR ESTOS DATOS

Los datos en `raw/` son los datos originales descargados de fuentes oficiales. **NO deben modificarse nunca**. Cualquier transformación debe guardarse en `processed/`.

### Subdirectorios

#### `raw/criminalidad/`
- **Fuente**: Ministerio del Interior - Portal Estadístico de Criminalidad
- **Formato**: CSV trimestral
- **Contenido**: 40 archivos trimestrales (2016Q1 - 2025Q4)
  - Criminalidad total por CCAA
  - Delitos contra la propiedad (hurtos, robos)
  - Delitos contra libertad sexual
- **Características**:
  - Datos publicados en formato **acumulado anual** (requieren desacumulación)
  - Periodicidad: Trimestral
  - Unidades: Número absoluto de delitos

#### `raw/tic_hogares/`
- **Fuente**: INE - Encuesta sobre Equipamiento y Uso de Tecnologías de Información y Comunicación en los Hogares (TIC-H)
- **Formato**: XLSX (diseño de registro), TAB (microdatos), TXT (cuestionarios)
- **Período**: 2016-2025
- **Subdirectorios**:
  - `cuestionarios/`: Ficheros TXT con definición de variables
  - `diseno_registro/`: Archivos XLSX con estructura de datos
  - `microdatos/`: Archivos TAB con microdatos individuales
- **Indicador generado**: INF_BAN (Porcentaje de hogares con banda ancha)

#### `raw/cis/`
- **Fuente**: Centro de Investigaciones Sociológicas (CIS)
- **Formato**: ZIP con archivos de microdatos
- **Contenido**:
  - `cis_sanidad.zip`: Barómetro Sanitario (Estudio FID3617)
    - Indicador: SAL_SAT (Satisfacción con el sistema sanitario)
    - Frecuencia: Trimestral
  - `cis_electoral.zip`: Participación Electoral (Estudio FID3619)
    - Indicador: SOC_PAR (Tasa de participación electoral)
    - Frecuencia: Anual

#### `raw/transparencia/`
- **Fuente**: Agencia Española de Transparencia
- **Formato**: XLSX, CSV
- **Contenido**:
  - Resoluciones de reclamaciones
  - Indicadores de transparencia gubernamental
- **Indicador generado**: GOB_TRA (Índice de Transparencia)

#### `raw/other/`
Otros datos que requieren descarga manual:

1. **mir_odio.xls**
   - Fuente: Ministerio del Interior - Oficina Nacional de Delitos de Odio
   - Indicador: LIB_ODI (Delitos de odio)
   - Frecuencia: Anual

2. **consulta_datainvex.xls**
   - Fuente: DataInvex (Ministerio de Industria, Comercio y Turismo)
   - Indicador: INV_IED (Inversión Extranjera Directa)
   - Frecuencia: Trimestral

3. **ss_afiliados.csv**
   - Fuente: Seguridad Social - Afiliados por CNAE
   - Indicadores:
     - SOC_ASO (Ocupados en actividades asociativas - Sector S)
     - CON_OCI (Ocupados en sectores intensivos en conocimiento - Sectores J+M)
   - Frecuencia: Mensual

4. **GOB_SEN_final.csv**
   - Fuente: Análisis de sentimiento procesado externamente
   - Indicadores: GOB_CON, GOB_TRA
   - Frecuencia: Trimestral

---

## Datos Processed (Procesados)

### `processed/criminalidad/`
- Series de criminalidad procesadas:
  - Desacumuladas (trimestres puros)
  - Normalizadas per cápita
  - Desestacionalizadas (STL)
- Archivos:
  - `Criminalidad_Unificada.csv`: Serie consolidada
  - `Criminalidad_Andalucia_ESP_Full_Trimestral.csv`: Versión trimestral completa

### `processed/indicadores/`
Contiene los 24 indicadores finales del IPA27 en formato CSV:

#### Indicadores Auxiliares
- `AUX_IPC.csv`: Índice de Precios al Consumo
- `AUX_POB.csv`: Población por CCAA
- `AUX_POB_enlazado.csv`: Población enlazada (series homogéneas)

#### Indicadores del IPA27 (24)

**Sociedades Inclusivas**
- SEG_CRI.csv, SEG_BAL.csv (Seguridad)
- LIB_ODI.csv, LIB_SEX.csv (Libertad)
- GOB_TRA.csv, GOB_CON.csv (Gobernanza)
- SOC_PAR.csv, SOC_ASO.csv (Capital Social)

**Economías Abiertas**
- INV_IED.csv, INV_HIP.csv (Inversión)
- EMP_NAT.csv, EMP_SOC.csv (Empresas)
- INF_BAN.csv, INF_TRA.csv (Infraestructura)
- ECO_PIT.csv, ECO_PIBpc.csv (Calidad Económica)

**Personas Empoderadas**
- VID_ARO.csv, VID_PAR.csv (Vida)
- SAL_ESP.csv, SAL_SAT.csv (Salud)
- EDU_ABA.csv, EDU_SUP.csv (Educación)
- CON_IDI.csv, CON_OCI.csv (Conocimiento)

### Formato de Archivos CSV

Estructura estándar:
```csv
Periodo,Andalucía,España
2016Q1,45.2,52.1
2016Q2,46.1,52.8
...
```

- **Columnas**:
  - `Periodo`: Trimestre en formato YYYYQN (ej: 2025Q3)
  - `Andalucía`: Valor para Andalucía
  - `España`: Valor para España (referencia comparativa)
- **Valores**: Pueden ser en unidades originales (antes de normalización) o normalizados (0-100)

---

## Fuentes de Datos Oficiales

| Fuente | URL | Indicadores |
|--------|-----|-------------|
| INE | https://www.ine.es | 15 indicadores (EPA, PIB, ECV, TIC-H, etc.) |
| IECA | https://www.juntadeandalucia.es/institutodeestadisticaycartografia | ECO_PIT |
| Ministerio del Interior | https://estadisticasdecriminalidad.ses.mir.es | SEG_CRI, SEG_BAL, LIB_SEX, LIB_ODI |
| CIS | https://www.cis.es | SAL_SAT, SOC_PAR |
| DataInvex | https://datainvex.comercio.es | INV_IED |
| Seguridad Social | https://www.seg-social.es | SOC_ASO, CON_OCI |

---

## Política de Datos

### Descarga y Almacenamiento
- Los datos se descargan de fuentes oficiales públicas
- Algunos datos requieren descarga manual por restricciones de acceso
- Los datos raw deben conservarse en su formato original

### Reproducibilidad
- Todo el procesamiento es reproducible ejecutando los notebooks en orden
- Los scripts documentan cada transformación aplicada
- Las fuentes de datos están claramente identificadas

### Actualización
- Los datos deben actualizarse trimestralmente tras la publicación de estadísticas oficiales
- El publication lag varía según la fuente (1-6 meses)

### Privacidad
- Todos los datos utilizados son públicos y agregados
- No se procesan datos personales individuales

---

## Mantenimiento

### Actualizar Datos
1. Descargar nuevos datos de fuentes oficiales
2. Colocar en `raw/` manteniendo la estructura
3. Ejecutar notebooks de procesamiento
4. Verificar coherencia de las series

### Backup
Se recomienda hacer backups periódicos de `data/raw/` ya que algunas fuentes eliminan datos históricos.

---

**Última actualización**: Enero 2026
**Período cubierto**: 2016Q1 - 2025Q3
**Total indicadores**: 24 + 3 auxiliares
