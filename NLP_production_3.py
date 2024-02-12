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


def process_column(df, column_index):
    nlp = spacy.load("en_core_web_sm")
    root_list = []
    column_name = df.columns[column_index]
    df = remove_nan_values(df, column_name)

    # for item in df.iloc[:, column_index][:100]:  # Process a subset of the data for testing
    items = df.iloc[:, column_index].tolist()  # Convert column to a list for efficient processing

    for item in items:
        str_item = str(item)
        corrected_str_item = spell_check(str_item)
        lower_str_item = corrected_str_item.lower()
        doc = nlp(lower_str_item)

        for token in doc:
            if token.dep_ == 'ROOT' and token.lemma_ != 'nan':
                root_list.append(token.lemma_)

        '''noun_chunks = list(doc.noun_chunks)
        for chunk in noun_chunks:
            if chunk.root.dep_ == 'ROOT' and chunk.root.lemma_ != 'nan':
                root_list.append(chunk.root.lemma_)'''

    word_freq = Counter(root_list)

    least_common = word_freq.most_common()[:-10-1:-1]  # Get the least frequent words

    print("Frequency of words in root_list:")
    for word, freq in word_freq.items():
        print(word, ":", freq)

    word_cloud = WordCloud(collocations=False, background_color='white').generate_from_frequencies(dict(least_common))
    plt.imshow(word_cloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

    return root_list


def main():
    csv_file = input("Enter the path of the CSV file: ")

    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print("File not found. Please enter a valid path.")
        return

    df = df.replace('\xa0', '', regex=True)

    while True:
        print("\n\nWhich column do you want to process?")
        for i, col in enumerate(df.columns):
            print(f"{i + 1}. {col}")
        print("0. Exit\n\n")

        choice = input("Enter your choice (1, 2, 3, or 0 to exit): ")

        if choice == "0":
            break

        try:
            column_index = int(choice) - 1
            if 0 <= column_index < len(df.columns):
                print(process_column(df, column_index))
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid choice. Please try again.")

    return 0


if __name__ == '__main__':
    main()
