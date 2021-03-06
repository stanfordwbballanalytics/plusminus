import openpyxl, os, numpy
import pandas as pd

os.chdir('../pbp_files')

pd.set_option('expand_frame_repr', False)

off_pos_l = ['TURNOVR', 'GOOD!', 'FOUL', 'MISSED']
def_pos_l = ['REBOUND (DEF)', 'STEAL']

op_pos_l = ['TURNOVR', 'GOOD!', 'FOUL']

files = [ f for f in os.listdir( os.curdir ) if os.path.isfile(f) ]

poss_by_game = {}

for file in files:
    if '.xlsx' in file and 'lock' not in file:

        print file
        wb = openpyxl.load_workbook(file)

        ws = wb.get_active_sheet()
        df = pd.DataFrame(ws.values)

        s, o = 4, 0 #indexing for stanford and opponent columns
        if 'Stanford' in df.ix[5,0]:
            s, o = o, s

        idx = numpy.where(df.ix[:,0].str.contains('------')==True)[0]
        idx = numpy.append(idx, len(df))

        intervals = [(i+1, j-1) for i, j in zip(idx[0:len(idx)], idx[1:])]

        currentperiod =0

        h = ['off_pos', 'def_pos', 'time', 'period']
        rows = []

        for interval in intervals:

            currentperiod =currentperiod +1
            period_df = df.ix[interval[0]:interval[1]]


            #separate by minutes:
            for min, min_df in period_df.groupby(1):
                time = min_df.ix[:,1].tolist()[0]

                stanford_row = min_df.ix[:,s].tolist()
                opponent_row = min_df.ix[:,o].tolist()

                if len(stanford_row) == stanford_row.count(None):


                    #if opponents committed a foul, turnover, or scored a point then stanford ends defensive possession
                    if [i for e in op_pos_l for i in opponent_row if (isinstance(i, unicode) or isinstance(i, str))and e in i]:

                        rows.append([0,1,time, currentperiod])

                else:

                    #check if end to offensive posession:
                    if [i for e in off_pos_l for i in stanford_row if (isinstance(i, unicode) or isinstance(i, str)) and e in i]:

                        rows.append([1,0,time, currentperiod])

                    #If There's a turnovr on the opponent's cell for a steal, if not, then we don't count it
                    else:

                        def_pos = [i for e in def_pos_l for i in stanford_row if (isinstance(i, unicode) or isinstance(i, str)) and e in i]

                        if def_pos:
                            if ['STEAL' for i in def_pos if 'STEAL' in i]: #account for the edge case where a turnover and steal is not recorded within on the same clock
                                if opponent_row.count(None) >0:

                                    pass
                                else:
                                     rows.append([0,1,time, currentperiod])
                            else:
                                rows.append([0,1,time, currentperiod])

        total_df = pd.DataFrame(rows, columns = h)
        total_df = total_df.sort(['period', 'time'], ascending=[1, 0])
        total_df.to_csv('../possession_tables/' + file.split('.xlsx')[0] + "_possession_table.csv", )
