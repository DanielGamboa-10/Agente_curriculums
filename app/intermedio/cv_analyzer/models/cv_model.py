from pydantic import BaseModel, Field
from typing import List, Optional

class AnalisisCriterio(BaseModel):
    puntuacion: int = Field(..., ge=0, le=100, description="Puntuación de 0 a 100 para este factor específico")
    justificacion: str = Field(..., description="Breve justificación o evidencia del candidato para este criterio")

class PonderacionCriterios(BaseModel):
    experiencia_relevante: AnalisisCriterio = Field(
        ..., 
        description="Puntuación y justificación para Experiencia relevante (40% peso)"
    )
    habilidades_tecnicas: AnalisisCriterio = Field(
        ..., 
        description="Puntuación y justificación para Habilidades técnicas (35% peso)"
    )
    formacion_certificaciones: AnalisisCriterio = Field(
        ..., 
        description="Puntuación y justificación para Formación y certificaciones (15% peso)"
    )
    coherencia_profesional: AnalisisCriterio = Field(
        ..., 
        description="Puntuación y justificación para Coherencia profesional y trayectoria (10% peso)"
    )

class AnalisisCV(BaseModel):
    nombre_candidato: str = Field(..., description="Nombre completo extraído del currículum vitae")
    experiencia_años: int = Field(..., ge=0, description="Años totales de experiencia laboral relevante estimados")
    habilidades_clave: List[str] = Field(..., description="Lista de habilidades técnicas y profesionales clave detectadas relevantes para el puesto")
    education: str = Field(..., description="Nivel educativo máximo, título obtenido y especialización o institución")
    experiencia_relevante: str = Field(..., description="Resumen ejecutivo del perfil y experiencia contrastada con el puesto solicitado")
    fortalezas: List[str] = Field(..., description="Principales fortalezas y ventajas competitivas del candidato frente a la vacante")
    areas_mejora: List[str] = Field(..., description="Áreas de desarrollo, brechas técnicas o aspectos a profundizar en entrevista")
    porcentaje_ajuste: int = Field(..., ge=0, le=100, description="Porcentaje global de ajuste al puesto entre 0 y 100 calculado según los pesos")
    
    # Campos enriquecidos para soporte del diseño UI (Paso 3)
    puesto_detectado: Optional[str] = Field(
        default="Perfil Profesional",
        description="Título o rol profesional identificado del candidato (ej: Senior Backend Engineer)"
    )
    resumen_ejecutivo: Optional[str] = Field(
        default=None,
        description="Resumen narrativo de alto impacto sobre el ajuste y potencial del perfil"
    )
    nivel_confianza: Optional[str] = Field(
        default="Alto (95%)",
        description="Nivel de confianza predictiva del análisis de IA"
    )
    criterios: Optional[PonderacionCriterios] = Field(
        default=None,
        description="Desglose detallado de los 4 factores clave de ponderación"
    )

