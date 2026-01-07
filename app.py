"""
SafarPak - Pakistan's Ultimate Travel Companion
Premium UI with themes, accessibility, responsive design, drive mode & offline support
"""

import streamlit as st
import pandas as pd
import folium
from folium import plugins
from streamlit_folium import st_folium
import time
import json
import base64
from datetime import datetime
from dijkstra import load_cities, build_graph, dijkstra, calculate_distance_km
from locations_data import get_all_locations, get_location_categories


# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="SafarPak",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================== THEME SYSTEM ====================
def get_theme_css(theme):
    """Return CSS for different themes."""
    
    themes = {
        "dark": {
            "bg_primary": "#0a0a0f",
            "bg_secondary": "#12121a",
            "bg_card": "#1a1a24",
            "bg_card_hover": "#22222e",
            "accent": "#22c55e",
            "accent_hover": "#16a34a",
            "text_primary": "#fafafa",
            "text_secondary": "#a1a1aa",
            "text_muted": "#71717a",
            "border": "#27272a",
            "success": "#22c55e",
            "warning": "#f59e0b",
            "error": "#ef4444",
            "info": "#3b82f6",
        },
        "light": {
            "bg_primary": "#fafafa",
            "bg_secondary": "#f4f4f5",
            "bg_card": "#ffffff",
            "bg_card_hover": "#f4f4f5",
            "accent": "#16a34a",
            "accent_hover": "#15803d",
            "text_primary": "#18181b",
            "text_secondary": "#52525b",
            "text_muted": "#a1a1aa",
            "border": "#e4e4e7",
            "success": "#16a34a",
            "warning": "#d97706",
            "error": "#dc2626",
            "info": "#2563eb",
        },
        "colorblind": {
            "bg_primary": "#0a0a0f",
            "bg_secondary": "#12121a",
            "bg_card": "#1a1a24",
            "bg_card_hover": "#22222e",
            "accent": "#0077bb",  # Blue - safe for most color blindness
            "accent_hover": "#005588",
            "text_primary": "#fafafa",
            "text_secondary": "#a1a1aa",
            "text_muted": "#71717a",
            "border": "#27272a",
            "success": "#0077bb",  # Blue instead of green
            "warning": "#ee7733",  # Orange - distinguishable
            "error": "#cc3311",    # Red-orange
            "info": "#33bbee",     # Cyan
        }
    }
    
    t = themes.get(theme, themes["dark"])
    
    return f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        :root {{
            --bg-primary: {t['bg_primary']};
            --bg-secondary: {t['bg_secondary']};
            --bg-card: {t['bg_card']};
            --bg-card-hover: {t['bg_card_hover']};
            --accent: {t['accent']};
            --accent-hover: {t['accent_hover']};
            --text-primary: {t['text_primary']};
            --text-secondary: {t['text_secondary']};
            --text-muted: {t['text_muted']};
            --border: {t['border']};
            --success: {t['success']};
            --warning: {t['warning']};
            --error: {t['error']};
            --info: {t['info']};
        }}
        
        * {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }}
        
        .stApp {{
            background: var(--bg-primary);
        }}
        
        #MainMenu, footer, header {{visibility: hidden;}}
        
        /* ===== RESPONSIVE CONTAINER ===== */
        .main-container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 1rem;
        }}
        
        /* Small Mobile (< 480px) */
        @media (max-width: 480px) {{
            .main-container {{
                padding: 0.25rem;
            }}
        }}
        
        /* Mobile (480px - 768px) */
        @media (max-width: 768px) {{
            .main-container {{
                padding: 0.5rem;
            }}
        }}
        
        /* Tablet (768px - 1024px) */
        @media (min-width: 768px) and (max-width: 1024px) {{
            .main-container {{
                padding: 0.75rem;
            }}
        }}
        
        /* Desktop (1024px - 1440px) */
        @media (min-width: 1024px) and (max-width: 1440px) {{
            .main-container {{
                padding: 1rem;
            }}
        }}
        
        /* Large Desktop (> 1440px) */
        @media (min-width: 1440px) {{
            .main-container {{
                padding: 1.5rem;
                max-width: 1600px;
            }}
        }}
        
        /* ===== HEADER ===== */
        .app-header {{
            text-align: center;
            padding: 2rem 1rem;
            margin-bottom: 1.5rem;
        }}
        
        .app-logo {{
            font-size: 3.5rem;
            margin-bottom: 0.5rem;
        }}
        
        /* Small Mobile */
        @media (max-width: 480px) {{
            .app-logo {{
                font-size: 2rem;
            }}
            .app-header {{
                padding: 1rem 0.5rem;
            }}
        }}
        
        /* Mobile */
        @media (max-width: 768px) {{
            .app-logo {{
                font-size: 2.5rem;
            }}
            .app-header {{
                padding: 1.5rem 1rem;
            }}
        }}
        
        /* Tablet */
        @media (min-width: 768px) and (max-width: 1024px) {{
            .app-logo {{
                font-size: 3rem;
            }}
        }}
        
        .app-title {{
            font-size: clamp(2rem, 5vw, 3rem);
            font-weight: 800;
            color: var(--accent);
            margin: 0;
            letter-spacing: -1px;
        }}
        
        .app-subtitle {{
            color: var(--text-secondary);
            font-size: clamp(0.875rem, 2vw, 1rem);
            margin-top: 0.5rem;
            font-weight: 400;
        }}
        
        /* ===== CARDS ===== */
        .card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            transition: all 0.2s ease;
        }}
        
        .card:hover {{
            border-color: var(--accent);
            background: var(--bg-card-hover);
        }}
        
        /* Small Mobile */
        @media (max-width: 480px) {{
            .card {{
                padding: 0.75rem;
                border-radius: 10px;
            }}
        }}
        
        /* Mobile */
        @media (max-width: 768px) {{
            .card {{
                padding: 1rem;
                border-radius: 12px;
            }}
        }}
        
        /* ===== INPUT SECTION ===== */
        .input-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
            margin-bottom: 1rem;
        }}
        
        /* Small Mobile & Mobile */
        @media (max-width: 768px) {{
            .input-grid {{
                grid-template-columns: 1fr;
                gap: 0.75rem;
            }}
        }}
        
        /* Tablet */
        @media (min-width: 768px) and (max-width: 1024px) {{
            .input-grid {{
                gap: 0.875rem;
            }}
        }}
        
        .input-card {{
            background: var(--bg-card);
            border: 2px solid var(--border);
            border-radius: 12px;
            padding: 1rem;
            transition: all 0.2s ease;
        }}
        
        .input-card:focus-within {{
            border-color: var(--accent);
        }}
        
        .input-label {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: var(--text-secondary);
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 0.5rem;
        }}
        
        .input-icon {{
            font-size: 1.25rem;
        }}
        
        /* ===== DROPDOWNS ===== */
        .stSelectbox > div > div {{
            background: var(--bg-secondary) !important;
            border: 2px solid var(--border) !important;
            border-radius: 10px !important;
            color: var(--text-primary) !important;
            font-weight: 500 !important;
        }}
        
        .stSelectbox > div > div:focus-within {{
            border-color: var(--accent) !important;
        }}
        
        [data-baseweb="select"] > div {{
            background: var(--bg-secondary) !important;
            color: var(--text-primary) !important;
        }}
        
        [data-baseweb="select"] input {{
            color: var(--text-primary) !important;
            background: transparent !important;
        }}
        
        [data-baseweb="select"] span {{
            color: var(--text-primary) !important;
        }}
        
        /* Ensure selected value is visible */
        [data-baseweb="select"] > div > div {{
            color: var(--text-primary) !important;
        }}
        
        [data-baseweb="select"] > div > div > div {{
            color: var(--text-primary) !important;
        }}
        
        /* Select value text */
        [data-baseweb="select"] [role="combobox"] {{
            color: var(--text-primary) !important;
        }}
        
        [data-baseweb="select"] [role="combobox"] > div {{
            color: var(--text-primary) !important;
        }}
        
        [data-baseweb="menu"] {{
            background: var(--bg-card) !important;
            border: 1px solid var(--border) !important;
        }}
        
        [data-baseweb="menu"] li {{
            color: var(--text-primary) !important;
        }}
        
        [data-baseweb="menu"] li:hover {{
            background: var(--accent) !important;
            color: var(--bg-primary) !important;
        }}
        
        /* Mobile-specific input fixes - AGGRESSIVE with fallbacks */
        @media (max-width: 768px) {{
            /* SELECTBOXES - All possible selectors with explicit fallbacks */
            .stSelectbox,
            .stSelectbox *,
            .stSelectbox > div,
            .stSelectbox > div > div,
            .stSelectbox > div > div > div {{
                color: var(--text-primary) !important;
            }}
            
            [data-baseweb="select"],
            [data-baseweb="select"] *,
            [data-baseweb="select"] > div,
            [data-baseweb="select"] > div > div,
            [data-baseweb="select"] > div > div > div,
            [data-baseweb="select"] > div > div > div > div {{
                color: var(--text-primary) !important;
            }}
            
            [data-baseweb="select"] input,
            [data-baseweb="select"] input[type="text"],
            [data-baseweb="select"] input[type="search"] {{
                color: var(--text-primary) !important;
                -webkit-text-fill-color: var(--text-primary) !important;
                background: transparent !important;
            }}
            
            [data-baseweb="select"] [role="combobox"],
            [data-baseweb="select"] [role="combobox"] *,
            [data-baseweb="select"] [role="combobox"] > div,
            [data-baseweb="select"] [role="combobox"] > div > div {{
                color: var(--text-primary) !important;
            }}
            
            [data-baseweb="select"] span,
            [data-baseweb="select"] span *,
            [data-baseweb="select"] div span {{
                color: var(--text-primary) !important;
            }}
            
            /* NUMBER INPUTS */
            .stNumberInput,
            .stNumberInput *,
            .stNumberInput input,
            .stNumberInput input[type="number"] {{
                color: var(--text-primary) !important;
                -webkit-text-fill-color: var(--text-primary) !important;
            }}
            
            [data-baseweb="input"],
            [data-baseweb="input"] *,
            [data-baseweb="input"] input,
            [data-baseweb="input"] input[type="number"] {{
                color: var(--text-primary) !important;
                -webkit-text-fill-color: var(--text-primary) !important;
            }}
            
            /* SLIDER LABELS */
            .stSlider,
            .stSlider label,
            .stSlider span,
            .stSlider * {{
                color: var(--text-primary) !important;
            }}
            
            /* Force visibility */
            .stSelectbox,
            .stNumberInput,
            .stSlider {{
                opacity: 1 !important;
                visibility: visible !important;
            }}
            
            /* Override black text that might be invisible on dark backgrounds */
            .stSelectbox [style*="color: rgb(0, 0, 0)"],
            .stSelectbox [style*="color:rgba(0,0,0"],
            .stNumberInput [style*="color: rgb(0, 0, 0)"],
            .stNumberInput [style*="color:rgba(0,0,0"] {{
                color: var(--text-primary) !important;
            }}
        }}
        
        /* ===== BUTTONS ===== */
        .stButton > button {{
            background: var(--accent) !important;
            color: var(--bg-primary) !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 0.875rem 2rem !important;
            font-size: 1rem !important;
            font-weight: 700 !important;
            transition: all 0.2s ease !important;
            width: 100%;
        }}
        
        .stButton > button:hover {{
            background: var(--accent-hover) !important;
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }}
        
        /* ===== SETTINGS ROW ===== */
        .settings-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin: 1rem 0;
        }}
        
        .setting-item {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 0.75rem 1rem;
        }}
        
        .setting-label {{
            color: var(--text-secondary);
            font-size: 0.7rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 0.25rem;
        }}
        
        /* ===== STATS GRID ===== */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1rem;
            margin: 1.5rem 0;
        }}
        
        /* Small Mobile */
        @media (max-width: 480px) {{
            .stats-grid {{
                grid-template-columns: 1fr;
                gap: 0.75rem;
            }}
            .stat-card {{
                padding: 1rem;
            }}
        }}
        
        /* Mobile */
        @media (max-width: 768px) {{
            .stats-grid {{
                grid-template-columns: repeat(2, 1fr);
                gap: 0.875rem;
            }}
        }}
        
        /* Tablet */
        @media (min-width: 768px) and (max-width: 1024px) {{
            .stats-grid {{
                grid-template-columns: repeat(4, 1fr);
                gap: 0.875rem;
            }}
        }}
        
        .stat-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.25rem;
            text-align: center;
            transition: all 0.2s ease;
        }}
        
        .stat-card:hover {{
            border-color: var(--accent);
            transform: translateY(-3px);
        }}
        
        .stat-value {{
            color: var(--accent);
            font-size: clamp(1.5rem, 4vw, 2rem);
            font-weight: 800;
            line-height: 1;
        }}
        
        .stat-label {{
            color: var(--text-muted);
            font-size: 0.7rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-top: 0.5rem;
        }}
        
        /* ===== ROUTE DISPLAY ===== */
        .route-card {{
            background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-secondary) 100%);
            border: 2px solid var(--accent);
            border-radius: 16px;
            padding: 1.5rem;
            margin: 1rem 0;
        }}
        
        .route-label {{
            color: var(--accent);
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 0.75rem;
        }}
        
        .route-path {{
            color: var(--text-primary);
            font-size: clamp(1rem, 2.5vw, 1.25rem);
            font-weight: 500;
            line-height: 1.8;
            word-wrap: break-word;
        }}
        
        .route-arrow {{
            color: var(--accent);
            margin: 0 0.5rem;
        }}
        
        /* ===== STOPS BADGES ===== */
        .stops-container {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            align-items: center;
            margin: 1rem 0;
        }}
        
        .stop-badge {{
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            white-space: nowrap;
        }}
        
        .stop-start {{
            background: var(--success);
            color: var(--bg-primary);
        }}
        
        .stop-mid {{
            background: var(--info);
            color: white;
        }}
        
        .stop-end {{
            background: var(--error);
            color: white;
        }}
        
        .stop-arrow {{
            color: var(--text-muted);
            font-size: 1.25rem;
        }}
        
        /* ===== NAV STEPS ===== */
        .nav-step {{
            background: var(--bg-card);
            border-left: 4px solid var(--accent);
            border-radius: 0 12px 12px 0;
            padding: 1rem 1.25rem;
            margin: 0.75rem 0;
            display: flex;
            align-items: center;
            gap: 1rem;
        }}
        
        /* Small Mobile */
        @media (max-width: 480px) {{
            .nav-step {{
                padding: 0.75rem;
                gap: 0.5rem;
                flex-direction: column;
                align-items: flex-start;
            }}
            .nav-number {{
                min-width: 28px;
                height: 28px;
                font-size: 0.75rem;
            }}
            .nav-cities {{
                font-size: 0.9rem;
            }}
            .nav-meta {{
                font-size: 0.75rem;
            }}
        }}
        
        /* Mobile */
        @media (max-width: 768px) {{
            .nav-step {{
                padding: 0.875rem 1rem;
                gap: 0.75rem;
            }}
        }}
        
        .nav-number {{
            background: var(--accent);
            color: var(--bg-primary);
            min-width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 0.875rem;
        }}
        
        .nav-content {{
            flex: 1;
        }}
        
        .nav-cities {{
            color: var(--text-primary);
            font-weight: 600;
            font-size: 1rem;
        }}
        
        .nav-meta {{
            color: var(--accent);
            font-size: 0.875rem;
            margin-top: 0.25rem;
        }}
        
        /* ===== PLACE CARDS ===== */
        .place-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1rem;
            margin: 0.5rem 0;
            display: flex;
            align-items: center;
            gap: 1rem;
            transition: all 0.2s ease;
        }}
        
        .place-card:hover {{
            border-color: var(--accent);
            background: var(--bg-card-hover);
        }}
        
        .place-icon {{
            font-size: 1.75rem;
            min-width: 45px;
            text-align: center;
        }}
        
        .place-info {{
            flex: 1;
            min-width: 0;
        }}
        
        .place-name {{
            color: var(--text-primary);
            font-weight: 600;
            font-size: 1rem;
            margin: 0;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}
        
        .place-detail {{
            color: var(--text-muted);
            font-size: 0.8rem;
            margin: 0.25rem 0;
        }}
        
        .place-rating {{
            color: var(--warning);
            font-size: 0.875rem;
        }}
        
        .place-distance {{
            color: var(--accent);
            font-weight: 700;
            font-size: 0.875rem;
            white-space: nowrap;
        }}
        
        /* ===== MAP CONTAINER ===== */
        .map-container {{
            border-radius: 16px;
            overflow: hidden;
            border: 2px solid var(--accent);
        }}
        
        /* ===== FUEL BREAKDOWN ===== */
        .fuel-breakdown {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1rem;
            margin: 1rem 0;
        }}
        
        .fuel-title {{
            color: var(--accent);
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 0.5rem;
        }}
        
        .fuel-details {{
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            color: var(--text-secondary);
            font-size: 0.85rem;
        }}
        
        .fuel-total {{
            color: var(--accent);
            font-weight: 700;
        }}
        
        /* ===== TABS ===== */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 0.25rem;
            background: var(--bg-secondary);
            border-radius: 12px;
            padding: 0.25rem;
            flex-wrap: wrap;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            background: transparent;
            border-radius: 10px;
            color: var(--text-secondary);
            font-weight: 600;
            padding: 0.625rem 1rem;
            font-size: 0.8rem;
        }}
        
        .stTabs [aria-selected="true"] {{
            background: var(--accent) !important;
            color: var(--bg-primary) !important;
        }}
        
        /* Small Mobile */
        @media (max-width: 480px) {{
            .stTabs [data-baseweb="tab"] {{
                padding: 0.4rem 0.5rem;
                font-size: 0.65rem;
            }}
            .stTabs [data-baseweb="tab-list"] {{
                gap: 0.15rem;
                padding: 0.15rem;
            }}
        }}
        
        /* Mobile */
        @media (max-width: 768px) {{
            .stTabs [data-baseweb="tab"] {{
                padding: 0.5rem 0.75rem;
                font-size: 0.7rem;
            }}
        }}
        
        /* Tablet */
        @media (min-width: 768px) and (max-width: 1024px) {{
            .stTabs [data-baseweb="tab"] {{
                padding: 0.6rem 0.9rem;
                font-size: 0.75rem;
            }}
        }}
        
        /* ===== SUCCESS/ERROR BANNERS ===== */
        .success-banner {{
            background: var(--bg-card);
            border: 2px solid var(--success);
            border-radius: 12px;
            padding: 1rem;
            text-align: center;
            margin: 1rem 0;
        }}
        
        .success-text {{
            color: var(--success);
            font-weight: 600;
        }}
        
        .error-banner {{
            background: var(--bg-card);
            border: 2px solid var(--error);
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
        }}
        
        .error-title {{
            color: var(--error);
            font-size: 1.25rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }}
        
        .error-text {{
            color: var(--text-secondary);
        }}
        
        /* ===== SIDEBAR ===== */
        [data-testid="stSidebar"] {{
            background: var(--bg-secondary);
        }}
        
        [data-testid="stSidebar"] .stMarkdown {{
            color: var(--text-primary);
        }}
        
        .sidebar-section {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1rem;
            margin: 0.5rem 0;
        }}
        
        .sidebar-title {{
            color: var(--accent);
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 0.75rem;
        }}
        
        /* ===== SLIDERS ===== */
        .stSlider > div > div > div {{
            background: var(--accent) !important;
        }}
        
        /* ===== THEME TOGGLE ===== */
        .theme-toggle {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 0.75rem;
            margin-bottom: 1rem;
        }}
        
        .theme-label {{
            color: var(--text-secondary);
            font-size: 0.7rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 0.5rem;
        }}
        
        /* ===== LIVE BADGE ===== */
        .live-badge {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: var(--bg-card);
            border: 1px solid var(--success);
            border-radius: 20px;
            padding: 0.375rem 0.875rem;
            margin-bottom: 1rem;
        }}
        
        .live-dot {{
            width: 8px;
            height: 8px;
            background: var(--success);
            border-radius: 50%;
            animation: pulse 1.5s infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.4; }}
        }}
        
        .live-text {{
            color: var(--success);
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        /* ===== WEATHER WIDGETS ===== */
        .weather-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1rem;
            margin: 1.5rem 0;
        }}
        
        .weather-card {{
            background: var(--info);
            border-radius: 12px;
            padding: 1rem;
            text-align: center;
            color: white;
        }}
        
        .weather-icon {{
            font-size: 2rem;
        }}
        
        .weather-temp {{
            font-size: 1.5rem;
            font-weight: 800;
        }}
        
        .weather-city {{
            font-size: 0.8rem;
            opacity: 0.9;
        }}
        
        /* ===== FOOTER ===== */
        .footer {{
            text-align: center;
            padding: 2rem 1rem;
            color: var(--text-muted);
            font-size: 0.875rem;
            border-top: 1px solid var(--border);
            margin-top: 2rem;
        }}
        
        /* ===== DRIVE MODE ===== */
        .drive-mode {{
            background: #000;
            border-radius: 20px;
            padding: 1.5rem;
            margin: 1rem 0;
        }}
        
        .drive-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid #222;
        }}
        
        .drive-status {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        .drive-live {{
            width: 12px;
            height: 12px;
            background: #22c55e;
            border-radius: 50%;
            animation: pulse 1.5s infinite;
        }}
        
        .drive-label {{
            color: #22c55e;
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .drive-current {{
            background: linear-gradient(135deg, #1a1a2e 0%, #0a0a0f 100%);
            border: 2px solid #22c55e;
            border-radius: 16px;
            padding: 1.5rem;
            text-align: center;
            margin-bottom: 1rem;
        }}
        
        .drive-direction {{
            color: #22c55e;
            font-size: 3rem;
            margin-bottom: 0.5rem;
        }}
        
        .drive-instruction {{
            color: #fff;
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }}
        
        .drive-distance {{
            color: #22c55e;
            font-size: 2.5rem;
            font-weight: 800;
        }}
        
        .drive-unit {{
            color: #666;
            font-size: 1rem;
            margin-left: 0.25rem;
        }}
        
        .drive-next {{
            background: #111;
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 1rem;
        }}
        
        .drive-next-label {{
            color: #666;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 0.5rem;
        }}
        
        .drive-next-text {{
            color: #fff;
            font-size: 1rem;
            font-weight: 500;
        }}
        
        .drive-progress {{
            background: #111;
            border-radius: 12px;
            padding: 1rem;
        }}
        
        .drive-progress-bar {{
            background: #222;
            border-radius: 8px;
            height: 8px;
            overflow: hidden;
            margin-bottom: 0.75rem;
        }}
        
        .drive-progress-fill {{
            background: linear-gradient(90deg, #22c55e, #4ade80);
            height: 100%;
            border-radius: 8px;
            transition: width 0.5s ease;
        }}
        
        .drive-stats {{
            display: flex;
            justify-content: space-between;
            color: #888;
            font-size: 0.85rem;
        }}
        
        .drive-eta {{
            color: #22c55e;
            font-weight: 600;
        }}
        
        /* ===== SAVE OFFLINE ===== */
        .offline-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1rem;
            margin: 0.5rem 0;
        }}
        
        .offline-title {{
            color: var(--text-primary);
            font-weight: 600;
            margin-bottom: 0.5rem;
        }}
        
        .offline-desc {{
            color: var(--text-muted);
            font-size: 0.85rem;
            margin-bottom: 0.75rem;
        }}
        
        .download-btn {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: var(--accent);
            color: var(--bg-primary);
            padding: 0.5rem 1rem;
            border-radius: 8px;
            font-weight: 600;
            font-size: 0.85rem;
            text-decoration: none;
            transition: all 0.2s ease;
        }}
        
        .download-btn:hover {{
            background: var(--accent-hover);
            transform: translateY(-1px);
        }}
        
        /* ===== ACCESSIBILITY ===== */
        @media (prefers-reduced-motion: reduce) {{
            *, *::before, *::after {{
                animation-duration: 0.01ms !important;
                transition-duration: 0.01ms !important;
            }}
        }}
        
        /* Focus indicators for keyboard navigation */
        *:focus-visible {{
            outline: 2px solid var(--accent);
            outline-offset: 2px;
        }}
        
        /* ===== RESPONSIVE UTILITIES ===== */
        
        /* Small Mobile - General adjustments */
        @media (max-width: 480px) {{
            .app-header {{
                margin-bottom: 1rem;
            }}
            .route-card {{
                padding: 1rem;
            }}
            .fuel-breakdown {{
                padding: 0.75rem;
            }}
            .fuel-details {{
                flex-direction: column;
                gap: 0.5rem;
            }}
            .place-card {{
                padding: 0.75rem;
                gap: 0.75rem;
            }}
            .place-icon {{
                font-size: 1.5rem;
                min-width: 40px;
            }}
            .stops-container {{
                flex-direction: column;
                align-items: flex-start;
            }}
            .stop-arrow {{
                transform: rotate(90deg);
                margin: 0.25rem 0;
            }}
            .button-container {{
                flex-direction: column;
            }}
        }}
        
        /* Mobile - Column adjustments */
        @media (max-width: 768px) {{
            /* Settings columns stack on mobile */
            .settings-row {{
                flex-direction: column;
            }}
            /* Drive mode adjustments */
            .drive-header {{
                flex-direction: column;
                gap: 0.75rem;
            }}
            .col-info1, .col-info2, .col-info3 {{
                margin-bottom: 0.5rem;
            }}
            /* Ensure Streamlit columns stack properly */
            [data-testid="column"] {{
                width: 100% !important;
                flex: 1 1 100% !important;
            }}
        }}
        
        /* Small Mobile - Force single column */
        @media (max-width: 480px) {{
            [data-testid="column"] {{
                width: 100% !important;
                flex: 1 1 100% !important;
                margin-bottom: 0.5rem;
            }}
            /* Stack all multi-column layouts */
            .stColumns {{
                flex-direction: column !important;
            }}
        }}
        
        /* Tablet - Optimize spacing */
        @media (min-width: 768px) and (max-width: 1024px) {{
            .stats-grid {{
                gap: 1rem;
            }}
            .route-card {{
                padding: 1.25rem;
            }}
        }}
        
        /* Desktop - Enhanced spacing */
        @media (min-width: 1024px) {{
            .stats-grid {{
                gap: 1.25rem;
            }}
            .route-card {{
                padding: 1.75rem;
            }}
        }}
        
        /* Large Desktop - Maximum width constraints */
        @media (min-width: 1440px) {{
            .app-header {{
                padding: 2.5rem 1rem;
            }}
            .route-card {{
                padding: 2rem;
            }}
        }}
        
        /* Landscape orientation adjustments */
        @media (max-height: 600px) and (orientation: landscape) {{
            .app-header {{
                padding: 1rem;
                margin-bottom: 0.75rem;
            }}
            .app-logo {{
                font-size: 2rem;
            }}
        }}
        
        /* ===== MOBILE APP-SPECIFIC UI ===== */
        
        /* Sidebar on mobile - accessible via toggle */
        @media (max-width: 768px) {{
            /* Show sidebar toggle button */
            [data-testid="stSidebarCollapseButton"] {{
                display: block !important;
                position: fixed !important;
                top: 1rem !important;
                right: 1rem !important;
                z-index: 1001 !important;
                background: var(--bg-card) !important;
                border: 2px solid var(--border) !important;
                border-radius: 12px !important;
                padding: 0.75rem !important;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important;
                min-width: 48px !important;
                min-height: 48px !important;
            }}
            
            /* Sidebar when open */
            [data-testid="stSidebar"][aria-expanded="true"] {{
                display: block !important;
                position: fixed !important;
                top: 0 !important;
                left: 0 !important;
                height: 100vh !important;
                z-index: 1000 !important;
                background: var(--bg-primary) !important;
                box-shadow: 2px 0 20px rgba(0,0,0,0.5) !important;
                overflow-y: auto !important;
                -webkit-overflow-scrolling: touch !important;
            }}
            
            /* Sidebar when closed */
            [data-testid="stSidebar"][aria-expanded="false"] {{
                display: none !important;
            }}
            
            .main .block-container {{
                padding-left: 1rem !important;
                padding-right: 1rem !important;
            }}
        }}
        
        /* Mobile Header - Compact */
        @media (max-width: 768px) {{
            .app-header {{
                padding: 1rem 0.5rem !important;
                margin-bottom: 1rem !important;
                position: sticky;
                top: 0;
                z-index: 100;
                background: var(--bg-primary);
                border-bottom: 1px solid var(--border);
                backdrop-filter: blur(10px);
            }}
            .app-logo {{
                font-size: 1.5rem !important;
                margin-bottom: 0.25rem !important;
            }}
            .app-title {{
                font-size: 1.5rem !important;
                margin: 0 !important;
            }}
            .app-subtitle {{
                font-size: 0.75rem !important;
                margin-top: 0.25rem !important;
            }}
        }}
        
        /* Full-screen map on mobile */
        @media (max-width: 768px) {{
            .map-container {{
                margin: 0 -1rem !important;
                border-radius: 0 !important;
            }}
            .map-container iframe {{
                height: 60vh !important;
                min-height: 400px !important;
            }}
        }}
        
        /* Mobile Tabs - Horizontal Scrollable */
        @media (max-width: 768px) {{
            [data-baseweb="tabs"] {{
                overflow-x: auto !important;
                -webkit-overflow-scrolling: touch;
                scrollbar-width: none;
                -ms-overflow-style: none;
                position: sticky;
                top: 0;
                z-index: 50;
                background: var(--bg-primary);
                padding: 0.5rem 0;
                margin: 0 -1rem;
                padding-left: 1rem;
                padding-right: 1rem;
            }}
            [data-baseweb="tabs"]::-webkit-scrollbar {{
                display: none;
            }}
            [data-baseweb="tab-list"] {{
                flex-wrap: nowrap !important;
                gap: 0.5rem !important;
            }}
            [data-baseweb="tab"] {{
                min-width: fit-content !important;
                padding: 0.75rem 1rem !important;
                font-size: 0.85rem !important;
                white-space: nowrap !important;
                border-radius: 12px !important;
            }}
            [data-baseweb="tab"][aria-selected="true"] {{
                background: var(--accent) !important;
                color: var(--bg-primary) !important;
            }}
        }}
        
        /* Larger Touch Targets on Mobile */
        @media (max-width: 768px) {{
            .stButton > button {{
                min-height: 48px !important;
                padding: 1rem 1.5rem !important;
                font-size: 1rem !important;
            }}
            .stSelectbox > div > div {{
                min-height: 48px !important;
                padding: 0.75rem 1rem !important;
            }}
            [data-baseweb="select"] {{
                min-height: 48px !important;
            }}
            .stSlider {{
                padding: 1rem 0 !important;
            }}
            .stNumberInput > div {{
                min-height: 48px !important;
            }}
            
            /* Ensure all text in selectboxes is visible */
            .stSelectbox label {{
                color: var(--text-secondary) !important;
            }}
            
            /* Select value display - most aggressive fix */
            .stSelectbox [data-baseweb="select"] {{
                color: var(--text-primary) !important;
            }}
            
            /* Force text color in all select children */
            .stSelectbox [data-baseweb="select"] * {{
                color: var(--text-primary) !important;
            }}
            
            /* The actual displayed value */
            .stSelectbox [data-baseweb="select"] > div {{
                color: var(--text-primary) !important;
            }}
            
            .stSelectbox [data-baseweb="select"] > div > div {{
                color: var(--text-primary) !important;
            }}
            
            .stSelectbox [data-baseweb="select"] > div > div > div {{
                color: var(--text-primary) !important;
            }}
            
            /* Input text visibility */
            .stSelectbox input {{
                color: var(--text-primary) !important;
                -webkit-text-fill-color: var(--text-primary) !important;
            }}
            
            /* Selected value text */
            .stSelectbox [role="combobox"] {{
                color: var(--text-primary) !important;
            }}
            
            .stSelectbox [role="combobox"] * {{
                color: var(--text-primary) !important;
            }}
            
            /* All spans in select */
            .stSelectbox [data-baseweb="select"] span {{
                color: var(--text-primary) !important;
            }}
            
            /* Number input text */
            .stNumberInput input {{
                color: var(--text-primary) !important;
                -webkit-text-fill-color: var(--text-primary) !important;
            }}
            
            /* Override any inline styles that might hide text */
            .stSelectbox [style*="color"] {{
                color: var(--text-primary) !important;
            }}
        }}
        
        /* Bottom Navigation Bar (Mobile Only) */
        @media (max-width: 768px) {{
            .mobile-bottom-nav {{
                position: fixed;
                bottom: 0;
                left: 0;
                right: 0;
                background: var(--bg-card);
                border-top: 2px solid var(--border);
                padding: 0.5rem 0;
                z-index: 1000;
                display: flex;
                justify-content: space-around;
                align-items: center;
                box-shadow: 0 -4px 20px rgba(0,0,0,0.3);
                backdrop-filter: blur(10px);
            }}
            .nav-item {{
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 0.25rem;
                padding: 0.5rem 1rem;
                color: var(--text-muted);
                text-decoration: none;
                font-size: 0.7rem;
                transition: all 0.2s ease;
                min-width: 60px;
            }}
            .nav-item:hover {{
                color: var(--accent);
                transform: translateY(-2px);
            }}
            .nav-item.active {{
                color: var(--accent);
            }}
            .nav-icon {{
                font-size: 1.5rem;
            }}
            /* Add padding to body to prevent content from being hidden behind bottom nav */
            .main .block-container {{
                padding-bottom: 80px !important;
            }}
        }}
        
        /* Hide bottom nav on desktop */
        @media (min-width: 769px) {{
            .mobile-bottom-nav {{
                display: none !important;
            }}
        }}
        
        /* Mobile Stats Grid - Single Column */
        @media (max-width: 480px) {{
            .stats-grid {{
                grid-template-columns: 1fr !important;
                gap: 0.75rem !important;
            }}
            .stat-card {{
                padding: 1rem !important;
            }}
        }}
        
        /* Mobile Input Section - Full Width Cards */
        @media (max-width: 768px) {{
            .input-card {{
                margin-bottom: 0.75rem !important;
            }}
            .stSelectbox {{
                margin-bottom: 0.5rem !important;
            }}
        }}
        
        /* Mobile Drive Mode - Full Screen Feel */
        @media (max-width: 768px) {{
            .drive-mode {{
                margin: 0 -1rem !important;
                border-radius: 0 !important;
                padding: 1rem !important;
            }}
            .drive-current {{
                padding: 1.25rem !important;
            }}
            .drive-direction {{
                font-size: 2.5rem !important;
            }}
            .drive-instruction {{
                font-size: 1.25rem !important;
            }}
            .drive-distance {{
                font-size: 2rem !important;
            }}
        }}
        
        /* Mobile Route Card - Better Spacing */
        @media (max-width: 768px) {{
            .route-card {{
                padding: 1rem !important;
                margin: 0.75rem 0 !important;
            }}
            .route-path {{
                font-size: 0.95rem !important;
                line-height: 1.6 !important;
            }}
        }}
        
        /* Mobile Navigation Steps - Vertical Stack */
        @media (max-width: 768px) {{
            .nav-step {{
                flex-direction: column !important;
                align-items: flex-start !important;
                padding: 1rem !important;
            }}
            .nav-number {{
                margin-bottom: 0.5rem !important;
            }}
        }}
        
        /* Mobile Place Cards - Compact */
        @media (max-width: 768px) {{
            .place-card {{
                padding: 0.875rem !important;
                gap: 0.75rem !important;
            }}
            .place-icon {{
                font-size: 1.5rem !important;
                min-width: 35px !important;
            }}
            .place-name {{
                font-size: 0.95rem !important;
            }}
        }}
        
        /* Mobile Settings - Stack Vertically */
        @media (max-width: 768px) {{
            .settings-grid {{
                grid-template-columns: 1fr !important;
                gap: 0.75rem !important;
            }}
            .setting-item {{
                padding: 1rem !important;
            }}
        }}
        
        /* Mobile Fuel Breakdown - Stack */
        @media (max-width: 768px) {{
            .fuel-breakdown {{
                padding: 1rem !important;
            }}
            .fuel-details {{
                flex-direction: column !important;
                gap: 0.5rem !important;
                align-items: flex-start !important;
            }}
        }}
        
        /* Mobile Stops - Vertical Layout */
        @media (max-width: 768px) {{
            .stops-container {{
                flex-direction: column !important;
                align-items: flex-start !important;
                gap: 0.5rem !important;
            }}
            .stop-arrow {{
                transform: rotate(90deg) !important;
                margin: 0.25rem 0 !important;
            }}
        }}
        
        /* Mobile Buttons - Full Width Stack */
        @media (max-width: 768px) {{
            .button-container {{
                flex-direction: column !important;
                gap: 0.75rem !important;
            }}
            .button-container button {{
                width: 100% !important;
            }}
        }}
        
        /* Mobile Footer - Compact */
        @media (max-width: 768px) {{
            .footer {{
                padding: 1.5rem 0.5rem !important;
                font-size: 0.8rem !important;
                margin-top: 1rem !important;
            }}
        }}
        
        /* Safe Area for Mobile Notches */
        @supports (padding: max(0px)) {{
            @media (max-width: 768px) {{
                .mobile-bottom-nav {{
                    padding-bottom: max(0.5rem, env(safe-area-inset-bottom));
                }}
                .app-header {{
                    padding-top: max(1rem, env(safe-area-inset-top));
                }}
            }}
        }}
        
        /* ===== MOBILE FEATURE COMPATIBILITY ===== */
        
        /* Ensure all interactive elements are touch-friendly */
        @media (max-width: 768px) {{
            /* Map interactivity on mobile */
            .map-container iframe,
            .map-container .folium-map {{
                touch-action: pan-x pan-y pinch-zoom !important;
                -webkit-overflow-scrolling: touch !important;
            }}
            
            /* Download links - ensure they work on mobile */
            .download-btn {{
                display: inline-block !important;
                min-height: 48px !important;
                padding: 0.75rem 1.5rem !important;
                font-size: 1rem !important;
                -webkit-tap-highlight-color: var(--accent) !important;
                touch-action: manipulation !important;
            }}
            
            /* Expanders - ensure they're touch-friendly */
            [data-baseweb="accordion"] {{
                touch-action: manipulation !important;
            }}
            
            [data-baseweb="accordion"] button {{
                min-height: 48px !important;
                padding: 1rem !important;
            }}
            
            /* Radio buttons - ensure they work on mobile */
            [data-baseweb="radio"] label {{
                min-height: 44px !important;
                padding: 0.75rem !important;
                touch-action: manipulation !important;
            }}
            
            /* Code blocks - ensure they're scrollable */
            .stCodeBlock,
            .stCodeBlock pre {{
                overflow-x: auto !important;
                -webkit-overflow-scrolling: touch !important;
                max-width: 100% !important;
            }}
            
            /* JSON viewer - ensure it's scrollable */
            [data-testid="stJson"] {{
                overflow-x: auto !important;
                -webkit-overflow-scrolling: touch !important;
                max-width: 100% !important;
            }}
            
            /* Progress bar - ensure it's visible */
            .stProgress > div > div {{
                min-height: 8px !important;
            }}
            
            /* Warning/Error messages - ensure they're readable */
            .stAlert {{
                padding: 1rem !important;
                font-size: 0.95rem !important;
                margin: 0.75rem 0 !important;
            }}
            
            /* Balloons animation - ensure it doesn't break layout */
            .stBalloonsContainer {{
                position: fixed !important;
                z-index: 9999 !important;
                pointer-events: none !important;
            }}
            
            /* Ensure all buttons have proper touch targets */
            button,
            [role="button"],
            .stButton > button,
            [data-baseweb="button"] {{
                min-height: 44px !important;
                min-width: 44px !important;
                touch-action: manipulation !important;
                -webkit-tap-highlight-color: rgba(34, 197, 94, 0.3) !important;
            }}
            
            /* Slider - ensure it's touch-friendly */
            [data-baseweb="slider"] {{
                touch-action: pan-x !important;
                min-height: 48px !important;
                padding: 1rem 0 !important;
            }}
            
            [data-baseweb="slider"] [role="slider"] {{
                min-width: 44px !important;
                min-height: 44px !important;
            }}
            
            /* Selectbox dropdown - ensure it's scrollable */
            [data-baseweb="menu"] {{
                max-height: 50vh !important;
                overflow-y: auto !important;
                -webkit-overflow-scrolling: touch !important;
            }}
            
            /* Number input - ensure it's usable */
            [data-baseweb="input"] input[type="number"] {{
                font-size: 16px !important; /* Prevents zoom on iOS */
                min-height: 48px !important;
            }}
            
            /* Text input - prevent zoom on focus (iOS) */
            input[type="text"],
            input[type="search"],
            input[type="number"] {{
                font-size: 16px !important;
            }}
            
            /* Ensure sidebar toggle works */
            [data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] {{
                min-width: 44px !important;
                min-height: 44px !important;
                touch-action: manipulation !important;
            }}
            
            /* Drive mode controls - ensure they're touch-friendly */
            .drive-mode button,
            #drive button {{
                min-height: 48px !important;
                font-size: 1rem !important;
                padding: 0.75rem 1rem !important;
                touch-action: manipulation !important;
            }}
            
            /* Drive mode info cards - ensure they stack properly */
            #drive [data-testid="column"] {{
                width: 100% !important;
                margin-bottom: 0.75rem !important;
            }}
            
            /* Drive mode navigation header - ensure it's readable */
            #drive > div > div:first-child {{
                padding: 1rem !important;
                margin-bottom: 1rem !important;
            }}
            
            /* Ensure all tabs are accessible */
            [data-baseweb="tab"] {{
                min-height: 44px !important;
                padding: 0.75rem 1rem !important;
                touch-action: manipulation !important;
            }}
            
            /* Ensure expanders work on mobile */
            [data-baseweb="accordion"] {{
                margin: 0.5rem 0 !important;
            }}
            
            [data-baseweb="accordion"] > div {{
                border-radius: 12px !important;
                overflow: hidden !important;
            }}
            
            /* Code blocks in expanders */
            .stCodeBlock {{
                font-size: 0.85rem !important;
                padding: 1rem !important;
            }}
            
            /* JSON viewer in expanders */
            [data-testid="stJson"] {{
                font-size: 0.85rem !important;
                padding: 0.5rem !important;
            }}
            
            /* Ensure warning/error messages are visible */
            [data-baseweb="alert"] {{
                padding: 1rem !important;
                margin: 0.75rem 0 !important;
                border-radius: 12px !important;
            }}
            
            /* Progress indicator */
            [data-testid="stProgressBar"] {{
                min-height: 8px !important;
            }}
            
            /* Ensure metric displays are readable */
            [data-testid="stMetricValue"] {{
                font-size: 1.5rem !important;
            }}
            
            [data-testid="stMetricLabel"] {{
                font-size: 0.9rem !important;
            }}
            
            /* Caption text */
            .stCaption {{
                font-size: 0.85rem !important;
                line-height: 1.5 !important;
            }}
            
            /* Ensure horizontal rules are visible */
            hr {{
                margin: 1rem 0 !important;
                border-color: var(--border) !important;
            }}
            
            /* Ensure all text in cards is readable */
            .card p,
            .card span,
            .card div {{
                font-size: clamp(0.875rem, 2.5vw, 1rem) !important;
                line-height: 1.6 !important;
            }}
            
            /* Nearby places cards - ensure they're tappable */
            .place-card {{
                cursor: pointer !important;
                -webkit-tap-highlight-color: rgba(34, 197, 94, 0.2) !important;
                touch-action: manipulation !important;
            }}
            
            /* Route path - ensure long names wrap */
            .route-path {{
                word-break: break-word !important;
                overflow-wrap: anywhere !important;
            }}
            
            /* Stop badges - ensure they're readable */
            .stop-badge {{
                font-size: 0.75rem !important;
                padding: 0.5rem 0.75rem !important;
                min-height: 32px !important;
                display: inline-flex !important;
                align-items: center !important;
            }}
            
            /* Navigation steps - ensure they're readable */
            .nav-step {{
                margin: 0.5rem 0 !important;
                padding: 1rem !important;
            }}
            
            /* Fuel breakdown - ensure it's readable */
            .fuel-breakdown {{
                padding: 1rem !important;
                margin: 1rem 0 !important;
            }}
            
            .fuel-details span {{
                display: block !important;
                margin: 0.5rem 0 !important;
            }}
            
            /* Stats grid - ensure cards are readable */
            .stat-card {{
                padding: 1rem !important;
                min-height: 100px !important;
            }}
            
            /* Ensure all text is readable */
            p, span, div, label {{
                -webkit-text-size-adjust: 100% !important;
                text-size-adjust: 100% !important;
            }}
            
            /* Prevent horizontal scroll */
            body, html {{
                overflow-x: hidden !important;
                max-width: 100vw !important;
            }}
            
            .main .block-container {{
                max-width: 100% !important;
                padding-left: 1rem !important;
                padding-right: 1rem !important;
            }}
        }}
        
        /* Small mobile specific fixes */
        @media (max-width: 480px) {{
            /* Even more compact on very small screens */
            .app-header {{
                padding: 0.75rem 0.5rem !important;
            }}
            
            .app-title {{
                font-size: 1.25rem !important;
            }}
            
            .stat-card {{
                padding: 0.875rem !important;
            }}
            
            .stat-value {{
                font-size: 1.5rem !important;
            }}
            
            /* Drive mode - more compact */
            .drive-current {{
                padding: 1rem !important;
            }}
            
            .drive-direction {{
                font-size: 2rem !important;
            }}
            
            .drive-instruction {{
                font-size: 1rem !important;
            }}
            
            .drive-distance {{
                font-size: 1.75rem !important;
            }}
        }}
        
        /* Print styles */
        @media print {{
            .stSidebar, .stButton, .stTabs, .mobile-bottom-nav {{
                display: none !important;
            }}
            .main-container {{
                max-width: 100%;
                padding: 0;
            }}
        }}
    </style>
    """


# ==================== SAMPLE DATA ====================
def get_nearby_places(location, category):
    """Get nearby places based on location and category. Returns different places for different cities."""
    
    # Normalize location name for matching
    location_lower = location.lower()
    
    # Determine city/region from location
    city_key = "islamabad"  # default
    if "karachi" in location_lower or "dha" in location_lower:
        city_key = "karachi"
    elif "lahore" in location_lower:
        city_key = "lahore"
    elif "islamabad" in location_lower or "f-7" in location_lower or "f-6" in location_lower or "f-8" in location_lower:
        city_key = "islamabad"
    elif "rawalpindi" in location_lower:
        city_key = "rawalpindi"
    elif "peshawar" in location_lower:
        city_key = "peshawar"
    elif "quetta" in location_lower:
        city_key = "quetta"
    elif "multan" in location_lower:
        city_key = "multan"
    elif "faisalabad" in location_lower:
        city_key = "faisalabad"
    
    # Location-specific places database
    places_by_city = {
        "karachi": {
            "restaurants": [
                {"name": "Kolachi", "type": "Seafood", "rating": 4.6, "distance": "1.2 km", "price": "$$$"},
                {"name": "Café Zouk", "type": "Continental", "rating": 4.5, "distance": "0.8 km", "price": "$$"},
                {"name": "Burns Road Food Street", "type": "Pakistani", "rating": 4.7, "distance": "2.5 km", "price": "$"},
                {"name": "BBQ Tonight", "type": "BBQ", "rating": 4.4, "distance": "1.5 km", "price": "$$"},
                {"name": "Salt n Pepper", "type": "Pakistani", "rating": 4.3, "distance": "1.8 km", "price": "$$"},
            ],
            "hotels": [
                {"name": "Pearl Continental", "type": "5-Star", "rating": 4.8, "distance": "1.0 km", "price": "$$$"},
                {"name": "Marriott Hotel", "type": "5-Star", "rating": 4.7, "distance": "1.5 km", "price": "$$$"},
                {"name": "Avari Towers", "type": "5-Star", "rating": 4.6, "distance": "2.0 km", "price": "$$$"},
                {"name": "Ramada Hotel", "type": "4-Star", "rating": 4.4, "distance": "0.8 km", "price": "$$"},
            ],
            "cafes": [
                {"name": "Gloria Jean's", "type": "Coffee Shop", "rating": 4.4, "distance": "0.3 km", "price": "$$"},
                {"name": "Espresso", "type": "Café", "rating": 4.3, "distance": "0.7 km", "price": "$$"},
                {"name": "The Second Cup", "type": "Coffee Shop", "rating": 4.2, "distance": "1.0 km", "price": "$$"},
                {"name": "Butlers Chocolate Café", "type": "Café", "rating": 4.5, "distance": "0.9 km", "price": "$$"},
            ],
            "parks": [
                {"name": "Clifton Beach", "type": "Beach", "rating": 4.5, "distance": "3.5 km", "price": "Free"},
                {"name": "Baghn-e-Jinnah", "type": "Park", "rating": 4.3, "distance": "2.8 km", "price": "Free"},
                {"name": "Hill Park", "type": "Recreation", "rating": 4.4, "distance": "4.0 km", "price": "Free"},
            ],
        },
        "islamabad": {
            "restaurants": [
                {"name": "Monal Restaurant", "type": "Pakistani", "rating": 4.7, "distance": "1.2 km", "price": "$$$"},
                {"name": "Burning Brownie", "type": "Café & Desserts", "rating": 4.3, "distance": "0.5 km", "price": "$$"},
                {"name": "Howdy", "type": "American", "rating": 4.2, "distance": "1.5 km", "price": "$$"},
                {"name": "Kabul Restaurant", "type": "Afghan", "rating": 4.6, "distance": "1.8 km", "price": "$$"},
                {"name": "Chaaye Khana", "type": "Pakistani", "rating": 4.4, "distance": "0.9 km", "price": "$$"},
            ],
            "hotels": [
                {"name": "Serena Hotel", "type": "5-Star", "rating": 4.9, "distance": "1.2 km", "price": "$$$"},
                {"name": "Marriott Hotel", "type": "5-Star", "rating": 4.8, "distance": "1.5 km", "price": "$$$"},
                {"name": "Ramada Hotel", "type": "4-Star", "rating": 4.4, "distance": "0.8 km", "price": "$$"},
                {"name": "Hotel One", "type": "Business", "rating": 4.2, "distance": "2.0 km", "price": "$$"},
            ],
            "cafes": [
                {"name": "Gloria Jean's", "type": "Coffee Shop", "rating": 4.4, "distance": "0.3 km", "price": "$$"},
                {"name": "Espresso", "type": "Café", "rating": 4.3, "distance": "0.7 km", "price": "$$"},
                {"name": "The Second Cup", "type": "Coffee Shop", "rating": 4.2, "distance": "1.0 km", "price": "$$"},
                {"name": "Café Flo", "type": "French Café", "rating": 4.5, "distance": "1.2 km", "price": "$$"},
            ],
            "parks": [
                {"name": "Fatima Jinnah Park", "type": "National Park", "rating": 4.6, "distance": "2.5 km", "price": "Free"},
                {"name": "Lake View Park", "type": "Recreation", "rating": 4.4, "distance": "3.0 km", "price": "$"},
                {"name": "Daman-e-Koh", "type": "Viewpoint", "rating": 4.8, "distance": "5.0 km", "price": "Free"},
                {"name": "Shakarparian", "type": "Park", "rating": 4.5, "distance": "4.5 km", "price": "Free"},
            ],
        },
        "lahore": {
            "restaurants": [
                {"name": "Café Aylanto", "type": "Continental", "rating": 4.6, "distance": "1.1 km", "price": "$$$"},
                {"name": "Butt Karahi", "type": "Pakistani", "rating": 4.8, "distance": "2.0 km", "price": "$$"},
                {"name": "Cooco's Den", "type": "Pakistani", "rating": 4.5, "distance": "3.5 km", "price": "$$"},
                {"name": "Food Street", "type": "Pakistani", "rating": 4.7, "distance": "4.0 km", "price": "$$"},
                {"name": "Salt n Pepper", "type": "Pakistani", "rating": 4.4, "distance": "1.5 km", "price": "$$"},
            ],
            "hotels": [
                {"name": "Pearl Continental", "type": "5-Star", "rating": 4.8, "distance": "1.0 km", "price": "$$$"},
                {"name": "Nishat Hotel", "type": "5-Star", "rating": 4.7, "distance": "1.8 km", "price": "$$$"},
                {"name": "Avari Hotel", "type": "5-Star", "rating": 4.6, "distance": "2.2 km", "price": "$$$"},
                {"name": "Hotel One", "type": "Business", "rating": 4.2, "distance": "1.5 km", "price": "$$"},
            ],
            "cafes": [
                {"name": "Gloria Jean's", "type": "Coffee Shop", "rating": 4.4, "distance": "0.5 km", "price": "$$"},
                {"name": "Espresso", "type": "Café", "rating": 4.3, "distance": "0.8 km", "price": "$$"},
                {"name": "Café Zouk", "type": "Café", "rating": 4.5, "distance": "1.2 km", "price": "$$"},
                {"name": "Butlers Chocolate Café", "type": "Café", "rating": 4.4, "distance": "0.9 km", "price": "$$"},
            ],
            "parks": [
                {"name": "Jinnah Park", "type": "Park", "rating": 4.5, "distance": "2.0 km", "price": "Free"},
                {"name": "Race Course Park", "type": "Recreation", "rating": 4.6, "distance": "3.5 km", "price": "Free"},
                {"name": "Shalimar Gardens", "type": "Historic", "rating": 4.8, "distance": "8.0 km", "price": "Rs.20"},
            ],
        },
    }
    
    # Default places (if city not found)
    default_places = {
        "restaurants": [
            {"name": "Local Restaurant", "type": "Pakistani", "rating": 4.2, "distance": "0.8 km", "price": "$$"},
            {"name": "Fast Food", "type": "Fast Food", "rating": 4.0, "distance": "1.2 km", "price": "$"},
            {"name": "Café", "type": "Café", "rating": 4.1, "distance": "0.5 km", "price": "$$"},
        ],
        "hotels": [
            {"name": "Local Hotel", "type": "3-Star", "rating": 4.0, "distance": "1.0 km", "price": "$$"},
            {"name": "Guest House", "type": "Budget", "rating": 3.8, "distance": "1.5 km", "price": "$"},
        ],
        "cafes": [
            {"name": "Coffee Shop", "type": "Coffee", "rating": 4.2, "distance": "0.5 km", "price": "$$"},
            {"name": "Local Café", "type": "Café", "rating": 4.0, "distance": "0.8 km", "price": "$"},
        ],
        "parks": [
            {"name": "Local Park", "type": "Park", "rating": 4.0, "distance": "1.5 km", "price": "Free"},
            {"name": "Recreation Area", "type": "Recreation", "rating": 3.9, "distance": "2.0 km", "price": "Free"},
        ],
    }
    
    # Get places for the city, fallback to default
    city_places = places_by_city.get(city_key, {})
    category_places = city_places.get(category, default_places.get(category, []))
    
    # If no places found, return empty list
    if not category_places:
        return []
    
    return category_places


# ==================== HELPER FUNCTIONS ====================
@st.cache_data
def load_data():
    return load_cities("pak_cities.csv")


@st.cache_data
def load_all_locations():
    cities = load_cities("pak_cities.csv")
    all_locations = {city["name"]: {"lat": city["lat"], "lon": city["lon"], "type": "city"} for city in cities}
    for name, coords in get_all_locations().items():
        if name not in all_locations:
            all_locations[name] = {"lat": coords[0], "lon": coords[1], "type": "area"}
    return all_locations


@st.cache_data
def build_city_graph(threshold):
    return build_graph(load_data(), threshold_km=threshold)


def find_nearest_city(loc_coords, cities):
    min_dist, nearest = float('inf'), None
    for city in cities:
        dist = calculate_distance_km(loc_coords["lat"], loc_coords["lon"], city["lat"], city["lon"])
        if dist < min_dist:
            min_dist, nearest = dist, city["name"]
    return nearest, min_dist


def find_route(source, dest, all_locations, cities, graph):
    src_coords, dst_coords = all_locations[source], all_locations[dest]
    direct = calculate_distance_km(src_coords["lat"], src_coords["lon"], dst_coords["lat"], dst_coords["lon"])
    
    if direct < 50:
        return [source, dest], round(direct, 2), "local"
    
    src_city, src_dist = find_nearest_city(src_coords, cities)
    dst_city, dst_dist = find_nearest_city(dst_coords, cities)
    
    if src_city == dst_city:
        return [source, dest], round(direct, 2), "local"
    
    try:
        city_path, city_dist = dijkstra(graph, src_city, dst_city)
        if city_path:
            path = [source] + ([src_city] if source != src_city else [])
            path += city_path[1:-1]
            path += ([dst_city] if dest != dst_city else []) + [dest]
            seen, unique = set(), []
            for p in path:
                if p not in seen:
                    seen.add(p)
                    unique.append(p)
            return unique, round(src_dist + city_dist + dst_dist, 2), "intercity"
    except:
        pass
    return [source, dest], round(direct, 2), "direct"


def create_map(path, locations, mode="car"):
    coords = [(locations[loc]["lat"], locations[loc]["lon"]) for loc in path]
    center = [sum(c[0] for c in coords)/len(coords), sum(c[1] for c in coords)/len(coords)]
    
    m = folium.Map(location=center, zoom_start=6, tiles='CartoDB dark_matter')
    
    colors = {"car": "#22c55e", "bike": "#f59e0b", "cycle": "#3b82f6", "walk": "#8b5cf6"}
    color = colors.get(mode, "#22c55e")
    
    folium.PolyLine(coords, weight=5, color=color, opacity=0.8).add_to(m)
    plugins.AntPath(coords, delay=1000, weight=3, color=color, pulse_color='#fff', dash_array=[10,20]).add_to(m)
    
    for i, loc in enumerate(path):
        lat, lon = locations[loc]["lat"], locations[loc]["lon"]
        if i == 0:
            ic = folium.Icon(color='green', icon='play', prefix='fa')
        elif i == len(path)-1:
            ic = folium.Icon(color='red', icon='flag-checkered', prefix='fa')
        else:
            ic = folium.Icon(color='blue', icon='circle', prefix='fa')
        folium.Marker([lat, lon], tooltip=loc, icon=ic).add_to(m)
    
    m.fit_bounds(coords)
    return m


def create_pin_map(center_lat=30.3753, center_lon=69.3451, existing_pin=None, pin_type="from"):
    """Create an interactive map for dropping pins."""
    m = folium.Map(location=[center_lat, center_lon], zoom_start=10, tiles='CartoDB dark_matter')
    
    # Add click handler
    m.add_child(folium.ClickForMarker())
    
    # Add existing pin if provided
    if existing_pin:
        lat, lon = existing_pin["lat"], existing_pin["lon"]
        color = 'green' if pin_type == "from" else 'red'
        icon = 'play' if pin_type == "from" else 'flag-checkered'
        folium.Marker(
            [lat, lon],
            tooltip=f"{pin_type.upper()}: {existing_pin.get('name', 'Custom Location')}",
            icon=folium.Icon(color=color, icon=icon, prefix='fa')
        ).add_to(m)
    
    # Add instructions
    folium.LatLngPopup().add_to(m)
    
    return m


def get_road_distance(straight_dist):
    """Convert straight-line distance to approximate road distance.
    Roads are typically 1.3-1.5x longer than straight line distance."""
    ROAD_FACTOR = 1.4  # Average road winding factor
    return round(straight_dist * ROAD_FACTOR, 1)


def est_time(dist, speed):
    """Estimate travel time based on distance and speed."""
    hrs = dist / speed if speed > 0 else 0
    if hrs < 1:
        return f"{int(hrs * 60)} min"
    else:
        h = int(hrs)
        m = int((hrs - h) * 60)
        return f"{h}h {m}m"


def format_route(path):
    return ' <span style="color: var(--accent);">→</span> '.join(f'<span style="color: var(--text-primary);">{p}</span>' for p in path)


def generate_offline_data(path, distance, all_locations, mode_key, fuel_avg, fuel_price, speed):
    """Generate downloadable route data for offline use."""
    route_data = {
        "app": "SafarPak",
        "generated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "note": "Distances are road estimates (1.4x straight-line distance)",
        "route": {
            "from": path[0],
            "to": path[-1],
            "total_distance_km": distance,
            "transport_mode": mode_key,
            "speed_kmh": speed,
            "stops": len(path) - 2 if len(path) > 2 else 0,
        },
        "directions": [],
        "coordinates": []
    }
    
    cumulative = 0
    for i, loc in enumerate(path):
        coords = all_locations[loc]
        route_data["coordinates"].append({
            "name": loc,
            "lat": coords["lat"],
            "lon": coords["lon"],
            "stop_number": i + 1
        })
        
        if i < len(path) - 1:
            next_loc = path[i + 1]
            next_coords = all_locations[next_loc]
            seg_straight = calculate_distance_km(coords["lat"], coords["lon"], 
                                                next_coords["lat"], next_coords["lon"])
            seg_dist = get_road_distance(seg_straight)
            cumulative += seg_dist
            
            route_data["directions"].append({
                "step": i + 1,
                "from": loc,
                "to": next_loc,
                "distance_km": round(seg_dist, 1),
                "cumulative_km": round(cumulative, 1),
                "est_time": est_time(seg_dist, speed),
                "instruction": f"Head towards {next_loc}"
            })
    
    # Fuel calculation
    if mode_key in ["car", "bike"]:
        liters = distance / (fuel_avg * (1.5 if mode_key == "bike" else 1))
        route_data["fuel"] = {
            "liters_needed": round(liters, 2),
            "cost_estimate": round(liters * fuel_price, 0),
            "fuel_average_kmpl": fuel_avg,
            "fuel_price_per_liter": fuel_price
        }
    
    return route_data


def create_text_route(route_data):
    """Create a text version of the route for offline viewing."""
    text = f"""
