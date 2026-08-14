# app/__init__.py
# This file makes 'app' a Python package.

# Import all models for easy access
from app.models import (
    Farmer,
    GenderEnum,
    FarmerStatusEnum,
    Enterprise,
    EnterpriseTypeEnum,
    EnterpriseStatusEnum,
    DigitalIdentity,
    Loan,
    LoanStatusEnum,
    LoanPurposeEnum,
    LoanTypeEnum,
    RepaymentFrequencyEnum,
    Repayment,
    RepaymentMethodEnum,
    RepaymentStatusEnum,
    RepaymentSourceEnum,
    User,
)

# Import all schemas for easy access
from app.schemas import (
    FarmerBase,
    FarmerCreate,
    FarmerUpdate,
    FarmerResponse,
    FarmerListResponse,
    EnterpriseBase,
    EnterpriseCreate,
    EnterpriseUpdate,
    EnterpriseResponse,
    LoanBase,
    LoanCreate,
    LoanUpdate,
    LoanResponse,
    LoanListResponse,
    UserRegister,
    UserLogin,
    Token,
    TokenData,
)

# Import AI modules
from app.ai import (
    SatelliteAnalyzer,
    WeatherProcessor,
    YieldPredictor,
    CreditScorer,
)

__all__ = [
    # Models
    "Farmer",
    "GenderEnum",
    "FarmerStatusEnum",
    "Enterprise",
    "EnterpriseTypeEnum",
    "EnterpriseStatusEnum",
    "DigitalIdentity",
    "Loan",
    "LoanStatusEnum",
    "LoanPurposeEnum",
    "LoanTypeEnum",
    "RepaymentFrequencyEnum",
    "Repayment",
    "RepaymentMethodEnum",
    "RepaymentStatusEnum",
    "RepaymentSourceEnum",
    "User",
    # Schemas
    "FarmerBase",
    "FarmerCreate",
    "FarmerUpdate",
    "FarmerResponse",
    "FarmerListResponse",
    "EnterpriseBase",
    "EnterpriseCreate",
    "EnterpriseUpdate",
    "EnterpriseResponse",
    "LoanBase",
    "LoanCreate",
    "LoanUpdate",
    "LoanResponse",
    "LoanListResponse",
    "UserRegister",
    "UserLogin",
    "Token",
    "TokenData",
    # AI
    "SatelliteAnalyzer",
    "WeatherProcessor",
    "YieldPredictor",
    "CreditScorer",
]
# app/services/__init__.py
from app.services.farmer_service import FarmerService
from app.services.loan_service import LoanService
from app.services.medf_service import MEDFService
from app.services.blockchain import BlockchainService
from app.services.satellite_service import SatelliteService
from app.services.weather_service import WeatherService

__all__ = [
    "FarmerService",
    "LoanService",
    "MEDFService",
    "BlockchainService",
    "SatelliteService",
    "WeatherService",
]