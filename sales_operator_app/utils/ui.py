"""
UI Utility Functions for Sales Operator.
Small utility functions for common UI patterns and styling.
"""

import streamlit as st
from typing import Optional

def spacer(height: int = 1) -> None:
    """
    Insert a vertical gap using st.markdown().
    
    Args:
        height (int): Height of the spacer in pixels (default: 1)
    """
    st.markdown(f"<div style='height: {height}px;'></div>", unsafe_allow_html=True)

def divider(label: str = "") -> None:
    """
    Show a horizontal line, optionally with a label.
    
    Args:
        label (str): Optional label to display in the center of the divider
    """
    if label:
        # Create a divider with centered label
        divider_html = f"""
        <div style="
            display: flex;
            align-items: center;
            margin: 20px 0;
        ">
            <div style="flex: 1; height: 1px; background: #e0e0e0;"></div>
            <span style="
                padding: 0 16px;
                color: #666;
                font-size: 14px;
                font-weight: 500;
                background: white;
            ">{label}</span>
            <div style="flex: 1; height: 1px; background: #e0e0e0;"></div>
        </div>
        """
        st.markdown(divider_html, unsafe_allow_html=True)
    else:
        # Simple horizontal line
        st.markdown("---")

def html_box(content: str, style: str = "") -> None:
    """
    Wrap any HTML block in a styled box.
    
    Args:
        content (str): HTML content to display
        style (str): Additional CSS styles to apply to the box
    """
    # Default box styling
    default_style = """
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 16px;
        margin: 12px 0;
        background: #f8f9fa;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    """
    
    # Combine default and custom styles
    combined_style = default_style + style
    
    box_html = f"""
    <div style="{combined_style}">
        {content}
    </div>
    """
    
    st.markdown(box_html, unsafe_allow_html=True)

def info_box(title: str, content: str, icon: str = "ℹ️") -> None:
    """
    Display an info box with title and content.
    
    Args:
        title (str): Title of the info box
        content (str): Content text
        icon (str): Icon to display (default: ℹ️)
    """
    info_html = f"""
    <div style="
        border-left: 4px solid #007bff;
        background: #f8f9fa;
        padding: 16px;
        margin: 12px 0;
        border-radius: 4px;
    ">
        <div style="
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 8px;
            font-weight: bold;
            color: #007bff;
        ">
            <span>{icon}</span>
            <span>{title}</span>
        </div>
        <div style="color: #555; line-height: 1.5;">
            {content}
        </div>
    </div>
    """
    st.markdown(info_html, unsafe_allow_html=True)

def success_box(title: str, content: str, icon: str = "✅") -> None:
    """
    Display a success box with title and content.
    
    Args:
        title (str): Title of the success box
        content (str): Content text
        icon (str): Icon to display (default: ✅)
    """
    success_html = f"""
    <div style="
        border-left: 4px solid #28a745;
        background: #f8fff9;
        padding: 16px;
        margin: 12px 0;
        border-radius: 4px;
    ">
        <div style="
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 8px;
            font-weight: bold;
            color: #28a745;
        ">
            <span>{icon}</span>
            <span>{title}</span>
        </div>
        <div style="color: #555; line-height: 1.5;">
            {content}
        </div>
    </div>
    """
    st.markdown(success_html, unsafe_allow_html=True)

def warning_box(title: str, content: str, icon: str = "⚠️") -> None:
    """
    Display a warning box with title and content.
    
    Args:
        title (str): Title of the warning box
        content (str): Content text
        icon (str): Icon to display (default: ⚠️)
    """
    warning_html = f"""
    <div style="
        border-left: 4px solid #ffc107;
        background: #fffbf0;
        padding: 16px;
        margin: 12px 0;
        border-radius: 4px;
    ">
        <div style="
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 8px;
            font-weight: bold;
            color: #856404;
        ">
            <span>{icon}</span>
            <span>{title}</span>
        </div>
        <div style="color: #555; line-height: 1.5;">
            {content}
        </div>
    </div>
    """
    st.markdown(warning_html, unsafe_allow_html=True) 