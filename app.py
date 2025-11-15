"""
Streamlit Frontend - AI-Powered Podcast Platform
"""
import streamlit as st
import requests
from typing import Optional
import os
from datetime import datetime

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# Custom CSS for Zeabur-inspired Theme
def load_custom_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    /* Global Styles */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Container - Zeabur Pure Black */
    .main {
        background: #000000 !important;
        color: #ffffff;
    }
    
    .block-container {
        max-width: 1200px !important;
        padding: 4rem 2rem !important;
    }
    
    /* Hero Section */
    .hero-title {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 4rem !important;
        line-height: 1.1;
        letter-spacing: -2px;
        margin-bottom: 1.5rem !important;
        background: linear-gradient(to right, #ffffff 20%, #999 40%, #ffffff 60%, #999 80%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: shine 3s linear infinite;
    }
    
    @keyframes shine {
        to {
            background-position: 200% center;
        }
    }
    
    /* Subtitle - Zeabur Style */
    .subtitle {
        font-size: 1.5rem;
        color: #666;
        font-weight: 400;
        line-height: 1.6;
        margin-bottom: 3rem;
    }
    
    .subtitle .highlight {
        color: #fff;
        font-weight: 600;
    }
    
    /* Animated Text */
    .animated-text {
        background: linear-gradient(90deg, #667eea, #764ba2, #667eea);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradient 3s ease infinite;
    }
    
    @keyframes gradient {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    /* Cards - Zeabur Pure Black */
    .episode-card {
        background: #0a0a0a;
        border: 1px solid #1a1a1a;
        border-radius: 24px;
        padding: 2.5rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .episode-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05), transparent);
        opacity: 0;
        transition: opacity 0.4s ease;
        pointer-events: none;
    }
    
    .episode-card:hover {
        border-color: #2a2a2a;
        transform: translateY(-8px);
        box-shadow: 0 24px 80px rgba(0, 0, 0, 0.8);
    }
    
    .episode-card:hover::before {
        opacity: 1;
    }
    
    .stContainer > div {
        background: transparent;
        border: none;
        padding: 0;
    }
    
    /* Buttons - Zeabur Style */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 1rem 2.5rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.6) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) scale(0.98) !important;
    }
    
    /* CTA Button */
    .cta-button {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 14px;
        padding: 1.2rem 3rem;
        font-weight: 600;
        font-size: 1.1rem;
        text-decoration: none;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        cursor: pointer;
    }
    
    .cta-button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.6);
        text-decoration: none;
        color: white;
    }
    
    /* Input Fields - Zeabur Pure Black */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: #0a0a0a !important;
        border: 1px solid #1a1a1a !important;
        border-radius: 16px !important;
        color: #ffffff !important;
        padding: 1.2rem !important;
        font-size: 1rem !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #2a2a2a !important;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.08) !important;
        background: #0f0f0f !important;
        outline: none !important;
    }
    
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: #555 !important;
    }
    
    /* File Uploader - Zeabur Pure Black */
    .stFileUploader > div {
        background: #0a0a0a !important;
        border: 2px dashed #1a1a1a !important;
        border-radius: 20px !important;
        padding: 3rem !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        text-align: center !important;
    }
    
    .stFileUploader > div:hover {
        border-color: #2a2a2a !important;
        background: #0f0f0f !important;
        transform: translateY(-4px) !important;
    }
    
    .stFileUploader label {
        color: #888 !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
    }
    
    /* Hide Sidebar */
    [data-testid="stSidebar"] {
        display: none !important;
    }
    
    [data-testid="collapsedControl"] {
        display: none !important;
    }
    
    /* Adjust main content width */
    .main .block-container {
        max-width: 1400px !important;
        padding-left: 4rem !important;
        padding-right: 4rem !important;
    }
    
    /* Divider - Zeabur Pure Black */
    hr {
        border: none;
        border-top: 1px solid #1a1a1a;
        margin: 4rem 0;
    }
    
    /* Success/Error Messages - Zeabur Style */
    .stSuccess {
        background: #0a0a0a !important;
        border: 1px solid #1a4d1a !important;
        border-radius: 16px !important;
        padding: 1.2rem !important;
        color: #4ade80 !important;
    }
    
    .stError {
        background: #0a0a0a !important;
        border: 1px solid #4d1a1a !important;
        border-radius: 16px !important;
        padding: 1.2rem !important;
        color: #f87171 !important;
    }
    
    .stWarning {
        background: #0a0a0a !important;
        border: 1px solid #4d3d1a !important;
        border-radius: 16px !important;
        padding: 1.2rem !important;
        color: #fbbf24 !important;
    }
    
    /* Audio Player - Zeabur Pure Black */
    audio {
        width: 100%;
        height: 60px;
        border-radius: 16px;
        background: #0a0a0a;
        border: 1px solid #1a1a1a;
        transition: all 0.4s ease;
    }
    
    audio:hover {
        border-color: #2a2a2a;
        background: #0f0f0f;
    }
    
    /* Image - Zeabur Style */
    img {
        border-radius: 20px;
        box-shadow: 0 12px 48px rgba(0, 0, 0, 0.8);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid #1a1a1a;
    }
    
    img:hover {
        transform: scale(1.03);
        box-shadow: 0 16px 64px rgba(0, 0, 0, 0.9);
        border-color: #2a2a2a;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Caption Text - Zeabur Pure Black */
    .caption {
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        color: #555;
        font-weight: 400;
        letter-spacing: 0;
    }
    
    /* Small Text */
    .text-sm {
        font-size: 1rem;
        color: #666;
        font-weight: 400;
    }
    
    /* Muted Text */
    .text-muted {
        color: #444;
        font-size: 0.95rem;
    }
    
    /* Heading Styles */
    h2 {
        font-weight: 800 !important;
        letter-spacing: -1px !important;
        color: #fff !important;
    }
    
    h3 {
        font-weight: 700 !important;
        letter-spacing: -0.5px !important;
        color: #fff !important;
    }
    
    /* Stats Badge - Zeabur Pure Black */
    .stat-badge {
        background: #0a0a0a;
        border: 1px solid #1a1a1a;
        border-radius: 12px;
        padding: 0.7rem 1.4rem;
        display: inline-block;
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        font-weight: 600;
        color: #888;
        margin: 0.25rem;
        transition: all 0.4s ease;
    }
    
    .stat-badge:hover {
        border-color: #2a2a2a;
        background: #0f0f0f;
        color: #aaa;
        transform: translateY(-2px);
    }
    
    /* Feature Icon */
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    /* Section Title */
    .section-title {
        font-size: 2.5rem;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 1rem;
        color: #fff;
    }
    
    /* Grid Layout */
    .grid-2 {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 2rem;
    }
    
    .grid-3 {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.5rem;
    }
    
    /* Pulse Animation */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .pulse {
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
    
    /* Glow Effect */
    .glow {
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.6),
                    0 0 40px rgba(102, 126, 234, 0.4),
                    0 0 60px rgba(102, 126, 234, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="AI Podcast Platform",
        page_icon="🎙️",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Load custom CSS
    load_custom_css()
    
    # Hero Section - Zeabur Style
    st.markdown(
        """
        <div style='text-align: center; padding: 6rem 0 4rem 0; max-width: 900px; margin: 0 auto;'>
            <h1 class='hero-title' style='font-size: 4.5rem; line-height: 1; margin-bottom: 2rem;'>
                Your AI Podcast<br/>Platform
            </h1>
            <p class='subtitle' style='font-size: 1.4rem; color: #666; line-height: 1.8; margin-bottom: 3rem;'>
                Stream and discover podcast episodes powered by<br/>
                <span class='animated-text' style='color: #fff; font-weight: 500;'>AI technology</span>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Main Area - Episode Library (Zeabur Style)
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown('<h2 style="font-size: 3rem; font-weight: 800; color: #fff; letter-spacing: -2px; margin-bottom: 1rem;">Episode Library</h2>', unsafe_allow_html=True)
        st.markdown('<p style="font-size: 1.2rem; color: #666; font-weight: 400;">All your podcast episodes in one place</p>', unsafe_allow_html=True)
    
    with col2:
        # Stats
        try:
            response = requests.get(f"{API_BASE_URL}/api/episodes", timeout=5)
            if response.status_code == 200:
                episode_count = len(response.json())
                st.markdown(
                    f'<div class="stat-badge" style="float: right; margin-top: 1rem;">{episode_count} Episodes</div>',
                    unsafe_allow_html=True
                )
        except:
            pass
    
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    try:
        # Fetch all episodes
        response = requests.get(f"{API_BASE_URL}/api/episodes", timeout=10)
        
        if response.status_code == 200:
            episodes = response.json()
            
            if not episodes:
                st.markdown(
                    """
                    <div style='text-align: center; padding: 8rem 3rem; background: #0a0a0a; border: 1px solid #1a1a1a; border-radius: 28px;'>
                        <div style='font-size: 5rem; margin-bottom: 2rem; opacity: 0.5;'>🎙️</div>
                        <h3 style='color: #fff; font-weight: 700; font-size: 2rem; margin-bottom: 1rem; letter-spacing: -1px;'>No Episodes Yet</h3>
                        <p style='color: #555; font-size: 1.15rem; line-height: 1.6; margin-bottom: 3rem;'>
                            Upload your first podcast episode<br/>from the sidebar to get started
                        </p>
                        <div style='color: #888; font-size: 0.95rem;'>← Start by uploading files</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                # Display each episode (Zeabur Pure Black Card)
                for idx, episode in enumerate(episodes):
                    # Episode card wrapper
                    st.markdown('<div class="episode-card">', unsafe_allow_html=True)
                    
                    col1, col2 = st.columns([1, 2.5])
                    
                    with col1:
                        # Display cover
                        image_url = f"{API_BASE_URL}{episode['image_url']}"
                        st.image(image_url, use_container_width=True)
                    
                    with col2:
                        # Episode badges
                        st.markdown(
                            f'<div style="margin-bottom: 1rem;">'
                            f'<span class="stat-badge" style="margin-right: 0.5rem;">Episode #{len(episodes) - idx}</span>'
                            f'<span class="stat-badge">ID: {episode["id"]}</span>'
                            f'</div>',
                            unsafe_allow_html=True
                        )
                        
                        # Title
                        st.markdown(f'<h3 style="font-size: 1.8rem; font-weight: 700; color: #fff; margin-bottom: 0.8rem; letter-spacing: -0.5px;">{episode["title"]}</h3>', unsafe_allow_html=True)
                        
                        # Format date
                        try:
                            created_at = datetime.fromisoformat(episode['created_at'])
                            formatted_date = created_at.strftime("%B %d, %Y • %H:%M")
                        except:
                            formatted_date = episode['created_at']
                        
                        st.markdown(
                            f'<p style="color: #555; font-size: 0.9rem; margin-bottom: 1.5rem;">{formatted_date}</p>',
                            unsafe_allow_html=True
                        )
                        
                        # Description
                        st.markdown(f'<p style="color: #888; font-size: 1.05rem; line-height: 1.6; margin-bottom: 2rem;">{episode["description"]}</p>', unsafe_allow_html=True)
                        
                        # Audio player
                        audio_url = f"{API_BASE_URL}{episode['audio_url']}"
                        st.audio(audio_url)
                        
                        # Download button
                        st.markdown(
                            f"""
                            <a href="{API_BASE_URL}{episode["audio_url"]}" download 
                               style="display: inline-block; margin-top: 1.5rem; padding: 0.8rem 2rem; 
                               background: #0a0a0a; border: 1px solid #1a1a1a; border-radius: 14px; 
                               color: #aaa; text-decoration: none; font-weight: 600; font-size: 0.95rem;
                               transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);"
                               onmouseover="this.style.borderColor='#2a2a2a'; this.style.background='#0f0f0f'; this.style.transform='translateY(-2px)';"
                               onmouseout="this.style.borderColor='#1a1a1a'; this.style.background='#0a0a0a'; this.style.transform='translateY(0)';">
                                ⬇️ Download Audio
                            </a>
                            """,
                            unsafe_allow_html=True
                        )
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                    st.markdown("<br><br>", unsafe_allow_html=True)
        else:
            st.error("❌ Failed to load episode library")
    
    except requests.exceptions.ConnectionError:
        st.markdown(
            """
            <div style='text-align: center; padding: 6rem 3rem; background: #0a0a0a; border: 1px solid #1a1a1a; border-radius: 28px;'>
                <div style='font-size: 5rem; margin-bottom: 2rem; opacity: 0.5;'>⚠️</div>
                <h3 style='color: #f87171; font-weight: 700; font-size: 2rem; margin-bottom: 1.5rem; letter-spacing: -1px;'>Connection Error</h3>
                <p style='color: #555; font-size: 1.1rem; margin-bottom: 2rem; line-height: 1.6;'>
                    Cannot connect to backend server
                </p>
                <code style='background: #000; padding: 0.8rem 1.5rem; border-radius: 12px; color: #888; font-size: 1rem; border: 1px solid #1a1a1a;'>
                    http://localhost:8000
                </code>
                <p style='color: #666; font-size: 0.95rem; margin-top: 2rem;'>
                    Please ensure FastAPI service is running
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
    except Exception as e:
        st.error(f"❌ Error occurred: {str(e)}")
    
    # Footer (Zeabur Pure Black Style)
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style='text-align: center; padding: 4rem 2rem 3rem 2rem; border-top: 1px solid #1a1a1a;'>
            <p style='color: #fff; font-weight: 700; font-size: 1.5rem; margin-bottom: 1rem; letter-spacing: -1px;'>
                AI Podcast Platform
            </p>
            <p style='color: #555; font-size: 1.05rem; margin-bottom: 3rem; line-height: 1.6;'>
                Powered by Streamlit + FastAPI + AI Technology
            </p>
            <div style='display: flex; justify-content: center; gap: 3rem; flex-wrap: wrap; margin-bottom: 3rem;'>
                <a href='#' style='color: #666; text-decoration: none; font-size: 0.95rem; transition: color 0.3s;' 
                   onmouseover='this.style.color="#aaa"' onmouseout='this.style.color="#666"'>Documentation</a>
                <a href='#' style='color: #666; text-decoration: none; font-size: 0.95rem; transition: color 0.3s;'
                   onmouseover='this.style.color="#aaa"' onmouseout='this.style.color="#666"'>API Reference</a>
                <a href='#' style='color: #666; text-decoration: none; font-size: 0.95rem; transition: color 0.3s;'
                   onmouseover='this.style.color="#aaa"' onmouseout='this.style.color="#666"'>Support</a>
            </div>
            <p style='color: #333; font-size: 0.9rem;'>
                © 2024 AI Podcast Platform. Built for the future of content creation.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()

