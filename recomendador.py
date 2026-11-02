
def recomendar_tecnicas(dificultad, materia):
    tecnicas = []

    if dificultad == "Concentrarme":
        tecnicas.append({
            "nombre": "Pomodoro",
            "descripcion": "Estudia en bloques de concentración con descansos breves."
        })

    elif dificultad == "Recordar información":
        tecnicas.append({
            "nombre": "Recuperación activa",
            "descripcion": "Intenta recordar lo aprendido sin consultar tus apuntes."
        })
        tecnicas.append({
            "nombre": "Repetición espaciada",
            "descripcion": "Repasa los temas en distintos días para mejorar la retención."
        })

    elif dificultad == "Entender los temas":
        tecnicas.append({
            "nombre": "Técnica Feynman",
            "descripcion": "Explica el tema con tus propias palabras y detecta lo que no comprendes."
        })

    else:
        tecnicas.append({
            "nombre": "Práctica intercalada",
            "descripcion": "Combina diferentes tipos de ejercicios para aprender a distinguir métodos."
        })

    if materia in ["Matemáticas", "Física", "Programación"]:
        tecnicas.append({
            "nombre": "Práctica de problemas",
            "descripcion": "Resuelve ejercicios nuevos y revisa tus errores."
        })
    else:
        tecnicas.append({
            "nombre": "Autoevaluación",
            "descripcion": "Responde preguntas sin consultar el material."
        })

    return tecnicas




def generar_plan(objetivo, dificultad, materias, minutos, dias):

    calendario = []

    # Número de bloques de estudio por día
    bloques = max(1, minutos // 45)

    # Evita dividir el tiempo en bloques demasiado pequeños
    bloques = min(bloques, len(materias))

    indice_materia = 0

    for dia in dias:

        sesiones = []

        tiempo_base = minutos // bloques
        sobrante = minutos % bloques

        for i in range(bloques):

            materia = materias[indice_materia % len(materias)]

            duracion = tiempo_base
            if i < sobrante:
                duracion += 1

            sesiones.append({
                "materia": materia,
                "duracion": duracion,
                "tecnicas": recomendar_tecnicas(
                    dificultad, materia
                )
            })

            indice_materia += 1

        calendario.append({
            "dia": dia,
            "sesiones": sesiones
        })

    return {
        "objetivo": objetivo,
        "materias": materias,
        "calendario": calendario,
        "minutos": minutos,
        "dias": len(dias),
        "horas_semanales": round(
            minutos * len(dias) / 60, 1
        )
    }
