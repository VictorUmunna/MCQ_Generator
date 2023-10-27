#Importing the needed files and packages

import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('popular')


from nltk.tokenize import sent_tokenize
from flashtext import KeywordProcessor
from pywsd.similarity import max_similarity
from pywsd.lesk import adapted_lesk
from pywsd.lesk import simple_lesk
from pywsd.lesk import cosine_lesk
from nltk.corpus import wordnet
from typing_extensions import TypeAlias
from nltk.corpus import stopwords
import streamlit as st
import nltk
import pke
import string
import requests
import json
import re
import random
import pandas as pd
import warnings
warnings.filterwarnings('ignore')


class mcq_generation():
    def __init__(self) -> None:
        pass

    # read the text data
    def read_data(self, filepath):
        """Read the text in a file path.

        Args:
            filepath: The path of the file.

        Returns:
            A text file
        """        
        file=open(filepath, encoding = 'unicode_escape')
        text=file.read().strip()
        return text
    

    
    # extract the important words(keywords) from the text article
    def extract_keywords(self, article: str) -> list[str]:
        """Extracts keywords  from an article using the MultipartiteRank algorithm.

        Args:
            article: The article text.

        Returns:
            A list of extracted keywords.
        """

        extractor = pke.unsupervised.MultipartiteRank()

        stop_words = list(string.punctuation)
        stop_words += ['-lrb-', '-rrb-', '-lcb-', '-rcb-', '-lsb-', '-rsb-']
        stop_words += stopwords.words('english')

        extractor.load_document(input=article, stoplist=stop_words)

        # Select the longest sequences of nouns and adjectives, that do not
        # contain punctuation marks or stopwords as candidates.
        
        pos = {'NOUN', 'PROPN', 'ADJ'}
        #pos = {'PROPN'}
        extractor.candidate_selection(pos=pos)

        # Build the Multipartite graph.
        extractor.candidate_weighting()

        # Get the 25-highest scored candidates as keyphrases.
        keyphrases = extractor.get_n_best(n=30)

        keywords = []
        for phrases in keyphrases:
            keywords.append(phrases[0])

        return keywords
    


    # Split the whole text article into an array/list of individual sentences.
    def split_text_to_sentences(self, article: str) -> list[str]:
        """Splits a text article into a list of individual sentences.

        Args:
            article: The text article.

        Returns:
            A list of individual sentences.
        """

        sentences = sent_tokenize(article)
        sentences = [sentence.strip() for sentence in sentences if len(sentence) > 15]
        #reason for the strip()?

        return sentences


        
    # Map the sentences which contain the keywords to the related keywords
    def map_sentences_to_keywords(self, words, sentences):
            
        """
        Maps the sentences which contain the keywords to the related keywords.

        Args:
            words: A list of keywords.
            sentences: A list of sentences.

        Returns:
            A dictionary mapping each keyword to a list of sentences that contain the keyword.
        """

        keywordProcessor = KeywordProcessor() #Using keyword processor as our processor for this task
        keySentences = {}
        for word in words:
            keySentences[word] = []
            keywordProcessor.add_keyword(word) #Adds key word to the processor

        for sentence in sentences:
            found = keywordProcessor.extract_keywords(sentence)
            for each in found:
                keySentences[each].append(sentence)

        for key in keySentences.keys():
            sortedSentences = sorted(keySentences[key], key=len, reverse=True)
            keySentences[key] = sortedSentences

        return keySentences
    


    # Get the sense of the word
    def get_word_sense(self, sentence, word):
        """
        Returns the most likely sense of a word in a given context.

        Args:
            sent: The sentence in which the word appears.
            words_new: The list of words to get the sense for.

        Returns:
            A synset representing the most likely sense of the word, or None if no
            synset is found.
        """

        word = word.lower()
        # Split the word with underscores(_) instead of spaces if there are multiple
        # words. This is necessary because wordnet does not support compound words.
        if len(word.split()) > 0:
            word = word.replace(" ", "_")

        synsets = wordnet.synsets(word, 'n')
        if synsets:
            # Use two different WSD algorithms, Wu-Palmer (WUP) and Adapted Lesk,
            # to determine the most likely sense of the word. The algorithm with the
            # lowest index is returned.
            wu_palmer_output = max_similarity(sentence, word, 'wup', pos='n')
            adapted_lesk_output = adapted_lesk(sentence, word, pos='n')
            lowest_index = min(synsets.index(wu_palmer_output), synsets.index(adapted_lesk_output))
            return synsets[lowest_index]
        else:
            return None
        


    # 
    def get_distractors_wordnet(self, syn, word):
        """Gets distractors for a word from WordNet.

        Args:
            syn: A WordNet synset.
            word: A string.

        Returns:
            A list of distractor words.
        """

        distractors = []
        word = word.lower()
        actual_word = word

        if len(word.split()) > 0:
            word = word.replace(" ", "_")

        hypernyms = syn.hypernyms()
        if not hypernyms:
            return distractors

        # Find the hyponyms of the first hypernym.
        hyponyms = hypernyms[0].hyponyms()

        # Iterate over the hyponyms and add them to the list of distractors,
        # if they are not the actual word and are not already in the list.
        for hypo in hyponyms:
            name = hypo.lemmas()[0].name()
            if name == actual_word:
                continue

            name = name.replace("_", " ")
            name = " ".join(w.capitalize() for w in name.split())
            if name not in distractors:
                distractors.append(name)

        return distractors


    


    def get_distractors_conceptnet(self, word):
        """Gets distractors for a word from ConceptNet.

        Args:
            word: A string.

        Returns:
            A list of distractor words.
        """

        word = word.lower()
        actual_word = word

        if len(word.split()) > 0:
            word = word.replace(" ", "_")

        distractors = []

        # Construct the first ConceptNet API query URL.
        url = (
            "http://api.conceptnet.io/query?node=/c/en/%s/n&rel=/r/PartOf&start=/c/en/%s&limit=5"
            % (word, word)
        )

        # Send the first ConceptNet API query and get the response.
        response = requests.get(url)
        data = response.json()

        # Iterate over the edges in the first ConceptNet API response.
        for edge in data["edges"]:

            # Get the link from the edge.
            link = edge["end"]["term"]

            # Construct the second ConceptNet API query URL.
            url2 = (
                "http://api.conceptnet.io/query?node=%s&rel=/r/PartOf&end=%s&limit=10"
                % (link, link)
            )

            # Send the second ConceptNet API query and get the response.
            response2 = requests.get(url2)
            data2 = response2.json()

            # Iterate over the edges in the second ConceptNet API response.
            for edge in data2["edges"]:

                # Get the word from the edge.
                word2 = edge["start"]["label"]

            # If the word is not already in the list of distractors and is different from the actual word, add it to the list.
            if word2 not in distractors and actual_word.lower() not in word2.lower():
                distractors.append(word2)

        # Return the list of distractors.
        return distractors

    


    # map the distractors to keywords
    def map_distractors(self, mapped_sentence, words_sense, distractors_wordnet, distractors_conceptnet):
        mapped_distractors = {}
        for keyword in mapped_sentence:
            # Get the word sense of the keyword.
            word_sense = words_sense(mapped_sentence[keyword][0], keyword)

            # If there is a word sense, then get the WordNet distractors.
            if word_sense:
                distractors = distractors_wordnet(word_sense, keyword)

                # If there are no WordNet distractors, then get the ConceptNet distractors.
                if len(distractors) == 0:
                    distractors = distractors_conceptnet(keyword)

                # If there are any distractors, then map them to the keyword.
                if len(distractors) != 0:
                    mapped_distractors[keyword] = distractors

            # If there is no word sense, then directly search for and map the ConceptNet distractors.
            else:
                distractors = distractors_conceptnet(keyword)

                # If there are any distractors, then map them to the keyword.
                if len(distractors) > 0:
                    mapped_distractors[keyword] = distractors
        # Print the mapped distractors.
        return mapped_distractors
    



    # print result
    def print_result(self, mapped_distractors, mapped_sentences):
        header_printed = False
        mcq_output = []

        iterator = 1  # To keep the count of the questions

        for keyword in mapped_distractors:
            # Get the first sentence from the set of sentences.
            sentence = mapped_sentences[keyword][0]

            pattern = re.compile(keyword, re.IGNORECASE)  # Converts into a regular expression for pattern matching
            option_string = pattern.sub("________", sentence)  # Replaces the keyword with underscores (blanks)

            # Prints the header if it has not already been printed.
            if not header_printed:
                mcq_output.append("*************************************** Multiple Choice Questions ***************************************")
                header_printed = True

            # Add the question along with a question number to the output list
            mcq_output.append(f"Question {iterator}: {option_string}")

            # Capitalizes the options and selects only 4 options
            options = [keyword.capitalize()]
            for distractor in mapped_distractors[keyword]:
                options.append(distractor)
                if len(options) == 4:
                    break

            # Shuffles the options so that the order is not always the same
            random.shuffle(options)

            # Add the options to the output list with each option on a new line
            opts = ['a', 'b', 'c', 'd']
            for i, option in enumerate(options):
                if i < len(opts):
                    mcq_output.append(f"\t{opts[i]}) {option}")

            mcq_output.append("")  # Add an empty line between questions
            iterator += 1  # Increase the counter

        # Return the MCQs as a string
        return "\n".join(mcq_output)


            







