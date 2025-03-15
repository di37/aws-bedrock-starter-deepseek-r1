# app/streamlit_app.py
import streamlit as st
from app.config import load_config
from app.bedrock_client import BedrockClientDeepseek

def initialize_session_state():
    """Initialize session state variables if they don't exist."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "client" not in st.session_state:
        config = load_config()
        st.session_state.client = BedrockClientDeepseek(config)
    
    # Default settings
    if "system_prompt" not in st.session_state:
        st.session_state.system_prompt = "You're a helpful assistant that specializes in physics."
    
    if "temperature" not in st.session_state:
        st.session_state.temperature = 0.7
    
    if "max_tokens" not in st.session_state:
        st.session_state.max_tokens = 4096
    
    if "top_p" not in st.session_state:
        st.session_state.top_p = 0.9
    
    if "use_streaming" not in st.session_state:
        st.session_state.use_streaming = True

def display_chat_history():
    """Display the chat history from session state."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

def render_sidebar():
    """Render the sidebar with model settings."""
    with st.sidebar:
        st.title("Model Settings")
        
        # System prompt
        st.session_state.system_prompt = st.text_area(
            "System Prompt",
            value=st.session_state.system_prompt,
            height=150,
            help="The system prompt guides the AI's behavior and expertise."
        )
        
        # Temperature slider
        st.session_state.temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.temperature,
            step=0.05,
            help="Higher values make output more random, lower values more deterministic."
        )
        
        # Max tokens slider
        st.session_state.max_tokens = st.slider(
            "Max Tokens",
            min_value=256,
            max_value=8192,
            value=st.session_state.max_tokens,
            step=256,
            help="Maximum number of tokens in the response."
        )
        
        # Top-p slider
        st.session_state.top_p = st.slider(
            "Top P",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.top_p,
            step=0.05,
            help="Nucleus sampling parameter. Lower values make output more focused."
        )
        
        # Streaming toggle
        st.session_state.use_streaming = st.toggle(
            "Enable Streaming",
            value=st.session_state.use_streaming,
            help="Stream the response token by token or receive the complete response."
        )
        
        # Clear chat button
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.rerun()

def handle_user_input(user_input):
    """Process user input and get model response."""
    if not user_input:
        return
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.write(user_input)
    
    # Get current settings
    system_message = st.session_state.system_prompt
    temperature = st.session_state.temperature
    max_tokens = st.session_state.max_tokens
    top_p = st.session_state.top_p
    use_streaming = st.session_state.use_streaming
    
    # Initialize response placeholder
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        # Create expandable section for reasoning (if available)
        with st.expander("View AI reasoning"):
            reasoning_placeholder = st.empty()

        # Initialize variables for collecting reasoning and final response
        reasoning_content = ""
        final_content = ""
        
        # Prepare conversation with context from chat history
        if len(st.session_state.messages) > 1:
            # Get previous messages to provide context
            previous_context = "\n\nPrevious conversation:\n"
            # Include up to last 5 exchanges (10 messages)
            start_idx = max(0, len(st.session_state.messages) - 11)
            for i in range(start_idx, len(st.session_state.messages) - 1):
                msg = st.session_state.messages[i]
                previous_context += f"{msg['role'].capitalize()}: {msg['content']}\n"
            
            # Add context to the current query
            enhanced_query = f"{previous_context}\n\nCurrent question: {user_input}"
        else:
            enhanced_query = user_input
        
        # Create the conversation object
        conversation = st.session_state.client.create_conversation(enhanced_query, system_message)
        
        # Process the model request based on streaming preference
        if use_streaming:
            # Stream the response
            for token in st.session_state.client.stream_query_model(
                conversation, max_tokens=max_tokens, temperature=temperature, top_p=top_p
            ):
                if token["part"] == "reasoning":
                    reasoning_content += token["text"]
                    reasoning_placeholder.markdown(reasoning_content)
                
                elif token["part"] == "final":
                    final_content += token["text"]
                    response_placeholder.markdown(final_content)
        else:
            # Show a spinner while waiting for the complete response
            with st.spinner("Thinking..."):
                response = st.session_state.client.query_model(
                    conversation, max_tokens=max_tokens, temperature=temperature, top_p=top_p
                )
                reasoning_content = response["reasoning_text"]
                final_content = response["response_text"]
                
                # Display the complete response
                reasoning_placeholder.markdown(reasoning_content)
                response_placeholder.markdown(final_content)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": final_content})

def main():
    """Main function to run the Streamlit application."""
    # Set page config
    st.set_page_config(
        page_title="Physics Assistant",
        page_icon="🔭",
        layout="wide"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Render sidebar with settings
    render_sidebar()
    
    # Display header
    st.title("🐋 Deepseek-R1 AWS Bedrock")
    st.markdown("Ask me any physics questions, and follow up with more questions!")
    
    # Display chat history
    display_chat_history()
    
    # Get user input
    user_input = st.chat_input("Ask a physics question...")
    
    # Handle user input
    if user_input:
        handle_user_input(user_input)

if __name__ == "__main__":
    main()