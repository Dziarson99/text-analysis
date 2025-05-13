
from functools import reduce
from collections import Counter
import re
import json
import csv
import matplotlib.pyplot as plt

# Lista słów uznanych za niecenzuralne
swear_words = {
    'kurwa', 'kurwy', 'kurwie', 'kurwą', 'kurwę',
    'chuj', 'chuja', 'chujowi', 'chujem', 'chujowy', 'chujowa', 'chujowe',
    'pierdolić', 'pierdoli', 'pierdolę', 'pierdolą', 'pierdolił', 'pierdolony', 'pierdolona',
    'jebany', 'jebana', 'jebane', 'jebani', 'jebane', 'jebac', 'jebać', 'jebie', 'jebią', 'jebał', 'jebłem',
    'pojebany', 'pojebana', 'pojebane', 'pojebani', 'pojebem', 'pojeb',
    'skurwysyn', 'skurwysyna', 'skurwysynem', 'skurwysyni',
    'mać',
    'dziwka', 'dziwki', 'dziwką', 'dziwek',
    'huja', 'huj', 'hujowi', 'hujem',
    'dupa', 'dupy', 'dupie', 'dupą',
    'zajebisty', 'zajebista', 'zajebiste', 'zajebiście',
    'ciul', 'ciula', 'ciulu',
    'szmata', 'szmatą', 'szmaty', 'szmat'
}

# Czyszczenie tekstu i zamiana na listę słów
def clean_and_split(text):
    return list(
        map(str.lower,
            filter(lambda w: w, re.split(r'\W+', text)))
    )

# Filtrowanie przekleństw
def filter_swears(words):
    return list(filter(lambda w: w not in swear_words, words))

# Mapowanie długości słów
def map_word_lengths(words):
    return list(map(len, words))

# Zliczanie wystąpień słów
def count_words(words):
    return Counter(words)

# Statystyki tekstu
def text_statistics(words):
    total_words = len(words)
    unique_words = len(set(words))
    avg_length = sum(map(len, words)) / total_words if total_words else 0
    return {
        "total_words": total_words,
        "unique_words": unique_words,
        "average_word_length": round(avg_length, 2)
    }

# Eksport danych do CSV
def export_to_csv(counter, filename):
    with open(filename, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Word", "Count"])
        for word, count in counter.items():
            writer.writerow([word, count])

# Eksport danych do JSON
def export_to_json(data, filename):
    with open(filename, "w", encoding="utf-8") as jsonfile:
        json.dump(data, jsonfile, indent=4)

# Zapis przefiltrowanego tekstu do pliku
def save_cleaned_text(text, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)

# Wykres najczęstszych słów
def plot_top_words(counter, top_n=10):
    top_items = counter.most_common(top_n)
    words, counts = zip(*top_items)
    plt.figure(figsize=(10, 6))
    plt.bar(words, counts, color='skyblue')
    plt.title(f"Top {top_n} najczęściej występujących słów")
    plt.ylabel("Liczba wystąpień")
    plt.xlabel("Słowo")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("top_words_plot.png")
    plt.close()

# Przykładowy tekst
if __name__ == "__main__":
    text = """
    Wczoraj na jednym z osiedli doszło do niecodziennej sytuacji. Pewien mężczyzna, jak twierdzą świadkowie, zaczął wrzeszczeć: „Kurwa, znowu nie działa ten jebany domofon!”. Po chwili dodał: „Co za chuj go projektował, przecież to jakiś pierdolony absurd!”.
    Zdarzenie przyciągnęło uwagę mieszkańców, którzy już wcześniej skarżyli się na problemy z urządzeniem. „To nie pierwszy raz, jak muszę dzwonić do zarządcy. Wszystko mają w dupie”, mówi pani Anna z trzeciego piętra.
    Władze spółdzielni odmówiły komentarza, ale zapowiedziały wewnętrzne postępowanie. Nie wiadomo jednak, czy coś się zmieni. „To po prostu pojebany system, nikt tu za nic nie odpowiada” – dodał jeden z lokatorów, wyraźnie poirytowany.
    Sprawa wzbudziła emocje także w lokalnych mediach społecznościowych. „Może w końcu ktoś się tym jebanym problemem zajmie!” – napisał jeden z internautów.
    """

    words = clean_and_split(text)
    clean_words = filter_swears(words)
    word_lengths = map_word_lengths(clean_words)
    word_count = count_words(clean_words)
    stats = text_statistics(clean_words)

    cleaned_text = ' '.join(clean_words)
    print("\n📜 Przefiltrowany tekst (bez przekleństw):\n", cleaned_text)

    export_to_csv(word_count, "word_counts.csv")
    export_to_json(stats, "text_stats.json")
    plot_top_words(word_count)
    save_cleaned_text(cleaned_text, "cleaned_text.txt")

    print("\nStatystyki tekstu:", stats)
    print("Top 5 słów:", word_count.most_common(5))
