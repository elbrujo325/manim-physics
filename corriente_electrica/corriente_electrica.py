""" Corriente Eléctrica — Cuando las cargas se mueven
=========================================================
@lomejorphysics · Reitz & Milford Cap. 5 / Griffiths Cap. 5.1

COMPILAR PREVIEW (15 FPS):
/home/odoo-01/bin/micromamba run -n manim manim --disable_caching --fps 15 -ql --format=mp4 -r 1080,1920 corriente_electrica.py CorrienteElectrica

COMPILAR FINAL (60 FPS):
/home/odoo-01/bin/micromamba run -n manim manim --disable_caching --fps 60 --resolution 1080,1920 -qh --format=mp4 corriente_electrica.py CorrienteElectrica
"""
from manim import *
import numpy as np

# ══════════════════════════════════════════════════════════════════════════
# COLORES (Paleta @lomejorphysics — probada)
# ══════════════════════════════════════════════════════════════════════════
BG = "#0d1117"
CLR_Q = "#FFD700"       # Carga positiva - dorado
CLR_QM = "#EF5350"      # Carga negativa (electrones) - rojo
CLR_E = "#4FC3F7"       # Campo eléctrico - cyan
CLR_J = "#FFA726"       # Corriente / densidad J - naranja
CLR_I = "#FF7043"       # Corriente I - naranja rojo
CLR_CONT = "#AB47BC"    # Continuidad - púrpura
CLR_N = "#66BB6A"       # Normal / vector - verde
CLR_RES = "#FFD54F"     # Resultado - amarillo brillante
CLR_FLUX = "#FFA726"    # Flujo - naranja
CLR_OHM = "#26C6DA"     # Ohm - teal

# ══════════════════════════════════════════════════════════════════════════
# TIPOGRAFÍA (Probada para Instagram)
# ══════════════════════════════════════════════════════════════════════════
S_TITLE = 76
S_EQ = 52
S_SUB = 44
S_TXT = 34
S_LBL = 30
S_NOTE = 26

ZONE_TTL = UP * 3.6
ZONE_EQ = UP * 0.4
ZONE_NOTE = DOWN * 3.2


# ══════════════════════════════════════════════════════════════════════════
# UTILIDADES
# ══════════════════════════════════════════════════════════════════════════
def _capsule(mob, color=BG, fill_op=0.92, buff=0.22):
    return BackgroundRectangle(mob, fill_opacity=fill_op, buff=buff, color=color).set_z_index(-1)

def _box(mob, color=CLR_RES, buff=0.35, sw=2.5):
    return SurroundingRectangle(mob, color=color, buff=buff, stroke_width=sw, corner_radius=0.15)

def _paso(txt):
    return Text(txt, font_size=S_NOTE, color=GREY_C).move_to(ZONE_NOTE)


