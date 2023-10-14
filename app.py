import streamlit as st
from mcq_generator_utils import mcq_generation

st.header('AUTOMATED MULTIPLE CHOICeS QUESTION GENERATOR')
st.subheader('Generates questions from your text article')

#upload the text file
file = st.file_uploader("Add text file!")

if file is not None:
    text = file.read()
    text = text.decode('utf-8')
    # Process the text or do whatever you need to do with it

    mcq = mcq_generation()
    keyword = mcq.extract_keywords(text)
    sentences = mcq.split_text_to_sentences(text)
    mapped_sentences = mcq.map_sentences_to_keywords(keyword,sentences)
    mapped_distractors = mcq.map_distractors(mapped_sentences, mcq.get_word_sense, mcq.get_distractors_wordnet, mcq.get_distractors_conceptnet)
    result = mcq.print_result(mapped_distractors, mapped_sentences)

    if st.button('Generate'):
        res = result
        st.write(res)

