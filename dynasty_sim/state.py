"""Central game state — replaces all global variables from the original code."""

from __future__ import annotations

from dataclasses import dataclass, field

from dynasty_sim.constants import POSITIONS, SEASON_WEEKS
from dynasty_sim.models import Player, Team, empty_roster


@dataclass
class GameState:
    """Holds every mutable piece of game data for a running session."""

    # The human player's team
    player_team: Team

    # All 15 CPU teams (does NOT include player_team)
    cpu_teams: list[Team]

    # Free-agent pool, keyed by position
    free_agents: dict[str, list[Player]] = field(
        default_factory=lambda: {pos: [] for pos in POSITIONS}
    )

    # Weekly matchup pairings — list of (team_a, team_b) tuples
    schedule: list[tuple[Team, Team]] = field(default_factory=list)

    # Current week (0 = pre-season, 1–SEASON_WEEKS = in-season)
    week: int = 0

    # Whether the season has started (player has typed ADVANCE at least once)
    season_active: bool = False

    # Player name lists loaded from CSVs
    first_names: list[str] = field(default_factory=list)
    last_names: list[str] = field(default_factory=list)

    # ------------------------------------------------------------------
    # Convenience helpers
    # ------------------------------------------------------------------

    @property
    def all_teams(self) -> list[Team]:
        """All teams including the player's team."""
        return [self.player_team] + self.cpu_teams

    @property
    def season_over(self) -> bool:
        return self.week > SEASON_WEEKS

    def find_opponent(self) -> Team | None:
        """Return the player's opponent for the current week, or None."""
        for team_a, team_b in self.schedule:
            if team_a.coach == self.player_team.coach:
                return team_b
            if team_b.coach == self.player_team.coach:
                return team_a
        return None
