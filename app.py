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
        
**Please evaluate the following content for adherence to Google's EEAT (Experience, Expertise, Authoritativeness, Trustworthiness) guidelines. Use the detailed guidelines provided below to assess the content. Provide an overall grade from F to A++ for how well it adheres to the guidelines, and surround the score in delimiters like '<<score: A>>' for easy extraction. Then, provide specific recommendations on how to improve the content according to the EEAT guidelines.**

---

### **EEAT Guidelines:**

#### **Content and Quality Questions:**

- **Originality and Value:**
  - Does the content provide original information, reporting, research, or analysis?
  - Does it offer substantial, complete, or comprehensive coverage of the topic?
  - Does it provide insightful analysis or interesting information beyond the obvious?
  - If drawing on other sources, does it add substantial additional value and originality rather than simply copying or rewriting?

- **Headings and Titles:**
  - Does the main heading or page title provide a descriptive, helpful summary of the content?
  - Does it avoid exaggeration or shock value?

- **User Engagement:**
  - Is this the sort of page you'd want to bookmark, share with a friend, or recommend?
  - Would you expect to see this content in or referenced by a printed magazine, encyclopedia, or book?

- **Comparative Value:**
  - Does the content provide substantial value compared to other pages in search results?

- **Quality and Presentation:**
  - Does the content have spelling or stylistic issues?
  - Is it well-produced, or does it appear sloppy or hastily created?
  - Is the content mass-produced or outsourced to many creators without adequate attention or care?

#### **Expertise Questions:**

- **Trustworthiness and Authority:**
  - Does the content present information in a way that makes you want to trust it?
    - Clear sourcing?
    - Evidence of expertise?
    - Background about the author or the site (e.g., links to an author page or About page)?

- **Reputation:**
  - If someone researched the site or author, would they find it well-trusted or widely recognized as an authority on the topic?

- **Expert Contribution:**
  - Is the content written or reviewed by an expert or enthusiast who knows the topic well?

- **Accuracy:**
  - Does the content have any easily verified factual errors?

#### **Focus on People-First Content:**

- **Audience Awareness:**
  - Do you have an existing or intended audience that would find the content useful if they came directly to you?

- **Demonstrated Expertise:**
  - Does the content clearly demonstrate first-hand expertise and depth of knowledge (e.g., expertise from actually using a product or service, or visiting a place)?

- **Purpose and Focus:**
  - Does your site have a primary purpose or focus?

- **User Satisfaction:**
  - After reading, will someone feel they've learned enough to achieve their goal?
  - Will they feel satisfied with their experience?

#### **Avoid Creating Search Engine-First Content:**

- **Motivation:**
  - Is the content primarily made to attract search engine visits?
  - Are you producing lots of content on various topics hoping some might perform well in search results?

- **Automation and Value:**
  - Are you using extensive automation to produce content on many topics?
  - Are you mainly summarizing others without adding much value?

- **Trends and Relevance:**
  - Are you writing about things simply because they are trending, not because they align with your audience?

- **Reader Experience:**
  - Does your content leave readers feeling they need to search again for better information?

- **Word Count and Freshness:**
  - Are you writing to a particular word count because you've heard Google prefers it? (Note: Google does not.)
  - Are you changing dates or adding/removing content primarily to make the site seem "fresh"?

- **Expertise and Authenticity:**
  - Did you enter a niche topic without any real expertise, mainly to get search traffic?
  - Does your content promise answers to questions that have no answer?

#### **"Who, How, and Why" of Content Creation:**

- **Who (Created the Content):**
  - Is it clear who authored the content?
  - Do pages have bylines where appropriate?
  - Do bylines link to information about the author, their background, and expertise?

- **How (Content Was Created):**
  - Is it evident if automation or AI was used in content creation?
  - Are you transparent about how and why automation or AI was utilized?

- **Why (Content Was Created):**
  - Is the primary purpose to help people and provide value?
  - Or is it mainly to attract search engine visits?

#### **E-E-A-T and Quality Rater Guidelines:**

- **Experience, Expertise, Authoritativeness, Trustworthiness:**
  - Does the content demonstrate these qualities?
  - Is the content helpful, reliable, and created for people first?

---

### **Content to Evaluate:**

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
