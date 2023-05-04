import nltk
from nltk.corpus import words, brown
from nltk.probability import FreqDist
from matplotlib import pyplot as plt

from GetUsedWords import extract_used_words


"""
[('a', 3905), ('e', 3506), ('r', 2542), ('o', 2334), ('i', 2286), ('s', 2035), ('l', 1975), ('t', 1953), ('n', 1928), ('u', 1604), ('c', 1327), ('y', 1263), ('d', 1175), ('h', 1144), ('m', 1109), ('p', 1032), ('b', 958), ('g', 904), ('k', 756), ('f', 526), ('w', 520), ('v', 397), ('z', 218), ('j', 171), ('x', 166), ('q', 71)]
[('a', 3905), ('e', 2435), ('o', 1702), ('i', 1544), ('r', 1446), ('s', 1193), ('t', 1140), ('u', 1116), ('n', 1049), ('l', 1017), ('y', 810), ('c', 748), ('d', 679), ('h', 644), ('p', 583), ('m', 573), ('b', 507), ('g', 495), ('k', 397), ('f', 334), ('w', 289), ('v', 201), ('z', 114), ('x', 98), ('j', 85), ('q', 44)]
"""

def get_filtered_sorted_words(used_words):
    # Download the necessary resources
    nltk.download('words')
    nltk.download('brown')

    # Get all 5-letter words in the English dictionary
    all_words = words.words()
    # remove all words where the first letter is capitalized
    five_letter_words = [word for word in all_words if len(word) == 5 and word[0].islower()]

    # Remove words that have been used before
    remaining_words = set(five_letter_words) - set(used_words)

    # Get the usage frequency of words in the English language
    freq_dist = FreqDist(word.lower() for word in brown.words())

    # Sort remaining words by their usage frequency in the English language
    sorted_words = sorted(remaining_words, key=lambda x: freq_dist[x], reverse=True)

    return sorted_words


def get_word_stats(words):
    # Get the usage frequency of words in the English language
    freq_dist = FreqDist(word.lower() for word in brown.words())
    sorted_words = sorted(words, key=lambda x: freq_dist[x], reverse=True)

    # Get the commonness of each letter in this list of words
    letter_freq = {}
    for word in sorted_words:
        for letter in word:
            letter = letter.lower()
            if letter not in letter_freq:
                letter_freq[letter] = 0
            letter_freq[letter] += 1

    # print the sorted letter frequency
    print(sorted(letter_freq.items(), key=lambda x: x[1], reverse=True))
    # plot the letter frequencies in a barchart sorted by frequency
    plt.bar(list(letter_freq.keys()), list(letter_freq.values()))
    # add a title to the chart
    plt.title('Letter frequency')
    # save the figure
    plt.savefig('letter_freq.png')
    plt.close()

    # Get the non-overlapping frequency of each letter in this list of words
    new_freq_dist = {}
    checked_words = set()
    for letter in sorted(letter_freq, key=letter_freq.get, reverse=True):
        new_freq_dist[letter] = letter_freq[letter]
        for word in sorted_words:
            if word in checked_words:
                continue
            checked_words.add(word)
            if letter in word:
                for other_letter in word:
                    other_letter = other_letter.lower()
                    if other_letter != letter:
                        letter_freq[other_letter] = max(0, letter_freq[other_letter] - 1)
    # plot the letter frequencies in a new bar chart
    # close any prev figs
    plt.bar(list(new_freq_dist.keys()), list(new_freq_dist.values()))
    # add a title to the chart
    plt.title('Non-overlapping letter frequency')
    # save the figure
    plt.savefig('non_overlapping_letter_freq.png')
    plt.close()

    # Print the commonness of each letter where the most common letter is first
    print(sorted(new_freq_dist.items(), key=lambda x: x[1], reverse=True))
    return new_freq_dist


def get_best_starting_word(letter_freq, usable_words):
    best_word = ''
    best_score = 0
    word_scores = {}

    for word in usable_words:
        if word.lower() in word_scores:
            continue
        unique_letters = set(word.lower())
        score = sum(letter_freq.get(letter, 0) for letter in unique_letters)
        word_scores[word] = score
        if score > best_score:
            best_word = word
            best_score = score

    # plot the best 15 words in a barchart
    # sort them first so we know they are the best
    word_scores = dict(sorted(word_scores.items(), key=lambda x: x[1], reverse=True))
    plt.bar(list(word_scores.keys())[:15], list(word_scores.values())[:15])
    # put the scores in the chart and rotate them so they are legible
    # shift them over so they are over their bar chart instead of to the right of it
    for i, v in enumerate(list(word_scores.values())[:15]):
        plt.text(i, v, str(v), color='black', rotation=-60, ha='center', va='bottom')

    # rotate the words on the x axis so they are legible
    plt.xticks(rotation=90)
    # add a title to the chart
    plt.title('Word scores\n')
    # save the figure
    plt.savefig('word_scores.png')
    plt.close()

    return best_word


if __name__ == '__main__':
    # Example usage
    used_words = extract_used_words('https://www.stadafa.com/2021/09/every-worlde-word-so-far-updated-daily.html')
    filtered_sorted_words = get_filtered_sorted_words(used_words)
    # split the words at the 80% mark to see where a reasonable wordle split might be.
    # print the 20 words before the split and the 20 words after the split.
    split = int(len(filtered_sorted_words) * 0.60)
    print(filtered_sorted_words[split - 20:split + 20])
    letter_freq = get_word_stats(filtered_sorted_words[:split])
    print(get_best_starting_word(letter_freq, filtered_sorted_words[:split]))
    # print(filtered_sorted_words)
