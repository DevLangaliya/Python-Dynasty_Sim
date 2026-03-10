"""Schedule generation for a dynasty season."""

from __future__ import annotations

import copy
import random

from dynasty_sim.models import Team


def generate_schedule(all_teams: list[Team]) -> list[tuple[Team, Team]]:
    """Pair all teams into matchups for the current week.

    Each call generates a fresh random pairing of all teams.  The returned
    list has len(all_teams) // 2 matchups; any bye team (odd count) is
    omitted.

    Args:
        all_teams: Every team participating in this week's slate.

    Returns:
        A list of (home, away) team pairs.
    """
    pool = list(all_teams)
    random.shuffle(pool)

    matchups: list[tuple[Team, Team]] = []
    while len(pool) >= 2:
        team_a = pool.pop()
        team_b = pool.pop()
        matchups.append((team_a, team_b))

    return matchups
