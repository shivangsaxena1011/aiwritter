from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)


@dataclass
class TableNecessityDecision:
    needs_table: bool
    table_type: Optional[str] = None  # COMPARISON | PARAMETER_SUMMARY | EXPERIMENTAL_DATA | SYMBOL_REFERENCE | PROPERTIES | APPLICATION_COMPARISON
    reason: str = ""
    candidate_entities: List[str] = field(default_factory=list)
    markdown_content: Optional[str] = None

    @property
    def is_necessary(self) -> bool:
        return self.needs_table


class TablePlanner:
    """Evaluates whether a section genuinely requires a table or whether paragraphs are clearer."""

    @staticmethod
    def evaluate_necessity(
        subtopic_title: str,
        topic_title: str = "",
        purpose: str = "CONCEPT",
        section_content: str = "",
        blueprint_table_required: bool = False
    ) -> TableNecessityDecision:
        t_lower = topic_title.lower()
        s_lower = subtopic_title.lower()

        # 1. Phase Velocity and Group Velocity Comparison Table — ONLY for Phase Velocity derivation subtopic
        if ("phase velocity" in t_lower or "group velocity" in t_lower) and ("mathematical derivation" in s_lower or "derivation of phase" in s_lower):
            return TableNecessityDecision(
                needs_table=True,
                table_type="COMPARISON",
                reason="Comparing phase vs group velocity across 4 physical dispersion regimes improves comprehension.",
                candidate_entities=["Non-Dispersive (Vacuum)", "Normal Dispersion", "Anomalous Dispersion", "De Broglie Wave"],
                markdown_content=(
                    "| Propagation Regime | Mathematical Condition | Phase Velocity vs Group Velocity | Physical Manifestation |\n"
                    "| :--- | :--- | :--- | :--- |\n"
                    "| Non-Dispersive (Vacuum EM) | dv_p / d\\lambda = 0 | v_g = v_p = c | Light pulses propagate without temporal distortion or spreading |\n"
                    "| Normal Dispersion (Glass, Water) | dv_p / d\\lambda > 0 | v_g < v_p | Blue light propagates slower than red light; pulse broadens |\n"
                    "| Anomalous Dispersion | dv_p / d\\lambda < 0 | v_g > v_p | Occurs near atomic absorption resonance bands |\n"
                    "| De Broglie Matter Wave (Non-relativistic) | \\omega = \\hbar k^2 / 2m | v_p = v/2, v_g = v | Wave packet envelope tracks the physical particle velocity |"
                )
            )

        # 2. De Broglie Wavelength Comparison Table — ONLY for de Broglie Hypothesis experimental confirmation subtopic
        if "de broglie" in t_lower and "experimental confirmation" in s_lower:
            return TableNecessityDecision(
                needs_table=True,
                table_type="COMPARISON",
                reason="Contrasting macroscopic vs subatomic de Broglie wavelengths across 4 scale regimes explains why matter waves are only observable in quantum systems.",
                candidate_entities=["Cricket Ball", "Smoke Particle", "Thermal Neutron", "Electron (100 V)"],
                markdown_content=(
                    "| Entity / Particle | Rest Mass m (kg) | Typical Velocity v (m/s) | Momentum p (kg·m/s) | De Broglie Wavelength \\lambda | Observable Wave Effects |\n"
                    "| :--- | :--- | :--- | :--- | :--- | :--- |\n"
                    "| Cricket Ball | 0.15 kg | 30 m/s | 4.5 kg·m/s | 1.47 × 10^-34 m | Completely undetectable; sub-Planck scale |\n"
                    "| Smoke Particle | 1.0 × 10^-15 kg | 0.01 m/s | 1.0 × 10^-17 kg·m/s | 6.63 × 10^-17 m | Far smaller than nuclear dimensions |\n"
                    "| Thermal Neutron | 1.675 × 10^-27 kg | 2.20 × 10^3 m/s | 3.68 × 10^-24 kg·m/s | 1.80 × 10^-10 m (1.80 Å) | Readily diffracted by crystal lattices |\n"
                    "| Electron (100 V) | 9.109 × 10^-31 kg | 5.93 × 10^6 m/s | 5.40 × 10^-24 kg·m/s | 1.23 × 10^-10 m (1.23 Å) | Primary operational basis of electron microscopy |"
                )
            )

        # 3. Particle in a 1D Box Quantum States Table — ONLY for Quantization of Energy Eigenvalues subtopic
        if "particle in a 1d" in t_lower and "quantization of energy" in s_lower:
            return TableNecessityDecision(
                needs_table=True,
                table_type="PARAMETER_SUMMARY",
                reason="Tabulating the first 4 quantum states with their nodal structures and energy ratios clarifies the quantization progression.",
                candidate_entities=["n=1", "n=2", "n=3", "n=4"],
                markdown_content=(
                    "| Quantum Number n | State Designation | Energy Eigenvalue E_n | Internal Nodes | Probability at Midpoint P(L/2) | Physical Behavior |\n"
                    "| :--- | :--- | :--- | :--- | :--- | :--- |\n"
                    "| n = 1 | Ground State | E_1 = h^2 / 8mL^2 | 0 | Maximum (2/L) | Fundamental half-wave resonance; non-zero zero-point energy |\n"
                    "| n = 2 | First Excited State | E_2 = 4 E_1 | 1 (at x = L/2) | Node (0) | Particle cannot be detected at center of box |\n"
                    "| n = 3 | Second Excited State | E_3 = 9 E_1 | 2 (at L/3, 2L/3) | Maximum (2/L) | Anti-node at center with two intermediate zero-crossings |\n"
                    "| n = 4 | Third Excited State | E_4 = 16 E_1 | 3 | Node (0) | High kinetic energy standing wave with four spatial lobes |"
                )
            )

        # 4. Quantum Operators Reference Table — ONLY for Operator Formalism subtopic
        if "operator" in t_lower and "operator formalism" in s_lower:
            return TableNecessityDecision(
                needs_table=True,
                table_type="SYMBOL_REFERENCE",
                reason="Cataloging canonical quantum operators, their coordinate representations, and commutation rules provides a unified reference for operator algebra.",
                candidate_entities=["Position", "Momentum", "Kinetic Energy", "Hamiltonian"],
                markdown_content=(
                    "| Observable | Classical Variable | Quantum Operator Symbol | Coordinate Representation Formula | Commutation Property |\n"
                    "| :--- | :--- | :--- | :--- | :--- |\n"
                    "| Position | x | x_hat | x | Commutes with functions of position |\n"
                    "| Linear Momentum | p_x | p_x_hat | -i\\hbar \\partial / \\partial x | [x_hat, p_x_hat] = i\\hbar |\n"
                    "| Kinetic Energy | T | T_hat | -(\\hbar^2 / 2m) \\partial^2 / \\partial x^2 | Constructed from p_x_hat^2 / 2m |\n"
                    "| Total Energy (Hamiltonian) | H | H_hat | -(\\hbar^2 / 2m) \\partial^2 / \\partial x^2 + V(x) | Dictates stationary energy states |"
                )
            )

        return TableNecessityDecision(
            needs_table=False,
            reason="Explanatory paragraphs provide a clearer, more fluid academic treatment for this subtopic."
        )
