import streamlit as st
import nltk
from mcq_generator_utils import mcq_generation
import io

st.markdown("<h1 style='text-align: center; color: #1E90FF;'>AUTOMATED MULTIPLE CHOICE QUESTION GENERATOR</h1>", unsafe_allow_html=True)

# Create a sidebar for file upload and download
st.sidebar.title('Upload :arrow_double_up:')


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

        # Get the generated MCQs as a string
        generated_mcqs = mcq_generator.print_result(mapped_distractors, mapped_sentences)

        # Display the generated MCQs
        st.text(generated_mcqs)

        st.sidebar.title('Download :arrow_double_down:')

        # Create a button in the sidebar to download the generated MCQs
        download_button = st.sidebar.download_button('Download Generated MCQs', generated_mcqs, key='download')

else:
    st.write("Upload a text file to generate MCQs.")
