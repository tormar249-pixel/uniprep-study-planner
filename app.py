import streamlit as st
from recomendador import generar_plan
from generador_pdf import crear_pdf
from tecnicas_estudio import TECNICAS
from estilos import aplicar_estilos


# Configuración de la aplicación
st.set_page_config(
    page_title="UniPrep Study Planner",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 UniPrep Study Planner")
st.caption("Tu asistente personalizado de aprendizaje")

# ====================================
# FORMULARIO DEL ESTUDIANTE
# ====================================

with st.form("diagnostico"):

    st.subheader("📋 Diagnóstico académico")

    nombre = st.text_input("Nombre del estudiante")

    objetivo = st.selectbox(
        "¿Cuál es tu objetivo?",
        [
            "Prepararme para un examen",
            "Mejorar mis calificaciones",
            "Aprender una habilidad nueva"
        ]
    )

    materias = st.multiselect(
        "Selecciona las materias que deseas estudiar",
        [
            "Matemáticas",
            "Física",
            "Química",
            "Biología",
            "Historia",
            "Geografía",
            "Español",
            "Programación",
            "Cálculo",
            "Álgebra lineal"
        ]
    )

    dificultad = st.selectbox(
        "¿Cuál es tu principal dificultad al estudiar?",
        [
            "Concentrarme",
            "Recordar información",
            "Entender los temas",
            "Resolver ejercicios"
        ]
    )

    minutos = st.select_slider(
        "¿Cuántos minutos puedes estudiar al día?",
        options=[30, 45, 60, 90, 120, 150, 180],
        value=60
    )

    dias = st.multiselect(
        "¿Qué días puedes estudiar?",
        [
            "Lunes",
            "Martes",
            "Miércoles",
            "Jueves",
            "Viernes",
            "Sábado",
            "Domingo"
        ],
        default=["Lunes", "Miércoles", "Viernes"]
    )

    enviar = st.form_submit_button(
        "✨ Generar mi plan personalizado",
        use_container_width=True
    )

# ====================================
# GENERAR PLAN
# ====================================

if enviar:

    if not nombre.strip():
        st.warning("Por favor, escribe tu nombre.")

    elif not materias:
        st.warning("Selecciona al menos una materia.")

    elif not dias:
        st.warning("Selecciona al menos un día.")

    else:

        plan = generar_plan(
            objetivo,
            dificultad,
            materias,
            minutos,
            dias
        )

        st.session_state["plan"] = plan
        st.session_state["nombre"] = nombre

# ====================================
# MOSTRAR RESULTADOS
# ====================================

if "plan" in st.session_state:

    plan = st.session_state["plan"]
    nombre_alumno = st.session_state["nombre"]

    st.divider()

    st.success(f"¡Tu plan está listo, {nombre_alumno}!")

    st.subheader("📊 Resumen de tu plan")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Horas por semana",
        plan["horas_semanales"]
    )

    col2.metric(
        "Materias",
        len(plan["materias"])
    )

    col3.metric(
        "Días de estudio",
        plan["dias"]
    )

    # ====================================
    # CALENDARIO SEMANAL
    # ====================================

    st.subheader("📅 Calendario semanal")

    for dia in plan["calendario"]:

        with st.container(border=True):

            st.markdown(f"### 📆 {dia['dia']}")

            for sesion in dia["sesiones"]:

                st.markdown(
                    f"**📚 {sesion['materia']} — "
                    f"{sesion['duracion']} minutos**"
                )

                st.write("**Técnicas recomendadas:**")

                for tecnica in sesion["tecnicas"]:

                    st.write(
                        f"🧠 {tecnica['nombre']}: "
                        f"{tecnica['descripcion']}"
                    )

                st.divider()

    # ====================================
    # DESCARGAR CALENDARIO
    # ====================================

    resumen = "UNIPREP STUDY PLANNER\n\n"

    resumen += f"Estudiante: {nombre_alumno}\n"
    resumen += f"Objetivo: {plan['objetivo']}\n"
    resumen += f"Materias: {', '.join(plan['materias'])}\n"
    resumen += f"Horas semanales: {plan['horas_semanales']}\n\n"

    resumen += "CALENDARIO SEMANAL\n\n"

    for dia in plan["calendario"]:

        resumen += f"{dia['dia']}:\n"

        for sesion in dia["sesiones"]:

            resumen += (
                f"  - {sesion['materia']}: "
                f"{sesion['duracion']} minutos\n"
            )

            for tecnica in sesion["tecnicas"]:
                resumen += f"    Técnica: {tecnica['nombre']}\n"

        resumen += "\n"


    # ====================================
    # GUÍA DE TÉCNICAS DE ESTUDIO
    # ====================================

    st.subheader("🧠 Aprende a utilizar tus técnicas")

    nombres_tecnicas = []

    for dia in plan["calendario"]:
        for sesion in dia["sesiones"]:
            for tecnica in sesion["tecnicas"]:
                nombre_tecnica = tecnica["nombre"]

                if nombre_tecnica not in nombres_tecnicas:
                    nombres_tecnicas.append(nombre_tecnica)

    for nombre_tecnica in nombres_tecnicas:

        if nombre_tecnica not in TECNICAS:
            continue

        informacion = TECNICAS[nombre_tecnica]

        with st.expander(f"📖 Cómo utilizar {nombre_tecnica}"):

            st.write(informacion["explicacion"])

            st.markdown("**Pasos para aplicarla:**")

            for numero, paso in enumerate(
                informacion["pasos"], start=1
            ):
                st.write(f"{numero}. {paso}")

            st.markdown("**Ejemplo práctico:**")
            st.info(informacion["ejemplo"])

            st.markdown("**Error frecuente:**")
            st.warning(informacion["error"])


    # ====================================
    # DESCARGAR CALENDARIO EN PDF
    # ====================================

    archivo_pdf = crear_pdf(
        plan,
        nombre_alumno
    )

    st.download_button(
        label="📄 Descargar mi calendario en PDF",
        data=archivo_pdf,
        file_name="Calendario_UniPrep.pdf",
        mime="application/pdf",
        use_container_width=True
    )
