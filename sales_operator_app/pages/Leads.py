import streamlit as st
import sys
from pathlib import Path

# Add the parent directory to the path so we can import from services
sys.path.append(str(Path(__file__).parent.parent))

from components.app_layout import page_wrapper
from services.lead_service import get_all_leads, add_lead

def main():
    """Main function for the Leads page."""
    
    page_wrapper("📇 Leads")
    
    # Lead Creation Form
    st.subheader("➕ Add New Lead")
    
    with st.form("add_lead_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Name *", placeholder="Enter lead name")
            company = st.text_input("Company", placeholder="Enter company name")
        
        with col2:
            email = st.text_input("Email", placeholder="Enter email address")
            status = st.selectbox(
                "Status",
                options=['new', 'contacted', 'qualified', 'closed'],
                index=0
            )
        
        submitted = st.form_submit_button("Add Lead", type="primary")
        
        if submitted:
            if name.strip():  # Check if name is provided
                success = add_lead(name, company, email, status)
                if success:
                    st.success(f"✅ Lead '{name}' added successfully!")
                    st.rerun()  # Refresh the page to show the new lead
                else:
                    st.error("❌ Failed to add lead. Please try again.")
            else:
                st.error("❌ Name is required!")
    
    st.markdown("---")
    
    # Add a refresh button
    if st.button("🔄 Refresh Leads"):
        st.rerun()
    
    # Fetch all leads
    leads = get_all_leads()
    
    if not leads:
        st.info("📭 No leads found. Add some leads to get started!")
        return
    
    # Display lead count
    st.subheader(f"📊 Total Leads: {len(leads)}")
    
    # Display leads
    st.markdown("### Recent Leads")
    
    for lead in leads:
        # Create a container for each lead
        with st.container():
            col1, col2, col3 = st.columns([3, 2, 1])
            
            with col1:
                # Format: Name from Company
                company_display = f" from {lead['company']}" if lead['company'] else ""
                st.markdown(f"**{lead['name']}**{company_display}")
            
            with col2:
                # Email
                if lead['email']:
                    st.markdown(f"📧 {lead['email']}")
                else:
                    st.markdown("📧 *No email*")
            
            with col3:
                # Status with color coding
                status = lead['status']
                if status == 'new':
                    st.markdown("🟢 **New**")
                elif status == 'contacted':
                    st.markdown("🟡 **Contacted**")
                elif status == 'qualified':
                    st.markdown("🔵 **Qualified**")
                elif status == 'converted':
                    st.markdown("🟣 **Converted**")
                elif status == 'closed':
                    st.markdown("🔴 **Closed**")
                else:
                    st.markdown(f"⚪ **{status.title()}**")
            
            # Add a subtle separator
            st.markdown("---")
    
    # Add some helpful information
    st.markdown("---")
    st.markdown("""
    ### 💡 Tips
    - Use the form above to add new leads
    - Use the refresh button to update the list
    - Leads are sorted by creation date (newest first)
    - Status colors help you quickly identify lead progress
    """)

if __name__ == "__main__":
    main() 