import pandas as pd
import spacy


def csv_data_str(df, n):
    # Replacing the blank spaces after sentence
    df = df.replace('\xa0', '', regex=True)

    col = [''] * n
    for i in range(n):
        # Isolating column 1 from the csv file as a string
        csv_column = (df[df.columns[i]].to_numpy()).tolist()

        list_to_str = ' # '.join(map(str, csv_column))
        col[i] += list_to_str
    return col


def main():
    # Reading the csv file
    df = pd.read_csv('10-Reflection Survey Student Analysis Report.csv')
    n = len(df.columns)
    all_columns = csv_data_str(df, n)

    for i in range(n):
        print("This is column", i + 1, ":", all_columns[i], "\n")

    return 0


if __name__ == '__main__':
    main()
