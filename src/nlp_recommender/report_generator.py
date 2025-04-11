import json
import datetime
import random
from jinja2 import Template

class NLGReportGenerator:
    def __init__(self):
        """Initialize the NLG report generator with templates"""
        # Load templates for different severity levels and contexts
        self.templates = self._initialize_templates()
        
        # Load transition phrases and sentence starters
        self.transitions = {
            "recommendations": [
                "Based on our analysis, we recommend the following actions:",
                "To mitigate this threat, consider implementing these strategies:",
                "Our system suggests the following countermeasures:",
                "To address this security issue, we advise taking these steps:",
                "The following mitigation strategies are recommended:"
            ],
            "urgency": [
                "Immediate action is required to prevent potential data loss.",
                "This threat requires urgent attention to minimize risk exposure.",
                "Prompt implementation of these measures is strongly advised.",
                "To reduce the risk of compromise, act on these recommendations as soon as possible.",
                "This situation calls for immediate security response."
            ],
            "low_urgency": [
                "While not critical, addressing these recommendations will improve your security posture.",
                "These measures should be implemented as part of routine security maintenance.",
                "Consider scheduling these improvements in your next maintenance window.",
                "These recommendations should be addressed in a timely but non-urgent manner.",
                "Implementation of these measures will provide additional security layers."
            ]
        }
        
        # Additional contextual phrases
        self.contextual_phrases = {
            "web_servers": [
                "Your web infrastructure may be vulnerable to this attack vector.",
                "Web servers exposed to the internet are particularly at risk.",
                "This threat primarily targets web-facing applications and services.",
                "Consider implementing additional protections for your web servers."
            ],
            "databases": [
                "Database systems should be specifically hardened against this threat.",
                "Data exfiltration is a primary risk with this attack pattern.",
                "Consider implementing additional database access controls and monitoring.",
                "This attack pattern often targets stored procedures and database queries."
            ],
            "network": [
                "Network infrastructure is the primary target of this attack.",
                "Consider implementing additional network segmentation to contain this threat.",
                "Network monitoring should be enhanced to detect similar attacks in the future.",
                "Traffic analysis and filtering are key defenses against this threat pattern."
            ]
        }
    
    def _initialize_templates(self):
        """Initialize Jinja2 templates for report generation"""
        templates = {
            "high_severity": Template("""
# URGENT SECURITY ALERT: {{ threat_type }}

**Severity: {{ severity }}/5 (HIGH)** | **Confidence: {{ confidence_pct }}%**
**Detected: {{ timestamp }}**

## Threat Description
{{ threat_description }}

{% if context_analysis %}
## Situational Context
{{ context_analysis }}
{% endif %}

## Recommended Immediate Actions
{{ urgency_statement }}

{% for mitigation in mitigations %}
### Strategy {{ loop.index }}: {{ mitigation.strategy }}
{{ mitigation.description }}

**Implementation Steps:**
{% for step in mitigation.steps %}
{{ loop.index }}. {{ step }}
{% endfor %}

**Resource Requirements:**
- Difficulty: {{ mitigation.difficulty }}/5
- Estimated time: {{ mitigation.estimated_hours }} hours
{% if mitigation.context_relevance %}
- Relevance to your environment: {{ mitigation_relevance(mitigation.context_relevance) }}
{% endif %}

{% endfor %}

## Additional Considerations
{{ additional_considerations }}

This alert requires immediate attention. Please escalate to your security team.
            """),
            
            "medium_severity": Template("""
# Security Alert: {{ threat_type }}

**Severity: {{ severity }}/5 (MEDIUM)** | **Confidence: {{ confidence_pct }}%**
**Detected: {{ timestamp }}**

## Threat Description
{{ threat_description }}

{% if context_analysis %}
## Situational Context
{{ context_analysis }}
{% endif %}

## Recommended Actions
{{ recommendations_intro }}

{% for mitigation in mitigations %}
### Strategy {{ loop.index }}: {{ mitigation.strategy }}
{{ mitigation.description }}

**Implementation Steps:**
{% for step in mitigation.steps %}
{{ loop.index }}. {{ step }}
{% endfor %}

**Resource Requirements:**
- Difficulty: {{ mitigation.difficulty }}/5
- Estimated time: {{ mitigation.estimated_hours }} hours
{% if mitigation.context_relevance %}
- Relevance to your environment: {{ mitigation_relevance(mitigation.context_relevance) }}
{% endif %}

{% endfor %}

## Additional Considerations
{{ additional_considerations }}

Please review and implement these recommendations according to your security policies.
            """),
            
            "low_severity": Template("""
# Security Notification: {{ threat_type }}

**Severity: {{ severity }}/5 (LOW)** | **Confidence: {{ confidence_pct }}%**
**Detected: {{ timestamp }}**

## Threat Description
{{ threat_description }}

{% if context_analysis %}
## Situational Context
{{ context_analysis }}
{% endif %}

## Suggested Actions
{{ low_urgency_statement }}

{% for mitigation in mitigations %}
### Strategy {{ loop.index }}: {{ mitigation.strategy }}
{{ mitigation.description }}

**Implementation Steps:**
{% for step in mitigation.steps %}
{{ loop.index }}. {{ step }}
{% endfor %}

**Resource Requirements:**
- Difficulty: {{ mitigation.difficulty }}/5
- Estimated time: {{ mitigation.estimated_hours }} hours
{% if mitigation.context_relevance %}
- Relevance to your environment: {{ mitigation_relevance(mitigation.context_relevance) }}
{% endif %}

{% endfor %}

## Additional Considerations
{{ additional_considerations }}

These recommendations can be implemented as part of regular security maintenance.
            """)
        }
        return templates
    
    def analyze_context(self, threat_type, context=None):
        """Generate contextual analysis based on the threat type and context"""
        if not context:
            return None
            
        # Determine which contextual phrases to use based on threat type and context
        context_lower = context.lower()
        relevant_contexts = []
        
        if any(term in context_lower for term in ["web", "http", "server", "application"]):
            relevant_contexts.append("web_servers")
        
        if any(term in context_lower for term in ["database", "sql", "data", "records"]):
            relevant_contexts.append("databases")
            
        if any(term in context_lower for term in ["network", "traffic", "packet", "router", "switch"]):
            relevant_contexts.append("network")
            
        # Generate contextual analysis
        analysis_parts = []
        
        # Add context-specific phrases
        for context_type in relevant_contexts:
            if context_type in self.contextual_phrases:
                analysis_parts.append(random.choice(self.contextual_phrases[context_type]))
        
        # If we have context parts, join them and return
        if analysis_parts:
            return " ".join(analysis_parts)
        else:
            return None
    
    def generate_additional_considerations(self, threat_type, severity):
        """Generate additional considerations based on threat type and severity"""
        considerations = []
        
        # General considerations
        general = [
            "Regular security assessments can help identify similar vulnerabilities before they are exploited.",
            "Employee security awareness training can reduce the risk of successful attacks.",
            "Ensure all systems are kept up-to-date with the latest security patches.",
            "Document all incident response actions for future reference and compliance purposes."
        ]
        
        # Add a general consideration
        considerations.append(random.choice(general))
        
        # Add threat-specific considerations
        if "DoS" in threat_type or "DDoS" in threat_type:
            considerations.append("Consider implementing a DDoS protection service if these attacks are frequent.")
        
        elif "Brute Force" in threat_type:
            considerations.append("Implementing multi-factor authentication would significantly reduce the risk of successful brute force attacks.")
        
        elif "Web Attack" in threat_type:
            considerations.append("Regular web application security testing can identify and remediate vulnerabilities before they are exploited.")
        
        elif "Botnet" in threat_type:
            considerations.append("Ensure all IoT devices and endpoints are regularly patched to prevent them from being recruited into botnets.")
        
        # Add severity-specific considerations
        if severity >= 4:
            considerations.append("Consider engaging with external security experts to assist with remediation of this high-severity issue.")
        
        # Return combined considerations
        return " ".join(considerations)
    
    def format_mitigation_relevance(self, relevance_score):
        """Format the relevance score as a human-readable string"""
        if relevance_score >= 0.8:
            return "Highly relevant"
        elif relevance_score >= 0.6:
            return "Relevant"
        elif relevance_score >= 0.4:
            return "Moderately relevant"
        else:
            return "Generally applicable"
    
    def generate_report(self, recommendation, context=None):
        """Generate a natural language report from the recommendation object"""
        # Extract key information
        threat_type = recommendation['threat_type']
        threat_desc = recommendation['threat_description']
        severity = recommendation['severity']
        confidence = recommendation['detection_confidence']
        mitigations = recommendation['mitigations']
        timestamp = datetime.datetime.fromisoformat(recommendation['timestamp']).strftime("%Y-%m-%d %H:%M:%S")
        
        # Select template based on severity
        if severity >= 4:
            template = self.templates["high_severity"]
        elif severity >= 2:
            template = self.templates["medium_severity"]
        else:
            template = self.templates["low_severity"]
        
        # Generate contextual analysis if context is provided
        context_analysis = self.analyze_context(threat_type, context) if context else None
        
        # Select appropriate phrases based on severity
        if severity >= 4:
            urgency_statement = random.choice(self.transitions["urgency"])
            recommendations_intro = random.choice(self.transitions["recommendations"])
            low_urgency_statement = None
        elif severity >= 2:
            urgency_statement = None
            recommendations_intro = random.choice(self.transitions["recommendations"])
            low_urgency_statement = None
        else:
            urgency_statement = None
            recommendations_intro = None
            low_urgency_statement = random.choice(self.transitions["low_urgency"])
        
        # Generate additional considerations
        additional_considerations = self.generate_additional_considerations(threat_type, severity)
        
        # Render template with all the information
        report = template.render(
            threat_type=threat_type,
            threat_description=threat_desc,
            severity=severity,
            confidence_pct=int(confidence * 100),
            timestamp=timestamp,
            mitigations=mitigations,
            context_analysis=context_analysis,
            urgency_statement=urgency_statement,
            recommendations_intro=recommendations_intro,
            low_urgency_statement=low_urgency_statement,
            additional_considerations=additional_considerations,
            mitigation_relevance=self.format_mitigation_relevance
        )
        
        return report

    def save_report(self, report, filename=None):
        """Save the generated report to a file"""
        if not filename:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"security_report_{timestamp}.md"
        
        with open(filename, 'w') as f:
            f.write(report)
        
        return filename

