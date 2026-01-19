"""
Streamlit UI styling and theme management
"""


def get_theme_css(theme: str) -> str:
    if theme == 'light':
        return """
        /* Light Theme */
        .main {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .sub-header {
            color: #667eea;
            border-bottom: 3px solid #667eea;
        }
        .metric-card {
            background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
            border-left: 5px solid #667eea;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.1);
        }
        .result-highlight {
            background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);
            border: 2px solid #4caf50;
            box-shadow: 0 8px 30px rgba(76, 175, 80, 0.15);
        }
        .chart-container {
            background: linear-gradient(135deg, #ffffff 0%, #f5f7fa 100%);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        }
        .debug-condition {
            background: linear-gradient(135deg, #f8f9ff 0%, #ffffff 100%);
            border-left: 4px solid #667eea;
            box-shadow: 0 2px 8px rgba(102, 126, 234, 0.08);
        }
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }
        .stNumberInput input, .stTextInput input {
            background-color: white;
            color: #333;
        }
        """
    else:  # dark theme
        return """
        /* Dark Theme */
        .stApp {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        }
        .main {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        }
        .main-header {
            background: linear-gradient(135deg, #00d4ff 0%, #0099ff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .sub-header {
            color: #00d4ff !important;
            border-bottom: 3px solid #00d4ff;
        }
        .metric-card {
            background: linear-gradient(135deg, #252b42 0%, #1e2235 100%);
            border-left: 5px solid #00d4ff;
            box-shadow: 0 4px 15px rgba(0, 212, 255, 0.1);
        }
        .metric-card h2, .metric-card h3, .metric-card h4, .metric-card p {
            color: #e0e0e0 !important;
        }
        .result-highlight {
            background: linear-gradient(135deg, #1e4620 0%, #2d5a2f 100%);
            border: 2px solid #4caf50;
            box-shadow: 0 8px 30px rgba(76, 175, 80, 0.15);
        }
        .result-highlight h1, .result-highlight h2, .result-highlight p {
            color: #e0e0e0 !important;
        }
        .chart-container {
            background: linear-gradient(135deg, #252b42 0%, #1e2235 100%);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        }
        .debug-condition {
            background: linear-gradient(135deg, #252b42 0%, #1e2235 100%);
            border-left: 4px solid #00d4ff;
            box-shadow: 0 2px 8px rgba(0, 212, 255, 0.08);
        }
        .stButton > button {
            background: linear-gradient(135deg, #00d4ff 0%, #0099ff 100%) !important;
            color: #1a1a2e !important;
            box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3);
        }
        .stNumberInput input, .stTextInput input {
            background-color: #252b42 !important;
            color: #e0e0e0 !important;
            border-color: #00d4ff !important;
        }
        .stMarkdown, .stMarkdown p, .stMarkdown span, .stMarkdown div {
            color: #e0e0e0 !important;
        }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        }
        [data-testid="stSidebar"] label, [data-testid="stSidebar"] p {
            color: #e0e0e0 !important;
        }
        .stDataFrame, .stDataFrame table {
            background-color: #252b42 !important;
            color: #e0e0e0 !important;
        }
        .stExpander {
            background-color: #252b42 !important;
            border: 1px solid #00d4ff !important;
        }
        .streamlit-expanderHeader {
            background-color: #252b42 !important;
            color: #00d4ff !important;
        }
        .streamlit-expanderHeader:hover {
            background-color: #2d3350 !important;
        }
        .streamlit-expanderHeader p, .streamlit-expanderHeader svg {
            color: #00d4ff !important;
            fill: #00d4ff !important;
        }
        .streamlit-expanderContent {
            background-color: #1e2235 !important;
            border: 1px solid #00d4ff !important;
            color: #e0e0e0 !important;
        }
        [data-testid="stExpander"] {
            background-color: #252b42 !important;
            border: 1px solid #00d4ff !important;
        }
        [data-testid="stExpander"] details {
            background-color: #252b42 !important;
        }
        [data-testid="stExpander"] summary {
            background-color: #252b42 !important;
            color: #00d4ff !important;
        }
        [data-testid="stExpander"] summary:hover {
            background-color: #2d3350 !important;
        }
        [data-testid="stExpander"] p, [data-testid="stExpander"] span, [data-testid="stExpander"] div, [data-testid="stExpander"] li {
            color: #e0e0e0 !important;
        }
        [data-testid="stExpander"] h1, [data-testid="stExpander"] h2, [data-testid="stExpander"] h3, [data-testid="stExpander"] h4 {
            color: #00d4ff !important;
        }
        [data-testid="stExpander"] label {
            color: #e0e0e0 !important;
        }
        [data-testid="stExpander"] .stMarkdown {
            color: #e0e0e0 !important;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #e0e0e0 !important;
        }
        [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
            background-color: transparent !important;
        }
        .element-container {
            background-color: transparent !important;
        }
        [data-testid="stHeader"] {
            background-color: transparent !important;
        }
        section[data-testid="stSidebar"] > div {
            background-color: #1a1a2e !important;
        }
        """


def get_sticky_header_style(theme: str) -> tuple[str, str]:
    if theme == 'light':
        return (
            "background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);",
            "color: white;"
        )
    else:
        return (
            "background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);",
            "color: #00d4ff;"
        )
