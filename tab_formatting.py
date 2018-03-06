import pandas as pd
import numpy as np


def generate_teams(tab_df):
    team_numbers = []
    team_names = []
    for team_string in tab_df["Team"]:
        team_number = team_string[:team_string.find("\r")]
        team_number = int(team_number)
        team_name = team_string[team_string.find("\r")+1:]
        team_name = team_name.replace("\r", " ")
        team_names.append(team_name)
        team_numbers.append(team_number)
    index_tuples = [("Team", "Number"), ("Team", "Name")]
    data1 = pd.Series(team_numbers)
    data2 = pd.Series(team_names)
    formatted_data = pd.concat([data1.to_frame(),data2.to_frame()], axis=1, keys=index_tuples)
    formatted_data.columns = formatted_data.columns.droplevel(2)
    return formatted_data


def generate_summary(tab_df):
    ballots_won = []
    ballots_lost = []
    ballots_tied = []
    total_ballots = []
    cs = []
    ocs = []
    pds = []
    for team_summary_pair in tab_df["Summary"].iteritems():
        team_wins = int(team_summary_pair[1][0])
        team_losses = int(team_summary_pair[1][2])
        team_ties = int(team_summary_pair[1][4])
        team_score = team_wins + (.5) * team_ties
        details = team_summary_pair[1][14:]
        cs_digits = 1
        if details[0] == "1" or details[0] == "2":
            cs_digits = 2
        else:
            pass
        if details[cs_digits] == ".":
            cs_digits += 2
        team_cs = float(details[0:cs_digits])
        details = details[cs_digits:]
        pd_start = max(details.find("+"), details.find("-"), details.find("#"))
        team_ocs = float(details[:pd_start])
        team_pd = np.NaN
        if details[pd_start] != "#": 
            team_pd = int(details[pd_start:])
        ballots_won.append(team_wins)
        ballots_lost.append(team_losses)
        ballots_tied.append(team_ties)
        total_ballots.append(team_score)
        cs.append(team_cs)
        ocs.append(team_ocs)
        pds.append(team_pd)
    index_tuples = list(zip(["Summary"]*7,["Ballots Won","Ballots Lost","Ballots Tied","CS","OCS","PD","Score"]))
    index = pd.MultiIndex.from_tuples(index_tuples)
    data = [ballots_won,ballots_lost,ballots_tied,cs,ocs,pds,total_ballots]
    data = np.array(data, dtype='float64').T
    formatted_data = pd.DataFrame(data,columns=index)
    return formatted_data


def generate_rounds(tab_df):
    rounds = []
    for i in range(4):
        roundnum = str(i+1)
        side = []
        opponent = []
        ballot1 = []
        ballot2 = []
        total_ballots = []
        for trial_string in tab_df["Round " + str(roundnum)]:
            if trial_string[0] == u'Π':
                side.append('P')
            else:
                side.append('D')
            opp = int(trial_string[3:7])
            opponent.append(opp)
            useful = trial_string[11:]
            nonties = useful.count("+") + useful.count("-")
            bal1 = 0
            bal2 = 0
            total = 0
            if nonties == 0:
                pass
            elif nonties == 1:
                if useful[-1] == "0":
                    bal1 = int(useful[:-1])
                else:
                    bal2 = int(useful[1:])
            else:
                second = max(useful.rfind("+"), useful.rfind("-"))
                bal1 = int(useful[:second])
                bal2 = int(useful[second:])
            ballot1.append(bal1)
            ballot2.append(bal2)
            for ballot in [bal1, bal2]:
                if ballot == 0:
                    total += 0.5
                elif ballot > 0:
                    total += 1
            total_ballots.append(total)
        data1 = pd.DataFrame(np.array([side]).T)
        data2 = pd.DataFrame(np.array([opponent, ballot1, ballot2], dtype='int64').T)
        data3 = pd.DataFrame(np.array([total_ballots], dtype='float64').T)
        index_tuples = list(zip(["Round " + roundnum]*5,["Side","Opponent","Ballot 1","Ballot 2","Total Ballots"]))
        index = pd.MultiIndex.from_tuples(index_tuples)
        formatted_round_data = pd.concat([data1,data2,data3], axis=1, keys=index_tuples)
        formatted_round_data.columns = index
        rounds.append(formatted_round_data)
    all_rounds = rounds[0].join(rounds[1]).join(rounds[2]).join(rounds[3])
    return all_rounds


def formatted_tab_df(tab_df):
    return generate_teams(tab_df).join(generate_rounds(tab_df)).join(generate_summary(tab_df))

print()