import io
from typing import Tuple, Dict, Any
from PyPDF2 import PdfReader

def extraer_texto_pdf(archivo_pdf) -> Tuple[str, Dict[str, Any]]:
    """
    Lee el archivo PDF en memoria con PyPDF2, recorre sus páginas y concatena
    el texto con separadores de página. Devuelve una tupla (texto, metadatos).
    
    Si no encuentra texto o falla la lectura, devuelve un mensaje descriptivo de error.
    """
    if archivo_pdf is None:
        return "Error: No se ha proporcionado ningún archivo PDF.", {}

    try:
        # Asegurarse de tener un stream de bytes
        if hasattr(archivo_pdf, "read"):
            stream = io.BytesIO(archivo_pdf.read())
            # Restablecer el puntero si es posible
            if hasattr(archivo_pdf, "seek"):
                archivo_pdf.seek(0)
        elif isinstance(archivo_pdf, (bytes, bytearray)):
            stream = io.BytesIO(archivo_pdf)
        else:
            return "Error: Formato de archivo no válido para lectura en memoria.", {}

        reader = PdfReader(stream)
        num_paginas = len(reader.pages)
        
        if num_paginas == 0:
            return "Error: El archivo PDF no contiene páginas legibles.", {}

        paginas_texto = []
        texto_acumulado = []

        for idx, pagina in enumerate(reader.pages, start=1):
            texto_pag = pagina.extract_text() or ""
            texto_limpio = texto_pag.strip()
            paginas_texto.append({
                "numero": idx,
                "texto": texto_limpio,
                "caracteres": len(texto_limpio)
            })
            if texto_limpio:
                texto_acumulado.append(f"--- Página {idx} ---\n{texto_limpio}")

        texto_completo = "\n\n".join(texto_acumulado).strip()

        if not texto_completo:
            return (
                "Error: No se pudo extraer texto seleccionable del documento. "
                "El PDF podría consistir únicamente en imágenes escaneadas sin capa OCR o estar protegido.",
                {"paginas": num_paginas, "texto_valido": False}
            )

        palabras_totales = len(texto_completo.split())
        # Estimación aproximada de tokens (1 token ≈ 4 caracteres / ~0.75 palabras)
        tokens_estimados = int(len(texto_completo) / 3.8)

        metadatos = {
            "paginas": num_paginas,
            "palabras": palabras_totales,
            "caracteres": len(texto_completo),
            "tokens_estimados": max(tokens_estimados, palabras_totales),
            "texto_valido": True,
            "paginas_detalle": paginas_texto
        }

        return texto_completo, metadatos

    except Exception as e:
        return f"Error crítico al procesar el archivo PDF con PyPDF2: {str(e)}", {"texto_valido": False}

