# libraries
import numpy as np
import pandas as pd
import datetime
import math
import xlsxwriter
pd.options.mode.chained_assignment = None  # allows us to change one datapoint in df (default is warn)



def part1(fname, opp, yr, mth, dy, loc, player1, player2, player3, player4, player5, mgin, pac12, top150):
    
    # import data
    data_raw = pd.read_excel('../../Data/%s.xlsx' % fname)
    
    # rename columns
    data = data_raw.rename(columns = {'Play-by-Play': 'HOME_TEAM', 'Unnamed: 1': 'TIME', 'Unnamed: 2': 'SCORE',                                      'Unnamed: 3': 'MARGIN', 'Unnamed: 4': 'AWAY_TEAM'})
    
    # identify opponent, date, and whether game is home or away
    data['OPPONENT'] = '%s' % opp
    data['DATE'] = datetime.datetime(yr, mth, dy)
    data['LOC'] = '%s' % loc
    
    # upcase
    data.AWAY_TEAM = data.AWAY_TEAM.str.upper()
    data.HOME_TEAM = data.HOME_TEAM.str.upper()

    # strip
    data.AWAY_TEAM = data.AWAY_TEAM.str.strip()
    data.HOME_TEAM = data.HOME_TEAM.str.strip()
    
    # fill blank spaces
    data.SCORE = data.SCORE.fillna(method = 'ffill')
    data.MARGIN = data.MARGIN.fillna(method = 'ffill')
    
    # create variable for the scores of home and away teams
    data['HOME_SCORE'] = data.SCORE.str.split('-').str[0]
    data['AWAY_SCORE'] = data.SCORE.str.split('-').str[1]
    
    # create variable for the scores of stanford and opponent
    data['SU_SCORE'] = 0
    data['OPP_SCORE'] = 0

    for row in range(len(data)):
        if data.LOC[row] == 'HOME':
            data.SU_SCORE[row] = data.HOME_SCORE[row]
            data.OPP_SCORE[row] = data.AWAY_SCORE[row]
        else:
            data.SU_SCORE[row] = data.AWAY_SCORE[row]
            data.OPP_SCORE[row] = data.HOME_SCORE[row]

    # create variable for quarter
    data['QUARTER'] = 0

    for row in np.arange(1,len(data),1):
        if data.TIME.str[:5][row] == '-----':
            data.QUARTER[row] = data.QUARTER[row-1] + 1
        else:
            data.QUARTER[row] = data.QUARTER[row-1]

    ## SWITCH ANNA WILSON's first name to ANNA_W
    data1b = data
    data1b.HOME_TEAM[data1b.HOME_TEAM == 'SUB IN : WILSON, ANNA'] = 'SUB IN : WILSON, ANNA_W'
    data1b.HOME_TEAM[data1b.HOME_TEAM == 'SUB OUT: WILSON, ANNA'] = 'SUB OUT: WILSON, ANNA_W'
    data1b.AWAY_TEAM[data1b.AWAY_TEAM == 'SUB IN : WILSON, ANNA'] = 'SUB IN : WILSON, ANNA_W'
    data1b.AWAY_TEAM[data1b.AWAY_TEAM == 'SUB OUT: WILSON, ANNA'] = 'SUB OUT: WILSON, ANNA_W'

    # start at 5th row
    data2 = data1b[5:].reset_index(drop=True)

    # create lineup list of STARTERS
    lineup = ['%s' % player1, '%s' % player2, '%s' % player3, '%s' % player4, '%s' % player5]
    lineup.sort()
    

    # create player variables
    for i in np.arange(1,6,1):
        data2['P%s' % i] = lineup[i - 1]
        data2['P%s' % i][1:] = np.nan

    # insert starting lineup whenever new quarter starts
    for row in np.arange(1,len(data2),1):
        if data2.TIME.str[:5][row] == '-----':
            data2.P1[row] = lineup[0]
            data2.P2[row] = lineup[1]
            data2.P3[row] = lineup[2]
            data2.P4[row] = lineup[3]
            data2.P5[row] = lineup[4]
