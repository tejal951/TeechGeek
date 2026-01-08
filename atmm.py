import streamlit as st
import time
import os

# ---------------- CONFIG ---------------- #

st.set_page_config("ATM Banking System", layout="wide")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "acc.txt")

# ---------------- FILE HANDLING ---------------- #

def ensure_file():
    """Ensure acc.txt exists (Streamlit Cloud safe)"""
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            f.write(
                "User:admin\n"
                "PIN:1234\n"
                "Balance:5000\n"
                "Transactions:\n"
                "Account created\n"
                "---\n"
            )

def load_users():
    ensure_file()
    users = {}

    with open(FILE_PATH, "r", encoding="utf-8") as f:
        content = f.read().strip()

    if not content:
        return users

    for block in content.split("---"):
        block = block.strip()
        if not block:
            continue

        lines = [l.strip() for l in block.splitlines()]
        try:
            user = lines[0].split(":", 1)[1].lower()
            pin = lines[1].split(":", 1)[1]
            bal = float(lines[2].split(":", 1)[1])
            tx = lines[4:] if len(lines) > 4 else []
            users[user] = {"PIN": pin, "Balance": bal, "Tx": tx}
        except Exception:
            continue

    return users

def save_users(users):
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        for u, d in users.items():
            f.write(f"User:{u}\n")
            f.write(f"PIN:{d['PIN']}\n")
            f.write(f"Balance:{d['Balance']}\n")
            f.write("Transactions:\n")
            for t in d["Tx"]:
                f.write(f"{t}\n")
            f.write("---\n")

# ---------------- SESSION ---------------- #

if "logged" not in st.session_state:
    st.session_state.logged = False
    st.session_state.page = "login"

users = load_users()

# ---------------- UI STYLE ---------------- #

st.markdown("""
<style>
body {background:#0b0f14;}
.big-title {font-size:36px;color:#3b82f6;font-weight:700}
.card {
    background:#111827;
    padding:25px;
    border-radius:18px;
    box-shadow:0 0 20px #000;
}
button {border-radius:12px!important;}
</style>
""", unsafe_allow_html=True)

# ---------------- LOGIN ---------------- #

if not st.session_state.logged:
    st.markdown("<div class='big-title'>🏦 ATM Login</div>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        user = st.text_input("Card Number / Username").strip().lower()
        pin = st.text_input("PIN", type="password").strip()

        if st.button("🔐 Insert Card / Login"):
            if user in users and pin == users[user]["PIN"]:
                st.session_state.logged = True
                st.session_state.user = user
                st.session_state.page = "balance"
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid credentials")

        st.markdown("</div>", unsafe_allow_html=True)

    st.stop()

# ---------------- SIDEBAR ---------------- #

st.sidebar.markdown("## 🏦 ATM Menu")

if st.sidebar.button("💰 Check Balance"):
    st.session_state.page = "balance"
if st.sidebar.button("➕ Deposit Money"):
    st.session_state.page = "deposit"
if st.sidebar.button("➖ Withdraw Money"):
    st.session_state.page = "withdraw"
if st.sidebar.button("🧾 Transaction History"):
    st.session_state.page = "history"
if st.sidebar.button("🚪 Logout"):
    st.session_state.logged = False
    st.rerun()

user = st.session_state.user

# ---------------- PAGES ---------------- #

st.markdown("<div class='card'>", unsafe_allow_html=True)

if st.session_state.page == "balance":
    st.subheader("💰 Current Balance")
    st.metric("Available Balance", f"₹ {users[user]['Balance']}")

elif st.session_state.page == "deposit":
    st.subheader("➕ Deposit Money")
    amt = st.number_input("Enter amount", min_value=1, step=100)
    if st.button("Confirm Deposit"):
        with st.spinner("Processing cash..."):
            time.sleep(1)
        users[user]["Balance"] += amt
        users[user]["Tx"].insert(0, f"Deposited ₹{amt}")
        save_users(users)
        st.success("Deposit successful")

elif st.session_state.page == "withdraw":
    st.subheader("➖ Withdraw Money")
    amt = st.number_input("Enter amount", min_value=1, step=100)
    if st.button("Confirm Withdrawal"):
        if amt <= users[user]["Balance"]:
            with st.spinner("Dispensing cash..."):
                time.sleep(1)
            users[user]["Balance"] -= amt
            users[user]["Tx"].insert(0, f"Withdrew ₹{amt}")
            save_users(users)
            st.success("Please collect your cash")
        else:
            st.error("Insufficient balance")

elif st.session_state.page == "history":
    st.subheader("🧾 Transaction History")
    for t in users[user]["Tx"]:
        st.write("•", t)

st.markdown("</div>", unsafe_allow_html=True)

