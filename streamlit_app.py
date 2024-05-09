import streamlit as st
import google.generativeai as genai

# Streamlit app
st.subheader("Gemini Playground")
with st.sidebar:
  google_api_key = st.text_input("Google API Key", type="password")
prompt = st.text_input("Query", label_visibility="collapsed")

# If Submit button is clicked
if st.button("Submit"):
  if not google_api_key.strip() or not prompt.strip():
    st.error("Please provide the missing fields.")
  else:
    try:
      with st.spinner("Please wait..."):
        genai.configure(api_key=google_api_key)  
        model = genai.GenerativeModel("gemini-pro")
        responses = model.generate_content(prompt, stream=False)
        st.success(responses.text)      
    except Exception as e:
      st.exception(f"Exception: {e}")
