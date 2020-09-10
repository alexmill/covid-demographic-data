import pandas as pd
import numpy as np
import datetime as dt
import us

def get_age_bucket(r):
    r = r.lower()
    r = r.replace('_plus','+').replace('plus', '+')
    r = r.replace('+','-100')
    r = r.replace('age_17', '[0-17]')
    r = r.replace('age_64', '[64-100]')
    r = r.replace('under 20', '[0-20]')
    r = r.replace('fatality', '')
    if 'avrg' in r or 'range' in r:
        return('')
    if 'unk' in r:
        return('unknown')
    if '[' in r:
        rng = r.split('[')[1].split(']')[0]
    elif 'age' in r:
        if 'age_' not in r:
            r = r.replace('age', 'age_')
        rng = r.split('age_')[1]
        if '-' not in rng:
            rng = rng.replace('_','-')
        else:
            return(rng)
    else:
        rng = r

    if '-' in rng:
        lo,hi = rng.split('-')
    elif '<' in rng:
        lo = 0
        hi = rng.split('<')[1]
    else:
        return(rng)
    
    #return((lo, hi))
    return(f'{lo}-{hi}')


def AL_formatter(state_raw, metric='cases'):
    state_raw = pd.DataFrame(state_raw)
    df = state_raw.loc[pd.isnull(state_raw['County Name']),:].sort_values('Scrape Time').reset_index(drop=True)
    df = df[['Scrape Time'] + df.columns[df.columns.str.contains('Age')].tolist()]
    df['date'] = pd.to_datetime(df['Scrape Time']).dt.date
    df = df.loc[~pd.isnull(df.date),:].drop(columns=['Scrape Time'])

    if metric=='cases':
        df = df[['date'] + df.columns[df.columns.str.contains('Cases')].tolist()]
    elif metric=='deaths':
        df = df[['date'] + df.columns[df.columns.str.contains('Deaths')].tolist()]

    df = df.set_index('date')
    df = df.drop_duplicates(keep='last')
    buckets = pd.Series(pd.Series(df.columns).apply(get_age_bucket).unique())
    df.columns = buckets.tolist()
    df = df.astype(np.int32, errors='ignore')
    return(df)


def GA_formatter(state_raw, metric='cases'):
    df = pd.DataFrame(state_raw)
    df['date'] = pd.to_datetime(df['Report Date']).dt.date

    if metric=='cases':
        df = df[['date', 'Report Date'] + [c for c in df.columns if 'Cases Age' in c]]
        df = df.sort_values(['date', '# Cases Age [0-1]', '# Cases Age [0-17]'])

    elif metric=='deaths':
        df = df[['date', 'Report Date'] + [c for c in df.columns if 'Deaths Age' in c]]
        df = df.sort_values(['date', '# Deaths Age [0-1]', '# Deaths Age [0-17]'])
    
    df = df.drop_duplicates(subset='date',keep='first')
    df = df.set_index('date')
    df = df.drop(columns=(['Report Date'] + df.columns[df.columns.str.contains('Missing/Unknown')].tolist() ))
    buckets = pd.Series(pd.Series(df.columns).apply(get_age_bucket).unique())
    df.columns = buckets.tolist()
    df = df.astype(np.int32, errors='ignore')
    return(df)


def CA_formatter(state_raw, metric='cases'):
    Metric = metric.capitalize()
    data = [r for r in state_raw if f'# {Metric} Age [0-17]' in r.keys()]
    df = pd.DataFrame(data)
    df.loc[df['Report Date'].isnull(),'Report Date'] = df.loc[df['Report Date'].isnull(),'Scrape Time']
    df['date'] = pd.to_datetime(df['Report Date'], errors='coerce').dt.date
    df = df.loc[~pd.isnull(df.date),]
    df = df.sort_values(['date', 'Total Cases'])
    case_cols = [c for c in df.columns if f'# {Metric} Age' in c]
    df = df[['date'] + case_cols]
    df = df.drop_duplicates(subset='date', keep='first')
    df = df.loc[df[case_cols].isnull().mean(1)!=1,:]
    df = df.loc[:,df.isnull().mean(0)!=1]
    df = df.loc[df.date>=dt.date(2020,6,29),:]
    df = df.set_index('date')
    buckets = pd.Series(pd.Series(df.columns).apply(get_age_bucket).unique())
    df.columns = buckets.tolist()
    df = df.astype(np.int32, errors='ignore')
    return(df)


