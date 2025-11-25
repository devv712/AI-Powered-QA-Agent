# AI-Powered QA Agent - Test Automation Platform

## 🎯 Project Overview

An intelligent, AI-powered system that revolutionizes QA testing by automatically generating comprehensive test cases and executable Selenium scripts from project documentation. Built using Retrieval Augmented Generation (RAG), this platform ensures all test reasoning is grounded strictly in provided documentation—no hallucinations.

### Current State
✅ **Production Ready** - Fully functional with professional UI/UX
- Modern, responsive design with gradient themes
- Secure OpenAI API key management via Replit Secrets
- Complete RAG pipeline with ChromaDB vector storage
- Three-phase workflow: Knowledge Base → Test Cases → Selenium Scripts

## 🏗️ Architecture

### Tech Stack
- **Frontend**: Streamlit with custom CSS styling
- **AI/LLM**: OpenAI GPT-5 (latest model as of Aug 2025)
- **RAG Framework**: LangChain with OpenAI embeddings
- **Vector Database**: ChromaDB with persistent storage
- **Document Processing**: PyMuPDF, BeautifulSoup, custom parsers
- **Automation**: Selenium WebDriver

### Core Components

#### 1. **app.py** - Main Streamlit Application
- Three-phase user interface
- Custom CSS for professional styling
- Session state management
- Progress indicators and user feedback

#### 2. **knowledge_base.py** - Vector Storage & RAG
- ChromaDB persistent client
- OpenAI text-embedding-3-small for embeddings
- RecursiveCharacterTextSplitter (1000 chars, 200 overlap)
- Semantic search and retrieval

#### 3. **test_case_agent.py** - AI Agents
- TestCaseAgent: Generates grounded test cases
- SeleniumScriptAgent: Creates executable Python scripts
- Both use GPT-5 with structured JSON output

#### 4. **document_parser.py** - Multi-format Parser
- Supports: MD, TXT, JSON, PDF, HTML
- Intelligent HTML element extraction
- Form and button analysis for Selenium generation

## 📊 Features

### Phase 1: Knowledge Base Ingestion
- Multi-format document upload (MD, TXT, JSON, PDF, HTML)
- Intelligent parsing and chunking
- Vector embeddings with ChromaDB
- Sample project for quick testing
- Progress tracking and validation

### Phase 2: Test Case Generation
- Natural language query interface
- Example queries for quick start
- RAG-based context retrieval (configurable 3-15 chunks)
- Structured JSON test case output
- Source document tracking
- Positive and negative test scenarios

### Phase 3: Selenium Script Generation
- Test case to Python script conversion
- HTML-aware selector extraction
- Production-ready code with:
  - Proper imports and setup
  - Explicit waits (WebDriverWait)
  - Error handling
  - Assertions
  - Comments and documentation
- Download functionality

## 🚀 Recent Changes (Session Nov 19, 2025)

### UI/UX Enhancements
1. **Modern Design System**
   - Gradient color scheme (purple/indigo theme)
   - Custom CSS for professional appearance
   - Smooth animations and transitions
   - Improved spacing and typography
   - Responsive layout

2. **Enhanced User Experience**
   - Progress bars for all AI operations
   - Clear status messages and feedback
   - Success banners with visual flair
   - Badge system for test case types
   - Expandable test case cards
   - Hover effects and micro-interactions

3. **Better Information Architecture**
   - Three distinct workflow phases
   - Sidebar navigation with stats
   - Example queries for guidance
   - Inline help and tooltips
   - Clear call-to-action buttons

### Technical Improvements
1. **Streamlit Configuration**
   - Custom theme in `.streamlit/config.toml`
   - Dark mode optimized
   - Server configured for port 5000
   - CORS and XSRF protection settings

2. **Code Quality**
   - Error handling improvements
   - Progress tracking for all operations
   - Session state management
   - Resource cleanup

3. **Security**
   - OpenAI API key via Replit Secrets
   - No hardcoded credentials
   - Environment variable validation

## 📁 Project Structure

```
.
├── app.py                      # Main Streamlit application (enhanced UI)
├── document_parser.py          # Multi-format document parsing
├── knowledge_base.py           # ChromaDB vector storage & RAG
├── test_case_agent.py          # AI agents for test/script generation
├── sample_project/             # Sample E-commerce checkout system
│   ├── checkout.html          # Sample checkout page
│   ├── product_specs.md       # Product specifications
│   ├── ui_ux_guide.txt        # UI/UX guidelines
│   └── api_endpoints.json     # API documentation
├── chroma_db/                 # ChromaDB persistence (auto-created)
├── pyproject.toml             # Python dependencies
├── .streamlit/                # Streamlit configuration
│   └── config.toml           # Theme and server settings
├── .replit                    # Replit configuration
├── replit.md                  # This file
└── README.md                  # Comprehensive project documentation
```

