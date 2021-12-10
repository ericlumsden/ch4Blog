import pandas as pd
import matplotlib.pyplot as plt

mlo = pd.read_csv("ch4_mlo_surface-insitu_1_ccgg_DailyData_matrix.txt", delim_whitespace=True)
brw = pd.read_csv("ch4_brw_surface-insitu_1_ccgg_DailyData_matrix.txt", delim_whitespace=True)

# Let's combine the values and their standard deviations for each sampling site into one dataframe
graph_set = mlo[['year', 'month', 'day', 'value', 'value_std_dev']].copy()
graph_set = graph_set.set_axis(['year', 'month', 'day', 'mlo_value', 'mlo_std_dev'], axis=1, inplace=False)
graph_set[['brw_value', 'brw_std_dev']] = brw[['value', 'value_std_dev']].copy()
graph_set['brw_qcflag'] = brw.qcflag
graph_set['mol_qcflag'] = mlo.qcflag
# There are instances in which the readings are wrong/erroneous, let's remove those
graph_set = graph_set[graph_set.mlo_value != -999.99]
graph_set = graph_set[graph_set.brw_value != -999.99]
graph_set.loc[graph_set.mol_qcflag == '*..', 'mlo_value'] = 'NaN'
graph_set.loc[graph_set.brw_qcflag == '*..', 'brw_value'] = 'NaN'
# Let's make some rows showing % changes of the methane values measured
graph_set['mlo_per'] = 100 * (graph_set['mlo_value'] - graph_set['mlo_value'].iloc[0]) / graph_set['mlo_value'].iloc[0]
graph_set['brw_per'] = 100 * (graph_set['brw_value'] - graph_set['brw_value'].iloc[0]) / graph_set['brw_value'].iloc[0]

# Now, plot them together
fig, ax = plt.subplots()
ax.plot(graph_set['year'], graph_set['mlo_value'], label='MLO', color='g')
#ax.fill_between(graph_set['year'], graph_set['mlo_value']-graph_set['mlo_std_dev'], graph_set['mlo_value']-graph_set['mlo_std_dev'], color='g', alpha=0.4)
ax.plot(graph_set['year'], graph_set['brw_value'], label='BRW', color='b')
#ax.fill_between(graph_set['year'], graph_set['brw_value']-graph_set['brw_std_dev'], graph_set['brw_value']-graph_set['brw_std_dev'], color='g', alpha=0.4)
# Let's look at the average value between the two readings, too
ax.plot(graph_set['year'], (graph_set['mlo_value']+graph_set['brw_value'])/2, label='AVG', color='r', alpha=0.5)
plt.xlabel('year')
plt.ylabel('dry-air mole fraciton')
plt.legend()
for ymaj in ax.yaxis.get_majorticklocs():
    ax.axhline(y=ymaj, ls='--', color='grey')
for x in ['top', 'right']:
    ax.spines[x].set_visible(False)

plt.savefig('methane_changes.png')

# Let's make a second that more clearly shows the average
fig2, ax2 = plt.subplots()
ax2.plot(graph_set['year'], graph_set['mlo_value'], label='MLO', color='g', alpha=0.4)
ax2.plot(graph_set['year'], graph_set['brw_value'], label='BRW', color='b', alpha=0.4)
ax2.plot(graph_set['year'], (graph_set['mlo_value']+graph_set['brw_value'])/2, label='AVG', color='r', alpha=1.)
plt.xlabel('year')
plt.ylabel('dry-air mole fraciton')
plt.legend()
for ymaj in ax2.yaxis.get_majorticklocs():
    ax2.axhline(y=ymaj, ls='--', color='grey')
for x in ['top', 'right']:
    ax2.spines[x].set_visible(False)


plt.savefig('methane_changes_avg.png')

# Now, let's make a final graph that shows % change
fig3, ax3 = plt.subplots()
ax3.plot(graph_set['year'], graph_set['mlo_per'], label='MLO', color='g', alpha=0.4)
ax3.plot(graph_set['year'], graph_set['brw_per'], label='BRW', color='b', alpha=0.4)
ax3.plot(graph_set['year'], (graph_set['mlo_per']+graph_set['brw_per'])/2, label='AVG', color='r', alpha=1.)
plt.xlabel('year')
plt.ylabel(f"% change since {graph_set['year'].iloc[0]}-{graph_set['month'].iloc[0]}-{graph_set['day'].iloc[0]}")
plt.legend()
for ymaj in ax3.yaxis.get_majorticklocs():
    ax3.axhline(y=ymaj, ls='--', color='grey')
for x in ['top', 'right']:
    ax3.spines[x].set_visible(False)


plt.savefig('methane_changes_per.png')
