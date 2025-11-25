import json
from typing import Dict, List, Optional, Any
from pathlib import Path
import fitz
from bs4 import BeautifulSoup


class DocumentParser:
    """
    Handles parsing of various document formats (MD, TXT, JSON, PDF, HTML)
    and extracts text content with metadata.
    """
    
    @staticmethod
    def parse_text_file(file_content: str, filename: str) -> Dict[str, str]:
        """
        Parse plain text or markdown files.
        
        Args:
            file_content: Content of the file as string
            filename: Name of the file
            
        Returns:
            Dictionary with text and metadata
        """
        return {
            "content": file_content,
            "source": filename,
            "type": "text"
        }
    
    @staticmethod
    def parse_json_file(file_content: str, filename: str) -> Dict[str, str]:
        """
        Parse JSON files and convert to readable text format.
        
        Args:
            file_content: JSON content as string
            filename: Name of the file
            
        Returns:
            Dictionary with formatted text and metadata
        """
        try:
            data = json.loads(file_content)
            
            formatted_text = f"JSON Document: {filename}\n\n"
            formatted_text += DocumentParser._format_json_recursive(data)
            
            return {
                "content": formatted_text,
                "source": filename,
                "type": "json"
            }
        except json.JSONDecodeError as e:
            return {
                "content": f"Error parsing JSON: {str(e)}\n\nRaw content:\n{file_content}",
                "source": filename,
                "type": "json_error"
            }
    
    @staticmethod
    def _format_json_recursive(data, indent=0) -> str:
        """
        Recursively format JSON data into readable text.
        
        Args:
            data: JSON data (dict, list, or primitive)
            indent: Current indentation level
            
        Returns:
            Formatted string representation
        """
        result = ""
        prefix = "  " * indent
        
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    result += f"{prefix}{key}:\n"
                    result += DocumentParser._format_json_recursive(value, indent + 1)
                else:
                    result += f"{prefix}{key}: {value}\n"
        elif isinstance(data, list):
            for i, item in enumerate(data):
                if isinstance(item, (dict, list)):
                    result += f"{prefix}[{i}]:\n"
                    result += DocumentParser._format_json_recursive(item, indent + 1)
                else:
                    result += f"{prefix}- {item}\n"
        else:
            result += f"{prefix}{data}\n"
        
        return result
    
    @staticmethod
    def parse_pdf_file(file_bytes: bytes, filename: str) -> Dict[str, str]:
        """
        Parse PDF files using PyMuPDF (fitz).
        
        Args:
            file_bytes: PDF file as bytes
            filename: Name of the file
            
        Returns:
            Dictionary with extracted text and metadata
        """
        try:
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            
            text_content = ""
            for page_num in range(len(doc)):
                page = doc[page_num]
                text_content += f"\n--- Page {page_num + 1} ---\n"
                page_text = page.get_text()
                text_content += str(page_text) if page_text else ""
            
            doc.close()
            
            return {
                "content": text_content,
                "source": filename,
                "type": "pdf"
            }
        except Exception as e:
            return {
                "content": f"Error parsing PDF: {str(e)}",
                "source": filename,
                "type": "pdf_error"
            }
    
    @staticmethod
    def parse_html_file(file_content: str, filename: str) -> Dict[str, str]:
        """
        Parse HTML files and extract both structure and text content.
        
        Args:
            file_content: HTML content as string
            filename: Name of the file
            
        Returns:
            Dictionary with extracted info and metadata
        """
        try:
            soup = BeautifulSoup(file_content, 'lxml')
            
            title = soup.title.string if soup.title else "No title"
            
            for script in soup(["script", "style"]):
                script.decompose()
            
            text_content = soup.get_text(separator='\n', strip=True)
            
            forms = soup.find_all('form')
            form_info = ""
            if forms:
                form_info = "\n\n=== FORM ELEMENTS ===\n"
                for i, form in enumerate(forms):
                    form_info += f"\nForm {i+1}:\n"
                    
                    inputs = form.find_all(['input', 'textarea', 'select', 'button'])
                    for inp in inputs:
                        tag_name = inp.name
                        inp_id = inp.get('id') or 'N/A'
                        inp_name = inp.get('name') or 'N/A'
                        inp_type = inp.get('type') or 'N/A'
                        inp_class = ' '.join(inp.get('class') or [])
                        
                        form_info += f"  - {tag_name}: id='{inp_id}', name='{inp_name}', type='{inp_type}', class='{inp_class}'\n"
            
            buttons = soup.find_all('button')
            button_info = ""
            if buttons:
                button_info = "\n\n=== BUTTONS ===\n"
                for btn in buttons:
                    btn_id = btn.get('id') or 'N/A'
                    btn_class = ' '.join(btn.get('class') or [])
                    btn_text = btn.get_text(strip=True)
                    btn_onclick = btn.get('onclick') or 'N/A'
                    button_info += f"  - Button: id='{btn_id}', class='{btn_class}', text='{btn_text}', onclick='{btn_onclick}'\n"
            
            ids_classes = "\n\n=== KEY IDENTIFIERS ===\n"
            elements_with_id = soup.find_all(id=True)
            for elem in elements_with_id[:50]:
                elem_id = elem.get('id') or ''
                elem_tag = elem.name or ''
                elem_class = ' '.join(elem.get('class') or [])
                ids_classes += f"  - {elem_tag}#{elem_id} (class: {elem_class})\n"
            
            full_content = f"HTML Document: {filename}\n"
            full_content += f"Title: {title}\n\n"
            full_content += "=== TEXT CONTENT ===\n"
            full_content += text_content
            full_content += form_info
            full_content += button_info
            full_content += ids_classes
            full_content += f"\n\n=== RAW HTML (for selector extraction) ===\n{file_content[:5000]}"
            
            return {
                "content": full_content,
                "source": filename,
                "type": "html",
                "raw_html": file_content
            }
        except Exception as e:
            return {
                "content": f"Error parsing HTML: {str(e)}\n\nRaw content:\n{file_content}",
                "source": filename,
                "type": "html_error"
            }
    
    @staticmethod
    def parse_document(file_content: Any, filename: str, file_type: Optional[str] = None) -> Dict[str, str]:
        """
        Main entry point for parsing any document type.
        
        Args:
            file_content: File content (string, bytes, or file-like object)
            filename: Name of the file
            file_type: Optional explicit file type
            
        Returns:
            Dictionary with parsed content and metadata
        """
        if hasattr(file_content, 'read'):
            file_content = file_content.read()
        
        if file_type is None:
            file_type = Path(filename).suffix.lower()
        
        if file_type in ['.md', '.txt']:
            if isinstance(file_content, bytes):
                file_content = file_content.decode('utf-8')
            return DocumentParser.parse_text_file(file_content, filename)
        
        elif file_type == '.json':
            if isinstance(file_content, bytes):
                file_content = file_content.decode('utf-8')
            return DocumentParser.parse_json_file(file_content, filename)
        
        elif file_type == '.pdf':
            if isinstance(file_content, str):
                file_content = file_content.encode('utf-8')
            return DocumentParser.parse_pdf_file(file_content, filename)
        
        elif file_type in ['.html', '.htm']:
            if isinstance(file_content, bytes):
                file_content = file_content.decode('utf-8')
            return DocumentParser.parse_html_file(file_content, filename)
        
        else:
            if isinstance(file_content, bytes):
                try:
                    file_content = file_content.decode('utf-8')
                except:
                    file_content = str(file_content)
            
            return {
                "content": file_content,
                "source": filename,
                "type": "unknown"
            }
