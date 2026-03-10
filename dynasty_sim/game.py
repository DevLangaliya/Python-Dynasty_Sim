"""Game-simulation engine — play-by-play logic and outcome calculation."""

from __future__ import annotations

import random
from dataclasses import dataclass, field

from dynasty_sim.constants import (
    PASS_OUTCOME_KEYS,
    PASS_OUTCOME_WEIGHTS,
    PASS_TACKLE_WEIGHTS,
    PASS_YARDAGE,
    PLAYS_PER_GAME,
    RUN_OUTCOME_KEYS,
    RUN_OUTCOME_WEIGHTS,
    RUN_TACKLE_WEIGHTS,
    RUN_YARDAGE,
)
from dynasty_sim.models import Player, Team


# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------


@dataclass
class PlayResult:
    """Structured result of a single offensive play."""

    description: str
    yards: int
    field_pos: int
    tackler: str = ""
    is_complete: bool = True  # False → incomplete pass


@dataclass
class KickoffResult:
    """Result of a kickoff."""

    description: str
    field_pos: int


@dataclass
class GameResult:
    """Final outcome of a simulated or played-out game."""

    winner: Team
    loser: Team
    play_log: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _collect_defenders(roster: dict[str, list[Player]]) -> list[Player]:
    """Return all defensive players (DL, LB, DB) from a roster."""
    defensive_positions = {"DL", "LB", "DB"}
    defenders: list[Player] = []
    for pos, players in roster.items():
        if pos in defensive_positions:
            defenders.extend(players)
    return defenders


# ---------------------------------------------------------------------------
# Coin toss
# ---------------------------------------------------------------------------


def coin_toss(team_a: Team, team_b: Team) -> tuple[str, Team, Team]:
    """Randomly determine who receives the opening kickoff.

    Returns:
        (announcement, receiving_team, kicking_team)
    """
    if random.randint(0, 1) == 1:
        receiver, kicker = team_b, team_a
    else:
        receiver, kicker = team_a, team_b

    announcement = f"The {receiver.name} wins the coin toss and will receive!"
    return announcement, receiver, kicker


# ---------------------------------------------------------------------------
# Kickoff
# ---------------------------------------------------------------------------


def do_kickoff(kicking_team: Team) -> KickoffResult:
    """Simulate a kickoff.  Returns the yard line the offense starts on."""
    k_list = kicking_team.roster.get("K", [])
    kicker = k_list[0] if k_list else None
    if kicker is None:
        field_pos = 25
        return KickoffResult(
            description="The kicker boots the ball to the 25-yard line.",
            field_pos=field_pos,
        )

    power = kicker.kick_power
    # Higher kick power → ball travels deeper → offense starts further back
    field_pos = int(power)
    if field_pos > 50:
        field_pos = 100 - field_pos

    return KickoffResult(
        description=(
            f"{kicker.full_name} kicks the ball off to the {field_pos}-yard line."
        ),
        field_pos=field_pos,
    )


# ---------------------------------------------------------------------------
# Single play simulation
# ---------------------------------------------------------------------------


def simulate_play(
    offense: Team,
    defense: Team,
    field_pos: int,
    play_type: str,
) -> PlayResult:
    """Simulate one offensive play.

    Args:
        offense: The team on offense.
        defense: The team on defense.
        field_pos: Current yard line (0 = own goal line, 100 = opponent end zone).
        play_type: "RUN" or "PASS".

    Returns:
        A PlayResult describing what happened.
    """
    defenders = _collect_defenders(defense.roster)

    if play_type == "RUN":
        return _simulate_run(offense, defenders, field_pos)
    return _simulate_pass(offense, defense, defenders, field_pos)


def _simulate_run(
    offense: Team,
    defenders: list[Player],
    field_pos: int,
) -> PlayResult:
    """Resolve a run play."""
    outcome_key = random.choices(RUN_OUTCOME_KEYS, weights=RUN_OUTCOME_WEIGHTS, k=1)[0]
    yards = random.choice(RUN_YARDAGE[outcome_key])
    new_pos = min(100, max(0, field_pos + yards))

    rb_list = offense.roster.get("RB", [])
    ball_carrier = rb_list[0] if rb_list else None
    carrier_name = ball_carrier.full_name if ball_carrier else "The running back"

    tackler_name = ""
    if defenders:
        weights = RUN_TACKLE_WEIGHTS[: len(defenders)]
        tackler = random.choices(defenders, weights=weights, k=1)[0]
        tackler_name = tackler.full_name

    if yards < 0:
        desc = (
            f"{carrier_name} is stuffed for a loss of {abs(yards)} yard(s). "
            f"Tackled by {tackler_name}. Ball on the {new_pos}-yard line."
        )
    else:
        desc = (
            f"{carrier_name} carries the ball for {yards} yard(s), "
            f"tackled by {tackler_name}. Ball on the {new_pos}-yard line."
        )

    return PlayResult(
        description=desc,
        yards=yards,
        field_pos=new_pos,
        tackler=tackler_name,
    )


