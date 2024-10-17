import streamlit as st
import os
import re
from openai import OpenAI

# Set your OpenAI API key
api_key = st.secrets["OPENAI_API_KEY"]

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

st.title("EEAT Content Evaluator")

# Text area for user input
user_content = st.text_area("Enter your content here:", height=300)

if st.button("Evaluate Content"):
    if user_content.strip() == '':
        st.warning("Please enter some content to evaluate.")
    else:
        # Construct the prompt
        prompt = f"""Please evaluate the following content for adherence to Google's EEAT (Experience, Expertise, Authoritativeness, Trustworthiness) guidelines. Provide an F to A++ score for how well it adheres to the guidelines, and surround the score in delimiters like '<<score: A>>'. Then, provide recommendations on how to improve the content according to the EEAT guidelines.

Content:

{user_content}
"""

        try:
            with st.spinner('Evaluating content...'):
                # Call the OpenAI API
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        },
                    ],
                )
        except Exception as e:
            st.error(f"An error occurred: {e}")
        else:
            # Extract the assistant's reply
            assistant_reply = response.choices[0].message.content

            # Extract the score using a regular expression
            score_pattern = r'<<score:\s*(.*?)>>'
            score_match = re.search(score_pattern, assistant_reply)

            if score_match:
                score = score_match.group(1)
                # Remove the score from the assistant's reply
                assistant_reply_without_score = re.sub(score_pattern, '', assistant_reply).strip()
            else:
                score = 'Not found'
                assistant_reply_without_score = assistant_reply

            # Display the assistant's reply and the score
            col1, col2 = st.columns([3, 1])

            with col1:
                st.subheader("Evaluation and Recommendations")
                st.write(assistant_reply_without_score)

            with col2:
                st.subheader("EEAT Score")
                st.info(score)
