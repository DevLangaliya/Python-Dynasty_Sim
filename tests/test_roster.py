"""Tests for dynasty_sim.roster."""

import pytest

from dynasty_sim.constants import BLANK_STATS, POSITION_CONFIGS, POSITIONS
from dynasty_sim.models import Player, empty_roster
from dynasty_sim.roster import (
    RosterFullError,
    cut_player,
    generate_player,
    generate_roster,
    load_names,
    sign_player,
)
import copy


@pytest.fixture(scope="module")
def names():
    return load_names()


class TestLoadNames:
    def test_returns_non_empty_lists(self, names):
        first, last = names
        assert len(first) > 0
        assert len(last) > 0

    def test_names_are_strings(self, names):
        first, last = names
        assert all(isinstance(n, str) for n in first[:10])
        assert all(isinstance(n, str) for n in last[:10])


class TestGeneratePlayer:
    def test_returns_player_instance(self, names):
        first, last = names
        p = generate_player("QB", first, last)
        assert isinstance(p, Player)

    def test_position_is_set_correctly(self, names):
        first, last = names
        for pos in POSITIONS:
            p = generate_player(pos, first, last)
            assert p.position == pos

    def test_stats_within_config_ranges(self, names):
        first, last = names
        for pos in POSITIONS:
            config = POSITION_CONFIGS[pos]
            p = generate_player(pos, first, last)
            for attr, (lo, hi) in config.stat_ranges.items():
                value = getattr(p, attr)
                assert lo <= value <= hi, (
                    f"{pos}.{attr} = {value} outside [{lo}, {hi}]"
                )

    def test_stats_dict_has_correct_keys(self, names):
        first, last = names
        p = generate_player("QB", first, last)
        assert set(p.stats.keys()) == set(BLANK_STATS.keys())

    def test_invalid_position_raises(self, names):
        first, last = names
        with pytest.raises(KeyError):
            generate_player("PUNTER", first, last)


class TestGenerateRoster:
    def test_correct_counts(self, names):
        first, last = names
        counts = {"QB": 1, "WR": 3}
        roster = generate_roster(counts, first, last)
        assert len(roster["QB"]) == 1
        assert len(roster["WR"]) == 3

    def test_all_positions_present(self, names):
        first, last = names
        roster = generate_roster({}, first, last)
        for pos in POSITIONS:
            assert pos in roster


class TestSignPlayer:
    def _make_agent(self, position="WR") -> Player:
        return Player(
            first_name="Free",
            last_name="Agent",
            position=position,
            speed=90,
            strength=70,
            catching=85,
            throw_power=25,
            throw_accuracy=20,
            tackle=50,
            coverage=20,
            kick_power=30,
            kick_accuracy=20,
            contract=2,
            stats=copy.deepcopy(BLANK_STATS),
        )

    def test_sign_player_adds_to_roster(self):
        roster = empty_roster()
        free_agents = {pos: [] for pos in POSITIONS}
        agent = self._make_agent("WR")
        free_agents["WR"].append(agent)

        signed = sign_player(roster, free_agents, "WR", 1)
        assert signed is agent
        assert agent in roster["WR"]
        assert agent not in free_agents["WR"]

    def test_sign_raises_on_invalid_index(self):
        roster = empty_roster()
        free_agents = {pos: [] for pos in POSITIONS}
        with pytest.raises(IndexError):
            sign_player(roster, free_agents, "QB", 1)

    def test_sign_raises_roster_full_without_replace(self):
        roster = empty_roster()
        free_agents = {pos: [] for pos in POSITIONS}
        # QB max_roster == 1 — fill it first
        existing = self._make_agent("QB")
        roster["QB"].append(existing)
        # Now add a free agent
        new_agent = self._make_agent("QB")
        free_agents["QB"].append(new_agent)
        with pytest.raises(RosterFullError):
            sign_player(roster, free_agents, "QB", 1)

    def test_sign_with_replace_swaps_player(self):
        roster = empty_roster()
        free_agents = {pos: [] for pos in POSITIONS}
        existing = self._make_agent("QB")
        existing.first_name = "Old"
        roster["QB"].append(existing)
        new_agent = self._make_agent("QB")
        new_agent.first_name = "New"
        free_agents["QB"].append(new_agent)

        signed = sign_player(roster, free_agents, "QB", 1, replace_index=1)
        assert signed is new_agent
        assert existing not in roster["QB"]


class TestCutPlayer:
    def _make_player(self, position="RB") -> Player:
        return Player(
            first_name="Cut",
            last_name="Me",
            position=position,
            speed=88,
            strength=70,
            catching=70,
            throw_power=25,
            throw_accuracy=20,
            tackle=50,
            coverage=20,
            kick_power=30,
            kick_accuracy=20,
            contract=1,
            stats=copy.deepcopy(BLANK_STATS),
        )

    def test_cut_removes_player(self):
        roster = empty_roster()
        p = self._make_player()
        roster["RB"].append(p)
        released = cut_player(roster, "RB", 1)
        assert released is p
        assert p not in roster["RB"]

    def test_cut_invalid_index_raises(self):
        roster = empty_roster()
        with pytest.raises(IndexError):
            cut_player(roster, "RB", 1)
