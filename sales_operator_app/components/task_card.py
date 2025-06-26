"""
Task Card Component for Sales Operator.
A reusable component to display tasks in a styled card format.
"""

import streamlit as st
from typing import Dict, Any, Optional

def render_task_card(task: Dict[str, Any], show_actions: bool = True) -> None:
    """
    Render a task as a styled card with title, score, revenue, tier, and action buttons.
    
    Args:
        task (Dict[str, Any]): Task dictionary with keys like title, score, potential_revenue, etc.
        show_actions (bool): Whether to show action buttons (Mark Done, etc.)
    """
    
    # Get task data with defaults
    title = task.get('title', 'Untitled Task')
    description = task.get('description', '')
    customer_name = task.get('customer_name', '')
    customer_tier = task.get('customer_tier', '')
    potential_revenue = task.get('potential_revenue', 0)
    score = task.get('score', 0)
    status = task.get('status', 'open')
    task_type = task.get('type', 'normal')
    due_date = task.get('due_date', '')
    next_followup = task.get('next_followup_date', '')
    
    # Status color mapping
    status_colors = {
        'open': '#28a745',
        'waiting': '#ffc107', 
        'done': '#6c757d'
    }
    
    # Tier color mapping
    tier_colors = {
        'A': '#dc3545',
        'B': '#fd7e14',
        'C': '#6f42c1'
    }
    
    # Task type icons
    type_icons = {
        'quick': '⚡',
        'normal': '📋'
    }
    
    # Create the card HTML
    card_html = f"""
    <div style="
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 16px;
        margin: 8px 0;
        background: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    ">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div style="flex: 1;">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                    <span style="font-size: 16px;">{type_icons.get(task_type, '📋')}</span>
                    <h3 style="margin: 0; color: #333; font-size: 18px;">{title}</h3>
                    <span style="
                        background: {status_colors.get(status, '#6c757d')};
                        color: white;
                        padding: 2px 8px;
                        border-radius: 12px;
                        font-size: 12px;
                        font-weight: bold;
                    ">{status.upper()}</span>
                </div>
                
                {f'<p style="color: #666; margin: 8px 0; font-size: 14px;">{description}</p>' if description else ''}
                
                <div style="display: flex; gap: 16px; margin-top: 12px; flex-wrap: wrap;">
                    {f'<div style="display: flex; align-items: center; gap: 4px;"><span>👤</span><span style="color: #555;">{customer_name}</span></div>' if customer_name else ''}
                    {f'<div style="display: flex; align-items: center; gap: 4px;"><span style="color: {tier_colors.get(customer_tier, '#6c757d')}; font-weight: bold;">{customer_tier}</span><span style="color: #555;">Tier</span></div>' if customer_tier else ''}
                    {f'<div style="display: flex; align-items: center; gap: 4px;"><span>💰</span><span style="color: #555;">${potential_revenue:,.0f}</span></div>' if potential_revenue else ''}
                    {f'<div style="display: flex; align-items: center; gap: 4px;"><span>📊</span><span style="color: #555; font-weight: bold;">{score:.1f}</span></div>' if score else ''}
                </div>
                
                <div style="display: flex; gap: 16px; margin-top: 8px; font-size: 12px; color: #888;">
                    {f'<div>📅 Due: {due_date}</div>' if due_date else ''}
                    {f'<div>⏰ Follow-up: {next_followup.split(" ")[0] if next_followup else ""}</div>' if next_followup else ''}
                </div>
            </div>
            
            {f'''
            <div style="display: flex; flex-direction: column; gap: 8px; margin-left: 16px;">
                <button style="
                    background: #007bff;
                    color: white;
                    border: none;
                    padding: 6px 12px;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 12px;
                " onclick="alert('Mark Done functionality would be implemented here')">Mark Done</button>
                <button style="
                    background: #6c757d;
                    color: white;
                    border: none;
                    padding: 6px 12px;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 12px;
                " onclick="alert('Edit functionality would be implemented here')">Edit</button>
            </div>
            ''' if show_actions else ''}
        </div>
    </div>
    """
    
    # Render the card
    st.markdown(card_html, unsafe_allow_html=True) 