#             print lineup
        else:
            pass

        
    # remove from list when subbing in/out
    if loc == 'HOME':
        for row in range(len(data2)):
            if data2.HOME_TEAM.str[:6][row] == 'SUB IN':
                # add player when it says sub in
                lineup.append(data2.HOME_TEAM.str[8:][row].split(',')[1].strip())
                lineup.sort()
            elif data2.HOME_TEAM.str[:7][row] == 'SUB OUT':
                # remove player when it says sub out
                lineup.remove(data2.HOME_TEAM.str[8:][row].split(',')[1].strip())
                lineup.sort()
                if len(lineup) <= 5:
                    # when lineup is back down to 5 players, write the player variables
                    data2.P1[row] = lineup[0]
                    data2.P2[row] = lineup[1]
                    data2.P3[row] = lineup[2]
                    data2.P4[row] = lineup[3]
                    data2.P5[row] = lineup[4]
#                     print lineup

                else:
                    pass
            elif data2.TIME.str[:5][row] == '-----':
                # do this when new quarter starts. lineup is starting lineup
                lineup = ['%s' % player1, '%s' % player2, '%s' % player3, '%s' % player4, '%s' % player5]
            else:
                pass

    else:
        for row in range(len(data2)):
            if data2.AWAY_TEAM.str[:6][row] == 'SUB IN':
                # add player when it says sub in
                lineup.append(data2.AWAY_TEAM.str[8:][row].split(',')[1].strip())
                lineup.sort()
            elif data2.AWAY_TEAM.str[:7][row] == 'SUB OUT':
                # remove player when it says sub out
                lineup.remove(data2.AWAY_TEAM.str[8:][row].split(',')[1].strip())
                lineup.sort()
                if len(lineup) <= 5:
                    # when lineup is back down to 5 players, write the player variables
                    data2.P1[row] = lineup[0]
                    data2.P2[row] = lineup[1]
                    data2.P3[row] = lineup[2]
                    data2.P4[row] = lineup[3]
                    data2.P5[row] = lineup[4]
