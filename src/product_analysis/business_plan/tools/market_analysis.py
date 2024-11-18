from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from typing import Dict, List, Tuple
import json
import concurrent.futures

class MarketAnalysisPipeline:
    """Advanced market analysis pipeline using NLP and ML techniques"""
    
    def __init__(self):
        self.sentiment_model = pipeline("sentiment-analysis")
        self.similarity_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    
        self.sector_tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
        self.sector_model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
        
        self.trend_keywords = {
            'growth': ['expanding', 'growing', 'rising', 'increasing', 'booming'],
            'decline': ['shrinking', 'declining', 'decreasing', 'falling', 'struggling'],
            'innovation': ['innovative', 'breakthrough', 'revolutionary', 'disrupting', 'cutting-edge'],
            'competition': ['competitive', 'saturated', 'crowded', 'consolidated', 'fragmented']
        }
        
    def analyze_market_data(self, business_plan: Dict) -> Dict:
        """Perform comprehensive market analysis on business plan"""
        market_section = ' '.join(business_plan.get("market_analysis", {}).get("content", []))
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_sentiment = executor.submit(self._analyze_sentiment, market_section)
            future_trends = executor.submit(self._identify_market_trends, market_section)
            future_opportunities = executor.submit(self._extract_opportunities, market_section)
            future_risks = executor.submit(self._analyze_market_risks, market_section)
            
            sentiment_results = future_sentiment.result()
            trend_results = future_trends.result()
            opportunity_results = future_opportunities.result()
            risk_results = future_risks.result()
        
        return {
            "market_sentiment": sentiment_results,
            "identified_trends": trend_results,
            "opportunities": opportunity_results,
            "risks": risk_results,
            "confidence_score": self._calculate_confidence_score([
                sentiment_results, trend_results, opportunity_results, risk_results
            ])
        }
    
    def _analyze_sentiment(self, text: str) -> Dict:
        """Analyze market sentiment with confidence scores"""
        try:
            sentiment_results = self.sentiment_model(text[:512])
            return {
                "sentiment": sentiment_results[0]['label'],
                "confidence": round(sentiment_results[0]['score'], 3),
                "interpretation": self._interpret_sentiment(sentiment_results[0])
            }
        except Exception as e:
            print(f"Sentiment analysis failed: {str(e)}")
            return {"sentiment": "NEUTRAL", "confidence": 0.0}
    
    def _identify_market_trends(self, text: str) -> List[Dict]:
        """Extract and analyze market trends"""
        trends = []
        
        text_embedding = self.similarity_model.encode(text)
        
        for trend_type, keywords in self.trend_keywords.items():
            keyword_embeddings = self.similarity_model.encode(keywords)
            
            similarities = cosine_similarity(
                [text_embedding],
                keyword_embeddings
            )[0]
            
            if max(similarities) > 0.6:
                trends.append({
                    "type": trend_type,
                    "confidence": round(float(max(similarities)), 3),
                    "keywords": [keywords[i] for i in range(len(similarities)) if similarities[i] > 0.6]
                })
        
        return sorted(trends, key=lambda x: x['confidence'], reverse=True)
    
    def _extract_opportunities(self, text: str) -> List[Dict]:
        """Extract market opportunities using NLP"""
        opportunities = []
        
        opportunity_indicators = [
            "opportunity", "potential", "growth", "emerging",
            "untapped", "promising", "innovative"
        ]
        
        sentences = text.split('.')
        for sentence in sentences:
            if any(indicator in sentence.lower() for indicator in opportunity_indicators):
                confidence = sum(1 for ind in opportunity_indicators if ind in sentence.lower()) / len(opportunity_indicators)
                
                opportunities.append({
                    "description": sentence.strip(),
                    "confidence": round(confidence, 3),
                    "keywords": [ind for ind in opportunity_indicators if ind in sentence.lower()]
                })
        
        return sorted(opportunities, key=lambda x: x['confidence'], reverse=True)[:5]
    
    def _analyze_market_risks(self, text: str) -> List[Dict]:
        """Analyze potential market risks"""
        risks = []
        
        risk_indicators = [
            "risk", "challenge", "threat", "competition",
            "regulatory", "uncertainty", "barrier"
        ]
        
        sentences = text.split('.')
        for sentence in sentences:
            if any(indicator in sentence.lower() for indicator in risk_indicators):
                confidence = sum(1 for ind in risk_indicators if ind in sentence.lower()) / len(risk_indicators)
                
                risks.append({
                    "description": sentence.strip(),
                    "confidence": round(confidence, 3),
                    "risk_type": self._classify_risk_type(sentence)
                })
        
        return sorted(risks, key=lambda x: x['confidence'], reverse=True)[:5]
    
    def _classify_risk_type(self, text: str) -> str:
        """Classify type of risk using FinBERT"""
        try:
            inputs = self.sector_tokenizer(text, return_tensors="pt", padding=True, truncation=True)
            outputs = self.sector_model(**inputs)
            
            predicted_class = outputs.logits.argmax().item()
            risk_types = ['operational', 'financial', 'regulatory', 'market', 'technology']
            return risk_types[predicted_class % len(risk_types)]
        except Exception as e:
            return "unclassified"
    
    def _interpret_sentiment(self, sentiment_result: Dict) -> str:
        """Interpret sentiment analysis results"""
        label = sentiment_result['label']
        score = sentiment_result['score']
        
        if label == 'POSITIVE' and score > 0.8:
            return "Strong positive market outlook"
        elif label == 'POSITIVE':
            return "Moderately positive market conditions"
        elif label == 'NEGATIVE' and score > 0.8:
            return "Significant market challenges"
        elif label == 'NEGATIVE':
            return "Some market concerns"
        else:
            return "Neutral market conditions"
    
    def _calculate_confidence_score(self, analyses: List) -> float:
        """Calculate overall confidence score for the analysis"""
        confidence_scores = []
        
        for analysis in analyses:
            if isinstance(analysis, dict) and 'confidence' in analysis:
                confidence_scores.append(analysis['confidence'])
            elif isinstance(analysis, list) and analysis:
                conf_values = [item.get('confidence', 0) for item in analysis if isinstance(item, dict)]
                if conf_values:
                    confidence_scores.append(sum(conf_values) / len(conf_values))
        
        return round(sum(confidence_scores) / len(confidence_scores), 3) if confidence_scores else 0.0