# Example usage
if __name__ == "__main__":
    # Initialize report generator
    report_generator = NLGReportGenerator()
    
    # Example recommendation object
    recommendation = {
        'timestamp': datetime.datetime.now().isoformat(),
        'threat_type': 'DoS / DDoS Attack',
        'threat_description': 'Our systems detected a distributed denial of service attack targeting your web infrastructure. The attack originated from multiple IP addresses across different geographic regions, suggesting a coordinated botnet attack. The attack pattern shows characteristics of a SYN flood combined with application layer (Layer 7) requests designed to exhaust server resources.',
        'severity': 4,
        'detection_confidence': 0.92,
        'mitigations': [
            {
                'strategy': 'Traffic Filtering',
                'description': 'Implement immediate traffic filtering at the network edge to mitigate the attack.',
                'steps': [
                    'Configure your firewall or WAF to block traffic from the attacking IP ranges.',
                    'Implement rate limiting for HTTP requests from single IP addresses.',
                    'Enable SYN cookies on all edge devices to mitigate SYN flood attacks.',
                    'Consider temporarily enabling captcha or challenge-response mechanisms for all users.'
                ],
                'difficulty': 3,
                'estimated_hours': 4,
                'context_relevance': 0.9
            },
            {
                'strategy': 'Scale Infrastructure',
                'description': 'Temporarily increase capacity to absorb the attack traffic while implementing filtering measures.',
                'steps': [
                    'Activate cloud-based auto-scaling for affected services if available.',
                    'Enable any available DDoS protection services from your hosting or CDN provider.',
                    'Consider temporarily routing traffic through a dedicated DDoS protection service.',
                    'Monitor system resources closely during scaling to prevent cost overruns.'
                ],
                'difficulty': 2,
                'estimated_hours': 2,
                'context_relevance': 0.8
            },
            {
                'strategy': 'Forensic Analysis',
                'description': 'Analyze attack patterns to improve future defenses while mitigating the current attack.',
                'steps': [
                    'Capture network traffic samples for later analysis.',
                    'Document attack signatures and patterns to create custom detection rules.',
                    'Identify potentially compromised systems that may be part of the attack.',
                    'Report attacking IP addresses to relevant ISPs and security organizations.'
                ],
                'difficulty': 4,
                'estimated_hours': 8,
                'context_relevance': 0.7
            }
        ]
    }
    
    # Provide context information
    context = "The attack is targeting our primary e-commerce web servers and has caused intermittent service disruptions. Our network monitoring shows unusual traffic patterns on ports 80 and 443."
    
    # Generate the report
    report = report_generator.generate_report(recommendation, context)
    
    # Save the report to a file (optional)
    filename = report_generator.save_report(report)
    
    # Print the report
    print(f"Report generated and saved to {filename}")
    print("\nReport Preview:")
    print("-" * 80)
    print(report[:500] + "...")
    print("-" * 80)
    
    # Example of generating different severity level reports
    
    # Medium severity example
    medium_recommendation = recommendation.copy()
    medium_recommendation['severity'] = 3
    medium_recommendation['threat_type'] = 'Brute Force Authentication Attack'
    medium_recommendation['threat_description'] = 'We detected multiple failed login attempts on your administrative interface from several IP addresses. The pattern suggests a distributed brute force attack attempting to compromise administrator accounts.'
    
    medium_context = "The attack is targeting our admin login portal. Our logs show repeated login attempts with different username variations."
    
    medium_report = report_generator.generate_report(medium_recommendation, medium_context)
    medium_filename = report_generator.save_report(medium_report, "medium_severity_report.md")
    
    # Low severity example
    low_recommendation = recommendation.copy()
    low_recommendation['severity'] = 1
    low_recommendation['threat_type'] = 'Outdated SSL Certificate'
    low_recommendation['threat_description'] = 'Our system detected that the SSL certificate for your secondary domain is approaching its expiration date. This could lead to security warnings for users if not addressed.'
    
    low_context = "The certificate expires in 14 days and is used on our documentation portal which receives moderate traffic."
    
    low_report = report_generator.generate_report(low_recommendation, low_context)
    low_filename = report_generator.save_report(low_report, "low_severity_report.md")