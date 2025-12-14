import tkinter as tk
from tkinter import ttk
from utils.binance_api import get_klines
from utils.indicators import calculate_rsi, calculate_moving_average, calculate_bollinger_bands
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import threading

class TechnicalAnalysisPanel:
    def __init__(self, parent, symbol):
        self.parent = parent
        self.symbol = symbol
        self.is_active = False
        self.current_interval = "1h"
        
        # Create UI
        self.frame = ttk.LabelFrame(parent, text=f"Technical Analysis - {symbol.upper()}", 
                                   padding=10)
        
        # Interval selector
        interval_frame = ttk.Frame(self.frame)
        interval_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(interval_frame, text="Interval:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.interval_var = tk.StringVar(value="1h")
        intervals = ["1m", "5m", "15m", "1h", "4h", "1d"]
        
        for interval in intervals:
            rb = ttk.Radiobutton(interval_frame, text=interval, value=interval,
                                variable=self.interval_var,
                                command=self.on_interval_change)
            rb.pack(side=tk.LEFT, padx=2)
        
        # Chart area
        self.chart_frame = ttk.Frame(self.frame)
        self.chart_frame.pack(fill=tk.BOTH, expand=True)
        
        self.figure = Figure(figsize=(8, 4), dpi=100)
        self.canvas = None
        
        # Indicators panel
        indicators_frame = ttk.LabelFrame(self.frame, text="Indicators", padding=10)
        indicators_frame.pack(fill=tk.X, pady=10)
        
        # Create indicator labels
        indicators_grid = ttk.Frame(indicators_frame)
        indicators_grid.pack()
        
        # Row 1
        ttk.Label(indicators_grid, text="RSI (14):", font=("Arial", 9)).grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.rsi_label = ttk.Label(indicators_grid, text="--", font=("Arial", 9, "bold"))
        self.rsi_label.grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(indicators_grid, text="MA (20):", font=("Arial", 9)).grid(
            row=0, column=2, sticky=tk.W, padx=20, pady=2)
        self.ma_label = ttk.Label(indicators_grid, text="--", font=("Arial", 9, "bold"))
        self.ma_label.grid(row=0, column=3, sticky=tk.W, padx=5, pady=2)
        
        # Row 2
        ttk.Label(indicators_grid, text="BB Upper:", font=("Arial", 9)).grid(
            row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.bb_upper_label = ttk.Label(indicators_grid, text="--", font=("Arial", 9, "bold"))
        self.bb_upper_label.grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(indicators_grid, text="BB Middle:", font=("Arial", 9)).grid(
            row=1, column=2, sticky=tk.W, padx=20, pady=2)
        self.bb_middle_label = ttk.Label(indicators_grid, text="--", font=("Arial", 9, "bold"))
        self.bb_middle_label.grid(row=1, column=3, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(indicators_grid, text="BB Lower:", font=("Arial", 9)).grid(
            row=1, column=4, sticky=tk.W, padx=20, pady=2)
        self.bb_lower_label = ttk.Label(indicators_grid, text="--", font=("Arial", 9, "bold"))
        self.bb_lower_label.grid(row=1, column=5, sticky=tk.W, padx=5, pady=2)
    
    def start(self):
        """Start the panel."""
        self.is_active = True
        self.refresh_data()
    
    def stop(self):
        """Stop the panel."""
        self.is_active = False
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None
    
    def on_interval_change(self):
        """Handle interval change."""
        self.current_interval = self.interval_var.get()
        self.refresh_data()
    
    def refresh_data(self):
        """Fetch and update chart data."""
        def fetch_and_update():
            klines = get_klines(self.symbol, self.current_interval, 100)
            if klines:
                self.parent.after(0, self.update_chart, klines)
        
        threading.Thread(target=fetch_and_update, daemon=True).start()
    
    def update_chart(self, klines):
        """Update the candlestick chart."""
        if not self.is_active:
            return

        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        
        self.figure.clear()       

        opens = []
        highs = []
        lows = []
        closes = []
        dates = []        

        for k in klines:
            dates.append(int(k[0]) / 1000)
            opens.append(float(k[1]))
            highs.append(float(k[2]))
            lows.append(float(k[3]))
            closes.append(float(k[4]))

        ax = self.figure.add_subplot(111)
        width = 0.7
        
        for i in range(len(dates)):
            if closes[i] >= opens[i]:
                color = 'green'
            else:
                color = 'red'
            ax.plot([i, i], [lows[i], highs[i]], color=color, linewidth=1)
            
            # Plot body
            ax.add_patch(plt.Rectangle((i - width/2, min(opens[i], closes[i])), 
                                      width, abs(closes[i] - opens[i]), 
                                      facecolor=color, edgecolor=color))
        
        # Calculate and plot moving average
        ma_period = 20
        if len(closes) >= ma_period:
            ma_values = [np.mean(closes[max(0, i-ma_period+1):i+1]) 
                        for i in range(len(closes))]
            ax.plot(ma_values, color='orange', label=f'MA{ma_period}', linewidth=1.5)
        
        ax.set_title(f'{self.symbol.upper()} - {self.current_interval}')
        ax.set_ylabel('Price (USDT)')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Update indicators
        if len(closes) > 14:
            rsi = calculate_rsi(closes)
            self.rsi_label.config(text=f"{rsi:.2f}")
            
            ma = calculate_moving_average(closes, 20)
            self.ma_label.config(text=f"{ma:.2f}")
            
            bb_upper, bb_middle, bb_lower = calculate_bollinger_bands(closes)
            self.bb_upper_label.config(text=f"{bb_upper:.2f}")
            self.bb_middle_label.config(text=f"{bb_middle:.2f}")
            self.bb_lower_label.config(text=f"{bb_lower:.2f}")
        
        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.figure, self.chart_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
    def pack_forget(self):
        self.frame.pack_forget()
    
    def grid(self, **kwargs):
        self.frame.grid(**kwargs)
    
    def grid_forget(self):
        self.frame.grid_forget()