"""
Potencial Eléctrico - Del Campo Conservativo a la Ecuación de Poisson
==========================================================
@lomejorphysics · Griffiths & López Rodríguez

COMPILAR PREVIEW (30 FPS):
/home/odoo-01/bin/micromamba run -n manim manim --disable_caching --fps 30 -ql --format=mp4 -r 1080,1920 potencial_electrico.py PotencialElectrico
"""

from manim import *
import numpy as np

# ══════════════════════════════════════════════════════════════════════════
# COLORES
# ══════════════════════════════════════════════════════════════════════════
BG         = "#0d1117"
CLR_Q      = "#FFD700"
CLR_E      = "#4FC3F7"
CLR_V      = "#AB47BC"
CLR_S      = "#26C6DA"
CLR_N      = "#66BB6A"
CLR_FLUX   = "#FFA726"
CLR_CANCEL = "#EF5350"
CLR_RES    = "#FFD54F"
CLR_LAPL   = "#E91E63"
CLR_POISSON= "#00BCD4"

# ══════════════════════════════════════════════════════════════════════════
# TIPOGRAFÍA  (reducida respecto al original para que no se solapen)
# ══════════════════════════════════════════════════════════════════════════
S_TITLE = 56
S_EQ    = 48
S_SUB   = 40
S_TXT   = 32
S_LBL   = 28
S_NOTE  = 24

# ══════════════════════════════════════════════════════════════════════════
# ZONAS VERTICALES  (formato 1080×1920, origin = centro)
# ══════════════════════════════════════════════════════════════════════════
ZONE_TTL  = UP * 7.5   # título de escena
ZONE_SUB  = UP * 6.2   # subtítulo
ZONE_EQ1  = UP * 4.2   # primera ecuación
ZONE_EQ2  = UP * 2.0   # segunda ecuación
ZONE_MID  = ORIGIN     # zona central para visuales
ZONE_NOTE = DOWN * 6.5  # notas al pie
ZONE_BRAND= DOWN * 7.8  # marca

# ══════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════
def capsule_bg(mob, fill_opacity=0.92, color=BG, buff=0.22):
    """BackgroundRectangle con esquinas redondeadas."""
    return BackgroundRectangle(mob, fill_opacity=fill_opacity, buff=buff, color=color)

def box(mob, color=CLR_RES, buff=0.3, sw=2.5, r=0.15):
    return SurroundingRectangle(mob, color=color, buff=buff, stroke_width=sw, corner_radius=r)


