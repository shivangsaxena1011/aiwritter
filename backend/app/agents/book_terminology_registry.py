"""
BookTerminologyRegistry — Cross-Chapter Terminology, Symbol, and Notation Registry.
Maintains consistent nomenclature, prevents drift in scientific spellings,
and registers canonical definitions throughout the textbook.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class TerminologyEntry(BaseModel):
    term: str
    preferred_name: str
    aliases: List[str] = Field(default_factory=list)
    definition: str
    first_introduction: str
    chapters_used: List[str] = Field(default_factory=list)
    notation: Optional[str] = None

class BookTerminologyRegistry:
    """
    Registry for textbook terminology, preventing erratic shifts in notation or spelling.
    """

    def __init__(self):
        self.entries: Dict[str, TerminologyEntry] = {}
        # Prepopulate canonical standard scientific terms
        self.register_term(
            term="schrodinger equation",
            preferred_name="Schrödinger equation",
            definition="A linear partial differential equation that governs the wave function of a quantum-mechanical system.",
            section_introduced="Quantum Mechanics Foundations",
            aliases=["schrodinger wave equation", "schrödinger's equation", "schroedinger equation"],
            notation="i\\hbar \\frac{\\partial \\Psi}{\\partial t} = \\hat{H}\\Psi"
        )
        self.register_term(
            term="de broglie wavelength",
            preferred_name="de Broglie wavelength",
            definition="The wavelength associated with a massive particle, inversely proportional to its linear momentum.",
            section_introduced="Wave Nature of Particles",
            aliases=["matter wavelength", "de broglie wave-length"],
            notation="\\lambda = \\frac{h}{p}"
        )
        self.register_term(
            term="planck constant",
            preferred_name="Planck constant",
            definition="A fundamental physical constant that relates the energy of a photon to its frequency.",
            section_introduced="Quantum Mechanics Foundations",
            aliases=["planck's constant"],
            notation="h = 6.626 \\times 10^{-34} \\text{ J}\\cdot\\text{s}"
        )
        self.register_term(
            term="heisenberg uncertainty principle",
            preferred_name="Heisenberg uncertainty principle",
            definition="A fundamental limit in quantum mechanics stating that position and momentum cannot both be precisely determined simultaneously.",
            section_introduced="Heisenberg Uncertainty Principle",
            aliases=["uncertainty principle", "heisenberg's uncertainty principle"],
            notation="\\Delta x \\cdot \\Delta p_x \\ge \\frac{\\hbar}{2}"
        )

    def register_term(
        self,
        term: str,
        preferred_name: str,
        definition: str,
        section_introduced: str,
        aliases: Optional[List[str]] = None,
        notation: Optional[str] = None
    ) -> TerminologyEntry:
        key = term.lower().strip()
        if key not in self.entries:
            entry = TerminologyEntry(
                term=key,
                preferred_name=preferred_name,
                aliases=aliases or [],
                definition=definition,
                first_introduction=section_introduced,
                chapters_used=[section_introduced],
                notation=notation
            )
            self.entries[key] = entry
            return entry
        else:
            entry = self.entries[key]
            if section_introduced not in entry.chapters_used:
                entry.chapters_used.append(section_introduced)
            return entry

    def get_preferred_name(self, text: str) -> Optional[str]:
        text_lower = text.lower().strip()
        if text_lower in self.entries:
            return self.entries[text_lower].preferred_name
        for entry in self.entries.values():
            if text_lower in [a.lower() for a in entry.aliases]:
                return entry.preferred_name
        return None

    def export_glossary(self) -> List[Dict[str, Any]]:
        return [entry.model_dump() for entry in self.entries.values()]

    def register_from_content(self, content: str, section_title: str) -> None:
        """Extracts and registers terms mentioned or defined in the text."""
        content_lower = content.lower()
        for term, entry in self.entries.items():
            if term in content_lower and section_title not in entry.chapters_used:
                entry.chapters_used.append(section_title)

    def get_summary(self) -> Dict[str, Any]:
        return {
            "total_registered_terms": len(self.entries),
            "conflicts": [],
            "terms": [e.preferred_name for e in self.entries.values()]
        }
