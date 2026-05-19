"""
Energía Electrostática – Del Trabajo al Campo
=========================================================
@lomejorphysics · Griffiths Cap. 2.4

v5 — Ajustes Teóricos y Estilos Finales (Iteración de Fluido Dinámico y Condensadores)
"""
from manim import *
import numpy as np

# ══════════════════════════════════════════════════════════════════════════
# COLORES (Paleta @lomejorphysics)
# ══════════════════════════════════════════════════════════════════════════
BG       = "#0d1117"
CLR_Q    = "#FFD700"
CLR_E    = "#4FC3F7"
CLR_W    = "#FF7043"
CLR_U    = "#AB47BC"
CLR_DENS = "#26C6DA"
CLR_RES  = "#FFD54F"
CLR_QM   = "#EF5350"
CLR_N    = "#66BB6A"

# ══════════════════════════════════════════════════════════════════════════
# TIPOGRAFÍA
# ══════════════════════════════════════════════════════════════════════════
S_TITLE = 76
S_EQ    = 52
S_SUB   = 42
S_TXT   = 34
S_LBL   = 30
S_NOTE  = 26

ZONE_TTL  = UP * 3.6
ZONE_EQ   = UP * 0.6
ZONE_EQ2  = DOWN * 1.0
ZONE_NOTE = DOWN * 3.3

def capsule_bg(mob, fill_op=0.92, color=BG, buff=0.22):
    return BackgroundRectangle(mob, fill_opacity=fill_op, buff=buff, color=color).set_z_index(-1)

def caja(mob, color=CLR_RES, buff=0.3, sw=2.5):
    return SurroundingRectangle(mob, color=color, buff=buff, stroke_width=sw, corner_radius=0.15)

def charge_dot(pos, positive=True, radius=0.13):
    color = CLR_Q if positive else CLR_QM
    sym = "+" if positive else "-"
    dot = Circle(radius=radius, color=color, fill_opacity=1).move_to(pos)
    lbl = Text(sym, font_size=int(radius * 200), color=BLACK, weight=BOLD).move_to(pos)
    return VGroup(dot, lbl)

def paso_label(txt):
    p = Text(txt, font_size=S_NOTE, color=GREY_C).move_to(ZONE_NOTE)
    return p

