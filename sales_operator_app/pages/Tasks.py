import streamlit as st
import sys
from pathlib import Path
from datetime import datetime, date
import pandas as pd

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

# Initialize session state for task form visibility
if "show_task_form" not in st.session_state:
    st.session_state["show_task_form"] = False

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
                    try:
                        # Try to parse as datetime with time
                        dt = datetime.strptime(task['due_date'], "%Y-%m-%d %H:%M:%S")
                        meta.append(f"Due: {dt.strftime('%m/%d/%Y %I:%M %p')}")
                    except:
                        try:
                            # Try to parse as date only
                            dt = datetime.strptime(task['due_date'], "%Y-%m-%d")
                            meta.append(f"Due: {dt.strftime('%m/%d/%Y')}")
                        except:
                            # Fall back to string
                            meta.append(f"Due: {task['due_date']}")
                if task.get('customer_name'):
                    meta.append(f"Customer: {task['customer_name']}")
                if task.get('potential_revenue'):
                    meta.append(f"💰 ${task['potential_revenue']}")
                if meta:
                    st.caption(" | ".join(meta))
            if checked:
                try:
                    mark_task_done(task['id'])
                    st.success(f"Task '{task['title']}' marked as done!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to mark task as done: {str(e)}")

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

        # Header row for prioritized tasks
        col1, col2, col3, col4, col5, col6, col7 = st.columns([2, 2, 1, 2, 2, 2, 1])
        col1.markdown("**Task Name**")
        col2.markdown("**Company**")
        col3.markdown("**Tier**")
        col4.markdown("**Potential Revenue**")
        col5.markdown("**Score**")
        col6.markdown("**Due Date**")
        col7.markdown("**Actions**")
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
                        try:
                            # Try to parse as datetime with time
                            dt = datetime.strptime(last_action, "%Y-%m-%d %H:%M:%S")
                            st.markdown(f"{dt.strftime('%m/%d/%Y')}<br>{dt.strftime('%I:%M %p')}", unsafe_allow_html=True)
                        except:
                            try:
                                # Try to parse as date only
                                dt = datetime.strptime(last_action, "%Y-%m-%d")
                                st.markdown(dt.strftime('%m/%d/%Y'))
                            except:
                                # Fall back to string
                                st.markdown(last_action)
                    elif isinstance(last_action, datetime):
                        st.markdown(f"{last_action.strftime('%m/%d/%Y')}<br>{last_action.strftime('%I:%M %p')}", unsafe_allow_html=True)
                    else:
                        st.markdown('-')
                with cols[6]:
                    # Prefer explicit follow_up_date and follow_up_time fields if present
                    follow_up_date = task.get('follow_up_date')
                    follow_up_time = task.get('follow_up_time')
                    if follow_up_date and follow_up_time:
                        try:
                            # If already date/time objects
                            date_str = follow_up_date.strftime("%m/%d/%Y") if hasattr(follow_up_date, 'strftime') else str(follow_up_date)
                            time_str = follow_up_time.strftime("%I:%M %p") if hasattr(follow_up_time, 'strftime') else str(follow_up_time)
                            st.markdown(f"{date_str}<br>{time_str}", unsafe_allow_html=True)
                        except Exception:
                            st.markdown(f"{follow_up_date}<br>{follow_up_time}", unsafe_allow_html=True)
                    else:
                        # Fallback to next_followup_date parsing
                        next_followup = task.get('next_followup_date')
                        if isinstance(next_followup, str):
                            try:
                                dt = datetime.strptime(next_followup, "%Y-%m-%d %H:%M:%S")
                                st.markdown(f"{dt.strftime('%m/%d/%Y')}<br>{dt.strftime('%I:%M %p')}", unsafe_allow_html=True)
                            except:
                                st.markdown(next_followup.split(' ')[0])
                        elif isinstance(next_followup, datetime):
                            st.markdown(f"{next_followup.strftime('%m/%d/%Y')}<br>{next_followup.strftime('%I:%M %p')}", unsafe_allow_html=True)
                        else:
                            st.markdown('-')
                with cols[7]:
                    if st.button("Complete", key=f"done_{task['id']}", type="primary"):
                        try:
                            mark_task_done(task['id'])
                            st.success(f"Task '{task['title']}' marked as done!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Failed to mark task as done: {str(e)}")

        st.markdown("---")

    # --- Section 3: Add New Task Form ---
    if st.button("➕ Add Task"):
        st.session_state["show_task_form"] = True

    # Show the task creation form if toggled on
    if st.session_state["show_task_form"]:
        with st.form("new_task_form", clear_on_submit=True):
            task_name = st.text_input("Task Name")
            company = st.text_input("Company")
            tier = st.selectbox("Tier", ["A", "B", "C"])
            revenue = st.number_input("Potential Revenue", step=100)
            due_date = st.date_input("Due Date")
            follow_up_time = st.time_input("Next Follow-up Time")

            submitted = st.form_submit_button("Create Task")
            if submitted:
                # Save the task to database
                data = {
                    "title": task_name.strip(),
                    "customer_name": company.strip(),
                    "customer_tier": tier,
                    "potential_revenue": revenue,
                    "type": "normal",
                    "status": "open"
                }
                
                if due_date:
                    data["due_date"] = due_date.strftime("%Y-%m-%d")
                
                if follow_up_time:
                    # Combine with today's date for next_followup_date
                    next_followup_datetime = datetime.combine(date.today(), follow_up_time)
                    data["next_followup_date"] = next_followup_datetime.strftime("%Y-%m-%d %H:%M:%S")
                
                try:
                    if add_task(data):
                        st.success(f"✅ Task '{task_name}' added!")
                        # Reset form visibility and rerun
                        st.session_state["show_task_form"] = False
                        st.rerun()
                    else:
                        st.error("Failed to add task. Please check your input.")
                except Exception as e:
                    st.error(f"Failed to add task: {str(e)}")

    # --- Section 1: Quick Tasks Table Example ---
    if quick_tasks:
        # Format date fields for table display
        for t in quick_tasks:
            if t.get('due_date'):
                try:
                    t['due_date'] = datetime.strptime(t['due_date'], "%Y-%m-%d").strftime("%m/%d/%Y")
                except Exception:
                    pass
        # st.table(quick_tasks)  # Uncomment if you want to display as a table

    # --- Section 2: Prioritized Tasks Table Example ---
    if open_tasks:
        table_data = []
        for t in open_tasks:
            # Format Due Date
            due_date = t.get('due_date')
            if due_date:
                try:
                    due_date_fmt = datetime.strptime(due_date, "%Y-%m-%d").strftime("%m/%d/%Y")
                except Exception:
                    due_date_fmt = due_date
            else:
                due_date_fmt = ''
            table_data.append({
                "Task Name": t.get("title", ""),
                "Company": t.get("customer_name", ""),
                "Tier": t.get("customer_tier", ""),
                "Due Date": due_date_fmt,
                "Follow-up Time": t.get("follow_up_time", ""),
                "Status": t.get("status", "")
            })
        df = pd.DataFrame(table_data)
        st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    main() 