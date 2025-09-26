import streamlit as st
from gtts import gTTS
import os
from langdetect import detect, lang_detect_exception
from deep_translator import GoogleTranslator
import pycountry
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
import nltk

# Download NLTK data
nltk.download('punkt')
nltk.download('words')

# Function to read text aloud
def read_aloud(text, language='en'):
    tts = gTTS(text=text, lang=language)
    tts.save("temp.mp3")
    os.system("start temp.mp3")

# Function to generate word cloud
def generate_wordcloud(text):
    english_words = set(nltk.corpus.words.words())
    words = word_tokenize(text)
    english_words_in_text = [word for word in words if word.lower() in english_words]
    english_text = ' '.join(english_words_in_text)
    
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(english_text)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    plt.tight_layout()
    return fig

# Main Streamlit app
st.title("Globalize")

# Optional background image
background_image = "back.jpg"  # Replace with your background image file
st.markdown(
    f"""
    <style>
    .reportview-container {{
        background: url(data:streamlit_env\\back.jpg;base64,{background_image});
        background-size: cover;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Two-column layout
col1, col2 = st.columns(2)

# User input
with col1:
    paragraph = st.text_area("Enter one paragraph:")

with col2:
    all_languages = [lang.name for lang in pycountry.languages]
    target_languages_input = st.multiselect(
        "Select the desired languages for translation:", all_languages
    )

# Button: Read Aloud
if st.button("Read Aloud"):
    read_aloud(paragraph)

# Detect input language
paragraph_language = None
if paragraph.strip():
    try:
        paragraph_language = detect(paragraph)
        language_name = pycountry.languages.get(alpha_2=paragraph_language).name
        st.write("Detected language:", language_name)
    except lang_detect_exception.LangDetectException as e:
        st.error(f"Language detection failed: {e}")
        paragraph_language = 'en'
        language_name = 'English'
    except KeyError:
        st.error("Language code not found in pycountry")
        language_name = 'Unknown'
    except Exception as e:
        st.error(f"Error during language detection: {e}")

# Translate to English if needed
if paragraph_language and paragraph_language != 'en':
    translated_paragraph = GoogleTranslator(source='auto', target='en').translate(paragraph)
    st.write("Translated to English:", translated_paragraph)
else:
    translated_paragraph = paragraph

# Generate and display word cloud
if translated_paragraph.strip():
    try:
        translated_paragraph = translated_paragraph.encode('utf-8', 'ignore').decode('utf-8')
        wordcloud_fig = generate_wordcloud(translated_paragraph)
        st.sidebar.subheader("Word Cloud")
        st.sidebar.pyplot(wordcloud_fig)
    except Exception as e:
        st.error(f"Error generating word cloud: {e}")

# Optional image below word cloud
st.sidebar.subheader("Image")
# st.sidebar.image("languages.jpg", use_column_width=True)

# Translate and read aloud into target languages
if st.button("Translate and Read Aloud"):
    target_languages = []

    # Convert selected language names to alpha_2 codes
    for lang_name in target_languages_input:
        try:
            lang_code = pycountry.languages.lookup(lang_name).alpha_2
            target_languages.append(lang_code)
        except LookupError:
            st.error(f"Language '{lang_name}' not found in pycountry")

    # Translate and read aloud for each target language
    for target_language in target_languages:
        try:
            translated_paragraph_target = GoogleTranslator(
                source='auto', target=target_language
            ).translate(paragraph)

            try:
                language_name = pycountry.languages.get(alpha_2=target_language).name
            except KeyError:
                language_name = target_language

            st.write(f"\nTranslated paragraph in {language_name}:")
            st.write(translated_paragraph_target)

            # Read aloud
            read_aloud(translated_paragraph_target, target_language)

        except Exception as e:
            st.error(f"Translation to {target_language} failed: {e}")

