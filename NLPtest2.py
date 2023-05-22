import pandas as pd
import spacy 

def csv_column_one(df):
    for item in df.iloc[:, 0]:
        data_type = type(item)

    return print(data_type)


def csv_column_two(df):
    for item in df.iloc[:, 1]:
        # Do something with the item in the first column
        print(item)

    return


def csv_column_three(df):
    for item in df.iloc[:, 2]:
        # Do something with the item in the third column
        print(item)

    return


def main():
    # Reading the csv file
    df = pd.read_csv('10-Reflection Survey Student Analysis Report.csv')
    # Replacing the blank spaces after sentence
    df = df.replace('\xa0', '', regex=True)
    csv_column_one(df)

    return 0


if __name__ == '__main__':
    main()
