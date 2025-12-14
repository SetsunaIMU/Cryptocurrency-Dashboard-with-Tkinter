import tkinter as tk
from tkinter import ttk
from utils.binance_api import get_order_book
import threading
import time

class OrderBookPanel:
    def __init__(self, parent, symbol):
        self.parent = parent
        self.symbol = symbol
        self.is_active = False
        
        # Create UI
        self.frame = ttk.LabelFrame(parent, text=f"Order Book - {symbol.upper()}", 
                                   padding=10)
        
        # Create headers
        header_frame = ttk.Frame(self.frame)
        header_frame.pack(fill=tk.X)
        
        ttk.Label(header_frame, text="Price (USDT)", font=("Arial", 10, "bold"),
                 width=15).pack(side=tk.LEFT, padx=2)
        ttk.Label(header_frame, text="Amount", font=("Arial", 10, "bold"),
                 width=15).pack(side=tk.LEFT, padx=2)
        ttk.Label(header_frame, text="Total", font=("Arial", 10, "bold"),
                 width=15).pack(side=tk.LEFT, padx=2)
        
        # Separator
        ttk.Separator(self.frame, orient='horizontal').pack(fill=tk.X, pady=5)
        
        # BIDS Section
        ttk.Label(self.frame, text="🟢 BIDS (BUY)", font=("Arial", 11, "bold"),
                 foreground="green").pack()
        
        self.bids_frame = ttk.Frame(self.frame)
        self.bids_frame.pack(fill=tk.X)
        
        self.bid_labels = []
        for i in range(10):
            frame = ttk.Frame(self.bids_frame)
            frame.pack(fill=tk.X, pady=1)
            
            price_label = ttk.Label(frame, text="--", font=("Arial", 9), width=15)
            price_label.pack(side=tk.LEFT, padx=2)
            
            amount_label = ttk.Label(frame, text="--", font=("Arial", 9), width=15)
            amount_label.pack(side=tk.LEFT, padx=2)
            
            total_label = ttk.Label(frame, text="--", font=("Arial", 9), width=15)
            total_label.pack(side=tk.LEFT, padx=2)
            
            self.bid_labels.append((price_label, amount_label, total_label))
        
        # Separator
        ttk.Separator(self.frame, orient='horizontal').pack(fill=tk.X, pady=10)
        
        # ASKS Section
        ttk.Label(self.frame, text="🔴 ASKS (SELL)", font=("Arial", 11, "bold"),
                 foreground="red").pack()
        
        self.asks_frame = ttk.Frame(self.frame)
        self.asks_frame.pack(fill=tk.X)
        
        self.ask_labels = []
        for i in range(10):
            frame = ttk.Frame(self.asks_frame)
            frame.pack(fill=tk.X, pady=1)
            
            price_label = ttk.Label(frame, text="--", font=("Arial", 9), width=15)
            price_label.pack(side=tk.LEFT, padx=2)
            
            amount_label = ttk.Label(frame, text="--", font=("Arial", 9), width=15)
            amount_label.pack(side=tk.LEFT, padx=2)
            
            total_label = ttk.Label(frame, text="--", font=("Arial", 9), width=15)
            total_label.pack(side=tk.LEFT, padx=2)
            
            self.ask_labels.append((price_label, amount_label, total_label))
        

    def start(self):
        """Start auto-refresh."""
        self.is_active = True
        self.refresh_data()
        self.auto_refresh()
    
    def stop(self):
        """Stop auto-refresh."""
        self.is_active = False
    
    def auto_refresh(self):
        """Auto-refresh order book every 5 seconds."""
        if not self.is_active:
            return
        
        self.refresh_data()
        self.parent.after(5000, self.auto_refresh)
    
    def refresh_data(self):
        """Fetch and display order book data."""
        def fetch_and_update():
            data = get_order_book(self.symbol, limit=10)
            if data:
                self.parent.after(0, self.update_display, data)
        
        threading.Thread(target=fetch_and_update, daemon=True).start()
    
    def update_display(self, data):
        """Update order book display."""
        if not self.frame.winfo_exists():
            return  
        for price_label, amount_label, total_label in self.bid_labels + self.ask_labels:
            if not price_label.winfo_exists():
                return
        bids = data.get('bids', [])[:10]
        asks = data.get('asks', [])[:10]
        
        # Update BIDS 
        for i, (price_label, amount_label, total_label) in enumerate(self.bid_labels):
            if i < len(bids):
                price, amount = bids[i]
                total = float(price) * float(amount)
                price_label.config(text=f"{float(price):,.2f}", foreground="green")
                amount_label.config(text=f"{float(amount):,.4f}")
                total_label.config(text=f"{total:,.2f}")
            else:
                price_label.config(text="--")
                amount_label.config(text="--")
                total_label.config(text="--")
        
        # Update ASKS
        asks_reversed = list(reversed(asks))
        
        for i, (price_label, amount_label, total_label) in enumerate(self.ask_labels):
            if i < len(asks_reversed):
                price, amount = asks_reversed[i]
                total = float(price) * float(amount)
                price_label.config(text=f"{float(price):,.2f}", foreground="red")
                amount_label.config(text=f"{float(amount):,.4f}")
                total_label.config(text=f"{total:,.2f}")
            else:
                price_label.config(text="--")
                amount_label.config(text="--")
                total_label.config(text="--")
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
    def pack_forget(self):
        self.frame.pack_forget()
    
    def grid(self, **kwargs):
        self.frame.grid(**kwargs)
    
    def grid_forget(self):
        self.frame.grid_forget()