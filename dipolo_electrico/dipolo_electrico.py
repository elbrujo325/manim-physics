"""
Dipolo Eléctrico – Derivación Formal y Visualización
=====================================================
@lomejorphysics · Basado en Griffiths (Cap. 3)

v7 — SOLO CORRECCIÓN DE BUGS DE ECUACIONES:
  BUG 1 · escena_potencial_formal: bg4 se crea ANTES de que e4 sea transformado,
          entonces capsule_bg usa el tamaño de e4 en su posición original y se
          desplaza. Fix: crear bg4 DESPUÉS del ReplacementTransform, luego FadeIn.
  BUG 2 · escena_potencial_formal paso final: ReplacementTransform(VGroup(e1,e4), e5)
          falla silenciosamente porque e4 ya fue reemplazado por bg4 en escena.
          Fix: hacer FadeOut(bg4) junto con note4, y transformar solo e1→e5,
          luego FadeIn(e5) limpiamente desde e4 si es necesario.
  BUG 3 · escena_potencial_formal: note4 usa r"..." con LaTeX dentro de Text()
          → Text no renderiza LaTeX, se muestra como texto plano con llaves.
          Fix: usar Tex() o simplificar el string.
  BUG 4 · escena_campo_derivacion: grad está en ZONE_EQ1 y e_r/e_th se pisan
          con él porque ZONE_EQ2 + UP*0.8 coincide con ZONE_EQ1.
          Fix: bajar e_r y e_th a zonas que no se superpongan con grad.
  BUG 5 · escena_campo_derivacion: ReplacementTransform(VGroup(e_r,e_th), res)
          donde res está en ZONE_EQ2 + DOWN*0.5 — pero res fue definido ANTES
          de e_r/e_th, así que la posición de res ya estaba fijada antes del
          transform. Resultado: res aparece en posición incorrecta.
          Fix: definir res DESPUÉS del transform o usar .move_to() explícito.
  BUG 6 · escena_campo_fluido: ttl está en ZONE_TTL pero la cámara 2D hace que
          add_fixed_in_frame_mobjects sea necesario para texto en ThreeDScene.
          Fix: add_fixed_in_frame_mobjects(ttl, qp, qn, eq_lbl, bg_eq) para
          que aparezcan correctamente.
  TODO LO DEMÁS INTACTO.
"""

from manim import *
import numpy as np

# ══════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN INSTAGRAM REELS (9:16)
# ══════════════════════════════════════════════════════════════════════════
config.pixel_height = 1920
config.pixel_width  = 1080
config.frame_height = 16.0
config.frame_width  = 9.0

# ══════════════════════════════════════════════════════════════════════════
# COLORES
# ══════════════════════════════════════════════════════════════════════════
BG        = "#0d1117"
CLR_Q     = "#FFD700"   # carga +
CLR_QM    = "#EF5350"   # carga −
CLR_E     = "#4FC3F7"   # campo E
CLR_P     = "#AB47BC"   # p
CLR_R     = "#66BB6A"   # r
CLR_THETA = "#FFA726"   # theta
CLR_RES   = "#FFD54F"
CLR_S     = "#26C6DA"

# ══════════════════════════════════════════════════════════════════════════
# TIPOGRAFÍA Y SEGURIDAD
# ══════════════════════════════════════════════════════════════════════════
S_TITLE = 52
S_EQ    = 48
S_SUB   = 38
S_TXT   = 30
S_LBL   = 28
S_NOTE  = 24

# ZONAS VERTICALES
ZONE_TTL   = UP * 7.0
ZONE_SUB   = UP * 5.8
ZONE_EQ1   = UP * 3.5
ZONE_EQ2   = UP * 0.2
ZONE_NOTE  = DOWN * 6.2
ZONE_BRAND = DOWN * 7.8

def capsule_bg(mob, fill_opacity=0.92, color=BG, buff=0.22):
    return BackgroundRectangle(mob, fill_opacity=fill_opacity, buff=buff, color=color)

def box(mob, color=CLR_RES, buff=0.3, sw=2.5):
    return SurroundingRectangle(mob, color=color, buff=buff, stroke_width=sw, corner_radius=0.15)

