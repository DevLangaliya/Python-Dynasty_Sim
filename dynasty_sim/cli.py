"""Command-line interface — main game loop and user interaction."""

from __future__ import annotations

import random
import sys

from dynasty_sim.constants import BASE_ROSTER_COUNTS, SEASON_WEEKS
from dynasty_sim.display import (
    show_depth_chart,
    show_free_agents,
    show_help,
    show_schedule,
    show_standings,
    show_team_stats,
)
from dynasty_sim.game import GameResult, play_by_play, sim_game
from dynasty_sim.models import Team, empty_roster
from dynasty_sim.roster import (
    RosterFullError,
    cut_player,
    generate_cpu_teams,
    generate_free_agents,
    generate_roster,
    load_names,
    sign_player,
)
from dynasty_sim.schedule import generate_schedule
from dynasty_sim.state import GameState


# ---------------------------------------------------------------------------
# Input helpers
# ---------------------------------------------------------------------------


def prompt_int(message: str, min_val: int, max_val: int) -> int:
    """Prompt until the user enters a valid integer within [min_val, max_val]."""
    while True:
        raw = input(message).strip()
        try:
            value = int(raw)
        except ValueError:
            print(f"  Please enter a number between {min_val} and {max_val}.")
            continue
        if min_val <= value <= max_val:
            return value
        print(f"  Please enter a number between {min_val} and {max_val}.")


def prompt_yes_no(message: str) -> bool:
    """Prompt until the user enters Y or N.  Returns True for yes."""
    while True:
        raw = input(message + " (y/n): ").strip().upper()
        if raw == "Y":
            return True
        if raw == "N":
            return False
        print("  Please enter Y or N.")


def prompt_position(message: str) -> str:
    """Prompt until the user enters a valid position code."""
    from dynasty_sim.constants import POSITIONS

    valid = {p.upper() for p in POSITIONS}
    while True:
        raw = input(message).strip().upper()
        if raw in valid:
            return raw
        print(f"  Valid positions: {', '.join(sorted(valid))}")


# ---------------------------------------------------------------------------
# Command handlers
# ---------------------------------------------------------------------------


def cmd_roster(state: GameState) -> None:
    show_depth_chart(state.player_team)


def cmd_free_agents(state: GameState) -> None:
    if not state.free_agents or all(
        len(v) == 0 for v in state.free_agents.values()
    ):
        state.free_agents = generate_free_agents(
            state.first_names, state.last_names
        )
    show_free_agents(state.free_agents)


def cmd_sign(state: GameState) -> None:
    """Walk the player through signing a free agent."""
    if all(len(v) == 0 for v in state.free_agents.values()):
        state.free_agents = generate_free_agents(
            state.first_names, state.last_names
        )
    show_free_agents(state.free_agents)

    position = prompt_position("Which position are you signing? ")
    agents = state.free_agents.get(position, [])
    if not agents:
        print(f"  No free agents available at {position}.")
        return

    agent_num = prompt_int(
        f"  Pick a player (1–{len(agents)}): ", 1, len(agents)
    )

    roster = state.player_team.roster
    from dynasty_sim.constants import POSITION_CONFIGS

    config = POSITION_CONFIGS[position]
    replace_index: int | None = None

    if len(roster[position]) >= config.max_roster:
        print(
            f"  Your {position} roster is full (max {config.max_roster}). "
            "You must release a player first."
        )
        show_depth_chart(state.player_team)
        if not prompt_yes_no("  Replace an existing player?"):
            print("  Signing cancelled.")
            return
        replace_index = prompt_int(
            f"  Which roster spot to replace (1–{len(roster[position])})?  ",
            1,
            len(roster[position]),
        )

    try:
        signed = sign_player(
            roster,
            state.free_agents,
            position,
            agent_num,
            replace_index,
        )
        print(f"\n  Signed: {signed.full_name} ({position})")
        show_depth_chart(state.player_team)
    except (IndexError, RosterFullError) as exc:
        print(f"  Error: {exc}")


def cmd_cut(state: GameState) -> None:
    """Walk the player through cutting a roster member."""
    show_depth_chart(state.player_team)
    position = prompt_position("Which position do you want to cut from? ")

    roster = state.player_team.roster
    players = roster.get(position, [])
    if not players:
        print(f"  No players at {position} to cut.")
        return

    player_num = prompt_int(
        f"  Which player to cut (1–{len(players)})? ", 1, len(players)
    )

    player_name = players[player_num - 1].full_name
    if not prompt_yes_no(
        f"  Cut {player_name}? This cannot be undone."
    ):
        print("  Cut cancelled.")
        return

    try:
        released = cut_player(roster, position, player_num)
        print(f"\n  Released: {released.full_name}")
        show_depth_chart(state.player_team)
    except IndexError as exc:
        print(f"  Error: {exc}")


def cmd_teams(state: GameState) -> None:
    for team in state.all_teams:
        show_depth_chart(team)


def cmd_schedule(state: GameState) -> None:
    if not state.schedule:
        print("  Schedule not yet generated. Type ADVANCE to start Week 1.")
        return
    show_schedule(state.schedule, state.week)


def cmd_standings(state: GameState) -> None:
    show_standings(state.all_teams)


def cmd_stats(state: GameState) -> None:
    show_team_stats(state.player_team)