#                     print lineup

                else:
                    pass
            elif data2.TIME.str[:5][row] == '-----':
                # do this when new quarter starts. lineup is starting lineup
                lineup = ['%s' % player1, '%s' % player2, '%s' % player3, '%s' % player4, '%s' % player5]
            else:
                pass        
        
        
    # fill in players down
    data2b = data2
    data2b.P1 = data2b.P1.fillna(method = 'ffill')
    data2b.P2 = data2b.P2.fillna(method = 'ffill')
    data2b.P3 = data2b.P3.fillna(method = 'ffill')
    data2b.P4 = data2b.P4.fillna(method = 'ffill')
    data2b.P5 = data2b.P5.fillna(method = 'ffill')

    
    
    # grab 
    data3 = data2b[(data2b.TIME.str[:2] == '10') | (data2b.TIME.str[:1] == '0')]
    data3b = data3[data3.TIME.str.contains(':')].reset_index(drop=True)
    


    # insert minutes, seconds, and time in seconds
    data3b['TIME_MIN'] = data3b.TIME.str.split(':').str[0]
    data3b['TIME_SEC'] = data3b.TIME.str.split(':').str[1]
    data3b['TIME_LEFT_SEC'] = 60*data3b.TIME_MIN.astype(int) + data3b.TIME_SEC.astype(int)

    # create lineup variable
    data3b['LINEUP'] = data3b.P1 + ", " + data3b.P2 + ", " + data3b.P3 +                         ", " + data3b.P4 + ", " + data3b.P5
        


    # figure out HOME/AWAY/SU/OPP score and convert to int
    def score_int(var):
        data3b['%s' % var][0] = 0
        for row in range(1,len(data3b)):
            if len(data3b['%s' % var][row]) == 0:
                data3b['%s' % var][row] = data3b['%s' % var][row-1]
            else:
                data3b['%s' % var][row] = int(data3b['%s' % var][row])

    score_int('HOME_SCORE')
    score_int('AWAY_SCORE')
    score_int('SU_SCORE')
    score_int('OPP_SCORE')

    # find out row by row margin differences (MARGIN2)
    data3b['MARGIN_SU'] = data3b.SU_SCORE - data3b.OPP_SCORE
    data3b['MARGIN_DIFF'] = data3b.MARGIN_SU - data3b.MARGIN_SU.shift()
    data3b['OFF_DIFF'] = data3b.SU_SCORE - data3b.SU_SCORE.shift()
    data3b['DEF_DIFF'] = data3b.OPP_SCORE - data3b.OPP_SCORE.shift()

    # find out row by row time differences (MARGIN2)
    data3b['TIME_DIFF'] = data3b.TIME_LEFT_SEC - data3b.TIME_LEFT_SEC.shift()
    data3b.TIME_DIFF[data3b.TIME_DIFF > 0] = 600 - data3b.TIME_LEFT_SEC
    # data3b.TIME_DIFF[data3b.TIME_DIFF > 0].shift() = data3b.TIME_DIFF.shift() + data3b.TIME_LEFT_SEC.shift()
    data3b.TIME_DIFF = abs(data3b.TIME_DIFF)

    # first row of MARGIN_DIFF and TIME_DIFF should be 0
    data3b.MARGIN_DIFF[0] = 0
    data3b.OFF_DIFF[0] = 0
    data3b.DEF_DIFF[0] = 0

    data3b.TIME_DIFF[0] = 600 - data3b.TIME_LEFT_SEC[0]
    


    # count only if margin is less than or equal to specified number
    data3c = data3b[abs(data3b.MARGIN_SU) <= mgin]

    
    
    
    
    
    ## START ANALYSIS
    
    data4a = data3c.reset_index(drop=True)

    # groupby everything we could
    data4b = data4a.groupby('LINEUP', as_index=False).sum()

    # separate groupby for margin/off/def difference
    data4c = data4a[['LINEUP','MARGIN_DIFF','OFF_DIFF','DEF_DIFF']]
    data4d = data4c.groupby('LINEUP', as_index = False).sum()
    

    # merge the two datasets
    data_agg = pd.merge(data4b, data4d, on = 'LINEUP', how = 'left')
    data_agg['TIME_DIFF_MIN'] = data_agg.TIME_DIFF / 60
    data_agg2 = data_agg[['LINEUP','TIME_DIFF_MIN','MARGIN_DIFF','OFF_DIFF','DEF_DIFF']]

    data_agg3 = data_agg2.sort_values(by = 'TIME_DIFF_MIN', ascending = False).reset_index(drop=True)
    data_agg3['DATE'] = datetime.datetime(yr, mth, dy)
    data_agg3['OPP'] = '%s' % opp
    data_agg3['PAC12'] = pac12 # pac-12 opponent?
    data_agg3['TOP150'] = top150 # top 100 opponent according to jeff sagarin?
    data_agg3['LOCATION'] = '%s' % loc
    
    data_agg4 = data_agg3[['DATE','OPP','LOCATION','PAC12','TOP150','LINEUP','TIME_DIFF_MIN',                           'MARGIN_DIFF','OFF_DIFF','DEF_DIFF']]
    
    return data_agg4