def _simulate_pass(
    offense: Team,
    defense: Team,
    defenders: list[Player],
    field_pos: int,
) -> PlayResult:
    """Resolve a pass play."""
    receivers: list[Player] = []
    for pos in ("WR", "TE"):
        receivers.extend(offense.roster.get(pos, []))

    if not receivers:
        return PlayResult(
            description="The quarterback has no receivers — incomplete pass.",
            yards=0,
            field_pos=field_pos,
            is_complete=False,
        )

    target = random.choice(receivers)

    # Pick a random DB as the coverage defender
    db_list = defense.roster.get("DB", [])
    if db_list:
        defender = random.choice(db_list)
        coverage_advantage = defender.coverage - target.catching
    else:
        coverage_advantage = 0

    # Higher advantage for the defender → lower catch probability
    catch_threshold = max(0, min(80, abs(coverage_advantage)))
    roll = random.randint(0, 100)

    qb_list = offense.roster.get("QB", [])
    qb_name = qb_list[0].full_name if qb_list else "The quarterback"

    if roll > catch_threshold:
        # Completion
        outcome_key = random.choices(
            PASS_OUTCOME_KEYS, weights=PASS_OUTCOME_WEIGHTS, k=1
        )[0]
        yards = random.choice(PASS_YARDAGE[outcome_key])
        new_pos = min(100, max(0, field_pos + yards))

        tackler_name = ""
        if defenders:
            weights = PASS_TACKLE_WEIGHTS[: len(defenders)]
            tackler = random.choices(defenders, weights=weights, k=1)[0]
            tackler_name = tackler.full_name

        desc = (
            f"{qb_name} finds {target.full_name} for {yards} yard(s). "
            f"Tackled by {tackler_name}. Ball on the {new_pos}-yard line."
        )
        return PlayResult(
            description=desc,
            yards=yards,
            field_pos=new_pos,
            tackler=tackler_name,
            is_complete=True,
        )
    else:
        # Incomplete
        defender_name = db_list[0].full_name if db_list else "the defender"
        desc = (
            f"{qb_name} targets {target.full_name}, "
            f"but the pass is broken up by {defender_name}. Incomplete."
        )
        return PlayResult(
            description=desc,
            yards=0,
            field_pos=field_pos,
            is_complete=False,
        )


# ---------------------------------------------------------------------------
# Drive / game loops
# ---------------------------------------------------------------------------


def play_by_play(offense: Team, defense: Team) -> list[str]:
    """Run a full play-by-play game sequence.

    Simulates PLAYS_PER_GAME offensive plays and returns a log of descriptions.
    The offensive team alternates after each possession (simplified — no scores
    or turnovers tracked; this preserves the original game's scope).

    Args:
        offense: The team that receives the opening kickoff.
        defense: The team that kicks off.

    Returns:
        A list of play-description strings (the full game log).
    """
    toss_msg, receiver, kicker = coin_toss(offense, defense)
    kickoff = do_kickoff(kicker)

    log: list[str] = [toss_msg, kickoff.description]
    field_pos = kickoff.field_pos

    current_offense = receiver
    current_defense = kicker

    for play_num in range(1, PLAYS_PER_GAME + 1):
        # Decide run or pass based on the offensive team's tendency
        roll = random.randint(1, 100)
        play_type = "RUN" if roll <= current_offense.run_tendency else "PASS"

        result = simulate_play(current_offense, current_defense, field_pos, play_type)
        log.append(f"Play {play_num}: {result.description}")
        field_pos = result.field_pos

        # Reset if the ball reaches either end zone
        if field_pos >= 100 or field_pos <= 0:
            field_pos = 25
            # Simple possession flip
            current_offense, current_defense = current_defense, current_offense

    return log


def sim_game(team_a: Team, team_b: Team) -> GameResult:
    """Simulate a game without play-by-play output.

    The winner is decided probabilistically based on team overall ratings.

    Args:
        team_a: One of the competing teams.
        team_b: The other competing team.

    Returns:
        A GameResult indicating the winner and loser.
    """
    ovr_a = team_a.overall()
    ovr_b = team_b.overall()
    total = ovr_a + ovr_b if (ovr_a + ovr_b) > 0 else 1

    # Team with higher overall has proportionally better chance of winning
    if random.randint(1, total) <= ovr_a:
        winner, loser = team_a, team_b
    else:
        winner, loser = team_b, team_a

    return GameResult(winner=winner, loser=loser)
