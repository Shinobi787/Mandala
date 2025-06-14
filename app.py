import streamlit as st
import openai
import requests
from io import BytesIO
from PIL import Image

# App Title
st.set_page_config(page_title="Mandala Art Generator 🎨", layout="centered")
st.title("🌀 Mandala Art Generator")
st.caption("Generate vivid, colorful, symmetrical mandala art from one inspiring word.")

# Sidebar: Example prompts
st.sidebar.header("🌟 Inspiration Examples")
example_prompts = ["harmony", "zen", "galaxy", "chakra", "balance", "dream", "energy", "nature", "universe"]
st.sidebar.write("Try one of these:")
for example in example_prompts:
    st.sidebar.write(f"• {example}")

# API Key input (hidden, secure)
api_key = st.text_input("🔑 Enter your OpenAI API Key", type="password")

# Word input from user
user_prompt = st.text_input("📝 Enter one word to inspire your mandala art")

# Button to trigger generation
if st.button("🎨 Generate Mandala"):

    if not api_key or not user_prompt:
        st.error("Please enter both the API key and a word.")
    else:
        openai.api_key = api_key

        # Prompt engineering
        dalle_prompt = (
            f"A vivid, colorful, symmetrical mandala art inspired by the word '{user_prompt}'. "
            "It should be elegant, vibrant, and visually harmonious. Digital art style."
        )

        # Show loading spinner
        with st.spinner("Generating mandala art..."):

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

                # Display the image
                st.image(image, caption=f"Mandala inspired by '{user_prompt}'", use_column_width=False)

                # Download button
                st.download_button(
                    label="📥 Download Mandala",
                    data=image_data,
                    file_name=f"mandala_{user_prompt}.png",
                    mime="image/png"
                )

            except Exception as e:
                st.error(f"Something went wrong: {e}")
