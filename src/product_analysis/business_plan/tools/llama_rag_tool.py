from crewai_tools import BaseTool, SerperDevTool, ScrapeWebsiteTool
from typing import Dict, Optional
from dataclasses import dataclass, field
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import numpy as np
from pathlib import Path
import pandas as pd
from datetime import datetime
import torch
from transformers import AutoTokenizer, AutoModel
import os


@dataclass
class DynamicRAGTool(BaseTool):
    """Enhanced Dynamic RAG tool with semantic search capabilities"""
    
    name: str = field(default="Dynamic Research Tool")
    description: str = field(default="Enhanced tool for gathering real-time business intelligence and market data with semantic search")
    search_tool: SerperDevTool = field(default_factory=SerperDevTool)
    scrape_tool: ScrapeWebsiteTool = field(default_factory=ScrapeWebsiteTool)
    
    def __post_init__(self):
        """Initialize additional components after creation"""
        try:
            self.model_name = "sentence-transformers/all-mpnet-base-v2"
            self.embeddings = HuggingFaceEmbeddings(model_name=self.model_name)
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModel.from_pretrained(self.model_name)
            
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            
            self.industry_cache = {}
            print("Enhanced RAG components initialized successfully")
        except Exception as e:
            print(f"Warning: Enhanced components initialization failed: {str(e)}")
            self.embeddings = None
            self.model = None

    def _run(self, query: str, context: Optional[Dict] = None) -> str:
        """Enhanced run method with semantic search"""
        try:
            search_queries = self._generate_search_queries(query, context)
            
            all_results = []
            for search_query in search_queries:
                try:
                    search_result = self.search_tool(search_query)

                    if isinstance(search_result, dict):                
                        for item in search_result.get('organic', [])[:3]:
                            url = item.get('link')
                            if url:
                                try:
                                    content = self.scrape_tool(url)
                                    if content:
                                        if context and context.get('industry'):
                                            self._update_industry_cache(
                                                context['industry'],
                                                content
                                            )
                                        
                                        if self.embeddings and self.model:
                                            relevance = self._calculate_relevance(query, content)
                                            if relevance > 0.6:
                                                all_results.append({
                                                    'content': content,
                                                    'relevance': relevance
                                                })
                                        else:
                                            all_results.append({'content': content})
                                except Exception as e:
                                    continue
                
                except Exception as e:
                    continue

            if not all_results:
                return "Unable to find relevant information. Please try rephrasing the query."
                
            if all_results and 'relevance' in all_results[0]:
                all_results.sort(key=lambda x: x['relevance'], reverse=True)
            
            return self._format_results(all_results, query)
            
        except Exception as e:
            return f"Error during research: {str(e)}"

    def _generate_search_queries(self, query: str, context: Optional[Dict]) -> list:
        """Generate specific search queries based on the context"""
        if not context:
            return [query]

        industry = context.get('industry', '').strip()
        market = context.get('target_market', '').strip()
        scale = context.get('scale', '').strip()
        
        base_queries = []
        
        # Market Analysis Queries
        if "market" in query.lower():
            base_queries.extend([
                f"{industry} industry market size {scale} scale current data",
                f"{industry} market growth rate {market} latest statistics",
                f"{industry} industry trends {market} analysis {datetime.now().year}",
                f"{industry} market opportunities {scale} business current"
            ])
            
        # Competitor Analysis Queries
        elif "competitor" in query.lower():
            base_queries.extend([
                f"leading competitors {industry} industry {market} current",
                f"market share analysis {industry} {scale} business",
                f"{industry} competitive landscape {market} latest",
                f"{industry} market leaders strategy analysis"
            ])
            
        # Financial Analysis Queries
        elif "financial" in query.lower():
            base_queries.extend([
                f"{industry} business financial metrics {scale} current",
                f"{industry} startup costs analysis {scale}",
                f"{industry} revenue models {market} analysis",
                f"{industry} profitability benchmarks current"
            ])
            
        # General Business Queries
        else:
            base_queries.extend([
                f"{query} {industry} industry latest",
                f"{query} {market} market current analysis",
                f"{query} {scale} business research"
            ])
        
        return base_queries

    def _calculate_relevance(self, query: str, content: str) -> float:
        """Calculate semantic relevance between query and content"""
        try:
            # Tokenize and get embeddings
            query_inputs = self.tokenizer(query, return_tensors="pt", padding=True, truncation=True)
            content_inputs = self.tokenizer(content, return_tensors="pt", padding=True, truncation=True)
            
            with torch.no_grad():
                query_outputs = self.model(**query_inputs)
                content_outputs = self.model(**content_inputs)
                
            query_embedding = query_outputs.last_hidden_state.mean(dim=1)
            content_embedding = content_outputs.last_hidden_state.mean(dim=1)
            
            # Calculate cosine similarity
            similarity = torch.nn.functional.cosine_similarity(
                query_embedding, content_embedding
            )
            
            return float(similarity[0])
        except Exception as e:
            print(f"Error calculating relevance: {str(e)}")
            return 0.0

    def _update_industry_cache(self, industry: str, content: str):
        """Update industry-specific cache"""
        if industry not in self.industry_cache:
            self.industry_cache[industry] = []
            
        self.industry_cache[industry].append({
            'content': content,
            'timestamp': datetime.now()
        })
        
        # Keep only recent entries (last 24 hours)
        self.industry_cache[industry] = [
            entry for entry in self.industry_cache[industry]
            if (datetime.now() - entry['timestamp']).days < 1
        ]

    def _format_results(self, results: list, query: str) -> str:
        """Format research results into structured output"""
        if not results:
            return "No relevant information found."
            
        # Categorize information
        categories = {
            'market_data': [],
            'trends': [],
            'competitors': [],
            'insights': []
        }
        
        for result in results:
            content = result['content']
            
            # Categorize based on content
            if any(term in content.lower() for term in ['market size', 'market share', 'market value']):
                categories['market_data'].append(content)
            elif any(term in content.lower() for term in ['trend', 'growth', 'development']):
                categories['trends'].append(content)
            elif any(term in content.lower() for term in ['competitor', 'competition', 'player']):
                categories['competitors'].append(content)
            else:
                categories['insights'].append(content)
        
        # Format output
        output = []
        for category, items in categories.items():
            if items:
                output.append(f"\n### {category.replace('_', ' ').title()}")
                output.extend([f"- {item[:500]}..." if len(item) > 500 else f"- {item}" 
                             for item in items[:3]])
        
        return "\n".join(output)

    def _clean_text(self, text: str) -> str:
        """Clean and normalize text content"""
        # Remove extra whitespace
        text = ' '.join(text.split())
        # Remove special characters
        text = ''.join(char for char in text if char.isalnum() or char.isspace() or char in '.,!?-')
        return text.strip()