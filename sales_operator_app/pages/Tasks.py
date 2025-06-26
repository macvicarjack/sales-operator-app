import streamlit as st
import sys
from pathlib import Path
from datetime import datetime, date

# Add the parent directory to the path so we can import from services
sys.path.append(str(Path(__file__).parent.parent))

from components.app_layout import page_wrapper
from services.task_service import (
    get_quick_tasks,
    get_open_tasks,
    mark_task_done,
    add_task,
    calculate_task_score
)

def main():
    page_wrapper("📋 Task Tracker")

    # --- Section 1: Quick Tasks ---
    st.header("⚡ Quick Tasks")
    quick_tasks = get_quick_tasks()
    if not quick_tasks:
        st.info("No quick tasks!")
    else:
        for task in quick_tasks:
            col1, col2 = st.columns([0.08, 0.92])
            with col1:
                checked = st.checkbox("", key=f"quick_{task['id']}")
            with col2:
                st.markdown(f"**{task['title']}**  ")
                meta = []
                if task.get('due_date'):
                    meta.append(f"Due: {task['due_date']}")
                if task.get('customer_name'):
                    meta.append(f"Customer: {task['customer_name']}")
                if task.get('potential_revenue'):
                    meta.append(f"💰 ${task['potential_revenue']}")
                if meta:
                    st.caption(" | ".join(meta))
            if checked:
                mark_task_done(task['id'])
                st.success(f"Task '{task['title']}' marked as done!")
                st.experimental_rerun()

        st.markdown("---")

    # --- Section 2: Prioritized Tasks ---
    st.header("🔥 Prioritized Tasks")
    open_tasks = [t for t in get_open_tasks() if t.get('type') != 'quick']
    if not open_tasks:
        st.info("No prioritized tasks!")
    else:
        # Calculate scores and sort
        for t in open_tasks:
            t['score'] = calculate_task_score(t)
        open_tasks.sort(key=lambda x: x['score'], reverse=True)

        # Table/card layout
        for task in open_tasks:
            with st.container():
                cols = st.columns([2, 1, 0.7, 1, 0.7, 1, 1, 0.7])
                with cols[0]:
                    st.markdown(f"**{task['title']}**")
                    if task.get('description'):
                        st.caption(task['description'])
                with cols[1]:
                    st.markdown(task.get('customer_name', ''))
                with cols[2]:
                    st.markdown(task.get('customer_tier', ''))
                with cols[3]:
                    st.markdown(f"${task.get('potential_revenue', 0)}")
                with cols[4]:
                    st.markdown(f"**{task['score']:.1f}**")
                with cols[5]:
                    last_action = task.get('last_action_date') or task.get('created_at')
                    if isinstance(last_action, str):
                        st.markdown(last_action.split(' ')[0])
                    elif isinstance(last_action, datetime):
                        st.markdown(last_action.strftime('%Y-%m-%d'))
                    else:
                        st.markdown('-')
                with cols[6]:
                    next_followup = task.get('next_followup_date')
                    if isinstance(next_followup, str):
                        st.markdown(next_followup.split(' ')[0])
                    elif isinstance(next_followup, datetime):
                        st.markdown(next_followup.strftime('%Y-%m-%d'))
                    else:
                        st.markdown('-')
                with cols[7]:
                    if st.button("Mark Done", key=f"done_{task['id']}"):
                        mark_task_done(task['id'])
                        st.success(f"Task '{task['title']}' marked as done!")
                        st.experimental_rerun()

        st.markdown("---")

    # --- Section 3: Add New Task Form ---
    st.header("➕ Add New Task")
    with st.form("task_form"):
        title = st.text_input("Task Name", max_chars=100)
        description = st.text_area("Description", max_chars=500)
        customer_name = st.text_input("Customer Name")
        customer_tier = st.selectbox("Customer Tier", options=["A", "B", "C"])
        potential_revenue = st.number_input("Potential Revenue ($)", min_value=0.0, step=100.0)
        task_type = st.radio("Task Type", options=["normal", "quick"], horizontal=True)
        
        # Due date for quick tasks
        due_date = None
        if task_type == "quick":
            due_date = st.date_input("Due Date", min_value=date.today())
        
        # Next follow-up date and time
        next_followup_date = st.date_input("Next Follow-up Date", value=date.today())
        next_followup_time = st.time_input("Next Follow-up Time", value=datetime.now().time())
        
        submitted = st.form_submit_button("Create Task")
        if submitted:
            # Combine date and time for next_followup_date
            next_followup_datetime = datetime.combine(next_followup_date, next_followup_time)
            
            data = {
                "title": title.strip(),
                "description": description.strip(),
                "customer_name": customer_name.strip(),
                "customer_tier": customer_tier,
                "potential_revenue": potential_revenue,
                "type": task_type,
                "status": "open",
                "next_followup_date": next_followup_datetime.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            if due_date:
                data["due_date"] = due_date.strftime("%Y-%m-%d")
            
            if add_task(data):
                st.success(f"Task '{title}' added!")
                st.experimental_rerun()
            else:
                st.error("Failed to add task. Please check your input.")

if __name__ == "__main__":
    main() 