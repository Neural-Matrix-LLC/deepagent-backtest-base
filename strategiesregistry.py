# Strategy registry
from strategies import Strategy
from customstrategy.customtradingstrategy import CustomTradingStrategy
from typing import Dict


STRATEGIES = {"custom_trading_strategy": CustomTradingStrategy()}


def get_strategy(name: str) -> Strategy:
    """Get strategy by name."""
    if name not in STRATEGIES:
        raise ValueError(f"Unknown strategy: {name}. Available: {list(STRATEGIES.keys())}")
    return STRATEGIES[name]


def list_strategies() -> Dict[str, str]:
    """List all available strategies with descriptions."""
    return {name: strategy.__doc__.split('\n')[0] for name, strategy in STRATEGIES.items()}