import pandas as pd
import numpy as np

# Generate data frame from csv file.
df = pd.read_csv('TestData-20210319.csv') 

# Generate table 1:
table1 = pd.pivot_table(df, values='TotMins', index=['Item'], columns=['State'], aggfunc=np.sum,
                        margins=True, margins_name='GrandTotal')
table1 = table1.sort_values(by='GrandTotal', ascending=False)
print('-------TABLE 1-------')
print(table1)
print('---------------------')

# Generate table 2: (Unfinished)
table2 = pd.pivot_table(df, values=['TotMins'], index=['ItemGroup', 'Item'], columns=['State'], aggfunc=np.sum,
                        margins=True, margins_name='GrandTotal')

print('-------TABLE 2-------')
print(table2)
print('---------------------')

# Generate table 3:
# Generate dataframe with Item04:
df_table3 = df[df['Item'] == 'Item04']

# Generate the first section of the table (Total Mins of Item04 trended by week):
table3_1 = pd.pivot_table(df_table3, values='TotMins', index='Week', columns='State', aggfunc=np.sum,
                          margins=True, margins_name='GrandTotal')

# Edit the table index name:
table3_1 = table3_1.reset_index()
table3_1 = table3_1.replace('GrandTotal', 'Total TotMins')
table3_1 = table3_1.set_index('Week')

# Generate second section of the table (% of Mins by state):
# Create a table skeleton:
table3_2 = table3_1.copy()
table3_2 = table3_2.drop(table3_2.index[:])

# Variables needed for the loop:
step = 0
p1 = ''
p2 = ''
p3 = ''
p4 = ''

# Loop through the table to calculate percentage of each cell.
while step < len(table3_1.index):
    p1 = str(round(table3_1['State1'].iloc[step] / table3_1['GrandTotal'].iloc[step] * 100)) + '%'
    p2 = str(round(table3_1['State2'].iloc[step] / table3_1['GrandTotal'].iloc[step] * 100)) + '%'
    p3 = str(round(table3_1['State3'].iloc[step] / table3_1['GrandTotal'].iloc[step] * 100)) + '%'
    p4 = str(round(table3_1['State4'].iloc[step] / table3_1['GrandTotal'].iloc[step] * 100)) + '%'
    table3_2 = table3_2.append({'State1': p1, 'State2': p2, 'State3': p3, 'State4': p4,
                                'GrandTotal': '100%'}, ignore_index=True)
    step = step + 1

# Edit second section of the table
table3_2['Week'] = table3_1.reset_index()['Week']
table3_2 = table3_2.replace('Total TotMins', 'Total % of Mins by State')
table3_2 = table3_2.set_index('Week')

# Concatenate two sections:
table3 = pd.concat([table3_1, table3_2])

#Rearrange the rows:
total_totmins = table3.loc['Total TotMins']
table3 = table3.drop('Total TotMins', axis=0)
table3 = table3.append(total_totmins)

print('-------TABLE 3-------')
print(table3)
print('---------------------')

# Generate table 4:
# Generate corresponding dataframe for the table: 
df_table4 = df[df['Item'] == 'Item07'][df['State'] == 'State4']
df_table4['Mins/Psn'] = df_table4['TotMins'] / df_table4['TotPeople']

# Create the table:
table4 = df_table4.pivot_table(values='Mins/Psn', index='Week', columns='Market', aggfunc=np.average,
                               margins=True, margins_name='GrandTotal')

print('-------TABLE 4-------')
print(table4)
print('---------------------')

# Generate table 5:
# Generate corresponding dataframe for the table:
mk9_gr2 = df[df['Market'] == 'Market09'][df['ItemGroup'] == 'ItemGroup2']

#Create table:
table5 = mk9_gr2.pivot_table(values='TotPeople', index='Week', columns='TimeOfActivity', aggfunc=np.sum,
                             margins=True, margins_name='GrandTotal')

print('-------TABLE 5-------')
print(table5)
print('---------------------')

# Generate table 6:
# Reuse the data from table 5:
table6 = table5.copy()

# Combine corresponding columns together:
table6['M-F'] = table5['M-F Afternoon'] + table5['M-F Morning']
table6['S&S'] = table5['S&S Afternoon'] + table5['S&S Morning']

# Drop old columns:
table6.drop(['M-F Afternoon', 'M-F Morning', 'S&S Afternoon', 'S&S Morning'], axis=1, inplace=True)

# Reorder the columns:
table6 = table6[['M-F', 'S&S', 'GrandTotal']]

print('-------TABLE 6-------')
print(table6)
print('---------------------')

# Generate table 7:
# Reuse data from table 6 and store them into a temporary table:
table7 = table6.copy().drop('GrandTotal', axis=1)
table7.drop('GrandTotal', inplace=True)
table7 = table7.reset_index()

# Create new table skeleton:
table_7 = table7.copy()
table_7 = table_7.reset_index()
table_7 = table_7.drop(table_7.index[:])

# Variables needed for the loop
finished = False
index = table7.index
sum_mf = 0
sum_ss = 0
avg_mf = 0
avg_ss = 0
i = 0
count = 0

# Loop through the rows and columns of the temporary table to gather necessary data.
# Perform calculation on each data.
# Generate data onto the skeleton table.
while i < len(index):
    sum_mf = sum_mf + table7['M-F'].iloc[i]
    sum_ss = sum_ss + table7['S&S'].iloc[i]
    count = count + 1
    i = i + 1
    if count == 4:
        avg_mf = round(sum_mf / 4)
        avg_ss = round(sum_ss / 4)

        table_7 = table_7.append({'Week': '4Wk to ' + table7['Week'].iloc[i - 1], 'M-F': avg_mf, 'S&S': avg_ss,
                                  'GroundTotal': avg_ss + avg_mf},
                                 ignore_index=True)
        sum_mf = 0
        sum_ss = 0
        avg_mf = 0
        avg_ss = 0
        i = i - 3
        count = 0

# Edit the table:
table_7 = table_7.drop(['index'], axis=1)
table_7 = table_7.set_index('Week')

print('-------TABLE 7-------')
print(table_7)
print('---------------------')
