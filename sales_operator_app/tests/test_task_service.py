"""
Tests for task_service module.
Tests task creation, retrieval, and scoring functionality.
"""

import pytest
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add the parent directory to the path so we can import from the app
sys.path.append(str(Path(__file__).parent.parent))

from services.task_service import (
    get_open_tasks,
    get_quick_tasks,
    add_task,
    mark_task_done,
    calculate_task_score
)

class TestTaskService:
    """Test class for task service functions."""
    
    def test_get_open_tasks_returns_list(self, test_db):
        """Test that get_open_tasks returns a list."""
        # Arrange: Set up test database connection
        # Note: We need to mock the database connection for this test
        # For now, we'll test the function signature and basic behavior
        
        # Act: Call the function
        tasks = get_open_tasks()
        
        # Assert: Should return a list
        assert isinstance(tasks, list)
    
    def test_calculate_task_score_range(self):
        """Test that calculate_task_score returns a score between 0-100."""
        # Arrange: Create test task data
        test_task = {
            "urgency": "high",
            "potential_revenue": 10000,
            "customer_tier": "A",
            "days_since_last_action": 1,
            "days_until_followup": 2
        }
        
        # Act: Calculate score
        score = calculate_task_score(test_task)
        
        # Assert: Score should be between 0 and 100
        assert 0 <= score <= 100
        assert isinstance(score, (int, float))
    
    def test_calculate_task_score_different_scenarios(self):
        """Test task score calculation with different scenarios."""
        # High priority task
        high_priority = {
            "urgency": "high",
            "potential_revenue": 50000,
            "customer_tier": "A",
            "days_since_last_action": 0,
            "days_until_followup": 1
        }
        high_score = calculate_task_score(high_priority)
        
        # Low priority task
        low_priority = {
            "urgency": "low",
            "potential_revenue": 1000,
            "customer_tier": "C",
            "days_since_last_action": 30,
            "days_until_followup": 60
        }
        low_score = calculate_task_score(low_priority)
        
        # Assert: High priority should have higher score
        assert high_score > low_score
        assert 0 <= high_score <= 100
        assert 0 <= low_score <= 100
    
    def test_add_task_basic_functionality(self, test_db, sample_task_data):
        """Test that add_task can insert a task."""
        # Arrange: Use sample task data
        
        # Act: Add task (this would need database mocking for full test)
        # For now, we'll test the function exists and has correct signature
        result = add_task(sample_task_data)
        
        # Assert: Should return a boolean indicating success
        assert isinstance(result, bool)
    
    def test_get_quick_tasks_returns_list(self):
        """Test that get_quick_tasks returns a list."""
        # Act: Call the function
        tasks = get_quick_tasks()
        
        # Assert: Should return a list
        assert isinstance(tasks, list)
    
    def test_mark_task_done_function_exists(self):
        """Test that mark_task_done function exists and is callable."""
        # Assert: Function should exist and be callable
        assert callable(mark_task_done)
    
    def test_task_score_with_missing_fields(self):
        """Test task score calculation handles missing fields gracefully."""
        # Arrange: Task with missing fields
        incomplete_task = {
            "urgency": "medium",
            "potential_revenue": 5000
            # Missing other fields
        }
        
        # Act: Calculate score
        score = calculate_task_score(incomplete_task)
        
        # Assert: Should still return a valid score
        assert 0 <= score <= 100
        assert isinstance(score, (int, float))
    
    def test_task_score_edge_cases(self):
        """Test task score calculation with edge case values."""
        # Zero revenue
        zero_revenue_task = {
            "urgency": "high",
            "potential_revenue": 0,
            "customer_tier": "A",
            "days_since_last_action": 0,
            "days_until_followup": 0
        }
        zero_score = calculate_task_score(zero_revenue_task)
        assert 0 <= zero_score <= 100
        
        # Very high revenue
        high_revenue_task = {
            "urgency": "high",
            "potential_revenue": 1000000,
            "customer_tier": "A",
            "days_since_last_action": 0,
            "days_until_followup": 0
        }
        high_score = calculate_task_score(high_revenue_task)
        assert 0 <= high_score <= 100 