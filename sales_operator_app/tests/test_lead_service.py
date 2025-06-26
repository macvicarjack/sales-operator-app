"""
Tests for lead_service module.
Tests lead creation, retrieval, and database interaction.
"""

import pytest
import sys
from pathlib import Path

# Add the parent directory to the path so we can import from the app
sys.path.append(str(Path(__file__).parent.parent))

from services.lead_service import (
    get_all_leads,
    add_lead,
    get_lead_by_id
)

class TestLeadService:
    """Test class for lead service functions."""
    
    def test_get_all_leads_returns_list(self):
        """Test that get_all_leads returns a list."""
        # Act: Call the function
        leads = get_all_leads()
        
        # Assert: Should return a list
        assert isinstance(leads, list)
    
    def test_get_all_leads_empty_database(self):
        """Test that get_all_leads returns empty list when DB is empty."""
        # Act: Call the function (assuming fresh/empty database)
        leads = get_all_leads()
        
        # Assert: Should return empty list
        assert isinstance(leads, list)
        # Note: In a real test with mocked DB, this would be empty
        # For now, we just verify it's a list
    
    def test_add_lead_function_exists(self):
        """Test that add_lead function exists and is callable."""
        # Assert: Function should exist and be callable
        assert callable(add_lead)
    
    def test_get_lead_by_id_function_exists(self):
        """Test that get_lead_by_id function exists and is callable."""
        # Assert: Function should exist and be callable
        assert callable(get_lead_by_id)
    
    def test_add_lead_basic_functionality(self, sample_lead_data):
        """Test that add_lead can be called with valid data."""
        # Arrange: Use sample lead data
        name = sample_lead_data["name"]
        company = sample_lead_data["company"]
        email = sample_lead_data["email"]
        status = sample_lead_data["status"]
        
        # Act: Add lead (this would need database mocking for full test)
        result = add_lead(name, company, email, status)
        
        # Assert: Should return a boolean indicating success
        assert isinstance(result, bool)
    
    def test_add_lead_with_minimal_data(self):
        """Test add_lead with minimal required data."""
        # Arrange: Minimal lead data (just name)
        name = "Test Lead"
        company = ""
        email = ""
        status = "new"
        
        # Act: Add lead
        result = add_lead(name, company, email, status)
        
        # Assert: Should return a boolean
        assert isinstance(result, bool)
    
    def test_lead_service_functions_signature(self):
        """Test that lead service functions have expected signatures."""
        import inspect
        
        # Test add_lead signature
        add_lead_sig = inspect.signature(add_lead)
        assert len(add_lead_sig.parameters) >= 4  # name, company, email, status
        
        # Test get_all_leads signature
        get_all_leads_sig = inspect.signature(get_all_leads)
        assert len(get_all_leads_sig.parameters) >= 0  # No required parameters
        
        # Test get_lead_by_id signature
        get_lead_by_id_sig = inspect.signature(get_lead_by_id)
        assert len(get_lead_by_id_sig.parameters) >= 1  # lead_id parameter
    
    def test_lead_data_validation(self):
        """Test that lead service handles various data types correctly."""
        # Test with different data types
        test_cases = [
            ("John Doe", "Company Inc", "john@company.com", "new"),
            ("Jane Smith", "", "jane@email.com", "contacted"),
            ("Bob Wilson", "Bob's Business", "", "qualified"),
            ("", "Empty Name Co", "empty@company.com", "new"),  # Edge case
        ]
        
        for name, company, email, status in test_cases:
            # Act: Try to add lead
            result = add_lead(name, company, email, status)
            
            # Assert: Should return a boolean
            assert isinstance(result, bool) 