def UT_formatter(state_raw, metric='cases'):
    if metric=='deaths':
        return(None)
    
    df = pd.DataFrame(state_raw)
    df['date'] = pd.to_datetime(df['Report Date']).dt.date
    df = df[['date'] + [c for c in df.columns if 'Cases Age' in c]]
    df = df.set_index('date')
    buckets = pd.Series(pd.Series(df.columns).apply(get_age_bucket).unique())
    df.columns = buckets.tolist()
    df = df.astype(np.int32, errors='ignore')
    return(df)


def MD_formatter(state_raw, metric='cases'):    
    df = pd.DataFrame(state_raw)
    df['date'] = pd.to_datetime(df['Report Date']).dt.date
    if metric=='cases':
        df = df[['date'] + [c for c in df.columns if 'Cases Age' in c]]
    elif metric=='deaths':
        df = df[['date'] + [c for c in df.columns if 'Deaths Age' in c]]
    df = df.set_index('date')
    buckets = pd.Series(pd.Series(df.columns).apply(get_age_bucket).unique())
    df.columns = buckets.tolist()
    df = df.astype(np.int32, errors='ignore')
    return(df)


def MN_formatter(state_raw, metric='cases'):    
    df = pd.DataFrame(state_raw)
    df['date'] = pd.to_datetime(df['Report Date']).dt.date
    if metric=='cases':
        df = df[['date'] + [c for c in df.columns if 'Cases Age' in c]]
    elif metric=='deaths':
        df = df[['date'] + [c for c in df.columns if 'Deaths Age' in c]]
    df = df.loc[df.date>dt.date(2020,4,9),:]
    df = df.set_index('date')
    buckets = pd.Series(pd.Series(df.columns).apply(get_age_bucket).unique())
    df.columns = buckets.tolist()
    df = df.astype(np.int32, errors='ignore')

    
    # Turns 5-year buckets into 10-year buckets
    for grp1,grp2 in [
            ('0-4', '5-9'),
            ('10-14', '15-19'),
            ('20-24', '25-29'),
            ('30-34', '35-39'),
            ('40-44', '45-49'),
            ('50-54', '55-59'),
            ('60-64', '65-69'),
            ('70-74', '75-79'),
            ('80-84', '85-89'),
            ('90-94', '95-99')
        ]:
            
        rows = (~pd.isnull(df[grp1]))
        combined = f"{grp1.split('-')[0]}-{grp2.split('-')[1]}"
        df.loc[rows,combined] = df.loc[rows, [grp1, grp2]].sum(1)
        df = df.drop(columns=[grp1, grp2])

    return(df)


def MI_formatter(state_raw, metric='cases'):
    df = pd.DataFrame(state_raw)
    df['date'] = pd.to_datetime(df['Report Date']).dt.date

    if metric=='cases':
        df = df[['date', 'Report Date'] + [c for c in df.columns if 'Cases Age' in c]]
        df = df.sort_values(['date', '# Cases Age [0-19]'])

    elif metric=='deaths':
        df = df[['date', 'Report Date'] + [c for c in df.columns if 'Deaths Age' in c]]
        df = df.sort_values(['date', '# Deaths Age [0-19]'])

    df = df.drop_duplicates(subset='date',keep='first')
    df = df.set_index('date')
    df = df.drop(columns=(['Report Date'] + df.columns[df.columns.str.contains('Missing/Unknown')].tolist() ))
    buckets = pd.Series(pd.Series(df.columns).apply(get_age_bucket).unique())
    df.columns = buckets.tolist()
    df = df.astype(np.int32, errors='ignore')
    return(df)


def OR_formatter(state_raw, metric='cases'):
    df = pd.DataFrame([r for r in state_raw if 'County Name' not in r.keys()])
    df['date'] = pd.to_datetime(df['Scrape Time']).dt.date

    if metric=='cases':
        df = df[['date', 'Scrape Time'] + [c for c in df.columns if 'Cases Age' in c]]
        df = df.sort_values(['date', '# Cases Age [20-29]'])

    elif metric=='deaths':
        df = df[['date', 'Scrape Time'] + [c for c in df.columns if 'Deaths Age' in c]]
        df = df.sort_values(['date', '# Deaths Age [20-29]'])

    df = df.drop_duplicates(subset='date',keep='first')
    df = df.set_index('date')
    df = df.drop(columns=(['Scrape Time'] + df.columns[df.columns.str.contains('Missing/Unknown')].tolist() ))
    buckets = pd.Series(pd.Series(df.columns).apply(get_age_bucket).unique())
    df.columns = buckets.tolist()
    df = df.astype(np.int32, errors='ignore')
    return(df)


