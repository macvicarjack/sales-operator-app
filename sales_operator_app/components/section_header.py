"""
Section Header Component for Sales Operator.
A reusable component to display section headers with icons and optional collapsible functionality.
"""

import streamlit as st
from typing import Optional

def section_header(label: str, icon: str = "", collapsible: bool = False, expanded: bool = True) -> Optional[bool]:
    """
    Display a bold emoji header using st.markdown().
    
    Args:
        label (str): The header text to display
        icon (str): Optional emoji or icon to display before the label
        collapsible (bool): Whether to make the section collapsible
        expanded (bool): Whether the section is expanded by default (only used if collapsible=True)
    
    Returns:
        Optional[bool]: If collapsible=True, returns the expanded state. Otherwise returns None.
    """
    
    # Create the header text
    header_text = f"{icon} {label}" if icon else label
    
    if collapsible:
        # Use st.expander for collapsible sections
        with st.expander(header_text, expanded=expanded):
            return True
    else:
        # Use st.markdown for regular headers
        st.markdown(f"### {header_text}")
        return None

def simple_header(label: str, icon: str = "") -> None:
    """
    Display a simple header without collapsible functionality.
    
    Args:
        label (str): The header text to display
        icon (str): Optional emoji or icon to display before the label
    """
    header_text = f"{icon} {label}" if icon else label
    st.markdown(f"### {header_text}")

def styled_header(label: str, icon: str = "", level: int = 3) -> None:
    """
    Display a styled header with custom formatting.
    
    Args:
        label (str): The header text to display
        icon (str): Optional emoji or icon to display before the label
        level (int): Header level (1-6, where 1 is largest)
    """
    header_text = f"{icon} {label}" if icon else label
    
    # Create styled header with HTML
    header_html = f"""
    <div style="
        border-bottom: 2px solid #007bff;
        padding-bottom: 8px;
        margin: 20px 0 16px 0;
    ">
        <h{level} style="
            margin: 0;
            color: #333;
            font-weight: bold;
            display: flex;
            align-items: center;
            gap: 8px;
        ">
            {header_text}
        </h{level}>
    </div>
    """
    
    st.markdown(header_html, unsafe_allow_html=True) 