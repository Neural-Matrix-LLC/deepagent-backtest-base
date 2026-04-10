from strategies import Strategy

class CustomTradingStrategy(Strategy):
    """Custom Trading Strategy"""

    name = "" # Set a unique name for your strategy
    lookback = 1 # Set lookback period if needed
    multi_asset = False # Set to True if your strategy operates on multiple assets
    default_tickers = [] # Set default tickers for your strategy (can be overridden via params)

    def validate_params(self, params):
        # Validate and set default parameters for your strategy
        # For example, ensure 'tickers' is provided or set to default
        params.setdefault("tickers", self.default_tickers)
        # Set default values for your strategy parameters
        params.setdefault("param_name", default_value) 
        return params


    def generate_signals(self, data, params):
        """Generate trading signals from price data.
        
        Single-asset strategies return a Signal dataclass.
        Multi-asset strategies return a DataFrame of position signals.
        """
        params = self.validate_params(params)
        # Implement your signal generation logic here using the input data and parameters.
        return None