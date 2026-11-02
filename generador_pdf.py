
from io import BytesIO
from html import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepTogether
)

from tecnicas_estudio import TECNICAS


# ==========================================
# COLORES UNIPREP MX
# ==========================================

AZUL_MARINO = colors.HexColor("#102A56")
AZUL = colors.HexColor("#2563EB")
AZUL_CLARO = colors.HexColor("#EAF2FF")
GRIS = colors.HexColor("#64748B")
BLANCO = colors.white


# ==========================================
# PIE DE PÁGINA
# ==========================================

def dibujar_pie_pagina(canvas, doc):

    canvas.saveState()

    ancho, alto = A4

    canvas.setStrokeColor(
        colors.HexColor("#DFE7F3")
    )

    canvas.line(
        2 * cm,
        1.6 * cm,
        ancho - 2 * cm,
        1.6 * cm
    )

    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(GRIS)

    canvas.drawString(
        2 * cm,
        1.2 * cm,
        "UniPrep MX | Study Planner"
    )

    canvas.drawRightString(
        ancho - 2 * cm,
        1.2 * cm,
        f"Página {doc.page}"
    )

    canvas.restoreState()


# ==========================================
# GENERADOR DEL DOCUMENTO PDF
# ==========================================

def crear_pdf(plan, nombre):

    buffer = BytesIO()

    documento = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2.2 * cm
    )

    estilos = getSampleStyleSheet()

    estilos.add(
        ParagraphStyle(
            name="TituloUniPrep",
            parent=estilos["Title"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=27,
            textColor=AZUL_MARINO,
            alignment=TA_CENTER,
            spaceAfter=14
        )
    )

    estilos.add(
        ParagraphStyle(
            name="SubtituloUniPrep",
            parent=estilos["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=18,
            textColor=AZUL_MARINO,
            spaceBefore=12,
            spaceAfter=8
        )
    )

    estilos.add(
        ParagraphStyle(
            name="TextoUniPrep",
            parent=estilos["BodyText"],
            fontName="Helvetica",
            fontSize=10,
            leading=15,
            spaceAfter=7
        )
    )

    estilos.add(
        ParagraphStyle(
            name="TablaUniPrep",
            parent=estilos["BodyText"],
            fontName="Helvetica",
            fontSize=9,
            leading=13
        )
    )

    estilos.add(
        ParagraphStyle(
            name="EncabezadoTablaUniPrep",
            parent=estilos["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=9,
            leading=13,
            textColor=BLANCO
        )
    )

    contenido = []

    # ==========================================
    # PORTADA / ENCABEZADO
    # ==========================================

    contenido.append(
        Paragraph(
            "UNIPREP MX",
            estilos["TituloUniPrep"]
        )
    )

    contenido.append(
        Paragraph(
            "Calendario personalizado de estudio",
            estilos["SubtituloUniPrep"]
        )
    )

    contenido.append(
        Spacer(1, 0.3 * cm)
    )

    # ==========================================
    # INFORMACIÓN DEL ESTUDIANTE
    # ==========================================

    datos_estudiante = [
        ("Estudiante", nombre),
        ("Objetivo", plan["objetivo"]),
        ("Materias", ", ".join(plan["materias"])),
        ("Días de estudio", str(plan["dias"])),
        (
            "Tiempo diario",
            f"{plan['minutos']} minutos"
        ),
        (
            "Horas semanales",
            f"{plan['horas_semanales']} horas"
        )
    ]

    for etiqueta, valor in datos_estudiante:

        contenido.append(
            Paragraph(
                f"<b>{escape(etiqueta)}:</b> "
                f"{escape(str(valor))}",
                estilos["TextoUniPrep"]
            )
        )

    contenido.append(
        Spacer(1, 0.4 * cm)
    )

    # ==========================================
    # CALENDARIO SEMANAL
    # ==========================================

    contenido.append(
        Paragraph(
            "Calendario semanal",
            estilos["SubtituloUniPrep"]
        )
    )

    for dia in plan["calendario"]:

        bloque_dia = []

        bloque_dia.append(
            Paragraph(
                escape(dia["dia"]),
                estilos["SubtituloUniPrep"]
            )
        )

        datos_tabla = [
            [
                Paragraph(
                    "Materia",
                    estilos["EncabezadoTablaUniPrep"]
                ),
                Paragraph(
                    "Duración",
                    estilos["EncabezadoTablaUniPrep"]
                ),
                Paragraph(
                    "Técnicas recomendadas",
                    estilos["EncabezadoTablaUniPrep"]
                )
            ]
        ]

        for sesion in dia["sesiones"]:

            nombres = ", ".join(
                tecnica["nombre"]
                for tecnica in sesion["tecnicas"]
            )

            datos_tabla.append(
                [
                    Paragraph(
                        escape(sesion["materia"]),
                        estilos["TablaUniPrep"]
                    ),
                    Paragraph(
                        f"{sesion['duracion']} min",
                        estilos["TablaUniPrep"]
                    ),
                    Paragraph(
                        escape(nombres),
                        estilos["TablaUniPrep"]
                    )
                ]
            )

        tabla = Table(
            datos_tabla,
            colWidths=[
                4.2 * cm,
                2.4 * cm,
                9.4 * cm
            ],
            repeatRows=1,
            hAlign="LEFT"
        )

        tabla.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        AZUL_MARINO
                    ),
                    (
                        "ROWBACKGROUNDS",
                        (0, 1),
                        (-1, -1),
                        [BLANCO, AZUL_CLARO]
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP"
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        9
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        9
                    ),
                    (
                        "LINEBELOW",
                        (0, 0),
                        (-1, 0),
                        1,
                        AZUL
                    )
                ]
            )
        )

        bloque_dia.append(tabla)
        bloque_dia.append(Spacer(1, 0.3 * cm))

        contenido.append(
            KeepTogether(bloque_dia)
        )

    # ==========================================
    # TÉCNICAS ÚNICAS RECOMENDADAS
    # ==========================================

    contenido.append(
        Spacer(1, 0.4 * cm)
    )

    contenido.append(
        Paragraph(
            "Guía de técnicas de estudio",
            estilos["SubtituloUniPrep"]
        )
    )

    tecnicas_unicas = {}

    for dia in plan["calendario"]:

        for sesion in dia["sesiones"]:

            for tecnica in sesion["tecnicas"]:

                nombre_tecnica = tecnica["nombre"]

                if nombre_tecnica not in tecnicas_unicas:

                    tecnicas_unicas[nombre_tecnica] = (
                        tecnica["descripcion"]
                    )

    # ==========================================
    # EXPLICACIÓN DE CADA TÉCNICA
    # ==========================================

    for nombre_tecnica, descripcion in tecnicas_unicas.items():

        informacion = TECNICAS.get(nombre_tecnica)

        contenido.append(
            Paragraph(
                escape(nombre_tecnica),
                estilos["SubtituloUniPrep"]
            )
        )

        contenido.append(
            Paragraph(
                escape(descripcion),
                estilos["TextoUniPrep"]
            )
        )

        if informacion:

            contenido.append(
                Paragraph(
                    "<b>Cómo aplicarla:</b>",
                    estilos["TextoUniPrep"]
                )
            )

            for numero, paso in enumerate(
                informacion["pasos"],
                start=1
            ):

                contenido.append(
                    Paragraph(
                        f"{numero}. {escape(paso)}",
                        estilos["TextoUniPrep"]
                    )
                )

            contenido.append(
                Paragraph(
                    "<b>Ejemplo práctico:</b> "
                    + escape(informacion["ejemplo"]),
                    estilos["TextoUniPrep"]
                )
            )

            contenido.append(
                Paragraph(
                    "<b>Error frecuente:</b> "
                    + escape(informacion["error"]),
                    estilos["TextoUniPrep"]
                )
            )

        contenido.append(
            Spacer(1, 0.3 * cm)
        )

    # ==========================================
    # CONSTRUIR PDF
    # ==========================================

    documento.build(
        contenido,
        onFirstPage=dibujar_pie_pagina,
        onLaterPages=dibujar_pie_pagina
    )

    pdf_bytes = buffer.getvalue()

    buffer.close()

    return pdf_bytes