def FL_formatter(state_raw, metric='cases'):
    df = pd.DataFrame([r for r in raw_json['USA']['FL'] if 'City Name' not in r.keys()])
    df['county'] = df['County Name'].str.lower().replace({'dade':'miami-dade'})

    # State totals included in report starting 7/17
    statedf = df.loc[df.county=='a state'].copy()
    df = df.loc[df.county!='a state']

    df['date'] = pd.to_datetime(df['Scrape Time']).dt.date

    # Data for Alachua county are missing for 5/8
    #df.loc[df['date']!=dt.date(2020,5,8),:]

    repeated_dates = df.groupby('date')['county'].count().loc[df.groupby('date')['county'].count()>69].index
    for date in repeated_dates:
        latest_scrape = df.loc[df.date==date,'Scrape Time'].unique().max()  
        to_drop = df.loc[(df.date==date) & (df['Scrape Time']!=latest_scrape),:].index
        df = df.drop(to_drop)
    df = df[['date'] + [c for c in df.columns if 'Cases Age' in c]]
    df = df.groupby('date').sum()

    buckets = pd.Series(pd.Series(df.columns).apply(get_age_bucket).unique())
    df.columns = buckets.tolist()
    df = df.astype(np.int32, errors='ignore')
    return(df)


state_functions = {
    'AL': {
        'formatter': AL_formatter,
        'deaths_notes': 'Data are missing for [5-17] age range.'
    }, 
    'CA': {'formatter': CA_formatter},
    'FL': {'formatter': FL_formatter},
    'GA': {'formatter': GA_formatter},
    'UT': {'formatter': UT_formatter},
    'MD': {'formatter': MD_formatter},
    #'MI': {'formatter': MI_formatter}, #bad data
    'MN': {'formatter': MN_formatter},
    'OR': {'formatter': OR_formatter},
}


population_file = pd.read_csv('../data/population-data.csv')
popdf = population_file[['STATE','NAME','SEX','AGE','POPEST2019_CIV']]
popdf = popdf.rename(columns={'POPEST2019_CIV':'POPULATION'})
popdf = popdf.loc[popdf.SEX==0,:].drop(columns=['SEX'])


def get_per_capita_data(ST=None, state_df=None, metric='cases'):
    """
    Takes output of state formatter and returns per-capita data
    and the set of age ranges contained within the data.
    
    Can either pass `state_df` directly or let the function
    call the state formatter automatically.
    """
    
    state_fips = int(us.states.lookup(ST).fips)
    state_fxn = state_functions[ST]['formatter']
    state_pop = popdf.loc[popdf.STATE==state_fips,:]
    
    if type(state_df)==type(None):

        state_raw = raw_json['USA'][ST]
        df = state_fxn(state_raw, metric=metric)
        
    else:
        df = state_df

    row_signatures = pd.Series(df.isnull().T.to_dict(orient='list')).apply(lambda r: tuple(r))
    unique_signatures = row_signatures.unique().tolist()
    row_groups = row_signatures.apply(lambda r: unique_signatures.index(r))


    grp_ranges = []
    for idx, grp in enumerate(row_groups.unique()):
        grouping = df.loc[row_groups==grp,:]
        null_cols = (grouping.isnull().mean(0)==1)
        null_colnames = df.columns[null_cols].tolist()
        group_colnames = sorted([c for c in df.columns if c not in ['unknown'] + null_colnames], key=lambda x:int(x.split('-')[0]))
        grouping = grouping[group_colnames]

        # precise population estimates top out at 84; 85+ is one group
        top_groups = [c for c in grouping.columns if int(c.split('-')[1])>50]
        if len(top_groups)>1:
            lo = int(top_groups[0].split('-')[0])
            hi = 100
            grouping[f'{lo}-{hi}'] = grouping[top_groups].sum(1)
            grouping = grouping.drop(columns=top_groups)

        range_populations = []
        for age_range in grouping.columns:
            lo,hi = [int(a) for a in age_range.split('-')]
            range_population = state_pop.loc[(state_pop.AGE>=lo) & (state_pop.AGE<=hi),'POPULATION'].sum()
            range_populations.append(range_population)
        range_populations = pd.Series(range_populations, index=grouping.columns)
        value_per_k = (grouping/range_populations)*1000

        grp_cols = sorted(value_per_k.columns, key=lambda x:int(x.split('-')[0]))
        if grp_cols not in grp_ranges:
            grp_ranges.append(grp_cols)

        if idx==0:
            formatted_df = value_per_k
        else:
            formatted_df = formatted_df.append(value_per_k)

    sorted_cols = sorted(formatted_df.columns, key=lambda x:int(x.split('-')[0]))
    formatted_df = formatted_df[sorted_cols]

    return(formatted_df, grp_ranges)