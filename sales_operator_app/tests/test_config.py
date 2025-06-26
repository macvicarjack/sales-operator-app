"""
Tests for config module.
Tests that configuration constants exist and have expected types/values.
"""

import pytest
import sys
from pathlib import Path

# Add the parent directory to the path so we can import from the app
sys.path.append(str(Path(__file__).parent.parent))

from utils.config import *

class TestConfig:
    """Test class for configuration constants."""
    
    def test_database_configuration_exists(self):
        """Test that database configuration constants exist."""
        # Assert: Database constants should exist
        assert hasattr(sys.modules[__name__], 'DATABASE_PATH')
        assert hasattr(sys.modules[__name__], 'DATABASE_TIMEOUT')
        
        # Assert: Should have expected types
        assert isinstance(DATABASE_PATH, str)
        assert isinstance(DATABASE_TIMEOUT, int)
        
        # Assert: Should have reasonable values
        assert DATABASE_TIMEOUT > 0
        assert "db" in DATABASE_PATH
    
    def test_task_configuration_exists(self):
        """Test that task configuration constants exist."""
        # Assert: Task constants should exist
        assert hasattr(sys.modules[__name__], 'TASK_STATUSES')
        assert hasattr(sys.modules[__name__], 'TASK_TYPES')
        assert hasattr(sys.modules[__name__], 'TASK_URGENCIES')
        assert hasattr(sys.modules[__name__], 'CUSTOMER_TIERS')
        
        # Assert: Should be lists
        assert isinstance(TASK_STATUSES, list)
        assert isinstance(TASK_TYPES, list)
        assert isinstance(TASK_URGENCIES, list)
        assert isinstance(CUSTOMER_TIERS, list)
        
        # Assert: Should not be empty
        assert len(TASK_STATUSES) > 0
        assert len(TASK_TYPES) > 0
        assert len(TASK_URGENCIES) > 0
        assert len(CUSTOMER_TIERS) > 0
        
        # Assert: Should contain expected values
        assert "open" in TASK_STATUSES
        assert "normal" in TASK_TYPES
        assert "high" in TASK_URGENCIES
        assert "A" in CUSTOMER_TIERS
    
    def test_lead_configuration_exists(self):
        """Test that lead configuration constants exist."""
        # Assert: Lead constants should exist
        assert hasattr(sys.modules[__name__], 'LEAD_STATUSES')
        assert hasattr(sys.modules[__name__], 'LEAD_SOURCES')
        
        # Assert: Should be lists
        assert isinstance(LEAD_STATUSES, list)
        assert isinstance(LEAD_SOURCES, list)
        
        # Assert: Should not be empty
        assert len(LEAD_STATUSES) > 0
        assert len(LEAD_SOURCES) > 0
        
        # Assert: Should contain expected values
        assert "new" in LEAD_STATUSES
        assert "website" in LEAD_SOURCES
    
    def test_scoring_configuration_exists(self):
        """Test that scoring configuration constants exist."""
        # Assert: Scoring constants should exist
        assert hasattr(sys.modules[__name__], 'MAX_TASK_SCORE')
        assert hasattr(sys.modules[__name__], 'MIN_TASK_SCORE')
        assert hasattr(sys.modules[__name__], 'REVENUE_WEIGHT')
        assert hasattr(sys.modules[__name__], 'URGENCY_WEIGHT')
        assert hasattr(sys.modules[__name__], 'CUSTOMER_TIER_WEIGHT')
        assert hasattr(sys.modules[__name__], 'TIME_WEIGHT')
        
        # Assert: Should have expected types
        assert isinstance(MAX_TASK_SCORE, int)
        assert isinstance(MIN_TASK_SCORE, int)
        assert isinstance(REVENUE_WEIGHT, float)
        assert isinstance(URGENCY_WEIGHT, float)
        assert isinstance(CUSTOMER_TIER_WEIGHT, float)
        assert isinstance(TIME_WEIGHT, float)
        
        # Assert: Should have reasonable values
        assert MAX_TASK_SCORE == 100
        assert MIN_TASK_SCORE == 0
        assert 0 <= REVENUE_WEIGHT <= 1
        assert 0 <= URGENCY_WEIGHT <= 1
        assert 0 <= CUSTOMER_TIER_WEIGHT <= 1
        assert 0 <= TIME_WEIGHT <= 1
        
        # Assert: Weights should sum to approximately 1.0
        total_weight = REVENUE_WEIGHT + URGENCY_WEIGHT + CUSTOMER_TIER_WEIGHT + TIME_WEIGHT
        assert abs(total_weight - 1.0) < 0.01
    
    def test_ui_configuration_exists(self):
        """Test that UI configuration constants exist."""
        # Assert: UI constants should exist
        assert hasattr(sys.modules[__name__], 'PAGE_TITLE')
        assert hasattr(sys.modules[__name__], 'PAGE_ICON')
        assert hasattr(sys.modules[__name__], 'LAYOUT')
        assert hasattr(sys.modules[__name__], 'THEME')
        
        # Assert: Should be strings
        assert isinstance(PAGE_TITLE, str)
        assert isinstance(PAGE_ICON, str)
        assert isinstance(LAYOUT, str)
        assert isinstance(THEME, str)
        
        # Assert: Should have reasonable values
        assert len(PAGE_TITLE) > 0
        assert len(PAGE_ICON) > 0
        assert LAYOUT in ["wide", "centered"]
        assert THEME in ["light", "dark"]
    
    def test_app_configuration_exists(self):
        """Test that app configuration constants exist."""
        # Assert: App constants should exist
        assert hasattr(sys.modules[__name__], 'APP_VERSION')
        assert hasattr(sys.modules[__name__], 'APP_NAME')
        assert hasattr(sys.modules[__name__], 'APP_DESCRIPTION')
        
        # Assert: Should be strings
        assert isinstance(APP_VERSION, str)
        assert isinstance(APP_NAME, str)
        assert isinstance(APP_DESCRIPTION, str)
        
        # Assert: Should have reasonable values
        assert len(APP_VERSION) > 0
        assert len(APP_NAME) > 0
        assert len(APP_DESCRIPTION) > 0
    
    def test_environment_configuration_exists(self):
        """Test that environment configuration constants exist."""
        # Assert: Environment constants should exist
        assert hasattr(sys.modules[__name__], 'ENVIRONMENT')
        assert hasattr(sys.modules[__name__], 'DEBUG_MODE')
        
        # Assert: Should have expected types
        assert isinstance(ENVIRONMENT, str)
        assert isinstance(DEBUG_MODE, bool)
        
        # Assert: Should have reasonable values
        assert ENVIRONMENT in ["development", "production", "testing"]
    
    def test_pagination_configuration_exists(self):
        """Test that pagination configuration constants exist."""
        # Assert: Pagination constants should exist
        assert hasattr(sys.modules[__name__], 'DEFAULT_PAGE_SIZE')
        assert hasattr(sys.modules[__name__], 'MAX_PAGE_SIZE')
        
        # Assert: Should be integers
        assert isinstance(DEFAULT_PAGE_SIZE, int)
        assert isinstance(MAX_PAGE_SIZE, int)
        
        # Assert: Should have reasonable values
        assert DEFAULT_PAGE_SIZE > 0
        assert MAX_PAGE_SIZE > DEFAULT_PAGE_SIZE
    
    def test_datetime_configuration_exists(self):
        """Test that date/time configuration constants exist."""
        # Assert: Date/time constants should exist
        assert hasattr(sys.modules[__name__], 'DATE_FORMAT')
        assert hasattr(sys.modules[__name__], 'DATETIME_FORMAT')
        assert hasattr(sys.modules[__name__], 'TIMEZONE')
        
        # Assert: Should be strings
        assert isinstance(DATE_FORMAT, str)
        assert isinstance(DATETIME_FORMAT, str)
        assert isinstance(TIMEZONE, str)
        
        # Assert: Should have reasonable values
        assert len(DATE_FORMAT) > 0
        assert len(DATETIME_FORMAT) > 0
        assert len(TIMEZONE) > 0
    
    def test_validation_configuration_exists(self):
        """Test that validation configuration constants exist."""
        # Assert: Validation constants should exist
        assert hasattr(sys.modules[__name__], 'MAX_NAME_LENGTH')
        assert hasattr(sys.modules[__name__], 'MAX_EMAIL_LENGTH')
        assert hasattr(sys.modules[__name__], 'MAX_COMPANY_LENGTH')
        assert hasattr(sys.modules[__name__], 'MAX_DESCRIPTION_LENGTH')
        assert hasattr(sys.modules[__name__], 'MIN_REVENUE')
        assert hasattr(sys.modules[__name__], 'MAX_REVENUE')
        
        # Assert: Should have expected types
        assert isinstance(MAX_NAME_LENGTH, int)
        assert isinstance(MAX_EMAIL_LENGTH, int)
        assert isinstance(MAX_COMPANY_LENGTH, int)
        assert isinstance(MAX_DESCRIPTION_LENGTH, int)
        assert isinstance(MIN_REVENUE, float)
        assert isinstance(MAX_REVENUE, float)
        
        # Assert: Should have reasonable values
        assert MAX_NAME_LENGTH > 0
        assert MAX_EMAIL_LENGTH > 0
        assert MAX_COMPANY_LENGTH > 0
        assert MAX_DESCRIPTION_LENGTH > 0
        assert MIN_REVENUE >= 0
        assert MAX_REVENUE > MIN_REVENUE 