import streamlit as st
from mcq_generator_utils import mcq_generation
import io

st.title('AUTOMATED MULTIPLE CHOICE QUESTION GENERATOR')

# Create a sidebar for file upload and download
st.sidebar.title('Upload')
st.sidebar.title('Download')

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

        # Get the generated MCQs as a string with options in new lines
        generated_mcqs = mcq_generator.print_result(mapped_distractors, mapped_sentences)

        # Display the generated MCQs with a scrollable container
        st.write(generated_mcqs, unsafe_allow_html=True)

        # Create a button in the sidebar to download the generated MCQs with the specified file name "mcq.txt"
        download_button = st.sidebar.download_button('Download Generated MCQs', generated_mcqs, key='mcq.txt')

else:
    st.write("Upload a text file to generate MCQs.")
