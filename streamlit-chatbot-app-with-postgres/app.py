import logging
import os
import streamlit as st
from databricks.sdk import WorkspaceClient
from postgres_utils import init_database, add_request, get_requests


w = WorkspaceClient()
client = w.serving_endpoints.get_open_ai_client()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure environment variable is set correctly
SERVING_ENDPOINT = os.getenv('SERVING_ENDPOINT')
assert SERVING_ENDPOINT, \
    ("Unable to determine serving endpoint to use for chatbot app. If developing locally, "
     "set the SERVING_ENDPOINT environment variable to the name of your serving endpoint. If "
     "deploying to a Databricks app, include a serving endpoint resource named "
     "'serving_endpoint' with CAN_QUERY permissions, as described in "
     "https://docs.databricks.com/aws/en/generative-ai/agent-framework/chat-app#deploy-the-databricks-app")

def get_user_info():
    headers = st.context.headers
    return dict(
        user_name=headers.get("X-Forwarded-Preferred-Username"),
        user_email=headers.get("X-Forwarded-Email"),
        user_id=headers.get("X-Forwarded-User"),
    )

user_info = get_user_info()

# Initialize database
if not init_database(w):
    st.stop()

# Streamlit app
if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

st.title("🧱 Chatbot App")

# Adding a past chats section. Currently get_requests only fetches the last 3 requests.
@st.fragment
def display_requests(w):
    with st.expander("Past chats"):
    
        chats = get_requests(w)
    
        if not chats:
            st.info("No past chats. Please talk to me!")
        else:
            for id, prompt, response, created_at in chats:
                col1, col2 = st.columns([0.2, 0.7])
            
                with col1:
                    st.markdown(f"{prompt}")
                    st.caption(f"Created: {created_at.strftime('%Y-%m-%d %H:%M')}")
            
                with col2:
                    st.markdown(f"{response}")

# Display past requests
display_requests(w)

st.markdown(
    """
    <div style='font-size: 20px; color: #E97451;'>
         💬 Talk to your agent!
    </div>
    """,
    unsafe_allow_html=True
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What can you do?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        # Query the Databricks serving endpoint.
        # Streaming as a tool calling agent goes through a list of "thoughts"
        streaming_response = client.responses.create(model=SERVING_ENDPOINT, input=st.session_state.messages, stream=True)
        resp = []
        for chunk in streaming_response:
            if (not hasattr(chunk.item, 'content') or (chunk.item.content is None)):
                pass
            else: 
                resp.append(chunk.item.content[0].text)
        assistant_response = resp
        # We only need the final response
        st.markdown(assistant_response[-1])
        # Log in database
        try:
            add_request(prompt, assistant_response[-1],w)
        except Exception as e:
            logger.error(f"Failed to log request to database: {e}")

    # Add final response to chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_response[-1]})



