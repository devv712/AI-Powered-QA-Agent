import os
import json
from typing import List, Dict, Any
from openai import OpenAI
from knowledge_base import KnowledgeBase


class TestCaseAgent:
    """
    Autonomous agent for generating test cases using RAG pipeline.
    Uses OpenAI LLM with retrieved context from knowledge base.
    """
    
    def __init__(self, knowledge_base: KnowledgeBase):
        """
        Initialize the test case generation agent.
        
        Args:
            knowledge_base: KnowledgeBase instance with ingested documents
        """
        self.kb = knowledge_base
        
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        self.client = OpenAI(api_key=api_key)
    
    def generate_test_cases(self, user_query: str, n_context_chunks: int = 8) -> Dict[str, Any]:
        """
        Generate test cases based on user query and retrieved documentation.
        
        Args:
            user_query: User's request for test cases
            n_context_chunks: Number of context chunks to retrieve
            
        Returns:
            Dictionary with generated test cases and metadata
        """
        query_results = self.kb.query(user_query, n_results=n_context_chunks)
        
        if not query_results["documents"]:
            return {
                "success": False,
                "error": "Knowledge base is empty. Please upload documents first.",
                "test_cases": []
            }
        
        context = self._build_context(query_results)
        
        prompt = self._build_test_case_prompt(user_query, context)
        
        try:
            # the newest OpenAI model is "gpt-5" which was released August 7, 2025.
            # do not change this unless explicitly requested by the user
            response = self.client.chat.completions.create(
                model="gpt-5",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert QA engineer specializing in test case design. "
                        "Generate comprehensive, documentation-grounded test cases. "
                        "CRITICAL: You must ONLY generate test cases based on the provided documentation context. "
                        "Do NOT hallucinate or invent features that are not mentioned in the context. "
                        "Every test case must reference the source document it is based on. "
                        "Respond with valid JSON only."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            if not content:
                return {
                    "success": False,
                    "error": "Empty response from LLM",
                    "test_cases": []
                }
            
            try:
                result = json.loads(content)
            except json.JSONDecodeError as je:
                return {
                    "success": False,
                    "error": f"Failed to parse JSON response: {str(je)}",
                    "test_cases": []
                }
            
            return {
                "success": True,
                "test_cases": result.get("test_cases", []),
                "query": user_query,
                "sources_used": list(set([m["source"] for m in query_results["metadatas"]]))
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error generating test cases: {str(e)}",
                "test_cases": []
            }
    
    def _build_context(self, query_results: Dict[str, Any]) -> str:
        """
        Build context string from query results.
        
        Args:
            query_results: Results from knowledge base query
            
        Returns:
            Formatted context string
        """
        context = "=== RETRIEVED DOCUMENTATION CONTEXT ===\n\n"
        
        for i, (doc, meta) in enumerate(zip(query_results["documents"], query_results["metadatas"])):
            context += f"[Source: {meta['source']}, Chunk {meta['chunk_index'] + 1}/{meta['total_chunks']}]\n"
            context += f"{doc}\n\n"
            context += "-" * 80 + "\n\n"
        
        return context
    
    def _build_test_case_prompt(self, user_query: str, context: str) -> str:
        """
        Build the prompt for test case generation.
        
        Args:
            user_query: User's query
            context: Retrieved documentation context
            
        Returns:
            Complete prompt string
        """
        prompt = f"""You are tasked with generating test cases for a web application based STRICTLY on the provided documentation.

USER REQUEST:
{user_query}

DOCUMENTATION CONTEXT:
{context}

INSTRUCTIONS:
1. Generate comprehensive test cases that cover the functionality described in the documentation
2. Include both positive (happy path) and negative (error) test cases
3. CRITICAL: Base ALL test cases ONLY on information found in the provided documentation context
4. Do NOT invent, assume, or hallucinate any features, behaviors, or requirements not explicitly mentioned
5. Each test case MUST reference the source document it is grounded in
6. Use the exact element IDs, names, and values mentioned in the documentation

OUTPUT FORMAT:
Respond with a JSON object in this exact structure:
{{
  "test_cases": [
    {{
      "test_id": "TC-001",
      "feature": "Feature name",
      "test_scenario": "Detailed test scenario description",
      "test_type": "positive or negative",
      "preconditions": "Any setup required before test",
      "test_steps": [
        "Step 1: ...",
        "Step 2: ...",
        "Step 3: ..."
      ],
      "test_data": {{
        "input_field": "value",
        "another_field": "value"
      }},
      "expected_result": "Expected outcome",
      "grounded_in": "source_document_name.ext"
    }}
  ]
}}

Generate 5-15 test cases covering different aspects of the requested functionality.
Ensure proper JSON formatting with no syntax errors.
"""
        return prompt


class SeleniumScriptAgent:
    """
    Agent for generating Selenium Python scripts from test cases.
    """
    
    def __init__(self, knowledge_base: KnowledgeBase):
        """
        Initialize the Selenium script generation agent.
        
        Args:
            knowledge_base: KnowledgeBase instance with HTML content
        """
        self.kb = knowledge_base
        
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        self.client = OpenAI(api_key=api_key)
    
    def generate_selenium_script(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate Selenium Python script from a test case.
        
        Args:
            test_case: Test case dictionary
            
        Returns:
            Dictionary with generated script and metadata
        """
        html_content = self.kb.get_html_content()
        
        if not html_content:
            return {
                "success": False,
                "error": "No HTML content found in knowledge base. Please upload HTML file.",
                "script": ""
            }
        
        query_results = self.kb.query(
            f"HTML elements for {test_case.get('feature', '')} {' '.join(test_case.get('test_steps', []))}",
            n_results=3
        )
        
        context = ""
        if query_results["documents"]:
            for doc in query_results["documents"]:
                context += doc + "\n\n"
        
        prompt = self._build_selenium_prompt(test_case, html_content, context)
        
        try:
            # the newest OpenAI model is "gpt-5" which was released August 7, 2025.
            # do not change this unless explicitly requested by the user
            response = self.client.chat.completions.create(
                model="gpt-5",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert Selenium (Python) automation engineer. "
                        "Generate clean, runnable Selenium WebDriver scripts. "
                        "CRITICAL: Use ONLY selectors that exist in the provided HTML. "
                        "Do NOT invent or hallucinate element IDs, names, or CSS selectors. "
                        "Include proper waits, error handling, and assertions. "
                        "The code should be production-ready and follow best practices. "
                        "Respond with valid JSON only, using this format: "
                        "{\"script\": \"<python code here>\", \"description\": \"brief description\"}"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"}
            )
            
            if not response or not response.choices:
                return {
                    "success": False,
                    "error": "Empty response from LLM",
                    "script": ""
                }
            
            message = response.choices[0].message
            
            if not hasattr(message, 'content') or not message.content:
                return {
                    "success": False,
                    "error": "Response message has no content",
                    "script": ""
                }
            
            try:
                result = json.loads(message.content)
            except json.JSONDecodeError as je:
                return {
                    "success": False,
                    "error": f"Failed to parse JSON response: {str(je)}",
                    "script": ""
                }
            
            script = result.get("script", "")
            if not script:
                return {
                    "success": False,
                    "error": "No script found in JSON response",
                    "script": ""
                }
            
            if len(script) < 10:
                return {
                    "success": False,
                    "error": "Generated script is too short",
                    "script": ""
                }
            
            return {
                "success": True,
                "script": script,
                "test_case_id": test_case.get("test_id", "Unknown"),
                "feature": test_case.get("feature", "Unknown")
            }
            
        except AttributeError as ae:
            return {
                "success": False,
                "error": f"Response structure error: {str(ae)}. The LLM response format may have changed.",
                "script": ""
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error generating Selenium script: {str(e)}",
                "script": ""
            }
    
    def _build_selenium_prompt(self, test_case: Dict[str, Any], html_content: str, context: str) -> str:
        """
        Build prompt for Selenium script generation.
        
        Args:
            test_case: Test case dictionary
            html_content: Raw HTML content
            context: Additional documentation context
            
        Returns:
            Complete prompt string
        """
        html_snippet = html_content[:8000] if len(html_content) > 8000 else html_content
        
        prompt = f"""Generate a complete, runnable Selenium Python script for the following test case.

TEST CASE:
Test ID: {test_case.get('test_id', 'N/A')}
Feature: {test_case.get('feature', 'N/A')}
Scenario: {test_case.get('test_scenario', 'N/A')}
Type: {test_case.get('test_type', 'N/A')}

Preconditions:
{test_case.get('preconditions', 'None')}

Test Steps:
{chr(10).join(test_case.get('test_steps', []))}

Test Data:
{json.dumps(test_case.get('test_data', {}), indent=2)}

Expected Result:
{test_case.get('expected_result', 'N/A')}

HTML CONTENT (use this to identify correct selectors):
{html_snippet}

DOCUMENTATION CONTEXT:
{context}

REQUIREMENTS:
1. Generate a complete Python script using Selenium WebDriver
2. Use the actual element IDs, names, and selectors from the HTML above
3. Include necessary imports (selenium, time, etc.)
4. Add explicit waits (WebDriverWait) instead of time.sleep where appropriate
5. Include assertions to verify expected results
6. Add comments explaining each major step
7. Use try-except for error handling where appropriate
8. The script should work with Chrome WebDriver
9. Include a main section to run the test
10. Open the HTML file directly (assume it's at './sample_project/checkout.html')

OUTPUT FORMAT:
Provide ONLY the Python code, no explanations before or after.
Use proper Python syntax and formatting.
Make the script immediately runnable.
"""
        return prompt
