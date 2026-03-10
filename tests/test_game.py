"""Tests for dynasty_sim.game."""

import pytest

from dynasty_sim.constants import BLANK_STATS
from dynasty_sim.game import (
    GameResult,
    KickoffResult,
    PlayResult,
    coin_toss,
    do_kickoff,
    sim_game,
    simulate_play,
)
from dynasty_sim.models import Player, Team, empty_roster
from dynasty_sim.roster import generate_player, generate_roster, load_names
import copy


@pytest.fixture(scope="module")
def names():
    return load_names()


@pytest.fixture(scope="module")
def full_team_a(names):
    first, last = names
    from dynasty_sim.constants import BASE_ROSTER_COUNTS
    roster = generate_roster(BASE_ROSTER_COUNTS, first, last)
    return Team(name="Tigers", coach="Coach A", roster=roster, run_tendency=50, pass_tendency=50)


@pytest.fixture(scope="module")
def full_team_b(names):
    first, last = names
    from dynasty_sim.constants import BASE_ROSTER_COUNTS
    roster = generate_roster(BASE_ROSTER_COUNTS, first, last)
    return Team(name="Lions", coach="Coach B", roster=roster, run_tendency=50, pass_tendency=50)


class TestCoinToss:
    def test_returns_two_distinct_teams(self, full_team_a, full_team_b):
        msg, receiver, kicker = coin_toss(full_team_a, full_team_b)
        assert receiver is not kicker
        assert receiver in (full_team_a, full_team_b)
        assert kicker in (full_team_a, full_team_b)

    def test_announcement_is_string(self, full_team_a, full_team_b):
        msg, _, _ = coin_toss(full_team_a, full_team_b)
        assert isinstance(msg, str)
        assert len(msg) > 0


class TestDoKickoff:
    def test_returns_kickoff_result(self, full_team_a):
        result = do_kickoff(full_team_a)
        assert isinstance(result, KickoffResult)

    def test_field_pos_in_valid_range(self, full_team_a):
        for _ in range(20):
            result = do_kickoff(full_team_a)
            assert 0 <= result.field_pos <= 100

    def test_no_kicker_defaults_gracefully(self):
        team = Team(name="X", coach="Y")
        result = do_kickoff(team)
        assert isinstance(result.field_pos, int)
        assert 0 <= result.field_pos <= 100


class TestSimulatePlay:
    def test_run_play_returns_play_result(self, full_team_a, full_team_b):
        result = simulate_play(full_team_a, full_team_b, 25, "RUN")
        assert isinstance(result, PlayResult)

    def test_pass_play_returns_play_result(self, full_team_a, full_team_b):
        result = simulate_play(full_team_a, full_team_b, 25, "PASS")
        assert isinstance(result, PlayResult)

    def test_field_pos_stays_in_range(self, full_team_a, full_team_b):
        for _ in range(50):
            result = simulate_play(full_team_a, full_team_b, 50, "RUN")
            assert 0 <= result.field_pos <= 100

    def test_description_is_non_empty_string(self, full_team_a, full_team_b):
        result = simulate_play(full_team_a, full_team_b, 30, "PASS")
        assert isinstance(result.description, str)
        assert len(result.description) > 0

    def test_pass_with_no_receivers_returns_incomplete(self):
        """A team with no WR/TE should produce an incomplete pass, not crash."""
        offense = Team(name="No Receivers", coach="Test")
        defense = Team(name="Defense", coach="Test2")
        result = simulate_play(offense, defense, 25, "PASS")
        assert result.is_complete is False


class TestSimGame:
    def test_returns_game_result(self, full_team_a, full_team_b):
        result = sim_game(full_team_a, full_team_b)
        assert isinstance(result, GameResult)

    def test_winner_and_loser_are_input_teams(self, full_team_a, full_team_b):
        result = sim_game(full_team_a, full_team_b)
        assert result.winner in (full_team_a, full_team_b)
        assert result.loser in (full_team_a, full_team_b)
        assert result.winner is not result.loser

    def test_equal_teams_produces_valid_result(self):
        from dynasty_sim.constants import BASE_ROSTER_COUNTS
        t1 = Team(name="A", coach="Coach1")
        t2 = Team(name="B", coach="Coach2")
        result = sim_game(t1, t2)
        assert result.winner in (t1, t2)
