import pandas as pd
import streamlit as st 


def top_locations(violations_df : pd.DataFrame, threshold=1000) -> pd.DataFrame:
    '''
    Return a dataframe of the locations of parking tickets with $1,000 or more in total aggregate violation amounts.  
    This dataframe is keyed on location (1 row per location) and has two columns: location and amount.  
    There should be 135 rows in this dataframe.
    '''
    pivot_df = violations_df.pivot_table(index='location', values='amount', aggfunc='sum')
    top_df = pivot_df[pivot_df['amount'] >= threshold]
    top_df = top_df.sort_values('amount', ascending=False)
    top_df['location'] = top_df.index
    top_df = top_df.reset_index(drop=True)
    return top_df


def top_locations_mappable(violations_df : pd.DataFrame, threshold=1000) -> pd.DataFrame:
    '''
    get top locations then add lat and long from the original dataframe.  
    Again this dataframe is keyed on location (1 row per location) and 4 columns: location, lat, lon, amount  
    Make sure you have the same number of rows as the top_locations dataframe
    '''

    top_df = top_locations(violations_df, threshold)
    combined = pd.merge(top_df, violations_df, left_on='location', right_on='location')
    top_loc_df = combined[['location', 'amount_x', 'lat', 'lon']]
    top_loc_dedupe_df = top_loc_df.drop_duplicates(subset='location')
    top_loc_dedupe_df = top_loc_dedupe_df.rename(columns={'amount_x': 'amount'})
    return top_loc_dedupe_df




def tickets_in_top_locations(violations_df : pd.DataFrame, threshold=1000) -> pd.DataFrame:

    '''
    Return a dataframe of the parking tickets that were issued in the top locations.  
    This dataframe is keyed on ticket number and has the same columns as the original dataframe.  
    It should just be a subset of the original dataframe where the location one of the top locations.  
    There should be 8,109 rows in this dataframe.
    '''

    top = top_locations(violations_df, threshold)
    del top['amount']
    combined = pd.merge(top, violations_df, left_on='location', right_on='location')

    return combined

if __name__ == '__main__':
    '''
    Main ETL job. 
    '''
    import streamlit as st
    import pandas as pd
    df = pd.read_csv('./cache/final_cuse_parking_violations.csv')
    top = top_locations(df)
    top.to_csv('./cache/top_locations.csv', index=False)
    top_map = top_locations_mappable(df)
    top_map.to_csv('./cache/top_locations_mappable.csv', index=False)
    top_tickets = tickets_in_top_locations(df)
    top_tickets.to_csv('./cache/tickets_in_top_locations.csv', index=False)
    st.write(top_map)