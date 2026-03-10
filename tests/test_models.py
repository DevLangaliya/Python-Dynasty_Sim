"""Tests for dynasty_sim.models."""

import pytest

from dynasty_sim.models import Player, Team, empty_roster
from dynasty_sim.constants import BLANK_STATS
import copy


def _make_player(**kwargs) -> Player:
    defaults = dict(
        first_name="John",
        last_name="Doe",
        position="QB",
        speed=75,
        strength=70,
        catching=40,
        throw_power=85,
        throw_accuracy=85,
        tackle=30,
        coverage=20,
        kick_power=45,
        kick_accuracy=20,
        contract=3,
        stats=copy.deepcopy(BLANK_STATS),
    )
    defaults.update(kwargs)
    return Player(**defaults)


class TestPlayer:
    def test_full_name(self):
        p = _make_player(first_name="Tom", last_name="Brady")
        assert p.full_name == "Tom Brady"

    def test_overall_qb_averages_key_attrs(self):
        p = _make_player(position="QB", throw_power=90, throw_accuracy=90, speed=75)
        # QB overall = (throw_power + throw_accuracy + speed) / 3
        expected = int((90 + 90 + 75) / 3)
        assert p.overall() == expected

    def test_overall_k_averages_key_attrs(self):
        p = _make_player(position="K", kick_accuracy=80, kick_power=80)
        # K overall = (kick_accuracy + kick_power) / 2
        expected = int((80 + 80) / 2)
        assert p.overall() == expected

    def test_overall_ol_is_strength_only(self):
        p = _make_player(position="OL", strength=88)
        assert p.overall() == 88

    def test_overall_unknown_position_returns_zero(self):
        p = _make_player(position="PUNTER")
        assert p.overall() == 0

    def test_stats_default_is_blank(self):
        p = _make_player()
        assert p.stats["Passing Yards"] == 0
        assert "Receiving Yards" in p.stats  # correct spelling


class TestTeam:
    def _make_team(self, **kwargs) -> Team:
        defaults = dict(name="Ballers", coach="Coach K")
        defaults.update(kwargs)
        return Team(**defaults)

    def test_record_format(self):
        t = self._make_team(wins=3, losses=2)
        assert t.record == "3-2"

    def test_win_pct_no_games(self):
        t = self._make_team()
        assert t.win_pct == 0.0

    def test_win_pct_calculated(self):
        t = self._make_team(wins=3, losses=1)
        assert t.win_pct == 0.75

    def test_overall_empty_roster(self):
        t = self._make_team()
        assert t.overall() == 0

    def test_overall_with_player(self):
        t = self._make_team()
        p = _make_player(position="QB", throw_power=90, throw_accuracy=90, speed=75)
        t.roster["QB"].append(p)
        assert t.overall() == p.overall()

    def test_empty_roster_has_all_positions(self):
        roster = empty_roster()
        for pos in ["QB", "RB", "WR", "TE", "OL", "DL", "LB", "DB", "K"]:
            assert pos in roster
            assert isinstance(roster[pos], list)
