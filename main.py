import random
import copy
import csv

firstnames = open('player_data/firstnames.csv')
lastnames = open('player_data/lastnames.csv')
csvreader = csv.reader(firstnames)
csvreader2 = csv.reader(lastnames)
rows2 = []
rows = []
long_yards = []
for i in range(21, 100):
    long_yards.append(i)
FIRST_NAMES = []
LAST_NAMES = []
DEPTH_CHART = {
    "QB": [],
    "RB": [],
    "WR": [],
    "TE": [],
    "OL": [],
    "DL": [],
    "LB": [],
    "DB": [],
    "K": []
}
FREE_AGENTS = {
    "QB": [],
    "RB": [],
    "WR": [],
    "TE": [],
    "OL": [],
    "DL": [],
    "LB": [],
    "DB": [],
    "K": []
}
STATS = {
    "Passing Attempts": 0,
    "Completions": 0,
    "Passing Yards": 0,
    "Touchdown Passes": 0,
    "Pass Interceptions": 0,
    "Rushing Attempts": 0,
    "Rushing Yards": 0,
    "Rushing Touchdowns": 0,
    "Receptions": 0,
    "Recieving Yards": 0,
    "Recieving Touchdowns": 0,
    "Tackles": 0,
    "Sacks": 0,
    "Interceptions": 0,
    "Field Goals Made": 0,
    "Field Goals Attempted": 0,
    "Field Goal Accuracy": 0,
    "Longest Field Goal": 0
}
RUN_OUTCOMES = {
    "LOSS": [-5, -4, -3, -2, -1],
    "SHORT": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "MID": [11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
    "LONG": long_yards,
}
PASS_OUTCOMES = {
    "LOSS": [-5, -4, -3, -2, -1],
    "SHORT": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "MID": [11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
    "LONG": long_yards
}
coach_names = [
    "Mike Ditka", "William Wonka", "Bilbo Baggins", "Lovie Smith", "James Neutron", "John Madden",
    "Deion Sanders", "Adam Gase", "Ronald McDonald", "Sean McVay", "Larry the Lobster", "Bruce Arians",
    "Curious George", "Mike McCarthy", "Squidward Tentacles"
]
team_names = [
    "Broncos", "Rams", "Browns", "Bears", "Dolphins", "Seahawks", "Commanders", "Packers", "Cardinals",
    "Patriots", "Buccaneers", "Lions", "Falcons", "Saints", "Panthers"
]
week = 0
fieldpos = 0
season = False
prospects = []
teams = []
matchups = [[], [], [], [], [], [], [], []]
coachnamer = ""
for row in csvreader:
    FIRST_NAMES.append(row[1].upper())
for row in csvreader2:
    LAST_NAMES.append(row[1])
FIRST_NAMES.pop(0)
LAST_NAMES.pop(0)


class Team:
    def __init__(self, name, wins, losses, coach, roster, runtend, passtend):
        self.name = name
        self.wins = wins
        self.losses = losses
        self.coach = coach
        self.roster = roster
        self.runtend = runtend
        self.passtend = passtend

    def get_name(self):
        return self.name

    def get_wins(self):
        return self.wins

    def get_losses(self):
        return self.losses

    def get_ratio(self):
        return round((self.wins / (self.wins + self.losses)), 3)

    def get_coach(self):
        return self.coach

    def get_roster(self):
        return self.roster

    def get_runtend(self):
        return self.runtend

    def get_passtend(self):
        return self.passtend

    def get_overall(self):
        val = 0
        for key, value in self.roster.items():
            for i in range(len(value)):
                val += get_ovr(value[i])
        return int(val / 24)


class Player:
    def __init__(self, fname, lname, pos, spd, stg, cat, thp, tpa, tkl, cov, kp, ka, con, stats):
        self.position = pos
        self.firstname = fname
        self.lastname = lname
        self.speed = spd
        self.strength = stg
        self.catching = cat
        self.throwpower = thp
        self.throwaccuracy = tpa
        self.tackle = tkl
        self.coverage = cov
        self.kickpower = kp
        self.kickaccuracy = ka
        self.contract = con
        self.stats = stats

    def get_speed(self):
        return self.speed

    def get_position(self):
        return self.position

    def get_catching(self):
        return self.catching

    def get_strength(self):
        return self.strength

    def get_throwpow(self):
        return self.throwpower

    def get_throwacc(self):
        return self.throwaccuracy

    def get_tackle(self):
        return self.tackle

    def get_coverage(self):
        return self.coverage

    def get_kickpow(self):
        return self.kickpower

    def get_kickacc(self):
        return self.kickaccuracy

    def get_contract(self):
        return self.contract

    def get_stats(self):
        return self.stats

    def get_fullname(self):
        return self.firstname + " " + self.lastname

    def get_overall(self, stat1, stat2, stat3):
        return (stat1 + stat2 + stat3) / 3


def gen_teams():
    global teams
    for i in range(len(team_names)):
        rt = random.randint(20, 80)
        pt = 100 - rt
        tempteam = copy.deepcopy(DEPTH_CHART)
        coachname = random.choice(coach_names)
        teamname = random.choice(team_names)
        team_names.pop(team_names.index(teamname))
        coach_names.pop(coach_names.index(coachname))
        teams.append(Team(teamname, 0, 0, coachname,
                          tempteam, rt, pt))


def gen_rb(team, times):
    statsheet = copy.deepcopy(STATS)
    while len(team["RB"]) < times:
        new_player = Player(random.choice(FIRST_NAMES), random.choice(LAST_NAMES), "RB", random.randint(85, 95),
                            random.randint(55, 85), random.randint(
            65, 80), random.randint(25, 35), random.randint(15, 25),
            random.randint(45, 65), random.randint(
            15, 25), random.randint(25, 45),
            random.randint(15, 35), random.randint(2, 5), statsheet)
        team["RB"].append(new_player)


def gen_wr(team, times):
    statsheet = copy.deepcopy(STATS)
    while len(team["WR"]) < times:
        new_player = Player(random.choice(FIRST_NAMES), random.choice(LAST_NAMES), "WR", random.randint(85, 99),
                            random.randint(65, 75), random.randint(
            75, 90), random.randint(25, 35), random.randint(15, 25),
            random.randint(45, 65), random.randint(
            15, 25), random.randint(25, 45),
            random.randint(15, 35), random.randint(2, 5), statsheet)
        team["WR"].append(new_player)


def gen_te(team, times):
    statsheet = copy.deepcopy(STATS)
    while len(team["TE"]) < times:
        new_player = Player(random.choice(FIRST_NAMES), random.choice(LAST_NAMES), "TE", random.randint(75, 90),
                            random.randint(75, 90), random.randint(
            70, 90), random.randint(25, 35), random.randint(15, 25),
            random.randint(45, 65), random.randint(
            15, 25), random.randint(25, 45),
            random.randint(15, 35), random.randint(2, 5), statsheet)
        team["TE"].append(new_player)


def gen_oline(team, times):
    statsheet = copy.deepcopy(STATS)
    while len(team["OL"]) < times:
        new_player = Player(random.choice(FIRST_NAMES), random.choice(LAST_NAMES), "OL", random.randint(55, 65),
                            random.randint(70, 95), random.randint(
            35, 55), random.randint(35, 45), random.randint(35, 45),
            random.randint(55, 65), random.randint(
            15, 25), random.randint(40, 50),
            random.randint(15, 30), random.randint(2, 5), statsheet)
        team["OL"].append(new_player)


def gen_db(team, times):
    statsheet = copy.deepcopy(STATS)
    while len(team["DB"]) < times:
        new_player = Player(random.choice(FIRST_NAMES), random.choice(LAST_NAMES), "DB", random.randint(75, 99),
                            random.randint(55, 80), random.randint(
            65, 85), random.randint(35, 45), random.randint(35, 45),
            random.randint(75, 90), random.randint(
            75, 95), random.randint(40, 50),
            random.randint(15, 30), random.randint(2, 5), statsheet)
        team["DB"].append(new_player)


def gen_lb(team, times):
    statsheet = copy.deepcopy(STATS)
    while len(team["LB"]) < times:
        new_player = Player(random.choice(FIRST_NAMES), random.choice(LAST_NAMES), "LB", random.randint(75, 95),
                            random.randint(75, 95), random.randint(
            35, 55), random.randint(35, 45), random.randint(35, 45),
            random.randint(75, 85), random.randint(
            65, 85), random.randint(40, 50),
            random.randint(15, 30), random.randint(2, 5), statsheet)
        team["LB"].append(new_player)


def gen_dline(team, times):
    statsheet = copy.deepcopy(STATS)
    while len(team["DL"]) < times:
        new_player = Player(random.choice(FIRST_NAMES), random.choice(LAST_NAMES), "DL", random.randint(65, 85),
                            random.randint(85, 95), random.randint(
            35, 55), random.randint(35, 45), random.randint(35, 45),
            random.randint(75, 95), random.randint(
            15, 25), random.randint(40, 50),
            random.randint(15, 30), random.randint(2, 5), statsheet)
        team["DL"].append(new_player)


def gen_qb(team, times):
    statsheet = copy.deepcopy(STATS)
    while len(team["QB"]) < times:
        new_player = Player(random.choice(FIRST_NAMES), random.choice(LAST_NAMES), "QB", random.randint(70, 85),
                            random.randint(60, 80), random.randint(
            35, 55), random.randint(75, 90), random.randint(75, 90),
            random.randint(25, 45), random.randint(
            15, 25), random.randint(40, 50),
            random.randint(15, 30), random.randint(2, 5), statsheet)
        team["QB"].append(new_player)


def gen_kick(team, times):
    statsheet = copy.deepcopy(STATS)
    while len(team["K"]) < times:
        new_player = Player(random.choice(FIRST_NAMES), random.choice(LAST_NAMES), "K", random.randint(70, 85),
                            random.randint(60, 70), random.randint(
            45, 55), random.randint(45, 55), random.randint(55, 65),
            random.randint(25, 45), random.randint(
            15, 25), random.randint(75, 90),
            random.randint(75, 90), random.randint(2, 5), statsheet)
        team["K"].append(new_player)


def gen_base_team(team):
    gen_lb(team, 3)
    gen_wr(team, 3)
    gen_te(team, 1)
    gen_qb(team, 1)
    gen_db(team, 4)
    gen_rb(team, 1)
    gen_oline(team, 5)
    gen_dline(team, 4)
    gen_kick(team, 1)


def show_winnings():
    for i in teams:
        print(
            f"Team Name: {i.get_name()}\nWins: {i.get_wins()}\nLosses: {i.get_losses()}\nWin/Loss Ratio: {i.get_ratio()}\n")


def get_ovr(player):
    if player.get_position() == "QB":
        return int(player.get_overall(player.get_throwpow(), player.get_throwacc(), player.get_speed()))
    elif player.get_position() == "RB":
        return int(player.get_overall(player.get_speed(), player.get_catching(), player.get_strength()))
    elif player.get_position() == "WR":
        return int(player.get_overall(player.get_speed(), player.get_catching(), player.get_strength()))
    elif player.get_position() == "TE":
        return int(player.get_overall(player.get_speed(), player.get_catching(), player.get_strength()))
    elif player.get_position() == "OL":
        return player.get_strength()
    elif player.get_position() == "LB":
        return int(player.get_overall(player.get_tackle(), player.get_strength(), player.get_coverage()))
    elif player.get_position() == "DL":
        return int(player.get_overall(player.get_tackle(), player.get_strength(), player.get_speed()))
    elif player.get_position() == "DB":
        return int(player.get_overall(player.get_coverage(), player.get_tackle(), player.get_speed()))
    elif player.get_position() == "K":
        return int((player.get_kickacc() + player.get_kickpow()) / 2)


def gen_freeagents(team):
    gen_qb(team, 4)
    gen_wr(team, 12)
    gen_rb(team, 4)
    gen_te(team, 4)
    gen_oline(team, 20)
    gen_dline(team, 16)
    gen_lb(team, 12)
    gen_db(team, 16)
    gen_kick(team, 4)
    show_freeagents(team)


def cut_player():
    spot = input("What position would you like to cut?\n")
    if spot.upper() == "QB":
        move = input(
            "If you cut this player, you automatically be made to sign another one. Proceed? (y/n)\n")
        if move.upper() == "Y":
            coach_dchart["QB"].pop(0)
            show_depth_chart(teams[0], coach_dchart)
        else:
            cut_player()
    elif spot.upper() == "RB":
        move = input(
            "If you cut this player, you automatically be made to sign another one. Proceed? (y/n)\n")
        if move.upper() == "Y":
            coach_dchart["RB"].pop(0)
            show_depth_chart(teams[0], coach_dchart)
        else:
            cut_player()
    elif spot.upper() == "WR":
        move = input(
            "If you cut this player, you automatically be made to sign another one. Proceed? (y/n)\n")
        if move.upper() == "Y":
            spot = int(input("Which player do you want to cut?\n"))
            coach_dchart["WR"].pop(spot - 1)
            show_depth_chart(teams[0], coach_dchart)
        else:
            cut_player()
    elif spot.upper() == "OL":
        move = input(
            "If you cut this player, you automatically be made to sign another one. Proceed? (y/n)\n")
        if move.upper() == "Y":
            spot = int(input("Which player do you want to cut?\n"))
            coach_dchart["OL"].pop(spot - 1)
            show_depth_chart(teams[0], coach_dchart)
        else:
            cut_player()
    elif spot.upper() == "DL":
        move = input(
            "If you cut this player, you automatically be made to sign another one. Proceed? (y/n)\n")
        if move.upper() == "Y":
            spot = int(input("Which player do you want to cut?\n"))
            coach_dchart["DL"].pop(spot - 1)
            show_depth_chart(teams[0], coach_dchart)
        else:
            cut_player()
    elif spot.upper() == "LB":
        move = input(
            "If you cut this player, you automatically be made to sign another one. Proceed? (y/n)\n")
        if move.upper() == "Y":
            spot = int(input("Which player do you want to cut?\n"))
            coach_dchart["LB"].pop(spot - 1)
            show_depth_chart(teams[0], coach_dchart)
        else:
            cut_player()
    elif spot.upper() == "DB":
        move = input(
            "If you cut this player, you automatically be made to sign another one. Proceed? (y/n)\n")
        if move.upper() == "Y":
            spot = int(input("Which player do you want to cut?\n"))
            coach_dchart["DB"].pop(spot - 1)
            show_depth_chart(teams[0], coach_dchart)
        else:
            cut_player()
    elif spot.upper() == "K":
        move = input(
            "If you cut this player, you automatically be made to sign another one. Proceed? (y/n)\n")
        if move.upper() == "Y":
            coach_dchart["K"].pop(0)
            show_depth_chart(teams[0], coach_dchart)
        else:
            cut_player()


def prompter():
    global FREE_AGENTS, teams, season, week
    move = input(f"\nWhat would you like to do {coachnamer}?\n")
    if move.upper() == "ROSTER":
        show_depth_chart(teams[0], coach_dchart)
        prompter()
    elif move.upper() == "FREE AGENTS":
        gen_freeagents(FREE_AGENTS)
        prompter()
    elif move.upper() == "CUT":
        cut_player()
        prompter()
    elif move.upper() == "SIGN":
        pass
    elif move.upper() == "TEAMS":
        for i in teams:
            show_depth_chart(i, i.get_roster())
        prompter()
    elif move.upper() == "SCHEDULE":
        show_schedule()
        prompter()
    elif move.upper() == "WINNINGS":
        show_winnings()
        prompter()
    elif move.upper() == "STATS":
        for key, value in coach_dchart.items():
            for i in range(len(value)):
                show_stats(coach_dchart[key][i].get_fullname(
                ), coach_dchart[key][i].get_stats())
        prompter()
    elif move.upper() == "GAME":
        if season:
            game_loop()
            prompter()
        else:
            print("The season has yet to start! Type in 'advance' to advance to week 1!")
            prompter()
    elif move.upper() == "ADVANCE":
        week += 1
        print(f"It is week {week}!")
        season = True
        prompter()
    else:
        print("That is not a valid command")
        prompter()


def show_depth_chart(name, roster):
    print("\nTeam Name: {}".format(name.get_name()) + " ----- Coach Name: {}".format(
        name.get_coach()) + " ----- Run Tendency: {}".format(name.get_runtend()) + " ----- Pass Tendency: {}".format(
        name.get_passtend()) + " ----- Overall Rating: {}".format(name.get_overall()))
    print("")
    for key, value in roster.items():
        print("Position: {}".format(key))
        for i in range(len(value)):
            print("Spot #{} ----- ".format(i + 1) + "Player Name: {}".format(value[i].get_fullname(
            )) + " ----- OVR rating: {}".format(get_ovr(value[i]))
                + " ----- Years left: {}".format(value[i].get_contract()))
        print("")


def show_freeagents(roster):
    for key, value in roster.items():
        print("Position: {}".format(key))
        for i in range(len(value)):
            print("Spot #{} ----- ".format(i + 1) + "Player Name: {}".format(value[i].get_fullname(
            )) + " ----- OVR rating: {}".format(get_ovr(value[i]))
                + " ----- Deal length: {}".format(value[i].get_contract()))
        print("")
    signer = input("What position are you interested in signing?\n")
    sign_agent(signer)


def sign_agent(position):
    if position.upper() == "QB":
        spot = int(input("Which player do you want to sign?\n"))
        if len(coach_dchart["QB"]) == 1:
            move = input(
                "You already have the maximum number of players allowed for this position. Would you like to replace a current player with this free agent? (y/n)\n")
            if move.upper() == "Y":
                coach_dchart["QB"].pop(0)
                coach_dchart["QB"].append(FREE_AGENTS["QB"][spot - 1])
                show_depth_chart(teams[0], coach_dchart)
                FREE_AGENTS["QB"].pop(spot - 1)
                return
        coach_dchart["QB"].append(FREE_AGENTS["QB"][spot - 1])
        show_depth_chart(teams[0], coach_dchart)
        FREE_AGENTS["QB"].pop(spot - 1)
    elif position.upper() == "RB":
        spot = int(input("Which player do you want to sign?\n"))
        if len(coach_dchart["RB"]) == 1:
            move = input(
                "You already have the maximum number of players allowed for this position. Would you like to replace a current player with this free agent? (y/n)\n")
            if move.upper() == "Y":
                coach_dchart["RB"].pop(0)
                coach_dchart["RB"].append(FREE_AGENTS["RB"][spot - 1])
                show_depth_chart(teams[0], coach_dchart)
                FREE_AGENTS["RB"].pop(spot - 1)
                return
        coach_dchart["RB"].append(FREE_AGENTS["RB"][spot - 1])
        show_depth_chart(teams[0], coach_dchart)
        FREE_AGENTS["RB"].pop(spot - 1)
    elif position.upper() == "WR":
        spot = int(input("Which player do you want to sign?\n"))
        if len(coach_dchart["WR"]) == 3:
            move = input(
                "You already have the maximum number of players allowed for this position. Would you like to replace a current player with this free agent? (y/n)\n")
            if move.upper() == "Y":
                switch = int(input(
                    "Which one of your own players would you like to replace with this free agent?\n"))
                coach_dchart["WR"].pop(switch - 1)
                coach_dchart["WR"].append(FREE_AGENTS["WR"][spot - 1])
                show_depth_chart(teams[0], coach_dchart)
                FREE_AGENTS["WR"].pop(spot - 1)
                return
        coach_dchart["WR"].append(FREE_AGENTS["WR"][spot - 1])
        show_depth_chart(teams[0], coach_dchart)
        FREE_AGENTS["WR"].pop(spot - 1)
    elif position.upper() == "TE":
        spot = int(input("Which player do you want to sign?\n"))
        if len(coach_dchart["TE"]) == 1:
            move = input(
                "You already have the maximum number of players allowed for this position. Would you like to replace a current player with this free agent? (y/n)\n")
            if move.upper() == "Y":
                coach_dchart["TE"].pop(0)
                coach_dchart["TE"].append(FREE_AGENTS["TE"][spot - 1])
                show_depth_chart(teams[0], coach_dchart)
                FREE_AGENTS["TE"].pop(spot - 1)
                return
        coach_dchart["TE"].append(FREE_AGENTS["TE"][spot - 1])
        show_depth_chart(teams[0], coach_dchart)
        FREE_AGENTS["TE"].pop(spot - 1)
    elif position.upper() == "OL":
        spot = int(input("Which player do you want to sign?\n"))
        if len(coach_dchart["OL"]) == 5:
            move = input(
                "You already have the maximum number of players allowed for this position. Would you like to replace a current player with this free agent? (y/n)\n")
            if move.upper() == "Y":
                switch = int(input(
                    "Which one of your own players would you like to replace with this free agent?\n"))
                coach_dchart["OL"].pop(switch - 1)
                coach_dchart["OL"].append(FREE_AGENTS["OL"][spot - 1])
                show_depth_chart(teams[0], coach_dchart)
                FREE_AGENTS["OL"].pop(spot - 1)
                return
        coach_dchart["OL"].append(FREE_AGENTS["OL"][spot - 1])
        show_depth_chart(teams[0], coach_dchart)
        FREE_AGENTS["OL"].pop(spot - 1)
    elif position.upper() == "DL":
        spot = int(input("Which player do you want to sign?\n"))
        if len(coach_dchart["DL"]) == 4:
            move = input(
                "You already have the maximum number of players allowed for this position. Would you like to replace a current player with this free agent? (y/n)\n")
            if move.upper() == "Y":
                switch = int(input(
                    "Which one of your own players would you like to replace with this free agent?\n"))
                coach_dchart["DL"].pop(switch - 1)
                coach_dchart["DL"].append(FREE_AGENTS["DL"][spot - 1])
                show_depth_chart(teams[0], coach_dchart)
                FREE_AGENTS["DL"].pop(spot - 1)
                return
        coach_dchart["DL"].append(FREE_AGENTS["DL"][spot - 1])
        show_depth_chart(teams[0], coach_dchart)
        FREE_AGENTS["DL"].pop(spot - 1)
    elif position.upper() == "LB":
        spot = int(input("Which player do you want to sign?\n"))
        if len(coach_dchart["LB"]) == 3:
            move = input(
                "You already have the maximum number of players allowed for this position. Would you like to replace a current player with this free agent? (y/n)\n")
            if move.upper() == "Y":
                switch = int(input(
                    "Which one of your own players would you like to replace with this free agent?\n"))
                coach_dchart["LB"].pop(switch - 1)
                coach_dchart["LB"].append(FREE_AGENTS["LB"][spot - 1])
                show_depth_chart(teams[0], coach_dchart)
                FREE_AGENTS["LB"].pop(spot - 1)
                return
        coach_dchart["LB"].append(FREE_AGENTS["LB"][spot - 1])
        show_depth_chart(teams[0], coach_dchart)
        FREE_AGENTS["LB"].pop(spot - 1)
    elif position.upper() == "DB":
        spot = int(input("Which player do you want to sign?\n"))
        if len(coach_dchart["DB"]) == 4:
            move = input(
                "You already have the maximum number of players allowed for this position. Would you like to replace a current player with this free agent? (y/n)\n")
            if move.upper() == "Y":
                switch = int(input(
                    "Which one of your own players would you like to replace with this free agent?\n"))
                coach_dchart["DB"].pop(switch - 1)
                coach_dchart["DB"].append(FREE_AGENTS["DB"][spot - 1])
                show_depth_chart(teams[0], coach_dchart)
                FREE_AGENTS["DB"].pop(spot - 1)
                return
        coach_dchart["DB"].append(FREE_AGENTS["DB"][spot - 1])
        show_depth_chart(teams[0], coach_dchart)
        FREE_AGENTS["DB"].pop(spot - 1)
    elif position.upper() == "K":
        spot = int(input("Which player do you want to sign?\n"))
        if len(coach_dchart["K"]) == 1:
            move = input(
                "You already have the maximum number of players allowed for this position. Would you like to replace a current player with this free agent? (y/n)\n")
            if move.upper() == "Y":
                coach_dchart["K"].pop(0)
                coach_dchart["K"].append(FREE_AGENTS["K"][spot - 1])
                show_depth_chart(teams[0], coach_dchart)
                FREE_AGENTS["K"].pop(spot - 1)
                return
        coach_dchart["K"].append(FREE_AGENTS["K"][spot - 1])
        show_depth_chart(teams[0], coach_dchart)
        FREE_AGENTS["K"].pop(spot - 1)
    prompter()


def show_stats(name, player):
    print("Player Name: {}".format(name))
    print("")
    for key, value in player.items():
        print("{}:".format(key) + " " + "{}".format(value))
    print("\n")


def make_matchups():
    global teams, week
    temp_teams = copy.deepcopy(teams)
    for i in range(len(matchups)):
        while len(matchups[i]) < 2:
            spot = random.choice(temp_teams)
            matchups[i].append(spot)
            temp_teams.pop(temp_teams.index(spot))


def show_schedule():
    print(f"Week {week} matchups:\n")
    for i in range(len(matchups)):
        print(matchups[i][0].get_name() + " vs. " + matchups[i][1].get_name())


def game_loop():
    global matchups, teams
    game = 0
    myteam = 0
    opp = 0
    for i in range(len(matchups)):
        for j in range(2):
            if matchups[i][j].get_coach() == teams[0].get_coach():
                game = i
                if j == 0:
                    opp = j + 1
                    myteam = j
                elif j == 1:
                    opp = j - 1
                    myteam = j
                break
    print(
        f"This weeks game is against the {matchups[game][opp].get_name()}")
    startgame = input("Would you like to begin the game? (y/n): ")
    if startgame.upper() == "Y":
        run_game(matchups[game][opp], matchups[game][myteam])
    else:
        return print("\nCome back when you have made your mind!\n")


def run_game(opp, myteam):
    sim = input(
        "Would you like to be present in the game or simulate it? (p/s): ")
    if sim.upper() == "P":
        play_by_play(opp, myteam)
    elif sim.upper() == "S":
        sim_game(opp, myteam)


def sim_game(t1, t2):
    print(t1.get_name(), t2.get_name())


def coin_toss(t1name, t2name, t1, t2):
    pick = random.randint(0, 1)
    if pick == 1:
        winner = t2name
        loser = t1name
        kickros = t1
        returnros = t2
    elif pick == 0:
        winner = t1name
        loser = t2name
        kickros = t2
        returnros = t1
    return f"The {winner} get to start with the ball!", winner, loser, kickros, returnros


def do_play(team, fieldpos, oppteam):
    roster = team.get_roster()
    # opproster = oppteam.get_roster()
    for i in range(50):
        playcall = random.randint(1, 100)
        if playcall < team.get_runtend():
            newinfo = (yardage_calc(oppteam, "RUN", fieldpos, roster["RB"][0], team)[0])
            print(newinfo[0])
            do_play(team, int(newinfo[1]), oppteam)
        elif playcall > team.get_runtend():
            recievers = []
            for values in roster["WR"]:
                recievers.append(values)
            for values in roster["TE"]:
                recievers.append(values)
            print(yardage_calc(oppteam, "PASS", fieldpos, recievers, team)[0])


def yardage_calc(oppteam, playtype, fieldpos, player, mainteam):
    opproster = oppteam.get_roster()
    mainroster = mainteam.get_roster()
    tacklers = []
    for keys, values in opproster.items():
        if keys == "QB" or keys == "RB" or keys == "WR" or keys == "TE" or keys == "OL" or keys == "K":
            continue
        else:
            for i in range(len(values)):
                tacklers.append(values[i])
    if playtype == "RUN":
        run_keys = []
        for keys in RUN_OUTCOMES:
            run_keys.append(keys)
        outcome = random.choices(run_keys, weights=[3, 76, 18, 3], k=1)
        if outcome[0] == "FUMBLE":
            netyards = 0
            fieldpos -= netyards
            return player.get_fullname() + f"FUMBLED!! Recovered by {tacklers[random.randint(0, len(tacklers))].get_fullname()}", fieldpos, netyards
        else:
            netyards = RUN_OUTCOMES[outcome[0]][random.randint(0, len(RUN_OUTCOMES[outcome[0]]) - 1)]
            fieldpos -= netyards
            tackler = random.choices(tacklers, weights=[15, 15, 15, 15, 8, 8, 8, 4, 4, 4, 4], k=1)
            # return fieldpos, netyards, tackler[0].get_fullname()
            return player.get_fullname() + f" is handed off the ball. He gains {netyards} yards and is tackled by {tackler[0].get_fullname()} on the {fieldpos}-yard line", fieldpos, netyards, tackler,
    elif playtype == "PASS":
        pass_keys = []
        for keys in PASS_OUTCOMES:
            pass_keys.append(keys)
        target = player[random.randint(0, len(player) - 1)]
        defender = opproster["DB"][player.index(target)]
        chance = defender.get_coverage() - target.get_catching()
        print(chance, abs(chance))
        pick = random.randint(chance, 100)
        if pick > abs(chance):
            outcome = random.choices(pass_keys, weights=[2, 33, 45, 20], k=1)
            netyards = PASS_OUTCOMES[outcome[0]][random.randint(0, len(PASS_OUTCOMES[outcome[0]]) - 1)]
            fieldpos -= netyards
            tackler = random.choices(tacklers, weights=[4, 4, 4, 4, 8, 8, 8, 15, 15, 15, 15], k=1)
            return mainroster["QB"][0].get_fullname() + f" passes the ball to {target.get_fullname()}, and gains {netyards} on the play, being tackled by {tackler[0].get_fullname()}. The ball is now on the {fieldpos}-yard line", fieldpos, netyards, tackler[0].get_fullname()
        elif pick < abs(chance):
            return("incomplete")


def play_by_play(t1, t2):
    toss_win = coin_toss(t1.get_name(), t2.get_name(), t1, t2)
    print("\n" + toss_win[0])
    result = do_kickoff(toss_win[3])
    print("\n" + result[0])
    do_play(toss_win[4], result[1], toss_win[3])


def do_kickoff(team):
    global fieldpos
    roster_ = team.get_roster()
    player = roster_["K"][0]
    name = player.get_fullname()
    power = player.get_kickpow()
    fieldpos = int(power)
    if fieldpos > 50:
        fieldpos = 100 - fieldpos
    return f"{name} kicks the ball off to the {fieldpos}-yard line", fieldpos


def main():
    global coach_dchart, DEPTH_CHART, teams, coachnamer
    rt = random.randint(20, 80)
    pt = 100 - rt
    coach_dchart = copy.deepcopy(DEPTH_CHART)
    gen_base_team(coach_dchart)
    coachnamer = str(input(
        "Welcome to an NFL Dynasty Simulator!\nMake sure to read the README file attached to understand how the game works\nOnce you have done that, enter in your coach's name below\n"))
    teams.append(Team("Ballers", 0, 0, coachnamer, coach_dchart, rt, pt))
    gen_teams()
    for i in teams:
        gen_base_team(i.get_roster())
    make_matchups()
    prompter()


main()
