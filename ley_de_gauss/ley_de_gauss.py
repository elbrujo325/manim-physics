"""
Ley de Gauss – Demostración Visual Rigurosa  v8
================================================
@lomejorphysics  ·  Griffiths & López Rodríguez

OPTIMIZACIONES v8 (compilación rápida sin perder calidad visual)
─────────────────────────────────────────────────────────────────
  • Superficie 3D: resolution=(10, 5) en lugar de (16, 8)
    → menos triángulos, mismo aspecto visual a distancia
  • Flechas 3D: reducidas de 24 a 16 (8 ángulos × 2 alturas)
    → mismo efecto visual, menos objetos que renderizar
  • Rotación cámara: wait(3) → wait(2) en superficie, wait(5) → wait(3) cierre
    → menos frames 3D totales (el cuello de botella principal)
  • --disable_caching: en escenas 3D el hash tarda más que renderizar desde cero

CORRECCIONES DE TRANSICIONES (mantenidas de v7)
─────────────────────────────────────────────────
  • Escenas 2D (phi=0): sin fixed_in_frame → Write/FadeIn funcionan limpio
  • Escenas 3D: fixed_in_frame solo para overlays, siempre con FadeIn (no Write)
  • Flechas salen del ORIGEN y atraviesan la esfera gaussiana
  • thickness=0.008 → flechas delgadas

COMPILAR PREVIEW RÁPIDO (baja calidad, segundos):
/home/odoo-01/bin/micromamba run -n manim manim \
    --disable_caching --fps 30 -ql --format=mp4 \
    ley_de_gauss.py LeyDeGauss

COMPILAR FINAL INSTAGRAM 9:16 Full HD 60fps:
/home/odoo-01/bin/micromamba run -n manim manim \
    --disable_caching --fps 60 --resolution 1080,1920 \
    -qh --format=mp4 ley_de_gauss.py LeyDeGauss

VIDEO RESULTANTE EN:
  media/videos/ley_de_gauss/1080p60/LeyDeGauss.mp4
"""

from manim import *
import numpy as np

# ── Paleta ───────────────────────────────────────────────────────────────────
BG         = "#0d1117"
CLR_Q      = "#FFD700"
CLR_E      = "#4FC3F7"
CLR_S      = "#26C6DA"
CLR_N      = "#66BB6A"
CLR_FLUX   = "#FFA726"
CLR_CANCEL = "#EF5350"
CLR_ACC    = "#AB47BC"
CLR_RES    = "#FFD54F"

# ── Tipografía ───────────────────────────────────────────────────────────────
S_TITLE = 76
S_EQ    = 52
S_SUB   = 44
S_TXT   = 34
S_LBL   = 30
S_NOTE  = 26

# ── Zonas verticales ─────────────────────────────────────────────────────────
ZONE_TTL  = UP * 3.6
ZONE_EQ   = UP * 0.4
ZONE_NOTE = DOWN * 3.2


def _capsule(mob, color, fill_op=0.88, cr=0.18, buff=0.22):
    cap = RoundedRectangle(
        corner_radius=cr,
        width=mob.width + buff * 2,
        height=mob.height + buff * 2,
        stroke_color=color, stroke_width=2.0,
        fill_color=BG, fill_opacity=fill_op,
    )
    cap.move_to(mob)
    return cap