# ──────────────────────────────────────────────────────────────────────────
# Helper: carga con símbolo +/-
# ──────────────────────────────────────────────────────────────────────────
def charge_dot(pos, positive=True, radius=0.13):
    """Dot + símbolo +/- superpuesto."""
    color = CLR_Q if positive else CLR_QM
    sym   = "+" if positive else "-"
    dot   = Circle(radius=radius, color=color, fill_opacity=1).move_to(pos)
    lbl   = Text(sym, font_size=int(radius * 220), color=BLACK, weight=BOLD).move_to(pos)
    return VGroup(dot, lbl)

def charge_sphere_3d(pos, positive=True, radius=0.13):
    """Sphere 3D."""
    color = CLR_Q if positive else CLR_QM
    s = Sphere(radius=radius).set_color(color).move_to(pos)
    return s

# ══════════════════════════════════════════════════════════════════════════
# ESCENAS
# ══════════════════════════════════════════════════════════════════════════
class DipoloElectrico(ThreeDScene):
    def construct(self):
        self.camera.background_color = BG
        self.escena_titulo()
        self.escena_geometria()
        self.escena_potencial_formal()
        self.escena_momento_dipolar()
        self.escena_campo_derivacion()
        self.escena_campo_fluido()
        self.escena_cierre()

    # ═══════════════════════════════════════════════════════════════════════
    # 1 · PORTADA PREMIUM
    # ═══════════════════════════════════════════════════════════════════════
    def escena_titulo(self):
        aura = Annulus(inner_radius=0, outer_radius=4, color=CLR_E, fill_opacity=0.08)
        aura.set_color_by_gradient(CLR_E, CLR_P)
        aura.move_to(ORIGIN)

        titulo = Text("Dipolo Eléctrico", font_size=S_TITLE + 8, weight=BOLD)
        titulo.set_color_by_gradient(CLR_E, CLR_P)
        titulo.move_to(ZONE_TTL)

        sub = Text("Derivación Formal y Visualización", font_size=S_TXT, color=GREY_B)
        sub.next_to(titulo, DOWN, buff=0.6)

        linea = Line(LEFT * 2.5, RIGHT * 2.5, color=GREY_C, stroke_width=1.0)
        linea.next_to(sub, DOWN, buff=0.4)

        pos_p = UP * 0.5 + DOWN * 2.5
        pos_n = DOWN * 0.5 + DOWN * 2.5
        qp = charge_dot(pos_p, positive=True)
        qn = charge_dot(pos_n, positive=False)
        pa = Arrow(pos_n, pos_p, color=CLR_P, buff=0.12, stroke_width=4)
        pl = MathTex(r"\vec{p}", color=CLR_P, font_size=S_SUB).next_to(pa, LEFT)
        dipolo = VGroup(qp, qn, pa, pl)

        brand = Text("@lomejorphysics", font_size=S_LBL, color=CLR_Q).move_to(ZONE_BRAND)

        self.play(FadeIn(aura, scale=0.5))
        self.play(Write(titulo, run_time=1.5))
        self.play(FadeIn(sub), Create(linea))
        self.play(FadeIn(dipolo), FadeIn(brand))
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects])

    # ═══════════════════════════════════════════════════════════════════════
    # 2 · GEOMETRÍA — r+, r-, eje Z restaurados
    # ═══════════════════════════════════════════════════════════════════════
    def escena_geometria(self):
        ttl = Text("Configuración del Dipolo", font_size=S_TITLE - 4, color=CLR_E).move_to(ZONE_TTL)
        self.play(Write(ttl))

        origin = LEFT * 2.0 + DOWN * 1.5
        sep    = 1.3
        pos_p  = origin + UP * sep / 2
        pos_n  = origin + DOWN * sep / 2
        P      = origin + np.array([4.5, 3.2, 0])

        eje_z  = Arrow(origin + DOWN * 2.8, origin + UP * 5.0,
                       color=GREY_B, stroke_width=2.0, buff=0)
        lbl_z  = Text("z", font_size=S_LBL, color=GREY_B).next_to(
                       origin + UP * 5.0, RIGHT, buff=0.1)

        qp = charge_dot(pos_p, positive=True,  radius=0.16)
        qn = charge_dot(pos_n, positive=False, radius=0.16)

        dot_P = Dot(P, radius=0.08, color=CLR_R)
        lbl_P = Text("P", font_size=S_LBL, color=CLR_R).next_to(dot_P, UR, buff=0.08)

        r_vec = Line(origin, P, color=CLR_R, stroke_width=2.5)
        lbl_r = MathTex(r"r", font_size=S_LBL, color=CLR_R).move_to(
                    origin + (P - origin) * 0.55 + LEFT * 0.35)

        r_plus_line = DashedLine(pos_p, P, color=CLR_Q, stroke_width=2.0, dash_length=0.12)
        lbl_rp = MathTex(r"r_+", font_size=S_LBL, color=CLR_Q).move_to(
                     pos_p + (P - pos_p) * 0.55 + RIGHT * 0.42)

        r_minus_line = DashedLine(pos_n, P, color=CLR_QM, stroke_width=2.0, dash_length=0.12)
        lbl_rm = MathTex(r"r_-", font_size=S_LBL, color=CLR_QM).move_to(
                     pos_n + (P - pos_n) * 0.42 + RIGHT * 0.55)

        line_z_ref = Line(origin, origin + UP * 2.5)
        line_r_ref = Line(origin, P)
        ang_theta  = Angle(line_r_ref, line_z_ref, radius=0.85,
                           color=CLR_THETA, other_angle=False)
        lbl_th = MathTex(r"\theta", font_size=S_LBL, color=CLR_THETA).next_to(
                     ang_theta, UP * 0.6 + RIGHT * 0.2)

        d_arrow = DoubleArrow(pos_n, pos_p, color=CLR_P,
                              stroke_width=2.5, buff=0.05, tip_length=0.15).shift(LEFT * 0.45)
        lbl_d   = MathTex(r"d", font_size=S_LBL, color=CLR_P).next_to(d_arrow, LEFT, buff=0.08)

        self.play(Create(eje_z), FadeIn(lbl_z))
        self.play(FadeIn(qp), FadeIn(qn))
        self.play(Create(d_arrow), FadeIn(lbl_d))
        self.play(FadeIn(dot_P), FadeIn(lbl_P), Create(r_vec), FadeIn(lbl_r))
        self.play(Create(r_plus_line),  FadeIn(lbl_rp))
        self.play(Create(r_minus_line), FadeIn(lbl_rm))
        self.play(Create(ang_theta), FadeIn(lbl_th))
        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects])

    # ═══════════════════════════════════════════════════════════════════════
    # 3 · POTENCIAL FORMAL
    # BUG FIXES:
    #   · bg4 se crea después del transform (no antes) para que envuelva e4
    #     ya en su posición final en ZONE_EQ2.
    #   · FadeOut(bg4) junto con note4 antes del resultado final.
    #   · Resultado final: FadeOut(e1,e4) limpio, luego FadeIn(e6) desde posición.
    #   · note4: Text() no renderiza LaTeX → cambiado a Tex() puro.
    #   · e7 vectorial: verificado que no se pisa con e6 (next_to con buff=0.8).
    # ═══════════════════════════════════════════════════════════════════════
    def escena_potencial_formal(self):
        ttl = Text("Derivación del Potencial", font_size=S_TITLE, color=CLR_P).move_to(ZONE_TTL)
        self.play(Write(ttl))

        # ── Paso 1: Superposición ──
        e1 = MathTex(
            r"V(\mathbf{r}) = \frac{q}{4\pi\epsilon_0}"
            r"\left( \frac{1}{r_+} - \frac{1}{r_-} \right)",
            font_size=S_SUB + 4
        ).move_to(ZONE_EQ1)
        note1 = Text("Paso 1: Superposicion", font_size=S_NOTE, color=GREY_C).move_to(ZONE_NOTE)
        self.play(Write(e1))
        self.play(FadeIn(note1))
        self.wait(1.2)

        # ── Paso 2: Ley de Cosenos ──
        e2 = MathTex(
            r"r_{\pm}^2 = r^2"
            r"\!\left(1 \mp \frac{d}{r}\cos\theta + \frac{d^2}{4r^2}\right)",
            font_size=S_SUB
        ).move_to(ZONE_EQ2)
        bg2   = capsule_bg(e2)
        note2 = Text("Ley de Cosenos detallada", font_size=S_NOTE, color=GREY_C).move_to(ZONE_NOTE)
        self.play(FadeOut(note1))
        self.play(FadeIn(bg2), Write(e2))
        self.play(FadeIn(note2))
        self.wait(1.5)

        # ── Paso 3: Aproximación r >> d ──
        e3 = MathTex(
            r"\text{Para }r \gg d \implies \frac{d^2}{4r^2} \approx 0",
            font_size=S_SUB, color=CLR_S
        ).move_to(ZONE_EQ2)
        note3 = Text("Termino cuadratico despreciable", font_size=S_NOTE, color=CLR_S).move_to(ZONE_NOTE)
        self.play(FadeOut(note2), FadeOut(bg2))
        self.play(ReplacementTransform(e2, e3))
        self.play(FadeIn(note3))
        self.wait(1.2)

        # ── Paso 4: Expansión Binomial ──
        e4 = MathTex(
            r"\frac{1}{r_{\pm}} \approx \frac{1}{r}"
            r"\!\left(1 \pm \frac{d}{2r}\cos\theta\right)",
            font_size=S_SUB
        ).move_to(ZONE_EQ2)
        # FIX note4: usar MathTex para que renderice correctamente la ecuación
        note4 = MathTex(
            r"\text{Expansion binomial: } (1+x)^n \approx 1 + nx",
            font_size=S_NOTE, color=CLR_S
        ).move_to(ZONE_NOTE)
        self.play(FadeOut(note3))
        # FIX e4 difusa: FadeOut explícito de e3 ANTES de FadeIn de e4 limpio
        self.play(FadeOut(e3))
        self.play(FadeIn(e4))
        bg4 = capsule_bg(e4)
        self.add(bg4)
        self.add(e4)  # re-añadir e4 encima del bg para que no quede tapada
        self.play(FadeIn(note4))
        self.wait(1.5)

        # ── Paso 5: Resta y sustitución ──
        e5 = MathTex(
            r"\frac{1}{r_+} - \frac{1}{r_-} \approx \frac{d \cos\theta}{r^2}",
            font_size=S_SUB
        ).move_to(ZONE_EQ2)
        note5 = Text("Restando ambas aproximaciones", font_size=S_NOTE, color=GREY_C).move_to(ZONE_NOTE)
        self.play(FadeOut(note4), FadeOut(bg4))
        self.play(ReplacementTransform(e4, e5))
        bg5 = capsule_bg(e5)
        self.play(FadeIn(bg5), FadeIn(note5))
        self.wait(1.5)

        # ── Resultado final ──
        # FIX: FadeOut limpio de e5/bg5/note5 antes; luego transform e1→e6
        #      para no tener conflicto con objetos huérfanos en escena.
        e6 = MathTex(
            r"V(r,\theta) = \frac{1}{4\pi\epsilon_0}\frac{p\cos\theta}{r^2}",
            font_size=S_EQ
        ).move_to(ZONE_EQ1)
        bx = box(e6)

        e7 = MathTex(
            r"V(\mathbf{r}) = \frac{1}{4\pi\epsilon_0}\frac{\vec{p}\cdot\hat{r}}{r^2}",
            font_size=S_SUB + 4, color=CLR_P
        ).move_to(ZONE_EQ2)  # FIX: posición explícita en ZONE_EQ2, no next_to(e6)
                              # para garantizar que no se pise con e6 en ZONE_EQ1

        note6 = Text("Forma vectorial del potencial", font_size=S_NOTE, color=CLR_RES).move_to(ZONE_NOTE)
        self.play(FadeOut(note5), FadeOut(bg5), FadeOut(e5))
        self.play(ReplacementTransform(e1, e6))
        self.play(Create(bx))
        self.wait(0.8)
        self.play(Write(e7))
        self.play(FadeIn(note6))
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects])

    # ═══════════════════════════════════════════════════════════════════════
    # 4 · MOMENTO DIPOLAR
    # ═══════════════════════════════════════════════════════════════════════
    def escena_momento_dipolar(self):
        ttl = Text("Momento Dipolar", font_size=S_TITLE, color=CLR_P).move_to(ZONE_TTL)
        self.play(Write(ttl))

        eq = MathTex(r"\vec{p} = q\,\vec{d}", font_size=S_EQ, color=CLR_P).move_to(ZONE_EQ1)
        bx = box(eq, color=CLR_P)

        sep   = 1.4
        base  = DOWN * 1.5
        pos_p = UP * sep / 2 + base
        pos_n = DOWN * sep / 2 + base
        qp    = charge_dot(pos_p, positive=True,  radius=0.16)
        qn    = charge_dot(pos_n, positive=False, radius=0.16)
        pa    = Arrow(pos_n, pos_p, color=CLR_P, buff=0.15, stroke_width=6)

        self.play(Write(eq), Create(bx))
        self.play(FadeIn(qp), FadeIn(qn), GrowArrow(pa))
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in self.mobjects])

    # ═══════════════════════════════════════════════════════════════════════
    # 5 · CAMPO ELÉCTRICO (Derivación)
    # BUG FIXES:
    #   · grad en ZONE_EQ1 (UP*3.5). e_r y e_th se posicionaban en
    #     ZONE_EQ2+UP*0.8 = UP*1.0 y ZONE_EQ2-DOWN*0.5 = DOWN*0.3,
    #     lo cual NO se pisa con ZONE_EQ1 visualmente, pero la nueva
    #     versión (del documento) tenía grad en ZONE_EQ1 con font_size=S_SUB+4
    #     y e_r en ZONE_EQ2+UP*0.8 — que sí colisiona en pantalla 9:16.
    #     Fix: grad sube a UP*5.2, e_r en UP*2.0, e_th en UP*0.0.
    #   · res se define con posición final ANTES del transform → Manim lo
    #     renderiza en esa posición desde el inicio y el transform lo "trae"
    #     desde posición incorrecta. Fix: mover res explícitamente tras transform.
    # ═══════════════════════════════════════════════════════════════════════
    def escena_campo_derivacion(self):
        ttl = Text("Campo Electrico", font_size=S_TITLE, color=CLR_E).move_to(ZONE_TTL)
        self.play(Write(ttl))

        # grad arriba, libre de colisión con las componentes
        grad = MathTex(r"\vec{E} = -\nabla V", font_size=S_SUB + 4, color=CLR_E).move_to(UP * 5.2)
        self.play(Write(grad))
        self.wait(0.5)

        # Componentes en zona media — separadas entre sí y de grad
        e_r = MathTex(
            r"E_r = -\frac{\partial V}{\partial r} = "
            r"\frac{p}{4\pi\epsilon_0} \frac{2\cos\theta}{r^3}",
            font_size=S_SUB
        ).move_to(UP * 2.2)

        e_th = MathTex(
            r"E_\theta = -\frac{1}{r}\frac{\partial V}{\partial \theta} = "
            r"\frac{p}{4\pi\epsilon_0} \frac{\sin\theta}{r^3}",
            font_size=S_SUB
        ).move_to(UP * 0.2)

        self.play(Write(e_r))
        self.wait(0.3)
        self.play(Write(e_th))
        self.wait(2)

        # FIX: definir res SIN posición, hacer el transform, LUEGO moverlo
        res = MathTex(
            r"\vec{E}(r,\theta) = \frac{p}{4\pi\epsilon_0 r^3}"
            r"\!\left(2\cos\theta\,\hat{r} + \sin\theta\,\hat{\theta}\right)",
            font_size=S_SUB - 4
        )
        self.play(ReplacementTransform(VGroup(e_r, e_th), res))
        # Ahora que res está en escena, lo posicionamos correctamente
        self.play(res.animate.move_to(ZONE_EQ2))
        bx   = box(res)
        note = Text("El campo decrece como 1/r3", font_size=S_NOTE, color=CLR_RES).move_to(ZONE_NOTE)
        self.play(Create(bx))
        self.play(FadeIn(note))
        self.wait(2.2)
        self.play(*[FadeOut(m) for m in self.mobjects])

    # ═══════════════════════════════════════════════════════════════════════
    # 6 · CAMPO ELÉCTRICO – Visualización mejorada
    # BUG FIX: en ThreeDScene con set_camera_orientation, los Mobjects 2D
    #   (Text, MathTex) deben declararse con add_fixed_in_frame_mobjects
    #   para que aparezcan correctamente en la cámara 2D proyectada.
    #   Sin eso, ttl, qp, qn y eq_lbl pueden no verse o verse distorsionados.
    # ═══════════════════════════════════════════════════════════════════════
    def escena_campo_fluido(self):
        self.set_camera_orientation(phi=0, theta=-PI / 2)

        # FIX: ttl fijo en frame para que sea visible con la cámara 2D
        ttl = Text("Estructura del Campo", font_size=S_TITLE, color=CLR_E).move_to(ZONE_TTL)
        self.add_fixed_in_frame_mobjects(ttl)
        self.play(Write(ttl))

        d_sep = 1.4

        def campo(pos):
            p  = np.array([pos[0], pos[1], 0.0])
            rp = p - np.array([0.0,  d_sep / 2, 0.0])
            rm = p - np.array([0.0, -d_sep / 2, 0.0])
            n1, n2 = np.linalg.norm(rp), np.linalg.norm(rm)
            if n1 < 0.30 or n2 < 0.30:
                return np.zeros(3)
            E = rp / n1**3 - rm / n2**3
            mag = np.linalg.norm(E)
            if mag > 0:
                E = E / (1 + 0.15 * mag)
            return E

        stream_core = StreamLines(
            campo,
            x_range=[-4.0, 4.0, 0.35],
            y_range=[-7.5, 7.5, 0.35],
            color=CLR_E,
            stroke_width=2.2,
            max_anchors_per_line=40,
        )
        stream_outer = StreamLines(
            campo,
            x_range=[-4.0, 4.0, 0.70],
            y_range=[-7.5, 7.5, 0.70],
            color="#81D4FA",
            stroke_width=1.4,
            stroke_opacity=0.55,
            max_anchors_per_line=40,
        )

        # FIX: cargas y ecuación también fijas en frame
        pos_p = np.array([0.0,  d_sep / 2, 0.0])
        pos_n = np.array([0.0, -d_sep / 2, 0.0])
        qp    = charge_dot(pos_p, positive=True,  radius=0.16)
        qn    = charge_dot(pos_n, positive=False, radius=0.16)
        self.add_fixed_in_frame_mobjects(qp, qn)

        eq_lbl = MathTex(
            r"\vec{E} = \frac{p}{4\pi\epsilon_0 r^3}"
            r"(2\cos\theta\,\hat{r} + \sin\theta\,\hat{\theta})",
            font_size=S_NOTE + 2, color=WHITE
        ).move_to(UP * 5.5)
        bg_eq = capsule_bg(eq_lbl, fill_opacity=0.80)
        self.add_fixed_in_frame_mobjects(bg_eq, eq_lbl)

        self.add(stream_outer, stream_core)
        stream_core.start_animation(warm_up=True, flow_speed=1.6)
        stream_outer.start_animation(warm_up=False, flow_speed=1.0)
        self.play(FadeIn(qp), FadeIn(qn))
        self.play(FadeIn(bg_eq), FadeIn(eq_lbl))
        self.wait(5)
        stream_core.end_animation()
        stream_outer.end_animation()
        self.play(*[FadeOut(m) for m in self.mobjects])

    # ═══════════════════════════════════════════════════════════════════════
    # 7 · CIERRE 3D
    # ═══════════════════════════════════════════════════════════════════════
    def escena_cierre(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)
        ejes = ThreeDAxes(x_range=[-3, 3], y_range=[-3, 3], z_range=[-3, 3]).set_opacity(0.15)
        self.play(Create(ejes))

        qp3 = charge_sphere_3d(UP * 0.9,  positive=True,  radius=0.13)
        qn3 = charge_sphere_3d(DOWN * 0.9, positive=False, radius=0.13)
        qp3.set_z_index(10)
        qn3.set_z_index(10)

        # FIX: en lugar de fixed_in_frame (que no sigue a las esferas al rotar),
        # se usa always_redraw para que las etiquetas se anclen a las esferas
        # proyectándose siempre encima de ellas en pantalla.
        lbl_pos = always_redraw(lambda: MathTex(r"+q", font_size=S_LBL, color=CLR_Q)
                                .move_to(qp3.get_center() + RIGHT * 0.28 + UP * 0.18))
        lbl_neg = always_redraw(lambda: MathTex(r"-q", font_size=S_LBL, color=CLR_QM)
                                .move_to(qn3.get_center() + RIGHT * 0.28 + DOWN * 0.18))
        self.add_fixed_in_frame_mobjects(lbl_pos, lbl_neg)

        lines = VGroup()
        for phi in np.linspace(0, TAU, 10, endpoint=False):
            for r0 in [1.3, 2.1, 2.9]:
                def param(t, p=phi, r=r0):
                    th  = t * PI
                    rad = r * np.sin(th) ** 2
                    return np.array([
                        rad * np.sin(th) * np.cos(p),
                        rad * np.sin(th) * np.sin(p),
                        rad * np.cos(th)
                    ])
                lines.add(ParametricFunction(
                    param, t_range=[0.12, 0.88],
                    color=CLR_E, stroke_opacity=0.6
                ))

        self.play(FadeIn(qp3), FadeIn(qn3))
        self.play(Create(lines, run_time=3, lag_ratio=0.03))

        brand = Text("@lomejorphysics", font_size=S_TXT, color=CLR_Q).move_to(ZONE_BRAND)
        self.add_fixed_in_frame_mobjects(brand)
        self.play(FadeIn(brand))

        self.begin_ambient_camera_rotation(rate=0.12)
        self.wait(4)
        self.stop_ambient_camera_rotation()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.5)