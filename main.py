import sys
import pandas as pd
import datetime

JT_COLUMNS = ['LotNo', 'Estate', 'InvoiceNo', 'Grade', 'Bags', 'NetKgs', 'TotalKgs', 'Price']
GLOBAL_COLUMNS = ["LotNo", "Estate", "Grade", "DQ", "InvoiceNo", "Price", "BUYER", "Bags", "NetKgs", "TotalKgs", "SAMPLE_KGS" ]
CTL_COLUMNS = ['LotNo', 'Estate', 'Grade', 'InvoiceNo', 'Bags', 'TotalKgs', 'Price', 'BUYER']

def get_date():
    x = datetime.datetime.now()
    return x.strftime('%d-%b-%Y')

def pre_process(filepath, broker):
    df = pd.read_excel(filepath, sheet_name=0)
    if broker == 'JT':
        df.drop(df.index[[0,1,2,3]], inplace=True)
        df.columns = JT_COLUMNS
    elif broker == 'GLOBAL':
        df.drop(df.index[[0,1,2]], inplace=True)
        df.columns = GLOBAL_COLUMNS
    elif broker == 'CTL':
        df.drop(df.index[[0]], inplace=True)
        df.columns = CTL_COLUMNS
    else:
        print('ERROR!!!! NO SUCH BROKER')
        return
    return df

def compute_stats(df, MARKS):
    # filter df based on marks
    for MARK in MARKS:
        MARK_LIST = [MARK]
        sub_df = df[df['Estate'].isin(MARK_LIST)]
        sub_df = sub_df[df['Price'] > 0]
        print('\n')
        print('===========================================')
        print(MARK)
        print('===========================================')
        if sub_df.empty:
            print('No Dispatch in this sale')
            continue
        total_bags = sub_df['Bags'].sum()
        total_kgs = sub_df['TotalKgs'].sum()
        avg_price = sub_df['Price'].mean()
        print('Total Bags:' + str(total_bags))
        print('Total Kgs:' + str(total_kgs))
        print('Avg Price:' + str(avg_price))
        print('\n')
        print('+++++++++++++++++')
        print('Grade-Wise Report')
        print('+++++++++++++++++')
        grade_df = sub_df.groupby(['Grade'])
        GRADES = grade_df.groups.keys()
        for grade in GRADES:
            print('\n')
            print('-------')
            print(str(grade))
            stat_df = grade_df.get_group(grade)
            stat_df.drop(columns=['Estate'])
            total_bags = stat_df['Bags'].sum()
            total_kgs = stat_df['TotalKgs'].sum()
            avg_price = stat_df['Price'].mean()
            print('Total Bags:' + str(total_bags))
            print('Total Kgs:' + str(total_kgs))
            print('Avg Price:' + str(avg_price))
        print('\n')
        print('+++++++++++++++++')
        print('  Out Lot Report ')
        print('+++++++++++++++++')
        outlot_df = sub_df[sub_df['Price'] == 0]
        if outlot_df.empty:
            print('No out lot')
        else:
            index = outlot_df.index
            total_lots = len(index)
            total_bags = stat_df['Bags'].sum()
            total_kgs = stat_df['TotalKgs'].sum()
            print('Total Lots:' + str(total_lots))
            print('Total Bags:' + str(total_bags))
            print('Total Kgs:' + str(total_kgs))
            print('\n')
            print('+++++++++++++++++')
            print(' Detailed Report ')
            print('+++++++++++++++++')
            print(outlot_df)

def build_mark_list(filepath, broker):
    df = pre_process(filepath, broker)
    mark_df = df.groupby(['Estate'])
    MARKS = mark_df.groups.keys()
    return MARKS


def build_mark_index(filepath, broker):
    df = pre_process(filepath, broker)
    mark_df = df.groupby(['Estate'])
    MARKS = mark_df.groups.keys()
    index = []
    i = 0
    for MARK in MARKS:
        mark_pair = (str(i), str(MARK))
        index.append(mark_pair)
        i = i + 1
    return index

def get_marks_with_index(filepath, broker, choices):
    MARK_LIST = []
    index = build_mark_index(filepath, broker)
    print(choices)
    for idx in index:
        (a,b) = idx
        if a in choices:
            MARK_LIST.append(b)
    print(MARK_LIST)
    return MARK_LIST


def main_process(filepath, broker, MARKS_LIST):
    broker = str(broker)
    date_postfix =  get_date()
    output_filepath = 'final_report_' + date_postfix + '_' + broker + '.txt'
    sys.stdout = open(output_filepath, 'w')
    print('BROKER: ' + broker)
    df = pre_process(filepath, broker)
    compute_stats(df, MARKS_LIST)
    sys.stdout.close()
    return output_filepath

