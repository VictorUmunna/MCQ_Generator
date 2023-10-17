import streamlit as st
from mcq_generator_utils import mcq_generation


st.title('Automated Multiple Choice Question Generator')
st.sidebar.title('Upload')

# File upload widget
file = st.sidebar.file_uploader("Add a text file")

if file is not None:
    text = file.read().decode('utf-8')

    # Create an instance of the mcq_generation class
    mcq_generator = mcq_generation()

    # Generate MCQs
    if st.sidebar.button('Generate MCQs'):
        st.subheader('Generated MCQs:')
        keywords = mcq_generator.extract_keywords(text)
        sentences = mcq_generator.split_text_to_sentences(text)
        mapped_sentences = mcq_generator.map_sentences_to_keywords(keywords, sentences)
        words_sense = mcq_generator.get_word_sense
        distractors_wordnet = mcq_generator.get_distractors_wordnet
        distractors_conceptnet = mcq_generator.get_distractors_conceptnet
        mapped_distractors = mcq_generator.map_distractors(mapped_sentences, words_sense, distractors_wordnet, distractors_conceptnet)

        # Print the generated MCQs
        mcq_generator.print_result(mapped_distractors, mapped_sentences)
else:
    st.write("Upload a text file to generate MCQs.")
