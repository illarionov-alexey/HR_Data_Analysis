import pandas as pd
import requests
import os


# scroll down to the bottom to implement your solution

def download_data():
    if not os.path.exists('../Data'):
        os.mkdir('../Data')

    # Download data if it is unavailable.
    if ('A_office_data.xml' not in os.listdir('../Data') and
            'B_office_data.xml' not in os.listdir('../Data') and
            'hr_data.xml' not in os.listdir('../Data')):
        print('A_office_data loading.')
        url = "https://www.dropbox.com/s/jpeknyzx57c4jb2/A_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/A_office_data.xml', 'wb').write(r.content)
        print('Loaded.')

        print('B_office_data loading.')
        url = "https://www.dropbox.com/s/hea0tbhir64u9t5/B_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/B_office_data.xml', 'wb').write(r.content)
        print('Loaded.')

        print('hr_data loading.')
        url = "https://www.dropbox.com/s/u6jzqqg1byajy0s/hr_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/hr_data.xml', 'wb').write(r.content)
        print('Loaded.')

    # All data in now loaded to the Data folder.
    return [pd.read_xml(f) for f in ['../Data/A_office_data.xml', '../Data/B_office_data.xml', '../Data/hr_data.xml']]


def first_stage(d_frames: list[pd.DataFrame], output: bool = False) -> list[pd.DataFrame]:
    A_df, B_df, HR_df = d_frames
    # Reindex all three datasets. It is required because some of the employee_office_id column values for offices A
    # and B match. For HR data, use the employee_id column as the index. For A and B offices, use the name of the office
    # and the employee_office_id column as indexes. For example, for office A, employee #125 will be A125.
    # The offices' data index should resemble HR's data index.
    A_df.set_index(pd.Index([f'A{o_id}' for o_id in A_df.employee_office_id]), inplace=True)
    B_df.set_index(pd.Index([f'B{o_id}' for o_id in B_df.employee_office_id]), inplace=True)
    HR_df.set_index('employee_id', inplace=True)
    # Print three Python lists containing office A, B, and HR data indexes.
    if output:
        print(A_df.index.to_list())
        print(B_df.index.to_list())
        print(HR_df.index.to_list())

    return d_frames


def second_stage(d_frames: list[pd.DataFrame], output: bool = False) -> pd.DataFrame:
    A_df, B_df, HR_df = d_frames
    # Use the concat() function from pandas to generate a unified dataset for offices A and B;
    AB_df = pd.concat([A_df, B_df])
    # Use df.merge() to carry out the left merging of the unified office dataset with HR's dataset. Merge both datasets
    # by index — use left_index and right_index parameters. Set indicator=True in df.merge().
    # For the final table, leave only those employees whose data is contained in both datasets;
    # Drop the employee_office_id, employee_id columns and the new column that contains a row source;
    # Sort the final dataset by index;
    AB_df = AB_df.join(HR_df, how='inner').drop(columns=['employee_office_id']).sort_index()
    # AB_df = AB_df.merge(HR_df,how='left',left_index=True,right_index=True,indicator=True)
    # AB_df = AB_df[AB_df._merge == 'both'].drop(columns=['employee_office_id','_merge']).sort_index()
    if output:
        # Print two Python lists: the final DataFrame index and the column names. Output each list on a separate line.
        print(AB_df.index.to_list())
        print(AB_df.columns.to_list())
    return AB_df


def third_stage(df: pd.DataFrame, output: bool = False) -> pd.DataFrame:
    if output:
        # What are the departments of the top ten employees in terms of working hours?
        print(df.sort_values(by='average_monthly_hours', ascending=False).head(10).Department.to_list())
        # What is the total number of projects on which IT department employees with low salaries have worked?
        print(df[(df.Department == 'IT') & (df.salary == 'low')].number_project.sum())
        # What are the last evaluation scores and the satisfaction levels of the employees A4, B7064, and A3033?
        print(df.loc[['A4', 'B7064', 'A3033'], ['last_evaluation', 'satisfaction_level']].values.tolist())
    return df


def forth_stage(df: pd.DataFrame, output: bool = False) -> pd.DataFrame:
    # the median number of projects the employees in a group worked on, and how many employees worked on more than
    # five projects; the mean and median time spent in the company;
    # the share of employees who've had work accidents;
    # the mean and standard deviation of the last evaluation score.
    d = {'number_project': ['median', ('count_bigger_5', lambda s: s[s > 5].count())],
         'time_spend_company': ['mean', 'median'],
         'Work_accident': ['mean'],
         'last_evaluation': ['mean', 'std']}
    agg = df.groupby(by='left').agg(d).round(2)
    if output:
        print(agg.to_dict())
    return df


def fifth_stage(df: pd.DataFrame, output: bool = False) -> pd.DataFrame:
    df1 = df.pivot_table(index='Department', columns=['left', 'salary'], values='average_monthly_hours',
                         aggfunc='median').round(2)
    df2 = df.pivot_table(index='time_spend_company', columns=['promotion_last_5years'],
                         values=['satisfaction_level', 'last_evaluation'],
                         aggfunc=['max', 'mean', 'min']).round(2)
    if output:
        print(df1[(df1[(0, 'high')] < df1[(0, 'medium')]) | (df1[(1, 'low')] < df1[(1, 'high')])].to_dict())
        print(df2[df2[('mean', 'last_evaluation', 1)] < df2[('mean', 'last_evaluation', 0)]].to_dict())
    return df


if __name__ == '__main__':
    pd.set_option('display.max_columns', 20)
    # write your code here
    fifth_stage(forth_stage(third_stage(second_stage(first_stage(download_data())))), True)
