import streamlit as st
from main import fetch_all_news

# 1. Page Configuration
st.set_page_config(
    page_title="Embedded News Hub",
    page_icon="⚡",
    layout="wide"
)

# 2. Custom CSS Injection for Dark Tech Theme & Compact Cards Grid
st.markdown("""
    <style>
    /* Force main background and text colors */
    .stApp {
        background-color: #0B0F19;
        color: #e2e8f0;
    }
    
    /* Compact Card styling inside grid columns */
    div[data-testid="stVerticalBlock"] div[data-testid="stContainer"] {
        background-color: #111827;
        border: 1px solid #1f2937;
        border-radius: 8px;
        padding: 12px 16px; /* مساحات داخلية أصغر وأكثر تناسقاً */
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.4);
        height: 100%;
        transition: all 0.3s ease;
    }
    div[data-testid="stVerticalBlock"] div[data-testid="stContainer"]:hover {
        border-color: #3b82f6;
        box-shadow: 0 6px 15px rgba(59, 130, 246, 0.15);
    }

    /* Make headers smaller and compact inside containers */
    div[data-testid="stContainer"] h3 {
        font-size: 1.05rem !important;
        line-height: 1.35 !important;
        margin-bottom: 4px !important;
    }

    /* Style primary buttons */
    .stButton>button {
        background-color: #3b82f6;
        color: #FFFFFF;
        border-radius: 8px;
        font-weight: 600;
        border: none;
        padding: 0.4rem 0.8rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #60a5fa;
        color: #FFFFFF;
        box-shadow: 0 0 15px rgba(96, 165, 250, 0.5);
    }

    /* Custom styling for links */
    a {
        color: #60a5fa !important;
        text-decoration: none;
        font-weight: 500;
        font-size: 0.9rem;
    }
    a:hover {
        text-decoration: underline;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Header and Title
st.title("⚡ Embedded & Automotive Systems Aggregator")
st.caption("A centralized dashboard to track cutting-edge embedded systems, firmware, and automotive software engineering news.")
st.divider()

# 4. Control Panel
col1, col2 = st.columns([1, 4])
with col1:
    fetch_btn = st.button("🔄 Fetch Latest News", use_container_width=True)

# 5. Fetch Logic
if fetch_btn or "articles" not in st.session_state:
    with st.spinner("Fetching the latest news from the world of embedded systems and automotive software engineering..."):
        st.session_state["articles"] = fetch_all_news()

articles = st.session_state.get("articles", [])

if not articles:
    st.info("No articles found at the moment.")
else:
    st.success(f"Successfully loaded {len(articles)} articles!")
    
    # 6. Grid Layout: Display 3 Cards per row
    cards_per_row = 3
    
    # Loop through articles in chunks of 3
    for i in range(0, len(articles), cards_per_row):
        row_articles = articles[i:i + cards_per_row]
        cols = st.columns(cards_per_row)
        
        for idx, item in enumerate(row_articles):
            with cols[idx]:
                with st.container(border=True):
                    # Title & Badge
                    if item["is_new"]:
                        st.subheader(f"✨ {item['title']}")
                    else:
                        st.subheader(item["title"])
                        
                    st.caption(f"📌 Source: **{item['source']}**")
                    
                    # Compact summary expander
                    with st.expander("📖 Read Summary"):
                        st.write(item["summary"])
                        
                    # Action link
                    st.markdown(f"🔗 [Read Article]({item['link']})")