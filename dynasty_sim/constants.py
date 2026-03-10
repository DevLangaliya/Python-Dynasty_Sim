"""Named constants and position configuration for the dynasty simulator."""

from dataclasses import dataclass, field
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

DATA_DIR = Path(__file__).parent.parent / "data"
FIRSTNAMES_CSV = DATA_DIR / "firstnames.csv"
LASTNAMES_CSV = DATA_DIR / "lastnames.csv"

# ---------------------------------------------------------------------------
# Position configuration
# ---------------------------------------------------------------------------

POSITIONS: list[str] = ["QB", "RB", "WR", "TE", "OL", "DL", "LB", "DB", "K"]


@dataclass(frozen=True)
class PositionConfig:
    """Roster limits and stat generation ranges for a single position."""

    max_roster: int
    # Maps attribute name → (min, max) for random generation
    stat_ranges: dict[str, tuple[int, int]] = field(default_factory=dict)
    # Attributes used to compute overall rating (in order)
    overall_attrs: tuple[str, ...] = field(default_factory=tuple)


POSITION_CONFIGS: dict[str, PositionConfig] = {
    "QB": PositionConfig(
        max_roster=1,
        stat_ranges={
            "speed": (70, 85),
            "strength": (60, 80),
            "catching": (35, 55),
            "throw_power": (75, 90),
            "throw_accuracy": (75, 90),
            "tackle": (25, 45),
            "coverage": (15, 25),
            "kick_power": (40, 50),
            "kick_accuracy": (15, 30),
            "contract": (2, 5),
        },
        overall_attrs=("throw_power", "throw_accuracy", "speed"),
    ),
    "RB": PositionConfig(
        max_roster=1,
        stat_ranges={
            "speed": (85, 95),
            "strength": (55, 85),
            "catching": (65, 80),
            "throw_power": (25, 35),
            "throw_accuracy": (15, 25),
            "tackle": (45, 65),
            "coverage": (15, 25),
            "kick_power": (25, 45),
            "kick_accuracy": (15, 35),
            "contract": (2, 5),
        },
        overall_attrs=("speed", "catching", "strength"),
    ),
    "WR": PositionConfig(
        max_roster=3,
        stat_ranges={
            "speed": (85, 99),
            "strength": (65, 75),
            "catching": (75, 90),
            "throw_power": (25, 35),
            "throw_accuracy": (15, 25),
            "tackle": (45, 65),
            "coverage": (15, 25),
            "kick_power": (25, 45),
            "kick_accuracy": (15, 35),
            "contract": (2, 5),
        },
        overall_attrs=("speed", "catching", "strength"),
    ),
    "TE": PositionConfig(
        max_roster=1,
        stat_ranges={
            "speed": (75, 90),
            "strength": (75, 90),
            "catching": (70, 90),
            "throw_power": (25, 35),
            "throw_accuracy": (15, 25),
            "tackle": (45, 65),
            "coverage": (15, 25),
            "kick_power": (25, 45),
            "kick_accuracy": (15, 35),
            "contract": (2, 5),
        },
        overall_attrs=("speed", "catching", "strength"),
    ),
    "OL": PositionConfig(
        max_roster=5,
        stat_ranges={
            "speed": (55, 65),
            "strength": (70, 95),
            "catching": (35, 55),
            "throw_power": (35, 45),
            "throw_accuracy": (35, 45),
            "tackle": (55, 65),
            "coverage": (15, 25),
            "kick_power": (40, 50),
            "kick_accuracy": (15, 30),
            "contract": (2, 5),
        },
        overall_attrs=("strength",),
    ),
    "DL": PositionConfig(
        max_roster=4,
        stat_ranges={
            "speed": (65, 85),
            "strength": (85, 95),
            "catching": (35, 55),
            "throw_power": (35, 45),
            "throw_accuracy": (35, 45),
            "tackle": (75, 95),
            "coverage": (15, 25),
            "kick_power": (40, 50),
            "kick_accuracy": (15, 30),
            "contract": (2, 5),
        },
        overall_attrs=("tackle", "strength", "speed"),
    ),
    "LB": PositionConfig(
        max_roster=3,
        stat_ranges={
            "speed": (75, 95),
            "strength": (75, 95),
            "catching": (35, 55),
            "throw_power": (35, 45),
            "throw_accuracy": (35, 45),
            "tackle": (75, 85),
            "coverage": (65, 85),
            "kick_power": (40, 50),
            "kick_accuracy": (15, 30),
            "contract": (2, 5),
        },
        overall_attrs=("tackle", "strength", "coverage"),
    ),
    "DB": PositionConfig(
        max_roster=4,
        stat_ranges={
            "speed": (75, 99),
            "strength": (55, 80),
            "catching": (65, 85),
            "throw_power": (35, 45),
            "throw_accuracy": (35, 45),
            "tackle": (75, 90),
            "coverage": (75, 95),
            "kick_power": (40, 50),
            "kick_accuracy": (15, 30),
            "contract": (2, 5),
        },
        overall_attrs=("coverage", "tackle", "speed"),
    ),
    "K": PositionConfig(
        max_roster=1,
        stat_ranges={
            "speed": (70, 85),
            "strength": (60, 70),
            "catching": (45, 55),
            "throw_power": (45, 55),
            "throw_accuracy": (55, 65),
            "tackle": (25, 45),
            "coverage": (15, 25),
            "kick_power": (75, 90),
            "kick_accuracy": (75, 90),
            "contract": (2, 5),
        },
        overall_attrs=("kick_accuracy", "kick_power"),
    ),
}

