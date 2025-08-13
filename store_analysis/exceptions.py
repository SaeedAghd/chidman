"""
Custom exceptions for store analysis application.
"""

class StoreAnalysisError(Exception):
    """Base exception for store analysis errors."""
    pass

class AnalysisProcessingError(StoreAnalysisError):
    """Raised when analysis processing fails."""
    pass

class InvalidDataError(StoreAnalysisError):
    """Raised when invalid data is provided."""
    pass

class PaymentRequiredError(StoreAnalysisError):
    """Raised when payment is required but not provided."""
    pass

class FileProcessingError(StoreAnalysisError):
    """Raised when file processing fails."""
    pass

class AIAnalysisError(StoreAnalysisError):
    """Raised when AI analysis fails."""
    pass

class CacheError(StoreAnalysisError):
    """Raised when cache operations fail."""
    pass

class SecurityError(StoreAnalysisError):
    """Raised when security validation fails."""
    pass 