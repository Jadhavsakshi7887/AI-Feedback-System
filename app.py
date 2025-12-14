import streamlit as st
import pandas as pd
import uuid
from llm_utils import call_llm
from datetime import datetime

DATA_PATH = "data/reviews.csv"

def load_data():
    try:
        return pd.read_csv(DATA_PATH)
    except:
        return pd.DataFrame(columns=[
            "id","rating","review",
            "ai_response","summary",
            "recommended_action","timestamp"
        ])

def save_data(df):
    df.to_csv(DATA_PATH, index=False)

st.sidebar.title("Dashboard")
page = st.sidebar.radio("Go to", ["User", "Admin"])

df = load_data()

# ---------------- USER DASHBOARD ----------------
if page == "User":
    st.title("Submit a Review")

    rating = st.slider("Rating", 1, 5, 3)
    review = st.text_area("Your Review")

    if st.button("Submit"):
        response_prompt = f"Write a polite response to this review:\n{review}"
        ai_response = call_llm(response_prompt)

        summary = call_llm(f"Summarize this review:\n{review}")
        action = call_llm(f"Suggest an action for this feedback:\n{review}")

        new_row = {
            "id": str(uuid.uuid4()),
            "rating": rating,
            "review": review,
            "ai_response": ai_response,
            "summary": summary,
            "recommended_action": action,
            "timestamp": datetime.now()
        }

        df = pd.concat([df, pd.DataFrame([new_row])])
        save_data(df)

        st.success("Submitted!")
        st.write("### AI Response")
        st.write(ai_response)

# ---------------- ADMIN DASHBOARD ----------------
else:
    st.title("Admin Dashboard")
    st.dataframe(df)

    st.metric("Average Rating", round(df["rating"].mean(), 2) if len(df) else 0)
