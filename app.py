import streamlit as st
import openai
import requests
from io import BytesIO
from PIL import Image

# Page setup
st.set_page_config(page_title="Mandala Art Generator 🌀", layout="centered")
st.title("🌀 Mandala Art Generator")
st.caption("Turn a single word into stunning mandala art using AI.")

# Sidebar with example words
st.sidebar.header("🌟 Try These Words")
for word in ["harmony", "zen", "chakra", "galaxy", "balance", "peace", "energy", "nature", "dream"]:
    st.sidebar.markdown(f"- {word}")

# Input: OpenAI API key
api_key = st.text_input("🔑 Enter your OpenAI API Key", type="password")

# Input: Word prompt
user_prompt = st.text_input("📝 Enter a word to inspire your mandala")

# Input: Style toggle
style = st.radio("🎨 Choose Mandala Style:", ["Color", "Black & White"])

# Generate button
if st.button("✨ Generate Mandala"):

    if not api_key or not user_prompt:
        st.error("Please enter both the API key and a word.")
    else:
        openai.api_key = api_key

        # Prompt engineering based on style
        if style == "Color":
            dalle_prompt = (
                f"A vivid, colorful, symmetrical mandala art inspired by the word '{user_prompt}'. "
                "It should be elegant, vibrant, and visually harmonious. Digital art style. Intricate details."
            )
        else:
            dalle_prompt = (
                f"A detailed, symmetrical mandala inspired by the word '{user_prompt}', in black and white. "
                "Fine line art sketch on a white background. No color. Highly intricate, clean, balanced."
            )

        with st.spinner("🎨 Generating your mandala..."):
            try:
                response = openai.images.generate(
                    model="dall-e-3",
                    prompt=dalle_prompt,
                    size="1024x1024",
                    quality="standard",
                    n=1,
                )

                image_url = response.data[0].url
                image_data = requests.get(image_url).content
                image = Image.open(BytesIO(image_data))

                # Show result
                st.image(image, caption=f"Mandala: '{user_prompt}' ({style})", use_column_width=False)

                # Download option
                st.download_button(
                    label="📥 Download Mandala",
                    data=image_data,
                    file_name=f"mandala_{user_prompt}_{style.lower().replace(' ', '_')}.png",
                    mime="image/png"
                )

            except Exception as e:
                st.error(f"❌ Error: {e}")
