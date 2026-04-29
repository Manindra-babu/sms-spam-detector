# 🚀 SpamGuard – Intelligent SMS Spam Detection System

![PyTorch](https://img.shields.io/badge/PyTorch-DeepLearning-red)
![Status](https://img.shields.io/badge/Deployment-Live-success)
![HuggingFace](https://img.shields.io/badge/%F0%9F%A4%97%20Space-Live-yellow)

## 📌 Overview
Spam messages are a major issue in digital communication, often used for scams and phishing attacks. This project builds a deep learning-based system that classifies SMS messages as **Spam** or **Not Spam** using advanced Natural Language Processing (NLP) techniques.

Unlike standard models, SpamGuard is built by fine-tuning a custom **GPT (Generative Pre-trained Transformer)** architecture from scratch using PyTorch.

---

## 🌐 Live Demo
The application is deployed on Hugging Face Spaces for real-time inference.

🔗 **[Click here to test the SpamGuard UI](https://huggingface.co/spaces/mani-359/spam-detector-ui)**

---

## 🎯 Features
* 📩 **Real-time Classification:** Instant spam detection via a web interface.
* 🧠 **GPT-Powered:** Uses a 124M parameter Transformer architecture.
* ⚡ **Optimized Inference:** PyTorch-based backend for millisecond response times.
* ☁️ **Cloud Native:** Dynamically pulls model weights from Hugging Face LFS.

---

## 🛠️ Tech Stack
* **Language:** Python
* **Deep Learning Framework:** PyTorch
* **Architecture:** GPT-based Transformer (Multi-Head Attention, LayerNorm, GELU)
* **Tokenization:** Tiktoken (BPE Encoding)
* **Deployment:** Hugging Face Spaces & Streamlit

---

## 🧠 Model Architecture
This project implements a high-performance Transformer model:
* **Custom Architecture:** Multi-layer Transformer blocks featuring self-attention and feed-forward networks.
* **Weights:** Fine-tuned on SMS datasets and saved as PyTorch `.pth` files.
* **Inference Pipeline:** 1. Text is tokenized using GPT-2 Byte Pair Encoding.
    2. Numerical vectors pass through 12 Transformer layers.
    3. A final classification head determines the "Spam" probability.

---

## 📊 Model Performance
* **Accuracy:** 95.67%
* **Precision:** 97.92%
* **Recall:** 93.38%

---

## 📂 Project Structure
```text
sms-spam-detector/
│── app.py                # Streamlit UI & Cloud Inference Logic
│── gpt_archticture.py    # Custom GPT Architecture & Transformer Blocks
│── requirements.txt      # Project Dependencies
│── README.md             # Documentation





