import streamlit as st

# -------------------------------------------------
# CONFIGURACIÓN GENERAL
# -------------------------------------------------

st.set_page_config(
    page_title="THE SCENE",
    page_icon="🎬",
    layout="centered"
)

# -------------------------------------------------
# ESTADO DE LA APP
# -------------------------------------------------

if "pantalla" not in st.session_state:
    st.session_state.pantalla = "inicio"

if "diagnostico" not in st.session_state:
    st.session_state.diagnostico = 0

if "decision" not in st.session_state:
    st.session_state.decision = None


# -------------------------------------------------
# FUNCIONES DE NAVEGACIÓN
# -------------------------------------------------

def ir_a(pantalla):
    st.session_state.pantalla = pantalla
    st.rerun()


# -------------------------------------------------
# PANTALLA 1: INICIO
# -------------------------------------------------

if st.session_state.pantalla == "inicio":

    st.title("🎬 THE SCENE")

    st.subheader("Desarrollo de habilidades directivas mediante decisiones y consecuencias")

    st.write(
        """
        **Enter the scene. Make the decision. Face the outcome.**

        THE SCENE es una experiencia de simulación que te coloca dentro de
        situaciones laborales donde tendrás que tomar decisiones.

        No buscamos una respuesta perfecta.

        Queremos observar **cómo decides cuando la situación se complica**.
        """
    )

    st.divider()

    st.write("### ¿Qué vas a hacer?")

    st.write(
        """
        1. Realizar un diagnóstico inicial.
        2. Entrar a una situación de trabajo.
        3. Tomar una decisión.
        4. Observar sus consecuencias.
        5. Recibir retroalimentación.
        6. Conocer tu Huella Directiva.
        """
    )

    if st.button("Comenzar", type="primary", use_container_width=True):
        ir_a("diagnostico")


# -------------------------------------------------
# PANTALLA 2: DIAGNÓSTICO
# -------------------------------------------------

elif st.session_state.pantalla == "diagnostico":

    st.title("Diagnóstico inicial")

    st.write(
        """
        Antes de entrar a THE SCENE queremos conocer cómo percibes actualmente
        tu forma de comunicarte y manejar situaciones difíciles.

        Responde del **1 al 5**:

        **1 = Casi nunca**  
        **5 = Casi siempre**
        """
    )

    p1 = st.slider(
        "1. Escucho la opinión de otras personas antes de responder.",
        1, 5, 3
    )

    p2 = st.slider(
        "2. Puedo explicar una decisión difícil con claridad y respeto.",
        1, 5, 3
    )

    p3 = st.slider(
        "3. Mantengo la calma cuando alguien no está de acuerdo conmigo.",
        1, 5, 3
    )

    p4 = st.slider(
        "4. Busco comprender los intereses de ambas partes en un conflicto.",
        1, 5, 3
    )

    p5 = st.slider(
        "5. Soy capaz de decir que no sin tratar mal a la otra persona.",
        1, 5, 3
    )

    p6 = st.slider(
        "6. Reconozco cuando mi forma de comunicarme afecta al equipo.",
        1, 5, 3
    )

    if st.button("Guardar diagnóstico y continuar", type="primary", use_container_width=True):

        promedio = (p1 + p2 + p3 + p4 + p5 + p6) / 6

        st.session_state.diagnostico = round(promedio, 1)

        ir_a("scene")


# -------------------------------------------------
# PANTALLA 3: LA CONTRAOFERTA
# -------------------------------------------------

elif st.session_state.pantalla == "scene":

    st.caption("THE SCENE #014")

    st.title("La Contraoferta")

    st.info(
        """
        **Tu papel:** Responsable de un equipo

        Una colaboradora con muy buenos resultados te informa que recibió una
        oferta de otra empresa.

        Le gustaría quedarse, pero espera una mejora salarial.

        Al mismo tiempo, Dirección acaba de pedirte reducir **10% el presupuesto
        de tu área**.

        Tienes que hablar con ella y tomar una decisión.
        """
    )

    st.write("### Tu objetivo")

    st.write(
        """
        Mantener la confianza, escuchar a la colaboradora y buscar una solución
        responsable **sin prometer algo que no puedes cumplir**.
        """
    )

    st.divider()

    st.write("### ¿Qué haces?")

    decision = st.radio(
        "Selecciona una decisión:",
        [
            "Prometo un aumento inmediato para evitar que se vaya.",
            "Le digo que no hay presupuesto y termino la conversación.",
            "Escucho sus motivos, explico el límite y busco alternativas reales."
        ],
        index=None
    )

    if st.button("Tomar decisión", type="primary", use_container_width=True):

        if decision is None:
            st.warning("Primero selecciona una decisión.")

        else:
            st.session_state.decision = decision
            ir_a("resultado")


# -------------------------------------------------
# PANTALLA 4: RESULTADO
# -------------------------------------------------

