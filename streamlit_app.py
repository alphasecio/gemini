import os, io, streamlit as st
import google.genai as genai
import PIL.Image
from google.genai import types

def get_env_var(key, required=False, default=None):
    value = os.getenv(key, default)
    if value is None or value.strip() == "":
        if required:
            raise EnvironmentError(f"{key} environment variable is required but not set.")
        return ""
    return value.strip()

# Get the vertex usage flag
use_vertex = get_env_var("GOOGLE_GENAI_USE_VERTEXAI", default="false").lower() == "true"

# Collect all variables
GOOGLE_API_KEY = get_env_var("GOOGLE_API_KEY")
GOOGLE_CLOUD_PROJECT = get_env_var("GOOGLE_CLOUD_PROJECT")
GOOGLE_CLOUD_LOCATION = get_env_var("GOOGLE_CLOUD_LOCATION")

# Conditional validation
if use_vertex:
    if not GOOGLE_CLOUD_PROJECT or not GOOGLE_CLOUD_LOCATION:
        raise EnvironmentError("GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION must be set when using Vertex AI.")
else:
    if not GOOGLE_API_KEY:
        raise EnvironmentError("GOOGLE_API_KEY must be set when not using Vertex AI.")

model_options = {
    "Gemini 1.5 Flash": "gemini-1.5-flash",
    "Gemini 2.0 Flash": "gemini-2.0-flash"
}

# Streamlit app config
st.set_page_config(page_title="Gemini Chatbot", page_icon="🧠", initial_sidebar_state="auto")

with st.sidebar:
    st.title("🧠 Gemini Chatbot")
    st.caption(
        """
        This chatbot uses Google Gemini to answer your questions. Upload an image and/or ask a question to get started.
        """
    )
    with st.expander("**⚙️ Model Settings**", expanded=True):
        model_option = st.selectbox("Model", list(model_options.keys()), disabled=True)
        MODEL = model_options[model_option]
    
# Initialise session state for client and messages
if "messages" not in st.session_state:
    st.session_state.messages = []

if "genai_client" not in st.session_state:
    try:
        if use_vertex:
            st.session_state.genai_client = genai.Client(vertexai=True, project=GOOGLE_CLOUD_PROJECT, location=GOOGLE_CLOUD_LOCATION)
        else:
            st.session_state.genai_client = genai.Client(api_key=GOOGLE_API_KEY)
    except Exception as e:
        st.error(f"Error: {e}")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User-Assistant chat interaction
if prompt := st.chat_input("Ask anything", accept_file=True, file_type=["jpg", "jpeg", "png"]):
  # User prompt
  with st.chat_message("user"):
    if prompt and prompt.text:
        st.markdown(prompt.text)
    
    image = None
    if prompt and prompt["files"]:
        image = prompt["files"][0]
        st.image(image)
    st.session_state.messages.append({"role": "user", "content": prompt.text})

  # Assistant response
  with st.chat_message("assistant"):
      try:
            contents = [prompt.text] if prompt.text else []
            if image:
                contents.append(PIL.Image.open(image))

            response = st.session_state.genai_client.models.generate_content(
                model=MODEL,
                contents=contents,
            )
            st.write(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
      except Exception as e:
          st.error(f"Error: {e}")
