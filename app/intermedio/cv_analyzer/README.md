# Analizador de Currículums con Inteligencia Artificial

Aplicación web y móvil desarrollada en Streamlit orientada a la evaluación objetiva de candidatos mediante la comparación sistemática entre un currículum en formato PDF y los requisitos técnicos de un puesto. El procesamiento extrae el texto en memoria, ejecuta inferencia estructurada mediante LangChain y ChatOpenAI (gpt-4o-mini) bajo una rúbrica de ponderación multicriterio, y presenta los resultados a través de un panel ejecutivo de toma de decisiones.

## Características Principales

- Ingesta de documentos en formato PDF con extracción de texto seleccionable en memoria mediante PyPDF2.
- Telemetría de documento con conteo de páginas, palabras, caracteres y estimación de tokens.
- Especificación estructurada del perfil requerido: título de la vacante, etiquetas de correspondencia rápida y descripción técnica integral.
- Inferencia determinística con ChatOpenAI (gpt-4o-mini, temperatura 0.2) y validación de esquema con Pydantic.
- Trazabilidad del pipeline en tiempo real dividida en cuatro fases: lectura binaria, preparación de directivas, inferencia del modelo y verificación estructural.
- Cuantificación global del nivel de adecuación (0 a 100) y desglose en cuatro factores ponderados.
- Categorización doble según umbrales institucionales de evaluación y recomendación final.
- Generación de informes ejecutivos descargables en formato PDF mediante ReportLab.
- Entorno de demostración con candidatos preconfigurados para verificación de umbrales extremos y casos intermedios.

## Criterios de Evaluación y Ponderación

El análisis evalúa al candidato sobre una escala porcentual estandarizada con base en las siguientes dimensiones:

| Criterio | Ponderación | Descripción |
| :--- | :---: | :--- |
| Experiencia relevante | 40 % | Trayectoria profesional en roles afines, responsabilidades directas y años de experiencia en el área. |
| Habilidades técnicas | 35 % | Correspondencia con tecnologías esenciales y deseables, arquitecturas de software y herramientas de ingeniería. |
| Formación y certificaciones | 15 % | Nivel académico, títulos de grado o posgrado y certificaciones de industria vigentes. |
| Coherencia profesional | 10 % | Continuidad, estabilidad en posiciones precedentes y progresión en responsabilidades. |

### Umbrales de Calificación

La clasificación principal segmenta el desempeño en cuatro bandas:

| Rango Porcentual | Evaluación Principal |
| :--- | :--- |
| 80 - 100 | Excelente |
| 60 - 79 | Bueno |
| 40 - 59 | Regular |
| 0 - 39 | Bajo |

La decisión de contratación se estructura en tres niveles:

| Rango Porcentual | Recomendación Final |
| :--- | :--- |
| 70 - 100 | Candidato recomendado |
| 50 - 69 | Candidato con potencial |
| 0 - 49 | Candidato no recomendado |

## Arquitectura del Proyecto

El repositorio adopta una separación clara de responsabilidades:

```text
Agente_Curriculums/
├── requirements.txt                      # Dependencias del entorno Python
├── Dockerfile                            # Especificación de contenedor Docker
├── docker-compose.yml                    # Configuración de orquestación local
└── app/
    └── intermedio/
        └── cv_analyzer/
            ├── app.py                    # Punto de entrada de la aplicación
            ├── README.md                 # Documentación técnica del módulo
            ├── models/
            │   └── cv_model.py           # Esquemas Pydantic AnalisisCV y submodelos
            ├── prompts/
            │   └── cv_prompts.py         # Plantillas de sistema y usuario para LangChain
            ├── services/
            │   ├── pdf_processor.py      # Extracción y metadatos de archivos PDF
            │   └── cv_evaluator.py       # Configuración de inferencia y motor de evaluación
            └── ui/
                └── streamlit_ui.py       # Interfaz de usuario, vistas y exportación PDF
```

### Esquema de Datos (AnalisisCV)

El modelo de salida estructura los siguientes campos validados:

