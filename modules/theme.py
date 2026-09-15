"""
Bright, aesthetic UI theme: warm gradient background, colorful cards,
and a mild floral doodle pattern (SVG, embedded as base64) behind everything.
"""

FLORAL_SVG_B64 = (
    "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMjAiIGhlaWdodD0iMjIwIj4KICA8ZyBv"
    "cGFjaXR5PSIwLjE2Ij4KICAgIDxnIHRyYW5zZm9ybT0idHJhbnNsYXRlKDQ1LDQ1KSI+CiAgICAgIDxlbGxpcHNlIGN4PSIw"
    "IiBjeT0iLTE2IiByeD0iOSIgcnk9IjE2IiBmaWxsPSIjRkY4RkIxIi8+CiAgICAgIDxlbGxpcHNlIGN4PSIwIiBjeT0iMTYi"
    "IHJ4PSI5IiByeT0iMTYiIGZpbGw9IiNGRjhGQjEiLz4KICAgICAgPGVsbGlwc2UgY3g9Ii0xNiIgY3k9IjAiIHJ4PSIxNiIg"
    "cnk9IjkiIGZpbGw9IiNGRjhGQjEiLz4KICAgICAgPGVsbGlwc2UgY3g9IjE2IiBjeT0iMCIgcng9IjE2IiByeT0iOSIgZmls"
    "bD0iI0ZGOEZCMSIvPgogICAgICA8Y2lyY2xlIGN4PSIwIiBjeT0iMCIgcj0iOCIgZmlsbD0iI0ZGRDE2NiIvPgogICAgPC9n"
    "PgogICAgPGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMTUwLDE1MCkiPgogICAgICA8ZWxsaXBzZSBjeD0iMCIgY3k9Ii0xMyIg"
    "cng9IjciIHJ5PSIxMyIgZmlsbD0iIzlBRDZDOCIvPgogICAgICA8ZWxsaXBzZSBjeD0iMCIgY3k9IjEzIiByeD0iNyIgcnk9"
    "IjEzIiBmaWxsPSIjOUFENkM4Ii8+CiAgICAgIDxlbGxpcHNlIGN4PSItMTMiIGN5PSIwIiByeD0iMTMiIHJ5PSI3IiBmaWxs"
    "PSIjOUFENkM4Ii8+CiAgICAgIDxlbGxpcHNlIGN4PSIxMyIgY3k9IjAiIHJ4PSIxMyIgcnk9IjciIGZpbGw9IiM5QUQ2Qzgi"
    "Lz4KICAgICAgPGNpcmNsZSBjeD0iMCIgY3k9IjAiIHI9IjYiIGZpbGw9IiNGRkQxNjYiLz4KICAgIDwvZz4KICAgIDxnIHRy"
    "YW5zZm9ybT0idHJhbnNsYXRlKDE2MCw0MCkiPgogICAgICA8ZWxsaXBzZSBjeD0iMCIgY3k9Ii05IiByeD0iNSIgcnk9Ijki"
    "IGZpbGw9IiNDN0I2RjUiLz4KICAgICAgPGVsbGlwc2UgY3g9IjAiIGN5PSI5IiByeD0iNSIgcnk9IjkiIGZpbGw9IiNDN0I2"
    "RjUiLz4KICAgICAgPGVsbGlwc2UgY3g9Ii05IiBjeT0iMCIgcng9IjkiIHJ5PSI1IiBmaWxsPSIjQzdCNkY1Ii8+CiAgICAg"
    "IDxlbGxpcHNlIGN4PSI5IiBjeT0iMCIgcng9IjkiIHJ5PSI1IiBmaWxsPSIjQzdCNkY1Ii8+CiAgICAgIDxjaXJjbGUgY3g9"
    "IjAiIGN5PSIwIiByPSI0IiBmaWxsPSIjRkZEMTY2Ii8+CiAgICA8L2c+CiAgICA8cGF0aCBkPSJNNDAgMTcwIFEyOCAxOTAg"
    "NDggMjA1IFE1NCAxODQgNDAgMTcwIFoiIGZpbGw9IiM5M0M1RkQiLz4KICAgIDxwYXRoIGQ9Ik0xOTAgMTAwIFEyMDUgODgg"
    "MjAwIDY4IFExODIgNzggMTkwIDEwMCBaIiBmaWxsPSIjQjdFNEM3Ii8+CiAgPC9nPgo8L3N2Zz4="
)


