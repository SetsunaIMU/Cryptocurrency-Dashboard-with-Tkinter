import tkinter as tk
from tkinter import ttk
import threading
from datetime import datetime
from utils.binance_api import get_recent_trades
from config import COLORS
class MarketTrade:
    def __init__(self, parent, symbol):
        self.parent = parent
        self.symbol = symbol.upper()
        self.is_active = False
        
        # Recent trades data
        self.recent_trades = []
        
        # Create UI
        self.frame = ttk.LabelFrame(parent, text=f"Recent Trades - {self.symbol}", 
                                   padding=5)
        
        # Header 
        header_frame = ttk.Frame(self.frame)
        header_frame.pack(fill=tk.X, pady=(0, 5))
        
        headers = [
            ("Price (USDT)", 15),
            ("Amount", 12), 
            ("Time", 10)
            ]
        for text, width in headers:
            ttk.Label(header_frame, text=text, 
                font=("Arial", 9, "bold"), width=width).pack(side=tk.LEFT, padx=2)

        # Trades display area
        trades_frame = ttk.Frame(self.frame)
        trades_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create text widget for trades
        self.trades_text = tk.Text(trades_frame, 
                                  height=15, 
                                  width=45,
                                  font=("Consolas", 9),
                                  bg='white',
                                  state='disabled')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(trades_frame, orient="vertical", command=self.trades_text.yview)
        self.trades_text.configure(yscrollcommand=scrollbar.set)
        
        self.trades_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure text tags for colors
        self.trades_text.tag_config('buy', foreground=COLORS['profit'])     
        self.trades_text.tag_config('sell', foreground=COLORS['loss'])    
        
        # Status label
        self.status_label = ttk.Label(self.frame, text="", font=("Arial", 8))
        self.status_label.pack(pady=5)
    
    def start(self):
        """Start auto-refresh."""
        self.is_active = True
        self.refresh_trades()
        self.auto_refresh()
    
    def stop(self):
        """Stop auto-refresh."""
        self.is_active = False
    
    def auto_refresh(self):
        """Auto-refresh every 2 seconds."""
        if not self.is_active:
            return
        
        self.parent.after(2000, self.auto_refresh)
        self.refresh_trades()
    
    def refresh_trades(self):
        """Fetch recent trades from Binance."""
        def fetch_data():
            try:
                trades_data = get_recent_trades(self.symbol, limit=40)
                
                if trades_data:  
                    self.parent.after(0, self.update_trades_display, trades_data)
                    
            except Exception as e:
                print(f"Error fetching trades: {e}")
        
        # Run in background thread
        threading.Thread(target=fetch_data, daemon=True).start()
    
    def update_trades_display(self, trades_data):
        """Update the trades display."""
        if not self.is_active:
            return
        
        # Update status
        self.status_label.config(text=f"Last update: {datetime.now().strftime('%H:%M:%S')}")
        
        # Clear text widget
        self.trades_text.config(state='normal')
        self.trades_text.delete(1.0, tk.END)
        
        # Add trades
        for trade in reversed(trades_data[:30]):
            try:
                # Format time
                trade_time = datetime.fromtimestamp(trade['time'] / 1000).strftime("%H:%M:%S")
                
                # Get data
                price = float(trade['price'])
                amount = float(trade['qty'])
                
                # Determine if buy or sell
                # ❗️ สำคัญ: ใน Binance isBuyerMaker มีความหมายต่างกัน
                # isBuyerMaker = True → ผู้ซื้อเป็น maker = SELL order (แดง)
                # isBuyerMaker = False → ผู้ขายเป็น maker = BUY order (เขียว)
                is_buy = not trade['isBuyerMaker']  
                tag = 'buy' if is_buy else 'sell'
                
                # Format line
                price_str = f"{price:>12,.2f}"
                amount_str = f"{amount:>10,.4f}"
                time_str = f"{trade_time:>10}"
                
                line = f"{price_str} | {amount_str} | {time_str}\n"
                
                # Insert with color tag
                self.trades_text.insert(tk.END, line, tag)
                
            except Exception as e:
                print(f"Error processing trade: {e}")
        
        # Scroll to top
        self.trades_text.see(1.0)
        self.trades_text.config(state='disabled')
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
    def pack_forget(self):
        self.frame.pack_forget()
    
    def grid(self, **kwargs):
        self.frame.grid(**kwargs)
    
    def grid_forget(self):
        self.frame.grid_forget()