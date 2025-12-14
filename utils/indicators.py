import numpy as np
from typing import List, Tuple

def calculate_rsi(prices: List[float], period: int = 14) -> float:
    """Calculate Relative Strength Index."""
    if len(prices) < period + 1:
        return 50
    
    deltas = np.diff(prices)
    seed = deltas[:period]
    
    up = seed[seed >= 0].sum() / period
    down = -seed[seed < 0].sum() / period
    
    if down == 0:
        return 100 if up > 0 else 50
    
    rs = up / down
    rsi = 100 - (100 / (1 + rs))
    return rsi


def calculate_moving_average(prices: List[float], period: int) -> float:
    """Calculate simple moving average."""
    if len(prices) < period:
        return sum(prices) / len(prices)
    return sum(prices[-period:]) / period


def calculate_bollinger_bands(prices: List[float], period: int = 20, 
                            num_std: float = 2) -> Tuple[float, float, float]:
    """Calculate Bollinger Bands."""
    if len(prices) < period:
        ma = sum(prices) / len(prices)
        std = np.std(prices) if len(prices) > 1 else 0
    else:
        ma = np.mean(prices[-period:])
        std = np.std(prices[-period:])
    
    upper = ma + (std * num_std)
    lower = ma - (std * num_std)
    
    return upper, ma, lower


def calculate_macd(prices: List[float], fast: int = 12, 
                  slow: int = 26, signal: int = 9) -> Tuple[float, float, float]:
    """Calculate MACD."""
    if len(prices) < slow:
        return 0, 0, 0
    
    # Calculate EMAs
    ema_fast = calculate_ema(prices, fast)
    ema_slow = calculate_ema(prices, slow)
    macd_line = ema_fast - ema_slow

    if len(prices) < slow + signal:
        signal_line = macd_line
    else:
        signal_line = calculate_ema(prices, signal)
    
    histogram = macd_line - signal_line
    
    return macd_line, signal_line, histogram


def calculate_ema(prices: List[float], period: int) -> float:
    """Calculate Exponential Moving Average."""
    if len(prices) < period:
        return sum(prices) / len(prices)
    
    multiplier = 2 / (period + 1)
    ema = prices[0]
    
    for price in prices[1:]:
        ema = (price * multiplier) + (ema * (1 - multiplier))
    
    return ema