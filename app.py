import streamlit as st
import re
from openai import OpenAI

# Set your OpenAI API key using st.secrets
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
        # Construct the enhanced prompt with detailed EEAT guidelines, excluding specific aspects
        prompt = f"""---
        
You are tasked with evaluating content for adherence to Google's EEAT (Experience, Expertise, Authoritativeness, Trustworthiness) guidelines. Your goal is to provide a comprehensive assessment and offer specific recommendations for improvement.

Here is the content to evaluate:

<content_to_evaluate>
{{CONTENT}}
</content_to_evaluate>

Please follow these steps to complete the evaluation:

1. Carefully read through the content provided above.

2. Evaluate the content based on each category of the EEAT guidelines:

   a) Content and Quality
   b) Expertise
   c) Focus on People-First Content
   d) Avoid Creating Search Engine-First Content
   e) Promote User Interaction
   f) "Who, How, and Why" of Content Creation
   g) E-E-A-T and Quality Rater Guidelines

   For each category, consider the specific questions and criteria outlined in the guidelines.

3. As you evaluate each category, make notes on strengths and areas for improvement. Be specific and provide examples from the content where possible.

4. Based on your evaluation, develop specific recommendations for improving the content according to the EEAT guidelines. These recommendations should be actionable and directly address any weaknesses you identified.

5. Determine an overall grade for the content's adherence to EEAT guidelines, ranging from F to A++. Consider the content's performance across all categories when assigning this grade.

6. Provide a justification for the grade you've assigned, summarizing the key strengths and weaknesses of the content in relation to the EEAT guidelines.

7. Format your response as follows:

<evaluation>
<category_assessments>
[Provide your assessment for each category of the EEAT guidelines here. Include specific examples and observations from the content.]
</category_assessments>

<recommendations>
[List your specific recommendations for improving the content here. Each recommendation should be clear, actionable, and directly tied to the EEAT guidelines.]
</recommendations>

<grade_justification>
[Provide your justification for the overall grade here, summarizing the key strengths and weaknesses of the content in relation to the EEAT guidelines.]
</grade_justification>

<overall_grade>
[Insert the overall grade here, surrounded by double angle brackets. For example: <<B+>>]
</overall_grade>
</evaluation>

Remember, do not consider Author Credentials, Imagery, or other forms of Visual Engagement in your evaluation. When evaluating Promote User Interaction, do not penalize the absence of a comment section as the content may not be published yet.

Provide your evaluation based solely on the content provided and the EEAT guidelines. Be thorough, objective, and constructive in your assessment.

{user_content}

---

Please ensure your evaluation is thorough and references specific aspects of the guidelines. Remember to provide the overall grade surrounded by delimiters like '<<score: A>>'.
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
            score_match = re.search(score_pattern, assistant_reply, re.IGNORECASE)

            if score_match:
                score = score_match.group(1).strip()
                # Remove the score from the assistant's reply
                assistant_reply_without_score = re.sub(score_pattern, '', assistant_reply, flags=re.IGNORECASE).strip()
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
