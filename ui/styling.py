import streamlit as st


def load_enterprise_theme():
    """Load professional enterprise architect theme CSS"""
    st.markdown("""
    <style>
        /* Enterprise color scheme */
        :root {
            --primary-color: #0066B3;
            --secondary-color: #1C85C5;
            --accent-color: #FF9A3C;
            --background-color: #F8FAFD;
            --text-color: #2C3E50;
            --border-color: #D9E2EC;
        }

        /* Global styles */
        .main {
            background-color: var(--background-color);
            color: var(--text-color);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* Header styling */
        header[data-testid="stHeader"] {
            background-color: white;
            border-bottom: 1px solid var(--border-color);
        }

        .main h1 {
            color: var(--primary-color);
            font-weight: 700;
            padding-bottom: 0.5rem;
            border-bottom: 3px solid var(--accent-color);
            width: fit-content;
        }

        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            background-color: white;
            border-right: 1px solid var(--border-color);
        }

        section[data-testid="stSidebar"] h1 {
            color: var(--primary-color);
            font-size: 1.5rem;
            padding-bottom: 0.3rem;
            border-bottom: 2px solid var(--accent-color);
            width: fit-content;
        }

        /* Form elements */
        div[data-testid="stTextArea"] label {
            font-weight: 500;
        }

        div[data-testid="stTextArea"] > div > div {
            border-radius: 6px;
            border: 1px solid var(--border-color);
        }

        [data-testid="stButton"] > button {
            background-color: var(--primary-color);
            color: white;
            font-weight: 500;
            border-radius: 4px;
            padding: 0.5rem 1.5rem;
            transition: all 0.2s ease;
        }

        [data-testid="stButton"] > button:hover {
            background-color: var(--secondary-color);
            transform: translateY(-1px);
            box-shadow: 0 3px 5px rgba(0,0,0,0.1);
        }

        /* Diagram container */
        .diagram-container {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 1rem;
            margin: 1rem 0;
        }

        .diagram-placeholder {
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            color: #B0BEC5;
        }

        /* Sample prompts */
        .sample-prompt {
            cursor: pointer;
            padding: 0.75rem 1rem;
            background-color: #F1F7FD;
            border-left: 3px solid var(--primary-color);
            border-radius: 4px;
            margin-bottom: 0.75rem;
            transition: all 0.2s ease;
        }

        .sample-prompt:hover {
            background-color: #E3F0FC;
            transform: translateX(2px);
        }
    </style>

    <!-- Import Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

    <!-- Import Font Awesome for icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    """, unsafe_allow_html=True)


def add_architect_banner():
    """Add solution architect persona banner"""
    st.markdown("""
    <div style="display: flex; align-items: center; margin-bottom: 1.5rem; 
         background: linear-gradient(135deg, #0A2463 0%, #1E4D9B 100%); 
         border-radius: 6px; padding: 1.25rem; color: white;">
        <div style="width: 70px; height: 70px; border-radius: 50%; 
             background-color: #3E92CC; display: flex; 
             justify-content: center; align-items: center; 
             margin-right: 1.25rem; border: 3px solid rgba(255,255,255,0.8);">
            <i class="fas fa-project-diagram fa-2x" style="color: white;"></i>
        </div>
        <div>
            <h1 style="margin: 0; padding: 0; border: none; color: white; 
                 font-size: 1.8rem; line-height: 1.2;">
                Enterprise Architect AI
            </h1>
            <p style="margin: 0.25rem 0 0.5rem 0; opacity: 0.9; font-size: 1rem;">
                System Design & Integration Expert
            </p>
            <div>
                <span style="display: inline-block; background-color: rgba(255,255,255,0.2); 
                      padding: 0.2rem 0.6rem; border-radius: 50px; 
                      font-size: 0.7rem; margin-right: 0.5rem;">
                    Cloud Architecture
                </span>
                <span style="display: inline-block; background-color: rgba(255,255,255,0.2); 
                      padding: 0.2rem 0.6rem; border-radius: 50px; 
                      font-size: 0.7rem; margin-right: 0.5rem;">
                    Data Engineering
                </span>
                <span style="display: inline-block; background-color: rgba(255,255,255,0.2); 
                      padding: 0.2rem 0.6rem; border-radius: 50px; 
                      font-size: 0.7rem;">
                    System Integration
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def add_professional_footer():
    """Add professional footer"""
    st.markdown("""
    <div style="margin-top: 2rem; padding-top: 1rem; 
         border-top: 1px solid #D9E2EC; font-size: 0.8rem; 
         color: #6c757d; text-align: center;">
        <p>© 2025 Enterprise Architect AI | System Design Assistant | v2.4.1</p>
    </div>
    """, unsafe_allow_html=True)


def style_mermaid_output():
    """Apply styles to mermaid diagram output"""
    st.markdown("""
    <style>
        /* Mermaid styling */
        .stMermaid {
            background-color: white !important;
            padding: 1.5rem !important;
            border-radius: 8px !important;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08) !important;
            margin-bottom: 1rem !important;
        }

        .stMermaid svg {
            max-width: 100% !important;
            height: auto !important;
        }

        /* Mermaid nodes */
        .stMermaid .node rect, 
        .stMermaid .node circle, 
        .stMermaid .node ellipse, 
        .stMermaid .node polygon, 
        .stMermaid .node path {
            fill: #f5f8fd !important;
            stroke: #0066B3 !important;
            stroke-width: 1px !important;
        }

        /* Mermaid text */
        .stMermaid .node text {
            font-family: 'Inter', sans-serif !important;
            font-size: 14px !important;
        }

        /* Mermaid edges */
        .stMermaid .edgePath .path {
            stroke: #1C85C5 !important;
            stroke-width: 1.5px !important;
        }

        .stMermaid .edgeLabel {
            background-color: white !important;
            padding: 2px 4px !important;
            border-radius: 2px !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 12px !important;
        }
    </style>
    """, unsafe_allow_html=True)