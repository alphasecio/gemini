import streamlit as st
import google.generativeai as genai
import PIL.Image

with st.sidebar:
  st.subheader("Gemini Playground")
  google_api_key = st.text_input("Google API key", type="password", value="")
  option = st.radio("Use Gemini to...", [
    "Answer a question",
    "Caption an image",
    "Blog about an image",
    "Summarize a transcript"
  ])

if option == "Answer a question":
  col1, col2 = st.columns([4,1])
  prompt = col1.text_input("Query", label_visibility="collapsed")
  if col2.button("Submit"):
    if not google_api_key.strip() or not prompt.strip():
      st.error("Please provide the missing fields.")
    else:
      try:
        with st.spinner("Please wait..."):
          genai.configure(api_key=google_api_key)
          model = genai.GenerativeModel("gemini-pro")
          response = model.generate_content(prompt, stream=False)
          st.success(response.text)
      except Exception as e:
        st.exception(f"Exception: {e}")
elif option == "Caption an image":
  image = st.file_uploader("Source Image", label_visibility="collapsed", type=("jpg", "jpeg", "png"))
  if image is not None:
    st.image(image, caption="Source Image")
  if st.button("Submit"):
    if not google_api_key.strip() or not image:
      st.error("Please provide the missing fields.")
    else:
      try:
        with st.spinner("Please wait..."):
          genai.configure(api_key=google_api_key)
          model = genai.GenerativeModel("gemini-pro-vision")
          response = model.generate_content(PIL.Image.open(image), stream=False)
          st.success(response.text)
      except Exception as e:
        st.exception(f"Exception: {e}")
elif option == "Blog about an image":
  prompt = "Write an engaging blog post based on this picture. It should include all significant objects identified."
  image = st.file_uploader("Source Image", label_visibility="collapsed", type=("jpg", "jpeg", "png"))
  if image is not None:
    st.image(image, caption="Source Image")
  if st.button("Submit"):
    if not google_api_key.strip() or not image:
      st.error("Please provide the missing fields.")
    else:
      try:
        with st.spinner("Please wait..."):
          genai.configure(api_key=google_api_key)
          model = genai.GenerativeModel("gemini-pro-vision")
          response = model.generate_content([prompt, PIL.Image.open(image)], stream=False)
          st.success(response.text)
      except Exception as e:
        st.exception(f"Exception: {e}") 
elif option == "Summarize a transcript":
  prompt = """Please read through the following transcript carefully. Then, write a concise summary of the key topics, ideas and conclusions covered in the discussion between the host and the guest(s). 
  
  Organize your summary into clear sections with descriptive headers, and use bullet points to list the main takeaways under each section.
  
  Some tips:
  - Focus on capturing the essence and key points succinctly, in your own words. Do not include any long verbatim quotes from the transcript.
  - Ignore any preamble and information about the guest's background, experience etc, and focus only on the key topic being discussed.
  - Aim for an overall summary length of around 400-600 words. 
  - Use a structured format to make the summary easy to read and navigate.

  Here is the full transcript of the podcast episode to summarize:
  """
  transcript = st.text_area("Podcast Transcript", label_visibility="collapsed", height=200)
  if st.button("Submit"):
    if not google_api_key.strip() or not transcript.strip():
      st.error("Please provide the missing fields.")
    else:
      try:
        with st.spinner("Please wait..."):
          genai.configure(api_key=google_api_key)
          model = genai.GenerativeModel("gemini-pro")
          response = model.generate_content(prompt, stream=False)
          st.success(response.text)
      except Exception as e:
        st.exception(f"Exception: {e}") 
