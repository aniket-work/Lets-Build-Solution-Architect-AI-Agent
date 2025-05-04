import streamlit as st
import uuid
import logging
from utils.logger_config import setup_logging
from ui.styling import load_enterprise_theme, add_architect_banner, add_professional_footer
from ui.components import add_project_description, enhance_example_prompts
from utils.diagram_parser import extract_mermaid_code, repair_mermaid_code
from services.diagram_service import DiagramGenerationService
from streamlit_mermaid import st_mermaid

# Initialize logging
logger = setup_logging()


class EnterpriseArchitectDashboard:
    """Main dashboard for the Enterprise Architect AI application"""

    def __init__(self):
        """Initialize the dashboard"""
        self.diagram_service = DiagramGenerationService()
        self._configure_page()
        self._initialize_session_state()

    def _configure_page(self):
        """Configure the page settings"""
        st.set_page_config(
            page_title="Enterprise Architect AI",
            page_icon="📊",
            layout="wide"
        )
        load_enterprise_theme()
        add_architect_banner()

    def _initialize_session_state(self):
        """Initialize session state variables"""
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "current_diagram" not in st.session_state:
            st.session_state.current_diagram = None
        if "diagram_id" not in st.session_state:
            st.session_state.diagram_id = str(uuid.uuid4())
        if "diagram_count" not in st.session_state:
            st.session_state.diagram_count = 0
        if "diagram_explanation" not in st.session_state:
            st.session_state.diagram_explanation = ""
        if "raw_response" not in st.session_state:
            st.session_state.raw_response = ""

    def _create_sidebar(self):
        """Create the sidebar with settings"""
        with st.sidebar:
            st.title("AI Agent Settings")

            # Agent selection
            agent_type = st.selectbox(
                "Select AI Agent",
                ["Enterprise Diagram Specialist"],
                index=0
            )

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

            return {
                "agent_type": agent_type,
                "model": model,
                "diagram_height": diagram_height,
                "show_controls": show_controls,
                "show_raw_response": show_raw_response
            }

    def render(self):
        """Render the dashboard"""
        st.title("Enterprise Architect AI")

        # Get sidebar settings
        settings = self._create_sidebar()

        # Add project description
        add_project_description()

        # Chat input
        user_input = st.text_area(
            "Enter your requirements",
            placeholder="Describe the architecture or system you want to design...",
            height=100
        )

        # Generate button
        if st.button("Generate Architecture", type="primary"):
            self._handle_generation(user_input, settings)

        # Display current diagram if exists
        self._display_current_diagram(settings)

        # Add example prompts and footer
        st.markdown("---")
        enhance_example_prompts()
        add_professional_footer()

    def _handle_generation(self, user_input, settings):
        """Handle diagram generation"""
        if not user_input:
            st.warning("Please enter architecture requirements first!")
            return

        with st.spinner("Generating Architecture Design..."):
            logger.info(f"Processing user request: {user_input[:100]}...")

            # Reset session state
            st.session_state.messages = []
            st.session_state.current_diagram = None
            st.session_state.diagram_id = str(uuid.uuid4())
            st.session_state.diagram_count = 0
            st.session_state.diagram_explanation = ""
            st.session_state.raw_response = ""

            # Add user message
            st.session_state.messages.append({"role": "user", "content": user_input})

            try:
                # Generate diagram
                self._generate_and_display_diagram(user_input, settings)
            except Exception as e:
                logger.error(f"Error generating architecture: {str(e)}")
                st.error(f"Error generating architecture: {str(e)}")

    def _generate_and_display_diagram(self, user_input, settings):
        """Generate and display diagram"""
        # Create containers
        response_container = st.container()
        diagram_container = st.container()
        debug_container = st.container()

        # Generate diagram
        response_stream = self.diagram_service.generate(
            user_input,
            model=settings["model"]
        )

        full_response = ""
        with response_container:
            for response in response_stream:
                if response.content:
                    full_response += response.content
                    st.session_state.raw_response = full_response

            # Process response
            self._process_diagram_response(
                full_response,
                diagram_container,
                debug_container,
                settings
            )

    def _process_diagram_response(self, response, diagram_container, debug_container, settings):
        """Process diagram response"""
        # Extract diagram code
        diagram_code = extract_mermaid_code(response)

        if diagram_code:
            # Repair if needed
            if len(diagram_code.splitlines()) <= 2:
                diagram_code = repair_mermaid_code(diagram_code)

            st.session_state.current_diagram = diagram_code
            st.session_state.diagram_count += 1

            # Display diagram
            with diagram_container:
                st.subheader("Generated Architecture")
                try:
                    st_mermaid(
                        diagram_code,
                        height=settings["diagram_height"],
                        show_controls=settings["show_controls"],
                        key=f"mermaid_{st.session_state.diagram_id}_{st.session_state.diagram_count}"
                    )
                except Exception as e:
                    st.error(f"Error rendering diagram: {str(e)}")
                    st.code(diagram_code, language="mermaid")

            # Extract explanation
            import re
            explanation = re.sub(r'```mermaid\n.*?\n```', '', response, flags=re.DOTALL).strip()
            if explanation:
                st.session_state.diagram_explanation = explanation
                st.subheader("Architecture Explanation")
                st.markdown(explanation)
        else:
            st.warning("Could not extract a valid diagram from the response.")

        # Show raw response if enabled
        with debug_container:
            if settings["show_raw_response"] and st.session_state.raw_response:
                st.subheader("Raw Model Response (Debug)")
                st.text_area("Response", st.session_state.raw_response, height=200, disabled=True)

    def _display_current_diagram(self, settings):
        """Display current diagram if it exists"""
        if st.session_state.current_diagram:
            st.subheader("Current Architecture Design")
            try:
                st_mermaid(
                    st.session_state.current_diagram,
                    height=settings["diagram_height"],
                    show_controls=settings["show_controls"],
                    key=f"current_mermaid_{st.session_state.diagram_id}"
                )
            except Exception as e:
                st.error(f"Error rendering current diagram: {str(e)}")
                st.code(st.session_state.current_diagram, language="mermaid")

            if st.session_state.diagram_explanation:
                st.subheader("Architecture Explanation")
                st.markdown(st.session_state.diagram_explanation)