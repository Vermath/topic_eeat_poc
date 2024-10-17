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
        # Construct the enhanced prompt with detailed EEAT guidelines
        prompt = f"""---
        
**You are tasked with evaluating content for adherence to Google's EEAT (Experience, Expertise, Authoritativeness, Trustworthiness) guidelines. Your goal is to provide a comprehensive assessment and offer specific recommendations for improvement.**

Here is the content to evaluate:

<content_to_evaluate>
{user_content}
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

            # Initialize variables to store extracted sections
            category_assessments = ""
            recommendations = ""
            grade_justification = ""
            overall_grade = ""

            # Extract the <category_assessments> section
            category_pattern = r'<category_assessments>\s*(.*?)\s*</category_assessments>'
            category_match = re.search(category_pattern, assistant_reply, re.DOTALL | re.IGNORECASE)
            if category_match:
                category_assessments = category_match.group(1).strip()

            # Extract the <recommendations> section
            recommendations_pattern = r'<recommendations>\s*(.*?)\s*</recommendations>'
            recommendations_match = re.search(recommendations_pattern, assistant_reply, re.DOTALL | re.IGNORECASE)
            if recommendations_match:
                recommendations = recommendations_match.group(1).strip()

            # Extract the <grade_justification> section
            grade_justification_pattern = r'<grade_justification>\s*(.*?)\s*</grade_justification>'
            grade_justification_match = re.search(grade_justification_pattern, assistant_reply, re.DOTALL | re.IGNORECASE)
            if grade_justification_match:
                grade_justification = grade_justification_match.group(1).strip()

            # Extract the <overall_grade> section with delimiters << >>
            overall_grade_pattern = r'<overall_grade>\s*<<\s*([^<>]+?)\s*>>\s*</overall_grade>'
            overall_grade_match = re.search(overall_grade_pattern, assistant_reply, re.DOTALL | re.IGNORECASE)
            if overall_grade_match:
                overall_grade = overall_grade_match.group(1).strip()

            # Display the assistant's reply sections and the overall grade
            col1, col2 = st.columns([3, 1])

            with col1:
                st.subheader("Evaluation and Recommendations")
                
                if category_assessments:
                    st.markdown("### Category Assessments")
                    st.write(category_assessments)
                
                if recommendations:
                    st.markdown("### Recommendations")
                    st.write(recommendations)
                
                if grade_justification:
                    st.markdown("### Grade Justification")
                    st.write(grade_justification)

            with col2:
                if overall_grade:
                    st.subheader("EEAT Score")
                    st.info(overall_grade)
                else:
                    st.subheader("EEAT Score")
                    st.info("Not found")