# ---------------------------------------------------------------------------
# Roster counts used when generating base teams and free-agent pools
# ---------------------------------------------------------------------------

BASE_ROSTER_COUNTS: dict[str, int] = {
    "QB": 1,
    "RB": 1,
    "WR": 3,
    "TE": 1,
    "OL": 5,
    "DL": 4,
    "LB": 3,
    "DB": 4,
    "K": 1,
}

FREE_AGENT_COUNTS: dict[str, int] = {
    "QB": 4,
    "RB": 4,
    "WR": 12,
    "TE": 4,
    "OL": 20,
    "DL": 16,
    "LB": 12,
    "DB": 16,
    "K": 4,
}

# ---------------------------------------------------------------------------
# Play outcome weights and yardage ranges
# ---------------------------------------------------------------------------

# Weights correspond to LOSS / SHORT / MID / LONG
RUN_OUTCOME_WEIGHTS: list[int] = [3, 76, 18, 3]
PASS_OUTCOME_WEIGHTS: list[int] = [2, 33, 45, 20]

RUN_YARDAGE: dict[str, list[int]] = {
    "LOSS": [-5, -4, -3, -2, -1],
    "SHORT": list(range(0, 11)),
    "MID": list(range(11, 21)),
    "LONG": list(range(21, 100)),
}

PASS_YARDAGE: dict[str, list[int]] = {
    "LOSS": [-5, -4, -3, -2, -1],
    "SHORT": list(range(0, 11)),
    "MID": list(range(11, 21)),
    "LONG": list(range(21, 100)),
}

RUN_OUTCOME_KEYS: list[str] = list(RUN_YARDAGE.keys())
PASS_OUTCOME_KEYS: list[str] = list(PASS_YARDAGE.keys())

# Defensive tackler weights: DL(4) LB(3) DB(4) — ordered DL first, DB last
# Used when choosing who makes the tackle on a run play
RUN_TACKLE_WEIGHTS: list[int] = [15, 15, 15, 15, 8, 8, 8, 4, 4, 4, 4]
# Pass tackles weight DBs and LBs higher
PASS_TACKLE_WEIGHTS: list[int] = [4, 4, 4, 4, 8, 8, 8, 15, 15, 15, 15]

# Total offensive plays simulated per game drive sequence
PLAYS_PER_GAME: int = 50

# Number of weeks in a season / matchup slots
SEASON_WEEKS: int = 8

# ---------------------------------------------------------------------------
# Blank stat template for new players
# ---------------------------------------------------------------------------

BLANK_STATS: dict[str, int] = {
    "Passing Attempts": 0,
    "Completions": 0,
    "Passing Yards": 0,
    "Touchdown Passes": 0,
    "Pass Interceptions": 0,
    "Rushing Attempts": 0,
    "Rushing Yards": 0,
    "Rushing Touchdowns": 0,
    "Receptions": 0,
    "Receiving Yards": 0,
    "Receiving Touchdowns": 0,
    "Tackles": 0,
    "Sacks": 0,
    "Interceptions": 0,
    "Field Goals Made": 0,
    "Field Goals Attempted": 0,
    "Field Goal Accuracy": 0,
    "Longest Field Goal": 0,
}

# ---------------------------------------------------------------------------
# Flavor data
# ---------------------------------------------------------------------------

COACH_NAMES: list[str] = [
    "Mike Ditka",
    "Lovie Smith",
    "John Madden",
    "Deion Sanders",
    "Adam Gase",
    "Sean McVay",
    "Bruce Arians",
    "Mike McCarthy",
    "Bill Belichick",
    "Andy Reid",
    "Kyle Shanahan",
    "Pete Carroll",
    "Mike Tomlin",
    "Dan Campbell",
    "Kevin O'Connell",
]

TEAM_NAMES: list[str] = [
    "Broncos",
    "Rams",
    "Browns",
    "Bears",
    "Dolphins",
    "Seahawks",
    "Commanders",
    "Packers",
    "Cardinals",
    "Patriots",
    "Buccaneers",
    "Lions",
    "Falcons",
    "Saints",
    "Panthers",
]