# ══════════════════════════════════════════════════════════════════════════
# ESCENA PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════
class CorrienteElectrica(ThreeDScene):
    def construct(self):
        self.camera.background_color = BG
        self.escena_titulo()
        self.escena_estatica_a_dinamica()
        self.escena_movimiento_cargas()
        self.escena_densidad_corriente()
        self.escena_ecuacion_continuidad()
        self.escena_ley_ohm()
        self.escena_fem()
        self.escena_cierre()


    # ═══════════════════════════════════════════════════════════════════════
    # ESCENA 1: TÍTULO
    # ═══════════════════════════════════════════════════════════════════════
    def escena_titulo(self):
        self.set_camera_orientation(phi=0, theta=-PI/2)

        titulo = Text("Corriente Eléctrica", font_size=S_TITLE)
        titulo.set_color_by_gradient(CLR_J, CLR_I)
        titulo.move_to(ZONE_TTL + DOWN * 0.3)

        sub = Text("Cuando las cargas se mueven", font_size=S_TXT, color=GREY_B)
        sub.next_to(titulo, DOWN, buff=0.5)

        linea = Line(LEFT * 2.5, RIGHT * 2.5, color=CLR_J, stroke_width=1.5)
        linea.next_to(sub, DOWN, buff=0.4)

        fuente = Text("Reitz & Milford · Capítulo 5", font_size=S_NOTE, color=GREY_C)
        fuente.next_to(linea, DOWN, buff=0.4)

        brand = Text("@lomejorphysics", font_size=S_LBL, color=CLR_Q)
        brand.move_to(ZONE_NOTE + DOWN * 0.4)

        # Visual: electrón moviéndose
        elec = Dot(DOWN * 1.8, radius=0.1, color=CLR_QM)
        lbl_e = Text("e⁻", font_size=S_LBL, color=CLR_QM).next_to(elec, DOWN, buff=0.1)
        trail = TracedPath(elec.get_center, stroke_color=CLR_J, stroke_width=2, stroke_opacity=0.6)

        self.play(Write(titulo, run_time=1.5))
        self.play(FadeIn(sub), GrowFromCenter(linea))
        self.play(FadeIn(fuente), FadeIn(brand))
        self.play(FadeIn(elec), FadeIn(lbl_e), FadeIn(trail))
        self.play(elec.animate.shift(RIGHT * 3), run_time=2)
        self.wait(1)
        self.play(*[FadeOut(m) for m in [titulo, sub, linea, fuente, brand, elec, lbl_e, trail]])


    # ═══════════════════════════════════════════════════════════════════════
    # ESCENA 2: DE LA ESTÁTICA A LA DINÁMICA
    # ═══════════════════════════════════════════════════════════════════════
    def escena_estatica_a_dinamica(self):
        self.set_camera_orientation(phi=0, theta=-PI/2)

        ttl = Text("De la Estática a la Dinámica", font_size=S_TITLE, color=CLR_E)
        ttl.move_to(ZONE_TTL)
        self.play(Write(ttl))

        # Parte 1: Cargas estáticas
        cargas_estaticas = VGroup()
        for i in range(6):
            x = (i - 2.5) * 1.2
            q = Dot(UP * 0.5 + RIGHT * x, radius=0.1, color=CLR_Q)
            cargas_estaticas.add(q)

        lbl_static = Text("Cargas en equilibrio → sin corriente", font_size=S_TXT, color=GREY_B)
        lbl_static.move_to(ZONE_NOTE)

        self.play(FadeIn(cargas_estaticas), FadeIn(lbl_static))
        self.wait(1.5)

        # Parte 2: Campo E aparece → cargas se mueven
        campo_e = VGroup(*[
            Arrow(LEFT * 3.5 + DOWN * y, RIGHT * 3.5 + DOWN * y,
                  color=CLR_E, stroke_width=1.5, buff=0, stroke_opacity=0.25)
            for y in [0.5, -0.5]
        ])

        lbl_E = MathTex(r"\vec{E}", font_size=S_LBL, color=CLR_E)
        lbl_E.next_to(campo_e[0], UP, buff=0.1)

        self.play(FadeIn(campo_e), FadeIn(lbl_E))
        self.play(ReplacementTransform(
            lbl_static,
            Text("Campo E → fuerza → movimiento", font_size=S_TXT, color=CLR_J).move_to(ZONE_NOTE)
        ))

        # Cargas se mueven
        self.play(LaggedStart(*[
            c.animate.shift(RIGHT * 1.5 + DOWN * 1.5) for c in cargas_estaticas
        ], lag_ratio=0.1, run_time=1.5))

        self.wait(1)

        # Definición de corriente
        eq_I = MathTex(r"I", r"=", r"\frac{dQ}{dt}", font_size=S_EQ)
        eq_I[0].set_color(CLR_I)
        eq_I.move_to(ZONE_EQ)
        bg = _capsule(eq_I)
        bx = _box(eq_I, color=CLR_I)

        nota = Text("Corriente = tasa de flujo de carga", font_size=S_NOTE, color=GREY_B)
        nota.move_to(ZONE_NOTE)

        self.play(FadeIn(bg), Write(eq_I))
        self.play(Create(bx))
        self.play(FadeIn(nota))
        self.wait(2)

        self.play(*[FadeOut(m) for m in [ttl, cargas_estaticas, campo_e, lbl_E, bg, eq_I, bx, nota]])


    # ═══════════════════════════════════════════════════════════════════════
    # ESCENA 3: MOVIMIENTO DE LAS CARGAS
    # ═══════════════════════════════════════════════════════════════════════
    def escena_movimiento_cargas(self):
        self.set_camera_orientation(phi=0, theta=-PI/2)

        ttl = Text("Movimiento de las Cargas", font_size=S_TITLE, color=CLR_QM)
        ttl.move_to(ZONE_TTL)
        self.play(Write(ttl))

        # Conductor rectangular
        conductor = Rectangle(width=6, height=1.8, color=GREY_C, fill_opacity=0.05, fill_color=GREY_D)
        conductor.shift(DOWN * 0.3)
        lbl_cond = Text("Conductor", font_size=S_NOTE, color=GREY_C).next_to(conductor, UP, buff=0.15)

        # Iones fijos (red positivos)
        iones = VGroup()
        for i in range(8):
            for j in range(3):
                x = (i - 3.5) * 0.7
                y = (j - 1) * 0.5 - 0.3
                ion = Dot(LEFT * x + UP * y, radius=0.04, color=CLR_Q)
                iones.add(ion)

        # Electrones libres (azul, moviéndose)
        electrones = VGroup()
        elec_positions = []
        for i in range(10):
            y = np.random.uniform(-0.8, 0.2) - 0.3
            x = np.random.uniform(-2.5, 2.5)
            elec = Dot(LEFT * x + UP * y, radius=0.06, color=CLR_QM)
            electrones.add(elec)
            elec_positions.append((x, y))

        self.play(Create(conductor), FadeIn(lbl_cond))
        self.play(FadeIn(iones))
        self.play(FadeIn(electrones))

        # Mostrar velocidad de arrastre
        nota1 = Text("Electrones vibran rápido... pero se mueven lento", font_size=S_NOTE, color=GREY_B)
        nota1.move_to(ZONE_NOTE)
        self.play(FadeIn(nota1))

        # Animar drift lento hacia la izquierda
        self.play(LaggedStart(*[
            e.animate.shift(LEFT * 1.5) for e in electrones
        ], lag_ratio=0.05, run_time=2.5))

        # Velocidad de arrastre
        eq_vd = MathTex(r"\vec{v}_d", font_size=S_SUB, color=CLR_QM)
        eq_vd.move_to(UP * 1.5)
        arrow_vd = Arrow(UP * 1.5 + RIGHT * 0.5, UP * 1.5 + LEFT * 1.2, color=CLR_QM, stroke_width=3, buff=0)
        self.play(FadeIn(eq_vd), Create(arrow_vd))

        self.wait(1)

        # Convención de corriente
        nota2 = Text("Convención: I va en sentido de E (opuesto a e⁻)", font_size=S_NOTE, color=CLR_I)
        nota2.move_to(ZONE_NOTE)
        self.play(ReplacementTransform(nota1, nota2))

        # Flecha de corriente (sentido opuesto a electrones)
        arrow_I = Arrow(LEFT * 1.5 + DOWN * 1.5, RIGHT * 1.5 + DOWN * 1.5,
                        color=CLR_I, stroke_width=3, buff=0)
        lbl_I_arrow = MathTex(r"I", font_size=S_LBL, color=CLR_I).next_to(arrow_I, DOWN, buff=0.1)
        self.play(Create(arrow_I), FadeIn(lbl_I_arrow))

        self.wait(2)
        self.play(*[FadeOut(m) for m in [ttl, conductor, lbl_cond, iones, electrones,
                                          eq_vd, arrow_vd, nota2, arrow_I, lbl_I_arrow]])


    # ═══════════════════════════════════════════════════════════════════════
    # ESCENA 4: DENSIDAD DE CORRIENTE J
    # ═══════════════════════════════════════════════════════════════════════
    def escena_densidad_corriente(self):
        self.set_camera_orientation(phi=0, theta=-PI/2)

        ttl = Text("Densidad de Corriente", font_size=S_TITLE, color=CLR_J)
        ttl.move_to(ZONE_TTL)
        self.play(Write(ttl))

        # Definición: J = ρv
        eq1 = MathTex(r"\vec{J}", r"=", r"\rho", r"\vec{v}", font_size=S_EQ)
        eq1[0].set_color(CLR_J)
        eq1[2].set_color(CLR_Q)
        eq1[3].set_color(CLR_QM)
        eq1.move_to(ZONE_EQ + UP * 1.5)
        bg1 = _capsule(eq1)
        p1 = _paso("Paso 1 · Densidad de corriente = carga × velocidad")
        self.play(FadeIn(bg1), Write(eq1), FadeIn(p1))
        self.wait(1.5)
        self.play(FadeOut(p1))

        # Visual: campo vectorial J en un conductor
        conductor = Rectangle(width=5, height=2.5, color=GREY_C, fill_opacity=0.04, fill_color=GREY_D)
        conductor.shift(DOWN * 0.3)

        def campo_J(pos):
            # J uniforme apuntando a la derecha dentro del conductor
            if abs(pos[0]) < 2.3 and abs(pos[1] + 0.3) < 1.1:
                return np.array([0.8, 0.0, 0.0])
            return np.zeros(3)

        campo_J_vis = ArrowVectorField(
            campo_J,
            x_range=[-2.2, 2.2, 0.6],
            y_range=[-1.2, 0.8, 0.5],
            color=CLR_J,
            length_func=lambda x: 0.5 * x,
            stroke_width=1.8,
        )

        self.play(Create(conductor), FadeIn(campo_J_vis, lag_ratio=0.02, run_time=1.5))

        # Geometría: I = ∫J·da
        eq2 = MathTex(r"I", r"=", r"\int_S", r"\vec{J}", r"\cdot", r"d\vec{a}", font_size=S_EQ)
        eq2[0].set_color(CLR_I)
        eq2[3].set_color(CLR_J)
        eq2[5].set_color(CLR_N)
        eq2.move_to(ZONE_EQ)
        bg2 = _capsule(eq2)
        p2 = _paso("Paso 2 · Corriente = flujo de J a través de la sección")
        self.play(FadeOut(bg1), ReplacementTransform(eq1, eq2, run_time=1.5), FadeIn(bg2), FadeIn(p2))
        self.wait(1.5)
        self.play(FadeOut(p2))

        # Sección transversal visual
        seccion = Line(UP * 0.7 + DOWN * 0.3, DOWN * 1.3 + DOWN * 0.3,
                       color=CLR_N, stroke_width=3)
        lbl_da = MathTex(r"d\vec{a}", font_size=S_NOTE, color=CLR_N)
        lbl_da.next_to(seccion, RIGHT, buff=0.15)

        self.play(Create(seccion), FadeIn(lbl_da))

        # Caso uniforme
        eq3 = MathTex(r"I", r"=", r"J", r"\cdot", r"A", font_size=S_SUB)
        eq3[0].set_color(CLR_I)
        eq3[2].set_color(CLR_J)
        eq3.move_to(ZONE_EQ + DOWN * 1.5)
        nota = Text("(J uniforme)", font_size=S_NOTE, color=GREY_B)
        nota.next_to(eq3, RIGHT, buff=0.2)
        self.play(Write(eq3), FadeIn(nota))

        self.wait(2)
        self.play(*[FadeOut(m) for m in [ttl, conductor, campo_J_vis, bg2, eq2,
                                          seccion, lbl_da, eq3, nota]])


    # ═══════════════════════════════════════════════════════════════════════
    # ESCENA 5: ECUACIÓN DE CONTINUIDAD
    # ═══════════════════════════════════════════════════════════════════════
    def escena_ecuacion_continuidad(self):
        self.set_camera_orientation(phi=0, theta=-PI/2)

        ttl = Text("Ecuación de Continuidad", font_size=S_TITLE, color=CLR_CONT)
        ttl.move_to(ZONE_TTL)
        self.play(Write(ttl))

        # Visual: volumen con cargas saliendo
        vol = Rectangle(width=2.5, height=2, color=CLR_CONT, fill_opacity=0.05, fill_color=GREY_D)
        vol.shift(UP * 0.5)
        lbl_vol = MathTex(r"V", font_size=S_SUB, color=CLR_CONT).move_to(vol)

        # Cargas dentro
        cargas_dentro = VGroup(*[
            Dot(vol.get_center() + UP * np.random.uniform(-0.6, 0.6) + RIGHT * np.random.uniform(-0.8, 0.8),
                radius=0.06, color=CLR_Q)
            for _ in range(8)
        ])

        # Flechas J saliendo
        flechas_J = VGroup(*[
            Arrow(vol.get_center() + d, vol.get_center() + d * 1.8,
                  color=CLR_J, stroke_width=2, buff=0.1)
            for d in [RIGHT * 1.25 + UP * 0.3, RIGHT * 1.25 + DOWN * 0.3,
                      LEFT * 1.25 + UP * 0.3, LEFT * 1.25 + DOWN * 0.3,
                      UP * 1.0 + RIGHT * 0.5, UP * 1.0 + LEFT * 0.5]
        ])

        lbl_J_out = MathTex(r"\vec{J}", font_size=S_LBL, color=CLR_J).next_to(flechas_J[0], RIGHT, buff=0.1)

        self.play(Create(vol), FadeIn(lbl_vol), FadeIn(cargas_dentro))
        self.play(LaggedStart(*[Create(f) for f in flechas_J], lag_ratio=0.08, run_time=1.5))
        self.play(FadeIn(lbl_J_out))

        # PASO 1: Conservación de carga
        eq1 = MathTex(r"\oint_S", r"\vec{J}", r"\cdot", r"d\vec{a}", r"=", r"-\frac{dQ}{dt}", font_size=S_SUB)
        eq1[1].set_color(CLR_J)
        eq1[3].set_color(CLR_N)
        eq1[5].set_color(CLR_Q)
        eq1.move_to(ZONE_EQ + UP * 1.5)
        bg1 = _capsule(eq1)
        p1 = _paso("Paso 1 · Carga que sale = carga que disminuye")
        self.play(FadeIn(bg1), Write(eq1), FadeIn(p1))
        self.wait(1.5)
        self.play(FadeOut(p1))

        # Animar cargas saliendo
        self.play(LaggedStart(*[
            c.animate.shift(RIGHT * 2 + UP * np.random.uniform(-1, 1))
            for c in cargas_dentro[:4]
        ], lag_ratio=0.1, run_time=1.5))

        # PASO 2: Teorema de la divergencia
        eq2 = MathTex(r"\oint_S", r"\vec{J}", r"\cdot", r"d\vec{a}", r"=", r"\int_V", r"(\nabla \cdot \vec{J})", r"\, d\tau", font_size=S_SUB)
        eq2[1].set_color(CLR_J)
        eq2[3].set_color(CLR_N)
        eq2[6].set_color(CLR_CONT)
        eq2.move_to(ZONE_EQ + UP * 0.3)
        bg2 = _capsule(eq2)
        p2 = _paso("Paso 2 · Teorema de la divergencia (Gauss para J)")
        self.play(FadeOut(bg1), ReplacementTransform(eq1, eq2, transform_mismatches=True, run_time=2),
                  FadeIn(bg2), FadeIn(p2))
        self.wait(1.5)
        self.play(FadeOut(p2))

        # PASO 3: Lado derecho
        eq3 = MathTex(r"-", r"\frac{dQ}{dt}", r"=", r"-\frac{\partial}{\partial t}", r"\int_V", r"\rho", r"\, d\tau", font_size=S_SUB)
        eq3[1].set_color(CLR_Q)
        eq3[5].set_color(CLR_Q)
        eq3.move_to(ZONE_EQ + DOWN * 0.7)
        bg3 = _capsule(eq3)
        p3 = _paso("Paso 3 · dQ/dt = cambio de carga en el volumen")
        self.play(FadeIn(bg3), Write(eq3), FadeIn(p3))
        self.wait(1.5)
        self.play(FadeOut(p3))

        # RESULTADO: Igualar y obtener forma local
        eq4 = MathTex(r"\nabla \cdot \vec{J}", r"=", r"-\frac{\partial \rho}{\partial t}", font_size=S_EQ)
        eq4[0].set_color(CLR_CONT)
        eq4[2].set_color(CLR_Q)
        eq4.move_to(ZONE_EQ + DOWN * 2)
        bx = _box(eq4, color=CLR_CONT)

        nota = Text("¡Conservación local de la carga!", font_size=S_TXT, color=CLR_CONT)
        nota.move_to(ZONE_NOTE)

        self.play(FadeOut(bg2), FadeOut(eq2), FadeOut(bg3), FadeOut(eq3))
        self.play(Write(eq4), Create(bx), FadeIn(nota))
        self.wait(2)

        # Régimen estacionario
        eq_est = MathTex(r"\nabla \cdot \vec{J}", r"=", r"0", font_size=S_SUB)
        eq_est[0].set_color(CLR_CONT)
        eq_est.move_to(ZONE_EQ + DOWN * 0.5)
        nota2 = Text("Régimen estacionario: lo que entra sale (Kirchhoff)", font_size=S_NOTE, color=GREY_B)
        nota2.move_to(ZONE_NOTE)
        self.play(ReplacementTransform(nota, nota2))
        self.play(Write(eq_est))
        self.wait(2)

        self.play(*[FadeOut(m) for m in [ttl, vol, lbl_vol, cargas_dentro, flechas_J, lbl_J_out,
                                          eq4, bx, nota2, eq_est]])


    # ═══════════════════════════════════════════════════════════════════════
    # ESCENA 6: LEY DE OHM MICROSCÓPICA
    # ═══════════════════════════════════════════════════════════════════════
    def escena_ley_ohm(self):
        self.set_camera_orientation(phi=0, theta=-PI/2)

        ttl = Text("Ley de Ohm Microscópica", font_size=S_TITLE, color=CLR_OHM)
        ttl.move_to(ZONE_TTL)
        self.play(Write(ttl))

        # Conductor con E adentro
        conductor = Rectangle(width=5.5, height=1.5, color=GREY_C, fill_opacity=0.04, fill_color=GREY_D)
        conductor.shift(DOWN * 0.5)

        campo = VGroup(*[
            Arrow(LEFT * 2.5 + DOWN * (y - 0.5), RIGHT * 2.5 + DOWN * (y - 0.5),
                  color=CLR_E, stroke_width=1.5, buff=0, stroke_opacity=0.3)
            for y in range(3)
        ])
        lbl_E = MathTex(r"\vec{E}", font_size=S_LBL, color=CLR_E).next_to(campo[1], UP, buff=0.1)

        # Electrones moviéndose
        electrones = VGroup(*[
            Dot(RIGHT * x + DOWN * (0.5 + np.random.uniform(-0.4, 0.4)),
                radius=0.06, color=CLR_QM)
            for x in np.linspace(-2, 2, 6)
        ])

        self.play(Create(conductor), FadeIn(campo), FadeIn(lbl_E))
        self.play(FadeIn(electrones))
        self.play(LaggedStart(*[
            e.animate.shift(LEFT * 2) for e in electrones
        ], lag_ratio=0.05, run_time=2))

        # Ecuación J = σE
        eq = MathTex(r"\vec{J}", r"=", r"\sigma", r"\vec{E}", font_size=S_EQ)
        eq[0].set_color(CLR_J)
        eq[2].set_color(CLR_OHM)
        eq[3].set_color(CLR_E)
        eq.move_to(ZONE_EQ + UP * 1)
        bg = _capsule(eq)
        bx = _box(eq, color=CLR_OHM)

        nota = Text("σ = conductividad (inverso de resistividad)", font_size=S_NOTE, color=GREY_B)
        nota.move_to(ZONE_NOTE)

        self.play(FadeIn(bg), Write(eq))
        self.play(Create(bx), FadeIn(nota))
        self.wait(1.5)

        # Forma macroscópica: V = IR
        eq_VIR = MathTex(r"V", r"=", r"I", r"R", font_size=S_SUB)
        eq_VIR[0].set_color(CLR_E)
        eq_VIR[2].set_color(CLR_I)
        eq_VIR.move_to(ZONE_EQ + DOWN * 0.8)
        nota2 = Text("Forma macroscópica (familiar)", font_size=S_NOTE, color=GREY_B)
        nota2.move_to(ZONE_NOTE)
        self.play(Write(eq_VIR), ReplacementTransform(nota, nota2))

        self.wait(2)
        self.play(*[FadeOut(m) for m in [ttl, conductor, campo, lbl_E, electrones,
                                          bg, eq, bx, nota2, eq_VIR]])


    # ═══════════════════════════════════════════════════════════════════════
    # ESCENA 7: FUERZA ELECTROMOTRIZ
    # ═══════════════════════════════════════════════════════════════════════
    def escena_fem(self):
        self.set_camera_orientation(phi=0, theta=-PI/2)

        ttl = Text("Fuerza Electromotriz", font_size=S_TITLE, color=CLR_I)
        ttl.move_to(ZONE_TTL)
        self.play(Write(ttl))

        sub = Text("¿Qué mantiene la corriente circulando?", font_size=S_TXT, color=GREY_B)
        sub.next_to(ttl, DOWN, buff=0.4)
        self.play(FadeIn(sub))

        # Circuito simple: batería + resistencia
        # Batería (lado izquierdo)
        bat_top = Line(LEFT * 1.5 + UP * 1.5, LEFT * 1.5 + UP * 0.3, color=CLR_I, stroke_width=2)
        bat_bot = Line(LEFT * 1.5 + DOWN * 0.3, LEFT * 1.5 + DOWN * 1.5, color=CLR_I, stroke_width=2)
        bat_plus = Text("+", font_size=S_LBL, color=CLR_Q).next_to(bat_top, LEFT, buff=0.1)
        bat_minus = Text("−", font_size=S_LBL, color=CLR_QM).next_to(bat_bot, LEFT, buff=0.1)
        bat_long = Line(LEFT * 1.5 + UP * 0.3, LEFT * 1.5 + DOWN * 0.3, color=CLR_I, stroke_width=3)
        bat_short = Line(LEFT * 1.8 + UP * 0.2, LEFT * 1.2 + UP * 0.2, color=CLR_I, stroke_width=2)
        bat_short2 = Line(LEFT * 1.8 + DOWN * 0.2, LEFT * 1.2 + DOWN * 0.2, color=CLR_I, stroke_width=1.5)

        # Resistencia (lado derecho) - zigzag
        res_pts = []
        for i in range(6):
            x = RIGHT * 1.5 + UP * (1.5 - i * 0.5)
            dx = RIGHT * 0.3 if i % 2 == 0 else LEFT * 0.3
            res_pts.append(x + dx)
        res_pts.insert(0, RIGHT * 1.5 + UP * 1.5)
        res_pts.append(RIGHT * 1.5 + DOWN * 1.5)
        resistencia = VMobject(color=CLR_OHM, stroke_width=2)
        resistencia.set_points_smoothly(res_pts)

        # Cables superior e inferior
        wire_top = Line(LEFT * 1.5 + UP * 1.5, RIGHT * 1.5 + UP * 1.5, color=GREY_B, stroke_width=1.5)
        wire_bot = Line(LEFT * 1.5 + DOWN * 1.5, RIGHT * 1.5 + DOWN * 1.5, color=GREY_B, stroke_width=1.5)

        lbl_bat = Text("ε", font_size=S_SUB, color=CLR_I).next_to(bat_long, LEFT, buff=0.4)
        lbl_R = Text("R", font_size=S_SUB, color=CLR_OHM).next_to(resistencia, RIGHT, buff=0.2)

        circuito = VGroup(bat_top, bat_bot, bat_long, bat_short, bat_short2,
                          bat_plus, bat_minus, resistencia, wire_top, wire_bot, lbl_bat, lbl_R)
        circuito.shift(DOWN * 0.5)

        self.play(Create(circuito), run_time=2)

        # Flecha de corriente
        arrow_I = Arrow(LEFT * 1.5 + UP * 1.0 + DOWN * 0.5,
                        RIGHT * 1.5 + UP * 1.0 + DOWN * 0.5,
                        color=CLR_I, stroke_width=2, buff=0.1, max_tip_length_to_length_ratio=0.15)
        lbl_arrow = MathTex(r"I", font_size=S_NOTE, color=CLR_I).next_to(arrow_I, UP, buff=0.1)
        self.play(Create(arrow_I), FadeIn(lbl_arrow))

        # Ecuación: ε = IR
        eq = MathTex(r"\varepsilon", r"=", r"I", r"R", font_size=S_EQ)
        eq[0].set_color(CLR_I)
        eq[2].set_color(CLR_I)
        eq.move_to(ZONE_EQ + UP * 1)
        bg = _capsule(eq)

        nota = Text("La fem impulsa la corriente a través de la resistencia", font_size=S_NOTE, color=GREY_B)
        nota.move_to(ZONE_NOTE)

        self.play(FadeIn(bg), Write(eq), FadeIn(nota))
        self.wait(1.5)
        self.play(FadeOut(nota))

        # Definición formal
        eq_formal = MathTex(r"\varepsilon", r"=", r"\oint", r"\vec{f}_s", r"\cdot", r"d\vec{l}", font_size=S_SUB)
        eq_formal[0].set_color(CLR_I)
        eq_formal[3].set_color(CLR_N)
        eq_formal.move_to(ZONE_EQ + DOWN * 0.5)
        nota2 = Text("f_s = fuerza no electrostática (batería, generador)", font_size=S_NOTE, color=GREY_B)
        nota2.move_to(ZONE_NOTE)
        self.play(Write(eq_formal), FadeIn(nota2))

        self.wait(2.5)
        self.play(FadeOut(sub))
        self.play(*[FadeOut(m) for m in [ttl, circuito, arrow_I, lbl_arrow, bg, eq, eq_formal, nota2]])


    # ═══════════════════════════════════════════════════════════════════════
    # ESCENA 8: CIERRE
    # ═══════════════════════════════════════════════════════════════════════
    def escena_cierre(self):
        self.move_camera(phi=65*DEGREES, theta=-30*DEGREES, run_time=1.5)

        # Ejes
        ejes = ThreeDAxes(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1], z_range=[-3, 3, 1],
            x_length=5, y_length=5, z_length=5,
        )
        ejes.set_color(GREY_C).set_stroke(opacity=0.3)
        self.play(Create(ejes, run_time=1))

        # Conductor 3D (cilindro simplificado con cubos)
        conductor = Cylinder(radius=1.2, height=4, color=GREY_C, fill_opacity=0.08, stroke_width=0.5, stroke_color=GREY_C)
        conductor.rotate(PI/2, axis=UP)
        self.play(Create(conductor, run_time=1.5))

        # Flechas de corriente J a través del conductor
        arrows = VGroup()
        for y in np.linspace(-0.8, 0.8, 3):
            for z in np.linspace(-0.8, 0.8, 3):
                start = np.array([-2.0, y, z])
                end = np.array([2.0, y, z])
                arrows.add(Arrow3D(start=start, end=end, color=CLR_J, thickness=0.008))

        self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.03, run_time=2))

        # Ecuación final
        ef = MathTex(r"\nabla \cdot \vec{J} = -\frac{\partial \rho}{\partial t}", font_size=S_SUB)
        ef.move_to(ZONE_TTL)
        efb = _capsule(ef, buff=0.2)
        self.add_fixed_in_frame_mobjects(efb, ef)
        self.play(FadeIn(efb), FadeIn(ef))

        # Branding
        brand = Text("@lomejorphysics", font_size=S_TXT, color=CLR_Q)
        brand.move_to(ZONE_NOTE)
        self.add_fixed_in_frame_mobjects(brand)
        self.play(FadeIn(brand))

        # Rotación
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(3)
        self.stop_ambient_camera_rotation()

        self.remove(efb, ef, brand)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.5)
