import tkinter as tk
from tkinter import ttk
from config import COLORS
from utils.binance_api import BinanceWebSocket  

class CryptoTicker:
    def __init__(self, parent, symbol, display_name):
        self.parent = parent
        self.symbol = symbol.lower()
        self.display_name = display_name
        self.is_active = False
        self.ws_manager = None 
        
        self.current_price = 0
        self.price_change = 0
        self.price_change_percent = 0
        self.volume = 0
        self.high_24h = 0
        self.low_24h = 0
        
        self.frame = ttk.Frame(parent, relief="solid", borderwidth=1, padding=4)
        
        style = ttk.Style()
        style.configure("Light.TFrame", background=COLORS["bg_light"])
        self.frame.configure(style="Light.TFrame")
        
        main_frame = ttk.Frame(self.frame, style="Light.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_columnconfigure(2, weight=1)
        
        # Row 0: currency&price
        row0_frame = ttk.Frame(main_frame, style="Light.TFrame")
        row0_frame.grid(row=0, column=0, columnspan=3, sticky="ew", pady=2)
        
        name_frame = ttk.Frame(row0_frame, style="Light.TFrame")
        name_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Label(name_frame, text=display_name, 
                 font=("Arial", 10, "bold"),
                 background=COLORS["bg_light"],
                 foreground=COLORS["text"]).pack(anchor=tk.W)
        
        self.price_label = tk.Label(row0_frame, text="--,---", 
                                    font=("Arial", 18, "bold"),
                                    bg=COLORS["bg_light"],
                                    fg=COLORS["text"])
        self.price_label.pack(side=tk.RIGHT)
        
        # Row 1: High/Low 
        row1_frame = ttk.Frame(main_frame, style="Light.TFrame")
        row1_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=2)
        
        hl_frame = ttk.Frame(row1_frame, style="Light.TFrame")
        hl_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # High
        high_frame = ttk.Frame(hl_frame, style="Light.TFrame")
        high_frame.pack(fill=tk.X, pady=1)
        
        ttk.Label(high_frame, text="24H High:", 
                 font=("Arial", 8),
                 background=COLORS["bg_light"],
                 foreground=COLORS["text_secondary"]).pack(side=tk.LEFT)
        
        self.high_label = tk.Label(high_frame, text="--", 
                                  font=("Arial", 9, "bold"),
                                  bg=COLORS["bg_light"],
                                  fg=COLORS["high"])
        self.high_label.pack(side=tk.LEFT, padx=2)
        
        # Low
        low_frame = ttk.Frame(hl_frame, style="Light.TFrame")
        low_frame.pack(fill=tk.X, pady=1)
        
        ttk.Label(low_frame, text="24H Low:", 
                 font=("Arial", 8),
                 background=COLORS["bg_light"],
                 foreground=COLORS["text_secondary"]).pack(side=tk.LEFT)
        
        self.low_label = tk.Label(low_frame, text="--", 
                                 font=("Arial", 9, "bold"),
                                 bg=COLORS["bg_light"],
                                 fg=COLORS["low"])
        self.low_label.pack(side=tk.LEFT, padx=2)
        
        # Row 2: Change + Vol 
        row2_frame = ttk.Frame(main_frame, style="Light.TFrame")
        row2_frame.grid(row=2, column=0, columnspan=3, sticky="ew", pady=2)
        
        right_frame = ttk.Frame(row2_frame, style="Light.TFrame")
        right_frame.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
        # 24H Change
        change_frame = ttk.Frame(right_frame, style="Light.TFrame")
        change_frame.pack(fill=tk.X, pady=1)
        
        ttk.Label(change_frame, text="24H Change:", 
                 font=("Arial", 8),
                 background=COLORS["bg_light"],
                 foreground=COLORS["text_secondary"]).pack(side=tk.LEFT)
        
        # frame for %
        change_display_frame = ttk.Frame(change_frame, style="Light.TFrame")
        change_display_frame.pack(side=tk.LEFT, padx=2)
        
        self.change_amount_label = tk.Label(change_display_frame, text="--", 
                                           font=("Arial", 9, "bold"),
                                           background=COLORS["bg_light"])
        self.change_amount_label.pack(side=tk.LEFT)
        
        self.change_percent_label = tk.Label(change_display_frame, text="(--%)", 
                                            font=("Arial", 9, "bold"),
                                            background=COLORS["bg_light"])
        self.change_percent_label.pack(side=tk.LEFT, padx=(2, 0))
        
        # Volume
        vol_frame = ttk.Frame(right_frame, style="Light.TFrame")
        vol_frame.pack(fill=tk.X, pady=1)
        
        ttk.Label(vol_frame, text="Vol:", 
                 font=("Arial", 8),
                 background=COLORS["bg_light"],
                 foreground=COLORS["text_secondary"]).pack(side=tk.LEFT)
        
        self.volume_label = ttk.Label(vol_frame, text="--", 
                                      font=("Arial", 9, "bold"),
                                      background=COLORS["bg_light"],
                                      foreground=COLORS["text"])
        self.volume_label.pack(side=tk.LEFT, padx=2)
    
    def start(self):
        if self.is_active:
            return
        
        self.is_active = True
        
        self.ws_manager = BinanceWebSocket(
            on_message_callback=self.on_message,
            on_error_callback=lambda err: print(f"{self.symbol} error: {err}")
        )

        self.ws_manager.connect_single(f"{self.symbol}@ticker")
    
    def stop(self):
        self.is_active = False
        if self.ws_manager:
            self.ws_manager.disconnect()
            self.ws_manager = None
    
    def on_message(self, data): 
        if not self.is_active:
            return

        price = float(data['c'])
        change = float(data['p'])  
        percent = float(data['P'])  
        volume = float(data['v'])
        high = float(data['h'])
        low = float(data['l'])
        
        self.current_price = price
        self.price_change = change
        self.price_change_percent = percent
        self.volume = volume
        self.high_24h = high
        self.low_24h = low
        
        self.parent.after(0, self.update_display, price, change, percent, volume, high, low)
    
    def update_display(self, price, change, percent, volume, high, low):
        if not self.is_active:
            return
        
        if change >= 0:
            color = COLORS["profit"]
            sign = "+"
        else:
            color = COLORS["loss"]
            sign = ""
        
        self.price_label.config(
            text=f"${price:,.2f}",
            fg=COLORS["text"]
        )
        
        self.high_label.config(text=f"${high:,.2f}")
        self.low_label.config(text=f"${low:,.2f}")

        self.change_amount_label.config(
            text=f"{sign}{abs(change):,.2f}",
            fg=color
        )
        
        self.change_percent_label.config(
            text=f"({sign}{abs(percent):.2f}%)",
            fg=color
        )
        
        volume_text = self.format_volume(volume)
        self.volume_label.config(text=volume_text)
    
    def format_volume(self, volume):
        if volume >= 1000000000:
            return f"{volume/1000000000:.2f}B"
        elif volume >= 1000000:
            return f"{volume/1000000:.2f}M"
        elif volume >= 1000:
            return f"{volume/1000:.2f}K"
        else:
            return f"{volume:,.0f}"
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
    def pack_forget(self):
        self.frame.pack_forget()
    
    def grid(self, **kwargs):
        self.frame.grid(**kwargs)
    
    def grid_forget(self):
        self.frame.grid_forget()