| Campo | Tipo | Definición |
| :--- | :--- | :--- |
| nombre_candidato | str | Nombre completo identificado en el documento |
| experiencia_años | int | Total estimado de años de trayectoria afín |
| habilidades_clave | list[str] | Competencias técnicas validadas para el puesto |
| education | str | Máximo grado formativo e institución de origen |
| experiencia_relevante | str | Síntesis narrativa de trayectoria afín |
| fortalezas | list[str] | Ventajas competitivas y puntos sobresalientes |
| areas_mejora | list[str] | Brechas técnicas y temas sugeridos para entrevista |
| porcentaje_ajuste | int | Puntuación general calculada (0 a 100) |
| puesto_detectado | str | Rol profesional inferido del candidato |
| resumen_ejecutivo | str | Conclusión técnica del perfil |
| nivel_confianza | str | Índice de certeza de la inferencia |
| criterios | PonderacionCriterios | Puntuación (0 a 100) y justificación por factor |

## Requisitos del Sistema

- Python 3.12 o 3.14.
- Clave de API de OpenAI (variable OPENAI_API_KEY) con acceso a gpt-4o-mini. Si no se dispone de cuota activa, el sistema opera mediante un evaluador heurístico estructurado de respaldo sin degradar la interfaz.
- Archivo PDF con capa de texto digital seleccionable (el sistema no realiza OCR sobre imágenes planas).

## Instalación y Ejecución

### 1. Entorno Local

Crear y activar un entorno virtual:

```bash
# En Linux/macOS
python3 -m venv .venv
source .venv/bin/activate

# En Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instalar las dependencias requeridas:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Configurar la variable de entorno:

```bash
# En Linux/macOS
export OPENAI_API_KEY="tu_clave_de_openai"

# En Windows PowerShell
$env:OPENAI_API_KEY = "tu_clave_de_openai"
```

Ejecutar la interfaz:

```bash
cd app/intermedio/cv_analyzer
python -m streamlit run app.py --server.port=8501
```

Acceder desde el navegador a: http://localhost:8501

### 2. Ejecución con Docker

Construcción y ejecución del contenedor independiente:

```bash
docker build -t talentai-analyzer .
docker run --rm -p 8501:8501 -e OPENAI_API_KEY talentai-analyzer
```

Ejecución mediante Docker Compose:

```bash
docker compose up -d --build
```

Detener el servicio:

```bash
docker compose down
```

## Flujo Operativo de la Aplicación

1. **Paso 1: Entrada de Datos**
   - El usuario carga el archivo PDF o utiliza los perfiles de prueba integrados.
   - Se ingresan los requerimientos técnicos y responsabilidades del puesto.
   - Al seleccionar "Analizar Candidato con IA", la interfaz valida la presencia de ambas entradas.

2. **Paso 2: Pipeline en Tiempo Real**
   - Extracción de texto con PyPDF2 sin persistencia binaria.
   - Construcción del prompt del sistema con directivas de ponderación institucional.
   - Ejecución de la cadena con ChatOpenAI y structured_output.
   - Validación de tipos de datos, coherencia de scoring y umbrales de decisión.

3. **Paso 3: Evaluación y Resultados**
   - Presentación de métricas consolidadas, porcentaje general de ajuste y recomendación.
   - Desglose analítico de los cuatro criterios clave con barras de progreso.
   - Visualización de competencias técnicas validadas, fortalezas y brechas.
   - Descarga del informe técnico en PDF estructurado y registro en memoria de sesión.

## Casos de Prueba Incluidos

La aplicación cuenta con perfiles precargados para verificar el funcionamiento de las clasificaciones:

- **Cumplimiento Óptimo (100 %):** Candidata con perfil senior, certificaciones avanzadas y ajuste completo a las tecnologías requeridas. Clasificación: Excelente / Candidato recomendado.
- **Caso Intermedio (78 %):** Candidato con experiencia sólida en backend y correspondencia mayoritaria. Clasificación: Bueno / Candidato recomendado.
- **Caso No Afín (18 %):** Perfil orientado al sector culinario y repostero sin antecedentes de desarrollo. Clasificación: Bajo / Candidato no recomendado.