class LeyDeGauss(ThreeDScene):

    def construct(self):
        self.camera.background_color = BG
        self.escena_titulo()
        self.escena_campo()
        self.escena_superficie_3d()
        self.escena_flujo()
        self.escena_deduccion()
        self.escena_resultado()
        self.escena_diferencial()
        self.escena_cierre()

    # ═══════════════════════════════════════════════════════════════════════
    # 1. TÍTULO — 2D limpio, sin fixed_in_frame
    # ═══════════════════════════════════════════════════════════════════════
    def escena_titulo(self):
        self.set_camera_orientation(phi=0, theta=-PI / 2)

        titulo = Text("Ley de Gauss", font_size=S_TITLE)
        titulo.set_color_by_gradient(CLR_E, CLR_S)
        titulo.move_to(ZONE_TTL + DOWN * 0.3)

        sub = Text(
            "Demostración desde el\nCálculo Vectorial",
            font_size=S_TXT, color=GREY_B, line_spacing=1.2,
        )
        sub.next_to(titulo, DOWN, buff=0.5)

        linea = Line(LEFT * 2.5, RIGHT * 2.5, color=CLR_S, stroke_width=1.5)
        linea.next_to(sub, DOWN, buff=0.4)

        fuente = Text("Griffiths & López Rodríguez", font_size=S_NOTE, color=GREY_C)
        fuente.next_to(linea, DOWN, buff=0.4)

        brand = Text("@lomejorphysics", font_size=S_LBL, color=CLR_Q)
        brand.move_to(ZONE_NOTE + DOWN * 0.4)

        self.play(Write(titulo, run_time=1.5))
        self.play(FadeIn(sub), GrowFromCenter(linea))
        self.play(FadeIn(fuente), FadeIn(brand))
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in [titulo, sub, linea, fuente, brand]])

    # ═══════════════════════════════════════════════════════════════════════
    # 2. CAMPO ELÉCTRICO — 2D, sin fixed_in_frame
    # ═══════════════════════════════════════════════════════════════════════
    def escena_campo(self):
        self.set_camera_orientation(phi=0, theta=-PI / 2)

        carga = Dot(ORIGIN, radius=0.12, color=CLR_Q)
        g1 = Circle(radius=0.22, color=CLR_Q, stroke_width=2, stroke_opacity=0.5)
        g2 = Circle(radius=0.32, color=CLR_Q, stroke_width=1, stroke_opacity=0.3)
        lbl = MathTex("+q", font_size=S_LBL, color=CLR_Q)
        lbl.next_to(carga, DOWN, buff=0.25)
        grp = VGroup(carga, g1, g2, lbl)
        self.play(FadeIn(grp, scale=0.5))
        self.wait(0.3)

        def e_fn(pos):
            r = np.array([pos[0], pos[1], 0.0])
            rn = np.linalg.norm(r)
            if rn < 0.4:
                return np.zeros(3)
            return r / (rn ** 2) * 0.4

        campo = ArrowVectorField(
            e_fn,
            x_range=[-4, 4, 0.8],
            y_range=[-6, 6, 0.8],
            colors=[CLR_E, TEAL_C, CLR_S],
            length_func=lambda x: np.clip(x, 0.1, 0.85),
            stroke_width=1.5,
        )
        self.play(FadeIn(campo, lag_ratio=0.02, run_time=2))

        eq = MathTex(
            r"\vec{E}", "=",
            r"\frac{q}{4\pi\epsilon_0 r^2}", r"\hat{r}",
            font_size=S_EQ,
        )
        eq[0].set_color(CLR_E)
        eq[2].set_color(CLR_Q)
        eq[3].set_color(CLR_N)
        eq.move_to(ZONE_TTL)
        bg = BackgroundRectangle(eq, fill_opacity=0.92, buff=0.2, color=BG)
        self.play(FadeIn(bg), Write(eq))

        nota = MathTex(
            r"\hat{r}", r"\text{ : vector unitario radial}",
            font_size=S_NOTE,
        )
        nota[0].set_color(CLR_N)
        nota.move_to(ZONE_NOTE)
        nb = BackgroundRectangle(nota, fill_opacity=0.9, buff=0.15, color=BG)
        self.play(FadeIn(nb), Write(nota))
        self.wait(2)

        self.play(*[FadeOut(m) for m in [campo, bg, eq, nb, nota, grp]])

    # ═══════════════════════════════════════════════════════════════════════
    # 3. SUPERFICIE GAUSSIANA 3D
    #    OPTIMIZADO: resolution reducida, 16 flechas, rotación 2s
    # ═══════════════════════════════════════════════════════════════════════
    def escena_superficie_3d(self):
        self.set_camera_orientation(phi=0, theta=-PI / 2)

        hdr = Text("Superficie Gaussiana", font_size=S_TITLE, color=CLR_S)
        hdr.move_to(ZONE_TTL)
        self.add_fixed_in_frame_mobjects(hdr)
        self.play(Write(hdr))

        # Mover cámara a 3D — título ya está fijo en frame, no se mueve
        self.move_camera(phi=70 * DEGREES, theta=-45 * DEGREES, run_time=1.5)

        ejes = ThreeDAxes(
            x_range=[-3.5, 3.5, 1], y_range=[-3.5, 3.5, 1],
            z_range=[-3.5, 3.5, 1],
            x_length=6, y_length=6, z_length=6,
        )
        ejes.set_color(GREY_C).set_stroke(opacity=0.4)
        xl = MathTex("x", font_size=S_LBL, color=RED_C).move_to([3.2, -0.3, 0])
        yl = MathTex("y", font_size=S_LBL, color=GREEN_C).move_to([-0.3, 3.2, 0])
        zl = MathTex("z", font_size=S_LBL, color=BLUE_C).move_to([0, -0.3, 3.2])
        self.play(Create(ejes, run_time=1), FadeIn(xl), FadeIn(yl), FadeIn(zl))

        cq = Sphere(radius=0.1, color=CLR_Q).set_opacity(1)
        self.play(FadeIn(cq))

        R = 2.2
        # OPTIMIZACIÓN: resolution (10,5)
        esf = Surface(
            lambda u, v: np.array([
                R * np.sin(v) * np.cos(u),
                R * np.sin(v) * np.sin(u),
                R * np.cos(v),
            ]),
            u_range=[0, TAU], v_range=[0, PI],
            resolution=(10, 5),
            fill_opacity=0.10,
            stroke_width=0.5, stroke_color=CLR_S,
            checkerboard_colors=[CLR_S, TEAL_D],
        )
        self.play(Create(esf, run_time=2))

        # OPTIMIZACIÓN: 16 flechas (8 phi × 2 alturas)
        # Salen del origen, atraviesan la esfera, delgadas
        arrows = VGroup()
        for i in range(8):
            phi_a = i * TAU / 8
            for j in range(1, 3):
                th = j * PI / 3
                d = np.array([
                    np.sin(th) * np.cos(phi_a),
                    np.sin(th) * np.sin(phi_a),
                    np.cos(th),
                ])
                arrows.add(Arrow3D(
                    start=d * 0.12,
                    end=d * (R + 0.55),
                    color=CLR_N,
                    thickness=0.008,
                ))
        self.play(LaggedStart(*[Create(a) for a in arrows],
                               lag_ratio=0.04, run_time=1.5))

        # Overlays: FadeIn limpio sin parpadeo
        nl = MathTex(r"\hat{n} = \hat{r}", font_size=S_SUB, color=CLR_N)
        nl.move_to(ZONE_NOTE)
        nb = BackgroundRectangle(nl, fill_opacity=0.92, buff=0.15, color=BG)
        self.add_fixed_in_frame_mobjects(nb, nl)
        self.play(FadeIn(nb), FadeIn(nl))

        da_eq = MathTex(r"d\vec{a}", "=", r"da\,\hat{n}", font_size=S_LBL)
        da_eq[0].set_color(CLR_N)
        da_eq[2].set_color(CLR_N)
        da_eq.to_corner(UR, buff=0.6)
        da_bg = BackgroundRectangle(da_eq, fill_opacity=0.92, buff=0.12, color=BG)
        self.add_fixed_in_frame_mobjects(da_bg, da_eq)
        self.play(FadeIn(da_bg), FadeIn(da_eq))

        # OPTIMIZACIÓN: rotación 2s en vez de 3s
        self.begin_ambient_camera_rotation(rate=0.12)
        self.wait(2)
        self.stop_ambient_camera_rotation()

        self.play(*[FadeOut(m) for m in [
            esf, arrows, cq, ejes, xl, yl, zl,
            hdr, nb, nl, da_bg, da_eq,
        ]])
        self.move_camera(phi=0, theta=-PI / 2, run_time=1)

    # ═══════════════════════════════════════════════════════════════════════
    # 4. FLUJO ELÉCTRICO — 2D, sin fixed_in_frame
    # ═══════════════════════════════════════════════════════════════════════
    def escena_flujo(self):
        self.set_camera_orientation(phi=0, theta=-PI / 2)

        ttl = Text("Flujo Eléctrico", font_size=S_TITLE, color=CLR_FLUX)
        ttl.move_to(ZONE_TTL)
        self.play(Write(ttl))

        circ = Circle(radius=2.0, color=CLR_S, stroke_width=2)
        cq   = Dot(ORIGIN, radius=0.1, color=CLR_Q)
        ql   = MathTex("+q", color=CLR_Q, font_size=S_LBL).next_to(cq, DL, buff=0.1)
        self.play(FadeIn(circ), FadeIn(cq), FadeIn(ql))

        # Flechas desde el origen, atraviesan el círculo
        flechas = VGroup()
        for i in range(16):
            a = i * TAU / 16
            flechas.add(Arrow(
                [0.15 * np.cos(a), 0.15 * np.sin(a), 0],
                [2.9  * np.cos(a), 2.9  * np.sin(a), 0],
                color=CLR_E, buff=0, stroke_width=1.6,
                max_tip_length_to_length_ratio=0.10,
            ))
        self.play(LaggedStart(*[GrowArrow(f) for f in flechas],
                               lag_ratio=0.04, run_time=1.5))

        eq = MathTex(
            r"\Phi_E", "=", r"\oint_S",
            r"\vec{E}", r"\cdot", r"d\vec{a}",
            font_size=S_EQ,
        )
        eq[0].set_color(CLR_FLUX)
        eq[3].set_color(CLR_E)
        eq[5].set_color(CLR_N)
        eq.move_to(ZONE_NOTE + UP * 0.4)
        ebg = BackgroundRectangle(eq, fill_opacity=0.92, buff=0.2, color=BG)
        self.play(FadeIn(ebg), Write(eq))

        pp = RIGHT * 2.0
        ev = Arrow(pp, pp + RIGHT * 0.9, color=CLR_E, stroke_width=3, buff=0)
        el = MathTex(r"\vec{E}", font_size=S_NOTE, color=CLR_E).next_to(ev, UP, buff=0.05)
        dv = Arrow(pp + DOWN * 0.18, pp + DOWN * 0.18 + RIGHT * 0.6,
                   color=CLR_N, stroke_width=3, buff=0)
        dl = MathTex(r"d\vec{a}", font_size=S_NOTE, color=CLR_N).next_to(dv, DOWN, buff=0.05)
        par = MathTex(r"\theta=0", font_size=S_NOTE, color=CLR_N)
        par.next_to(pp, UP, buff=0.55)
        self.play(GrowArrow(ev), FadeIn(el), GrowArrow(dv), FadeIn(dl), Write(par))
        self.wait(2)

        self.play(*[FadeOut(m) for m in [
            ttl, circ, cq, ql, flechas, ebg, eq, ev, el, dv, dl, par,
        ]])

    # ═══════════════════════════════════════════════════════════════════════
    # 5. DEDUCCIÓN MATEMÁTICA — 2D, sin fixed_in_frame
    #    TransformMatchingTex funciona perfectamente en phi=0
    # ═══════════════════════════════════════════════════════════════════════
    def escena_deduccion(self):
        self.set_camera_orientation(phi=0, theta=-PI / 2)

        ttl = Text("Deducción Matemática", font_size=S_TITLE, color=CLR_S)
        ttl.move_to(ZONE_TTL)
        self.play(Write(ttl))

        def paso_label(txt):
            p = Text(txt, font_size=S_NOTE, color=GREY_C)
            p.move_to(ZONE_NOTE + UP * 0.5)
            return p

        def nota_cap(tex, color=CLR_RES):
            n = MathTex(tex, font_size=S_NOTE, color=color)
            n.move_to(ZONE_NOTE)
            cap = _capsule(n, color)
            self.play(FadeIn(cap), Write(n))
            return VGroup(cap, n)

        # PASO 1
        e1 = MathTex(
            r"{{ \Phi_E }}", r"{{ = }}",
            r"{{ \oint_S }}", r"{{ \vec{E} }}",
            r"{{ \cdot }}", r"{{ d\vec{a} }}",
            font_size=S_SUB,
        )
        e1[0].set_color(CLR_FLUX)
        e1[3].set_color(CLR_E)
        e1[5].set_color(CLR_N)
        e1.move_to(ZONE_EQ)
        p1 = paso_label("Paso 1 · Definición de flujo")
        self.play(Write(e1), FadeIn(p1))
        self.wait(1.5)
        self.play(FadeOut(p1))

        # PASO 2
        e2 = MathTex(
            r"{{ \Phi_E }}", r"{{ = }}",
            r"{{ \oint_S }}",
            r"{{ \frac{q}{4\pi\epsilon_0 r^2} }}",
            r"{{ \hat{r} }}", r"{{ \cdot }}",
            r"{{ \hat{r} }}", r"{{ \,da }}",
            font_size=S_SUB,
        )
        e2[0].set_color(CLR_FLUX)
        e2[3].set_color(CLR_Q)
        e2[4].set_color(CLR_N)
        e2[6].set_color(CLR_N)
        e2.move_to(ZONE_EQ)
        p2 = paso_label("Paso 2 · Sustituir E y da")
        self.play(
            TransformMatchingTex(e1, e2, transform_mismatches=True, run_time=2),
            FadeIn(p2),
        )
        self.wait(1.5)
        self.play(FadeOut(p2))

        nc1 = nota_cap(r"\hat{r} \cdot \hat{r} = 1", CLR_N)
        self.wait(0.8)

        # PASO 3
        e3 = MathTex(
            r"{{ \Phi_E }}", r"{{ = }}",
            r"{{ \oint_S }}",
            r"{{ \frac{q}{4\pi\epsilon_0 r^2} }}",
            r"{{ \,da }}",
            font_size=S_SUB,
        )
        e3[0].set_color(CLR_FLUX)
        e3[3].set_color(CLR_Q)
        e3.move_to(ZONE_EQ)
        p3 = paso_label("Paso 3 · r̂ · r̂ = 1")
        self.play(
            TransformMatchingTex(e2, e3, transform_mismatches=True, run_time=1.5),
            FadeOut(nc1),
            FadeIn(p3),
        )
        self.wait(1.5)
        self.play(FadeOut(p3))

        # PASO 4
        nc2 = nota_cap(
            r"E \text{ cte. en esfera} \Rightarrow \text{sale de } \oint",
            GREY_B,
        )
        self.wait(0.5)
        e4 = MathTex(
            r"{{ \Phi_E }}", r"{{ = }}",
            r"{{ \frac{q}{4\pi\epsilon_0 r^2} }}",
            r"{{ \oint_S }}", r"{{ da }}",
            font_size=S_SUB,
        )
        e4[0].set_color(CLR_FLUX)
        e4[2].set_color(CLR_Q)
        e4.move_to(ZONE_EQ)
        p4 = paso_label("Paso 4 · E sale de la integral")
        self.play(
            ReplacementTransform(e3, e4, run_time=1.5),
            FadeOut(nc2),
            FadeIn(p4),
        )
        self.wait(1.5)
        self.play(FadeOut(p4))

        # PASO 5
        nc3 = nota_cap(r"\oint_S da = 4\pi r^2", CLR_N)
        self.wait(0.5)
        e5 = MathTex(
            r"{{ \Phi_E }}", r"{{ = }}",
            r"{{ \frac{q}{4\pi\epsilon_0 r^2} }}",
            r"{{ \cdot }}",
            r"{{ 4\pi r^2 }}",
            font_size=S_SUB,
        )
        e5[0].set_color(CLR_FLUX)
        e5[2].set_color(CLR_Q)
        e5[4].set_color(CLR_N)
        e5.move_to(ZONE_EQ)
        p5 = paso_label("Paso 5 · Área = 4πr²")
        self.play(
            TransformMatchingTex(e4, e5, transform_mismatches=True, run_time=1.8),
            FadeOut(nc3),
            FadeIn(p5),
        )
        self.wait(1.5)
        self.play(FadeOut(p5))

        # CANCELACIÓN 4πr²
        cancel_lbl = MathTex(
            r"4\pi r^2 \text{ se cancela}",
            font_size=S_NOTE, color=CLR_CANCEL,
        )
        cancel_lbl.move_to(ZONE_NOTE + UP * 0.8)
        cl_cap = _capsule(cancel_lbl, CLR_CANCEL)
        self.play(FadeIn(cl_cap), Write(cancel_lbl))
        cross_frac = Cross(e5[2], color=CLR_CANCEL, stroke_width=3)
        cross_4pi  = Cross(e5[4], color=CLR_CANCEL, stroke_width=3)
        self.play(Create(cross_frac), Create(cross_4pi), run_time=0.8)
        self.wait(1.0)

        # PASO 6 — Resultado
        e6 = MathTex(
            r"{{ \Phi_E }}", r"{{ = }}",
            r"{{ \frac{q}{\epsilon_0} }}",
            font_size=60,
        )
        e6[0].set_color(CLR_FLUX)
        e6[2].set_color(CLR_RES)
        e6.move_to(ZONE_EQ)
        self.play(
            ReplacementTransform(e5, e6, run_time=2),
            FadeOut(cross_frac), FadeOut(cross_4pi),
            FadeOut(cl_cap), FadeOut(cancel_lbl),
        )
        box = SurroundingRectangle(
            e6, color=CLR_RES, buff=0.35,
            stroke_width=3, corner_radius=0.15,
        )
        self.play(Create(box))
        self.wait(2.5)
        self.play(FadeOut(ttl), FadeOut(e6), FadeOut(box))

    # ═══════════════════════════════════════════════════════════════════════
    # 6. LEY DE GAUSS — 2D, sin fixed_in_frame
    # ═══════════════════════════════════════════════════════════════════════
    def escena_resultado(self):
        self.set_camera_orientation(phi=0, theta=-PI / 2)

        ttl = Text("Ley de Gauss", font_size=S_TITLE, color=CLR_E)
        ttl.move_to(ZONE_TTL)

        ley = MathTex(
            r"\oint_S", r"\vec{E}", r"\cdot", r"d\vec{a}", "=",
            r"\frac{Q_{enc}}{\epsilon_0}",
            font_size=S_EQ,
        )
        ley[1].set_color(CLR_E)
        ley[3].set_color(CLR_N)
        ley[5].set_color(CLR_RES)
        ley.move_to(ZONE_EQ + UP * 0.3)

        bx = SurroundingRectangle(
            ley, color=CLR_S, buff=0.35,
            stroke_width=3, corner_radius=0.15,
        )

        exp = VGroup(
            Text("El flujo eléctrico a través de",    font_size=S_TXT, color=GREY_B),
            Text("cualquier superficie cerrada es",    font_size=S_TXT, color=GREY_B),
            Text("proporcional a la carga encerrada.", font_size=S_TXT, color=GREY_B),
        ).arrange(DOWN, buff=0.08)
        exp.next_to(bx, DOWN, buff=0.55)

        sup = MathTex(
            r"Q_{enc}", "=", r"\sum_i q_i",
            font_size=S_TXT, color=GREY_A,
        )
        sup[0].set_color(CLR_RES)
        sup.next_to(exp, DOWN, buff=0.4)

        self.play(Write(ttl))
        self.play(Write(ley, run_time=1.5), Create(bx))
        self.play(FadeIn(exp))
        self.play(FadeIn(sup))
        self.wait(3)
        self.play(*[FadeOut(m) for m in [ttl, exp, sup, ley, bx]])

    # ═══════════════════════════════════════════════════════════════════════
    # 7. FORMA DIFERENCIAL — 2D, sin fixed_in_frame
    # ═══════════════════════════════════════════════════════════════════════
    def escena_diferencial(self):
        self.set_camera_orientation(phi=0, theta=-PI / 2)

        ley_sm = MathTex(
            r"\oint_S", r"\vec{E}", r"\cdot", r"d\vec{a}", "=",
            r"\frac{Q_{enc}}{\epsilon_0}",
            font_size=36,
        )
        ley_sm[1].set_color(CLR_E)
        ley_sm[3].set_color(CLR_N)
        ley_sm[5].set_color(CLR_RES)
        ley_sm.move_to(ZONE_TTL + DOWN * 0.2)
        bx_sm = SurroundingRectangle(
            ley_sm, color=CLR_S, buff=0.15,
            stroke_width=2, corner_radius=0.12,
        )
        li = Text("Forma Integral", font_size=S_NOTE, color=GREY_C)
        li.next_to(bx_sm, DOWN, buff=0.1)
        self.play(FadeIn(ley_sm), Create(bx_sm), FadeIn(li))

        td_ttl = Text("Teorema de la Divergencia", font_size=S_TXT, color=CLR_ACC)
        td_ttl.move_to(ZONE_EQ + UP * 1.1)
        td_eq = MathTex(
            r"\int_V", r"(\nabla \cdot \vec{v})", r"\,d\tau", "=",
            r"\oint_S", r"\vec{v}", r"\cdot", r"d\vec{a}",
            font_size=S_SUB,
        )
        td_eq[1].set_color(CLR_ACC)
        td_eq.next_to(td_ttl, DOWN, buff=0.3)
        self.play(Write(td_ttl))
        self.play(Write(td_eq))
        self.wait(1.5)

        arr = Arrow(UP * 0.1, DOWN * 0.1, color=GREY_A, stroke_width=2)
        arr.next_to(td_eq, DOWN, buff=0.3)
        self.play(GrowArrow(arr))

        fd = MathTex(
            r"\nabla \cdot \vec{E}", "=", r"\frac{\rho}{\epsilon_0}",
            font_size=S_EQ,
        )
        fd[0].set_color(CLR_E)
        fd[2].set_color(CLR_RES)
        fd.next_to(arr, DOWN, buff=0.3)
        fb = SurroundingRectangle(
            fd, color=CLR_ACC, buff=0.25,
            stroke_width=3, corner_radius=0.15,
        )
        ld = Text("Forma Diferencial", font_size=S_NOTE, color=GREY_C)
        ld.next_to(fb, DOWN, buff=0.1)
        nota = Text(
            "La divergencia mide cómo el campo se expande",
            font_size=S_NOTE, color=GREY_B,
        )
        nota.move_to(ZONE_NOTE)

        self.play(Write(fd, run_time=1.5), Create(fb))
        self.play(FadeIn(ld), FadeIn(nota))
        self.wait(3)
        self.play(*[FadeOut(m) for m in [
            ley_sm, bx_sm, li, td_ttl, td_eq, arr, fd, fb, ld, nota,
        ]])

    # ═══════════════════════════════════════════════════════════════════════
    # 8. CIERRE 3D
    #    OPTIMIZADO: resolution (10,5), 12 flechas, rotación 3s
    # ═══════════════════════════════════════════════════════════════════════
    def escena_cierre(self):
        self.move_camera(phi=65 * DEGREES, theta=-50 * DEGREES, run_time=1.5)

        ejes = ThreeDAxes(
            x_range=[-3.5, 3.5, 1], y_range=[-3.5, 3.5, 1],
            z_range=[-3.5, 3.5, 1],
            x_length=6, y_length=6, z_length=6,
        )
        ejes.set_color(GREY_C).set_stroke(opacity=0.3)
        self.play(Create(ejes, run_time=1))

        cq = Sphere(radius=0.12, color=CLR_Q).set_opacity(1)
        self.play(FadeIn(cq))

        R = 2.2
        # OPTIMIZACIÓN: resolution (10,5)
        esf = Surface(
            lambda u, v: np.array([
                R * np.sin(v) * np.cos(u),
                R * np.sin(v) * np.sin(u),
                R * np.cos(v),
            ]),
            u_range=[0, TAU], v_range=[0, PI],
            resolution=(10, 5),
            fill_opacity=0.08,
            stroke_width=0.4, stroke_color=CLR_S,
        )
        self.play(Create(esf, run_time=1.5))

        # OPTIMIZACIÓN: 12 flechas (6 phi × 2 alturas)
        lns = VGroup()
        for i in range(6):
            phi_a = i * TAU / 6
            for j in range(1, 3):
                th = j * PI / 3
                d = np.array([
                    np.sin(th) * np.cos(phi_a),
                    np.sin(th) * np.sin(phi_a),
                    np.cos(th),
                ])
                lns.add(Arrow3D(
                    start=d * 0.12,
                    end=d * (R + 0.6),
                    color=CLR_E,
                    thickness=0.008,
                ))
        self.play(LaggedStart(*[Create(l) for l in lns],
                               lag_ratio=0.04, run_time=1.5))

        ef = MathTex(
            r"\oint_S \vec{E} \cdot d\vec{a} = \frac{Q_{enc}}{\epsilon_0}",
            font_size=S_SUB,
        )
        ef.move_to(ZONE_TTL)
        efb = BackgroundRectangle(ef, fill_opacity=0.9, buff=0.2, color=BG)
        self.add_fixed_in_frame_mobjects(efb, ef)
        self.play(FadeIn(efb), FadeIn(ef))

        brand = Text("@lomejorphysics", font_size=S_TXT, color=CLR_Q)
        brand.move_to(ZONE_NOTE)
        self.add_fixed_in_frame_mobjects(brand)
        self.play(FadeIn(brand))

        # OPTIMIZACIÓN: rotación 3s en vez de 5s
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(3)
        self.stop_ambient_camera_rotation()

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.5)