game_20161111calpoly = part1('20161111calpoly','CAL_POLY', 2016, 11, 11, 'HOME', 'KAYLEE',                                  'ERICA','BRIANA','MARTA','BRITTANY', 20, 0, 0)
game_20161114texas = part1('20161114texas','TEXAS', 2016, 11, 14, 'HOME', 'KAYLEE',                                  'ERICA','BRIANA','MARTA','BRITTANY', 20, 0, 1)
game_20161118gonzaga = part1('20161118gonzaga','GONZAGA', 2016, 11, 18, 'HOME', 'KAYLEE',                                  'ERICA','BRIANA','MARTA','BRITTANY', 20, 0, 1)
game_20161120csun = part1('20161120csun','CSUN', 2016, 11, 20, 'HOME', 'KAYLEE',                                  'ERICA','BRIANA','BRITTANY','KARLIE', 20, 0, 0)
game_20161124northeastern = part1('20161124northeastern','NORTHEASTERN', 2016, 11, 24, 'HOME', 'ALANNA',                                  'ERICA','BRIANA','BRITTANY','KARLIE', 20, 0, 0)
game_20161125wichitast = part1('20161125wichitast','WICHITA_ST', 2016, 11, 25, 'AWAY', 'ALANNA',                                  'ERICA','BRIANA','BRITTANY','KARLIE', 20, 0, 0)
game_20161126purdue = part1('20161126purdue','PURDUE', 2016, 11, 26, 'AWAY', 'ALANNA',                                  'ERICA','BRITTANY','MARTA','KARLIE', 20, 0, 1)
game_20161201csubakersfield = part1('20161201csubakersfield','CSU_BAKERSFIELD', 2016, 12, 1, 'AWAY', 'MARTA',                                  'ERICA','BRIANA','BRITTANY','KARLIE', 20, 0, 0)
game_20161204ucdavis = part1('20161204ucdavis','UC_DAVIS', 2016, 12, 4, 'HOME', 'MARTA',                                  'ERICA','BRIANA','BRITTANY','KARLIE', 20, 0, 1)
game_20161218tennessee = part1('20161218tennessee','TENNESSEE', 2016, 12, 18, 'AWAY', 'MARTA',                                  'ERICA','BRIANA','BRITTANY','KARLIE', 20, 0, 1)
game_20161221georgewashington = part1('20161221georgewashington','GEORGE_WASHINGTON', 2016, 12, 21, 'AWAY', 'MARTA',                                  'ERICA','BRIANA','BRITTANY','KARLIE', 20, 0, 1)
game_20161228yale = part1('20161228yale','YALE', 2016, 12, 28, 'HOME', 'NADIA',                                  'ERICA','BRIANA','BRITTANY','KARLIE', 20, 0, 0)
game_20161230arizonastate = part1('20161230arizonastate','ARIZONA_STATE', 2016, 12, 30, 'AWAY', 'NADIA',                                  'ERICA','BRIANA','BRITTANY','KARLIE', 20, 1, 1)
game_20170101arizona = part1('20170101arizona','ARIZONA', 2017, 1, 1, 'AWAY', 'NADIA',                                  'ERICA','BRIANA','BRITTANY','KARLIE', 20, 1, 1)


game_agg = pd.concat([
                      game_20161111calpoly,game_20161114texas,game_20161118gonzaga,game_20161120csun,\
                      game_20161124northeastern,game_20161125wichitast,game_20161126purdue,\
                      game_20161201csubakersfield,game_20161204ucdavis,game_20161218tennessee,\
                      game_20161221georgewashington,game_20161230arizonastate,\
                      game_20170101arizona
                     ])


game_agg1b = game_agg[game_agg.TOP150 == 1]
game_agg1c = game_agg[game_agg.PAC12 == 1]

game_agg2t = game_agg1b.groupby(by = 'LINEUP', as_index = False).sum()
game_agg2p = game_agg1c.groupby(by = 'LINEUP', as_index = False).sum()

game_agg3t = game_agg2t.sort_values(by = 'TIME_DIFF_MIN', ascending = False).reset_index(drop=True)
game_agg3p = game_agg2p.sort_values(by = 'TIME_DIFF_MIN', ascending = False).reset_index(drop=True)

game_agg3t['MARGIN/MIN'] = game_agg3t.MARGIN_DIFF / game_agg3t.TIME_DIFF_MIN
game_agg3p['MARGIN/MIN'] = game_agg3p.MARGIN_DIFF / game_agg3p.TIME_DIFF_MIN

game_agg4t = game_agg3t[['LINEUP','TIME_DIFF_MIN','MARGIN_DIFF','OFF_DIFF','DEF_DIFF','MARGIN/MIN']]
game_agg4p = game_agg3p[['LINEUP','TIME_DIFF_MIN','MARGIN_DIFF','OFF_DIFF','DEF_DIFF','MARGIN/MIN']]

print game_agg4t


# export

# game_agg4t.to_excel('../../Output/PlusMinusLineupsTop150.xlsx', index = False)
# game_agg4p.to_excel('../Output/PlusMinusLineupsPac12.xlsx', index = False)
