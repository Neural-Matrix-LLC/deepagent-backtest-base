#!/usr/bin/env python3
"""
Trading Strategy Definitions
Each strategy implements generate_signals() returning entry/exit signals.
"""

import numpy as np
import pandas as pd
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class Signal:
    """Trading signal with entry/exit information."""
    entry: bool = False
    exit: bool = False
    direction: str = "long"  # "long" or "short"
    strength: float = 1.0    # Signal strength 0-1


class Strategy(ABC):
    """Base class for all trading strategies."""
    
    name: str = "base"
    lookback: int = 1
    multi_asset: bool = False
    
    @abstractmethod
    def generate_signals(self, data: pd.DataFrame, params: Dict[str, Any]) -> 'Signal | pd.DataFrame':
        """Generate trading signals from price data.
        
        Single-asset strategies return a Signal dataclass.
        Multi-asset strategies return a DataFrame of position signals.
        """
        pass
    
    def validate_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and set default parameters."""
        return params


