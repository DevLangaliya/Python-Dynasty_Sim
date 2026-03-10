# NFL Dynasty Simulator

An NFL dynasty simulator written in Python. Manage your team's roster, sign and cut players, and compete through a full season of play-by-play football.

## Installation

```bash
pip install -e .
```

Or run directly:

```bash
python -m dynasty_sim.cli
```

## Gameplay Commands

| Command       | Description                                      |
|---------------|--------------------------------------------------|
| `ROSTER`      | View your current depth chart                    |
| `FREE AGENTS` | Browse and sign available free agents            |
| `SIGN`        | Sign a free agent (prompts for position/player)  |
| `CUT`         | Release a player from your roster                |
| `TEAMS`       | View all 15 teams and their depth charts         |
| `SCHEDULE`    | View the current week's matchups                 |
| `STANDINGS`   | View win/loss standings for all teams            |
| `STATS`       | View your players' season statistics             |
| `GAME`        | Play or simulate the current week's game         |
| `ADVANCE`     | Advance to the next week                         |
| `HELP`        | Show all available commands                      |
| `QUIT`        | Exit the simulator                               |

## Rules

- Each position has a roster limit: QB×1, RB×1, WR×3, TE×1, OL×5, DL×4, LB×3, DB×4, K×1
- Signing a player when at the position limit prompts you to replace an existing player
- Use `ADVANCE` to progress through the 8-week season
- A game can be played live (play-by-play) or simulated

## Running Tests

```bash
python -m pytest tests/ -v
```
