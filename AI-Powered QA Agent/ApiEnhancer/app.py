import streamlit as st
import os
import json
from pathlib import Path
from knowledge_base import KnowledgeBase
from test_case_agent import TestCaseAgent, SeleniumScriptAgent

st.set_page_config(
    page_title="AI QA Agent - Test Automation",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.8rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.2rem;
        margin-top: 0.5rem;
        font-weight: 400;
    }
    
    .phase-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
        transition: transform 0.2s;
    }
    
    .phase-card:hover {
        transform: translateX(4px);
    }
    
    .stats-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
    }
    
    .stats-number {
        font-size: 2.5rem;
        font-weight: 700;
        line-height: 1;
    }
    
    .stats-label {
        font-size: 0.9rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    
    .success-banner {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.3);
    }
    
    .info-card {
        background: #1e293b;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #334155;
        margin: 1rem 0;
    }
    
    .test-case-card {
        background: #1e293b;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 3px solid #667eea;
        margin: 1rem 0;
        transition: all 0.3s;
    }
    
    .test-case-card:hover {
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.4);
        transform: translateY(-2px);
    }
    
    .badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 0.5rem;
    }
    
    .badge-positive {
        background: rgba(16, 185, 129, 0.2);
        color: #10b981;
        border: 1px solid #10b981;
    }
    
    .badge-negative {
        background: rgba(239, 68, 68, 0.2);
        color: #ef4444;
        border: 1px solid #ef4444;
    }
    
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    div[data-testid="stExpander"] {
        background: #1e293b;
        border-radius: 12px;
        border: 1px solid #334155;
    }
    
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    .feature-item {
        background: #1e293b;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        border: 1px solid #334155;
        transition: all 0.3s;
    }
    
    .feature-item:hover {
        border-color: #667eea;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

if 'kb' not in st.session_state:
    st.session_state.kb = None
if 'test_cases' not in st.session_state:
    st.session_state.test_cases = []
if 'generated_script' not in st.session_state:
    st.session_state.generated_script = None
if 'kb_stats' not in st.session_state:
    st.session_state.kb_stats = None

st.markdown("""
<div class="main-header">
    <h1>🤖 AI-Powered QA Agent</h1>
    <p>Intelligent Test Case & Selenium Script Generation Platform</p>
</div>
""", unsafe_allow_html=True)

api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    st.error("⚠️ **OPENAI_API_KEY not configured**")
    st.info("💡 Please add your OpenAI API key in the Secrets section to activate this application.")
    st.stop()

with st.sidebar:
    st.markdown("### 🎯 Navigation")
    phase = st.radio(
        "Choose your workflow phase:",
        ["📚 Phase 1: Knowledge Base", "🧪 Phase 2: Test Cases", "⚙️ Phase 3: Selenium Scripts"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    st.markdown("### 💡 How It Works")
    st.markdown("""
    <div class="info-card">
        <b>Step 1:</b> Upload your documentation<br>
        <b>Step 2:</b> AI generates test cases<br>
        <b>Step 3:</b> Get Selenium automation scripts<br><br>
        All powered by <b>RAG + OpenAI GPT</b>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.kb_stats:
        st.markdown("---")
        st.markdown("### 📊 Knowledge Base")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="stats-box">
                <div class="stats-number">{st.session_state.kb_stats['total_documents']}</div>
                <div class="stats-label">Documents</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stats-box">
                <div class="stats-number">{st.session_state.kb_stats['total_chunks']}</div>
                <div class="stats-label">Chunks</div>
            </div>
            """, unsafe_allow_html=True)
        
        html_status = "✅ Ready" if st.session_state.kb_stats['has_html'] else "❌ Missing"
        st.markdown(f"**HTML Status:** {html_status}")
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; opacity: 0.6; font-size: 0.85rem;'>
        Built with Streamlit, LangChain & OpenAI<br>
        Version 2.0
    </div>
    """, unsafe_allow_html=True)

if phase == "📚 Phase 1: Knowledge Base":
    st.markdown("## 📚 Knowledge Base Ingestion")
    st.markdown("Upload your project documentation to build an intelligent knowledge base powered by vector embeddings.")
    
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1], gap="large")
    
    with col1:
        st.markdown("### 📄 Documentation Upload")
        st.markdown("Upload specifications, API docs, UI/UX guides, and any project documentation.")
        
        uploaded_docs = st.file_uploader(
            "Choose documentation files",
            type=['md', 'txt', 'json', 'pdf'],
            accept_multiple_files=True,
            help="Supported: Markdown, Text, JSON, PDF"
        )
        
        st.markdown("### 🌐 HTML Upload")
        st.markdown("Upload the target HTML file or paste HTML code for Selenium script generation.")
        
        uploaded_html = st.file_uploader(
            "Choose HTML file",
            type=['html', 'htm'],
            help="Required for generating Selenium scripts"
        )
        
        html_text = st.text_area(
            "Or paste HTML content:",
            height=120,
            placeholder="<html>...</html>",
            help="Paste your HTML code here as an alternative to file upload"
        )
    
    with col2:
        st.markdown("### 📦 Quick Start")
        st.markdown("""
        <div class="info-card">
            <b>Sample Project Included!</b><br><br>
            Try the demo with our sample e-commerce checkout system:<br>
            • checkout.html<br>
            • product_specs.md<br>
            • ui_ux_guide.txt<br>
            • api_endpoints.json
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Load Sample Project", use_container_width=True, type="primary"):
            try:
                sample_files = []
                sample_dir = Path("sample_project")
                
                if sample_dir.exists():
                    for file_path in sample_dir.glob("*"):
                        if file_path.is_file():
                            with open(file_path, 'rb') as f:
                                content = f.read()
                                sample_files.append((content, file_path.name))
                    
                    if sample_files:
                        with st.spinner("🔄 Building knowledge base..."):
                            kb = KnowledgeBase()
                            results = kb.ingest_multiple_documents(sample_files)
                        
                        st.session_state.kb = kb
                        st.session_state.kb_stats = kb.get_stats()
                        
                        st.markdown(f"""
                        <div class="success-banner">
                            <h3 style='margin: 0;'>✅ Success!</h3>
                            <p style='margin: 0.5rem 0 0 0;'>Knowledge base built with {len(results)} sample files</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        for result in results:
                            st.success(f"✓ **{result['filename']}**: {result['chunks_created']} chunks ({result['type']})")
                        
                        st.balloons()
                    else:
                        st.warning("No sample files found in sample_project/ directory")
                else:
                    st.warning("sample_project/ directory not found")
            
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        build_btn = st.button("🔨 Build Knowledge Base", type="primary", use_container_width=True)
    
    if build_btn:
        files_to_process = []
        
        if uploaded_docs:
            for uploaded_file in uploaded_docs:
                content = uploaded_file.read()
                files_to_process.append((content, uploaded_file.name))
        
        if uploaded_html:
            content = uploaded_html.read()
            files_to_process.append((content, uploaded_html.name))
        elif html_text.strip():
            files_to_process.append((html_text.encode('utf-8'), "pasted_html.html"))
        
        if not files_to_process:
            st.warning("⚠️ Please upload at least one document to build the knowledge base.")
        else:
            try:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                status_text.text("🔄 Initializing knowledge base...")
                progress_bar.progress(20)
                
                kb = KnowledgeBase()
                
                status_text.text("📝 Processing documents and creating embeddings...")
                progress_bar.progress(50)
                
                results = kb.ingest_multiple_documents(files_to_process)
                
                progress_bar.progress(80)
                status_text.text("✨ Finalizing...")
                
                st.session_state.kb = kb
                st.session_state.kb_stats = kb.get_stats()
                
                progress_bar.progress(100)
                status_text.empty()
                progress_bar.empty()
                
                st.markdown("""
                <div class="success-banner">
                    <h3 style='margin: 0;'>✅ Knowledge Base Built Successfully!</h3>
                    <p style='margin: 0.5rem 0 0 0;'>Your documents have been processed and embedded</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("### 📊 Ingestion Results")
                for result in results:
                    st.success(f"✓ **{result['filename']}**: {result['chunks_created']} chunks ({result['type']})")
                
                stats = kb.get_stats()
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Documents", stats['total_documents'])
                with col2:
                    st.metric("Total Chunks", stats['total_chunks'])
                with col3:
                    st.metric("HTML Status", "✅ Loaded" if stats['has_html'] else "❌ Missing")
                
                st.balloons()
            
            except Exception as e:
                st.error(f"❌ Error building knowledge base: {str(e)}")
                st.info("💡 Tip: Make sure your OpenAI API key is valid and has sufficient credits.")

elif phase == "🧪 Phase 2: Test Cases":
    st.markdown("## 🧪 AI Test Case Generation")
    st.markdown("Let AI generate comprehensive, documentation-grounded test cases using RAG technology.")
    
    if st.session_state.kb is None:
        st.warning("⚠️ **Knowledge base not ready**")
        st.info("👈 Please go to Phase 1 and upload your documentation first.")
    else:
        st.markdown("---")
        
        st.markdown("### 💬 Example Queries")
        st.markdown("Click any example to get started quickly:")
        
        example_queries = [
            "Generate all positive and negative test cases for the discount code feature",
            "Create test cases for form validation on the checkout page",
            "Generate test cases for the shopping cart functionality",
            "Create test cases for shipping method selection",
            "Generate test cases for the complete checkout flow"
        ]
        
        cols = st.columns(3)
        for i, query in enumerate(example_queries):
            with cols[i % 3]:
                if st.button(f"💡 {query[:25]}...", key=f"example_{i}", use_container_width=True):
                    st.session_state.user_query = query
                    st.rerun()
        
        st.markdown("---")
        st.markdown("### ✍️ Your Query")
        
        user_query = st.text_area(
            "Describe what you want to test:",
            value=st.session_state.get('user_query', ''),
            height=100,
            placeholder="Example: Generate comprehensive test cases for user authentication with valid and invalid credentials",
            help="Be specific about the feature or flow you want to test"
        )
        
        col1, col2 = st.columns([3, 1])
        with col1:
            generate_btn = st.button("🚀 Generate Test Cases", type="primary", use_container_width=True)
        with col2:
            n_chunks = st.number_input("Context chunks", min_value=3, max_value=15, value=8, help="More chunks = more context but slower generation")
        
        if generate_btn:
            if not user_query.strip():
                st.warning("⚠️ Please enter a query describing what you want to test.")
            else:
                try:
                    agent = TestCaseAgent(st.session_state.kb)
                    
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    status_text.text("🔍 Searching documentation...")
                    progress_bar.progress(25)
                    
                    status_text.text("🤖 AI is analyzing and generating test cases...")
                    progress_bar.progress(50)
                    
                    result = agent.generate_test_cases(user_query, n_context_chunks=n_chunks)
                    
                    progress_bar.progress(90)
                    
                    if result['success']:
                        progress_bar.progress(100)
                        status_text.empty()
                        progress_bar.empty()
                        
                        st.session_state.test_cases = result['test_cases']
                        
                        st.markdown(f"""
                        <div class="success-banner">
                            <h3 style='margin: 0;'>✅ Generated {len(result['test_cases'])} Test Cases!</h3>
                            <p style='margin: 0.5rem 0 0 0;'>Based on: {', '.join(result['sources_used'])}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("---")
                        st.markdown("### 📋 Generated Test Cases")
                        
                        for i, tc in enumerate(result['test_cases']):
                            test_type_badge = "badge-positive" if tc.get('test_type', '').lower() == 'positive' else "badge-negative"
                            
                            with st.expander(f"**{tc.get('test_id', f'TC-{i+1}')}**: {tc.get('test_scenario', 'Test Case')}", expanded=(i < 2)):
                                st.markdown(f"""
                                <div class="test-case-card">
                                    <span class="badge {test_type_badge}">{tc.get('test_type', 'N/A').upper()}</span>
                                    <span class="badge" style="background: rgba(102, 126, 234, 0.2); color: #667eea; border: 1px solid #667eea;">{tc.get('feature', 'N/A')}</span>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                col1, col2 = st.columns([2, 1])
                                
                                with col1:
                                    st.markdown(f"**📝 Scenario:** {tc.get('test_scenario', 'N/A')}")
                                    if tc.get('preconditions'):
                                        st.markdown(f"**🔧 Preconditions:** {tc.get('preconditions')}")
                                
                                with col2:
                                    st.markdown(f"**📚 Source:** `{tc.get('grounded_in', 'N/A')}`")
                                
                                if tc.get('test_steps'):
                                    st.markdown("**📋 Test Steps:**")
                                    for step in tc.get('test_steps', []):
                                        st.markdown(f"- {step}")
                                
                                if tc.get('test_data'):
                                    st.markdown("**📊 Test Data:**")
                                    st.json(tc.get('test_data'))
                                
                                st.markdown(f"**✅ Expected Result:** {tc.get('expected_result', 'N/A')}")
                        
                        st.success("💡 **Next Step:** Proceed to Phase 3 to generate Selenium automation scripts!")
                    
                    else:
                        progress_bar.empty()
                        status_text.empty()
                        st.error(f"❌ {result.get('error', 'Unknown error occurred')}")
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        
        if st.session_state.test_cases:
            st.markdown("---")
            st.info(f"📊 **{len(st.session_state.test_cases)} test cases** are ready for script generation in Phase 3")

elif phase == "⚙️ Phase 3: Selenium Scripts":
    st.markdown("## ⚙️ Selenium Script Generation")
    st.markdown("Convert your test cases into production-ready Selenium automation scripts.")
    
    if st.session_state.kb is None:
        st.warning("⚠️ **Knowledge base not ready**")
        st.info("👈 Please complete Phase 1 first.")
    elif not st.session_state.test_cases:
        st.warning("⚠️ **No test cases available**")
        st.info("👈 Please generate test cases in Phase 2 first.")
    else:
        st.markdown("---")
        
        st.markdown("### 🎯 Select Test Case")
        
        test_case_options = [
            f"{tc.get('test_id', f'TC-{i+1}')}: {tc.get('test_scenario', 'Test Case')}"
            for i, tc in enumerate(st.session_state.test_cases)
        ]
        
        selected_index = st.selectbox(
            "Choose a test case to convert:",
            range(len(test_case_options)),
            format_func=lambda i: test_case_options[i],
            label_visibility="collapsed"
        )
        
        selected_test_case = st.session_state.test_cases[selected_index]
        
        with st.expander("📋 **Test Case Details**", expanded=True):
            test_type_badge = "badge-positive" if selected_test_case.get('test_type', '').lower() == 'positive' else "badge-negative"
            
            st.markdown(f"""
            <div class="test-case-card">
                <h4 style='margin: 0 0 1rem 0;'>{selected_test_case.get('test_id', 'N/A')}</h4>
                <span class="badge {test_type_badge}">{selected_test_case.get('test_type', 'N/A').upper()}</span>
                <span class="badge" style="background: rgba(102, 126, 234, 0.2); color: #667eea; border: 1px solid #667eea;">{selected_test_case.get('feature', 'N/A')}</span>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**📝 Scenario:** {selected_test_case.get('test_scenario', 'N/A')}")
            
            with col2:
                st.markdown(f"**📚 Source:** `{selected_test_case.get('grounded_in', 'N/A')}`")
            
            if selected_test_case.get('test_steps'):
                st.markdown("**📋 Test Steps:**")
                for step in selected_test_case.get('test_steps', []):
                    st.markdown(f"- {step}")
        
        st.markdown("---")
        
        if st.button("🔧 Generate Selenium Script", type="primary", use_container_width=True):
            try:
                agent = SeleniumScriptAgent(st.session_state.kb)
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                status_text.text("🔍 Analyzing HTML structure...")
                progress_bar.progress(25)
                
                status_text.text("🤖 Generating Selenium script...")
                progress_bar.progress(60)
                
                result = agent.generate_selenium_script(selected_test_case)
                
                progress_bar.progress(90)
                
                if result['success']:
                    progress_bar.progress(100)
                    status_text.empty()
                    progress_bar.empty()
                    
                    st.session_state.generated_script = result['script']
                    
                    st.markdown(f"""
                    <div class="success-banner">
                        <h3 style='margin: 0;'>✅ Selenium Script Generated!</h3>
                        <p style='margin: 0.5rem 0 0 0;'>For test case: {result['test_case_id']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("### 📝 Generated Python Script")
                    
                    st.code(result['script'], language='python', line_numbers=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            label="💾 Download Script",
                            data=result['script'],
                            file_name=f"{result['test_case_id']}_selenium_script.py",
                            mime="text/x-python",
                            use_container_width=True,
                            type="primary"
                        )
                    
                    st.markdown("---")
                    st.markdown("### 🚀 How to Run This Script")
                    st.markdown("""
                    <div class="info-card">
                        <b>Prerequisites:</b><br>
                        1. Install Selenium: <code>pip install selenium</code><br>
                        2. Download ChromeDriver matching your Chrome version<br>
                        3. Add ChromeDriver to PATH or place in project directory<br><br>
                        <b>Run the script:</b><br>
                        <code>python {}_selenium_script.py</code><br><br>
                        <b>Note:</b> Adjust file paths in the script if needed.
                    </div>
                    """.format(result['test_case_id']), unsafe_allow_html=True)
                
                else:
                    progress_bar.empty()
                    status_text.empty()
                    st.error(f"❌ {result.get('error', 'Unknown error occurred')}")
            
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
        
        if st.session_state.generated_script:
            st.markdown("---")
            with st.expander("📄 **View Previously Generated Script**", expanded=False):
                st.code(st.session_state.generated_script, language='python')

st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem; opacity: 0.6;'>
    <p style='margin: 0; font-size: 0.9rem;'>🤖 AI-Powered QA Agent | Built with Streamlit, LangChain & OpenAI GPT</p>
    <p style='margin: 0.5rem 0 0 0; font-size: 0.8rem;'>Autonomous test generation using Retrieval Augmented Generation (RAG)</p>
</div>
""", unsafe_allow_html=True)
