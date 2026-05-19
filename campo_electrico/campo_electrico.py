"""
Campo Eléctrico - @lomejorphysics (Reel Edition)
================================================
Rigor Matemático: Griffiths / López Rodríguez
Estilo Visual: 3Blue1Brown
Formato: Instagram Reels (9:16)

Compilar con:
/home/odoo-01/bin/micromamba run -n manim manim -p -ql --fps 60 -r 1080,1920 \
    "códigos y archivos/campo_electrico/campo_electrico.py"
"""

from manim import *
import numpy as np

# ── Identidad Visual ──
COLORS = [BLUE_E, TEAL, GREEN, YELLOW, ORANGE, RED]
COLOR_SOURCE = RED_D
COLOR_TEST = GREEN_D
COLOR_VEC_R = YELLOW
COLOR_VEC_RP = TEAL
COLOR_SEP = ORANGE


class CampoElectrico(MovingCameraScene):
    """Video educativo: Ley de Coulomb → Campo Eléctrico."""

    def construct(self):
        self.intro_reel()                       # 1. Título
        self.geometria_vectorial()               # 2. Sistema de referencia + vectores posición
        self.ley_coulomb_formal()                # 3. Ley de Coulomb con notación rigurosa
        self.definicion_campo_electrico()         # 4. Paso de F a E (límite, López Rodríguez)
        self.visualizacion_campo()               # 5. Campo vectorial + StreamLines
        self.cierre()                            # 6. Mensaje final

    # ─────────────────────────────────────────
    # 1. INTRODUCCIÓN
    # ─────────────────────────────────────────
    def intro_reel(self):
        titulo = MathTex("\\vec{E}", font_size=180).set_color_by_gradient(BLUE, TEAL)
        sub = Text("Campo Eléctrico", font_size=40, color=GRAY_A)
        sub.next_to(titulo, DOWN, buff=0.8)

        self.play(Write(titulo), run_time=1.5)
        self.play(FadeIn(sub, shift=UP*0.3))
        self.wait(1.5)
        self.play(FadeOut(titulo, sub))

    # ─────────────────────────────────────────
    # 2. GEOMETRÍA VECTORIAL (r, r', separación)
    # ─────────────────────────────────────────
    def geometria_vectorial(self):
        header = Text("I. Geometría del problema", font_size=28, color=GRAY_B)
        header.to_edge(UP, buff=0.6)
        self.play(FadeIn(header))

        # — Sistema de referencia (ejes cartesianos) —
        axes = Axes(
            x_range=[-5, 6, 1], y_range=[-4, 5, 1],
            x_length=9, y_length=7,
            axis_config={"color": GRAY, "stroke_width": 1.5,
                         "include_ticks": False},
        ).shift(DOWN*0.3)
        x_label = axes.get_x_axis_label("x", direction=RIGHT).set_color(GRAY)
        y_label = axes.get_y_axis_label("y", direction=UP).set_color(GRAY)
        origin_dot = Dot(axes.c2p(0, 0), color=WHITE, radius=0.06)
        origin_label = MathTex("O", font_size=28, color=WHITE).next_to(origin_dot, DL, buff=0.15)

        self.play(Create(axes), FadeIn(x_label, y_label, origin_dot, origin_label))
        self.wait(0.5)

        # — Posiciones de las cargas (separadas para vectores largos) —
        pos_source = np.array([-1.0, 3.0, 0])   # r' (carga fuente Q)
        pos_field  = np.array([4.5, -1.0, 0])   # r  (punto de campo / carga q)

        source_point = axes.c2p(*pos_source[:2])
        field_point  = axes.c2p(*pos_field[:2])

        # Cargas
        charge_Q = self.get_charge(1, pos=source_point, color=COLOR_SOURCE)
        charge_q = self.get_charge(1, pos=field_point, color=COLOR_TEST)
        label_Q = MathTex("Q", font_size=30, color=COLOR_SOURCE).next_to(charge_Q, UL, buff=0.15)
        label_q = MathTex("q",  font_size=30, color=COLOR_TEST).next_to(charge_q, DR, buff=0.15)

        self.play(
            LaggedStart(FadeIn(charge_Q), FadeIn(charge_q), lag_ratio=0.4),
            LaggedStart(Write(label_Q), Write(label_q), lag_ratio=0.4),
        )
        self.wait(0.5)

        # — Vector posición r' (del origen a la carga fuente Q) —
        vec_rp = Arrow(
            axes.c2p(0, 0), source_point,
            color=COLOR_VEC_RP, buff=0, stroke_width=3,
        )
        vec_rp_label = MathTex("\\mathbf{r}'", font_size=32, color=COLOR_VEC_RP)
        vec_rp_label.next_to(vec_rp.get_center(), LEFT, buff=0.2)

        self.play(GrowArrow(vec_rp), Write(vec_rp_label))
        self.wait(0.5)

        # — Vector posición r (del origen al punto de campo / carga q) —
        vec_r = Arrow(
            axes.c2p(0, 0), field_point,
            color=COLOR_VEC_R, buff=0, stroke_width=3,
        )
        vec_r_label = MathTex("\\mathbf{r}", font_size=32, color=COLOR_VEC_R)
        vec_r_label.next_to(vec_r.get_center(), DOWN, buff=0.2)

        self.play(GrowArrow(vec_r), Write(vec_r_label))
        self.wait(0.5)

        # — Vector de separación r = r − r' (de Q hacia q) —
        vec_sep = Arrow(
            source_point, field_point,
            color=COLOR_SEP, buff=0, stroke_width=4,
        )
        vec_sep_label = MathTex(
            "\\boldsymbol{r}", font_size=34, color=COLOR_SEP
        ).next_to(vec_sep.get_center(), UP, buff=0.2)

        self.play(GrowArrow(vec_sep), Write(vec_sep_label))

        # — Ecuación de definición de la separación —
        sep_eq = MathTex(
            "\\boldsymbol{r}", "=", "\\mathbf{r}", "-", "\\mathbf{r}'",
            font_size=40,
        ).to_edge(DOWN, buff=0.8)
        sep_eq[0].set_color(COLOR_SEP)
        sep_eq[2].set_color(COLOR_VEC_R)
        sep_eq[4].set_color(COLOR_VEC_RP)

        self.play(Write(sep_eq))
        self.wait(2)

        # Guardar elementos para reusar o limpiar
        self.geo_group = VGroup(
            axes, x_label, y_label, origin_dot, origin_label,
            charge_Q, charge_q, label_Q, label_q,
            vec_rp, vec_rp_label, vec_r, vec_r_label,
            vec_sep, vec_sep_label, sep_eq, header,
        )

        self.play(FadeOut(self.geo_group))

    # ─────────────────────────────────────────
    # 3. LEY DE COULOMB (notación formal)
    # ─────────────────────────────────────────
    def ley_coulomb_formal(self):
        header = Text("II. Ley de Coulomb", font_size=28, color=GRAY_B)
        header.to_edge(UP, buff=0.6)
        self.play(FadeIn(header))

        # Fórmula completa con 1/(4πε₀)
        coulomb = MathTex(
            "\\vec{F}",
            "=",
            "\\frac{1}{4\\pi\\varepsilon_0}",
            "\\frac{q\\, Q}{r^2}",
            "\\hat{r}",
            font_size=44,
        ).shift(UP*1.5)
        coulomb[0].set_color(YELLOW)

        self.play(Write(coulomb), run_time=1.5)
        self.wait(0.5)

        # Recordatorio de r (separación)
        sep_reminder = MathTex(
            "\\boldsymbol{r} = \\mathbf{r} - \\mathbf{r}'"
            "\\,,\\quad r = |\\boldsymbol{r}|",
            font_size=30, color=GRAY_A,
        ).next_to(coulomb, DOWN, buff=0.6)

        self.play(FadeIn(sep_reminder))
        self.wait(1)

        # Destacar la dependencia 1/r²
        box = SurroundingRectangle(coulomb[3], color=TEAL, buff=0.1)
        nota_r2 = Text("Decae con el cuadrado de la distancia",
                        font_size=18, color=TEAL, slant=ITALIC)
        nota_r2.next_to(box, DOWN, buff=0.3)

        self.play(Create(box), FadeIn(nota_r2))
        self.wait(2)

        # Principio de superposición (mención breve)
        superpos = MathTex(
            "\\vec{F}_{\\text{total}}",
            "=",
            "\\frac{1}{4\\pi\\varepsilon_0}",
            "\\sum_{i=1}^{n}",
            "\\frac{q\\, q_i}{r_i^{\\,2}}",
            "\\hat{r}_i",
            font_size=38,
        ).next_to(sep_reminder, DOWN, buff=1.2)

        nota_sup = Text("Principio de superposición lineal",
                        font_size=20, color=GREEN_A, slant=ITALIC)
        nota_sup.next_to(superpos, DOWN, buff=0.3)

        self.play(
            FadeOut(box, nota_r2),
            Write(superpos), FadeIn(nota_sup),
        )
        self.wait(2.5)

        self.coulomb_group = VGroup(header, coulomb, sep_reminder, superpos, nota_sup)
        self.play(FadeOut(self.coulomb_group))

    # ─────────────────────────────────────────
    # 4. DEFINICIÓN DE CAMPO ELÉCTRICO
    # ─────────────────────────────────────────
    def definicion_campo_electrico(self):
        header = Text("III. Campo eléctrico", font_size=28, color=GRAY_B)
        header.to_edge(UP, buff=0.6)
        self.play(FadeIn(header))

        # Paso 1: F / q₀
        step1 = MathTex(
            "\\vec{E}",
            "\\equiv",
            "\\lim_{\\Delta q \\to 0}",
            "\\frac{\\vec{F}_{\\Delta q}}{\\Delta q}",
            font_size=48,
        ).shift(UP*1.5)
        step1[0].set_color(BLUE)

        nota = Text(
            "La carga de prueba no debe perturbar la fuente",
            font_size=18, color=BLUE_A, slant=ITALIC,
        ).next_to(step1, DOWN, buff=0.5)

        self.play(Write(step1), run_time=1.5)
        self.play(FadeIn(nota, shift=UP*0.2))
        self.wait(2)

        # Paso 2: Resultado para carga puntual
        step2 = MathTex(
            "\\vec{E}(\\mathbf{r})",
            "=",
            "\\frac{1}{4\\pi\\varepsilon_0}",
            "\\frac{Q}{r^2}",
            "\\hat{r}",
            font_size=46,
        ).next_to(nota, DOWN, buff=1.2)
        step2[0].set_color(BLUE)

        self.play(Write(step2))
        self.play(Indicate(step2[0]))
        self.wait(1)

        # Paso 3: Propiedad local
        local = MathTex(
            "\\vec{F}", "=", "q_0", "\\vec{E}",
            font_size=50,
        ).next_to(step2, DOWN, buff=1.2)
        local[3].set_color(BLUE)

        local_nota = Text(
            "Conociendo E, predecimos F sobre cualquier carga",
            font_size=18, color=GRAY_A, slant=ITALIC,
        ).next_to(local, DOWN, buff=0.3)

        self.play(Write(local), FadeIn(local_nota))
        self.wait(2.5)

        self.play(FadeOut(header, step1, nota, step2, local, local_nota))

    # ─────────────────────────────────────────
    # 5. VISUALIZACIÓN DEL CAMPO
    # ─────────────────────────────────────────
    def visualizacion_campo(self):
        header = Text("IV. Visualización", font_size=28, color=GRAY_B)
        header.to_edge(UP, buff=0.6)
        self.play(FadeIn(header))

        # Carga fuente
        source = self.get_charge(1, pos=ORIGIN, color=COLOR_SOURCE)
        label_q = MathTex("+Q", font_size=30).next_to(source, DR, buff=0.1)

        def campo_func(p):
            r = p - source.get_center()
            dist = np.linalg.norm(r)
            if dist < 0.5:
                return ORIGIN
            return r / (dist**3) * 2.0

        # Campo de flechas
        field = ArrowVectorField(
            campo_func,
            colors=COLORS,
            x_range=[-5, 5, 0.9],
            y_range=[-5, 5, 0.9],
            length_func=lambda x: np.clip(x, 0.15, 0.7),
        )

        # StreamLines
        stream = StreamLines(
            campo_func,
            colors=COLORS,
            stroke_width=2,
            x_range=[-5, 5, 0.8],
            y_range=[-5, 5, 0.8],
        )

        self.play(Create(source), Write(label_q))
        self.play(Create(field), run_time=2)
        self.wait(1)

        # Transición a líneas de flujo
        self.play(FadeOut(field), FadeIn(stream))
        stream.start_animation(warm_up=True, flow_speed=1.2)
        self.wait(3)

        # Carga de prueba con flecha dinámica
        test = self.get_charge(1, pos=RIGHT*3, color=COLOR_TEST).scale(0.6)
        test_lbl = MathTex("q_0", color=COLOR_TEST, font_size=28).next_to(test, DOWN)

        force_arrow = always_redraw(lambda: Arrow(
            test.get_center(),
            test.get_center() + campo_func(test.get_center()) * 1.8,
            color=YELLOW, buff=0,
        ))

        f_eq = MathTex(
            "\\vec{F} = q_0\\,\\vec{E}", color=YELLOW, font_size=34,
        ).to_edge(DOWN, buff=1)

        self.play(FadeIn(test, test_lbl), Create(force_arrow), Write(f_eq))
        self.play(test.animate.move_to(UL*2), run_time=2.5)
        self.play(test.animate.move_to(DR*2.5), run_time=2.5)
        self.play(test.animate.move_to(LEFT*3 + DOWN), run_time=2.5)
        self.wait(1)

        self.play(FadeOut(
            stream, source, label_q, test, test_lbl,
            force_arrow, f_eq, header,
        ))

    # ─────────────────────────────────────────
    # 6. CIERRE
    # ─────────────────────────────────────────
    def cierre(self):
        msg = Text(
            "El campo es una propiedad\ndel espacio mismo.",
            font_size=32, color=BLUE_A, line_spacing=1.4,
        ).move_to(ORIGIN)
        canal = Text("@lomejorphysics", font_size=24, color=GRAY_B)
        canal.next_to(msg, DOWN, buff=1)

        self.play(Write(msg), run_time=1.5)
        self.play(FadeIn(canal, shift=UP*0.2))
        self.wait(3)
        self.play(FadeOut(msg, canal))

    # ─────────────────────────────────────────
    # UTILIDADES
    # ─────────────────────────────────────────
    def get_charge(self, val, pos=ORIGIN, color=RED):
        """Carga estilizada con símbolo interior."""
        symbol = "+" if val >= 0 else "-"
        return VGroup(
            Circle(radius=0.18, color=color, fill_opacity=0.9, fill_color=color),
            MathTex(symbol, color=WHITE).scale(0.5),
        ).move_to(pos)
