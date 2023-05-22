import pandas as pd
import spacy
from spacy import displacy


def csv_column_one(df):
    nlp = spacy.load("en_core_web_sm")
    root_list = []

    for item in df.iloc[:, 0]:
        str_item = str(item)
        doc = nlp(str_item)

        for token in doc:
            if token.dep_ == 'ROOT':
                root_list.append(token.text)


def csv_column_two(df):
    nlp = spacy.load("en_core_web_sm")
    root_list = []

    for item in df.iloc[:, 1]:
        str_item = str(item)
        doc = nlp(str_item)

        for token in doc:
            if token.dep_ == 'ROOT':
                root_list.append(token.text)

    return print(root_list)


def csv_column_three(df):
    nlp = spacy.load("en_core_web_sm")
    root_list = []

    for item in df.iloc[:, 0]:
        str_item = str(item)
        doc = nlp(str_item)

        for token in doc:
            if token.dep_ == 'ROOT':
                root_list.append(token.text)

    return print(root_list)


def main():
    df = pd.read_csv('10-Reflection Survey Student Analysis Report.csv')
    df = df.replace('\xa0', '', regex=True)

    csv_column_one(df)
    return 0


if __name__ == '__main__':
    main()
