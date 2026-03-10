"""Terminal display functions — pure output, no side effects."""

from __future__ import annotations

from dynasty_sim.models import Player, Team


# ---------------------------------------------------------------------------
# Depth chart / roster
# ---------------------------------------------------------------------------


def show_depth_chart(team: Team) -> None:
    """Print a formatted depth chart for a single team."""
    print(
        f"\n{'=' * 60}\n"
        f"  {team.name.upper()}  |  Coach: {team.coach}\n"
        f"  Record: {team.record}  |  "
        f"Run/Pass: {team.run_tendency}/{team.pass_tendency}  |  "
        f"OVR: {team.overall()}\n"
        f"{'=' * 60}"
    )
    for position, players in team.roster.items():
        if not players:
            print(f"\n  {position}: (empty)")
            continue
        print(f"\n  {position}:")
        for idx, player in enumerate(players, start=1):
            print(
                f"    #{idx}  {player.full_name:<24}  "
                f"OVR: {player.overall():>3}  |  "
                f"Contract: {player.contract} yr(s)"
            )
    print()


# ---------------------------------------------------------------------------
# Free agents
# ---------------------------------------------------------------------------


def show_free_agents(free_agents: dict[str, list[Player]]) -> None:
    """Print the entire free-agent pool grouped by position."""
    print(f"\n{'=' * 60}")
    print("  FREE AGENTS")
    print(f"{'=' * 60}")
    for position, players in free_agents.items():
        if not players:
            continue
        print(f"\n  {position}:")
        for idx, player in enumerate(players, start=1):
            print(
                f"    #{idx}  {player.full_name:<24}  "
                f"OVR: {player.overall():>3}  |  "
                f"Contract: {player.contract} yr(s)"
            )
    print()


# ---------------------------------------------------------------------------
# Stats
# ---------------------------------------------------------------------------


def show_player_stats(player: Player) -> None:
    """Print a single player's season statistics."""
    print(f"\n  {player.full_name} ({player.position})")
    print(f"  {'─' * 40}")
    for stat, value in player.stats.items():
        if value != 0:
            print(f"    {stat:<30} {value}")
    print()


def show_team_stats(team: Team) -> None:
    """Print season statistics for every player on a team."""
    print(f"\n{'=' * 60}")
    print(f"  STATS — {team.name.upper()}")
    print(f"{'=' * 60}")
    for players in team.roster.values():
        for player in players:
            show_player_stats(player)


# ---------------------------------------------------------------------------
# Schedule / standings
# ---------------------------------------------------------------------------


def show_schedule(matchups: list[tuple[Team, Team]], week: int) -> None:
    """Print the matchup list for the given week."""
    print(f"\n{'=' * 60}")
    print(f"  WEEK {week} SCHEDULE")
    print(f"{'=' * 60}")
    for idx, (home, away) in enumerate(matchups, start=1):
        print(f"  Game {idx}: {home.name} vs. {away.name}")
    print()


def show_standings(all_teams: list[Team]) -> None:
    """Print win/loss standings for all teams, sorted by win percentage."""
    print(f"\n{'=' * 60}")
    print("  STANDINGS")
    print(f"{'=' * 60}")
    sorted_teams = sorted(all_teams, key=lambda t: t.win_pct, reverse=True)
    print(f"  {'Team':<20} {'W':>4} {'L':>4} {'PCT':>6}")
    print(f"  {'─' * 40}")
    for team in sorted_teams:
        print(
            f"  {team.name:<20} {team.wins:>4} {team.losses:>4} "
            f"{team.win_pct:>6.3f}"
        )
    print()


# ---------------------------------------------------------------------------
# Help
# ---------------------------------------------------------------------------


def show_help() -> None:
    """Print the list of available commands."""
    commands = [
        ("ROSTER",       "View your current depth chart"),
        ("FREE AGENTS",  "View and sign available free agents"),
        ("SIGN",         "Sign a free agent (prompts for details)"),
        ("CUT",          "Release a player from your roster"),
        ("TEAMS",        "View all teams' depth charts"),
        ("SCHEDULE",     "View this week's matchups"),
        ("STANDINGS",    "View win/loss standings"),
        ("STATS",        "View your players' season statistics"),
        ("GAME",         "Play or simulate this week's game"),
        ("ADVANCE",      "Advance to the next week"),
        ("HELP",         "Show this help text"),
        ("QUIT",         "Exit the simulator"),
    ]
    print(f"\n{'=' * 60}")
    print("  COMMANDS")
    print(f"{'=' * 60}")
    for cmd, desc in commands:
        print(f"  {cmd:<16} {desc}")
    print()
