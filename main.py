import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from components.ticker import CryptoTicker
from components.orderbook import OrderBookPanel
from components.technical import TechnicalAnalysisPanel
from components.market_trade import MarketTrade
from config import SYMBOLS, COLORS

class CryptoDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Crypto Dashboard - Single Asset")
        self.root.geometry("1400x900")

        self.setup_styles()
        
        # Load saved preferences
        self.preferences = self.load_preferences()
        
        # Current viewing symbol
        self.current_symbol = self.preferences.get('current_symbol', 'btcusdt')
        
        # Active panels for current symbol
        self.ticker = None
        self.orderbook = None
        self.technical = None
        self.market_trade = None
        
        # Create main container
        self.main_container = ttk.Frame(root)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create control panel
        self.create_control_panel()
        
        # Create content area
        self.create_content_area()
        
        # Initialize with current symbol
        self.switch_currency(self.current_symbol)
        
        # Setup window close handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_styles(self):
        """Configure ttk styles."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        self.root.configure(bg=COLORS['bg_dark'])
        
        style.configure('TFrame', background=COLORS['bg_light'])
        style.configure('TLabel', background=COLORS['bg_light'], 
                       foreground=COLORS['text'])
        style.configure('TButton', background=COLORS['bg_light'],
                       foreground=COLORS['text'])
        style.configure('TLabelframe', background=COLORS['bg_light'],
                       foreground=COLORS['text'])
        style.configure('TLabelframe.Label', background=COLORS['bg_light'],
                       foreground=COLORS['text'])
        style.configure('TCheckbutton', background=COLORS['bg_light'],
                       foreground=COLORS['text'])
        style.configure('TRadiobutton', background=COLORS['bg_light'],
                       foreground=COLORS['text'])
        
        style.configure('TCombobox', 
                       fieldbackground='white',
                       background='white',
                       foreground=COLORS['text'])
    
    def load_preferences(self):
        """Load saved user preferences."""
        try:
            if os.path.exists('preferences.json'):
                with open('preferences.json', 'r') as f:
                    return json.load(f)
        except:
            pass
        return {
            'current_symbol': 'btcusdt',
            'visible_panels': ['ticker', 'orderbook', 'technical', 'market_trade']
        }
    
    def save_preferences(self):
        """Save user preferences."""
        self.preferences['current_symbol'] = self.current_symbol
        try:
            with open('preferences.json', 'w') as f:
                json.dump(self.preferences, f)
        except:
            pass
    
    def create_control_panel(self):
        """Create the top control panel with dropdown selector."""
        control_frame = tk.Frame(self.main_container, height=70, bg=COLORS['bg_dark'])
        control_frame.pack(fill=tk.X, padx=15, pady=10)
        control_frame.pack_propagate(False)
        
        title_label = tk.Label(control_frame, text="🚀 CRYPTO DASHBOARD", 
                              font=("Arial", 20, "bold"),
                              bg=COLORS['bg_dark'],
                              fg='white')
        title_label.pack(side=tk.LEFT, padx=20)
        
        selector_frame = tk.Frame(control_frame, bg=COLORS['bg_dark'])
        selector_frame.pack(side=tk.RIGHT, padx=20)
        
        tk.Label(selector_frame, text="Select Currency:", 
                font=("Arial", 12),
                bg=COLORS['bg_dark'],
                fg='white').pack(side=tk.LEFT, padx=(0, 10))
        
        self.currency_var = tk.StringVar()
        self.currency_combo = ttk.Combobox(
            selector_frame,
            textvariable=self.currency_var,
            values=[symbol_info['name'] for symbol_info in SYMBOLS],
            state='readonly',
            width=15,
            font=("Arial", 11),
            background='white'
        )
        self.currency_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        current_symbol_info = next((s for s in SYMBOLS if s['symbol'] == self.current_symbol), SYMBOLS[0])
        self.currency_var.set(current_symbol_info['name'])
        
        self.currency_combo.bind('<<ComboboxSelected>>', self.on_currency_selected)
        
        panels_frame = tk.Frame(control_frame, bg=COLORS['bg_dark'])
        panels_frame.pack(side=tk.LEFT, padx=50)
        
        tk.Label(panels_frame, text="Panels:", 
                font=("Arial", 12),
                bg=COLORS['bg_dark'],
                fg='white').pack(side=tk.LEFT, padx=(0, 10))
        
        self.panel_vars = {
            'ticker': tk.BooleanVar(value='ticker' in self.preferences['visible_panels']),
            'orderbook': tk.BooleanVar(value='orderbook' in self.preferences['visible_panels']),
            'technical': tk.BooleanVar(value='technical' in self.preferences['visible_panels']),
            'market_trade': tk.BooleanVar(value='market_trade' in self.preferences['visible_panels']),
        }
        
        panel_names = [
            ('ticker', '📈 Ticker'),
            ('orderbook', '📊 Order Book'),
            ('technical', '📉 Chart'),
            ('market_trade', '💹 Recent Trades'),
        ]
        
        for panel_id, panel_name in panel_names:
            cb = tk.Checkbutton(panels_frame, 
                              text=panel_name,
                              variable=self.panel_vars[panel_id],
                              command=lambda p=panel_id: self.toggle_panel_type(p),
                              bg=COLORS['bg_dark'],
                              fg='white',
                              selectcolor=COLORS['bg_dark'],
                              activebackground=COLORS['bg_dark'],
                              activeforeground='white',
                              font=("Arial", 10))
            cb.pack(side=tk.LEFT, padx=5)
    
    def create_content_area(self):
        """Create the main content area."""
        self.content_frame = tk.Frame(self.main_container, bg=COLORS['bg_dark'])
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 10))
        
        self.asset_display_frame = tk.Frame(self.content_frame, bg=COLORS['bg_dark'])
        self.asset_display_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.asset_name_label = tk.Label(self.asset_display_frame, 
                                        text="BTC/USDT",
                                        font=("Arial", 14, "bold"),
                                        bg=COLORS['bg_dark'],
                                        fg='white')
        self.asset_name_label.pack()
        
        self.panels_container = tk.Frame(self.content_frame, bg=COLORS['bg_dark'])
        self.panels_container.pack(fill=tk.BOTH, expand=True)
    
    def on_currency_selected(self, event=None):
        """Handle currency selection from dropdown."""
        selected_name = self.currency_var.get()
        if not selected_name:
            return
        
        symbol_info = next((s for s in SYMBOLS if s['name'] == selected_name), None)
        if not symbol_info:
            return
        
        symbol = symbol_info['symbol']
        
        self.switch_currency(symbol)
    
    def switch_currency(self, symbol):
        """Switch to a different currency."""
        self.stop_current_panels()
        
        self.current_symbol = symbol
        
        symbol_info = next((s for s in SYMBOLS if s['symbol'] == symbol), SYMBOLS[0])
        self.asset_name_label.config(text=symbol_info['name'])
        
        self.create_panels_for_symbol(symbol_info)
        
        self.save_preferences()
    
    def stop_current_panels(self):
        """Stop and remove all current panels."""
        if self.ticker:
            self.ticker.stop()
            self.ticker.frame.pack_forget()
            self.ticker = None
        
        if self.orderbook:
            self.orderbook.stop()
            self.orderbook.frame.pack_forget()
            self.orderbook = None
        
        if self.technical:
            self.technical.stop()
            self.technical.frame.pack_forget()
            self.technical = None
        
        if self.market_trade:
            self.market_trade.stop()
            self.market_trade.frame.pack_forget()
            self.market_trade = None
        
        for widget in self.panels_container.winfo_children():
            widget.destroy()
    
    def create_panels_for_symbol(self, symbol_info):
        """Create all panels for the current symbol."""
        symbol = symbol_info['symbol']
        name = symbol_info['name']
        
        # Main container
        main_bottom_frame = tk.Frame(self.panels_container, bg=COLORS['bg_dark'])
        main_bottom_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid
        main_bottom_frame.columnconfigure(0, weight=1)  # Column 0: Order Book
        main_bottom_frame.columnconfigure(1, weight=2)  # Column 1: Technical Chart 
        main_bottom_frame.columnconfigure(2, weight=1)  # Column 2: Ticker + Recent Trades
        main_bottom_frame.rowconfigure(0, weight=1)

        if self.panel_vars['orderbook'].get():
            orderbook_container = tk.Frame(main_bottom_frame, bg=COLORS['bg_dark'])
            orderbook_container.grid(row=0, column=0, padx=(0, 5), pady=5, sticky="nsew")
            
            self.orderbook = OrderBookPanel(orderbook_container, symbol)
            self.orderbook.pack(fill=tk.BOTH, expand=True)
            self.orderbook.start()
 
        if self.panel_vars['technical'].get():
            chart_container = tk.Frame(main_bottom_frame, bg=COLORS['bg_dark'])
            chart_container.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
            
            self.technical = TechnicalAnalysisPanel(chart_container, symbol)
            self.technical.pack(fill=tk.BOTH, expand=True)
            self.technical.start()
        
        if self.panel_vars['ticker'].get() or self.panel_vars['market_trade'].get():
            right_container = tk.Frame(main_bottom_frame, bg=COLORS['bg_dark'])
            right_container.grid(row=0, column=2, padx=(5, 0), pady=5, sticky="nsew")
            
            # Configure right container grid
            right_container.columnconfigure(0, weight=1)
            right_container.rowconfigure(0, weight=0)  
            right_container.rowconfigure(1, weight=1) 
            
            # Ticker panel (top)
            if self.panel_vars['ticker'].get():
                self.ticker = CryptoTicker(right_container, symbol, name)
                self.ticker.grid(row=0, column=0, padx=0, pady=(0, 5), sticky="nsew")
                self.ticker.start()
            
            # Recent Trades panel (bottom)
            if self.panel_vars['market_trade'].get():
                self.market_trade = MarketTrade(right_container, symbol)
                self.market_trade.grid(row=1, column=0, padx=0, pady=5, sticky="nsew")
                self.market_trade.start()
    
    def toggle_panel_type(self, panel_type):
        """Toggle a panel type on/off."""
        visible_panels = []
        for p, var in self.panel_vars.items():
            if var.get():
                visible_panels.append(p)
        self.preferences['visible_panels'] = visible_panels
        
        symbol_info = next((s for s in SYMBOLS if s['symbol'] == self.current_symbol), SYMBOLS[0])
        self.stop_current_panels()
        self.create_panels_for_symbol(symbol_info)
        
        self.save_preferences()
    
    def on_closing(self):
        """Clean shutdown of all WebSocket connections."""
        self.stop_current_panels()
        self.save_preferences()
        self.root.destroy()

def main():
    root = tk.Tk()
    
    root.title("Crypto Dashboard - Market Trade")
    
    try:
        app = CryptoDashboard(root)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start application: {str(e)}")
        return
    
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{1400}x{900}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()