## 🔑 Environment Configuration

### Required Secrets
- `OPENAI_API_KEY`: Your OpenAI API key (starts with `sk-`)
  - Get from: https://platform.openai.com/api-keys
  - Used for: GPT-5 completions and text embeddings
  - Cost: ~$0.02-0.08 per test case/script generation

### Dependencies (Installed)
- streamlit>=1.51.0
- langchain>=1.0.0
- langchain-openai>=1.0.0
- langchain-community>=0.4.0
- chromadb>=1.3.0
- selenium>=4.0.0
- beautifulsoup4>=4.12.0
- pymupdf>=1.24.0
- python-dotenv>=1.0.0
- lxml>=6.0.0
- openai>=1.0.0

## 💡 User Preferences

### Coding Style
- Clean, readable Python code
- Type hints where beneficial (not overly strict)
- Comprehensive error handling
- Clear variable names
- Docstrings for all classes and methods

### Design Preferences
- Modern, professional UI
- Dark theme with purple/indigo accents
- Smooth animations and transitions
- Clear visual hierarchy
- Accessible and responsive

### Workflow Preferences
- Three-phase approach (linear workflow)
- Sample data for quick testing
- Progress indicators for AI operations
- Clear error messages with solutions
- Download functionality for generated code

## 🎨 UI/UX Design Guidelines

### Color Palette
- **Primary**: #667eea (Indigo)
- **Secondary**: #764ba2 (Purple)
- **Success**: #10b981 (Green)
- **Error**: #ef4444 (Red)
- **Background**: #0F172A (Dark blue-gray)
- **Cards**: #1E293B (Lighter blue-gray)
- **Text**: #F8FAFC (Off-white)

### Typography
- Font: Inter (Google Fonts)
- Headers: 700 weight
- Body: 400 weight
- Code: Monospace

### Components
- Cards with border-left accents
- Gradient backgrounds for headers/CTAs
- Badge system for categorization
- Expandable sections for details
- Hover states for interactivity

## 📈 Performance Considerations

### Optimal Usage
- **Document Size**: Keep individual documents under 50KB
- **Number of Documents**: 3-10 is ideal for performance
- **Context Chunks**: Start with 8, adjust based on complexity
- **API Costs**: 
  - Test case generation: ~$0.02-0.05
  - Script generation: ~$0.03-0.08
  - Embeddings: ~$0.001 per document

### Known Limitations
- ChromaDB resets on each session (by design for clean testing)
- Large PDF files may take longer to process
- HTML must be uploaded for Selenium script generation
- Requires active internet for OpenAI API calls

## 🔧 Troubleshooting

### Common Issues

**"OPENAI_API_KEY not set"**
- Add your API key in Replit Secrets
- Key format: `sk-...`

**"Knowledge base is empty"**
- Complete Phase 1 first
- Upload at least one document

**"No HTML content found"**
- Upload HTML file in Phase 1
- Or paste HTML content in text area

**Slow generation**
- Reduce context chunks (try 4-6)
- Use smaller documents
- Check internet connection

### Browser Console Warnings
The sidebar color warnings are cosmetic and don't affect functionality. They're related to Streamlit's theme system and can be safely ignored.

## 🎯 Future Enhancements (Ideas)

- [ ] Support for more test frameworks (Playwright, Cypress)
- [ ] Test execution reporting dashboard
- [ ] Integration with CI/CD pipelines
- [ ] Support for API testing (Postman/REST)
- [ ] Multi-language script generation
- [ ] Test data generation
- [ ] Visual regression testing
- [ ] Database persistence across sessions

## 📝 License

This project was created for demonstration and educational purposes. Feel free to use and modify.

## 🙏 Credits

Built with:
- [Streamlit](https://streamlit.io/) - Web UI framework
- [OpenAI GPT-5](https://openai.com/) - AI language model
- [LangChain](https://www.langchain.com/) - RAG framework
- [ChromaDB](https://www.trychroma.com/) - Vector database
- [Selenium](https://www.selenium.dev/) - Web automation

---

**Last Updated**: November 19, 2025
**Version**: 2.0 (Enhanced UI/UX)
**Status**: Production Ready ✅
