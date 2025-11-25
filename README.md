[README.md](https://github.com/user-attachments/files/23750045/README.md)
# Autonomous QA Agent for Test Case and Script Generation

An intelligent AI-powered system that builds a "testing brain" from project documentation to generate comprehensive test cases and executable Selenium scripts. The system uses Retrieval Augmented Generation (RAG) to ensure all test reasoning is grounded strictly in provided documentation—no hallucinations.

## 🎯 Features

### Phase 1: Knowledge Base Ingestion
- **Multi-format Support**: Upload MD, TXT, JSON, PDF, and HTML files
- **Intelligent Parsing**: Custom parsers extract meaningful content from each format
- **Vector Storage**: ChromaDB with OpenAI embeddings for semantic search
- **Smart Chunking**: RecursiveCharacterTextSplitter maintains context while chunking
- **Metadata Preservation**: Tracks source documents for every piece of information

### Phase 2: Test Case Generation
- **RAG Pipeline**: Retrieves relevant context before generating test cases
- **Documentation-Grounded**: All test cases reference source documents
- **Comprehensive Coverage**: Generates both positive and negative test scenarios
- **Structured Output**: JSON format with test IDs, steps, data, and expected results
- **No Hallucinations**: Strict adherence to provided documentation

### Phase 3: Selenium Script Generation
- **HTML-Aware**: Uses actual element selectors from your HTML files
- **Executable Scripts**: Production-ready Python Selenium code
- **Best Practices**: Includes waits, error handling, and assertions
- **Instant Download**: Copy or download generated scripts

## 📋 Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Sample Files](#sample-files)
- [How It Works](#how-it-works)
- [API Reference](#api-reference)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## 🔧 Requirements

### System Requirements
- Python 3.11 or higher
- 2GB RAM minimum (4GB recommended)
- Internet connection (for OpenAI API)

### Python Dependencies
All dependencies are listed in `pyproject.toml`:

```toml
streamlit>=1.51.0
langchain>=1.0.0
langchain-openai>=1.0.0
langchain-community>=0.4.0
chromadb>=1.3.0
selenium>=4.0.0
beautifulsoup4>=4.12.0
pymupdf>=1.24.0
python-dotenv>=1.0.0
lxml>=6.0.0
openai>=1.0.0
```

## 🚀 Installation

### Option 1: Run on Replit (Recommended)

This project is pre-configured for Replit:

1. **Fork/Clone this Repl**
2. **Set your OpenAI API Key**:
   - Click on "Secrets" (lock icon) in the left sidebar
   - Add a new secret: `OPENAI_API_KEY` = `your-api-key-here`
3. **Click "Run"** - The app will start automatically!

### Option 2: Local Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd autonomous-qa-agent
   ```

2. **Install Python 3.11+**:
   ```bash
   python --version  # Should be 3.11 or higher
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   
   Or using uv (faster):
   ```bash
   uv pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your-openai-api-key-here
   ```

5. **Run the application**:
   ```bash
   streamlit run app.py --server.port 5000
   ```

6. **Access the app**:
   Open your browser to `http://localhost:5000`

## ⚙️ Configuration

### OpenAI API Key

You **must** provide an OpenAI API key to use this application:

1. **Get an API Key**:
   - Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
   - Create a new API key
   - Copy the key (starts with `sk-...`)

2. **Set the Key**:
   - **Replit**: Add to Secrets as `OPENAI_API_KEY`
   - **Local**: Add to `.env` file as shown above

### ChromaDB Configuration

ChromaDB is configured to persist in `./chroma_db` directory. This is created automatically when you build the knowledge base.

## 📖 Usage

### Step-by-Step Guide

#### Phase 1: Build Knowledge Base

1. **Navigate to Phase 1** in the sidebar
2. **Upload Documents**:
   - Click "Upload documentation files"
   - Select your MD, TXT, JSON, or PDF files
   - These should be product specs, UI/UX guides, API docs, etc.
3. **Upload HTML**:
   - Click "Upload target HTML file"
   - Select your HTML file (e.g., checkout.html)
   - Or paste HTML content in the text area
4. **Build Knowledge Base**:
   - Click "🔨 Build Knowledge Base"
   - Wait for processing (typically 10-30 seconds)
   - Review the ingestion results

**Quick Start**: Click "📥 Load Sample Files" to use the included sample project!

#### Phase 2: Generate Test Cases

1. **Navigate to Phase 2** in the sidebar
2. **Enter a Query**:
   - Type your test case request, for example:
     - "Generate all positive and negative test cases for the discount code feature"
     - "Create test cases for form validation on the checkout page"
   - Or click one of the example queries
3. **Generate Test Cases**:
   - Click "🚀 Generate Test Cases"
   - Wait for the AI agent (typically 15-45 seconds)
   - Review the generated test cases
4. **Verify Grounding**:
   - Each test case shows which source document it's based on
   - Expand test cases to see full details

#### Phase 3: Generate Selenium Scripts

1. **Navigate to Phase 3** in the sidebar
2. **Select a Test Case**:
   - Use the dropdown to select from generated test cases
   - Review the test case details
3. **Generate Script**:
   - Click "🔧 Generate Selenium Script"
   - Wait for script generation (typically 20-60 seconds)
   - Review the generated Python code
4. **Download Script**:
   - Click "💾 Download Script" to save as .py file
   - Or copy the code directly from the viewer

### Running Generated Scripts

To execute a generated Selenium script:

1. **Install Selenium**:
   ```bash
   pip install selenium
   ```

2. **Download ChromeDriver**:
   - Visit [ChromeDriver Downloads](https://chromedriver.chromium.org/downloads)
   - Download version matching your Chrome browser
   - Add to PATH or place in project directory

3. **Update File Path** (if needed):
   - Scripts assume HTML is at `./sample_project/checkout.html`
   - Modify path in script if your file is elsewhere

4. **Run the Script**:
   ```bash
   python TC-001_selenium_script.py
   ```

## 📁 Project Structure

```
autonomous-qa-agent/
├── app.py                      # Main Streamlit application
├── document_parser.py          # Multi-format document parsing
├── knowledge_base.py           # ChromaDB vector storage & RAG
├── test_case_agent.py          # Test case & script generation agents
├── sample_project/             # Sample E-Shop project
│   ├── checkout.html          # Sample checkout page
│   ├── product_specs.md       # Product specifications
│   ├── ui_ux_guide.txt        # UI/UX guidelines
│   └── api_endpoints.json     # API documentation
├── chroma_db/                 # ChromaDB persistence (auto-created)
├── pyproject.toml             # Python dependencies
├── .replit                    # Replit configuration
├── .streamlit/                # Streamlit configuration
│   └── config.toml
└── README.md                  # This file
```

## 📦 Sample Files

This project includes a complete sample e-commerce checkout system for demonstration:

### checkout.html
A fully functional single-page checkout application featuring:
- 3 products with "Add to Cart" functionality
- Shopping cart with quantity controls
- Discount code system (SAVE15, SAVE10)
- User details form with validation
- Shipping method selection (Standard/Express)
- Payment method selection (Credit Card/PayPal)
- Complete checkout flow with success message

### product_specs.md
Comprehensive product specifications including:
- Product catalog details
- Discount code rules (SAVE15 = 15% off, SAVE10 = 10% off)
- Shipping costs (Standard = Free, Express = $10)
- Form validation rules
- Price calculation examples
- Business logic documentation

### ui_ux_guide.txt
Detailed UI/UX guidelines covering:
- Color scheme and branding
- Typography standards
- Form validation display rules (errors in RED text)
- Button styling (Pay Now button must be GREEN)
- Element IDs and selectors
- Accessibility requirements
- Visual feedback specifications

### api_endpoints.json
API documentation including:
- Endpoint specifications (POST /apply_coupon, POST /submit_order, etc.)
- Request/response formats
- Validation rules
- Business logic
- Error codes
- Rate limits

## 🔍 How It Works

### Architecture Overview

```
┌─────────────────┐
│  User Interface │  (Streamlit)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Document Parser │  (Handles MD, TXT, JSON, PDF, HTML)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Knowledge Base  │  (ChromaDB + OpenAI Embeddings)
│  - Text Chunking│
│  - Vector Store │
│  - Metadata     │
└────────┬────────┘
         │
         ├───────────────┐
         │               │
         ▼               ▼
┌────────────────┐  ┌────────────────┐
│ Test Case Agent│  │ Selenium Agent │
│  - RAG Pipeline│  │  - Script Gen  │
│  - OpenAI GPT-5│  │  - OpenAI GPT-5│
└────────────────┘  └────────────────┘
```

### RAG Pipeline Details

1. **Document Ingestion**:
   - Parse documents with format-specific handlers
   - Split into chunks (1000 chars, 200 overlap)
   - Generate embeddings using OpenAI text-embedding-3-small
   - Store in ChromaDB with metadata

2. **Test Case Generation**:
   - User query → Embed query
   - Retrieve top-k relevant chunks from ChromaDB
   - Construct prompt with retrieved context
   - LLM generates structured test cases
   - Each test case references source document

3. **Selenium Script Generation**:
   - Receive selected test case
   - Retrieve HTML content from knowledge base
   - Extract element selectors and structure
   - LLM generates executable Python code
   - Include proper waits, assertions, error handling

### Key Technologies

- **Streamlit**: Web UI framework
- **LangChain**: RAG orchestration and text splitting
- **ChromaDB**: Vector database for semantic search
- **OpenAI GPT-5**: Latest language model (released Aug 2025)
- **OpenAI Embeddings**: text-embedding-3-small model
- **Selenium**: Web automation framework
- **BeautifulSoup**: HTML parsing
- **PyMuPDF**: PDF text extraction

## 📚 API Reference

### DocumentParser

```python
from document_parser import DocumentParser

# Parse any document type
parsed = DocumentParser.parse_document(
    file_content="<content>",
    filename="document.md",
    file_type=".md"  # Optional
)
# Returns: {"content": str, "source": str, "type": str}
```

### KnowledgeBase

```python
from knowledge_base import KnowledgeBase

# Initialize
kb = KnowledgeBase(
    collection_name="qa_docs",
    persist_directory="./chroma_db"
)

# Ingest documents
result = kb.ingest_document(file_content, filename)

# Query
results = kb.query("discount code", n_results=5)

# Get stats
stats = kb.get_stats()
```

### TestCaseAgent

```python
from test_case_agent import TestCaseAgent

# Initialize with knowledge base
agent = TestCaseAgent(kb)

# Generate test cases
result = agent.generate_test_cases(
    user_query="Generate test cases for discount feature",
    n_context_chunks=8
)
# Returns: {"success": bool, "test_cases": list, "sources_used": list}
```

### SeleniumScriptAgent

```python
from test_case_agent import SeleniumScriptAgent

# Initialize with knowledge base
agent = SeleniumScriptAgent(kb)

# Generate Selenium script
result = agent.generate_selenium_script(test_case)
# Returns: {"success": bool, "script": str, "test_case_id": str}
```

## 🐛 Troubleshooting

### Common Issues

#### "OPENAI_API_KEY environment variable not set"
**Solution**: Make sure you've added your OpenAI API key to Secrets (Replit) or .env file (local).

#### "Knowledge base is empty"
**Solution**: Complete Phase 1 by uploading documents and clicking "Build Knowledge Base" before proceeding to Phase 2.

#### "No HTML content found"
**Solution**: Upload an HTML file in Phase 1. The system needs HTML structure to generate accurate Selenium scripts.

#### ChromaDB errors
**Solution**: Delete the `chroma_db` folder and rebuild the knowledge base. This resets the vector database.

#### Slow generation times
**Solution**: 
- Reduce the number of context chunks in Phase 2 (default: 8)
- Use smaller documents
- Check your internet connection (API calls require network)

#### Script generation failures
**Solution**:
- Ensure HTML was uploaded in Phase 1
- Try regenerating with a different test case
- Check that test case has clear, specific steps

### Performance Tips

1. **Optimal Document Size**: 
   - Keep individual documents under 50KB for best performance
   - Split very large documents into sections

2. **Number of Documents**:
   - 3-10 documents is ideal
   - More documents = slower queries but better context

3. **Context Chunks**:
   - Start with 8 chunks (default)
   - Increase to 12-15 for complex features
   - Decrease to 4-6 for simple features

4. **API Costs**:
   - Each test case generation: ~$0.02-0.05
   - Each script generation: ~$0.03-0.08
   - Embeddings: ~$0.001 per document

## 📝 License

This project is created as an assignment demonstration. Feel free to use and modify for educational purposes.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [OpenAI GPT-5](https://openai.com/)
- Vector storage by [ChromaDB](https://www.trychroma.com/)
- RAG framework by [LangChain](https://www.langchain.com/)

---

## 📧 Support

For issues or questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review the [Usage](#usage) guide
3. Ensure all dependencies are installed correctly
4. Verify your OpenAI API key is set properly

---

**Built with ❤️ using AI-powered testing automation**