# ══════════════════════════════════════════════════════════════════════════
# ESCENA PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════
class EnergiaElectrostatica(ThreeDScene):
    def construct(self):
        # Proporciones de cámara vertical (9:16)
        
        self.camera.background_color = BG
        self.escena_titulo()
        self.escena_trabajo_deduccion()
        self.escena_ensamblaje_visual()
        self.escena_formula_general()
        self.escena_forma_simetrica()
        self.escena_distribucion_continua()
        self.escena_derivacion_densidad()
        self.escena_condensador_deduccion()
        self.escena_cierre()

    def escena_titulo(self):
        self.set_camera_orientation(phi=0, theta=-PI / 2)
        titulo = Text("Energía Electrostática", font_size=S_TITLE).set_color_by_gradient(CLR_W, CLR_U).move_to(ZONE_TTL + DOWN * 0.3)
        sub = Text("Del trabajo contra el campo\na la energía del campo", font_size=S_TXT, color=GREY_B, line_spacing=1.2).next_to(titulo, DOWN, buff=0.5)
        linea = Line(LEFT * 2.5, RIGHT * 2.5, color=CLR_W, stroke_width=1.5).next_to(sub, DOWN, buff=0.4)
        fuente = Text("Griffiths · Capítulo 2.4", font_size=S_NOTE, color=GREY_C).next_to(linea, DOWN, buff=0.4)
        brand = Text("@lomejorphysics", font_size=S_LBL, color=CLR_Q).move_to(ZONE_NOTE + DOWN * 0.3)

        q = Dot(LEFT * 1.5 + DOWN * 1.6, radius=0.12, color=CLR_Q)
        fl = Arrow(LEFT * 2 + DOWN * 1.6, RIGHT * 2 + DOWN * 1.6, color=CLR_E, stroke_width=3, buff=0)
        lbl_e = MathTex(r"\vec{E}", font_size=S_NOTE, color=CLR_E).next_to(fl, DOWN, buff=0.15)

        self.play(Write(titulo, run_time=1.5))
        self.play(FadeIn(sub), GrowFromCenter(linea))
        self.play(FadeIn(fuente), FadeIn(brand))
        self.play(FadeIn(q), FadeIn(fl), FadeIn(lbl_e))
        self.play(q.animate.move_to(RIGHT * 0.5 + DOWN * 1.6), run_time=1.5)
        self.wait(1)
        self.play(*[FadeOut(m) for m in self.mobjects])

    def escena_trabajo_deduccion(self):
        self.set_camera_orientation(phi=0, theta=-PI / 2)
        ttl = Text("Trabajo contra el Campo", font_size=S_TITLE, color=CLR_W).move_to(ZONE_TTL)
        self.play(Write(ttl))
        campo = VGroup(*[Arrow(LEFT * 3 + UP * y, RIGHT * 3 + UP * y, color=CLR_E, stroke_width=1.2, buff=0, stroke_opacity=0.2) for y in [-1.5, -0.5, 0.5, 1.5]])
        self.play(FadeIn(campo))

        e1 = MathTex(r"\vec{F}_e", r"=", r"Q", r"\vec{E}", font_size=S_EQ).move_to(ZONE_EQ)
        e1[0].set_color(CLR_W); e1[2].set_color(CLR_Q); e1[3].set_color(CLR_E)
        bg1 = capsule_bg(e1)
        p1 = paso_label("Paso 1 · Fuerza eléctrica sobre Q")
        self.play(FadeIn(bg1), Write(e1), FadeIn(p1))
        self.wait(1); self.play(FadeOut(p1))

        e2 = MathTex(r"\vec{F}_{ext}", r"=", r"-Q", r"\vec{E}", font_size=S_EQ).move_to(ZONE_EQ)
        e2[0].set_color(CLR_N); e2[2].set_color(CLR_Q); e2[3].set_color(CLR_E)
        bg2 = capsule_bg(e2)
        p2 = paso_label("Paso 2 · Fuerza mínima del agente externo")
        self.play(FadeOut(bg1), ReplacementTransform(e1, e2), FadeIn(bg2), FadeIn(p2))
        self.wait(1); self.play(FadeOut(p2))

        e3 = MathTex(r"W", r"=", r"\int_a^b", r"\vec{F}_{ext}", r"\cdot", r"d\vec{l}", font_size=S_EQ).move_to(ZONE_EQ)
        e3[0].set_color(CLR_W); e3[3].set_color(CLR_N); e3[5].set_color(CLR_W)
        bg3 = capsule_bg(e3)
        p3 = paso_label("Paso 3 · Definición de trabajo mecánico")
        self.play(FadeOut(bg2), ReplacementTransform(e2, e3), FadeIn(bg3), FadeIn(p3))
        self.wait(1); self.play(FadeOut(p3))

        e4 = MathTex(r"W", r"=", r"-Q", r"\int_a^b", r"\vec{E}", r"\cdot", r"d\vec{l}", font_size=S_EQ).move_to(ZONE_EQ)
        e4[0].set_color(CLR_W); e4[2].set_color(CLR_Q); e4[4].set_color(CLR_E); e4[6].set_color(CLR_W)
        bg4 = capsule_bg(e4)
        p4 = paso_label("Paso 4 · Sustituir Fₑₓₜ = −QE")
        self.play(FadeOut(bg3), ReplacementTransform(e3, e4), FadeIn(bg4), FadeIn(p4))
        self.wait(1); self.play(FadeOut(p4))

        e5 = MathTex(r"W", r"=", r"Q", r"\left[", r"V(\mathbf{b})", r"-", r"V(\mathbf{a})", r"\right]", font_size=S_SUB).move_to(ZONE_EQ)
        e5[0].set_color(CLR_W); e5[2].set_color(CLR_Q); e5[4].set_color(CLR_U); e5[6].set_color(CLR_U)
        bg5 = capsule_bg(e5)
        p5 = paso_label("Paso 5 · Definición de potencial eléctrico")
        self.play(FadeOut(bg4), ReplacementTransform(e4, e5), FadeIn(bg5), FadeIn(p5))
        self.wait(1.5); self.play(FadeOut(p5))

        e6 = MathTex(r"W", r"=", r"Q", r"V(\mathbf{r})", font_size=S_EQ).move_to(ZONE_EQ)
        e6[0].set_color(CLR_W); e6[2].set_color(CLR_Q); e6[3].set_color(CLR_U)
        bg6 = capsule_bg(e6)
        bx6 = caja(e6, color=CLR_W)
        p6 = paso_label("Resultado · Si V(∞)=0 → W = QV(r)").set_color(CLR_RES)
        self.play(FadeOut(bg5), ReplacementTransform(e5, e6), FadeIn(bg6), FadeIn(p6))
        self.play(Create(bx6))
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects])

    def escena_ensamblaje_visual(self):
        self.set_camera_orientation(phi=0, theta=-PI / 2)
        ttl = Text("Ensamblaje de Cargas", font_size=S_TITLE, color=CLR_U).move_to(ZONE_TTL)
        self.play(Write(ttl))

        p1 = LEFT * 1.8 + DOWN * 0.5
        p2 = RIGHT * 1.8 + DOWN * 0.5
        p3 = UP * 1.5

        q1 = charge_dot(LEFT * 4.5 + DOWN * 0.5, positive=True, radius=0.15)
        l1 = MathTex("q_1", font_size=S_LBL, color=CLR_Q)
        l1.add_updater(lambda m: m.next_to(q1, DOWN, buff=0.12))

        q2 = charge_dot(RIGHT * 4.5 + DOWN * 0.5, positive=True, radius=0.15)
        l2 = MathTex("q_2", font_size=S_LBL, color=CLR_Q)
        l2.add_updater(lambda m: m.next_to(q2, DOWN, buff=0.12))

        q3 = charge_dot(UP * 4.5, positive=True, radius=0.15)
        l3 = MathTex("q_3", font_size=S_LBL, color=CLR_Q)
        l3.add_updater(lambda m: m.next_to(q3, RIGHT, buff=0.12))

        # Vector Field variables
        v1, v2, v3 = ValueTracker(0), ValueTracker(0), ValueTracker(0)

        def func_campo(pos):
            val = np.array([0.0, 0.0, 0.0])
            for q, v in [(q1, v1), (q2, v2), (q3, v3)]:
                m = v.get_value()
                if m > 0.05:
                    r_vec = pos[:2] - q.get_center()[:2]
                    r = np.linalg.norm(r_vec) + 1e-3
                    if r < 0.3: r = 0.3
                    E = (r_vec/r) * min(1.8, 0.8/r**1.8) * m
                    val += np.array([E[0], E[1], 0])
            return val

        campo_vec = always_redraw(lambda: ArrowVectorField(
            func_campo, x_range=[-4, 4, 0.7], y_range=[-3, 2, 0.7],
            color=CLR_E, length_func=lambda n: 0.45 * (1 - np.exp(-n))
        ).set_z_index(-2).set_opacity(0.4 if v1.get_value() > 0 else 0))
        self.add(campo_vec)

        # Q1 entra
        self.play(FadeIn(q1), FadeIn(l1), v1.animate.set_value(1))
        eq_w1 = MathTex(r"W_1", r"=", r"0", font_size=S_SUB).move_to(ZONE_EQ)
        eq_w1[0].set_color(CLR_W)
        bg_w1 = capsule_bg(eq_w1)
        n1 = paso_label("No hay campo previo → trabajo nulo")
        self.play(FadeIn(bg_w1), Write(eq_w1), FadeIn(n1))
        self.play(q1.animate.move_to(p1), run_time=1.5, rate_func=rate_functions.ease_in_out_sine)
        self.play(Flash(p1, color=CLR_Q, line_length=0.15, num_lines=8, flash_radius=0.3, run_time=0.5))
        l1.clear_updaters(); l1.next_to(q1, DOWN, buff=0.12)

        # Q2 entra
        self.play(FadeOut(bg_w1), FadeOut(eq_w1), FadeOut(n1))
        self.play(FadeIn(q2), FadeIn(l2), v2.animate.set_value(1))
        w2a = MathTex(r"W_2", r"=", r"q_2", r"V_1(\mathbf{r}_2)", font_size=S_SUB).move_to(ZONE_EQ)
        w2a[0].set_color(CLR_W); w2a[2].set_color(CLR_Q); w2a[3].set_color(CLR_U)
        bg_w2a = capsule_bg(w2a)
        n2a = paso_label("W₂ = q₂ × potencial de q₁ en r₂")
        self.play(FadeIn(bg_w2a), Write(w2a), FadeIn(n2a))
        self.wait(0.8)

        w2b = MathTex(r"W_2", r"=", r"\frac{1}{4\pi\epsilon_0}", r"\frac{q_1 q_2}{r_{12}}", font_size=S_SUB).move_to(ZONE_EQ)
        w2b[0].set_color(CLR_W)
        bg_w2b = capsule_bg(w2b)
        n2b = paso_label("Sustituir V₁ = q₁/(4πε₀r₁₂)")
        self.play(FadeOut(bg_w2a), FadeOut(n2a), ReplacementTransform(w2a, w2b), FadeIn(bg_w2b), FadeIn(n2b))

        self.play(q2.animate.move_to(p2), run_time=1.5, rate_func=rate_functions.ease_in_out_sine)
        self.play(Flash(p2, color=CLR_Q, line_length=0.15, num_lines=8, flash_radius=0.3, run_time=0.5))
        l2.clear_updaters(); l2.next_to(q2, DOWN, buff=0.12)
        r12_line = DashedLine(p1, p2, color=GREY_B, stroke_width=1.5, dash_length=0.1)
        lr12 = MathTex("r_{12}", font_size=S_NOTE - 2, color=GREY_B).move_to((p1 + p2) / 2 + DOWN * 0.3)
        self.play(Create(r12_line), FadeIn(lr12))
        self.wait(0.8)

        # Q3 entra
        self.play(FadeOut(bg_w2b), FadeOut(w2b), FadeOut(n2b))
        self.play(FadeIn(q3), FadeIn(l3), v3.animate.set_value(1))
        w3a = MathTex(r"W_3", r"=", r"q_3", r"\left[V_1(\mathbf{r}_3) + V_2(\mathbf{r}_3)\right]", font_size=S_SUB - 4).move_to(ZONE_EQ)
        w3a[0].set_color(CLR_W); w3a[2].set_color(CLR_Q)
        bg_w3a = capsule_bg(w3a)
        n3a = paso_label("q₃ interactúa contra el campo vectorial V(1+2)")
        self.play(FadeIn(bg_w3a), Write(w3a), FadeIn(n3a))
        self.wait(0.8)

        w3b = MathTex(r"W_3", r"=", r"\frac{1}{4\pi\epsilon_0}", r"q_3\!\left(\frac{q_1}{r_{13}}+\frac{q_2}{r_{23}}\right)", font_size=S_SUB - 6).move_to(ZONE_EQ)
        w3b[0].set_color(CLR_W)
        bg_w3b = capsule_bg(w3b)
        n3b = paso_label("Sustituir ambas contribuciones previas de V")
        self.play(FadeOut(bg_w3a), FadeOut(n3a), ReplacementTransform(w3a, w3b), FadeIn(bg_w3b), FadeIn(n3b))

        self.play(q3.animate.move_to(p3), run_time=1.5, rate_func=rate_functions.ease_in_out_sine)
        self.play(Flash(p3, color=CLR_Q, line_length=0.15, num_lines=8, flash_radius=0.3, run_time=0.5))
        l3.clear_updaters(); l3.next_to(q3, RIGHT, buff=0.12)
        r13_line = DashedLine(p1, p3, color=GREY_B, stroke_width=1.5, dash_length=0.1)
        r23_line = DashedLine(p2, p3, color=GREY_B, stroke_width=1.5, dash_length=0.1)
        self.play(Create(r13_line), Create(r23_line))
        
        self.wait(1)
        campo_vec.clear_updaters()
        self.play(*[FadeOut(m) for m in self.mobjects])

    def escena_formula_general(self):
        self.set_camera_orientation(phi=0, theta=-PI / 2)
        ttl = Text("Energía Total", font_size=S_TITLE, color=CLR_U).move_to(ZONE_TTL)
        self.play(Write(ttl))

        e1 = MathTex(r"W_{total}", r"=", r"W_1", r"+", r"W_2", r"+", r"W_3", r"+ \cdots", font_size=S_SUB).move_to(ZONE_EQ)
        e1[0].set_color(CLR_W); e1[2].set_color(CLR_W); e1[4].set_color(CLR_W); e1[6].set_color(CLR_W)
        bg1 = capsule_bg(e1)
        p1 = paso_label("Paso 1 · Sumar trabajo de cada carga")
        self.play(FadeIn(bg1), Write(e1), FadeIn(p1))
        self.wait(1); self.play(FadeOut(p1))

        e2 = MathTex(r"W", r"=", r"\frac{1}{4\pi\epsilon_0}", r"\left(", r"\frac{q_1 q_2}{r_{12}}", r"+\frac{q_1 q_3}{r_{13}}", r"+\frac{q_2 q_3}{r_{23}}", r"+\cdots\right)", font_size=S_SUB - 6).move_to(ZONE_EQ)
        e2[0].set_color(CLR_W)
        bg2 = capsule_bg(e2)
        p2 = paso_label("Paso 2 · Cada par contribuye un término")
        self.play(FadeOut(bg1), ReplacementTransform(e1, e2), FadeIn(bg2), FadeIn(p2))
        self.wait(1.5); self.play(FadeOut(p2))

        e3 = MathTex(r"W", r"=", r"\frac{1}{4\pi\epsilon_0}", r"\sum_{i=1}^{n}", r"\sum_{j>i}", r"\frac{q_i q_j}{r_{ij}}", font_size=S_EQ - 4).move_to(ZONE_EQ)
        e3[0].set_color(CLR_W)
        bg3 = capsule_bg(e3)
        bx3 = caja(e3, color=CLR_W)
        p3 = paso_label("Resultado · j > i evita contar pares dos veces").set_color(CLR_RES)
        self.play(FadeOut(bg2), ReplacementTransform(e2, e3), FadeIn(bg3), FadeIn(p3))
        self.play(Create(bx3))
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects])

    def escena_forma_simetrica(self):
        self.set_camera_orientation(phi=0, theta=-PI / 2)
        ttl = Text("Forma Simétrica", font_size=S_TITLE, color=CLR_U).move_to(ZONE_TTL)
        self.play(Write(ttl))

        e1 = MathTex(r"W", r"=", r"\frac{1}{2}", r"\frac{1}{4\pi\epsilon_0}", r"\sum_{i=1}^{n}", r"\sum_{j \neq i}", r"\frac{q_i q_j}{r_{ij}}", font_size=S_SUB - 4).move_to(ZONE_EQ)
        e1[0].set_color(CLR_W); e1[2].set_color(CLR_U)
        bg1 = capsule_bg(e1)
        p1 = paso_label("Paso 1 · Contar cada par dos veces → factor ½")
        self.play(FadeIn(bg1), Write(e1), FadeIn(p1))
        self.wait(1.2); self.play(FadeOut(p1))

        e2a = MathTex(r"V(\mathbf{r}_i)", r"=", r"\frac{1}{4\pi\epsilon_0}", r"\sum_{j \neq i}", r"\frac{q_j}{r_{ij}}", font_size=S_SUB - 2).move_to(ZONE_EQ2)
        e2a[0].set_color(CLR_U)
        bg2a = capsule_bg(e2a)
        p2 = paso_label("Paso 2 · La suma interna ES el potencial V(rᵢ)")
        self.play(FadeIn(bg2a), Write(e2a), FadeIn(p2))
        self.wait(1.2); self.play(FadeOut(p2))

        e3 = MathTex(r"W", r"=", r"\frac{1}{2}", r"\sum_{i=1}^{n}", r"q_i", r"V(\mathbf{r}_i)", font_size=S_EQ).move_to(ZONE_EQ)
        e3[0].set_color(CLR_W); e3[2].set_color(CLR_U); e3[4].set_color(CLR_Q); e3[5].set_color(CLR_U)
        bg3 = capsule_bg(e3)
        bx3 = caja(e3, color=CLR_U)
        p3 = paso_label("Resultado · W = ½ Σ qᵢV(rᵢ)").set_color(CLR_RES)
        self.play(FadeOut(bg1), FadeOut(e1), FadeOut(bg2a), FadeOut(e2a))
        self.play(FadeIn(bg3), Write(e3), FadeIn(p3))
        self.play(Create(bx3))
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects])

    def escena_distribucion_continua(self):
        self.set_camera_orientation(phi=0, theta=-PI / 2)
        ttl = Text("Distribución Continua", font_size=S_TITLE, color=CLR_U).move_to(ZONE_TTL)
        self.play(Write(ttl))

        e1 = MathTex(r"W", r"=", r"\frac{1}{2}", r"\sum_{i=1}^{n}", r"q_i", r"V(\mathbf{r}_i)", font_size=S_SUB).move_to(ZONE_EQ)
        e1[0].set_color(CLR_W); e1[2].set_color(CLR_U); e1[4].set_color(CLR_Q)
        bg1 = capsule_bg(e1)
        p1 = paso_label("Punto de partida: forma discreta")
        self.play(FadeIn(bg1), Write(e1), FadeIn(p1))
        self.wait(1); self.play(FadeOut(p1))

        e2a = MathTex(r"q_i", r"\longrightarrow", r"\rho\, d\tau", font_size=S_SUB, color=CLR_Q).move_to(ZONE_EQ2)
        bg2a = capsule_bg(e2a)
        p2 = paso_label("Paso 2 · Carga discreta → fluido suave (densidad × Vol)")
        self.play(FadeIn(bg2a), Write(e2a), FadeIn(p2))
        self.wait(1); self.play(FadeOut(p2))

        e3 = MathTex(r"W", r"=", r"\frac{1}{2}", r"\int", r"\rho", r"V", r"\, d\tau", font_size=S_EQ).move_to(ZONE_EQ)
        e3[0].set_color(CLR_W); e3[2].set_color(CLR_U); e3[4].set_color(CLR_Q); e3[5].set_color(CLR_U)
        bg3 = capsule_bg(e3)
        bx3 = caja(e3, color=CLR_U)
        p3 = paso_label("Resultado · Forma integral para ρ (Incluye Auto-Energía)").set_color(CLR_RES)
        self.play(FadeOut(bg1), FadeOut(e1), FadeOut(bg2a), FadeOut(e2a))
        self.play(FadeIn(bg3), Write(e3), FadeIn(p3))
        self.play(Create(bx3))
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects])

    def escena_derivacion_densidad(self):
        self.set_camera_orientation(phi=0, theta=-PI / 2)
        ttl = Text("Densidad del Campo", font_size=S_TITLE, color=CLR_DENS).move_to(ZONE_TTL)
        self.play(Write(ttl))

        e1 = MathTex(r"W", r"=", r"\frac{1}{2}", r"\int", r"\rho", r"V", r"\, d\tau", font_size=S_SUB).move_to(ZONE_EQ)
        e1[0].set_color(CLR_W); e1[4].set_color(CLR_Q); e1[5].set_color(CLR_U)
        p1 = paso_label("Paso 1 · Forma con densidad de carga")
        self.play(Write(e1), FadeIn(p1))
        self.wait(1); self.play(FadeOut(p1))

        e2 = MathTex(r"W", r"=", r"\frac{\epsilon_0}{2}", r"\int", r"(\nabla\!\cdot\!\vec{E})", r"V", r"\, d\tau", font_size=S_SUB).move_to(ZONE_EQ)
        e2[0].set_color(CLR_W); e2[4].set_color(CLR_E); e2[5].set_color(CLR_U)
        p2 = paso_label("Paso 2 · Ley de Gauss: ρ = ε₀∇·E")
        self.play(ReplacementTransform(e1, e2, run_time=2), FadeIn(p2))
        self.wait(1.2); self.play(FadeOut(p2))

        ident = MathTex(r"\nabla\!\cdot\!(V\vec{E})", r"=", r"V(\nabla\!\cdot\!\vec{E})", r"+", r"\vec{E}\!\cdot\!(\nabla V)", font_size=S_SUB - 4, color=CLR_N).move_to(ZONE_EQ2)
        bg_id = capsule_bg(ident)
        p3 = paso_label("Paso 3 · Identidad del gradiente")
        self.play(FadeIn(bg_id), Write(ident), FadeIn(p3))
        self.wait(1.5); self.play(FadeOut(p3), FadeOut(bg_id), FadeOut(ident))

        e4 = MathTex(r"W", r"=", r"\frac{\epsilon_0}{2}", r"\left[", r"\int E^2\, d\tau", r"+", r"\oint_{S} V\vec{E}\!\cdot\! d\vec{a}", r"\right]", font_size=S_SUB - 6).move_to(ZONE_EQ)
        e4[0].set_color(CLR_W); e4[4].set_color(CLR_E); e4[6].set_color(GREY_B)
        p4 = paso_label("Paso 4 · Integ. por partes + ∇V = −E")
        self.play(ReplacementTransform(e2, e4, run_time=2), FadeIn(p4))
        self.wait(1.2); self.play(FadeOut(p4))

        cross = Cross(e4[6], color=CLR_QM, stroke_width=3)
        # Deducción de límite al infinito
        p5_r1 = MathTex(r"V \sim \frac{1}{r}, \quad E \sim \frac{1}{r^2}, \quad da \sim r^2", font_size=S_NOTE, color=CLR_QM).move_to(ZONE_NOTE + UP*0.4)
        p5_r2 = MathTex(r"\implies \oint \sim \left(\frac{1}{r^3}\right)r^2 = \frac{1}{r} \xrightarrow{r\to\infty} 0", font_size=S_NOTE, color=CLR_QM).next_to(p5_r1, DOWN, buff=0.15)
        
        self.play(Create(cross), FadeIn(p5_r1))
        self.play(FadeIn(p5_r2))
        self.wait(2.5)

        e6 = MathTex(r"W", r"=", r"\frac{\epsilon_0}{2}", r"\int_{\text{todo}}", r"E^2", r"\, d\tau", font_size=S_EQ).move_to(ZONE_EQ)
        e6[0].set_color(CLR_W); e6[4].set_color(CLR_E)
        bx6 = caja(e6, color=CLR_DENS)
        p6 = paso_label("¡La energía la almacena la tensión del campo!").set_color(CLR_DENS)
        self.play(FadeOut(cross), FadeOut(p5_r1), FadeOut(p5_r2))
        self.play(ReplacementTransform(e4, e6, run_time=2), FadeIn(p6))
        self.play(Create(bx6))
        self.wait(2)

        # ── EXPERIMENTO DE ARREGLO ELECTROSTÁTICO / FLUIDO DINÁMICO ──
        ttl_dens = Text("Energía de un Arreglo Electrostático", font_size=S_SUB+10, color=CLR_DENS).move_to(ZONE_TTL)
        self.play(ReplacementTransform(ttl, ttl_dens), FadeOut(bx6), FadeOut(e6), FadeOut(p6))

        carga1 = Dot(LEFT*2.5 + DOWN*0.6, radius=0.14, color=CLR_Q, z_index=3)
        lbl_c1 = MathTex("+q_1", font_size=S_NOTE, color=CLR_Q)
        lbl_c1.add_updater(lambda m: m.next_to(carga1, DOWN, buff=0.15))
        
        carga2 = Dot(RIGHT*4.5 + DOWN*0.6, radius=0.14, color=CLR_Q, z_index=3)
        lbl_c2 = MathTex("+q_2", font_size=S_NOTE, color=CLR_Q)
        lbl_c2.add_updater(lambda m: m.next_to(carga2, DOWN, buff=0.15))

        def campo_coulomb_dinamico(pos):
            r1_vec = pos[:2] - carga1.get_center()[:2]
            r1 = np.linalg.norm(r1_vec) + 1e-4
            if r1 < 0.35: r1 = 0.35
            E1 = (r1_vec / r1) * min(1.2, 0.8 / r1**1.8)
            
            r2_vec = pos[:2] - carga2.get_center()[:2]
            r2 = np.linalg.norm(r2_vec) + 1e-4
            if r2 < 0.35: r2 = 0.35
            E2 = (r2_vec / r2) * min(1.2, 0.8 / r2**1.8)
            
            return np.array([*(E1 + E2), 0])

        stream = always_redraw(lambda: StreamLines(
            campo_coulomb_dinamico,
            x_range=[-3.5, 3.5, 0.5],
            y_range=[-3.5, 2.5, 0.5],
            color=CLR_E,
            stroke_width=2.0,
            max_color_scheme_value=2.5,
        ))

        val_u = ValueTracker(23.4) # Energía base aprox
        n_energia = VGroup(
            Text("Energía Acumulada: ", font_size=S_SUB-6, color=CLR_W),
            DecimalNumber(23.4, num_decimal_places=1, color=CLR_W, font_size=S_SUB-6),
            Text(" Joules", font_size=S_SUB-6, color=CLR_W)
        ).arrange(RIGHT, buff=0.15).move_to(ZONE_NOTE + UP*0.5)
        n_energia[1].add_updater(lambda m: m.set_value(val_u.get_value()))
        
        bg_n = capsule_bg(n_energia)

        info_lbl = MathTex(r"\text{(Se requiere trabajo para traslapar } \vec{E}_1 \text{ con } \vec{E}_2 \text{)}", font_size=S_NOTE-2, color=GREY_C).next_to(n_energia, UP, buff=0.2)

        self.play(FadeIn(carga1), FadeIn(lbl_c1), FadeIn(info_lbl), FadeIn(bg_n), FadeIn(n_energia))
        self.add(stream)
        stream.start_animation(warm_up=False, flow_speed=1.5)
        self.wait(1.5)

        self.play(FadeIn(carga2), FadeIn(lbl_c2))
        
        self.play(
            carga2.animate.move_to(RIGHT*1.5 + DOWN*0.6),
            val_u.animate.set_value(89.2),
            n_energia[0].animate.set_color(CLR_RES),
            n_energia[1].animate.set_color(CLR_RES),
            run_time=2.5, rate_func=rate_functions.ease_in_out_sine
        )
        self.wait(1)

        self.play(
            carga1.animate.move_to(LEFT*0.9 + DOWN*0.6),
            carga2.animate.move_to(RIGHT*0.9 + DOWN*0.6),
            val_u.animate.set_value(314.7),
            n_energia[0].animate.set_color(CLR_QM),
            n_energia[1].animate.set_color(CLR_QM),
            run_time=2, rate_func=rate_functions.ease_in_out_sine
        )
        self.wait(3)

        stream.end_animation()
        lbl_c1.clear_updaters(); lbl_c2.clear_updaters(); n_energia[1].clear_updaters()
        self.play(*[FadeOut(m) for m in self.mobjects])

    def escena_condensador_deduccion(self):
        self.set_camera_orientation(phi=0, theta=-PI / 2)
        ttl = Text("Energía del Condensador", font_size=S_TITLE, color=CLR_E).move_to(ZONE_TTL)
        self.play(Write(ttl))

        # CONDENSADOR UN POCO MAS ABAJO (DOWN*1.2) PARA NO SOLAPAR ECUACIONES ARRIBA
        desfase_y = -1.2
        placa_p = Rectangle(width=0.15, height=2.5, color=CLR_Q, fill_opacity=0.3, fill_color=CLR_Q).move_to(LEFT * 1.5 + UP * desfase_y)
        placa_n = Rectangle(width=0.15, height=2.5, color=CLR_QM, fill_opacity=0.3, fill_color=CLR_QM).move_to(RIGHT * 1.5 + UP * desfase_y)
        lbl_p = MathTex("+Q", font_size=S_NOTE, color=CLR_Q).next_to(placa_p, LEFT, buff=0.1)
        lbl_n = MathTex("-Q", font_size=S_NOTE, color=CLR_QM).next_to(placa_n, RIGHT, buff=0.1)

        # Flechas más pequeñas (max_tip_length_to_length_ratio)
        flechas = VGroup(*[
            Arrow(LEFT * 1.3 + UP * (y + desfase_y),
                  RIGHT * 1.3 + UP * (y + desfase_y),
                  color=CLR_E, stroke_width=2.5, buff=0, max_tip_length_to_length_ratio=0.08)
            for y in np.linspace(-1.20, 1.20, 6)
        ])

        self.play(Create(placa_p), Create(placa_n), FadeIn(lbl_p), FadeIn(lbl_n))
        self.play(LaggedStart(*[Create(f) for f in flechas], lag_ratio=0.1, run_time=1))

        # Equations moved UP to avoid overlap with mid-positioned capacitor
        eq1 = MathTex(r"dW", r"=", r"V\, dq", r"=", r"\frac{q}{C}", r"dq", font_size=S_SUB).move_to(ZONE_EQ + UP * 1.5)
        eq1[0].set_color(CLR_W)
        bg1 = capsule_bg(eq1)
        self.play(FadeIn(bg1), Write(eq1))
        self.wait(1.5)

        eq2 = MathTex(r"W", r"=", r"\int_0^Q", r"\frac{q}{C}", r"\, dq", r"=", r"\frac{1}{2}", r"\frac{Q^2}{C}", font_size=S_SUB).move_to(ZONE_EQ + UP * 1.5)
        eq2[0].set_color(CLR_W); eq2[6].set_color(CLR_U)
        bg2 = capsule_bg(eq2)
        self.play(FadeOut(bg1), ReplacementTransform(eq1, eq2), FadeIn(bg2))
        self.wait(1.5)

        f1 = MathTex(r"W = \frac{1}{2}CV^2", font_size=S_SUB)
        f1[0].set_color(CLR_W)
        f2 = MathTex(r"W = \frac{1}{2}\frac{Q^2}{C}", font_size=S_SUB - 2)
        f3 = MathTex(r"W = \frac{1}{2}QV", font_size=S_SUB - 2)

        formas = VGroup(f1, f2, f3).arrange(RIGHT, buff=0.8).move_to(ZONE_EQ + UP * 1.5)
        bg_f = capsule_bg(formas, buff=0.3)
        bx_f = caja(formas, color=CLR_RES, buff=0.35)
        self.play(FadeOut(bg2), FadeOut(eq2))
        self.play(FadeIn(bg_f), Write(f1), Write(f2), Write(f3))
        self.play(Create(bx_f))
        self.wait(2)

        self.play(FadeOut(bg_f), FadeOut(formas), FadeOut(bx_f))

        eq_ver = MathTex(r"W", r"=", r"\frac{\epsilon_0}{2}", r"E^2", r"\cdot", r"\text{Vol}", r"=", r"\frac{\epsilon_0}{2}", r"\frac{Q^2}{\epsilon_0^2 A^2}", r"(A d)", r"=", r"\frac{1}{2}\frac{Q^2}{C}", font_size=S_SUB - 8).move_to(ZONE_EQ + UP*1.4)
        eq_ver[0].set_color(CLR_W)
        bg_v = capsule_bg(eq_ver)
        p4 = MathTex(r"\text{Concordancia con la densidad de campo}", font_size=S_NOTE, color=CLR_DENS).next_to(eq_ver, UP, buff=0.2)
        self.play(FadeIn(bg_v), Write(eq_ver), FadeIn(p4))
        self.wait(3)

        self.play(*[FadeOut(m) for m in self.mobjects])

    def escena_cierre(self):
        self.move_camera(phi=65 * DEGREES, theta=-30 * DEGREES, run_time=1.5)

        ejes = ThreeDAxes(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1], z_range=[-3, 3, 1],
            x_length=5, y_length=5, z_length=5,
        )
        ejes.set_color(GREY_C).set_stroke(opacity=0.3)
        self.play(Create(ejes, run_time=1))

        # PLACAS MUCHO MÁS GRANDES PARA CONTACTAR CON TODAS LAS FLECHAS
        placa_pos = Cube(side_length=0.1, fill_opacity=0.6, fill_color=CLR_Q, stroke_width=0.5)
        placa_pos.scale([1, 40, 40]).move_to(LEFT * 1.5)

        placa_neg = Cube(side_length=0.1, fill_opacity=0.6, fill_color=CLR_QM, stroke_width=0.5)
        placa_neg.scale([1, 40, 40]).move_to(RIGHT * 1.5)

        self.play(FadeIn(placa_pos), FadeIn(placa_neg))

        # FLECHAS MUCHO MÁS FINAS (thickness 0.003 en lugar de default/0.008)
        arrows = VGroup()
        for y in np.linspace(-1.8, 1.8, 4):
            for z in np.linspace(-1.8, 1.8, 4):
                arrows.add(Arrow3D(start=np.array([-1.4, y, z]), end=np.array([1.4, y, z]), color=CLR_E, thickness=0.003))
        self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.02, run_time=2.0))

        ef = MathTex(r"u = \frac{1}{2}\epsilon_0 E^2", font_size=S_SUB).move_to(ZONE_TTL)
        efb = capsule_bg(ef, buff=0.2)
        self.add_fixed_in_frame_mobjects(efb, ef)
        self.play(FadeIn(efb), FadeIn(ef))

        brand = Text("@lomejorphysics", font_size=S_TXT, color=CLR_Q).move_to(ZONE_NOTE)
        self.add_fixed_in_frame_mobjects(brand)
        self.play(FadeIn(brand))

        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(4)
        self.stop_ambient_camera_rotation()

        self.remove(efb, ef, brand)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.5)
