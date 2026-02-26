"""
ASES Configuration Module
Centralized configuration for the Autonomous Strategy Evolution System
"""
import os
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

# Firebase Configuration
@dataclass
class FirebaseConfig:
    """Firebase configuration for state management"""
    project_id: str = os.getenv("FIREBASE_PROJECT_ID", "ases-trading")
    credential_path: str = os.getenv("FIREBASE_CREDENTIAL_PATH", "./serviceAccountKey.json")
    collection_prefix: str = "ases_"
    
    def get_collection_name(self, entity: str) -> str:
        """Generate collection name with prefix"""
        return f"{self.collection_prefix}{entity}"

# Exchange Configuration
@dataclass
class ExchangeConfig:
    """Exchange connection configuration"""
    exchange_id: str = "binance"
    api_key: str = os.getenv("EXCHANGE_API_KEY", "")
    api_secret: str = os.getenv("EXCHANGE_API_SECRET", "")
    sandbox_mode: bool = True  # Start in paper trading mode
    rate_limit: int = 10  # requests per second
    timeout: int = 30  # seconds

# System Configuration
@dataclass
class SystemConfig:
    """System-wide configuration"""
    log_level: str = "INFO"
    max_concurrent_strategies: int = 5
    evolution_cycle_hours: int = 24
    min_backtest_period_days: int = 30
    max_drawdown_threshold: float = 0.20  # 20% max drawdown
    min_sharpe_ratio: float = 1.0
    
    # Performance thresholds
    performance_thresholds: Dict[str, float] = field(default_factory=lambda: {
        "min_profit_factor": 1.5,
        "min_win_rate": 0.45,
        "max_daily_loss": 0.05,
        "min_trades_per_day": 3
    })

# Strategy Configuration
@dataclass 
class StrategyConfig:
    """Strategy generation and testing configuration"""
    available_timeframes: list = field(default_factory=lambda: ["5m", "15m", "1h", "4h", "1d"])
    max_indicators_per_strategy: int = 5
    available_indicators: list = field(default_factory=lambda: [
        "sma", "ema", "rsi", "macd", "bollinger_bands", 
        "atr", "stochastic", "obv", "vwap"
    ])
    min_correlation_threshold: float = 0.3
    max_correlation_threshold: float = 0.8

@dataclass
class ASESConfig:
    """Main configuration container"""
    firebase: FirebaseConfig = field(default_factory=FirebaseConfig)
    exchange: ExchangeConfig = field(default_factory=ExchangeConfig)
    system: SystemConfig = field(default_factory=SystemConfig)
    strategy: StrategyConfig = field(default_factory=StrategyConfig)
    
    @classmethod
    def load_from_env(cls) -> "ASESConfig":
        """Load configuration from environment variables"""
        return cls()

# Initialize global configuration
config = ASESConfig.load_from_env()