def cmd_game(state: GameState) -> None:
    """Play or simulate the current week's game."""
    if not state.season_active:
        print("  The season hasn't started yet. Type ADVANCE to begin Week 1.")
        return

    opponent = state.find_opponent()
    if opponent is None:
        print("  Could not find your matchup for this week.")
        return

    print(f"\n  This week: {state.player_team.name} vs. {opponent.name}")
    if not prompt_yes_no("  Ready to play?"):
        print("  Come back when you're ready!")
        return

    mode = ""
    while mode not in ("P", "S"):
        mode = input("  Play live (P) or simulate (S)? ").strip().upper()

    if mode == "P":
        _run_play_by_play(state, opponent)
    else:
        _run_sim_game(state, opponent)


def _run_play_by_play(state: GameState, opponent: Team) -> None:
    log = play_by_play(state.player_team, opponent)
    print()
    for line in log:
        print(f"  {line}")
    _record_result(state, opponent)


def _run_sim_game(state: GameState, opponent: Team) -> None:
    result = sim_game(state.player_team, opponent)
    print(f"\n  Final: {result.winner.name} defeats {result.loser.name}!")
    _record_result(state, opponent)


def _record_result(state: GameState, opponent: Team) -> None:
    """Apply a coin-flip win/loss to both teams after a game."""
    # In play-by-play mode the original game had no score tracking,
    # so we determine the outcome probabilistically — same as sim_game.
    result = sim_game(state.player_team, opponent)
    if result.winner is state.player_team:
        state.player_team.wins += 1
        opponent.losses += 1
        print(f"\n  Result: {state.player_team.name} WIN! ({state.player_team.record})")
    else:
        state.player_team.losses += 1
        opponent.wins += 1
        print(f"\n  Result: {state.player_team.name} LOSS. ({state.player_team.record})")


def cmd_advance(state: GameState) -> None:
    if state.season_over:
        print("  The season is already over. Final standings:")
        show_standings(state.all_teams)
        return
    state.week += 1
    state.season_active = True
    state.schedule = generate_schedule(state.all_teams)
    print(f"\n  Advancing to Week {state.week}!")
    show_schedule(state.schedule, state.week)


def cmd_help(_state: GameState) -> None:
    show_help()


def cmd_quit(_state: GameState) -> str:
    print("\n  Thanks for playing Dynasty Sim. See you next season!\n")
    return "QUIT"


# ---------------------------------------------------------------------------
# Command dispatch table
# ---------------------------------------------------------------------------

COMMANDS: dict[str, object] = {
    "ROSTER":       cmd_roster,
    "FREE AGENTS":  cmd_free_agents,
    "SIGN":         cmd_sign,
    "CUT":          cmd_cut,
    "TEAMS":        cmd_teams,
    "SCHEDULE":     cmd_schedule,
    "STANDINGS":    cmd_standings,
    "STATS":        cmd_stats,
    "GAME":         cmd_game,
    "ADVANCE":      cmd_advance,
    "HELP":         cmd_help,
    "QUIT":         cmd_quit,
}


# ---------------------------------------------------------------------------
# Main game loop
# ---------------------------------------------------------------------------


def run(state: GameState) -> None:
    """Main REPL loop.  Runs until the player types QUIT."""
    show_help()
    while True:
        try:
            raw = input(f"\n[Week {state.week}] {state.player_team.coach}> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        command = raw.upper()
        handler = COMMANDS.get(command)
        if handler is None:
            print(f"  Unknown command '{raw}'. Type HELP for the full list.")
            continue

        result = handler(state)  # type: ignore[operator]
        if result == "QUIT":
            break


# ---------------------------------------------------------------------------
# Initialisation
# ---------------------------------------------------------------------------


def _build_initial_state(coach_name: str) -> GameState:
    """Construct a fresh GameState for a new game."""
    try:
        first_names, last_names = load_names()
    except FileNotFoundError as exc:
        print(f"Error loading name data: {exc}")
        sys.exit(1)

    run_tendency = random.randint(20, 80)
    pass_tendency = 100 - run_tendency
    player_roster = generate_roster(BASE_ROSTER_COUNTS, first_names, last_names)

    player_team = Team(
        name="Ballers",
        coach=coach_name,
        roster=player_roster,
        run_tendency=run_tendency,
        pass_tendency=pass_tendency,
    )

    cpu_teams = generate_cpu_teams(first_names, last_names)
    free_agents = generate_free_agents(first_names, last_names)

    state = GameState(
        player_team=player_team,
        cpu_teams=cpu_teams,
        free_agents=free_agents,
        first_names=first_names,
        last_names=last_names,
    )

    # Generate week 0 schedule so SCHEDULE command works before first ADVANCE
    state.schedule = generate_schedule(state.all_teams)

    return state


def main() -> None:
    """Entry point for the dynasty simulator."""
    print(
        "\n╔══════════════════════════════════════════╗\n"
        "║       NFL DYNASTY SIMULATOR v1.0         ║\n"
        "╚══════════════════════════════════════════╝\n"
    )
    print("  Welcome! Build your franchise and lead your team to glory.")
    print("  (Type HELP at any time to see available commands.)\n")

    coach_name = input("  Enter your coach's name: ").strip()
    if not coach_name:
        coach_name = "Coach"

    state = _build_initial_state(coach_name)

    print(f"\n  Welcome, {coach_name}! Your team is the {state.player_team.name}.")
    print(f"  Run tendency: {state.player_team.run_tendency}  |  "
          f"Pass tendency: {state.player_team.pass_tendency}")
    print(f"  Team OVR: {state.player_team.overall()}\n")
    print(f"  The season is {SEASON_WEEKS} weeks long. Type ADVANCE to begin Week 1.")

    run(state)


if __name__ == "__main__":
    main()
