import anthropic
import streamlit as st

### Sidebar contents
with st.sidebar:
    st.title("What's your profile?")

    country = st.text_input("Country", value="USA")

    age = st.text_input("Age", value=24)

    industry = st.text_input("Industry or Field of Expertise", value="Information Technology")

    education_level = st.selectbox(
        "Education level",
        ("High school", "Bachelor’s degree", "Master’s or above")
    )

    field_of_study = st.text_input("Field of Study", value="Computer Science")

    work_experience = st.selectbox(
        "Work Experience",
        ("<1 year", "1-3 years", "3-7 years", "7+ years")
    )

    family_situation = st.selectbox(
        "Family situation",
        ("Single", "Married with no kids", "Married with kid(s)")
    )
    
    your_prompt = st.text_input(label="Your Prompt", value=f"I am a {age} year old person from {country}. I work in, or want to work in, the {industry} industry. I have {education_level} education level in {field_of_study}. My family situation is that I am {family_situation}.")

SYSTEM_PROMPT = '''
You are an expert immigration assistant. Your job is to provide the user with the best 3 to 5 options of countries they could immigrate to based on their profile.
Given the following user profile, generate a list of suitable countries for immigration, including visa options, accommodation arrangements, and other relevant factors:

- Country of Domicile: {country}
- Age: {age}
- Education Level: {education_level}
- Field of Study: {field_of_study}
- Work Experience Level: {work_experience}
- Family Situation: {family_situation}
- Industry or Field of Expertise: {industry}

Please consider the following in your recommendations:

1. Visa Options: Identify which countries offer feasible immigration pathways based on the user's education and work experience. Include specific visa programs, such as skilled worker visas, investor visas, working holiday visas, or family reunification, that align with the user's profile.

2. Housing/Accommodation Arrangements: Based on the desired destination, suggest suitable housing options. Take into account the user's budget, preferred location, required amenities, and family size. Offer insights into temporary accommodations for initial settlement (such as short-term rentals or serviced apartments) and long-term housing solutions (like rental properties or purchasing options).

3. Cost of Living and Budget Compatibility: Evaluate the cost of living in the recommended countries and how it aligns with the user’s current and desired income. Provide guidance on managing living expenses, including housing, healthcare, education (if applicable for dependents), and general lifestyle costs.

4. Quality of Life Factors: Briefly touch on aspects that could influence the quality of life, including the country’s healthcare system, education system, safety, and cultural integration opportunities, especially considering the user's family situation.

Your recommendations should help the user make an informed decision about which country or countries could be the best fit for their immigration goals, considering professional opportunities, lifestyle preferences, and family needs.
'''

def generate_response(question): 
    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        messages=[{"role":"user", "content":question}],
    )
    return response.content[0].text

st.title("Immigrate AI")

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "I am Immigrate AI. I can help you with all your immigration needs. How may I help you today?"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User-provided prompt
if user_prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.write(process_user_input())

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_response(user_prompt) 
            st.write(response) 
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)
