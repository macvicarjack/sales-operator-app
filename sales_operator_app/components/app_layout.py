"""
App Layout Component for Sales Operator.
Provides consistent page layout wrapper for all pages.
"""

import streamlit as st
import sys
from pathlib import Path

# Add the parent directory to the path so we can import from utils and components
sys.path.append(str(Path(__file__).parent.parent))

from utils.ui import spacer
from components.section_header import section_header

def page_wrapper(title: str) -> None:
    """
    Create a consistent page layout wrapper.
    
    Args:
        title (str): Page title, can include emoji (e.g., "📋 Task Tracker")
    """
    
    # Extract emoji and clean title
    emoji = ""
    clean_title = title
    
    # Check if title starts with an emoji (common emoji characters)
    if title and len(title) > 1:
        first_char = title[0]
        # Check if first character is likely an emoji (not alphanumeric or common punctuation)
        if not first_char.isalnum() and first_char not in ".,;:!?":
            # Look for space after emoji
            space_index = title.find(" ")
            if space_index > 0:
                emoji = title[:space_index]
                clean_title = title[space_index + 1:].strip()
    
    # Set page configuration
    st.set_page_config(
        page_title=clean_title,
        page_icon=emoji if emoji else "📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Add spacing before title
    spacer(20)
    
    # Render section header with title and emoji
    section_header(clean_title, emoji)
    
    # Add spacing after title
    spacer(10)

def simple_page_wrapper(title: str, icon: str = "") -> None:
    """
    Create a simple page layout wrapper without section header styling.
    
    Args:
        title (str): Page title
        icon (str): Optional emoji icon
    """
    
    # Set page configuration
    st.set_page_config(
        page_title=title,
        page_icon=icon if icon else "📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Add spacing before title
    spacer(20)
    
    # Simple title display
    if icon:
        st.title(f"{icon} {title}")
    else:
        st.title(title)
    
    # Add spacing after title
    spacer(10)

def dashboard_wrapper(title: str, subtitle: str = "") -> None:
    """
    Create a dashboard-style page layout wrapper.
    
    Args:
        title (str): Page title
        subtitle (str): Optional subtitle
    """
    
    # Set page configuration
    st.set_page_config(
        page_title=title,
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Add spacing before title
    spacer(20)
    
    # Dashboard-style header
    st.markdown(f"""
    <div style="
        border-bottom: 2px solid #4A90E2;
        padding-bottom: 16px;
        margin-bottom: 24px;
    ">
        <h1 style="
            margin: 0;
            color: #333;
            font-size: 32px;
            font-weight: bold;
        ">{title}</h1>
        {f'<p style="margin: 8px 0 0 0; color: #666; font-size: 16px;">{subtitle}</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)
    
    # Add spacing after header
    spacer(10) 