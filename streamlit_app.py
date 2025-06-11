import os, io, streamlit as st
import google.genai as genai
import PIL.Image

# Determine if Vertex AI is to be used
use_vertex = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "false").lower() == "true"

if use_vertex:
    # If using Vertex AI, project and location are required
    google_cloud_project = os.getenv("GOOGLE_CLOUD_PROJECT")
    google_cloud_location = os.getenv("GOOGLE_CLOUD_LOCATION")
    google_api_key = None

    if not google_cloud_project or google_cloud_project.strip() == "":
        raise EnvironmentError("GOOGLE_CLOUD_PROJECT environment variable is required but not set when using Vertex AI.")
    if not google_cloud_location or google_cloud_location.strip() == "":
        raise EnvironmentError("GOOGLE_CLOUD_LOCATION environment variable is required but not set when using Vertex AI.")
else:
    # If not using Vertex AI, Google API key is required
    google_api_key = os.getenv("GOOGLE_API_KEY")
    google_cloud_project = None
    google_cloud_location = None

    if not google_api_key or google_api_key.strip() == "":
        raise EnvironmentError("GOOGLE_API_KEY environment variable is required but not set when not using Vertex AI.")

model_options = {
    "Gemini 2.0 Flash": "gemini-2.0-flash",
    "Gemini 2.5 Flash": "gemini-2.5-flash-preview-05-20"
}

# Streamlit app config
st.set_page_config(page_title="Gemini Chatbot", page_icon="💬", initial_sidebar_state="auto")

with st.sidebar:
    st.title("💬 Gemini Chatbot")
    st.caption(
        """
        This chatbot uses Google Gemini to answer your questions. Upload an image and/or ask a question to get started.
        """
    )
    with st.expander("**⚙️ Model Settings**", expanded=True):
        model_option = st.selectbox("Model", list(model_options.keys()), disabled=False)
        model = model_options[model_option]
    
# Initialise session state for client and messages
if "messages" not in st.session_state:
    st.session_state.messages = []

if "genai_client" not in st.session_state:
    try:
        if use_vertex:
            st.session_state.genai_client = genai.Client(vertexai=True, project=google_cloud_project, location=google_cloud_location)
        else:
            st.session_state.genai_client = genai.Client(api_key=google_api_key)
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
            with st.spinner("Please wait..."):
                contents = [prompt.text] if prompt.text else []
                if image:
                    contents.append(PIL.Image.open(image))

                response = st.session_state.genai_client.models.generate_content(
                    model=model,
                    contents=contents,
                )
                st.write(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
      except Exception as e:
          st.error(f"Error: {e}")
