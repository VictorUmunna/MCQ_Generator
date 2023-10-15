import streamlit as st
from mcq_generator_utils import mcq_generation

st.header('AUTOMATED MULTIPLE CHOICE QUESTION GENERATOR')
st.subheader('Generates questions from your text article')

#upload the text file
file = st.file_uploader("Add text file!")

#@st.cache_data
def generate_mcq(text):
     mcq = mcq_generation()
     keyword = mcq.extract_keywords(text)
     sentences = mcq.split_text_to_sentences(text)
     mapped_sentences = mcq.map_sentences_to_keywords(keyword,sentences)
     mapped_distractors = mcq.map_distractors(mapped_sentences, mcq.get_word_sense, mcq.get_distractors_wordnet, mcq.get_distractors_conceptnet)
     result = mcq.print_result(mapped_distractors, mapped_sentences)
     return result

if file is not None:
     text = file.read()
     text = text.decode('utf-8')
     # Process the text or do whatever you need to do with it

     if st.button('Generate'):
         res = generate_mcq(text)

        # Initialize a Boolean variable to track whether the header has been printed.
        header_printed = False

        # Initialize a list to store the results.
        results = []

        # Iterate over the mapped distractors.
        for keyword, distractors in mapped_distractors.items():

        # If the header has not been printed, then print it.
            if not header_printed:
                st.write('**Multiple Choice Questions**')
                header_printed = True

            # Construct the question.
            question = 'Which of the following is the best definition for the word "{}"?'.format(keyword)

            # Add the question to the list of results.
            results.append(question)

            # Add the distractors to the list of results.
            for distractor in distractors:
                results.append(distractor)

            # Add a blank line to the list of results.
            results.append('')

        # Print the results to the console.
        for result in results:
            st.write(result)
