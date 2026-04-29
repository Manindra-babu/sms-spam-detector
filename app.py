import os
import streamlit as st
import torch
import tiktoken
from pathlib import Path
from huggingface_hub import hf_hub_download

# Fix relative paths
os.chdir(Path(__file__).parent)
from gpt_archticture import GPTModel

# Page Config
st.set_page_config(page_title="Spam Classifier UI", page_icon="🛡️", layout="centered")

st.title("✉️ SMS Spam Classifier")
st.write("Enter an SMS message below to check if it's spam or not.")

@st.cache_resource(show_spinner="Downloading model weights from Hugging Face...")
def load_model():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = tiktoken.get_encoding("gpt2")
    
    # Load model architecture for GPT-2 Small (124M)
    BASE_CONFIG = {
        "vocab_size": 50257,
        "context_length": 1024,
        "drop_rate": 0.0,
        "qkv_bias": True,
        "emb_dim": 768,
        "n_layers": 12,
        "n_heads": 12
    }
    
    model = GPTModel(BASE_CONFIG)
    num_classes = 2
    model.out_head = torch.nn.Linear(in_features=BASE_CONFIG["emb_dim"], out_features=num_classes)
    
    # --- NEW: Fetch weights directly from your Hugging Face repo ---
    try:
        model_path = hf_hub_download(
            repo_id="mani-359/sms-spam-detector", 
            filename="review_classifier.pth",
            token="YOUR_HUGGINGFACE_TOKEN_HERE" # Added token for private repo access
        )
        model.load_state_dict(torch.load(model_path, map_location=device, weights_only=True))
    except Exception as e:
        st.error(f"Failed to load model from Hugging Face. Error: {e}")
        return None, None, None
    # ---------------------------------------------------------------

    model.to(device)
    model.eval()
    
    return model, tokenizer, device

model, tokenizer, device = load_model()

def classify_sms(text, model, tokenizer, device, max_length=256, pad_token_id=50256):
    input_ids = tokenizer.encode(text)
    
    # Truncate and pad
    supported_context_length = model.pos_emb.weight.shape[0]
    input_ids = input_ids[:min(max_length, supported_context_length)]
    input_ids += [pad_token_id] * (max_length - len(input_ids))
    
    input_tensor = torch.tensor(input_ids, device=device).unsqueeze(0)
    
    with torch.no_grad():
        logits = model(input_tensor)[:, -1, :]
        
    predicted_label = torch.argmax(logits, dim=-1).item()
    return "Spam 🚫" if predicted_label == 1 else "Not Spam ✅"

def set_text(text):
    st.session_state.user_text = text

st.markdown("💡 **Try an example:**")
col1, col2, col3 = st.columns(3)
col1.button("💳 Fake Netflix (Spam)", on_click=set_text, args=("URGENT: Your Netflix account has been suspended due to an unrecognized login. Click here immediately to verify your billing details: http://netflix-secure-update24.com/auth",))
col2.button("📦 Fake Delivery (Spam)", on_click=set_text, args=("Amazon Alert: Your package #AMZ99482-B is pending delivery. A $2.99 customs fee is required. Please pay at https://amzn-delivery-fees.net to release your parcel within 24hrs.",))
col3.button("☕ Normal Coffee (Ham)", on_click=set_text, args=("Hey, are we still meeting up for coffee later this afternoon? Need to confirm our plans.",))

if "user_text" not in st.session_state:
    st.session_state.user_text = ""

user_input = st.text_area("Your Message:", key="user_text", placeholder="Type your SMS message here...", height=150)

if st.button("Check", type="primary", use_container_width=True):
    if user_input.strip() == "":
        st.error("Please enter a message to classify.")
    elif model is None:
        st.error("Model unavailable.")
    else:
        with st.spinner("Classifying..."):
            result = classify_sms(user_input, model, tokenizer, device)
            
        st.markdown("### Result:")
        if "Spam" in result:
            st.error(f"**{result}**")
        else:
            st.success(f"**{result}**")
