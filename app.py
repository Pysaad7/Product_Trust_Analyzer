import streamlit as st
from scraper import fetch_reviews
from textblob import TextBlob
import pandas as pd

# Page Configuration
st.set_page_config(page_title="AI Trust Analyzer", page_icon="🛡️", layout="wide")

st.title("🛡️ AI Product Trust & Sentiment Analyzer")
st.markdown("---")

# Sidebar for Info
st.sidebar.header("About Project")
st.sidebar.info("Yeh system AI ke zariye product reviews ko analyze karta hai aur batata hai ke product kharidna safe hai ya nahi.")

# Input Section
product_url = st.text_input("🔗 Paste Product Link (Amazon, Daraz, etc.):")

if st.button("Analyze Sentiment & Trust"):
    if product_url:
        with st.spinner('🕵️ AI is scanning the page... Please wait (15-20s)'):
            results = fetch_reviews(product_url)
            
        if results:
            # Calculation logic
            total_polarity = 0
            pos, neg, neu = 0, 0, 0
            
            for r in results:
                analysis = TextBlob(r)
                score = analysis.sentiment.polarity
                total_polarity += score
                if score > 0: pos += 1
                elif score < 0: neg += 1
                else: neu += 1
            
            avg_sentiment = total_polarity / len(results)
            trust_score = (avg_sentiment + 1) * 50

            # --- TOP METRICS ---
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Reviews Found", len(results))
            col2.metric("Trust Score", f"{trust_score:.1f}%")
            
            with col3:
                if trust_score > 70:
                    st.success("✅ HIGH TRUST")
                elif trust_score > 40:
                    st.warning("⚠️ MEDIUM RISK")
                else:
                    st.error("🚨 HIGH RISK")

            st.markdown("---")

            # --- CHARTS & ANALYSIS ---
            c1, c2 = st.columns([1, 1])
            
            with c1:
                st.subheader("📊 Sentiment Distribution")
                chart_data = pd.DataFrame({
                    'Sentiment': ['Positive 😊', 'Neutral 😐', 'Negative 😡'],
                    'Count': [pos, neu, neg]
                })
                st.bar_chart(chart_data.set_index('Sentiment'))

            with c2:
                st.subheader("📝 AI Recommendation")
                if trust_score > 75:
                    st.write("Dikhne mein ye product bilkul authentic lag raha hai. Zyadatar customers khush hain.")
                elif trust_score > 45:
                    st.write("Mixed feedback hai. Kuch log khush hain lekin kuch ko maslay aye hain. Zara soch samajh kar order karein.")
                else:
                    st.write("Bohat zyada negative feedback hai. Is seller se bachna behtar hai.")

            # --- DETAILED REVIEWS ---
            st.markdown("---")
            with st.expander("🔍 Click to view extracted reviews"):
                for i, r in enumerate(results):
                    st.write(f"**{i+1}.** {r}")
        else:
            st.error("Koi review nahi mil saka. Shayad link sahi nahi hai ya page load nahi hua.")
    else:
        st.warning("Pehle link to dalein!")