def get_custom_css() -> str:
    return f"""
<style>
    html, body, [class*="css"] {{
        font-family: 'Segoe UI', 'Poppins', 'Inter', sans-serif;
    }}

    .stApp {{
        background-color: #FFFBF5;
        background-image:
            linear-gradient(180deg, rgba(255,251,245,0.94) 0%, rgba(255,244,236,0.94) 100%),
            url("data:image/svg+xml;base64,{FLORAL_SVG_B64}");
        background-size: auto, 220px 220px;
        background-repeat: repeat, repeat;
    }}

    /* Header banner */
    .app-header {{
        padding: 1.6rem 2rem;
        border-radius: 18px;
        background: linear-gradient(120deg, #FF8FB1 0%, #FFB27A 45%, #8FD9C4 100%);
        color: #1F2937;
        margin-bottom: 1.6rem;
        box-shadow: 0 10px 26px rgba(255, 143, 177, 0.25);
    }}
    .app-header h1 {{ margin: 0; font-size: 1.8rem; font-weight: 800; color: #1F2937; }}
    .app-header p {{ margin: 0.4rem 0 0 0; font-size: 0.98rem; color: #374151; }}

    /* Login hero */
    .login-hero {{
        text-align: center;
        padding: 1.2rem 0 0.6rem 0;
    }}
    .login-hero h1 {{
        font-size: 2.1rem;
        background: linear-gradient(90deg, #EC4899, #F97316, #10B981);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }}
    .login-hero p {{ color: #6B7280; font-size: 1rem; }}

    /* Generic content card */
    .card {{
        background: #FFFFFF;
        border: 1px solid #FCE7F3;
        border-radius: 16px;
        padding: 1.3rem 1.5rem;
        margin-bottom: 1.1rem;
        box-shadow: 0 4px 14px rgba(0,0,0,0.04);
    }}
    .card h4 {{ margin-top: 0; color: #1F2937; }}

    /* Metric card */
    .metric-card {{
        border-radius: 16px;
        padding: 1.1rem 1.2rem;
        text-align: center;
        color: white;
        box-shadow: 0 6px 16px rgba(0,0,0,0.10);
    }}
    .metric-card .label {{
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        opacity: 0.9;
    }}
    .metric-card .value {{
        font-size: 2rem;
        font-weight: 800;
        margin-top: 0.15rem;
    }}
    .grad-pink {{ background: linear-gradient(135deg, #F472B6, #EC4899); }}
    .grad-orange {{ background: linear-gradient(135deg, #FB923C, #F97316); }}
    .grad-teal {{ background: linear-gradient(135deg, #2DD4BF, #14B8A6); }}
    .grad-purple {{ background: linear-gradient(135deg, #A78BFA, #8B5CF6); }}

    /* Pills */
    .pill {{
        display: inline-block;
        padding: 0.28rem 0.75rem;
        border-radius: 999px;
        font-size: 0.82rem;
        margin: 0.15rem 0.25rem 0.15rem 0;
        font-weight: 700;
    }}
    .pill-green {{ background: #DCFCE7; color: #15803D; }}
    .pill-red {{ background: #FEE2E2; color: #B91C1C; }}
    .pill-blue {{ background: #DBEAFE; color: #1D4ED8; }}
    .pill-purple {{ background: #EDE9FE; color: #6D28D9; }}

    .category-badge {{
        display: inline-block;
        padding: 0.45rem 1.1rem;
        border-radius: 10px;
        font-weight: 800;
        font-size: 1rem;
    }}
    .cat-strong {{ background: #DCFCE7; color: #15803D; }}
    .cat-moderate {{ background: #FEF3C7; color: #B45309; }}
    .cat-low {{ background: #FEE2E2; color: #B91C1C; }}

    .fairness-note {{
        background: #EFF6FF;
        border-left: 4px solid #3B82F6;
        padding: 0.9rem 1.1rem;
        border-radius: 10px;
        color: #1E3A8A;
        font-size: 0.92rem;
    }}

    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #FFF1F5 0%, #FFF7ED 100%);
        border-right: 1px solid #FCE7F3;
    }}

    .stButton>button {{
        border-radius: 10px;
        font-weight: 700;
    }}
</style>
"""
