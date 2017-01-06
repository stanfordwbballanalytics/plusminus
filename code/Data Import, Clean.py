# libraries
import numpy as np
import pandas as pd
import datetime
import math
import xlsxwriter

pd.options.mode.chained_assignment = None  # allows us to change one datapoint in df (default is warn)



# import data
data_raw = pd.read_excel('../../Data/20170101arizona.xlsx')


data_raw.shape


data_raw.head(15)


# rename columns
data = data_raw.rename(columns = {'Play-by-Play': 'HOME_TEAM', 'Unnamed: 1': 'TIME', 'Unnamed: 2': 'SCORE',                                      'Unnamed: 3': 'MARGIN', 'Unnamed: 4': 'AWAY_TEAM'})


# identify opponent, date, and whether game is home or away
data['OPPONENT'] = 'ARIZONA'
data['DATE'] = datetime.datetime(2017, 1,1)
data['LOC'] = 'AWAY'


# upcase
data.AWAY_TEAM = data.AWAY_TEAM.str.upper()
data.HOME_TEAM = data.HOME_TEAM.str.upper()

# strip
data.AWAY_TEAM = data.AWAY_TEAM.str.strip()
data.HOME_TEAM = data.HOME_TEAM.str.strip()

# fill NAs with value before
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


# set starters
starters = ['NADIA','ERICA','BRIANA','BRITTANY','KARLIE']


# create lineup list of STARTERS
lineup = ['NADIA','ERICA','BRIANA','BRITTANY','KARLIE']
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
    else:
        pass
    

# remove from list when subbing in/out

if data2.LOC[1] == 'HOME':
    for row in range(len(data2)):
        print row
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
                print lineup

            else:
                pass
        elif data2.TIME.str[:5][row] == '-----':
            # do this when new quarter starts. lineup is starting lineup
            lineup = ['NADIA','ERICA','BRIANA','BRITTANY','KARLIE']
        else:
            pass
        
else:
    for row in range(len(data2)):
        print row
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
                print data2.TIME[row], lineup

            else:
                pass
        elif data2.TIME.str[:5][row] == '-----':
            # do this when new quarter starts. lineup is starting lineup
            lineup = ['NADIA','ERICA','BRIANA','BRITTANY','KARLIE']
        else:
            pass



# fill in players down
data2b = data2
data2b.P1 = data2b.P1.fillna(method = 'ffill')
data2b.P2 = data2b.P2.fillna(method = 'ffill')
data2b.P3 = data2b.P3.fillna(method = 'ffill')
data2b.P4 = data2b.P4.fillna(method = 'ffill')
data2b.P5 = data2b.P5.fillna(method = 'ffill')



# keep rows that have time only (delete others) 
data3 = data2b[(data2b.TIME.str[:2] == '10') | (data2b.TIME.str[:1] == '0')]
data3b = data3[data3.TIME.str.contains(':')].reset_index(drop=True)



# insert minutes, seconds, and time in seconds
data3b['TIME_MIN'] = data3b.TIME.str.split(':').str[0]
data3b['TIME_SEC'] = data3b.TIME.str.split(':').str[1]
data3b['TIME_LEFT_SEC'] = 60*data3b.TIME_MIN.astype(int) + data3b.TIME_SEC.astype(int)



# create lineup variable
data3b['LINEUP'] = data3b.P1 + ", " + data3b.P2 + ", " + data3b.P3 + ", " + data3b.P4 + ", " + data3b.P5


### check if individual player is in
def player_in(pname):
    data3b['%s' % pname] = 0
    for row in range(len(data3b)):
        if '%s' % pname in data3b.LINEUP[row]:
            data3b['%s' % pname][row] = 1
            
player_in('KARLIE')
player_in('BRIANA')
player_in('KAYLEE')
player_in('ERICA')
player_in('DIJONAI')
player_in('NADIA')
player_in('BRITTANY')
player_in('MARTA')
player_in('ALANNA')
player_in('ANNA')



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


# check how many nulls per column
data3b.isnull().sum()


# count only if margin is less than or equal to 20
data3c = data3b[abs(data3b.MARGIN_SU) <= 20]
data3c.shape, data3b.shape


# reset index
data4a = data3c.reset_index(drop=True)
data4a.head(10)


# groupby everything we could
data4b = data4a.groupby('LINEUP', as_index=False).sum()
data4b


# separate groupby for margin difference
data4c = data4a[['LINEUP','MARGIN_DIFF','OFF_DIFF','DEF_DIFF']]
data4d = data4c.groupby('LINEUP', as_index = False).sum()
data4d


data4b.TIME_DIFF.sum(), 40*60


data4a.MARGIN_DIFF.describe()


type(data4a.MARGIN_DIFF[150])


# merge the two datasets
data_agg = pd.merge(data4b, data4d, on = 'LINEUP', how = 'left')
data_agg['TIME_DIFF_MIN'] = data_agg.TIME_DIFF / 60
data_agg['MARGIN/MIN'] = data_agg.MARGIN_DIFF / data_agg.TIME_DIFF_MIN
data_agg2 = data_agg[['LINEUP','TIME_DIFF_MIN','MARGIN_DIFF','OFF_DIFF','DEF_DIFF','MARGIN/MIN']]


data_agg3 = data_agg2.sort_values(by = 'TIME_DIFF_MIN', ascending = False).reset_index(drop=True)
print data_agg3



