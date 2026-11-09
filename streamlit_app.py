import streamlit as st
import os

# =========================================================
# CONFIGURACIÓN GENERAL
# =========================================================

st.set_page_config(
    page_title="THE SCENE",
    page_icon="🎬",
    layout="centered"
)

# =========================================================
# ESTILO VISUAL
# =========================================================

st.markdown("""
<style>

.block-container {
    max-width: 920px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

h1 {
    font-size: 42px !important;
    font-weight: 800 !important;
}

h2, h3 {
    font-weight: 700 !important;
}

.main-title {
    font-size: 56px;
    font-weight: 900;
    margin-bottom: 0px;
}

.subtitle {
    font-size: 20px;
    color: #555555;
    margin-bottom: 28px;
}

.names {
    color: #777777;
    font-size: 14px;
    margin-top: -18px;
    margin-bottom: 25px;
}

.scene-box {
    background-color: #f6f6f8;
    padding: 24px;
    border-radius: 14px;
    border: 1px solid #e4e4e7;
    margin-bottom: 20px;
}

.skill-card {
    background-color: #fafafa;
    padding: 16px;
    border-radius: 12px;
    border: 1px solid #e7e7e7;
    text-align: center;
    min-height: 115px;
}

.small-text {
    color: #6c6c6c;
    font-size: 13px;
}

.scene-number {
    color: #777777;
    font-size: 13px;
    font-weight: 600;
}

.ai-box {
    background-color: #f1f5ff;
    padding: 20px;
    border-radius: 12px;
    border-left: 5px solid #5874d8;
    margin-top: 15px;
    margin-bottom: 15px;
}

.result-box {
    background-color: #fafafa;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #e5e5e5;
    margin-bottom: 18px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HABILIDADES
# =========================================================

HABILIDADES = [
    "Tiempo y priorización",
    "Comunicación e influencia",
    "Creatividad e innovación",
    "Pensamiento estratégico",
    "Toma de decisiones",
    "Liderazgo ético"
]

ICONOS = {
    "Tiempo y priorización": "⏱️",
    "Comunicación e influencia": "💬",
    "Creatividad e innovación": "💡",
    "Pensamiento estratégico": "🧠",
    "Toma de decisiones": "⚖️",
    "Liderazgo ético": "🧭"
}

# =========================================================
# ESTADO DE SESIÓN
# =========================================================

if "pantalla" not in st.session_state:
    st.session_state.pantalla = "inicio"

if "autopercepcion" not in st.session_state:
    st.session_state.autopercepcion = {}

if "resultados_scenes" not in st.session_state:
    st.session_state.resultados_scenes = {}

if "scene_actual" not in st.session_state:
    st.session_state.scene_actual = None

if "mensaje_usuario" not in st.session_state:
    st.session_state.mensaje_usuario = ""

if "reaccion_ia" not in st.session_state:
    st.session_state.reaccion_ia = None


# =========================================================
# FUNCIONES
# =========================================================

def ir_a(pantalla):
    st.session_state.pantalla = pantalla
    st.rerun()


def obtener_api_key():
    try:
        if "OPENAI_API_KEY" in st.secrets:
            return st.secrets["OPENAI_API_KEY"]
    except Exception:
        pass

    return os.getenv("OPENAI_API_KEY")


def generar_reaccion_ia(mensaje):
    api_key = obtener_api_key()

    if not api_key:
        return None

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)

        prompt = f"""
Eres una colaboradora de alto desempeño dentro de una empresa.

Acabas de decirle a tu jefe que recibiste una oferta laboral de otra empresa.
Te gustaría permanecer en tu trabajo actual, pero esperas una mejora salarial.

Tu jefe sabe que Dirección le pidió reducir 10% el presupuesto del área.

El jefe acaba de responderte lo siguiente:

"{mensaje}"

Responde como la colaboradora.

Reglas:
- Responde en español.
- Sé realista y profesional.
- No expliques que eres una inteligencia artificial.
- No evalúes al usuario.
- No digas cuál era la respuesta correcta.
- Reacciona directamente a lo que dijo.
- Muestra emociones razonables como confianza, duda, preocupación o apertura.
- Máximo 90 palabras.
"""

        response = client.responses.create(
            model="gpt-6-luna",
            input=prompt
        )

        return response.output_text

    except Exception:
        return None


def guardar_resultado(scene_id, scores, decision, feedback):
    st.session_state.resultados_scenes[scene_id] = {
        "scores": scores,
        "decision": decision,
        "feedback": feedback
    }


def calcular_desempeno():
    acumulado = {h: [] for h in HABILIDADES}

    for resultado in st.session_state.resultados_scenes.values():
        for habilidad, puntuacion in resultado["scores"].items():
            acumulado[habilidad].append(puntuacion)

    desempeno = {}

    for habilidad in HABILIDADES:
        if acumulado[habilidad]:
            desempeno[habilidad] = round(
                sum(acumulado[habilidad]) /
                len(acumulado[habilidad]),
                1
            )
        else:
            desempeno[habilidad] = None

    return desempeno


def reiniciar_todo():
    st.session_state.pantalla = "inicio"
    st.session_state.autopercepcion = {}
    st.session_state.resultados_scenes = {}
    st.session_state.scene_actual = None
    st.session_state.mensaje_usuario = ""
    st.session_state.reaccion_ia = None
    st.rerun()


# =========================================================
# PANTALLA 1 — INICIO
# =========================================================

if st.session_state.pantalla == "inicio":

    st.markdown(
        '<div class="main-title">🎬 THE SCENE</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Desarrollo de habilidades directivas mediante decisiones y consecuencias.</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="names">
        José Miguel Castellanos · Dulce María Rocha · Ximena Díaz
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="scene-box">

        <b>Enter the scene. Make the decision. Face the outcome.</b>

        <br><br>

        THE SCENE es una experiencia de simulación diseñada para practicar
        habilidades directivas mediante situaciones laborales.

        <br><br>

        El objetivo no es encontrar una respuesta perfecta, sino observar
        <b>cómo decides cuando existen presión, intereses distintos,
        recursos limitados e incertidumbre.</b>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("### Las 6 habilidades directivas")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="skill-card">
            ⏱️<br>
            <b>Tiempo y priorización</b>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="skill-card">
            💬<br>
            <b>Comunicación e influencia</b>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div class="skill-card">
            💡<br>
            <b>Creatividad e innovación</b>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    col4, col5, col6 = st.columns(3)

    with col4:
        st.markdown(
            """
            <div class="skill-card">
            🧠<br>
            <b>Pensamiento estratégico</b>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col5:
        st.markdown(
            """
            <div class="skill-card">
            ⚖️<br>
            <b>Toma de decisiones</b>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col6:
        st.markdown(
            """
            <div class="skill-card">
            🧭<br>
            <b>Liderazgo ético</b>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    st.write("### ¿Cómo funciona?")

    st.write("""
    1. Realizas un diagnóstico inicial.
    2. Obtienes tu perfil de autopercepción.
    3. Entras a tres situaciones de trabajo.
    4. Tomas decisiones.
    5. Observas las consecuencias.
    6. Recibes retroalimentación.
    7. Comparas percepción y comportamiento.
    8. Construyes tu Huella Directiva.
    9. Recibes una práctica recomendada.
    """)

    if st.button(
        "Comenzar experiencia",
        type="primary",
        use_container_width=True
    ):
        ir_a("diagnostico")


# =========================================================
# PANTALLA 2 — DIAGNÓSTICO
# =========================================================

elif st.session_state.pantalla == "diagnostico":

    st.title("Diagnóstico inicial")

    st.markdown(
        """
        <div class="scene-box">

        Antes de entrar a las simulaciones queremos conocer
        <b>cómo percibes actualmente tus propias habilidades directivas.</b>

        <br><br>

        Responde cada afirmación del 1 al 5.

        <br><br>

        <b>1 = Casi nunca</b><br>
        <b>5 = Casi siempre</b>

        <br><br>

        Este diagnóstico es orientativo y no corresponde a una prueba
        psicométrica validada.

        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("### ⏱️ Tiempo y priorización")

    t1 = st.slider(
        "1. Distingo entre lo urgente y lo realmente importante.",
        1, 5, 3
    )

    t2 = st.slider(
        "2. Sé cuándo realizar una tarea personalmente y cuándo delegarla.",
        1, 5, 3
    )

    st.divider()

    st.write("### 💬 Comunicación e influencia")

    c1 = st.slider(
        "3. Escucho la opinión de otras personas antes de responder.",
        1, 5, 3
    )

    c2 = st.slider(
        "4. Puedo comunicar una decisión difícil con claridad y respeto.",
        1, 5, 3
    )

    st.divider()

    st.write("### 💡 Creatividad e innovación")

    cr1 = st.slider(
        "5. Antes de elegir una solución considero diferentes alternativas.",
        1, 5, 3
    )

    cr2 = st.slider(
        "6. Puedo cambiar de enfoque cuando una solución no está funcionando.",
        1, 5, 3
    )

    st.divider()

    st.write("### 🧠 Pensamiento estratégico")

    e1 = st.slider(
        "7. Antes de decidir considero las posibles consecuencias a futuro.",
        1, 5, 3
    )

    e2 = st.slider(
        "8. Intento comprender el panorama completo antes de enfocarme en un solo problema.",
        1, 5, 3
    )

    st.divider()

    st.write("### ⚖️ Toma de decisiones")

    d1 = st.slider(
        "9. Puedo tomar una decisión aunque no tenga toda la información.",
        1, 5, 3
    )

    d2 = st.slider(
        "10. Asumo responsabilidad por las decisiones que tomo.",
        1, 5, 3
    )

    st.divider()

    st.write("### 🧭 Liderazgo ético")

    l1 = st.slider(
        "11. Considero cómo mis decisiones pueden afectar a otras personas.",
        1, 5, 3
    )

    l2 = st.slider(
        "12. Evito prometer algo que probablemente no podré cumplir.",
        1, 5, 3
    )

    if st.button(
        "Guardar diagnóstico",
        type="primary",
        use_container_width=True
    ):

        st.session_state.autopercepcion = {
            "Tiempo y priorización": round((t1 + t2) / 2, 1),
            "Comunicación e influencia": round((c1 + c2) / 2, 1),
            "Creatividad e innovación": round((cr1 + cr2) / 2, 1),
            "Pensamiento estratégico": round((e1 + e2) / 2, 1),
            "Toma de decisiones": round((d1 + d2) / 2, 1),
            "Liderazgo ético": round((l1 + l2) / 2, 1)
        }

        ir_a("perfil")


# =========================================================
# PANTALLA 3 — PERFIL INICIAL
# =========================================================

elif st.session_state.pantalla == "perfil":

    st.title("Tu perfil inicial")

    st.write("""
    Este resultado representa **cómo percibes actualmente tus propias
    habilidades directivas**.

    Más adelante compararemos esta percepción con las decisiones que
    tomes dentro de THE SCENE.
    """)

    st.divider()

    aut = st.session_state.autopercepcion

    col1, col2 = st.columns(2)

    with col1:

        for habilidad in [
            "Tiempo y priorización",
            "Creatividad e innovación",
            "Toma de decisiones"
        ]:

            st.metric(
                f"{ICONOS[habilidad]} {habilidad}",
                f"{aut[habilidad]}/5"
            )

            st.progress(aut[habilidad] / 5)

    with col2:

        for habilidad in [
            "Comunicación e influencia",
            "Pensamiento estratégico",
            "Liderazgo ético"
        ]:

            st.metric(
                f"{ICONOS[habilidad]} {habilidad}",
                f"{aut[habilidad]}/5"
            )

            st.progress(aut[habilidad] / 5)

    st.info(
        """
        Este resultado no representa todavía tu desempeño.

        La Huella Directiva se construirá comparando lo que crees que
        harías con lo que realmente decides dentro de las simulaciones.
        """
    )

    if st.button(
        "Entrar a THE SCENE",
        type="primary",
        use_container_width=True
    ):
        ir_a("menu_scenes")


# =========================================================
# PANTALLA 4 — MENÚ DE SCENES
# =========================================================

elif st.session_state.pantalla == "menu_scenes":

    st.title("Selecciona una Scene")

    completadas = st.session_state.resultados_scenes

    st.write(
        "Cada situación pone a prueba distintas habilidades al mismo tiempo."
    )

    st.divider()

    # SCENE 1
    st.write("### 🎬 Scene #014 — La Contraoferta")

    st.write(
        "Una colaboradora clave recibió otra oferta laboral mientras tu área enfrenta una reducción de presupuesto."
    )

    if "scene1" in completadas:
        st.success("Scene completada")

    if st.button(
        "Entrar a La Contraoferta",
        use_container_width=True
    ):
        st.session_state.scene_actual = "scene1"
        st.session_state.reaccion_ia = None
        ir_a("scene1")

    st.divider()

    # SCENE 2
    st.write("### ⏱️ Scene #021 — Todo es urgente")

    st.write(
        "Varias tareas importantes llegan al mismo tiempo y tienes que decidir qué atender, qué programar y qué delegar."
    )

    if "scene2" in completadas:
        st.success("Scene completada")

    if st.button(
        "Entrar a Todo es urgente",
        use_container_width=True
    ):
        st.session_state.scene_actual = "scene2"
        ir_a("scene2")

    st.divider()

    # SCENE 3
    st.write("### 💡 Scene #032 — El proceso ya no funciona")

    st.write(
        "Un proceso interno está provocando retrasos y debes decidir cómo mejorarlo con recursos limitados."
    )

    if "scene3" in completadas:
        st.success("Scene completada")

    if st.button(
        "Entrar a El proceso ya no funciona",
        use_container_width=True
    ):
        st.session_state.scene_actual = "scene3"
        ir_a("scene3")

    st.divider()

    if len(completadas) == 3:

        st.success(
            "Has completado las tres Scenes. Tu Huella Directiva está lista."
        )

        if st.button(
            "Ver mi Huella Directiva",
            type="primary",
            use_container_width=True
        ):
            ir_a("huella")


# =========================================================
# SCENE 1 — LA CONTRAOFERTA
# =========================================================

elif st.session_state.pantalla == "scene1":

    st.markdown(
        '<div class="scene-number">THE SCENE #014</div>',
        unsafe_allow_html=True
    )

    st.title("La Contraoferta")

    st.markdown(
        """
        <div class="scene-box">

        <b>Tu papel:</b> Responsable de un equipo.

        <br><br>

        Una de tus colaboradoras con mejores resultados te informa que
        recibió una oferta de otra empresa.

        <br><br>

        Te dice que preferiría quedarse, pero espera una mejora salarial.

        <br><br>

        Al mismo tiempo, Dirección acaba de pedir una reducción del
        <b>10% del presupuesto de tu área.</b>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("### ¿Qué haces?")

    decision = st.radio(
        "Selecciona una decisión:",
        [
            "Le prometo un aumento inmediato para evitar que se vaya.",
            "Le digo que no hay presupuesto y cierro la conversación.",
            "Escucho sus motivos, explico la situación y busco alternativas reales."
        ],
        index=None
    )

    st.write("### ¿Qué le dirías?")

    mensaje = st.text_area(
        "Escribe brevemente cómo hablarías con la colaboradora:",
        placeholder="Ejemplo: Entiendo tu situación y quiero conocer mejor qué estás buscando..."
    )

    if st.button(
        "Tomar decisión",
        type="primary",
        use_container_width=True
    ):

        if decision is None:
            st.warning("Selecciona una decisión antes de continuar.")

        elif not mensaje.strip():
            st.warning("Escribe brevemente qué le dirías.")

        else:

            st.session_state.decision_scene1 = decision
            st.session_state.mensaje_usuario = mensaje
            st.session_state.reaccion_ia = None

            ir_a("resultado_scene1")


# =========================================================
# RESULTADO SCENE 1
# =========================================================

elif st.session_state.pantalla == "resultado_scene1":

    st.title("Consecuencia")

    decision = st.session_state.decision_scene1

    if decision == "Le prometo un aumento inmediato para evitar que se vaya.":

        st.error("La colaboradora se tranquiliza... por ahora.")

        st.write("""
        La conversación termina con cierta tranquilidad.

        Sin embargo, todavía no tienes autorización para cumplir la promesa.

        Si después no logras conseguir el aumento, la confianza puede disminuir.
        """)

        scores = {
            "Comunicación e influencia": 3,
            "Pensamiento estratégico": 2,
            "Toma de decisiones": 2,
            "Liderazgo ético": 2
        }

        feedback = (
            "Redujiste la tensión inmediata, pero asumiste un compromiso "
            "que todavía no depende completamente de ti."
        )

    elif decision == "Le digo que no hay presupuesto y cierro la conversación.":

        st.warning("La respuesta es clara, pero la conversación termina fría.")

        st.write("""
        Fuiste directo respecto a la restricción presupuestal.

        Sin embargo, la colaboradora siente que su situación no fue realmente
        escuchada y podría continuar buscando otra oportunidad.
        """)

        scores = {
            "Comunicación e influencia": 2,
            "Pensamiento estratégico": 2,
            "Toma de decisiones": 3,
            "Liderazgo ético": 4
        }

        feedback = (
            "Fuiste honesto respecto a la restricción, pero faltó explorar "
            "los intereses de la colaboradora antes de cerrar la conversación."
        )

    else:

        st.success("La conversación abre una negociación más honesta.")

        st.write("""
        Escuchas las razones por las que la oferta es importante.

        Después explicas las restricciones presupuestales sin prometer algo
        que no puedes garantizar.

        Ambos comienzan a explorar alternativas reales.

        Esto no garantiza que la colaboradora permanezca, pero conserva una
        conversación basada en confianza y transparencia.
        """)

        scores = {
            "Comunicación e influencia": 5,
            "Pensamiento estratégico": 4,
            "Toma de decisiones": 4,
            "Liderazgo ético": 5
        }

        feedback = (
            "Combinaste escucha, claridad y responsabilidad sin crear una "
            "expectativa que todavía no puedes garantizar."
        )

    guardar_resultado(
        "scene1",
        scores,
        decision,
        feedback
    )

    st.divider()

    st.write("### Retroalimentación")

    st.info(feedback)

    st.write("### 🤖 Reacción adaptativa")

    if st.session_state.reaccion_ia is None:

        with st.spinner("La colaboradora está respondiendo..."):
            reaccion = generar_reaccion_ia(
                st.session_state.mensaje_usuario
            )

        st.session_state.reaccion_ia = reaccion

    if st.session_state.reaccion_ia:

        st.markdown(
            f"""
            <div class="ai-box">
            <b>Respuesta de la colaboradora:</b><br><br>
            {st.session_state.reaccion_ia}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.caption(
            "La reacción fue generada dinámicamente a partir del mensaje escrito por el usuario."
        )

    else:

        st.markdown(
            """
            <div class="ai-box">
            <b>Modo de respaldo:</b><br><br>

            La función de IA no está conectada en este momento.
            La simulación continúa utilizando las consecuencias
            previamente definidas.
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "🔄 Replay",
            use_container_width=True
        ):
            st.session_state.reaccion_ia = None
            ir_a("scene1")

    with col2:
        if st.button(
            "Continuar",
            type="primary",
            use_container_width=True
        ):
            ir_a("menu_scenes")


# =========================================================
# SCENE 2 — TODO ES URGENTE
# =========================================================

elif st.session_state.pantalla == "scene2":

    st.markdown(
        '<div class="scene-number">THE SCENE #021</div>',
        unsafe_allow_html=True
    )

    st.title("Todo es urgente")

    st.markdown(
        """
        <div class="scene-box">

        Son las 9:00 de la mañana.

        <br><br>

        En los próximos minutos ocurren cuatro cosas:

        <br><br>

        • Un cliente importante solicita una llamada urgente.<br>
        • Tienes un reporte que vence hoy a las 3:00 p.m.<br>
        • Un integrante de tu equipo necesita ayuda con una tarea que él puede resolver con orientación.<br>
        • A las 10:00 a.m. tienes una reunión estratégica que no puedes mover.

        <br><br>

        No puedes hacer todo al mismo tiempo.

        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("### ¿Qué haces primero?")

    decision = st.radio(
        "Selecciona una estrategia:",
        [
            "Intento atender personalmente todo conforme vaya llegando.",
            "Cancelo la reunión estratégica para resolver primero las urgencias.",
            "Priorizo por impacto y plazo: atiendo al cliente, delego con orientación y protejo la reunión estratégica."
        ],
        index=None
    )

    if st.button(
        "Tomar decisión",
        type="primary",
        use_container_width=True
    ):

        if decision is None:
            st.warning("Selecciona una decisión.")

        else:
            st.session_state.decision_scene2 = decision
            ir_a("resultado_scene2")


# =========================================================
# RESULTADO SCENE 2
# =========================================================

elif st.session_state.pantalla == "resultado_scene2":

    st.title("Consecuencia")

    decision = st.session_state.decision_scene2

    if decision == "Intento atender personalmente todo conforme vaya llegando.":

        st.error("El día se convierte en una cadena de interrupciones.")

        st.write("""
        Resuelves varios asuntos pequeños, pero cambias constantemente de tarea.

        El reporte se retrasa y llegas mal preparado a la reunión estratégica.

        Tu equipo también continúa dependiendo demasiado de ti.
        """)

        scores = {
            "Tiempo y priorización": 2,
            "Toma de decisiones": 2,
            "Liderazgo ético": 3,
            "Pensamiento estratégico": 2
        }

        feedback = (
            "Responder a todo personalmente genera sensación de productividad, "
            "pero reduce el enfoque y limita la capacidad del equipo."
        )

    elif decision == "Cancelo la reunión estratégica para resolver primero las urgencias.":

        st.warning("Resuelves lo inmediato, pero sacrificas una actividad de alto impacto.")

        st.write("""
        Algunas urgencias quedan resueltas.

        Sin embargo, cancelaste una reunión estratégica que involucraba
        decisiones importantes para las siguientes semanas.
        """)

        scores = {
            "Tiempo y priorización": 3,
            "Toma de decisiones": 3,
            "Liderazgo ético": 3,
            "Pensamiento estratégico": 2
        }

        feedback = (
            "Atendiste lo urgente, pero diste prioridad al corto plazo "
            "sobre una actividad con mayor impacto futuro."
        )

    else:

        st.success("Organizas el día según impacto, plazo y responsabilidad.")

        st.write("""
        Atiendes primero el asunto crítico del cliente.

        Después orientas al integrante del equipo para que pueda continuar
        sin depender completamente de ti.

        Mantienes la reunión estratégica y reservas después un bloque de
        trabajo para terminar el reporte.
        """)

        scores = {
            "Tiempo y priorización": 5,
            "Toma de decisiones": 5,
            "Liderazgo ético": 4,
            "Pensamiento estratégico": 5
        }

        feedback = (
            "Priorizaste según impacto y plazo, utilizaste delegación "
            "y protegiste una actividad estratégica."
        )

    guardar_resultado(
        "scene2",
        scores,
        decision,
        feedback
    )

    st.divider()

    st.info(feedback)

    st.write(
        """
        Esta decisión no mide únicamente administración del tiempo.
        También muestra cómo delegas, decides bajo presión y proteges
        actividades estratégicas.
        """
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "🔄 Replay",
            use_container_width=True
        ):
            ir_a("scene2")

    with col2:
        if st.button(
            "Continuar",
            type="primary",
            use_container_width=True
        ):
            ir_a("menu_scenes")


# =========================================================
# SCENE 3 — EL PROCESO YA NO FUNCIONA
# =========================================================

elif st.session_state.pantalla == "scene3":

    st.markdown(
        '<div class="scene-number">THE SCENE #032</div>',
        unsafe_allow_html=True
    )

    st.title("El proceso ya no funciona")

    st.markdown(
        """
        <div class="scene-box">

        Durante los últimos dos meses, el equipo entrega reportes con retraso.

        <br><br>

        El proceso requiere pasar por cinco revisiones diferentes y varias
        personas repiten tareas.

        <br><br>

        La Dirección quiere mejorar los tiempos, pero no autorizó contratar
        más personal ni comprar un sistema nuevo.

        <br><br>

        Tienes que proponer una solución.

        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("### ¿Qué propones?")

    decision = st.radio(
        "Selecciona una alternativa:",
        [
            "Pido al equipo trabajar más rápido y establezco fechas más estrictas.",
            "Elimino varias revisiones inmediatamente para acelerar las entregas.",
            "Mapeo el proceso con el equipo, identifico pasos repetidos y pruebo una mejora pequeña antes de cambiar todo."
        ],
        index=None
    )

    if st.button(
        "Tomar decisión",
        type="primary",
        use_container_width=True
    ):

        if decision is None:
            st.warning("Selecciona una decisión.")

        else:
            st.session_state.decision_scene3 = decision
            ir_a("resultado_scene3")


# =========================================================
# RESULTADO SCENE 3
# =========================================================

elif st.session_state.pantalla == "resultado_scene3":

    st.title("Consecuencia")

    decision = st.session_state.decision_scene3

    if decision == "Pido al equipo trabajar más rápido y establezco fechas más estrictas.":

        st.error("El problema continúa.")

        st.write("""
        El equipo intenta acelerar el trabajo, pero el proceso sigue teniendo
        los mismos pasos repetidos.

        Aumenta la presión sin eliminar la causa del retraso.
        """)

        scores = {
            "Creatividad e innovación": 2,
            "Pensamiento estratégico": 2,
            "Toma de decisiones": 2,
            "Liderazgo ético": 2
        }

        feedback = (
            "Exigiste mayor velocidad, pero no modificaste la causa estructural "
            "del problema."
        )

    elif decision == "Elimino varias revisiones inmediatamente para acelerar las entregas.":

        st.warning("El proceso se acelera, pero aparecen nuevos riesgos.")

        st.write("""
        Los tiempos mejoran temporalmente.

        Sin embargo, eliminaste controles sin probar primero cuáles eran
        realmente innecesarios y empiezan a aparecer errores.
        """)

        scores = {
            "Creatividad e innovación": 3,
            "Pensamiento estratégico": 2,
            "Toma de decisiones": 3,
            "Liderazgo ético": 3
        }

        feedback = (
            "Cambiaste el proceso, pero lo hiciste sin una prueba previa "
            "ni suficiente análisis de consecuencias."
        )

    else:

        st.success("El equipo identifica una mejora viable.")

        st.write("""
        Analizan juntos el proceso actual.

        Detectan tareas duplicadas y diseñan una versión simplificada.

        Primero prueban el cambio durante una semana antes de modificar
        definitivamente el proceso.
        """)

        scores = {
            "Creatividad e innovación": 5,
            "Pensamiento estratégico": 5,
            "Toma de decisiones": 4,
            "Liderazgo ético": 5
        }

        feedback = (
            "Buscaste una alternativa dentro de las restricciones, involucraste "
            "al equipo y probaste la solución antes de aplicarla completamente."
        )

    guardar_resultado(
        "scene3",
        scores,
        decision,
        feedback
    )

    st.divider()

    st.info(feedback)

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "🔄 Replay",
            use_container_width=True
        ):
            ir_a("scene3")

    with col2:
        if st.button(
            "Continuar",
            type="primary",
            use_container_width=True
        ):
            ir_a("menu_scenes")


# =========================================================
# HUELLA DIRECTIVA
# =========================================================

elif st.session_state.pantalla == "huella":

    st.title("Tu Huella Directiva")

    st.write("""
    La Huella Directiva compara tu autopercepción inicial con los patrones
    observados a través de las tres simulaciones.
    """)

    desempeno = calcular_desempeno()
    aut = st.session_state.autopercepcion

    st.divider()

    st.write("### Desempeño observado")

    col1, col2 = st.columns(2)

    orden_izq = [
        "Tiempo y priorización",
        "Creatividad e innovación",
        "Toma de decisiones"
    ]

    orden_der = [
        "Comunicación e influencia",
        "Pensamiento estratégico",
        "Liderazgo ético"
    ]

    with col1:

        for habilidad in orden_izq:

            valor = desempeno[habilidad]

            st.metric(
                f"{ICONOS[habilidad]} {habilidad}",
                f"{valor}/5"
            )

            st.progress(valor / 5)

    with col2:

        for habilidad in orden_der:

            valor = desempeno[habilidad]

            st.metric(
                f"{ICONOS[habilidad]} {habilidad}",
                f"{valor}/5"
            )

            st.progress(valor / 5)

    st.divider()

    st.write("### Autopercepción vs. comportamiento")

    for habilidad in HABILIDADES:

        diferencia = round(
            desempeno[habilidad] - aut[habilidad],
            1
        )

        col_a, col_b, col_c = st.columns(3)

        with col_a:
            st.write(
                f"**{ICONOS[habilidad]} {habilidad}**"
            )

        with col_b:
            st.write(
                f"Autopercepción: **{aut[habilidad]}/5**"
            )

        with col_c:
            st.write(
                f"Observado: **{desempeno[habilidad]}/5**"
            )

        if diferencia <= -0.7:

            st.warning(
                "Posible punto ciego: tu autopercepción fue mayor que el comportamiento observado."
            )

        elif diferencia >= 0.7:

            st.success(
                "Tu desempeño observado fue superior a tu autopercepción."
            )

        else:

            st.caption(
                "Autopercepción y comportamiento relativamente similares."
            )

        st.write("")

    # =====================================================
    # HABILIDAD MÁS BAJA
    # =====================================================

    habilidad_mas_baja = min(
        desempeno,
        key=desempeno.get
    )

    st.divider()

    st.write("### Entrenamiento adaptativo")

    st.info(
        f"""
        Tu área con menor puntuación observada fue:

        **{ICONOS[habilidad_mas_baja]} {habilidad_mas_baja}
        — {desempeno[habilidad_mas_baja]}/5**

        THE SCENE utiliza este resultado para recomendar tu siguiente práctica.
        """
    )

    recomendaciones = {

        "Tiempo y priorización":
            "Practica escenarios donde tengas que distinguir entre urgencia, impacto y delegación.",

        "Comunicación e influencia":
            "Practica escuchar antes de proponer soluciones y comunicar límites con claridad.",

        "Creatividad e innovación":
            "Practica generar varias alternativas antes de elegir una solución.",

        "Pensamiento estratégico":
            "Practica decisiones considerando consecuencias de corto y largo plazo.",

        "Toma de decisiones":
            "Practica elegir una alternativa aun cuando la información sea incompleta.",

        "Liderazgo ético":
            "Practica decisiones donde debas equilibrar resultados, responsabilidad y efecto sobre otras personas."
    }

    st.success(
        recomendaciones[habilidad_mas_baja]
    )

    # =====================================================
    # PLAN PERSONAL
    # =====================================================

    st.divider()

    st.write("### Plan personal de mejora")

    st.write(
        f"""
        **Habilidad prioritaria:** {habilidad_mas_baja}

        **Acción sugerida:** {recomendaciones[habilidad_mas_baja]}

        **Objetivo:** aplicar esta conducta de manera consciente en la
        siguiente simulación o situación real de trabajo.

        **Seguimiento:** utilizar Replay para comparar decisiones y observar
        si el resultado mejora.
        """
    )

    # =====================================================
    # EXPLICACIÓN DE MEDICIÓN TRANSVERSAL
    # =====================================================

    st.divider()

    st.write("### Medición transversal")

    st.write("""
    THE SCENE no evalúa cada habilidad de forma aislada.

    Una misma decisión puede mostrar simultáneamente comunicación,
    pensamiento estratégico, toma de decisiones, liderazgo,
    creatividad o administración del tiempo.

    Esto permite construir una visión más integral del comportamiento directivo.
    """)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "🎬 Volver a las Scenes",
            use_container_width=True
        ):
            ir_a("menu_scenes")

    with col2:

        if st.button(
            "🔄 Reiniciar experiencia",
            use_container_width=True
        ):
            reiniciar_todo()