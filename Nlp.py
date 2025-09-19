import streamlit as st
import pandas as pd
from nltk.tokenize import WhitespaceTokenizer
from nltk.tokenize import sent_tokenize
from nltk.tokenize import blankline_tokenize
import nltk

st.set_page_config(layout="wide")

m_col1,m_col2 = st.columns([1,1])
# Initialize session state for Words visibility
if 'show_words' not in st.session_state:
    st.session_state.show_words = False
if 'show_sentences' not in st.session_state:
    st.session_state.show_sentences = False
if 'show_paragraphs' not in st.session_state:
    st.session_state.show_paragraphs = False
if 'show_bigrams' not in st.session_state:
    st.session_state.show_bigrams = False
if 'show_trigrams' not in st.session_state:
    st.session_state.show_trigrams = False
if 'show_ngrams' not in st.session_state:
    st.session_state.show_ngrams = False

def find_words():
    st.session_state.show_words = True
    
def find_sentences():
    st.session_state.show_sentences = True

def find_paragraphs():
    st.session_state.show_paragraphs = True
    
def find_bigrams():
    st.session_state.show_bigrams = True
    
def find_trigrams():
    st.session_state.show_trigrams = True

def find_ngrams():
    st.session_state.show_ngrams = True
    
with m_col1:
    st.title("Natural Language Processing - Tokenization")
    
    st.write("Wecome! This web page performs tokenization for text provided in below text area.")
    
    test_string = '''This is a sample text. You can enter any text here'''
    
    test_string = st.text_area(
        label='Enter Text', 
        value = test_string
        )
    
    c1,c2 = st.columns(2)
    with c1:
        st.button(label="Show Words", on_click=find_words)
        st.button(label="Show Sentences", on_click=find_sentences)
        st.button(label="Show Paragraphs", on_click=find_paragraphs)
    with c2:
        st.button(label="Show Bigrams", on_click=find_bigrams)
        st.button(label="Show Trigrams", on_click=find_trigrams)
        st.button(label="Show Ngrams(4)", on_click=find_ngrams)
    
with m_col2:
    placeholder = st.empty()
    
text_tokens = WhitespaceTokenizer().tokenize(test_string)

if(st.session_state.show_words):
    df = pd.DataFrame()
    df.style.hide(axis="index")
    df['Tokens']=text_tokens
    placeholder.table(df)
    st.session_state.show_words = False

if(st.session_state.show_sentences):
    text_sent = sent_tokenize(test_string)
    df = pd.DataFrame()
    df.style.hide(axis="index")
    df['Sentences']=text_sent
    placeholder.table(df)
    st.session_state.show_sentences = False

if(st.session_state.show_paragraphs):
    text_para = blankline_tokenize(test_string)
    df = pd.DataFrame()
    df.style.hide(axis="index")
    df['Paragraphs']=text_para
    placeholder.table(df)
    st.session_state.show_paragraphs = False
    
if(st.session_state.show_bigrams):
    text_bigrams = list(nltk.bigrams(text_tokens))
    df = pd.DataFrame()
    df.style.hide(axis="index")
    df['Bigrams']=text_bigrams
    placeholder.table(df)
    st.session_state.show_bigrams= False

if(st.session_state.show_trigrams):
    text_trigrams = list(nltk.trigrams(text_tokens))
    df = pd.DataFrame()
    df.style.hide(axis="index")
    df['Trigrams']=text_trigrams
    placeholder.table(df)
    st.session_state.show_trigrams = False

if(st.session_state.show_ngrams):
    text_ngrams = list(nltk.ngrams(text_tokens,4))
    df = pd.DataFrame()
    df.style.hide(axis="index")
    df['Ngrams(4)']=text_ngrams
    placeholder.table(df)
    st.session_state.show_ngrams = False