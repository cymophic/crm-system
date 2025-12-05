# Date Formats
DATE_FORMAT = "M d, Y"  # e.g., Jan 15, 2025
SHORT_DATE_FORMAT = "m/d/Y"  # e.g., 01/15/2025
DATE_INPUT_FORMATS = [
    "%Y-%m-%d",  # 2025-01-15
    "%m/%d/%Y",  # 01/15/2025
    "%m/%d/%y",  # 01/15/25
]

# Time Formats
TIME_FORMAT = "g:i A"  # e.g., 2:30 PM
SHORT_TIME_FORMAT = "H:i"  # e.g., 14:30
DATETIME_FORMAT = "M d, Y g:i A"  # e.g., Jan 15, 2025 2:30 PM
SHORT_DATETIME_FORMAT = "m/d/Y H:i"  # e.g., 01/15/2025 14:30

# Number Formats
USE_THOUSAND_SEPARATOR = True
THOUSAND_SEPARATOR = ","
DECIMAL_SEPARATOR = "."
NUMBER_GROUPING = 3
