# Analizador de Currículums con Inteligencia Artificial (TalentAI)

Aplicación web y móvil desarrollada con Streamlit, LangChain, PyPDF2 y modelos de lenguaje de OpenAI (gpt-4o-mini), orientada a la evaluación objetiva de candidatos mediante la contrastación sistemática entre un currículum vitae en formato PDF y los requisitos técnicos de un puesto de trabajo.

El sistema procesa el documento en memoria, ejecuta inferencia determinística estructurada bajo una rúbrica de ponderación multicriterio, y presenta los resultados a través de un panel analítico ejecutivo en modo oscuro.

---

## Tabla de Contenidos

- [Características Principales](#características-principales)
- [Criterios de Evaluación y Ponderación](#criterios-de-evaluación-y-ponderación)
- [Umbrales de Calificación y Decisión](#umbrales-de-calificación-y-decisión)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Esquema de Salida Pydantic](#esquema-de-salida-pydantic)
- [Requisitos Técnicos](#requisitos-técnicos)
- [Instalación y Ejecución Local](#instalación-y-ejecución-local)
- [Ejecución con Docker](#ejecución-con-docker)
- [Flujo de la Aplicación](#flujo-de-la-aplicación)
- [Casos de Prueba Integrados](#casos-de-prueba-integrados)

---

## Características Principales

- **Ingesta de Documentos en Memoria:** Lectura y extracción directa de texto digital desde archivos PDF mediante PyPDF2, sin almacenamiento persistente ni escritura temporal de archivos binarios.
- **Telemetría y Métricas del Documento:** Identificación inmediata del número de páginas, palabras, caracteres y conteo estimado de tokens a ser procesados.
- **Entrada Estructurada del Puesto:** Definición del rol vacante, etiquetas de coincidencia rápida y campo detallado para requisitos mandatorios, competencias deseables y responsabilidades del puesto.
- **Inferencia Determinística Estructurada:** Integración con LangChain y ChatOpenAI (`gpt-4o-mini`, temperatura 0.2) utilizando `with_structured_output` respaldado por esquemas Pydantic.
- **Mecanismo de Respaldo Heurístico:** Motor de análisis sintáctico local que garantiza continuidad operativa y respuesta estructurada en escenarios de indisponibilidad de API o cuota de servicio.
- **Monitoreo del Pipeline en Tiempo Real:** Visualización en vivo de las fases de inferencia (extracción de texto, formateo de directivas de sistema, llamada a LLM y validación de tipos).
- **Interfaz Ejecutiva en Modo Oscuro:** Interfaz optimizada con contraste uniforme (Deep Obsidian Dark Mode) inspirada en sistemas de diseño de alta precisión.
- **Exportación de Informes en PDF:** Módulo de generación de informes técnicos formales en formato PDF utilizando ReportLab para descarga inmediata.

---

## Criterios de Evaluación y Ponderación

El análisis evalúa al candidato sobre una escala estandarizada de 0 a 100 puntos a partir de cuatro dimensiones cardinales:

| Factor | Ponderación | Alcance Evaluado |
| :--- | :---: | :--- |
| **Experiencia Relevante** | **40 %** | Trayectoria profesional en roles técnicos análogos, responsabilidades operativas y años de experiencia real contrastados frente a la vacante. |
| **Habilidades Técnicas** | **35 %** | Dominio y correspondencia con el conjunto de tecnologías obligatorias y deseables, lenguajes, frameworks, bases de datos y arquitecturas. |
| **Formación y Certificaciones** | **15 %** | Nivel educativo máximo acreditado, pertinencia de la carrera o especialización e idoneidad de certificaciones oficiales de industria. |
| **Coherencia Profesional** | **10 %** | Continuidad en la trayectoria, evolución de responsabilidades, estabilidad contractual y balance general del perfil. |

---

## Umbrales de Calificación y Decisión

La aplicación aplica dos niveles complementarios de evaluación institucional:

### 1. Evaluación Principal

| Porcentaje Obtenido | Calificación Principal |
| :---: | :--- |
| 80 - 100 % | Excelente |
| 60 - 79 % | Bueno |
| 40 - 59 % | Regular |
| 0 - 39 % | Bajo |

### 2. Recomendación Final de Contratación

| Porcentaje Obtenido | Decisión Institucional |
| :---: | :--- |
| 70 - 100 % | Candidato recomendado |
| 50 - 69 % | Candidato con potencial |
| 0 - 49 % | Candidato no recomendado |

---

## Estructura del Proyecto

El proyecto implementa una arquitectura modular desacoplada:

```text
Agente_Curriculums/
├── .gitignore                            # Exclusión de entornos virtuales y cachés
├── Dockerfile                            # Imagen base con Python 3.12 y dependencias
├── docker-compose.yml                    # Orquestación de contenedores para despliegue
├── requirements.txt                      # Lista de dependencias del entorno
├── README.md                             # Documentación global del repositorio
├── .streamlit/
│   └── config.toml                       # Configuración de tema oscuro de Streamlit
└── app/
    └── intermedio/
        └── cv_analyzer/
            ├── app.py                    # Punto de entrada de la aplicación Streamlit
            ├── README.md                 # Documentación técnica del módulo
            ├── models/
            │   └── cv_model.py           # Modelos Pydantic (AnalisisCV, Criterios)
            ├── prompts/
            │   └── cv_prompts.py         # Plantillas de sistema y usuario para LangChain
            ├── services/
            │   ├── pdf_processor.py      # Extracción y telemetría de archivos PDF
            │   └── cv_evaluator.py       # Invocación estructurada a OpenAI y respaldo
            └── ui/
                └── streamlit_ui.py       # Frontend de Streamlit, estilos CSS y exportación
```

---

## Esquema de Salida Pydantic

El análisis responde obligatoriamente al modelo `AnalisisCV`:

| Atributo | Tipo | Descripción |
| :--- | :--- | :--- |
| `nombre_candidato` | `str` | Nombre completo extraído del currículum |
| `experiencia_años` | `int` | Total estimado de años de trayectoria relevante |
| `habilidades_clave` | `list[str]` | Habilidades técnicas verificadas y afines al puesto |
| `education` | `str` | Nivel educativo máximo, titulación e institución |
| `experiencia_relevante` | `str` | Síntesis narrativa de la trayectoria contrastada |
| `fortalezas` | `list[str]` | Principales ventajas competitivas frente a la vacante |
| `areas_mejora` | `list[str]` | Brechas técnicas y puntos de profundización en entrevista |
| `porcentaje_ajuste` | `int` | Porcentaje global calculado (validado entre 0 y 100) |
| `puesto_detectado` | `str` | Rol profesional identificado en el candidato |
| `resumen_ejecutivo` | `str` | Conclusión analítica del modelo sobre el perfil |
| `nivel_confianza` | `str` | Nivel de certeza predictiva del análisis |
| `criterios` | `PonderacionCriterios` | Puntuación individual (0 a 100) y justificación por factor |

---

## Requisitos Técnicos

- Python 3.12 o 3.14.
- Conexión a Internet para la comunicación con el endpoint de OpenAI.
- Variable de entorno `OPENAI_API_KEY` configurada. En ausencia de clave, el sistema conmuta automáticamente a evaluación asistida local estructurada.
- Archivos PDF con capas de texto seleccionables (el software no incorpora OCR para escaneos de imágenes planas).

---

## Instalación y Ejecución Local

### 1. Clonar el Repositorio

```bash
git clone https://github.com/DanielGamboa-10/Agente_curriculums.git
cd Agente_curriculums
```

### 2. Configurar el Entorno Virtual

En Linux / macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

En Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar Dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configurar la Clave de API

En Linux / macOS:
```bash
export OPENAI_API_KEY="tu_clave_de_openai"
```

En Windows (PowerShell):
```powershell
$env:OPENAI_API_KEY = "tu_clave_de_openai"
```

### 5. Iniciar la Aplicación

```bash
cd app/intermedio/cv_analyzer
python -m streamlit run app.py --server.port=8501
```

Abre en tu navegador: `http://localhost:8501`

---

## Ejecución con Docker

### Contenedor Independiente

```bash
docker build -t talentai-analyzer .
docker run --rm -p 8501:8501 -e OPENAI_API_KEY talentai-analyzer
```

### Mediante Docker Compose

```bash
docker compose up -d --build
```

Para detener los contenedores:
```bash
docker compose down
```

---

## Flujo de la Aplicación

1. **Paso 1: Entrada de Datos (Carga & Puesto):**  
   Carga del archivo PDF o selección de un perfil de demostración rápida, verificación de texto seleccionable, e ingreso de los parámetros del puesto.
2. **Paso 2: Pipeline LLM en Tiempo Real (Análisis):**  
   Monitoreo secuencial de la extracción binaria, estructuración de directivas de sistema, llamada a OpenAI y validación de tipos Pydantic.
3. **Paso 3: Resultados y Auditoría (Evaluación):**  
   Visualización del porcentaje global, indicador Match Gauge circular, desglose de los cuatro criterios ponderados, tarjetas de fortalezas y brechas, descarga del informe en PDF y registro en el historial.

---

## Casos de Prueba Integrados

Para verificar el correcto funcionamiento de los umbrales institucionales, la aplicación incorpora botones de demostración directa:

- **Pasa al 100 % (Dra. Elena Santillán Ramos):**  
  Perfil técnico de alta cualificación con correspondencia absoluta en todas las tecnologías obligatorias y deseables, certificaciones AWS/Docker y liderazgo de microservicios.  
  *Resultado:* 100 % de match | Excelente | Candidato recomendado.
- **Caso Intermedio / Regular (Carlos Mendoza):**  
  Desarrollador con trayectoria sólida en backend, APIs y PostgreSQL con gaps menores en tecnologías específicas.  
  *Resultado:* 78 % de match | Bueno | Candidato recomendado.
- **No Pasa / No Afín (Juan Pérez Gómez):**  
  Perfil perteneciente al área de repostería y gastronomía sin competencias de desarrollo técnico ni bases de datos.  
  *Resultado:* 18 % de match | Bajo | Candidato no recomendado.
