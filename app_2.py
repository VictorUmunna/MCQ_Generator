import streamlit as st
from mcq_generator_utils import mcq_generation

# Streamlit app header
st.header('AUTOMATED MULTIPLE CHOICE QUESTION GENERATOR')
st.subheader('Generates questions from your text article')

# Upload a text file
file = st.file_uploader("Upload a text file")

def generate_mcq(text):
    mcq = mcq_generation()
    keyword = mcq.extract_keywords(text)
    sentences = mcq.split_text_to_sentences(text)
    mapped_sentences = mcq.map_sentences_to_keywords(keyword, sentences)
    mapped_distractors = mcq.map_distractors(mapped_sentences, mcq.get_word_sense(), mcq.get_distractors_wordnet, mcq.get_distractors_conceptnet)
    result = mcq.print_result(mapped_distractors, mapped_sentences)
    return result

if file is not None:
    text = file.read().decode('utf-8')
    
    # Process the text and generate MCQs when the button is clicked
    if st.button('Generate'):
        res = generate_mcq(text)
        
        # Display the generated questions
        st.write(res)


