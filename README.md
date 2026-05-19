# 🎬 Manim Physics — @lomejorphysics

Educational physics animations built with [Manim](https://www.manim.community/) for [@lomejorphysics](https://instagram.com/lomejorphysics) — an Instagram channel dedicated to showing the mathematical foundations behind physical phenomena.

## 🎥 Animations

| Topic | Description | Key Concepts |
|-------|-------------|--------------|
| [**Gauss's Law**](./ley_de_gauss/) | Full derivation with 3D Gaussian surface, vector field visualization, and step-by-step math | ∇·E = ρ/ε₀, flux integral, spherical symmetry |
| [**Electric Field**](./campo_electrico/) | Vector field visualization with ArrowVectorField + point charge interactions | Coulomb's law, superposition, field lines |
| [**Electric Potential**](./potencial_electrico/) | Scalar potential visualization with equipotential surfaces | V = kQ/r, gradient → E, work-energy |
| [**Electric Dipole**](./dipolo_electrico/) | Dipole field and potential with 3D visualization | p = qd, far-field approximation, torque |
| [**Electrostatic Energy**](./energia_electrostatica/) | Energy stored in charge distributions and capacitors | U = ½ε₀∫E²dV, capacitance |
| [**Electric Current**](./corriente_electrica/) | Current flow, resistance, and Ohm's law with animated charges | J = σE, drift velocity, circuits |

## ⭐ Featured

The **Gauss's Law** animation reached **400+ likes** on Instagram in 2 days — the channel's most successful video.

## 🛠️ Tech Stack

- **Manim** v0.18.1 — Mathematical animation engine (3Blue1Brown style)
- **Python** — All animations are pure Python
- **LaTeX** — Equations rendered with MathTex
- **3D Scenes** — ThreeDScene for Gaussian surfaces and spatial visualizations

## 🚀 How to Run

```bash
# Install Manim (via micromamba)
micromamba create -n manim python=3.11
micromamba activate manim
pip install manim

# Preview (low quality, fast)
manim -ql archivo.py SceneName

# Production quality (1080x1920 for Instagram Reels)
manim -qh --fps 60 -r 1080,1920 archivo.py SceneName
```

## 🎨 Style

- **Dark background** with warm color palette (gold, orange, teal)
- **Step-by-step mathematical derivations** — no shortcuts
- **Vector field visualizations** using `ArrowVectorField`
- **3D scenes** with camera rotation for spatial concepts
- **Branding** — @lomejorphysics at start and end of each video

---

<div align="center">

*Made with ❤️ and physics — [@lomejorphysics](https://instagram.com/lomejorphysics)*

</div>
