from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import datetime as dt
import us



def plot_data(ST, metric='cases', count='rate', roll=7, formatted_df=None, grp_ranges=None):
    min_periods = min(roll,int(roll/2)+1)

    if type(formatted_df)==type(None):
        formatted_df, grp_ranges = get_per_capita_data(ST, metric=metric)


    formatted_df.index = pd.to_datetime(sorted(formatted_df.index))
    if count=='rate':
        formatted_df = formatted_df.diff().rolling(f'{roll}d', min_periods=min_periods, closed='both').mean()
    elif count=='total':
        formatted_df = formatted_df.rolling(f'{roll}d', min_periods=min_periods, closed='both').mean()
    if roll>1:
        formatted_df = formatted_df.iloc[:-1*min_periods,:]

    import matplotlib.dates as mdates
    ax = formatted_df.plot()
    #dates = mdates.drange(formatted_df.index[0], formatted_df.index[-1], dt.timedelta(days=30))
    #ax.set_xticks(dates)
    #ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    #plt.xticks(rotation=20)


    handles, labels = ax.get_legend_handles_labels()

    existing_labels = []
    for idx, grp in enumerate(grp_ranges):
        grp_idx = [labels.index(grp[i]) for i in range(len(grp))]
        grp_handles = pd.Series(handles)[grp_idx].tolist()
        grp_labels = pd.Series(labels)[grp_idx].tolist()
        
        grp_handles = [grp_handles[j] for j in range(len(grp_labels)) if grp_labels[j] not in existing_labels]
        grp_labels = [l for l in grp_labels if l not in existing_labels]
        
        existing_labels.extend(grp_labels)

        grp_legend = ax.legend(grp_handles, grp_labels, loc=idx)
        ax.add_artist(grp_legend)

    state_name = us.states.lookup(ST).name
    _ = plt.suptitle(f'{metric.capitalize()} per 1000 by age group: {state_name}', y=0.95, fontsize=14)
    if roll>1:
        _ = plt.title(f'Rolling {roll} day average', fontsize=10)
    else:
        _ = plt.title(f'Per day', fontsize=10)
    #if f'{metric}_notes' in state_functions[ST].keys():
    #    print(state_functions[ST][f'{metric}_notes'])
    
    #return(formatted_df)
