"""Core data models for the dynasty simulator."""

from __future__ import annotations

import copy
from dataclasses import dataclass, field

from dynasty_sim.constants import BLANK_STATS, POSITION_CONFIGS, POSITIONS


@dataclass
class Player:
    """Represents a single player on a roster or in the free-agent pool."""

    first_name: str
    last_name: str
    position: str
    speed: int
    strength: int
    catching: int
    throw_power: int
    throw_accuracy: int
    tackle: int
    coverage: int
    kick_power: int
    kick_accuracy: int
    contract: int
    stats: dict[str, int] = field(default_factory=lambda: copy.deepcopy(BLANK_STATS))

    # ------------------------------------------------------------------
    # Computed properties
    # ------------------------------------------------------------------

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def overall(self) -> int:
        """Return an overall rating based on the position's key attributes."""
        config = POSITION_CONFIGS.get(self.position)
        if config is None or not config.overall_attrs:
            return 0
        values = [getattr(self, attr) for attr in config.overall_attrs]
        return int(sum(values) / len(values))


def empty_roster() -> dict[str, list[Player]]:
    """Return a fresh roster dict with an empty list for every position."""
    return {pos: [] for pos in POSITIONS}


@dataclass
class Team:
    """Represents a franchise — holds the roster, record, and coaching info."""

    name: str
    coach: str
    roster: dict[str, list[Player]] = field(default_factory=empty_roster)
    wins: int = 0
    losses: int = 0
    run_tendency: int = 50
    pass_tendency: int = 50

    # ------------------------------------------------------------------
    # Computed properties
    # ------------------------------------------------------------------

    @property
    def record(self) -> str:
        return f"{self.wins}-{self.losses}"

    @property
    def win_pct(self) -> float:
        total = self.wins + self.losses
        return round(self.wins / total, 3) if total > 0 else 0.0

    def overall(self) -> int:
        """Average overall rating across all rostered players."""
        players = [p for group in self.roster.values() for p in group]
        if not players:
            return 0
        return int(sum(p.overall() for p in players) / len(players))
