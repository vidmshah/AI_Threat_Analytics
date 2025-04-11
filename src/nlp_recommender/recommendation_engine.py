import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy
import datetime

class ThreatMitigationRecommender:
    def __init__(self, knowledge_base_path="cicids_mitigations_kb.json"):
        """Initialize the recommendation engine with the knowledge base"""
        # Load knowledge base
        with open(knowledge_base_path, 'r') as f:
            self.knowledge_base = json.load(f)
        
        # Load NLP model
        self.nlp = spacy.load("en_core_web_md")  # Medium-sized model with word vectors
        
        # Create vectorizer for threat matching
        self.vectorizer = TfidfVectorizer(stop_words='english')
        
        # Prepare corpus for vectorization
        self.threat_types = list(self.knowledge_base.keys())
        corpus = [f"{threat_type} {self.knowledge_base[threat_type]['description']}" 
                 for threat_type in self.threat_types]
        
        # Fit vectorizer
        self.threat_vectors = self.vectorizer.fit_transform(corpus)
    
    def map_detection_to_threat_type(self, detection_result):
        """Map detection results to known threat types in the knowledge base"""
        # Extract relevant info from detection result
        # Assume detection_result is a dict with 'attack_type', 'confidence', etc.
        attack_type = detection_result.get('attack_type', '')
        description = detection_result.get('description', '')
        
        # Create a query string combining the attack type and description
        query = f"{attack_type} {description}"
        query_vector = self.vectorizer.transform([query])
        
        # Calculate similarity with known threat types
        similarities = cosine_similarity(query_vector, self.threat_vectors)[0]
        
        # Get the best match
        best_match_idx = np.argmax(similarities)
        best_match_score = similarities[best_match_idx]
        best_match_type = self.threat_types[best_match_idx]
        
        return {
            'matched_threat': best_match_type,
            'confidence': float(best_match_score),
            'original_detection': detection_result
        }
    
    def get_mitigations(self, threat_type, top_n=3):
        """Get the top N most effective mitigation strategies for a threat type"""
        if threat_type not in self.knowledge_base:
            return []
        
        # Get mitigations from knowledge base
        mitigations = self.knowledge_base[threat_type]['mitigations']
        
        # Sort by effectiveness
        sorted_mitigations = sorted(mitigations, key=lambda x: x['effectiveness'], reverse=True)
        
        # Return top N
        return sorted_mitigations[:top_n]
    
    def rank_mitigations_by_context(self, mitigations, context=None):
        """Rank mitigations considering the specific context"""
        if not context or not mitigations:
            return mitigations
        
        # Process context with spaCy
        context_doc = self.nlp(context)
        
        # Calculate relevance scores based on context
        scored_mitigations = []
        for mitigation in mitigations:
            # Create a combined text from mitigation information
            mitigation_text = f"{mitigation['strategy']} {mitigation['description']} " + \
                             " ".join(mitigation['steps'])
            mitigation_doc = self.nlp(mitigation_text)
            
            # Calculate semantic similarity between context and mitigation
            similarity = context_doc.similarity(mitigation_doc)
            
            # Adjust the base effectiveness with the context relevance
            adjusted_score = 0.7 * mitigation['effectiveness'] + 0.3 * similarity
            
            scored_mitigations.append({
                **mitigation,
                'context_relevance': float(similarity),
                'adjusted_score': float(adjusted_score)
            })
        
        # Sort by adjusted score
        return sorted(scored_mitigations, key=lambda x: x['adjusted_score'], reverse=True)
    
    def generate_recommendations(self, detection_result, context=None, max_recommendations=3):
        """Generate comprehensive mitigation recommendations based on detected threats"""
        # Map detection to threat type
        threat_mapping = self.map_detection_to_threat_type(detection_result)
        threat_type = threat_mapping['matched_threat']
        confidence = threat_mapping['confidence']
        
        # Get threat details
        threat_details = self.knowledge_base.get(threat_type, {})
        severity = threat_details.get('severity', 3)
        
        # Get and rank mitigations
        mitigations = self.get_mitigations(threat_type)
        if context:
            mitigations = self.rank_mitigations_by_context(mitigations, context)
        
        # Limit to max recommendations
        mitigations = mitigations[:max_recommendations]
        
        # Create recommendation object
        recommendation = {
            'timestamp': datetime.datetime.now().isoformat(),
            'threat_type': threat_type,
            'threat_description': threat_details.get('description', ''),
            'severity': severity,
            'detection_confidence': confidence,
            'original_detection': detection_result,
            'mitigations': mitigations
        }
        
        return recommendation
    
    def generate_report(self, recommendation):
        """Generate a human-readable report from the recommendation object"""
        threat_type = recommendation['threat_type']
        threat_desc = recommendation['threat_description']
        severity = recommendation['severity']
        confidence = recommendation['detection_confidence']
        mitigations = recommendation['mitigations']
        timestamp = recommendation['timestamp']
        
        # Create report header
        report = [
            f"THREAT MITIGATION REPORT",
            f"Generated: {timestamp}",
            f"",
            f"THREAT IDENTIFICATION",
            f"Type: {threat_type}",
            f"Severity: {severity}/5",
            f"Detection Confidence: {confidence:.2f}",
            f"Description: {threat_desc}",
            f""
        ]
        
        # Add mitigation strategies
        report.append(f"RECOMMENDED MITIGATION STRATEGIES")
        
        for i, mitigation in enumerate(mitigations, 1):
            report.extend([
                f"",
                f"Strategy {i}: {mitigation['strategy']}",
                f"Description: {mitigation['description']}",
                f"Implementation Difficulty: {mitigation['difficulty']}/5",
                f"Estimated Implementation Time: {mitigation['estimated_hours']} hours",
                f"Effectiveness Rating: {mitigation['effectiveness']:.2f}",
                f"",
                f"Implementation Steps:"
            ])
            
            for j, step in enumerate(mitigation['steps'], 1):
                report.append(f"  {j}. {step}")
            
            if 'context_relevance' in mitigation:
                report.append(f"")
                report.append(f"Context Relevance: {mitigation['context_relevance']:.2f}")
        
        # Add footer
        report.extend([
            f"",
            f"NOTE: This recommendation is based on automated analysis and should be reviewed by security personnel."
        ])
        
        return "\n".join(report)

# Example usage
if __name__ == "__main__":
    # Initialize recommender
    recommender = ThreatMitigationRecommender()
    
    # Example detection result
    detection = {
        'attack_type': 'DDoS',
        'confidence': 0.92,
        'source_ips': ['192.168.1.5', '10.0.0.3'],
        'target_ip': '172.16.0.10',
        'description': 'HTTP flood attack targeting web server',
        'timestamp': '2023-04-01T15:23:45'
    }
    
    # Example context (could be from system monitoring, user input, etc.)
    context = "Our web application is experiencing high traffic and slow response times. The system is hosted in AWS and protected by a basic firewall."
    
    # Generate recommendations
    recommendation = recommender.generate_recommendations(detection, context)
    
    # Generate report
    report = recommender.generate_report(recommendation)
    print(report)