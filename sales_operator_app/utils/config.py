"""
Configuration constants and settings for Sales Operator app.
"""

# Database Configuration
DATABASE_PATH = "db/sales_operator.db"
DATABASE_TIMEOUT = 30

# Task Configuration
TASK_STATUSES = ["open", "in_progress", "completed", "cancelled"]
TASK_TYPES = ["normal", "quick", "followup", "meeting"]
TASK_URGENCIES = ["low", "medium", "high", "critical"]
CUSTOMER_TIERS = ["A", "B", "C", "D"]

# Lead Configuration
LEAD_STATUSES = ["new", "contacted", "qualified", "converted", "closed", "lost"]
LEAD_SOURCES = ["website", "referral", "cold_call", "social_media", "event", "other"]

# Scoring Configuration
MAX_TASK_SCORE = 100
MIN_TASK_SCORE = 0
REVENUE_WEIGHT = 0.4
URGENCY_WEIGHT = 0.3
CUSTOMER_TIER_WEIGHT = 0.2
TIME_WEIGHT = 0.1

# Application-wide constants
TIER_WEIGHTS = {'A': 3, 'B': 2, 'C': 1}
TASK_SCORE_WEIGHTS = {
    "revenue": 0.2,
    "tier": 0.2,
    "days_open": 0.4,
    "next_followup": 0.2
}
DEFAULT_FOLLOWUP_DAYS = 3

# UI Configuration
PAGE_TITLE = "Sales Operator"
PAGE_ICON = "📊"
LAYOUT = "wide"
THEME = "light"

# App Configuration
APP_VERSION = "1.0.0"
APP_NAME = "Sales Operator"
APP_DESCRIPTION = "A comprehensive sales management and task tracking application"

# Environment Configuration
ENVIRONMENT = "development"  # Can be overridden by environment variable
DEBUG_MODE = True

# Pagination Configuration
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# Date/Time Configuration
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
TIMEZONE = "UTC"

# Validation Configuration
MAX_NAME_LENGTH = 100
MAX_EMAIL_LENGTH = 255
MAX_COMPANY_LENGTH = 200
MAX_DESCRIPTION_LENGTH = 1000
MIN_REVENUE = 0.0
MAX_REVENUE = 999999999.99 