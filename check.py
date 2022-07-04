import argparse
from typing import overload
import pandas as pd
import numpy as np
from datetime import datetime


def parse_arguments():
    now = datetime.now()
    month = str(now.month).zfill(2)
    output_default = f'toggl_overlaps_{now.year}_{month}.csv'

    parser = argparse.ArgumentParser(description='Toggle overlap checker')
    parser.add_argument('input', type=str, help='path to monthly csv export from toggl tracker')
    parser.add_argument('-o', '--output', type=str, default=output_default, help='path for detected overlaps')
    args = parser.parse_args()
    return args.input, args.output


def add_computed_columns(df):
    df['startTimestamp'] = df['Start date'] + ' ' + df['Start time']
    df['startTimestamp'] = np.floor(df['startTimestamp'].apply(lambda x: datetime.fromisoformat(x).timestamp()) / 60)

    df['endTimestamp'] = df['End date'] + ' ' + df['End time']
    df['endTimestamp'] = np.floor(df['endTimestamp'].apply(lambda x: datetime.fromisoformat(x).timestamp()) / 60)


if __name__ == '__main__':
    input_path, output_path = parse_arguments()

    print('Loading data...')
    df = pd.read_csv(input_path)
    
    print('Adding computed columns...')
    add_computed_columns(df)
    
    print('Checking for overlaps...')
    overlap_count = 0
    
    overlaps = []
    for name, group in df.groupby(['User']):
        rows_count = group.shape[0]
        for i in range(rows_count):
            i_row = group.iloc[i]
            for j in range(i + 1, rows_count):
                j_row = group.iloc[j]
                if ((i_row['startTimestamp'] < j_row['endTimestamp']) and (j_row['startTimestamp'] < i_row['endTimestamp'])):
                    overlap_minutes = min(i_row['endTimestamp'], j_row['endTimestamp']) - max(i_row['startTimestamp'], j_row['startTimestamp'])
                    row = [name,
                           i_row['Start date'], 
                           f"{i_row['Start time']} - {i_row['End time']}",
                           f"{j_row['Start time']} - {j_row['End time']}",
                           overlap_minutes]
                    overlaps.append(row)
                    overlap_count += 1
    
    if overlap_count == 0:
        print('\nNo overlaps found, hurray!')
    else:
        print(f'\n{overlap_count} overlaps found :(\nExporting to "{output_path}"...')
        overlaps_df = pd.DataFrame(overlaps, columns=['user', 'day', 'time1', 'time2', 'overlap_minutes'])
        overlaps_df.to_csv(output_path, index=False)
