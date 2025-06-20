import streamlit as st
from ctransformers import AutoModelForCausalLM

# Load the local language model (cached to avoid reloading)
@st.cache_resource
def load_model():
    return AutoModelForCausalLM.from_pretrained(
        "TheBloke/orca_mini_3b-GGUF",          # Hugging Face model path
        model_file="orca-mini-3b.Q4_0.gguf",   # Local model file (downloaded separately)
        model_type="llama",                    # Model type
        gpu_layers=0                           # Set >0 to use GPU layers (if available)
    )

model = load_model()

# Simple chatbot UI
def run_chatbot():
    st.title("🤖 Answer Assistant")
    st.markdown("Ask me anything related to advertising, marketing, or strategy!")

    user_input = st.text_input("💬 Your Question:")

    if user_input:
        with st.spinner("Generating response..."):
            response = model(user_input, max_new_tokens=100)
            st.success(response)