# ══════════════════════════════════════════════════════════════════════════
# ESCENA PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════
class PotencialElectrico(ThreeDScene):
    def construct(self):
        self.camera.background_color = BG
        self.escena_titulo()
        self.escena_conservativo()
        self.escena_independencia_camino()
        self.escena_potencial_def()
        self.escena_deduccion_V()
        self.escena_gradiente()
        self.escena_poisson()
        self.escena_laplaciano()
        self.escena_cierre()

    # ═══════════════════════════════════════════════════════════════════════
    # ESCENA 1: TÍTULO
    # ═══════════════════════════════════════════════════════════════════════
    def escena_titulo(self):
        self.set_camera_orientation(phi=0, theta=-PI / 2)

        titulo = Text("Potencial Eléctrico", font_size=S_TITLE)
        titulo.move_to(ZONE_TTL + DOWN * 0.5)

        sub = Text(
            "Del Campo Conservativo\na la Ecuación de Poisson",
            font_size=S_TXT, color=GREY_B, line_spacing=1.2,
        )
        sub.next_to(titulo, DOWN, buff=0.5)

        linea = Line(LEFT * 2.5, RIGHT * 2.5, color=CLR_V, stroke_width=1.5)
        linea.next_to(sub, DOWN, buff=0.4)

        fuente = Text("Griffiths & López Rodríguez", font_size=S_NOTE, color=GREY_C)
        fuente.next_to(linea, DOWN, buff=0.35)

        brand = Text("@lomejorphysics", font_size=S_LBL, color=CLR_Q)
        brand.move_to(ZONE_BRAND)

        self.play(Write(titulo, run_time=1.5))
        self.play(FadeIn(sub), GrowFromCenter(linea))
        self.play(FadeIn(fuente), FadeIn(brand))
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in [titulo, sub, linea, fuente, brand]])

    # ═══════════════════════════════════════════════════════════════════════
    # ESCENA 2: CAMPO CONSERVATIVO  (REDISEÑADA AL ESTILO 3B1B)
    # ═══════════════════════════════════════════════════════════════════════
    def escena_conservativo(self):
        """
        Visualización del rotacional cero estilo 3B1B:
          1. ArrowVectorField radial (campo de Coulomb).
          2. Paleta/ruedita que NO gira → concepto de rotacional nulo.
          3. Curva cerrada con ShowPassingFlash → trabajo = 0.
          4. Ecuaciones posicionadas SIN solapar nada.
        """
        self.set_camera_orientation(phi=0, theta=-PI / 2)

        # ── Título ──────────────────────────────────────────────────────
        ttl = Text("Campo Conservativo", font_size=S_TITLE, color=CLR_E)
        ttl.move_to(ZONE_TTL)
        self.play(Write(ttl))

        # ── ArrowVectorField radial: E ∝ r̂/r² ──────────────────────────
        # Escala suavizada para que los vectores centrales no sean enormes
        def campo_coulomb(pos):
            r = np.linalg.norm(pos[:2])
            if r < 0.4:
                return np.zeros(3)
            mag = min(1.0, 0.8 / r**1.5)
            return np.array([pos[0] / r, pos[1] / r, 0]) * mag

        vf = ArrowVectorField(
            campo_coulomb,
            x_range=[-3.5, 3.5, 0.7],
            y_range=[-5.0, 5.0, 0.7],
            color=CLR_E,
            length_func=lambda n: 0.35 * n,
        )
        vf.set_opacity(0.35)

        stream_lines = StreamLines(
            campo_coulomb,
            x_range=[-3.5, 3.5, 0.4],
            y_range=[-5.0, 5.0, 0.4],
            color=CLR_E,
            stroke_width=2,
            max_color_scheme_value=2
        )

        carga = Dot(ORIGIN, radius=0.18, color=CLR_Q, z_index=3)
        lbl_q = MathTex("+q", font_size=S_LBL, color=CLR_Q).next_to(carga, DOWN, buff=0.15)

        self.play(FadeIn(vf, lag_ratio=0.01, run_time=1.5), FadeIn(carga, lbl_q))
        
        self.add(stream_lines)
        stream_lines.start_animation(warm_up=False, flow_speed=1.5)
        self.wait(1.5)

        # ── PALETA giratoria (paddle wheel) ────────────────────────────
        # Simula una pequeña rueda de aspas colocada en el campo.
        # Para un campo radial (conservativo) la rueda NO gira.
        wheel_center = np.array([1.8, 1.8, 0])

        def make_paddle(center, angle_offset=0):
            spokes = VGroup()
            for k in range(4):
                a = angle_offset + k * PI / 2
                tip = center + 0.22 * np.array([np.cos(a), np.sin(a), 0])
                spokes.add(Line(center, tip, color=CLR_RES, stroke_width=3))
            hub = Dot(center, radius=0.06, color=CLR_RES, z_index=4)
            return VGroup(spokes, hub)

        paddle = make_paddle(wheel_center)
        self.play(FadeIn(paddle))

        # La paleta aparece pero NO rota → anotación textual
        nota_paddle = Text("Flujo irrotacional → Rotacional nulo", font_size=S_NOTE, color=GREY_B)
        nota_paddle.move_to(ZONE_NOTE)
        bg_np = capsule_bg(nota_paddle)
        self.play(FadeIn(bg_np), FadeIn(nota_paddle))
        
        # Aplicamos Wiggle para simular la interacción con el fluido (pequeña vibración sin rotación neta)
        self.play(Wiggle(paddle, run_time=1.5, rotation_angle=0.04 * PI, scale_value=1.02))
        
        # Movemos la paleta a otro punto para mostrar que en ningún lugar rota
        self.play(paddle.animate.move_to([-1.5, 2.0, 0]), run_time=1.5, rate_func=rate_functions.smooth)
        self.play(Wiggle(paddle, run_time=1.0, rotation_angle=0.04 * PI, scale_value=1.02))
        
        # Mover a un tercer punto
        self.play(paddle.animate.move_to([1.0, -2.5, 0]), run_time=1.5, rate_func=rate_functions.smooth)
        self.play(Wiggle(paddle, run_time=1.0, rotation_angle=0.04 * PI, scale_value=1.02))
        self.wait(1.0)

        # ── Ecuación ∇ × E = 0  (posicionada en ZONE_EQ1, encima del visual) ──
        eq_rot = MathTex(
            r"\nabla", r"\times", r"\vec{E}", "=", "0",
            font_size=S_EQ,
        )
        eq_rot.move_to(ZONE_EQ1)
        bg_rot = capsule_bg(eq_rot)
        self.play(FadeOut(bg_np), FadeOut(nota_paddle))
        self.play(FadeIn(bg_rot), Write(eq_rot))

        nota_rot = Text("El campo eléctrico es irrotacional", font_size=S_NOTE, color=GREY_B)
        nota_rot.move_to(ZONE_NOTE)
        bg_nr = capsule_bg(nota_rot)
        self.play(FadeIn(bg_nr), FadeIn(nota_rot))
        self.wait(1.5)

        # ── Trayectoria cerrada + ShowPassingFlash ──────────────────────
        # Un contorno circular centrado en la carga
        loop = Circle(radius=2.2, color=CLR_FLUX, stroke_width=3).rotate(-PI / 2)
        arrow_tip = Arrow(
            loop.get_bottom() + LEFT * 0.01,
            loop.get_bottom() + LEFT * 0.3,
            color=CLR_FLUX, buff=0, stroke_width=3, max_tip_length_to_length_ratio=0.35,
        )

        eq_stokes = MathTex(
            r"\oint_C \vec{E} \cdot d\vec{l} = 0",
            font_size=S_EQ,
        )
        eq_stokes.move_to(ZONE_EQ2)
        bg_stokes = capsule_bg(eq_stokes)

        nota_stokes = Text("Trabajo nulo en trayectoria cerrada", font_size=S_NOTE, color=GREY_B)
        nota_stokes.move_to(ZONE_NOTE)
        bg_ns = capsule_bg(nota_stokes)

        self.play(FadeOut(bg_nr), FadeOut(nota_rot))
        self.play(Create(loop), FadeIn(arrow_tip))
        self.play(
            ShowPassingFlash(
                loop.copy().set_color(YELLOW).set_stroke(width=6),
                time_width=0.4,
                run_time=2,
            )
        )
        self.play(FadeIn(bg_stokes), Write(eq_stokes))
        self.play(FadeIn(bg_ns), FadeIn(nota_stokes))
        self.wait(2)

        self.play(*[FadeOut(m) for m in self.mobjects])

    # ═══════════════════════════════════════════════════════════════════════
    # ESCENA 2.5: INDEPENDENCIA DEL CAMINO  (mejorada)
    # ═══════════════════════════════════════════════════════════════════════
    def escena_independencia_camino(self):
        self.set_camera_orientation(phi=0, theta=-PI / 2)

        ttl = Text("Independencia del Camino", font_size=S_TITLE, color=CLR_N)
        ttl.move_to(ZONE_TTL)
        self.play(Write(ttl))

        # ── Puntos A y B más abajo, dejando espacio para ecuaciones arriba ──
        y_pts = -0.5
        punto_a = Dot(LEFT * 3, radius=0.1, color=CLR_N).shift(UP * y_pts)
        lbl_a   = MathTex("A", font_size=S_LBL, color=CLR_N).next_to(punto_a, LEFT, buff=0.12)
        punto_b = Dot(RIGHT * 3, radius=0.1, color=CLR_V).shift(UP * y_pts)
        lbl_b   = MathTex("B", font_size=S_LBL, color=CLR_V).next_to(punto_b, RIGHT, buff=0.12)
        self.play(FadeIn(punto_a, lbl_a, punto_b, lbl_b))

        # ── Tres caminos con colores distintos ──────────────────────────
        start = punto_a.get_center()
        end   = punto_b.get_center()

        camino_1 = Line(start, end, color=CLR_E, stroke_width=3)
        camino_2 = ArcBetweenPoints(start, end, angle=TAU / 5,  color=CLR_S,    stroke_width=3)
        camino_3 = ArcBetweenPoints(start, end, angle=-TAU / 4, color=CLR_LAPL, stroke_width=3)

        # Añadir punta de flecha al final de cada camino
        for c in [camino_1, camino_2, camino_3]:
            c.add_tip(tip_length=0.18)

        # Etiquetas a mitad de cada camino, desplazadas perpendicularmente
        lbl_c1 = MathTex("C_1", font_size=S_NOTE, color=CLR_E).move_to(
            (start + end) / 2 + DOWN * 0.3
        )
        lbl_c2 = MathTex("C_2", font_size=S_NOTE, color=CLR_S).move_to(
            (start + end) / 2 + UP * 1.2
        )
        lbl_c3 = MathTex("C_3", font_size=S_NOTE, color=CLR_LAPL).move_to(
            (start + end) / 2 + DOWN * 1.8
        )

        self.play(
            Create(camino_1), FadeIn(lbl_c1),
            run_time=0.8,
        )
        self.play(Create(camino_2), FadeIn(lbl_c2), run_time=0.8)
        self.play(Create(camino_3), FadeIn(lbl_c3), run_time=0.8)

        # ── Ecuación principal en ZONE_EQ1 ──────────────────────────────
        eq = MathTex(
            r"\int_{C_1}\!\vec{E}\cdot d\vec{l}"
            r"=\int_{C_2}\!\vec{E}\cdot d\vec{l}"
            r"=\int_{C_3}\!\vec{E}\cdot d\vec{l}",
            font_size=S_SUB,
        )
        eq.move_to(ZONE_EQ1)
        bg_eq = capsule_bg(eq)
        self.play(FadeIn(bg_eq), Write(eq))

        nota = Text("Sólo depende del punto inicial y final", font_size=S_NOTE, color=GREY_B)
        nota.move_to(ZONE_NOTE)
        bg_nota = capsule_bg(nota)
        self.play(FadeIn(bg_nota), FadeIn(nota))
        self.wait(2)

        # ── Highlight animado: tres caminos se iluminan en secuencia ────
        for camino, col in [
            (camino_1, CLR_E),
            (camino_2, CLR_S),
            (camino_3, CLR_LAPL),
        ]:
            self.play(
                ShowPassingFlash(
                    camino.copy().set_color(WHITE).set_stroke(width=8),
                    time_width=0.5,
                    run_time=0.8,
                )
            )

        # ── Teorema fundamental del gradiente ───────────────────────────
        eq_f = MathTex(
            r"\int_A^B \vec{E}\cdot d\vec{l}",
            r"\ =\ ",
            r"V(A) - V(B)",
            font_size=S_SUB,
        )
        eq_f.move_to(ZONE_EQ2)
        bg_f = capsule_bg(eq_f)

        nota_th = Text("Teorema Fundamental del Gradiente", font_size=S_NOTE, color=CLR_N)
        nota_th.move_to(ZONE_NOTE)
        bg_nth = capsule_bg(nota_th)

        self.play(FadeOut(bg_nota), FadeOut(nota))
        self.play(FadeIn(bg_f), Write(eq_f))
        self.play(FadeIn(bg_nth), FadeIn(nota_th))
        self.wait(2.5)

        self.play(*[FadeOut(m) for m in self.mobjects])

    # ═══════════════════════════════════════════════════════════════════════
    # ESCENA 3: DEFINICIÓN DE POTENCIAL
    # ═══════════════════════════════════════════════════════════════════════
    def escena_potencial_def(self):
        self.set_camera_orientation(phi=0, theta=-PI / 2)

        ttl = Text("Definición de Potencial", font_size=S_TITLE, color=CLR_V)
        ttl.move_to(ZONE_TTL)
        self.play(Write(ttl))

        eq_def = MathTex(
            r"V(\vec{r})", "=",
            r"-\int_{\mathcal{O}}^{\vec{r}}", r"\vec{E}", r"\cdot", r"d\vec{l}",
            font_size=S_EQ,
        )
        eq_def.move_to(ZONE_EQ1)
        bg_def = capsule_bg(eq_def)
        self.play(FadeIn(bg_def), Write(eq_def))

        nota = Text("Trabajo por unidad de carga desde la referencia", font_size=S_NOTE, color=GREY_B)
        nota.move_to(ZONE_NOTE)
        bg_nota = capsule_bg(nota)
        self.play(FadeIn(bg_nota), FadeIn(nota))
        self.wait(1.5)

        # ── Animación: carga viniendo del infinito ──────────────────────
        # Representamos el "infinito" como un punto fuera de cuadro izquierdo
        # y la posición r como punto a la derecha. Una partícula se mueve a lo
        # largo de un arco levemente curvado para dar estética.

        y_vis = -1.5     # altura del visual
        x_inf = -4.5
        x_r   =  2.5

        pos_inf = np.array([x_inf, y_vis, 0])
        pos_r   = np.array([x_r,   y_vis, 0])

        punto_r   = Dot(pos_r,   radius=0.1, color=CLR_V)
        lbl_r     = MathTex(r"\vec{r}", font_size=S_LBL, color=CLR_V).next_to(punto_r, UP, buff=0.1)

        # "∞" representado como texto + línea discontinua muy a la izquierda
        lbl_inf = MathTex(r"\infty", font_size=S_LBL, color=GREY_C)
        lbl_inf.move_to(pos_inf + UP * 0.35)
        linea_inf = DashedLine(
            pos_inf + DOWN * 0.3,
            pos_inf + DOWN * 0.85,
            color=GREY_C, stroke_width=1.5,
        )

        # Partícula de prueba: pequeño punto dorado
        carga_test = Dot(pos_inf, radius=0.14, color=CLR_Q, z_index=4)
        lbl_qt = MathTex("+q_0", font_size=S_NOTE, color=CLR_Q)
        lbl_qt.add_updater(lambda m: m.next_to(carga_test, DOWN, buff=0.12))

        # Trayectoria: arco suavemente curvado hacia abajo y a la derecha
        traj = ArcBetweenPoints(pos_inf, pos_r, angle=-0.3, color=CLR_E, stroke_width=2)

        # Fondo negro que "borra" el rastro del label conforme avanza
        # (solución: no usar updater en el label sino hacerlo desaparecer)
        self.play(FadeIn(punto_r, lbl_r, lbl_inf, linea_inf))
        self.play(FadeIn(carga_test, lbl_qt))
        self.play(
            MoveAlongPath(carga_test, traj),
            Create(traj),
            run_time=2.8,
            rate_func=rate_functions.ease_in_out_sine,
        )
        lbl_qt.clear_updaters()

        # Pulso al llegar
        self.play(
            Flash(pos_r, color=CLR_V, line_length=0.2, num_lines=10, flash_radius=0.4),
            run_time=0.6,
        )

        nota2 = MathTex(
            r"V(\infty) = 0", r"\quad \Rightarrow \quad",
            r"V(\vec{r}) = -\int_{\infty}^{\vec{r}} \vec{E}\cdot d\vec{l}",
            font_size=S_SUB,
        )
        nota2.move_to(ZONE_EQ2)
        bg_n2 = capsule_bg(nota2)
        self.play(FadeOut(bg_nota), FadeOut(nota))
        self.play(FadeIn(bg_n2), Write(nota2))
        self.wait(2)

        self.play(*[FadeOut(m) for m in self.mobjects])

    # ═══════════════════════════════════════════════════════════════════════
    # ESCENA 4: DEDUCCIÓN DEL POTENCIAL + LÍMITE COMO r→∞ + CASO GENERAL
    # ═══════════════════════════════════════════════════════════════════════
    def escena_deduccion_V(self):
        self.set_camera_orientation(phi=0, theta=-PI / 2)

        ttl = Text("Para una Carga Puntual", font_size=S_TITLE, color=CLR_V)
        ttl.move_to(ZONE_TTL)
        self.play(Write(ttl))

        # ── Paso 1 ───────────────────────────────────────────────────────
        e1 = MathTex(
            r"V(r)", r"=", r"-\int_{\infty}^{r}", r"E\,dr'",
            font_size=S_SUB,
        )
        e1.move_to(ZONE_EQ1)
        p1_lbl = Text("Paso 1 · Campo radial E(r)", font_size=S_NOTE, color=GREY_C)
        p1_lbl.move_to(ZONE_NOTE)
        bg_p1 = capsule_bg(p1_lbl)
        self.play(Write(e1), FadeIn(bg_p1), FadeIn(p1_lbl))
        self.wait(1)
        self.play(FadeOut(bg_p1), FadeOut(p1_lbl))

        # ── Paso 2 ───────────────────────────────────────────────────────
        e2 = MathTex(
            r"V(r)", r"=", r"-\int_{\infty}^{r}",
            r"\frac{q}{4\pi\epsilon_0 r'^2}", r"\,dr'",
            font_size=S_SUB,
        )
        e2.move_to(ZONE_EQ1)
        p2_lbl = Text("Paso 2 · Sustituir campo de carga puntual", font_size=S_NOTE, color=GREY_C)
        p2_lbl.move_to(ZONE_NOTE)
        bg_p2 = capsule_bg(p2_lbl)
        self.play(
            TransformMatchingTex(e1, e2, transform_mismatches=True, run_time=1.5),
            FadeIn(bg_p2), FadeIn(p2_lbl),
        )
        self.wait(1)
        self.play(FadeOut(bg_p2), FadeOut(p2_lbl))

        # ── Paso 3: límite explícito con r′ → ∞ ─────────────────────────
        e3 = MathTex(
            r"V(r)", r"=",
            r"-\frac{q}{4\pi\epsilon_0}",
            r"\left[-\frac{1}{r'}\right]_{r'=\infty}^{r'=r}",
            font_size=S_SUB,
        )
        e3.move_to(ZONE_EQ1)
        p3_lbl = Text("Paso 3 · Integrar y evaluar límites", font_size=S_NOTE, color=GREY_C)
        p3_lbl.move_to(ZONE_NOTE)
        bg_p3 = capsule_bg(p3_lbl)
        self.play(
            TransformMatchingTex(e2, e3, transform_mismatches=True, run_time=1.5),
            FadeIn(bg_p3), FadeIn(p3_lbl),
        )
        self.wait(1.2)
        self.play(FadeOut(bg_p3), FadeOut(p3_lbl))

        # ── Paso 3b: expansión del límite ────────────────────────────────
        e3b = MathTex(
            r"V(r)", r"=",
            r"-\frac{q}{4\pi\epsilon_0}",
            r"\left(-\frac{1}{r} - \underbrace{\left(-\frac{1}{\infty}\right)}_{\to\,0}\right)",
            font_size=S_SUB,
        )
        e3b.move_to(ZONE_EQ1)
        nota_lim = MathTex(
            r"\lim_{r'\to\infty}\frac{1}{r'} = 0",
            font_size=S_SUB, color=CLR_N,
        )
        nota_lim.move_to(ZONE_EQ2)
        bg_lim = capsule_bg(nota_lim)
        self.play(
            TransformMatchingTex(e3, e3b, transform_mismatches=True, run_time=1.5),
        )
        self.play(FadeIn(bg_lim), Write(nota_lim))
        self.wait(1.5)
        self.play(FadeOut(bg_lim), FadeOut(nota_lim))

        # ── Resultado carga puntual ──────────────────────────────────────
        e4 = MathTex(
            r"V(r)", r"=", r"\frac{q}{4\pi\epsilon_0\,r}",
            font_size=60,
        )
        e4.move_to(ZONE_EQ1)
        bx4 = box(e4, color=CLR_RES)
        self.play(
            TransformMatchingTex(e3b, e4, transform_mismatches=True, run_time=1.5),
        )
        self.play(Create(bx4))

        nota_res = Text(
            "El potencial cae como 1/r para una carga puntual",
            font_size=S_NOTE, color=GREY_B,
        )
        nota_res.move_to(ZONE_NOTE)
        bg_nres = capsule_bg(nota_res)
        self.play(FadeIn(bg_nres), FadeIn(nota_res))
        self.wait(2)
        self.play(FadeOut(bg_nres), FadeOut(nota_res))

        # ── Caso general: distribución arbitraria de carga ───────────────
        sep = Line(LEFT * 2.8, RIGHT * 2.8, color=GREY_D, stroke_width=0.8)
        sep.move_to(ZONE_EQ2 + UP * 0.5)

        lbl_gen = Text("Distribución arbitraria de carga:", font_size=S_NOTE, color=CLR_S)
        lbl_gen.move_to(ZONE_EQ2 + DOWN * 0.3)
        bg_gen_lbl = capsule_bg(lbl_gen)

        e_vol = MathTex(
            r"V(\vec{r})", r"=",
            r"\frac{1}{4\pi\epsilon_0}",
            r"\int_{\mathcal{V}}",
            r"\frac{\rho(\vec{r}\,')}{\lvert\vec{r}-\vec{r}\,'\rvert}",
            r"\,d^3r'",
            font_size=S_SUB,
        )
        e_vol.move_to(ZONE_EQ2 + DOWN * 1.6)
        bg_evol = capsule_bg(e_vol)
        bx_vol  = box(e_vol, color=CLR_S, buff=0.25, sw=2)

        self.play(GrowFromCenter(sep))
        self.play(FadeIn(bg_gen_lbl), FadeIn(lbl_gen))
        self.play(FadeIn(bg_evol), Write(e_vol))
        self.play(Create(bx_vol))

        nota_vol = Text(
            "ρ es la densidad volumétrica de carga",
            font_size=S_NOTE, color=GREY_B,
        )
        nota_vol.move_to(ZONE_NOTE)
        bg_nvol = capsule_bg(nota_vol)
        self.play(FadeIn(bg_nvol), FadeIn(nota_vol))
        self.wait(2.5)

        self.play(*[FadeOut(m) for m in self.mobjects])

    # ═══════════════════════════════════════════════════════════════════════
    # ESCENA 5: GRADIENTE  +  JUSTIFICACIÓN ∇×E = 0 → E = -∇V
    # ═══════════════════════════════════════════════════════════════════════
    def escena_gradiente(self):
        self.set_camera_orientation(phi=0, theta=-PI / 2)

        ttl = Text("Relación con el Gradiente", font_size=S_TITLE, color=CLR_V)
        ttl.move_to(ZONE_TTL)
        self.play(Write(ttl))

        # ── Por qué E = -∇V: argumento desde ∇×E = 0 ───────────────────
        # Recordatorio del rotacional nulo
        eq_rot = MathTex(r"\nabla\times\vec{E}=0", font_size=S_EQ, color=CLR_E)
        eq_rot.move_to(ZONE_EQ1)
        bg_rot = capsule_bg(eq_rot)
        nota_rot = Text(
            "Por ser conservativo, ∇×E = 0",
            font_size=S_NOTE, color=GREY_B,
        )
        nota_rot.move_to(ZONE_NOTE)
        bg_nr = capsule_bg(nota_rot)
        self.play(FadeIn(bg_rot), Write(eq_rot))
        self.play(FadeIn(bg_nr), FadeIn(nota_rot))
        self.wait(1.5)

        # Identidad vectorial: ∇×(∇f) ≡ 0 para cualquier escalar f
        eq_id = MathTex(
            r"\nabla\times(\nabla f) \equiv 0",
            r"\quad \forall\, f",
            font_size=S_SUB, color=CLR_N,
        )
        eq_id.move_to(ZONE_EQ2)
        bg_id = capsule_bg(eq_id)
        nota_id = Text(
            "El rotacional de cualquier gradiente es cero",
            font_size=S_NOTE, color=GREY_B,
        )
        nota_id.move_to(ZONE_NOTE)
        bg_ni = capsule_bg(nota_id)
        self.play(FadeOut(bg_nr), FadeOut(nota_rot))
        self.play(FadeIn(bg_id), Write(eq_id))
        self.play(FadeIn(bg_ni), FadeIn(nota_id))
        self.wait(1.5)

        # Por lo tanto podemos escribir E como gradiente de un escalar
        nota_cons = Text(
            "⟹ Podemos escribir  E = −∇V  para algún escalar V",
            font_size=S_NOTE, color=CLR_V,
        )
        nota_cons.move_to(ZONE_NOTE)
        bg_nc = capsule_bg(nota_cons)
        self.play(FadeOut(bg_ni), FadeOut(nota_id))
        self.play(FadeIn(bg_nc), FadeIn(nota_cons))
        self.wait(1.5)
        self.play(FadeOut(bg_id), FadeOut(eq_id), FadeOut(bg_nc), FadeOut(nota_cons))

        # ── Ecuación principal ───────────────────────────────────────────
        eq_grad = MathTex(r"\vec{E} = -\nabla V", font_size=S_EQ)
        eq_grad.move_to(ZONE_EQ1)
        bg_grad = capsule_bg(eq_grad)
        bx_grad = box(eq_grad, color=CLR_V)
        self.play(ReplacementTransform(bg_rot, bg_grad), ReplacementTransform(eq_rot, eq_grad))
        self.play(Create(bx_grad))

        nota_grad = Text("El gradiente apunta hacia el máximo potencial", font_size=S_NOTE, color=GREY_B)
        nota_grad.move_to(ZONE_NOTE)
        bg_ng = capsule_bg(nota_grad)
        self.play(FadeIn(bg_ng), FadeIn(nota_grad))
        self.wait(1.5)

        # ── Componentes cartesianas ──────────────────────────────────────
        eq_exp = MathTex(
            r"\vec{E} = -\left(",
            r"\frac{\partial V}{\partial x}\hat{i}",
            r"+\frac{\partial V}{\partial y}\hat{j}",
            r"+\frac{\partial V}{\partial z}\hat{k}",
            r"\right)",
            font_size=S_SUB,
        )
        eq_exp.move_to(ZONE_EQ2)
        bg_exp = capsule_bg(eq_exp)
        self.play(FadeIn(bg_exp), Write(eq_exp))
        self.wait(1.5)

        # ── Visual: superficies equipotenciales y campo perpendicular ────
        carga_g = Dot(ORIGIN + DOWN * 1.2, radius=0.1, color=CLR_Q, z_index=3)
        lbl_qg  = MathTex("+q", font_size=S_NOTE, color=CLR_Q).next_to(carga_g, DOWN, buff=0.12)

        eq1 = Circle(radius=1.3, color=CLR_V, stroke_width=1.5, stroke_opacity=0.55)
        eq1.move_to(carga_g.get_center())
        eq2 = Circle(radius=2.1, color=CLR_V, stroke_width=1, stroke_opacity=0.35)
        eq2.move_to(carga_g.get_center())

        lbl_v1 = MathTex("V_1", font_size=S_NOTE, color=CLR_V).move_to(
            carga_g.get_center() + RIGHT * 1.3 + UP * 0.25
        )
        lbl_v2 = MathTex("V_2", font_size=S_NOTE, color=CLR_V).move_to(
            carga_g.get_center() + RIGHT * 2.1 + UP * 0.25
        )

        # Flecha perpendicular a las equipotenciales
        flecha_e = Arrow(
            carga_g.get_center(),
            carga_g.get_center() + RIGHT * 2.5,
            color=CLR_E, stroke_width=3, buff=0,
        )
        lbl_e = MathTex(r"\vec{E}", font_size=S_LBL, color=CLR_E).next_to(flecha_e, UP, buff=0.08)

        self.play(FadeIn(carga_g, lbl_qg))
        self.play(Create(eq1), Create(eq2))
        self.play(FadeIn(lbl_v1, lbl_v2))
        self.play(GrowArrow(flecha_e), FadeIn(lbl_e))

        nota2 = Text("E ⊥ superficies equipotenciales", font_size=S_NOTE, color=GREY_B)
        nota2.move_to(ZONE_NOTE)
        bg_n2 = capsule_bg(nota2)
        self.play(FadeOut(bg_ng), FadeOut(nota_grad))
        self.play(FadeIn(bg_n2), FadeIn(nota2))
        self.wait(2)

        self.play(*[FadeOut(m) for m in self.mobjects])

    # ═══════════════════════════════════════════════════════════════════════
    # ESCENA 6: ECUACIÓN DE POISSON  (posicionamiento corregido)
    # ═══════════════════════════════════════════════════════════════════════
    def escena_poisson(self):
        self.set_camera_orientation(phi=0, theta=-PI / 2)

        # ── Título + subtítulo sin solapar ──────────────────────────────
        ttl = Text("Ecuación de Poisson", font_size=S_TITLE, color=CLR_POISSON)
        ttl.move_to(ZONE_TTL)
        self.play(Write(ttl))

        sub = Text("Conexión con la Ley de Gauss", font_size=S_TXT, color=GREY_B)
        sub.move_to(ZONE_SUB)
        self.play(FadeIn(sub))

        # ── Paso 1: Ley de Gauss diferencial en ZONE_EQ1 ───────────────
        e1 = MathTex(
            r"\nabla\cdot\vec{E} = \frac{\rho}{\epsilon_0}",
            font_size=S_EQ,
        )
        e1.move_to(ZONE_EQ1)
        bg_e1 = capsule_bg(e1)

        p1_lbl = Text("1ª Ley de Maxwell (forma diferencial)", font_size=S_NOTE, color=GREY_C)
        p1_lbl.move_to(ZONE_NOTE)
        bg_p1 = capsule_bg(p1_lbl)
        self.play(FadeIn(bg_e1), Write(e1), FadeIn(bg_p1), FadeIn(p1_lbl))
        self.wait(1.5)
        self.play(FadeOut(bg_p1), FadeOut(p1_lbl))

        # ── Paso 1b: recordar E = -∇V en ZONE_EQ2 ──────────────────────
        eq_ev = MathTex(r"\vec{E} = -\nabla V", font_size=S_SUB, color=CLR_V)
        eq_ev.move_to(ZONE_EQ2)
        bg_ev = capsule_bg(eq_ev)
        nota_ev = Text("Recordando E = −∇V (campo conservativo)", font_size=S_NOTE, color=CLR_V)
        nota_ev.move_to(ZONE_NOTE)
        bg_nev = capsule_bg(nota_ev)
        self.play(FadeIn(bg_ev), Write(eq_ev))
        self.play(FadeIn(bg_nev), FadeIn(nota_ev))
        self.wait(1.5)
        self.play(FadeOut(bg_nev), FadeOut(nota_ev))

        # ── Paso 2: Sustituir en ZONE_EQ1 ──────────────────────────────
        e2 = MathTex(
            r"\nabla\cdot(-\nabla V) = \frac{\rho}{\epsilon_0}",
            font_size=S_SUB,
        )
        e2.move_to(ZONE_EQ1)
        bg_e2 = capsule_bg(e2)

        p2_lbl = Text("Paso 2 · Sustituir  E = −∇V", font_size=S_NOTE, color=GREY_C)
        p2_lbl.move_to(ZONE_NOTE)
        bg_p2 = capsule_bg(p2_lbl)
        self.play(
            ReplacementTransform(bg_e1, bg_e2),
            TransformMatchingTex(e1, e2, transform_mismatches=True, run_time=2),
            FadeOut(bg_ev), FadeOut(eq_ev),
            FadeIn(bg_p2), FadeIn(p2_lbl),
        )
        self.wait(1.5)
        self.play(FadeOut(bg_p2), FadeOut(p2_lbl))

        # ── Resultado: Ecuación de Poisson (en ZONE_EQ1, más grande) ───
        e3 = MathTex(
            r"\nabla^2 V = -\frac{\rho}{\epsilon_0}",
            font_size=S_EQ,
        )
        e3.move_to(ZONE_EQ1)
        bg_e3 = capsule_bg(e3)
        bx3   = box(e3, color=CLR_POISSON, sw=3)

        p3_lbl = Text("Ecuación de Poisson", font_size=S_NOTE, color=CLR_POISSON)
        p3_lbl.move_to(ZONE_NOTE)
        bg_p3 = capsule_bg(p3_lbl)

        self.play(
            ReplacementTransform(bg_e2, bg_e3),
            ReplacementTransform(e2, e3, run_time=2),
            FadeIn(bg_p3), FadeIn(p3_lbl),
        )
        self.play(Create(bx3))
        self.wait(2.5)

        # ── Caso especial: Laplace (ρ = 0) ─────────────────────────────
        e_lap = MathTex(
            r"\rho=0 \quad\Rightarrow\quad \nabla^2 V = 0",
            font_size=S_SUB, color=CLR_LAPL,
        )
        e_lap.move_to(ZONE_EQ2)
        bg_lap = capsule_bg(e_lap)
        nota_lap = Text("Ecuación de Laplace (sin cargas)", font_size=S_NOTE, color=CLR_LAPL)
        nota_lap.move_to(ZONE_NOTE)
        bg_nlap = capsule_bg(nota_lap)
        self.play(FadeOut(bg_p3), FadeOut(p3_lbl))
        self.play(FadeIn(bg_lap), Write(e_lap))
        self.play(FadeIn(bg_nlap), FadeIn(nota_lap))
        self.wait(2)

        self.play(*[FadeOut(m) for m in self.mobjects])

    # ═══════════════════════════════════════════════════════════════════════
    # ESCENA 7: LAPLACIANO
    # ═══════════════════════════════════════════════════════════════════════
    def escena_laplaciano(self):
        self.set_camera_orientation(phi=0, theta=-PI / 2)

        ttl = Text("El Laplaciano Escalar", font_size=S_TITLE, color=CLR_LAPL)
        ttl.move_to(ZONE_TTL)
        self.play(Write(ttl))

        eq_lap = MathTex(r"\nabla^2 = \nabla\cdot\nabla", font_size=S_EQ)
        eq_lap.move_to(ZONE_EQ1)
        bg_lap = capsule_bg(eq_lap)
        self.play(FadeIn(bg_lap), Write(eq_lap))

        eq_exp = MathTex(
            r"\nabla^2 V =",
            r"\frac{\partial^2 V}{\partial x^2}",
            r"+\frac{\partial^2 V}{\partial y^2}",
            r"+\frac{\partial^2 V}{\partial z^2}",
            font_size=S_SUB,
        )
        eq_exp.move_to(ZONE_EQ2)
        bg_exp = capsule_bg(eq_exp)
        self.play(FadeIn(bg_exp), Write(eq_exp))

        nota = Text("Mide la curvatura del potencial en cada punto", font_size=S_NOTE, color=GREY_B)
        nota.move_to(ZONE_NOTE)
        bg_nota = capsule_bg(nota)
        self.play(FadeIn(bg_nota), FadeIn(nota))
        self.wait(2)

        # Interpretación física (bloque de texto organizado)
        interp = VGroup(
            Text("Interpretación física:", font_size=S_TXT, color=CLR_LAPL),
            MathTex(r"\nabla^2 V > 0 \;\Rightarrow\; V\text{ tiene mínimo local}", font_size=S_NOTE, color=GREY_B),
            MathTex(r"\nabla^2 V < 0 \;\Rightarrow\; V\text{ tiene máximo local}", font_size=S_NOTE, color=GREY_B),
            MathTex(r"\nabla^2 V = 0 \;\Rightarrow\; V\text{ es armónica (Laplace)}", font_size=S_NOTE, color=GREY_B),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        interp.move_to(ZONE_MID + DOWN * 1.0)
        bg_interp = capsule_bg(interp, buff=0.3)

        self.play(FadeOut(bg_nota), FadeOut(nota))
        self.play(FadeIn(bg_interp), FadeIn(interp))
        self.wait(2.5)

        self.play(*[FadeOut(m) for m in self.mobjects])

    # ═══════════════════════════════════════════════════════════════════════
    # ESCENA 8: CIERRE 3D
    # ═══════════════════════════════════════════════════════════════════════
    def escena_cierre(self):
        self.move_camera(phi=65 * DEGREES, theta=-30 * DEGREES, run_time=1.5)

        ejes = ThreeDAxes(
            x_range=[-4, 4, 1], y_range=[-4, 4, 1], z_range=[-1, 5, 1],
            x_length=6, y_length=6, z_length=4,
        )
        self.play(Create(ejes, run_time=1))

        # Superficie de potencial Coulombiano
        peak = Surface(
            lambda u, v: np.array([
                u, v,
                2 / np.sqrt(u ** 2 + v ** 2 + 0.15),
            ]),
            u_range=[-3, 3], v_range=[-3, 3],
            resolution=(30, 30),
            fill_opacity=0.4,
            stroke_width=0.5,
            stroke_color=CLR_V,
            checkerboard_colors=[CLR_E, CLR_S],
        )
        self.play(Create(peak, run_time=2))

        ef = MathTex(
            r"\nabla^2 V = -\frac{\rho}{\epsilon_0}",
            font_size=S_SUB,
        )
        ef.move_to(ZONE_TTL)
        efb = capsule_bg(ef, buff=0.25)
        self.add_fixed_in_frame_mobjects(efb, ef)
        self.play(FadeIn(efb), Write(ef))

        txt_curv = Text(
            "Pico local de carga = concavidad negativa de V",
            font_size=S_NOTE, color=CLR_POISSON,
        )
        txt_curv.next_to(ef, DOWN, buff=0.4)
        txt_curv_b = capsule_bg(txt_curv, buff=0.2)
        self.add_fixed_in_frame_mobjects(txt_curv_b, txt_curv)
        self.play(FadeIn(txt_curv_b), FadeIn(txt_curv))

        brand = Text("@lomejorphysics", font_size=S_TXT, color=CLR_Q)
        brand.move_to(ZONE_BRAND)
        self.add_fixed_in_frame_mobjects(brand)
        self.play(FadeIn(brand))

        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(3)
        self.stop_ambient_camera_rotation()

        self.remove(efb, ef, txt_curv_b, txt_curv, brand)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.5)