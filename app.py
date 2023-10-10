import streamlit as st
from mcq_generator_utils import mcq_generation

st.header('AUTOMATED MULTIPLE CHOICS QUESTION GENERATOR')
st.subheader('Generates questions from your text article')

#upload the text file
text_file = st.file_uploader("Add text file !")