╔══════════════════════════════════════════════════════════════╗
║                     🧭 SAFARPAK ROUTE                        ║
╚══════════════════════════════════════════════════════════════╝

📅 Generated: {route_data['generated']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📍 ROUTE SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   From: {route_data['route']['from']}
   To:   {route_data['route']['to']}
   
   🛣️  Total Distance: ~{route_data['route']['total_distance_km']} km (road estimate)
   🚗  Transport Mode: {route_data['route']['transport_mode'].upper()}
   🏎️  Speed: {route_data['route']['speed_kmh']} km/h
   📍  Stops: {route_data['route']['stops']}

"""
    
    if 'fuel' in route_data:
        text += f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⛽ FUEL ESTIMATE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Liters Needed: {route_data['fuel']['liters_needed']} L
   Estimated Cost: Rs. {int(route_data['fuel']['cost_estimate']):,}
   (Based on {route_data['fuel']['fuel_average_kmpl']} km/L @ Rs.{route_data['fuel']['fuel_price_per_liter']}/L)

"""
    
    text += f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧭 TURN-BY-TURN DIRECTIONS (at {route_data['route']['speed_kmh']} km/h)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
    
    for d in route_data['directions']:
        text += f"""   [{d['step']}] {d['from']} → {d['to']}
       📏 ~{d['distance_km']} km • ⏱️ {d['est_time']} (Total: {d['cumulative_km']} km)
       
"""
    
    text += """   [🏁] DESTINATION REACHED!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📍 COORDINATES (For GPS)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
    
    for c in route_data['coordinates']:
        text += f"   {c['stop_number']}. {c['name']}: {c['lat']:.6f}, {c['lon']:.6f}\n"
    
    text += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                    Safe Travels! 🇵🇰
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    return text


def get_download_link(content, filename, file_type="text"):
    """Generate a download link for the content."""
    if file_type == "json":
        b64 = base64.b64encode(json.dumps(content, indent=2).encode()).decode()
        mime = "application/json"
    else:
        b64 = base64.b64encode(content.encode()).decode()
        mime = "text/plain"
    
    return f'<a href="data:{mime};base64,{b64}" download="{filename}" class="download-btn">📥 Download {filename}</a>'


def get_direction_icon(from_loc, to_loc, all_locations):
    """Get appropriate direction icon based on bearing."""
    from_coords = all_locations[from_loc]
    to_coords = all_locations[to_loc]
    
    lat_diff = to_coords["lat"] - from_coords["lat"]
    lon_diff = to_coords["lon"] - from_coords["lon"]
    
    if abs(lat_diff) > abs(lon_diff):
        return "⬆️" if lat_diff > 0 else "⬇️"
    else:
        return "➡️" if lon_diff > 0 else "⬅️"


# ==================== MAIN APP ====================
def main():
    # Initialize theme in session state
    if 'theme' not in st.session_state:
        st.session_state.theme = 'dark'
    
    # Initialize custom locations
    if 'custom_locations' not in st.session_state:
        st.session_state.custom_locations = {}
    
    # Load data first
    try:
        cities = load_data()
        all_locations = load_all_locations()
        # Add custom locations to all_locations
        all_locations.update(st.session_state.custom_locations)
        location_names = sorted(all_locations.keys())
        location_categories = get_location_categories()
    except FileNotFoundError:
        st.error("⚠️ Run `python data_preparation.py` first!")
        st.stop()
    
    # Sidebar
    with st.sidebar:
        st.markdown("## ⚙️ Settings")
        
        # Theme selector
        st.markdown("**🎨 Theme**")
        theme = st.radio(
            "Select theme",
            options=["dark", "light", "colorblind"],
            format_func=lambda x: {"dark": "🌙 Dark", "light": "☀️ Light", "colorblind": "👁️ Color Blind"}[x],
            horizontal=True,
            label_visibility="collapsed"
        )
        st.session_state.theme = theme
        
        st.markdown("---")
        
        # Location browser
        st.markdown("**📍 Location Browser**")
        for cat, locs in location_categories.items():
            with st.expander(f"{cat} ({len(locs)})"):
                for loc in locs[:8]:
                    st.caption(f"• {loc}")
                if len(locs) > 8:
                    st.caption(f"*+{len(locs)-8} more*")
        
        st.markdown("---")
        st.metric("Total Locations", len(location_names))
    
    # Apply theme CSS
    st.markdown(get_theme_css(st.session_state.theme), unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div id="top" class="app-header">
        <div class="app-logo">🧭</div>
        <h1 class="app-title">SafarPak</h1>
        <p class="app-subtitle">Your Travel Companion Across Pakistan</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Input Section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="input-label">
            <span class="input-icon">📍</span> FROM
        </div>
        """, unsafe_allow_html=True)
        
        # Location selection row
        col1a, col1b = st.columns([3, 1])
        with col1a:
            source = st.selectbox("From", location_names, 
                                 index=location_names.index("DHA Karachi") if "DHA Karachi" in location_names else 0,
                                 label_visibility="collapsed", key="src")
        with col1b:
            col1b1, col1b2 = st.columns(2)
            with col1b1:
                if st.button("📍", key="from_live", help="Get my location", use_container_width=True):
                    st.session_state.get_from_live = True
            with col1b2:
                if st.button("🗺️", key="from_pin", help="Drop pin on map", use_container_width=True):
                    st.session_state.show_from_pin_map = True
        
        # Show pin map for FROM if requested
        if st.session_state.get('show_from_pin_map', False):
            st.markdown("**📍 Click on map to set FROM location:**")
            from_pin_coords = st.session_state.get('from_pin_coords', None)
            center = [30.3753, 69.3451]  # Default center (Pakistan)
            if from_pin_coords:
                center = [from_pin_coords['lat'], from_pin_coords['lon']]
            elif source in all_locations:
                center = [all_locations[source]['lat'], all_locations[source]['lon']]
            
            pin_map_from = create_pin_map(center[0], center[1], from_pin_coords, "from")
            map_data_from = st_folium(pin_map_from, width=None, height=300, returned_objects=["last_clicked"])
            
            if map_data_from.get("last_clicked"):
                lat = map_data_from["last_clicked"]["lat"]
                lon = map_data_from["last_clicked"]["lng"]
                custom_name = f"Custom From ({lat:.4f}, {lon:.4f})"
                st.session_state.custom_locations[custom_name] = {"lat": lat, "lon": lon, "type": "custom"}
                st.session_state.from_pin_coords = {"lat": lat, "lon": lon, "name": custom_name}
                source = custom_name
                st.session_state.show_from_pin_map = False
                st.rerun()
            
            if st.button("❌ Cancel", key="cancel_from_pin"):
                st.session_state.show_from_pin_map = False
                st.rerun()
    
    with col2:
        st.markdown("""
        <div class="input-label">
            <span class="input-icon">🎯</span> TO
        </div>
        """, unsafe_allow_html=True)
        
        # Location selection row
        col2a, col2b = st.columns([3, 1])
        with col2a:
            dest = st.selectbox("To", location_names,
                               index=location_names.index("F-7 Islamabad") if "F-7 Islamabad" in location_names else 1,
                               label_visibility="collapsed", key="dst")
        with col2b:
            col2b1, col2b2 = st.columns(2)
            with col2b1:
                if st.button("📍", key="to_live", help="Get my location", use_container_width=True):
                    st.session_state.get_to_live = True
            with col2b2:
                if st.button("🗺️", key="to_pin", help="Drop pin on map", use_container_width=True):
                    st.session_state.show_to_pin_map = True
        
        # Show pin map for TO if requested
        if st.session_state.get('show_to_pin_map', False):
            st.markdown("**🎯 Click on map to set TO location:**")
            to_pin_coords = st.session_state.get('to_pin_coords', None)
            center = [30.3753, 69.3451]  # Default center (Pakistan)
            if to_pin_coords:
                center = [to_pin_coords['lat'], to_pin_coords['lon']]
            elif dest in all_locations:
                center = [all_locations[dest]['lat'], all_locations[dest]['lon']]
            
            pin_map_to = create_pin_map(center[0], center[1], to_pin_coords, "to")
            map_data_to = st_folium(pin_map_to, width=None, height=300, returned_objects=["last_clicked"])
            
            if map_data_to.get("last_clicked"):
                lat = map_data_to["last_clicked"]["lat"]
                lon = map_data_to["last_clicked"]["lng"]
                custom_name = f"Custom To ({lat:.4f}, {lon:.4f})"
                st.session_state.custom_locations[custom_name] = {"lat": lat, "lon": lon, "type": "custom"}
                st.session_state.to_pin_coords = {"lat": lat, "lon": lon, "name": custom_name}
                dest = custom_name
                st.session_state.show_to_pin_map = False
                st.rerun()
            
            if st.button("❌ Cancel", key="cancel_to_pin"):
                st.session_state.show_to_pin_map = False
                st.rerun()
    
    # Hidden inputs - render normally but hide completely with CSS/JS
    from_live_data = st.text_input("", value="", key="from_live_data", label_visibility="collapsed", disabled=True)
    to_live_data = st.text_input("", value="", key="to_live_data", label_visibility="collapsed", disabled=True)
    
    # Aggressive CSS and JS to hide them completely - placed AFTER inputs so it can target them
    st.markdown("""
    <style>
        /* Target EVERYTHING related to these inputs - most aggressive selectors */
        section[data-testid*="from_live_data"],
        section[data-testid*="to_live_data"],
        div[data-testid*="from_live_data"],
        div[data-testid*="to_live_data"],
        section:has(input[data-testid*="from_live_data"]),
        section:has(input[data-testid*="to_live_data"]),
        div:has(input[data-testid*="from_live_data"]),
        div:has(input[data-testid*="to_live_data"]),
        .stTextInput:has(input[data-testid*="from_live_data"]),
        .stTextInput:has(input[data-testid*="to_live_data"]),
        input[data-testid*="from_live_data"],
        input[data-testid*="to_live_data"],
        label[for*="from_live_data"],
        label[for*="to_live_data"] {
            display: none !important;
            visibility: hidden !important;
            height: 0 !important;
            min-height: 0 !important;
            max-height: 0 !important;
            width: 0 !important;
            min-width: 0 !important;
            max-width: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            position: fixed !important;
            left: -99999px !important;
            top: -99999px !important;
            opacity: 0 !important;
            pointer-events: none !important;
            overflow: hidden !important;
            border: none !important;
            font-size: 0 !important;
            line-height: 0 !important;
            clip: rect(0, 0, 0, 0) !important;
        }
    </style>
    <script>
        (function() {
            function hideCompletely() {
                // Find ALL elements related to these inputs
                const allSelectors = [
                    'section[data-testid*="from_live_data"]',
                    'section[data-testid*="to_live_data"]',
                    'div[data-testid*="from_live_data"]',
                    'div[data-testid*="to_live_data"]',
                    'input[data-testid*="from_live_data"]',
                    'input[data-testid*="to_live_data"]'
                ];
                
                allSelectors.forEach(selector => {
                    try {
                        document.querySelectorAll(selector).forEach(el => {
                            // Apply comprehensive hiding
                            el.style.setProperty('display', 'none', 'important');
                            el.style.setProperty('visibility', 'hidden', 'important');
                            el.style.setProperty('height', '0', 'important');
                            el.style.setProperty('width', '0', 'important');
                            el.style.setProperty('margin', '0', 'important');
                            el.style.setProperty('padding', '0', 'important');
                            el.style.setProperty('position', 'fixed', 'important');
                            el.style.setProperty('left', '-99999px', 'important');
                            el.style.setProperty('top', '-99999px', 'important');
                            el.style.setProperty('opacity', '0', 'important');
                            el.style.setProperty('pointer-events', 'none', 'important');
                            el.style.setProperty('overflow', 'hidden', 'important');
                            el.style.setProperty('border', 'none', 'important');
                            el.style.setProperty('font-size', '0', 'important');
                            el.style.setProperty('line-height', '0', 'important');
                            
                            // Hide all children recursively
                            el.querySelectorAll('*').forEach(child => {
                                child.style.setProperty('display', 'none', 'important');
                                child.style.setProperty('visibility', 'hidden', 'important');
                            });
                            
                            // Hide parent containers up to 3 levels
                            let parent = el.parentElement;
                            for (let i = 0; i < 3 && parent && parent !== document.body; i++) {
                                if (parent.querySelector && parent.querySelector(selector)) {
                                    parent.style.setProperty('display', 'none', 'important');
                                    parent.style.setProperty('visibility', 'hidden', 'important');
                                    parent.style.setProperty('height', '0', 'important');
                                }
                                parent = parent.parentElement;
                            }
                        });
                    } catch(e) {}
                });
                
                // Fix accessibility attributes
                const fromInput = document.querySelector('input[data-testid*="from_live_data"]');
                const toInput = document.querySelector('input[data-testid*="to_live_data"]');
                
                if (fromInput) {
                    if (!fromInput.id) fromInput.id = 'from_live_data_input';
                    if (!fromInput.name) fromInput.name = 'from_live_data';
                    if (!fromInput.getAttribute('autocomplete')) fromInput.setAttribute('autocomplete', 'off');
                    if (!fromInput.getAttribute('aria-label')) fromInput.setAttribute('aria-label', 'Hidden input for from location data');
                }
                
                if (toInput) {
                    if (!toInput.id) toInput.id = 'to_live_data_input';
                    if (!toInput.name) toInput.name = 'to_live_data';
                    if (!toInput.getAttribute('autocomplete')) toInput.setAttribute('autocomplete', 'off');
                    if (!toInput.getAttribute('aria-label')) toInput.setAttribute('aria-label', 'Hidden input for to location data');
                }
            }
            
            // Run immediately
            hideCompletely();
            
            // Run on DOM ready
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', hideCompletely);
            }
            
            // Run very frequently to catch any rendering
            [1, 5, 10, 25, 50, 100, 200, 500, 1000, 2000, 3000].forEach(delay => {
                setTimeout(hideCompletely, delay);
            });
            
            // Watch for DOM changes aggressively
            const observer = new MutationObserver(() => {
                setTimeout(hideCompletely, 1);
            });
            observer.observe(document.body, { 
                childList: true, 
                subtree: true, 
                attributes: true,
                attributeFilter: ['style', 'class', 'data-testid']
            });
        })();
    </script>
    """, unsafe_allow_html=True)
    
    # Process live location data
    if from_live_data and from_live_data != "":
        try:
            data = json.loads(from_live_data)
            custom_name = f"My Location (From) - {data['lat']:.4f}, {data['lon']:.4f}"
            st.session_state.custom_locations[custom_name] = {
                "lat": data['lat'],
                "lon": data['lon'],
                "type": "custom"
            }
            all_locations[custom_name] = st.session_state.custom_locations[custom_name]
            location_names = sorted(all_locations.keys())
            source = custom_name
            st.session_state.from_live_data = ""  # Clear after processing
            st.rerun()
        except:
            pass
    
    if to_live_data and to_live_data != "":
        try:
            data = json.loads(to_live_data)
            custom_name = f"My Location (To) - {data['lat']:.4f}, {data['lon']:.4f}"
            st.session_state.custom_locations[custom_name] = {
                "lat": data['lat'],
                "lon": data['lon'],
                "type": "custom"
            }
            all_locations[custom_name] = st.session_state.custom_locations[custom_name]
            location_names = sorted(all_locations.keys())
            dest = custom_name
            st.session_state.to_live_data = ""  # Clear after processing
            st.rerun()
        except:
            pass
    
    # Handle live location requests
    if st.session_state.get('get_from_live', False):
        st.session_state.get_from_live = False
        st.markdown("""
        <script>
        (function() {{
            if (navigator.geolocation) {{
                const loadingMsg = document.createElement('div');
                loadingMsg.innerHTML = '📍 Getting your location...';
                loadingMsg.style.cssText = 'position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:#22c55e;color:white;padding:1rem 2rem;border-radius:12px;z-index:10000;';
                document.body.appendChild(loadingMsg);
                
                navigator.geolocation.getCurrentPosition(function(position) {{
                    const lat = position.coords.latitude;
                    const lon = position.coords.longitude;
                    loadingMsg.remove();
                    
                    // Check if in Pakistan (rough bounds)
                    if (lat >= 23.5 && lat <= 37.0 && lon >= 60.0 && lon <= 77.0) {{
                        // Update hidden input
                        const input = document.querySelector('input[data-testid*="from_live_data"]');
                        if (input) {{
                            input.value = JSON.stringify({{lat: lat, lon: lon}});
                            input.dispatchEvent(new Event('input', {{bubbles: true}}));
                            // Trigger Streamlit update
                            setTimeout(() => {{
                                const event = new Event('change', {{bubbles: true}});
                                input.dispatchEvent(event);
                                window.parent.postMessage({{type: 'streamlit:setFrameHeight', height: document.body.scrollHeight}}, '*');
                            }}, 100);
                        }}
                    }} else {{
                        loadingMsg.remove();
                        alert("Location is outside Pakistan. Please use pin drop instead.");
                    }}
                }}, function(error) {{
                    loadingMsg.remove();
                    alert("Unable to get your location: " + error.message + ". Please use pin drop instead.");
                }}, {{timeout: 10000, enableHighAccuracy: true}});
            }} else {{
                alert("Geolocation is not supported by your browser. Please use pin drop instead.");
            }}
        }})();
        </script>
        """, unsafe_allow_html=True)
    
    if st.session_state.get('get_to_live', False):
        st.session_state.get_to_live = False
        st.markdown("""
        <script>
        (function() {{
            if (navigator.geolocation) {{
                const loadingMsg = document.createElement('div');
                loadingMsg.innerHTML = '📍 Getting your location...';
                loadingMsg.style.cssText = 'position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:#22c55e;color:white;padding:1rem 2rem;border-radius:12px;z-index:10000;';
                document.body.appendChild(loadingMsg);
                
                navigator.geolocation.getCurrentPosition(function(position) {{
                    const lat = position.coords.latitude;
                    const lon = position.coords.longitude;
                    loadingMsg.remove();
                    
                    // Check if in Pakistan (rough bounds)
                    if (lat >= 23.5 && lat <= 37.0 && lon >= 60.0 && lon <= 77.0) {{
                        // Update hidden input
                        const input = document.querySelector('input[data-testid*="to_live_data"]');
                        if (input) {{
                            input.value = JSON.stringify({{lat: lat, lon: lon}});
                            input.dispatchEvent(new Event('input', {{bubbles: true}}));
                            // Trigger Streamlit update
                            setTimeout(() => {{
                                const event = new Event('change', {{bubbles: true}});
                                input.dispatchEvent(event);
                                window.parent.postMessage({{type: 'streamlit:setFrameHeight', height: document.body.scrollHeight}}, '*');
                            }}, 100);
                        }}
                    }} else {{
                        loadingMsg.remove();
                        alert("Location is outside Pakistan. Please use pin drop instead.");
                    }}
                }}, function(error) {{
                    loadingMsg.remove();
                    alert("Unable to get your location: " + error.message + ". Please use pin drop instead.");
                }}, {{timeout: 10000, enableHighAccuracy: true}});
            }} else {{
                alert("Geolocation is not supported by your browser. Please use pin drop instead.");
            }}
        }})();
        </script>
        """, unsafe_allow_html=True)
    
    # Settings Row 1
    c1, c2, c3 = st.columns(3)
    with c1:
        mode = st.selectbox("🚗 Mode", ["🚗 Car", "🏍️ Bike", "🚴 Cycle", "🚶 Walk"], label_visibility="collapsed")
        mode_key = mode.split()[1].lower()
    with c2:
        # Speed selector based on mode
        speed_options = {
            "car": [40, 50, 60, 70, 80, 90, 100, 110, 120],
            "bike": [30, 40, 50, 60, 70, 80],
            "cycle": [10, 15, 20, 25, 30],
            "walk": [3, 4, 5, 6, 7]
        }
        default_speeds = {"car": 60, "bike": 50, "cycle": 15, "walk": 5}
        selected_speed = st.selectbox(
            f"🏎️ Speed (km/h)", 
            options=speed_options.get(mode_key, [60]),
            index=speed_options.get(mode_key, [60]).index(default_speeds.get(mode_key, 60)) if default_speeds.get(mode_key, 60) in speed_options.get(mode_key, [60]) else 0,
            label_visibility="collapsed"
        )
    with c3:
        threshold = st.slider("🔗 Range (km)", 100, 500, 300, 25)
    
    # Settings Row 2
    c4, c5 = st.columns(2)
    with c4:
        fuel_avg = st.number_input("⛽ Car Avg (km/L)", 5.0, 30.0, 12.0, 0.5)
    with c5:
        fuel_price = st.number_input("💰 Fuel Price (Rs/L)", 100, 400, 260, 5)
    
    # Direct distance
    if source != dest:
        direct_straight = calculate_distance_km(
            all_locations[source]["lat"], all_locations[source]["lon"],
            all_locations[dest]["lat"], all_locations[dest]["lon"]
        )
        direct_road = get_road_distance(direct_straight)
        route_type = "🏙️ Local" if direct_straight < 50 else "🛣️ Inter-City"
        st.markdown(f'<p style="text-align:center;color:var(--text-muted);">📏 Est. Road Distance: <strong style="color:var(--accent);">~{direct_road:.0f} km</strong> • {route_type}</p>', unsafe_allow_html=True)
    
    # Find Route Button
    if st.button("🔍 FIND ROUTE", use_container_width=True):
        if source == dest:
            st.warning("⚠️ Select different locations!")
        else:
            progress = st.progress(0)
            progress.progress(30)
            graph = build_city_graph(threshold)
            progress.progress(60)
            path, straight_distance, route_mode = find_route(source, dest, all_locations, cities, graph)
            # Apply road factor for realistic distance
            distance = get_road_distance(straight_distance)
            progress.progress(100)
            time.sleep(0.2)
            progress.empty()
            
            if path:
                # Store route in session state so it persists across reruns
                st.session_state.current_route = {
                    "path": path,
                    "distance": distance,
                    "straight_distance": straight_distance,
                    "route_mode": route_mode,
                    "source": source,
                    "dest": dest,
                    "mode_key": mode_key,
                    "selected_speed": selected_speed,
                    "fuel_avg": fuel_avg,
                    "fuel_price": fuel_price
                }
    
    # Display route if it exists in session state (persists across reruns)
    if 'current_route' in st.session_state:
        route_data = st.session_state.current_route
        path = route_data["path"]
        distance = route_data["distance"]
        route_mode = route_data["route_mode"]
        mode_key = route_data["mode_key"]
        selected_speed = route_data["selected_speed"]
        fuel_avg = route_data["fuel_avg"]
        fuel_price = route_data["fuel_price"]
        
        if path:
            # Live badge
            st.markdown('<div class="live-badge"><div class="live-dot"></div><span class="live-text">Route Found</span></div>', unsafe_allow_html=True)
            
            # Route display
            st.markdown(f"""
            <div class="route-card">
                <p class="route-label">🛣️ OPTIMAL ROUTE</p>
                <p class="route-path">{format_route(path)}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Stats
            travel_time = est_time(distance, selected_speed)
            stops = len(path) - 2 if len(path) > 2 else 0
            
            if mode_key in ["car", "bike"]:
                liters = distance / (fuel_avg * (1.5 if mode_key == "bike" else 1))
                fuel_cost = int(liters * fuel_price)
                fuel_display = f"Rs.{fuel_cost:,}"
            else:
                liters, fuel_cost = 0, 0
                fuel_display = "Free 🌱"
            
            st.markdown(f"""
            <div class="stats-grid">
                <div class="stat-card"><p class="stat-value">~{distance:.0f}</p><p class="stat-label">Road KM</p></div>
                <div class="stat-card"><p class="stat-value">{stops}</p><p class="stat-label">Stops</p></div>
                <div class="stat-card"><p class="stat-value">{travel_time}</p><p class="stat-label">@ {selected_speed}km/h</p></div>
                <div class="stat-card"><p class="stat-value">{fuel_display}</p><p class="stat-label">Fuel Cost</p></div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f'<p style="text-align:center;color:var(--text-muted);font-size:0.8rem;margin-top:-0.5rem;">📏 Distances are road estimates • ⏱️ Time based on {selected_speed} km/h average speed</p>', unsafe_allow_html=True)
            
            # Fuel breakdown
            if mode_key in ["car", "bike"]:
                st.markdown(f"""
                <div class="fuel-breakdown">
                    <p class="fuel-title">⛽ Fuel Breakdown</p>
                    <div class="fuel-details">
                        <span>Distance: {distance} km</span>
                        <span>Avg: {fuel_avg} km/L</span>
                        <span>Liters: {liters:.1f} L</span>
                        <span>@ Rs.{fuel_price}/L</span>
                        <span class="fuel-total">= Rs.{fuel_cost:,}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Stops overview
            if len(path) > 2:
                stops_html = '<div class="stops-container">'
                for i, stop in enumerate(path):
                    if i == 0:
                        stops_html += f'<span class="stop-badge stop-start">START: {stop}</span>'
                    elif i == len(path) - 1:
                        stops_html += f'<span class="stop-badge stop-end">END: {stop}</span>'
                    else:
                        stops_html += f'<span class="stop-badge stop-mid">STOP {i}: {stop}</span>'
                    if i < len(path) - 1:
                        stops_html += '<span class="stop-arrow">→</span>'
                stops_html += '</div>'
                st.markdown(stops_html, unsafe_allow_html=True)
            
            # Tabs
            tabs = st.tabs(["🗺️ MAP", "🚗 DRIVE", "📍 DIRECTIONS", "💾 OFFLINE", "🍽️ FOOD", "🏨 STAY", "☕ CAFÉS", "🌳 PARKS"])
            
            with tabs[0]:  # MAP
                st.markdown('<div id="map" class="map-container">', unsafe_allow_html=True)
                st_folium(create_map(path, all_locations, mode_key), width=None, height=450, returned_objects=[])
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('<p style="text-align:center;color:var(--text-muted);margin-top:0.5rem;">🟢 Start • 🔵 Stop • 🔴 End</p>', unsafe_allow_html=True)
            
            with tabs[1]:  # DRIVE MODE
                st.markdown('<div id="drive"></div>', unsafe_allow_html=True)
                # Initialize drive mode state
                if 'drive_step' not in st.session_state:
                    st.session_state.drive_step = 0
                
                current_step = st.session_state.drive_step
                
                if current_step < len(path) - 1:
                    current_loc = path[current_step]
                    next_loc = path[current_step + 1]
                    
                    seg_dist_straight = calculate_distance_km(
                        all_locations[current_loc]["lat"], all_locations[current_loc]["lon"],
                        all_locations[next_loc]["lat"], all_locations[next_loc]["lon"]
                    )
                    seg_dist = get_road_distance(seg_dist_straight)
                    
                    # Calculate remaining distance
                    remaining_straight = 0
                    for i in range(current_step, len(path) - 1):
                        remaining_straight += calculate_distance_km(
                            all_locations[path[i]]["lat"], all_locations[path[i]]["lon"],
                            all_locations[path[i+1]]["lat"], all_locations[path[i+1]]["lon"]
                        )
                    remaining = get_road_distance(remaining_straight)
                    
                    progress_pct = ((distance - remaining) / distance) * 100 if distance > 0 else 0
                    eta = est_time(remaining, selected_speed)
                    direction_icon = get_direction_icon(current_loc, next_loc, all_locations)
                    
                    # Create mini map for current segment
                    drive_map = folium.Map(
                        location=[all_locations[current_loc]["lat"], all_locations[current_loc]["lon"]],
                        zoom_start=10,
                        tiles='CartoDB dark_matter'
                    )
                    
                    # Add markers for current segment
                    folium.Marker(
                        [all_locations[current_loc]["lat"], all_locations[current_loc]["lon"]],
                        tooltip="📍 You are here",
                        icon=folium.Icon(color='green', icon='car', prefix='fa')
                    ).add_to(drive_map)
                    
                    folium.Marker(
                        [all_locations[next_loc]["lat"], all_locations[next_loc]["lon"]],
                        tooltip=f"🎯 Next: {next_loc}",
                        icon=folium.Icon(color='blue', icon='flag', prefix='fa')
                    ).add_to(drive_map)
                    
                    # Add route line
                    segment_coords = [
                        [all_locations[current_loc]["lat"], all_locations[current_loc]["lon"]],
                        [all_locations[next_loc]["lat"], all_locations[next_loc]["lon"]]
                    ]
                    folium.PolyLine(segment_coords, weight=6, color='#22c55e', opacity=0.9).add_to(drive_map)
                    plugins.AntPath(segment_coords, delay=800, weight=4, color='#22c55e', pulse_color='#fff').add_to(drive_map)
                    
                    drive_map.fit_bounds(segment_coords, padding=[50, 50])
                    
                    # Navigation Header Card
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #1a472a 0%, #0d1f12 100%); border-radius: 16px; padding: 20px; margin-bottom: 15px; border: 2px solid #22c55e;">
                        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 15px;">
                            <div style="display: flex; align-items: center; gap: 10px;">
                                <div style="width: 12px; height: 12px; background: #22c55e; border-radius: 50%; animation: pulse 1.5s infinite;"></div>
                                <span style="color: #22c55e; font-weight: 700; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;">NAVIGATING</span>
                            </div>
                            <span style="color: #888; font-size: 0.85rem;">Step {current_step + 1}/{len(path) - 1}</span>
                        </div>
                        <div style="text-align: center;">
                            <div style="font-size: 4rem; margin-bottom: 5px;">{direction_icon}</div>
                            <p style="color: #fff; font-size: 1.8rem; font-weight: 700; margin: 10px 0;">Head to {next_loc}</p>
                            <p style="color: #22c55e; font-size: 3rem; font-weight: 800;">~{seg_dist:.0f} <span style="font-size: 1.2rem; color: #888;">km</span></p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Mini Map
                    st_folium(drive_map, width=None, height=250, returned_objects=[])
                    
                    # Info Cards Row
                    col_info1, col_info2, col_info3 = st.columns(3)
                    with col_info1:
                        st.markdown(f"""
                        <div style="background: #111; border-radius: 12px; padding: 15px; text-align: center;">
                            <p style="color: #666; font-size: 0.75rem; margin-bottom: 5px;">📍 FROM</p>
                            <p style="color: #fff; font-size: 1rem; font-weight: 600;">{current_loc}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    with col_info2:
                        st.markdown(f"""
                        <div style="background: #111; border-radius: 12px; padding: 15px; text-align: center;">
                            <p style="color: #666; font-size: 0.75rem; margin-bottom: 5px;">🎯 TO</p>
                            <p style="color: #22c55e; font-size: 1rem; font-weight: 600;">{next_loc}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    with col_info3:
                        st.markdown(f"""
                        <div style="background: #111; border-radius: 12px; padding: 15px; text-align: center;">
                            <p style="color: #666; font-size: 0.75rem; margin-bottom: 5px;">⏱️ SEGMENT</p>
                            <p style="color: #4ade80; font-size: 1rem; font-weight: 600;">{est_time(seg_dist, selected_speed)}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Progress Bar
                    st.markdown(f"""
                    <div style="background: #111; border-radius: 12px; padding: 15px; margin: 15px 0;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                            <span style="color: #888; font-size: 0.85rem;">Journey Progress</span>
                            <span style="color: #22c55e; font-weight: 600;">{progress_pct:.0f}%</span>
                        </div>
                        <div style="background: #222; border-radius: 10px; height: 12px; overflow: hidden;">
                            <div style="background: linear-gradient(90deg, #22c55e, #4ade80); width: {progress_pct:.0f}%; height: 100%; border-radius: 10px; transition: width 0.5s;"></div>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-top: 10px;">
                            <span style="color: #888;">📏 {remaining:.0f} km left</span>
                            <span style="color: #22c55e; font-weight: 600;">🕐 ETA: {eta}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Next stop preview
                    if current_step + 2 < len(path):
                        st.markdown(f"""
                        <div style="background: #0a0a0a; border: 1px solid #222; border-radius: 12px; padding: 12px;">
                            <p style="color: #666; font-size: 0.75rem; margin-bottom: 5px;">⏭️ THEN CONTINUE TO</p>
                            <p style="color: #888; font-size: 0.95rem;">{path[current_step + 2]}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Navigation Controls
                    col_d1, col_d2, col_d3 = st.columns([1, 1, 1])
                    with col_d1:
                        if st.button("⬅️ BACK", use_container_width=True, disabled=(current_step == 0)):
                            if st.session_state.drive_step > 0:
                                st.session_state.drive_step -= 1
                                st.rerun()
                    with col_d2:
                        if st.button("🔄 RESTART", use_container_width=True):
                            st.session_state.drive_step = 0
                            st.rerun()
                    with col_d3:
                        if st.button("NEXT ➡️", use_container_width=True, type="primary"):
                            if st.session_state.drive_step < len(path) - 2:
                                st.session_state.drive_step += 1
                                st.rerun()
                
                else:
                    # Arrived at destination
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #1a472a 0%, #0d1f12 100%); border-radius: 20px; padding: 40px; text-align: center; border: 3px solid #22c55e;">
                        <div style="font-size: 5rem; margin-bottom: 15px;">🏁</div>
                        <h2 style="color: #22c55e; font-size: 2rem; margin-bottom: 10px;">You Have Arrived!</h2>
                        <p style="color: #fff; font-size: 1.3rem; margin-bottom: 5px;">{path[-1]}</p>
                        <p style="color: #888; font-size: 1rem;">Journey Complete • Total: ~{distance:.0f} km</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("🔄 Start Over", use_container_width=True):
                        st.session_state.drive_step = 0
                        st.rerun()
                    
                    st.balloons()
                
                with tabs[2]:  # DIRECTIONS
                    st.markdown("### 🧭 Directions")
                    st.markdown(f"*Distances are road estimates at **{selected_speed} km/h***")
                    badge_color = "var(--info)" if route_mode == "local" else "var(--success)"
                    badge_text = "🏙️ Local" if route_mode == "local" else "🛣️ Inter-City"
                    st.markdown(f'<span style="background:{badge_color};color:white;padding:4px 12px;border-radius:20px;font-size:0.8rem;">{badge_text}</span>', unsafe_allow_html=True)
                    
                    cumulative = 0
                    for i in range(len(path) - 1):
                        frm, to = path[i], path[i+1]
                        seg_straight = calculate_distance_km(all_locations[frm]["lat"], all_locations[frm]["lon"],
                                                            all_locations[to]["lat"], all_locations[to]["lon"])
                        seg_dist = get_road_distance(seg_straight)
                        cumulative += seg_dist
                        direction = get_direction_icon(frm, to, all_locations)
                        st.markdown(f"""
                        <div class="nav-step">
                            <div class="nav-number">{direction}</div>
                            <div class="nav-content">
                                <p class="nav-cities">{frm} → {to}</p>
                                <p class="nav-meta">📏 ~{seg_dist:.0f} km • ⏱️ {est_time(seg_dist, selected_speed)} • Total: {cumulative:.0f} km</p>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class="nav-step" style="border-left-color: var(--error);">
                        <div class="nav-number" style="background: var(--error);">🏁</div>
                        <div class="nav-content">
                            <p class="nav-cities">Arrived at {path[-1]}</p>
                            <p class="nav-meta">🎉 Journey Complete!</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with tabs[3]:  # OFFLINE SAVE
                    st.markdown("### 💾 Save for Offline")
                    st.markdown("*Download your route to use without internet*")
                    
                    # Generate offline data
                    offline_data = generate_offline_data(path, distance, all_locations, mode_key, fuel_avg, fuel_price, selected_speed)
                    text_route = create_text_route(offline_data)
                    
                    st.markdown("---")
                    
                    # Text file download
                    st.markdown("""
                    <div class="offline-card">
                        <p class="offline-title">📄 Text Route (Printable)</p>
                        <p class="offline-desc">Plain text format - perfect for printing or viewing on any device</p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown(get_download_link(text_route, f"SafarPak_Route_{path[0]}_to_{path[-1]}.txt", "text"), unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # JSON file download
                    st.markdown("""
                    <div class="offline-card">
                        <p class="offline-title">📊 JSON Data (Technical)</p>
                        <p class="offline-desc">Machine-readable format with coordinates for GPS apps</p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown(get_download_link(offline_data, f"SafarPak_Route_{path[0]}_to_{path[-1]}.json", "json"), unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Preview
                    with st.expander("👁️ Preview Text Route"):
                        st.code(text_route, language=None)
                    
                    with st.expander("👁️ Preview JSON Data"):
                        st.json(offline_data)
                    
                    st.markdown("""
                    <div style="background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; padding: 1rem; margin-top: 1rem;">
                        <p style="color: var(--text-secondary); font-size: 0.85rem;">
                            💡 <strong>Tip:</strong> Save these files before your journey. The text file works offline on any device, 
                            while the JSON file can be imported into GPS navigation apps.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Nearby places tabs (adjusted indices)
                categories = [(4, "restaurants", "🍽️"), (5, "hotels", "🏨"), (6, "cafes", "☕"), (7, "parks", "🌳")]
                
                for idx, cat, icon in categories:
                    with tabs[idx]:
                        if idx == 4:  # First places tab
                            st.markdown('<div id="places"></div>', unsafe_allow_html=True)
                        st.markdown(f"### {icon} Nearby {cat.title()}")
                        
                        # Default to last location in path
                        default_idx = len(path) - 1 if path else 0
                        
                        # Use unique key for each category - Streamlit will maintain state automatically
                        selected = st.selectbox(
                            f"📍 Location:", 
                            path, 
                            index=default_idx, 
                            key=f"places_sel_{cat}_{idx}",  # Unique key per category and tab
                            label_visibility="collapsed"
                        )
                        
                        # Show selected location with visual feedback
                        st.markdown(f"*Showing {cat} near **{selected}***")
                        
                        # Get places for selected location - this will update when dropdown changes
                        # The function uses the selected location name to determine city and return appropriate places
                        places = get_nearby_places(selected, cat)
                        
                        # Show count of places found
                        if places:
                            st.caption(f"📍 Found {len(places)} {cat} near {selected}")
                        
                        if places:
                            for place in places:
                                stars = "⭐" * int(place['rating'])
                                st.markdown(f"""
                                <div class="place-card">
                                    <div class="place-icon">{icon}</div>
                                    <div class="place-info">
                                        <p class="place-name">{place['name']}</p>
                                        <p class="place-detail">{place['type']} • {place['price']}</p>
                                        <p class="place-rating">{stars} {place['rating']}</p>
                                    </div>
                                    <div class="place-distance">{place['distance']}</div>
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.info(f"📍 No {cat} found near {selected}. Try selecting a different location along your route.")
            
            st.markdown(f'<div class="success-banner"><p class="success-text">✅ Route: {len(path)} locations, {distance} km</p></div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="error-banner">
                <p class="error-title">❌ No Route Found</p>
                <p class="error-text">Try increasing the range or select different locations.</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Mobile Bottom Navigation (Mobile Only)
    st.markdown("""
    <div class="mobile-bottom-nav">
        <div class="nav-item" onclick="window.scrollTo({{top: 0, behavior: 'smooth'}});">
            <span class="nav-icon">🧭</span>
            <span>Route</span>
        </div>
        <div class="nav-item" onclick="document.getElementById('map')?.scrollIntoView({{behavior: 'smooth'}});">
            <span class="nav-icon">🗺️</span>
            <span>Map</span>
        </div>
        <div class="nav-item" onclick="document.getElementById('drive')?.scrollIntoView({{behavior: 'smooth'}});">
            <span class="nav-icon">🚗</span>
            <span>Drive</span>
        </div>
        <div class="nav-item" onclick="document.getElementById('places')?.scrollIntoView({{behavior: 'smooth'}});">
            <span class="nav-icon">📍</span>
            <span>Places</span>
        </div>
        <div class="nav-item" onclick="toggleSidebar();">
            <span class="nav-icon">⚙️</span>
            <span>Menu</span>
        </div>
    </div>
    <script>
        // Make nav items clickable
        document.querySelectorAll('.nav-item').forEach(item => {{
            item.style.cursor = 'pointer';
        }});
        
        // Toggle sidebar function
        function toggleSidebar() {{
            const sidebar = document.querySelector('[data-testid="stSidebar"]');
            const toggleButton = document.querySelector('[data-testid="stSidebarCollapseButton"]');
            if (sidebar && toggleButton) {{
                const isExpanded = sidebar.getAttribute('aria-expanded') === 'true';
                if (!isExpanded) {{
                    toggleButton.click();
                }} else {{
                    toggleButton.click();
                }}
            }}
        }}
        
        // Ensure sidebar is accessible on mobile
        function ensureSidebarAccessible() {{
            const sidebar = document.querySelector('[data-testid="stSidebar"]');
            const toggleButton = document.querySelector('[data-testid="stSidebarCollapseButton"]');
            if (sidebar && toggleButton) {{
                // Make sure toggle button is visible on mobile
                if (window.innerWidth <= 768) {{
                    toggleButton.style.display = 'block';
                    toggleButton.style.position = 'fixed';
                    toggleButton.style.top = '1rem';
                    toggleButton.style.right = '1rem';
                    toggleButton.style.zIndex = '1001';
                }}
            }}
        }}
        
        // Run sidebar accessibility check
        ensureSidebarAccessible();
        window.addEventListener('resize', ensureSidebarAccessible);
        
        // AGGRESSIVE fix for all input text visibility on mobile
        function fixAllInputText() {{
            // Get theme colors
            const root = document.documentElement;
            const computedStyle = getComputedStyle(root);
            const isDark = computedStyle.getPropertyValue('--bg-primary').trim().includes('0a0a0f') || 
                         computedStyle.getPropertyValue('--bg-primary').trim().includes('0a0a');
            const textColor = isDark ? '#fafafa' : '#18181b';
            
            // Fix all selectboxes
            const selects = document.querySelectorAll('[data-baseweb="select"]');
            selects.forEach(select => {{
                // Fix all elements inside select
                const allElements = select.querySelectorAll('*');
                allElements.forEach(el => {{
                    el.style.color = textColor + ' !important';
                    el.style.setProperty('color', textColor, 'important');
                }});
                
                // Fix inputs specifically
                const inputs = select.querySelectorAll('input');
                inputs.forEach(input => {{
                    input.style.color = textColor;
                    input.style.setProperty('color', textColor, 'important');
                    input.style.webkitTextFillColor = textColor;
                    input.style.setProperty('-webkit-text-fill-color', textColor, 'important');
                }});
                
                // Fix the select container itself
                select.style.color = textColor;
                select.style.setProperty('color', textColor, 'important');
            }});
            
            // Fix all number inputs
            const numberInputs = document.querySelectorAll('[data-baseweb="input"] input[type="number"]');
            numberInputs.forEach(input => {{
                input.style.color = textColor;
                input.style.setProperty('color', textColor, 'important');
                input.style.webkitTextFillColor = textColor;
                input.style.setProperty('-webkit-text-fill-color', textColor, 'important');
            }});
            
            // Fix Streamlit number input containers
            const stNumberInputs = document.querySelectorAll('.stNumberInput input');
            stNumberInputs.forEach(input => {{
                input.style.color = textColor;
                input.style.setProperty('color', textColor, 'important');
                input.style.webkitTextFillColor = textColor;
                input.style.setProperty('-webkit-text-fill-color', textColor, 'important');
            }});
            
            // Fix slider labels
            const sliderLabels = document.querySelectorAll('.stSlider label, .stSlider span');
            sliderLabels.forEach(label => {{
                label.style.color = textColor;
                label.style.setProperty('color', textColor, 'important');
            }});
        }}
        
        // Run immediately and multiple times to catch all elements
        if (document.readyState === 'loading') {{
            document.addEventListener('DOMContentLoaded', fixAllInputText);
        }} else {{
            fixAllInputText();
        }}
        
        // Run multiple times to catch dynamically loaded elements
        setTimeout(fixAllInputText, 100);
        setTimeout(fixAllInputText, 300);
        setTimeout(fixAllInputText, 500);
        setTimeout(fixAllInputText, 1000);
        setTimeout(fixAllInputText, 2000);
        
        // Also run when Streamlit reruns
        const observer = new MutationObserver(() => {{
            setTimeout(fixAllInputText, 100);
            ensureSidebarAccessible();
        }});
        observer.observe(document.body, {{ childList: true, subtree: true }});
        
        // Ensure maps are interactive on mobile
        function ensureMapInteractivity() {{
            const maps = document.querySelectorAll('.folium-map, iframe[src*="folium"]');
            maps.forEach(map => {{
                map.style.pointerEvents = 'auto';
                map.style.touchAction = 'pan-x pan-y pinch-zoom';
                // Remove any overlays that might block interaction
                const overlays = map.parentElement.querySelectorAll('.folium-overlay');
                overlays.forEach(overlay => {{
                    overlay.style.pointerEvents = 'none';
                }});
            }});
        }}
        
        // Run map interactivity check
        setTimeout(ensureMapInteractivity, 500);
        setTimeout(ensureMapInteractivity, 1500);
        setTimeout(ensureMapInteractivity, 3000);
        
        // Ensure download links work on mobile
        function ensureDownloadLinks() {{
            const downloadLinks = document.querySelectorAll('.download-btn, a[download]');
            downloadLinks.forEach(link => {{
                link.style.display = 'inline-block';
                link.style.minHeight = '48px';
                link.style.padding = '0.75rem 1.5rem';
                link.style.touchAction = 'manipulation';
                link.style.webkitTapHighlightColor = 'rgba(34, 197, 94, 0.3)';
            }});
        }}
        
        setTimeout(ensureDownloadLinks, 500);
        
        // Prevent double-tap zoom on buttons (iOS)
        let lastTouchEnd = 0;
        document.addEventListener('touchend', function(event) {{
            const now = Date.now();
            if (now - lastTouchEnd <= 300) {{
                event.preventDefault();
            }}
            lastTouchEnd = now;
        }}, false);
        
        // Improve touch scrolling
        document.addEventListener('touchstart', function(e) {{
            if (e.target.closest('.map-container, .folium-map')) {{
                // Allow map scrolling
                return;
            }}
        }}, {{ passive: true }});
    </script>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p><strong>SafarPak</strong> — Explore Pakistan with Confidence 🇵🇰</p>
        <p style="font-size:0.75rem;margin-top:0.5rem;">Navigate • Discover • Experience</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
