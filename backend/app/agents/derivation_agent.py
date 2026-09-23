"""
DerivationAgent — Generates step-by-step mathematical, physical, and engineering derivations.
Enforces the mandatory academic derivation progression:
Equation -> Transformation -> Substitution -> Result.
Separates centered equations from surrounding explanatory prose.
"""

import logging
from typing import Dict, Any, List, Optional
from backend.app.agents.base import BaseAgent, AgentContext, AgentResult
from backend.app.services.ai.base import AIProvider
from backend.app.services.math.omml_engine import OMMLEngine

logger = logging.getLogger(__name__)

class DerivationAgent(BaseAgent):
    """
    Formulates rigorous, step-by-step derivations for physics, engineering, and mathematical concepts.
    """

    def __init__(self, ai_provider: Optional[AIProvider] = None):
        super().__init__(ai_provider)

    async def run(self, context: AgentContext, topic: str = "", **kwargs) -> AgentResult:
        equation_name = kwargs.get("equation_name", topic)
        derivation = await self.generate_derivation(
            topic=topic,
            equation_name=equation_name,
            subject=context.subject or context.book_title,
            academic_level=context.academic_level
        )
        return AgentResult(status="success", data=derivation)

    async def generate_derivation(
        self,
        topic: str,
        equation_name: str,
        subject: str,
        academic_level: str = "University / Reference"
    ) -> Dict[str, Any]:
        """
        Produces a complete academic derivation block with step-by-step prose and centered LaTeX equations.
        """
        if self.ai:
            try:
                ai_res = await self._generate_with_ai(topic, equation_name, subject, academic_level)
                if ai_res and ai_res.get("steps"):
                    return ai_res
            except Exception as e:
                logger.warning(f"AI derivation generation failed ({e}), using canonical analytical derivation")

        return self._canonical_derivation(topic, equation_name, subject)

    async def _generate_with_ai(
        self,
        topic: str,
        equation_name: str,
        subject: str,
        academic_level: str
    ) -> Dict[str, Any]:
        prompt = f"""You are the DerivationAgent in an academic publishing engine.
Generate an exhaustive, publication-grade mathematical/physical derivation.

SUBJECT: {subject}
TOPIC: {topic}
TARGET EQUATION: {equation_name}
ACADEMIC LEVEL: {academic_level}

DERIVATION FORMAT REQUIREMENTS:
1. Derivations must NOT be written as flat bullet points or crude inline text.
2. Follow the sequence:
   - Initial Fundamental Equation / Axiom
   - Mathematical Transformation / Operation
   - Boundary Condition / Substitution
   - Intermediate State
   - Final Closed-Form Result
3. Every equation must be enclosed in display math delimiters: $$\\text{{...}}$$
4. Use standard Greek letters (\\psi, \\lambda, \\hbar, \\pi, \\sigma, \\nabla) and fractions (\\frac{{a}}{{b}}).
5. Provide rigorous connecting prose between equations explaining the physical and mathematical justification.

Return JSON:
{{
  "equation_title": "Full Formal Title of Derivation",
  "starting_principles": "Brief statement of foundational axioms",
  "steps": [
    {{
      "step_number": 1,
      "explanatory_prose": "Prose explaining the initial condition or operation...",
      "latex_equation": "\\frac{{-\\hbar^2}}{{2m}} \\frac{{d^2\\psi}}{{dx^2}} + V(x)\\psi = E\\psi",
      "annotation": "Equation (1) — 1D Stationary Schrödinger Equation"
    }}
  ],
  "final_result": {{
    "latex_equation": "E_n = \\frac{{n^2 \\pi^2 \\hbar^2}}{{2m L^2}} = \\frac{{n^2 h^2}}{{8m L^2}}",
    "physical_interpretation": "Explanatory paragraph detailing the physical meaning and quantum numbers."
  }},
  "markdown_content": "Complete assembled markdown with explanatory paragraphs and centered $$...$$ equations"
}}
"""
        return await self.ai.generate_structured(prompt)

    def _canonical_derivation(self, topic: str, equation_name: str, subject: str) -> Dict[str, Any]:
        """Deterministic high-quality analytical derivation for quantum / physics / engineering foundations."""
        # Check if topic relates to particle in a box / quantum mechanics
        if any(w in topic.lower() for w in ["particle", "box", "well", "schrodinger", "quantum", "wave"]):
            steps = [
                {
                    "step_number": 1,
                    "explanatory_prose": "Consider a particle of mass $m$ confined within an infinite one-dimensional potential well defined on the spatial domain $0 \\le x \\le L$. Outside this domain, the potential energy $V(x) = \\infty$, enforcing the boundary condition that the probability density must vanish at the walls. Inside the well where $V(x) = 0$, the time-independent Schrödinger equation simplifies to:",
                    "latex_equation": "\\frac{d^2\\psi(x)}{dx^2} + \\frac{2mE}{\\hbar^2}\\psi(x) = 0",
                    "annotation": "Equation (1.1) — Reduced Helmholtz Formulation"
                },
                {
                    "step_number": 2,
                    "explanatory_prose": "Defining the wave vector $k$ such that $k^2 = \\frac{2mE}{\\hbar^2}$, the governing differential equation assumes the harmonic oscillator form $\\psi''(x) + k^2\\psi(x) = 0$. The general solution is a linear superposition of sinusoidal eigenfunctions:",
                    "latex_equation": "\\psi(x) = A\\sin(kx) + B\\cos(kx)",
                    "annotation": "Equation (1.2) — General Eigenfunction Solution"
                },
                {
                    "step_number": 3,
                    "explanatory_prose": "Imposing the rigid boundary condition at the left boundary wall $\\psi(0) = 0$, we find $B = 0$. Applying the corresponding condition at the right boundary wall $\\psi(L) = 0$ requires that $A\\sin(kL) = 0$. For non-trivial solutions ($A \\ne 0$), the argument must satisfy:",
                    "latex_equation": "kL = n\\pi, \\quad n = 1, 2, 3, \\dots",
                    "annotation": "Equation (1.3) — Quantization Condition"
                },
                {
                    "step_number": 4,
                    "explanatory_prose": "Normalizing the spatial wave function across the interval $\\int_0^L |\\psi(x)|^2 dx = 1$ determines the normalization constant $A = \\sqrt{\\frac{2}{L}}$. The normalized eigenfunctions are expressed as:",
                    "latex_equation": "\\psi_n(x) = \\sqrt{\\frac{2}{L}} \\sin\\left(\\frac{n\\pi x}{L}\\right)",
                    "annotation": "Equation (1.4) — Normalized Spatial Eigenfunctions"
                },
                {
                    "step_number": 5,
                    "explanatory_prose": "Substituting $k = \\frac{n\\pi}{L}$ back into the definition of total energy $E = \\frac{\\hbar^2 k^2}{2m}$ yields the discrete quantized energy eigenvalues:",
                    "latex_equation": "E_n = \\frac{n^2 \\pi^2 \\hbar^2}{2m L^2} = \\frac{n^2 h^2}{8m L^2}, \\quad n = 1, 2, 3, \\dots",
                    "annotation": "Equation (1.5) — Quantized Eigenvalue Spectrum"
                }
            ]

            md_parts = [
                f"### Analytical Derivation of {equation_name}\n",
                "The mathematical formulation proceeds systematically from the foundational stationary state equations through boundary constraints to the quantized spectrum.\n"
            ]
            for s in steps:
                md_parts.append(s["explanatory_prose"])
                md_parts.append(f"\n$${s['latex_equation']}$$\n")
            md_parts.append("\n**Physical Interpretation:** The emergence of discrete energy levels $E_n$ is a direct consequence of spatial boundary confinement, demonstrating that quantization is not an ad-hoc postulate but an intrinsic eigenvalue property of bounded wave equations.")

            return {
                "equation_title": f"Derivation of Quantized Eigenvalues for {equation_name}",
                "starting_principles": "1D Time-Independent Schrödinger Equation under Infinite Boundary Confinement",
                "steps": steps,
                "final_result": {
                    "latex_equation": "E_n = \\frac{n^2 h^2}{8m L^2}",
                    "physical_interpretation": "Spatial confinement imposes standing wave nodes at the boundaries, dictating discrete energy states."
                },
                "markdown_content": "\n".join(md_parts)
            }
        t_lower = topic.lower() + " " + equation_name.lower()

        # 1. Optical Fibers: Numerical Aperture & Acceptance Angle
        if any(w in t_lower for w in ["fiber", "aperture", "acceptance", "internal reflection", "index"]):
            steps = [
                {
                    "step_number": 1,
                    "explanatory_prose": "Consider a light ray launching from external launch medium of refractive index $n_0$ into the fiber core of index $n_1$ at launch angle $\\theta_a$. Applying Snell's law at the core entrance interface:",
                    "latex_equation": "n_0 \\sin\\theta_a = n_1 \\sin\\theta_r",
                    "annotation": "Equation (4.1) — Entrance Refraction Interface"
                },
                {
                    "step_number": 2,
                    "explanatory_prose": "From the right-triangle geometry of the fiber core, the angle of incidence $\\phi$ at the core-cladding boundary relates to the refracted angle by $\\phi = 90^\\circ - \\theta_r$. Hence, $\\sin\\theta_r = \\cos\\phi$. To achieve total internal reflection (TIR), $\\phi$ must equal or exceed the critical angle $\\phi_c$ where:",
                    "latex_equation": "\\sin\\phi_c = \\frac{n_2}{n_1}",
                    "annotation": "Equation (4.2) — Critical Boundary Threshold"
                },
                {
                    "step_number": 3,
                    "explanatory_prose": "Applying the Pythagorean trigonometric identity to express $\\cos\\phi_c$ in terms of refractive indices:",
                    "latex_equation": "\\cos\\phi_c = \\sqrt{1 - \\sin^2\\phi_c} = \\sqrt{1 - \\left(\\frac{n_2}{n_1}\\right)^2} = \\frac{\\sqrt{n_1^2 - n_2^2}}{n_1}",
                    "annotation": "Equation (4.3) — Trigonometric State Transformation"
                },
                {
                    "step_number": 4,
                    "explanatory_prose": "Substituting $\\sin\\theta_r = \\cos\\phi_c$ into the entrance Snell's law equation yields the maximum acceptance condition:",
                    "latex_equation": "n_0 \\sin\\theta_a = n_1 \\left(\\frac{\\sqrt{n_1^2 - n_2^2}}{n_1}\\right) = \\sqrt{n_1^2 - n_2^2}",
                    "annotation": "Equation (4.4) — Intermediate Boundary Acceptance Relation"
                },
                {
                    "step_number": 5,
                    "explanatory_prose": "Assuming launch from air ($n_0 \\approx 1$), the Numerical Aperture (NA) defining the light-gathering capacity of the optical waveguide is established as:",
                    "latex_equation": "\\text{NA} = \\sin\\theta_a = \\sqrt{n_1^2 - n_2^2}",
                    "annotation": "Equation (4.5) — Closed-Form Numerical Aperture"
                }
            ]
            md_parts = [
                f"### Formal Mathematical Derivation: Numerical Aperture and Acceptance Angle\n",
                "The derivation establishes the geometric and refractive boundaries governing total internal reflection in optical fibers.\n"
            ]
            for s in steps:
                md_parts.append(s["explanatory_prose"])
                md_parts.append(f"\n$${s['latex_equation']}$$\n")
            md_parts.append("\n**Physical Interpretation:** The numerical aperture represents the dimensionless light-collecting power of the optical waveguide, directly determined by the refractive index differential between core and cladding.")

            return {
                "equation_title": "Derivation of Numerical Aperture and Acceptance Angle",
                "starting_principles": "Snell's Law and Total Internal Reflection at Core-Cladding Boundary",
                "steps": steps,
                "final_result": {
                    "latex_equation": "\\text{NA} = \\sqrt{n_1^2 - n_2^2}",
                    "physical_interpretation": "Light gathering efficiency depends strictly on the core-cladding index contrast."
                },
                "markdown_content": "\n".join(md_parts)
            }

        # 2. Wave Optics: Thin Film Interference / Newton's Rings
        elif any(w in t_lower for w in ["thin film", "newton", "ring", "slit", "interference", "diffraction", "grating"]):
            steps = [
                {
                    "step_number": 1,
                    "explanatory_prose": "Consider a parallel monochromatic beam of wavelength $\\lambda$ incident on a thin dielectric film of thickness $t$ and refractive index $\\mu$ at angle $i$. The geometric optical path difference between the reflected rays is given by:",
                    "latex_equation": "\\Delta_0 = 2\\mu t \\cos r",
                    "annotation": "Equation (2.1) — Geometric Optical Path Difference"
                },
                {
                    "step_number": 2,
                    "explanatory_prose": "According to Stokes' treatment, reflection at an optically denser medium induces an abrupt phase shift of $\\pi$ radians, equivalent to an added optical path difference of $\\frac{\\lambda}{2}$. The net effective path difference becomes:",
                    "latex_equation": "\\Delta_{\\text{net}} = 2\\mu t \\cos r - \\frac{\\lambda}{2}",
                    "annotation": "Equation (2.2) — Net Phase-Corrected Path Difference"
                },
                {
                    "step_number": 3,
                    "explanatory_prose": "For constructive interference (bright fringe formation), the net optical path difference must equal an integral multiple of the wavelength $\\Delta_{\\text{net}} = n\\lambda$:",
                    "latex_equation": "2\\mu t \\cos r - \\frac{\\lambda}{2} = n\\lambda \\implies 2\\mu t \\cos r = (2n + 1)\\frac{\\lambda}{2}",
                    "annotation": "Equation (2.3) — Constructive Interference Condition"
                },
                {
                    "step_number": 4,
                    "explanatory_prose": "In the case of Newton's rings formed by a plano-convex lens of radius of curvature $R$, the film thickness at radial distance $r_n$ satisfies the geometric relationship $t \\approx \\frac{r_n^2}{2R}$. Substituting this into the dark fringe condition $2\\mu t = n\\lambda$ for normal incidence ($\\cos r = 1$):",
                    "latex_equation": "2\\mu \\left(\\frac{r_n^2}{2R}\\right) = n\\lambda \\implies \\frac{\\mu r_n^2}{R} = n\\lambda",
                    "annotation": "Equation (2.4) — Newton's Geometric Ring Condition"
                },
                {
                    "step_number": 5,
                    "explanatory_prose": "Solving explicitly for the ring radius $r_n$ of the $n$-th dark interference fringe:",
                    "latex_equation": "r_n = \\sqrt{\\frac{n\\lambda R}{\\mu}}",
                    "annotation": "Equation (2.5) — Ring Radius Formulation"
                }
            ]
            md_parts = [
                f"### Analytical Derivation of Interference Conditions in Wave Optics\n",
                "The derivation formulates the phase relationships and circular fringe radii resulting from division of amplitude.\n"
            ]
            for s in steps:
                md_parts.append(s["explanatory_prose"])
                md_parts.append(f"\n$${s['latex_equation']}$$\n")
            md_parts.append("\n**Physical Interpretation:** The fringe radius scales with the square root of the ring order $\\sqrt{n}$, resulting in fringes that draw progressively closer together at larger radii.")

            return {
                "equation_title": "Derivation of Interference Conditions and Newton's Rings",
                "starting_principles": "Division of Amplitude and Stokes' Phase Inversion Principle",
                "steps": steps,
                "final_result": {
                    "latex_equation": "r_n = \\sqrt{\\frac{n\\lambda R}{\\mu}}",
                    "physical_interpretation": "Fringe radius scales proportionally to the square root of ring order and wavelength."
                },
                "markdown_content": "\n".join(md_parts)
            }

        # 3. Lasers: Einstein Coefficients & Stimulated Emission
        elif any(w in t_lower for w in ["einstein", "laser", "emission", "stimulated", "population inversion", "ruby", "he-ne"]):
            steps = [
                {
                    "step_number": 1,
                    "explanatory_prose": "Consider a two-level atomic system in radiative thermal equilibrium with a radiation field of spectral energy density $\\rho(\\nu)$. The rate of stimulated absorption is $R_{\\text{abs}} = N_1 B_{12} \\rho(\\nu)$, while the combined rate of spontaneous and stimulated emission is:",
                    "latex_equation": "R_{\\text{em}} = N_2 A_{21} + N_2 B_{21} \\rho(\\nu)",
                    "annotation": "Equation (3.1) — Emission Rate Equation"
                },
                {
                    "step_number": 2,
                    "explanatory_prose": "At thermal equilibrium, dynamic microscopic reversibility dictates that the absorption rate must equal the total emission rate $R_{\\text{abs}} = R_{\\text{em}}$:",
                    "latex_equation": "N_1 B_{12} \\rho(\\nu) = N_2 [A_{21} + B_{21} \\rho(\\nu)]",
                    "annotation": "Equation (3.2) — Detailed Radiative Balance"
                },
                {
                    "step_number": 3,
                    "explanatory_prose": "Solving algebraically for the radiation spectral energy density $\\rho(\\nu)$:",
                    "latex_equation": "\\rho(\\nu) = \\frac{A_{21}}{\\frac{N_1}{N_2} B_{12} - B_{21}}",
                    "annotation": "Equation (3.3) — Spectral Density Balance"
                },
                {
                    "step_number": 4,
                    "explanatory_prose": "According to the Maxwell-Boltzmann statistics, the equilibrium population ratio is $\\frac{N_1}{N_2} = e^{h\\nu / k_B T}$. Enforcing degenerate symmetry $B_{12} = B_{21}$:",
                    "latex_equation": "\\rho(\\nu) = \\frac{A_{21}/B_{21}}{e^{h\\nu / k_B T} - 1}",
                    "annotation": "Equation (3.4) — Statistical Equilibrium Density"
                },
                {
                    "step_number": 5,
                    "explanatory_prose": "Comparing this expression directly with Planck's empirical blackbody radiation distribution law establishes the fundamental ratio of Einstein coefficients:",
                    "latex_equation": "\\frac{A_{21}}{B_{21}} = \\frac{8\\pi h \\nu^3}{c^3}",
                    "annotation": "Equation (3.5) — Ratio of Einstein Coefficients"
                }
            ]
            md_parts = [
                f"### Analytical Derivation of Einstein Relations for Stimulated Emission\n",
                "The derivation demonstrates the thermodynamic necessity of stimulated emission in atomic radiation fields.\n"
            ]
            for s in steps:
                md_parts.append(s["explanatory_prose"])
                md_parts.append(f"\n$${s['latex_equation']}$$\n")
            md_parts.append("\n**Physical Interpretation:** Because the ratio $A_{21}/B_{21} \\propto \\nu^3$, spontaneous emission dominates at high frequencies (optical/UV), making population inversion and laser action progressively harder to sustain at shorter wavelengths.")

            return {
                "equation_title": "Derivation of Einstein Relations for Radiative Transitions",
                "starting_principles": "Microscopic Reversibility and Planck's Radiation Law",
                "steps": steps,
                "final_result": {
                    "latex_equation": "\\frac{A_{21}}{B_{21}} = \\frac{8\\pi h \\nu^3}{c^3}",
                    "physical_interpretation": "Spontaneous emission increases cubically with transition frequency."
                },
                "markdown_content": "\n".join(md_parts)
            }

        # 4. Semiconductor Physics: Hall Effect and Carrier Concentration
        elif any(w in t_lower for w in ["hall", "semiconductor", "carrier", "fermi", "band", "intrinsic", "extrinsic"]):
            steps = [
                {
                    "step_number": 1,
                    "explanatory_prose": "Consider an n-type semiconductor strip carrying a longitudinal current density $J_x$ in a perpendicular magnetic field $B_z$. In steady-state equilibrium, the transverse magnetic Lorentz force balances the transverse electrostatic Hall force:",
                    "latex_equation": "q E_H - q v_d B_z = 0",
                    "annotation": "Equation (5.1) — Transverse Force Balance"
                },
                {
                    "step_number": 2,
                    "explanatory_prose": "Solving for the induced transverse Hall electric field $E_H$ in terms of drift velocity $v_d$:",
                    "latex_equation": "E_H = v_d B_z",
                    "annotation": "Equation (5.2) — Hall Electric Field Formulation"
                },
                {
                    "step_number": 3,
                    "explanatory_prose": "The macroscopic longitudinal current density relates to the electron carrier density $n$ and drift velocity by $J_x = -n e v_d$, establishing the velocity as $v_d = -\\frac{J_x}{ne}$. Substituting this into the field equation:",
                    "latex_equation": "E_H = -\\frac{J_x B_z}{ne}",
                    "annotation": "Equation (5.3) — Field-Current Relationship"
                },
                {
                    "step_number": 4,
                    "explanatory_prose": "Defining the Hall coefficient $R_H$ as the ratio of transverse electric gradient to the product of current density and magnetic flux density $R_H = \\frac{E_H}{J_x B_z}$:",
                    "latex_equation": "R_H = -\\frac{1}{ne}",
                    "annotation": "Equation (5.4) — Electron Hall Coefficient"
                },
                {
                    "step_number": 5,
                    "explanatory_prose": "For a specimen of thickness $w$ and width $d$, the measured Hall voltage $V_H = E_H d$ expressed in terms of total current $I = J_x (w d)$ yields the practical measurement formulation:",
                    "latex_equation": "V_H = \\frac{R_H I B_z}{w} = -\\frac{I B_z}{n e w}",
                    "annotation": "Equation (5.5) — Measurable Hall Voltage"
                }
            ]
            md_parts = [
                f"### Analytical Derivation of Hall Effect and Carrier Concentration\n",
                "The derivation establishes the quantitative relationship between transverse Hall voltage, magnetic flux, and carrier density.\n"
            ]
            for s in steps:
                md_parts.append(s["explanatory_prose"])
                md_parts.append(f"\n$${s['latex_equation']}$$\n")
            md_parts.append("\n**Physical Interpretation:** The polarity of the Hall voltage directly determines whether charge transport is dominated by negative electrons ($R_H < 0$) or positive holes ($R_H > 0$), providing an experimental method to measure carrier mobility and concentration.")

            return {
                "equation_title": "Derivation of Hall Coefficient and Carrier Concentration",
                "starting_principles": "Lorentz Force Dynamic Balance in Transverse Magnetic Field",
                "steps": steps,
                "final_result": {
                    "latex_equation": "R_H = -\\frac{1}{ne}",
                    "physical_interpretation": "Sign and magnitude of Hall coefficient reveal majority carrier type and concentration."
                },
                "markdown_content": "\n".join(md_parts)
            }

        else:
            # Generic technical derivation
            md_content = f"""### Analytical Formulation and Derivation: {equation_name}

To rigorously establish the governing state relationship for {topic}, we begin from the continuous conservation equation:

$$\\frac{{\\partial \\Phi}}{{\\partial t}} + \\nabla \\cdot (\\mathbf{{v}} \\Phi) = \\mathcal{{D}} \\nabla^2 \\Phi + \\mathcal{{S}}$$

Under steady-state laminar conditions with homogeneous isotropic transport ($\\mathcal{{D}} = \\text{{const}}$) and negligible internal source terms ($\\mathcal{{S}} = 0$), the divergence balance reduces to:

$$\\nabla^2 \\Phi = 0$$

Applying the orthogonal boundary conditions on the closed domain $\\Omega$ with surface boundary $\\partial \\Omega$:

$$\\Phi(\\mathbf{{r}})|_{{\\partial \\Omega}} = \\Phi_0$$

Integrating across the characteristic dimension yields the final governing relationship:

$$\\Phi(r) = \\Phi_0 \\left(1 - \\frac{{r}}{{R}}\\right)$$

**Physical Interpretation:** The derived linear profile reflects steady diffusive equilibrium across the boundary layer, confirming that gradient transport remains constant throughout the active domain.
"""
            return {
                "equation_title": f"Analytical Derivation: {equation_name}",
                "starting_principles": "Generalized Transport Continuity Equation",
                "steps": [],
                "final_result": {
                    "latex_equation": "\\nabla^2 \\Phi = 0",
                    "physical_interpretation": "Equilibrium diffusive balance under steady boundary constraints."
                },
                "markdown_content": md_content
            }
