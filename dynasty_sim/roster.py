"""Player generation and roster-management functions."""

from __future__ import annotations

import csv
import copy
import random

from dynasty_sim.constants import (
    BASE_ROSTER_COUNTS,
    COACH_NAMES,
    FIRSTNAMES_CSV,
    FREE_AGENT_COUNTS,
    LASTNAMES_CSV,
    POSITION_CONFIGS,
    POSITIONS,
    TEAM_NAMES,
    BLANK_STATS,
)
from dynasty_sim.models import Player, Team, empty_roster


# ---------------------------------------------------------------------------
# Name loading
# ---------------------------------------------------------------------------


def load_names() -> tuple[list[str], list[str]]:
    """Load first and last name lists from the data CSV files.

    Returns:
        A (first_names, last_names) tuple, both as uppercase string lists.

    Raises:
        FileNotFoundError: If either CSV file is missing.
    """
    first_names: list[str] = []
    last_names: list[str] = []

    with open(FIRSTNAMES_CSV, newline="", encoding="utf-8") as fh:
        reader = csv.reader(fh)
        next(reader)  # skip header row
        for row in reader:
            if len(row) > 1:
                first_names.append(row[1].upper())

    with open(LASTNAMES_CSV, newline="", encoding="utf-8") as fh:
        reader = csv.reader(fh)
        next(reader)  # skip header row
        for row in reader:
            if len(row) > 1:
                last_names.append(row[1].upper())

    return first_names, last_names


# ---------------------------------------------------------------------------
# Player generation
# ---------------------------------------------------------------------------


def generate_player(
    position: str,
    first_names: list[str],
    last_names: list[str],
) -> Player:
    """Generate a random player for the given position.

    Args:
        position: One of the nine valid position codes (QB, RB, …).
        first_names: Pool of first names to draw from.
        last_names: Pool of last names to draw from.

    Returns:
        A freshly constructed Player with randomised attributes.

    Raises:
        KeyError: If *position* is not in POSITION_CONFIGS.
    """
    config = POSITION_CONFIGS[position]
    attrs = {
        attr: random.randint(lo, hi)
        for attr, (lo, hi) in config.stat_ranges.items()
    }
    return Player(
        first_name=random.choice(first_names),
        last_name=random.choice(last_names),
        position=position,
        stats=copy.deepcopy(BLANK_STATS),
        **attrs,
    )


def generate_roster(
    counts: dict[str, int],
    first_names: list[str],
    last_names: list[str],
) -> dict[str, list[Player]]:
    """Generate a complete roster dict given position → count mapping."""
    roster = empty_roster()
    for position, count in counts.items():
        while len(roster[position]) < count:
            roster[position].append(
                generate_player(position, first_names, last_names)
            )
    return roster


# ---------------------------------------------------------------------------
# Team generation
# ---------------------------------------------------------------------------


def generate_cpu_teams(
    first_names: list[str],
    last_names: list[str],
) -> list[Team]:
    """Create all CPU-controlled teams with randomised rosters.

    Returns:
        A list of 15 Team objects.
    """
    available_names = list(TEAM_NAMES)
    available_coaches = list(COACH_NAMES)
    teams: list[Team] = []

    for _ in range(len(available_names)):
        team_name = random.choice(available_names)
        available_names.remove(team_name)

        coach = random.choice(available_coaches)
        available_coaches.remove(coach)

        run_tendency = random.randint(20, 80)
        pass_tendency = 100 - run_tendency

        roster = generate_roster(BASE_ROSTER_COUNTS, first_names, last_names)
        teams.append(
            Team(
                name=team_name,
                coach=coach,
                roster=roster,
                run_tendency=run_tendency,
                pass_tendency=pass_tendency,
            )
        )

    return teams


def generate_free_agents(
    first_names: list[str],
    last_names: list[str],
) -> dict[str, list[Player]]:
    """Build a fresh free-agent pool.

    Returns:
        A dict mapping each position to a list of available players.
    """
    pool: dict[str, list[Player]] = {pos: [] for pos in POSITIONS}
    for position, count in FREE_AGENT_COUNTS.items():
        while len(pool[position]) < count:
            pool[position].append(
                generate_player(position, first_names, last_names)
            )
    return pool


# ---------------------------------------------------------------------------
# Roster management — sign and cut
# ---------------------------------------------------------------------------


class RosterFullError(Exception):
    """Raised when a roster slot is at capacity and no replacement was made."""


def sign_player(
    roster: dict[str, list[Player]],
    free_agents: dict[str, list[Player]],
    position: str,
    agent_index: int,
    replace_index: int | None = None,
) -> Player:
    """Sign a free agent to the given roster.

    Args:
        roster: The team roster dict to modify in place.
        free_agents: The free-agent pool dict to pull from.
        position: Position code (e.g. "WR").
        agent_index: 1-based index into free_agents[position].
        replace_index: 1-based index of the roster player to cut first.
            Required when the position is at capacity.

    Returns:
        The Player who was signed.

    Raises:
        IndexError: If agent_index or replace_index are out of range.
        RosterFullError: If at capacity and replace_index was not provided.
        KeyError: If position is invalid.
    """
    config = POSITION_CONFIGS[position]
    slot = roster[position]
    agents = free_agents[position]

    zero_based = agent_index - 1
    if not (0 <= zero_based < len(agents)):
        raise IndexError(
            f"Agent #{agent_index} does not exist for position {position}."
        )

    if len(slot) >= config.max_roster:
        if replace_index is None:
            raise RosterFullError(
                f"{position} roster is full (max {config.max_roster})."
            )
        cut_index = replace_index - 1
        if not (0 <= cut_index < len(slot)):
            raise IndexError(
                f"Roster spot #{replace_index} does not exist for {position}."
            )
        slot.pop(cut_index)

    signed = agents.pop(zero_based)
    slot.append(signed)
    return signed


def cut_player(
    roster: dict[str, list[Player]],
    position: str,
    player_index: int,
) -> Player:
    """Release a player from the roster.

    Args:
        roster: The team roster dict to modify in place.
        position: Position code.
        player_index: 1-based index of the player to cut.

    Returns:
        The cut Player.

    Raises:
        IndexError: If player_index is out of range.
        KeyError: If position is invalid.
    """
    slot = roster[position]
    zero_based = player_index - 1
    if not (0 <= zero_based < len(slot)):
        raise IndexError(
            f"Roster spot #{player_index} does not exist for {position}."
        )
    return slot.pop(zero_based)
