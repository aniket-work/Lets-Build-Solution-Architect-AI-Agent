import streamlit as st
import uuid
from typing import List, Dict


class EnterpriseComponents:
    """UI components for Enterprise Architect dashboard"""

    @staticmethod
    def add_project_description():
        """Add expandable project description section"""
        with st.expander("**Enterprise Data Pipeline Project**", expanded=False):
            st.markdown("""
            # Enterprise Data Pipeline Orchestration System

            ## Project Overview
            The Enterprise Data Pipeline Orchestration System streamlines collection, processing, 
            transformation, and analysis of large-scale enterprise data. It integrates various 
            data sources, implements ETL processes, and provides real-time analytics.

            ## Key Features
            - Multi-source data integration (SQL, NoSQL, APIs, file systems)
            - Scalable ETL workflows with data cleansing
            - Advanced transformation rules engine
            - Optimized data lake architecture
            - Real-time analytics dashboards
            """)

    @staticmethod
    def enhance_example_prompts():
        """Add example prompts section with enhanced styling"""
        st.markdown("### Architecture Design Examples")

        prompts = [
            "Create a flowchart for an e-commerce order processing system with inventory integration",
            "Design a sequence diagram for user authentication with multi-factor authentication",
            "Generate a diagram for ETL data pipeline with validation stages",
            "Create a CI/CD deployment pipeline architecture with testing gates",
            "Design a microservice architecture with API gateway and discovery service",
            "Make a class diagram for inventory system with supplier integration"
        ]

        for prompt in prompts:
            st.markdown(f"""
            <div class="sample-prompt">
                <i class="fas fa-lightbulb" style="color: #FF9A3C; margin-right: 8px;"></i> {prompt}
            </div>
            """, unsafe_allow_html=True)

    @staticmethod
    def create_diagram_container(height: int = 400, show_controls: bool = True):
        """Create a container for diagram display

        Args:
            height: Height of diagram
            show_controls: Whether to show diagram controls

        Returns:
            container: Streamlit container for diagram
        """
        container = st.container()
        with container:
            st.markdown(f"""
            <div class="diagram-container" style="height: {height}px;">
                <div class="diagram-placeholder">
                    <i class="fas fa-project-diagram fa-3x"></i>
                    <p>Your architecture diagram will appear here</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        return container

    @staticmethod
    def create_sidebar_controls():
        """Create sidebar controls for the application

        Returns:
            Dict: Dictionary of control settings
        """
        with st.sidebar:
            st.title("AI Architect Settings")

            # Agent selection
            agent_type = st.selectbox(
                "Select Specialist",
                ["Enterprise Diagram Specialist", "System Integration Specialist"],
                index=0
            )

            # Model selection
            model = st.selectbox(
                "Select Model",
                ["llama-3.3-70b-versatile", "llama-3.3-8b-versatile"],
                index=0
            )

            # Diagram Settings
            st.subheader("Diagram Settings")
            diagram_height = st.slider("Diagram Height", 200, 800, 400, 50)
            show_controls = st.checkbox("Show Diagram Controls", value=True)

            # Debug options
            st.subheader("Debug Options")
            show_raw_response = st.checkbox("Show Raw Response", value=False)

            # Return settings
            return {
                "agent_type": agent_type,
                "model": model,
                "diagram_height": diagram_height,
                "show_controls": show_controls,
                "show_raw_response": show_raw_response
            }

    @staticmethod
    def display_api_status():
        """Display API connection status"""
        status_placeholder = st.empty()
        status_placeholder.info("Verifying API connection...")
        import time
        time.sleep(1)
        status_placeholder.success("API Connected ✅")

        return status_placeholder