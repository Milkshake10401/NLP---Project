import pandas as pd
import spacy
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from autocorrect import Speller


def remove_nan_values(df, column_name):
    df[column_name].dropna(inplace=True)

    return df


def spell_check(text):
    spell = Speller(lang='en')
    corrected_text = spell(text)

    return corrected_text


def csv_column_one(df):
    nlp = spacy.load("en_core_web_sm")
    root_list = []

    column_name = df.columns[0]  # Assuming you want to remove NaN values from the first column

    # Remove NaN values from the specified column
    df = remove_nan_values(df, column_name)

    for item in df.iloc[:, 0]:
        str_item = str(item)
        corrected_str_item = spell_check(str_item)  # Spell check the text
        lower_str_item = corrected_str_item.lower()
        doc = nlp(lower_str_item)

        for token in doc:
            if token.dep_ == 'ROOT' and token.lemma_ != 'nan':
                root_list.append(token.lemma_)
    word_freq = Counter(root_list)

    print("Frequency of words in root_list:")
    for word, freq in word_freq.items():
        print(word, ":", freq)

    word_cloud = WordCloud(collocations=False, background_color='white').generate(' '.join(root_list))
    plt.imshow(word_cloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

    return root_list


def csv_column_two(df):
    nlp = spacy.load("en_core_web_sm")
    root_list = []

    column_name = df.columns[1]  # Assuming you want to remove NaN values from the first column

    # Remove NaN values from the specified column
    df = remove_nan_values(df, column_name)

    for item in df.iloc[:, 1]:
        str_item = str(item)
        corrected_str_item = spell_check(str_item)  # Spell check the text
        lower_str_item = corrected_str_item.lower()
        doc = nlp(lower_str_item)

        for token in doc:
            if token.dep_ == 'ROOT' and token.lemma_ != 'nan':
                root_list.append(token.lemma_)
    word_freq = Counter(root_list)

    print("Frequency of words in root_list:")
    for word, freq in word_freq.items():
        print(word, ":", freq)

    word_cloud = WordCloud(collocations=False, background_color='white').generate(' '.join(root_list))
    plt.imshow(word_cloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

    return root_list


def csv_column_three(df):
    nlp = spacy.load("en_core_web_sm")
    root_list = []

    column_name = df.columns[2]  # Assuming you want to remove NaN values from the first column

    # Remove NaN values from the specified column
    df = remove_nan_values(df, column_name)

    for item in df.iloc[:, 2]:
        str_item = str(item)
        corrected_str_item = spell_check(str_item)  # Spell check the text
        lower_str_item = corrected_str_item.lower()
        doc = nlp(lower_str_item)

        for token in doc:
            if token.dep_ == 'ROOT' and token.lemma_ != 'nan':
                root_list.append(token.lemma_)
    word_freq = Counter(root_list)

    print("Frequency of words in root_list:")
    for word, freq in word_freq.items():
        print(word, ":", freq)

    word_cloud = WordCloud(collocations=False, background_color='white').generate(' '.join(root_list))
    plt.imshow(word_cloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

    return root_list


def main():
    df = pd.read_csv('10-Reflection Survey Student Analysis Report.csv')
    df = df.replace('\xa0', '', regex=True)

    while True:

        print("Which column do you want to process?")
        print("1. First Column")
        print("2. Second Column")
        print("3. Third Column")
        print("0. Exit")

        choice = input("Enter your choice (1, 2, 3, or 0 to exit): ")

        if choice == "1":
            print(csv_column_one(df))
        elif choice == "2":
            print(csv_column_two(df))
        elif choice == "3":
            print(csv_column_three(df))
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")

    return 0


if __name__ == '__main__':
    main()