elif st.session_state.pantalla == "resultado":

    st.title("Resultado de tu decisión")

    decision = st.session_state.decision

    # OPCIÓN 1
    if decision == "Prometo un aumento inmediato para evitar que se vaya.":

        st.error("La colaboradora se tranquiliza... por ahora.")

        st.write(
            """
            Le aseguras que encontrarás la forma de conseguir el aumento.

            La conversación termina bien, pero existe un problema:
            **todavía no tienes autorización para cumplir esa promesa**.

            Si después no puedes cumplirla, la confianza puede disminuir aún más.
            """
        )

        comunicacion = 3
        decisiones = 2
        estrategia = 2
        etica = 2

        retro = (
            "Lograste reducir la tensión del momento, pero asumiste un compromiso "
            "que todavía no depende completamente de ti."
        )

    # OPCIÓN 2
    elif decision == "Le digo que no hay presupuesto y termino la conversación.":

        st.warning("La respuesta es clara, pero la conversación termina fría.")

        st.write(
            """
            Explicas que no existe presupuesto disponible y das por terminado
            el tema.

            Fuiste directo, pero la colaboradora siente que su situación no fue
            realmente escuchada.

            Podría continuar buscando otra oportunidad.
            """
        )

        comunicacion = 2
        decisiones = 3
        estrategia = 2
        etica = 4

        retro = (
            "Fuiste honesto respecto a las restricciones, pero faltó escuchar "
            "antes de cerrar la conversación."
        )

    # OPCIÓN 3
    else:

        st.success("La conversación abre una negociación más honesta.")

        st.write(
            """
            Escuchas por qué la oferta es importante para ella.

            Después explicas que actualmente existen restricciones de presupuesto
            y que no puedes prometer un aumento sin autorización.

            Juntos comienzan a revisar alternativas reales.

            Esto **no garantiza que la colaboradora se quede**, pero mantiene
            abierta una conversación basada en confianza y transparencia.
            """
        )

        comunicacion = 5
        decisiones = 4
        estrategia = 4
        etica = 5

        retro = (
            "Escuchaste antes de responder, explicaste el límite con claridad "
            "y evitaste prometer algo que todavía no puedes cumplir."
        )

    st.divider()

    st.write("### Retroalimentación")

    st.write(retro)

    st.write(
        """
        En THE SCENE una decisión no se considera simplemente
        **correcta o incorrecta**.

        También observamos sus consecuencias y el contexto en el que fue tomada.
        """
    )

    if st.button("Ver mi Huella Directiva", type="primary", use_container_width=True):

        st.session_state.comunicacion = comunicacion
        st.session_state.decisiones = decisiones
        st.session_state.estrategia = estrategia
        st.session_state.etica = etica

        ir_a("huella")


# -------------------------------------------------
# PANTALLA 5: HUELLA DIRECTIVA
# -------------------------------------------------

elif st.session_state.pantalla == "huella":

    st.title("Tu Huella Directiva")

    st.write(
        """
        La Huella Directiva reúne patrones observados en tus decisiones.

        Una sola Scene puede mostrar información sobre **varias habilidades
        directivas al mismo tiempo**.
        """
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Comunicación e influencia",
            f"{st.session_state.comunicacion}/5"
        )

        st.metric(
            "Pensamiento estratégico",
            f"{st.session_state.estrategia}/5"
        )

    with col2:

        st.metric(
            "Toma de decisiones",
            f"{st.session_state.decisiones}/5"
        )

        st.metric(
            "Liderazgo ético",
            f"{st.session_state.etica}/5"
        )

    st.divider()

    st.write("### Autopercepción inicial")

    st.metric(
        "Promedio del diagnóstico",
        f"{st.session_state.diagnostico}/5"
    )

    promedio_real = round(
        (
            st.session_state.comunicacion
            + st.session_state.decisiones
            + st.session_state.estrategia
            + st.session_state.etica
        ) / 4,
        1
    )

    st.write("### Desempeño observado")

    st.metric(
        "Promedio dentro de la Scene",
        f"{promedio_real}/5"
    )

    diferencia = round(st.session_state.diagnostico - promedio_real, 1)

    st.divider()

    st.write("### Posible punto ciego")

    if diferencia >= 0.7:

        st.warning(
            """
            Tu autopercepción fue más alta que tu desempeño dentro de esta Scene.

            Esto no significa que seas un mal líder. Puede indicar que existe una
            diferencia entre **cómo crees que reaccionarías y cómo decides cuando
            existe presión**.
            """
        )

    elif diferencia <= -0.7:

        st.success(
            """
            Tu desempeño en esta Scene fue superior a tu propia autopercepción.

            Es posible que tengas habilidades que actualmente estás
            subestimando.
            """
        )

    else:

        st.info(
            """
            Tu autopercepción y tu desempeño observado fueron relativamente
            similares.
            """
        )

    st.write("### Siguiente práctica recomendada")

    if st.session_state.comunicacion <= 3:

        st.write(
            "Practicar escucha activa antes de proponer una solución."
        )

    elif st.session_state.estrategia <= 3:

        st.write(
            "Practicar decisiones considerando consecuencias de corto y largo plazo."
        )

    elif st.session_state.decisiones <= 3:

        st.write(
            "Practicar decisiones con información incompleta y recursos limitados."
        )

    else:

        st.write(
            "Continuar con escenarios más complejos que combinen varias habilidades."
        )

    st.divider()

    col_a, col_b = st.columns(2)

    with col_a:

        if st.button("🔄 Replay", use_container_width=True):

            st.session_state.decision = None
            ir_a("scene")

    with col_b:

        if st.button("🏠 Volver al inicio", use_container_width=True):

            st.session_state.pantalla = "inicio"
            st.session_state.decision = None
            st.rerun()