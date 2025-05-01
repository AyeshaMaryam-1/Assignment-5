import streamlit as st
import hashlib
import json
import time
import uuid
import base64
from cryptography.fernet import Fernet

# ---------------- Session Initialization ---------------- #
if 'failed_attempts' not in st.session_state:
    st.session_state.failed_attempts = 0
if 'stored_data' not in st.session_state:
    st.session_state.stored_data = {}
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"
if 'last_attempt_time' not in st.session_state:
    st.session_state.last_attempt_time = 0

# ---------------- Utility Functions ---------------- #
def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

def generate_key_from_passkey(passkey):
    hashed = hashlib.sha256(passkey.encode()).digest()
    return base64.urlsafe_b64encode(hashed[:32])

def encrypt_data(text, passkey):
    key = generate_key_from_passkey(passkey)
    return Fernet(key).encrypt(text.encode()).decode()

def decrypt_data(encrypted_text, passkey, data_id):
    try:
        if data_id in st.session_state.stored_data:
            stored = st.session_state.stored_data[data_id]
            if stored["passkey"] == hash_passkey(passkey):
                key = generate_key_from_passkey(passkey)
                decrypted = Fernet(key).decrypt(encrypted_text.encode()).decode()
                st.session_state.failed_attempts = 0
                return decrypted
        st.session_state.failed_attempts += 1
        st.session_state.last_attempt_time = time.time()
        return None
    except Exception:
        st.session_state.failed_attempts += 1
        st.session_state.last_attempt_time = time.time()
        return None

def generate_data_id():
    return str(uuid.uuid4())

def reset_failed_attempts():
    st.session_state.failed_attempts = 0

def change_page(page):
    st.session_state.current_page = page

# ---------------- UI Setup ---------------- #
st.set_page_config(page_title="Secure Encryption App", page_icon="🔐", layout="centered")
st.title("🔐 Secure Data Encryption System")

# ---------------- Sidebar Navigation ---------------- #
menu = ["Home", "Store Data", "Retrieve Data", "Login"]
choice = st.sidebar.selectbox("📍 Navigation", menu, index=menu.index(st.session_state.current_page))
st.session_state.current_page = choice

# ---------------- Access Control ---------------- #
if st.session_state.failed_attempts >= 3:
    st.session_state.current_page = "Login"
    st.warning("🔒 Too many failed attempts. Please reauthorize.")

# ---------------- Pages ---------------- #

# HOME
if st.session_state.current_page == "Home":
    st.subheader("🏠 Welcome to the Secure Data System")
    st.write("Securely **store** and **retrieve** data using a secret passkey.")
    st.success(f"🔐 Encrypted entries stored: {len(st.session_state.stored_data)}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝 Store New Data", use_container_width=True):
            change_page("Store Data")
    with col2:
        if st.button("🔍 Retrieve Data", use_container_width=True):
            change_page("Retrieve Data")

# STORE DATA
elif st.session_state.current_page == "Store Data":
    st.subheader("📦 Store Data Securely")
    data = st.text_area("🔏 Enter your data")
    passkey = st.text_input("🔐 Create Passkey", type="password")
    confirm_passkey = st.text_input("🔐 Confirm Passkey", type="password")

    if st.button("Encrypt & Save"):
        if not (data and passkey and confirm_passkey):
            st.error("⚠️ All fields are required.")
        elif passkey != confirm_passkey:
            st.error("❗ Passkeys do not match.")
        else:
            data_id = generate_data_id()
            encrypted = encrypt_data(data, passkey)
            st.session_state.stored_data[data_id] = {
                "encrypted_text": encrypted,
                "passkey": hash_passkey(passkey)
            }
            st.success("✅ Data encrypted and stored.")
            st.code(data_id, language="text")
            st.info("🔖 Save your Data ID for future retrieval.")

# RETRIEVE DATA
elif st.session_state.current_page == "Retrieve Data":
    st.subheader("🔓 Retrieve Encrypted Data")
    st.info(f"Attempts remaining: {3 - st.session_state.failed_attempts}")

    data_id = st.text_input("🆔 Enter Data ID")
    passkey = st.text_input("🔐 Enter Passkey", type="password")

    if st.button("Decrypt"):
        if not (data_id and passkey):
            st.error("⚠️ Both fields are required.")
        elif data_id not in st.session_state.stored_data:
            st.error("❌ Invalid Data ID.")
        else:
            encrypted_text = st.session_state.stored_data[data_id]["encrypted_text"]
            decrypted = decrypt_data(encrypted_text, passkey, data_id)
            if decrypted:
                st.success("✅ Decryption successful!")
                st.code(decrypted, language="text")
            else:
                st.error(f"❌ Incorrect passkey. Attempts left: {3 - st.session_state.failed_attempts}")
                if st.session_state.failed_attempts >= 3:
                    st.warning("🔒 Too many failed attempts. Redirecting...")
                    st.rerun()

# LOGIN (Reauthorization)
elif st.session_state.current_page == "Login":
    st.subheader("🔐 Reauthorization Required")

    if time.time() - st.session_state.last_attempt_time < 10:
        wait_time = int(10 - (time.time() - st.session_state.last_attempt_time))
        st.warning(f"⏳ Please wait {wait_time} seconds before retrying.")
    else:
        master_pass = st.text_input("🔑 Master Password", type="password")
        if st.button("Login"):
            if master_pass == "admin123":  # Replace for production
                reset_failed_attempts()
                st.success("✅ Access restored.")
                change_page("Home")
                st.rerun()
            else:
                st.error("❌ Incorrect master password.")

# ---------------- Footer ---------------- #
st.markdown("---")
st.markdown("Secure Data Encryption App — Educational Project")