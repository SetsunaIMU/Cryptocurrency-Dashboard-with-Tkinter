import websocket
import json
import threading
import requests

class BinanceWebSocket:
    def __init__(self, on_message_callback, on_error_callback=None):
        self.ws = None
        self.is_active = False
        self.on_message_callback = on_message_callback
        self.on_error_callback = on_error_callback
        
    def connect_single(self, stream_name):
        """Connect to a single WebSocket stream."""
        if self.is_active:
            self.disconnect()
            
        self.is_active = True
        stream_url = f"wss://stream.binance.com:9443/ws/{stream_name}"
        
        self.ws = websocket.WebSocketApp(
            stream_url,
            on_message=self._on_message_single,
            on_error=self._on_error,
            on_close=self._on_close,
            on_open=self._on_open
        )
        
        threading.Thread(target=self.ws.run_forever, daemon=True).start()
        return self
    
    def connect_multiple(self, streams):
        """Connect to multiple Binance WebSocket streams."""
        if self.is_active:
            self.disconnect()
            
        self.is_active = True
        stream_url = f"wss://stream.binance.com:9443/stream?streams={'/'.join(streams)}"
        
        self.ws = websocket.WebSocketApp(
            stream_url,
            on_message=self._on_message_multiple,
            on_error=self._on_error,
            on_close=self._on_close,
            on_open=self._on_open
        )
        
        threading.Thread(target=self.ws.run_forever, daemon=True).start()
        return self
    
    def _on_message_single(self, ws, message):
        """Handle single stream messages."""
        if not self.is_active:
            return
        
        try:
            data = json.loads(message)
            self.on_message_callback(data)
        except Exception as e:
            if self.on_error_callback:
                self.on_error_callback(f"Message error: {e}")
    
    def _on_message_multiple(self, ws, message):
        """Handle multiple streams messages."""
        if not self.is_active:
            return
        
        try:
            data = json.loads(message)
            self.on_message_callback(data)
        except Exception as e:
            if self.on_error_callback:
                self.on_error_callback(f"Message error: {e}")
    
    def _on_error(self, ws, error):
        """Handle WebSocket errors."""
        self.is_active = False 
        if self.on_error_callback:
            self.on_error_callback(f"WebSocket error: {error}")
    
    def _on_close(self, ws, close_status_code, close_msg):
        self.is_active = False
    
    def _on_open(self, ws):
        pass
    
    def disconnect(self):
        """Disconnect WebSocket."""
        self.is_active = False
        if self.ws:
            self.ws.close()
            self.ws = None

def get_order_book(symbol, limit=10):
    """Get order book data from Binance REST API."""
    try:
        url = f"https://api.binance.com/api/v3/depth"
        params = {"symbol": symbol.upper(), "limit": limit}
        response = requests.get(url, params=params)
        return response.json()
    except Exception as e:
        print(f"Error fetching order book: {e}")
        return None

def get_recent_trades(symbol, limit=20):
    """Get recent trades from Binance."""
    try:
        url = f"https://api.binance.com/api/v3/trades"
        params = {"symbol": symbol.upper(), "limit": limit}
        response = requests.get(url, params=params)
        return response.json()
    except Exception as e:
        print(f"Error fetching trades: {e}")
        return None

def get_klines(symbol, interval="1h", limit=100):
    """Get candlestick data."""
    try:
        url = f"https://api.binance.com/api/v3/klines"
        params = {
            "symbol": symbol.upper(),
            "interval": interval,
            "limit": limit
        }
        response = requests.get(url, params=params)
        return response.json()
    except Exception as e:
        print(f"Error fetching klines: {e}")
        return None