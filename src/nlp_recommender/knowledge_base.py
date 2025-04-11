import pandas as pd
import json

# Define the knowledge base structure for CICIDS2018 dataset threats
# The CICIDS2018 dataset includes various attack types like DoS, DDoS, Brute Force, XSS, SQL Injection, etc.

cicids_mitigations = {
    "DoS / DDoS": {
        "description": "Denial of Service or Distributed Denial of Service attacks that aim to make a network resource unavailable.",
        "severity": 4,
        "mitigations": [
            {
                "strategy": "Traffic filtering and rate limiting",
                "description": "Implement traffic filtering and rate limiting at network boundaries.",
                "steps": [
                    "Configure firewall rules to filter known malicious traffic patterns",
                    "Implement rate limiting for incoming requests",
                    "Deploy anti-DDoS solutions at network edge",
                    "Configure SYN flood protection mechanisms"
                ],
                "difficulty": 3,
                "estimated_hours": 16,
                "effectiveness": 0.85
            },
            {
                "strategy": "Traffic distribution",
                "description": "Distribute traffic across multiple servers to minimize impact.",
                "steps": [
                    "Implement load balancing across multiple servers",
                    "Configure auto-scaling for critical services",
                    "Use content delivery networks (CDNs) to absorb traffic",
                    "Set up anycast network addressing"
                ],
                "difficulty": 4,
                "estimated_hours": 24,
                "effectiveness": 0.9
            },
            {
                "strategy": "Traffic analysis and anomaly detection",
                "description": "Continuously monitor traffic patterns to identify and respond to anomalies.",
                "steps": [
                    "Deploy network monitoring tools to establish baseline traffic patterns",
                    "Configure automated alerts for traffic anomalies",
                    "Implement traffic analysis to distinguish legitimate from attack traffic",
                    "Create incident response playbooks for DoS/DDoS scenarios"
                ],
                "difficulty": 3,
                "estimated_hours": 20,
                "effectiveness": 0.8
            }
        ]
    },
    "Port Scan": {
        "description": "Reconnaissance attacks that probe network ports to discover services running on a system.",
        "severity": 2,
        "mitigations": [
            {
                "strategy": "Firewall configuration",
                "description": "Configure firewalls to limit exposed ports and detect scanning activities.",
                "steps": [
                    "Implement default-deny firewall policies",
                    "Close all unnecessary ports on public-facing systems",
                    "Configure port scan detection on firewalls and IDS",
                    "Implement connection rate limiting"
                ],
                "difficulty": 2,
                "estimated_hours": 8,
                "effectiveness": 0.9
            },
            {
                "strategy": "Network segmentation",
                "description": "Segment networks to limit lateral movement following successful scans.",
                "steps": [
                    "Implement network segmentation with VLANs or subnets",
                    "Deploy internal firewalls between network segments",
                    "Use private VLANs for sensitive systems",
                    "Implement zero-trust network principles"
                ],
                "difficulty": 4,
                "estimated_hours": 40,
                "effectiveness": 0.95
            }
        ]
    },
    "Brute Force": {
        "description": "Attacks that attempt to guess passwords or encryption keys through exhaustive trials.",
        "severity": 3,
        "mitigations": [
            {
                "strategy": "Account lockout policies",
                "description": "Implement account lockout after multiple failed authentication attempts.",
                "steps": [
                    "Configure account lockout after 5-10 failed attempts",
                    "Implement progressive delays between authentication attempts",
                    "Set up alerts for multiple failed login attempts",
                    "Create an account recovery process for legitimate lockouts"
                ],
                "difficulty": 1,
                "estimated_hours": 4,
                "effectiveness": 0.85
            },
            {
                "strategy": "Multi-factor authentication",
                "description": "Require additional authentication factors beyond passwords.",
                "steps": [
                    "Deploy MFA solutions for all critical systems and accounts",
                    "Require MFA for administrative access",
                    "Implement app-based or hardware token authentication",
                    "Create backup authentication methods for emergency access"
                ],
                "difficulty": 3,
                "estimated_hours": 20,
                "effectiveness": 0.95
            },
            {
                "strategy": "Password policy enforcement",
                "description": "Enforce strong password policies to resist brute force attacks.",
                "steps": [
                    "Implement minimum password complexity requirements",
                    "Check passwords against common password lists",
                    "Require regular password rotation for sensitive accounts",
                    "Consider implementing passwordless authentication"
                ],
                "difficulty": 2,
                "estimated_hours": 8,
                "effectiveness": 0.75
            }
        ]
    },
    "Web Attack": {
        "description": "Attacks targeting web applications, including SQL Injection, XSS, and other OWASP Top 10 vulnerabilities.",
        "severity": 4,
        "mitigations": [
            {
                "strategy": "Input validation and sanitization",
                "description": "Validate and sanitize all user inputs to prevent injection attacks.",
                "steps": [
                    "Implement server-side input validation for all user-submitted data",
                    "Use parameterized queries for database interactions",
                    "Sanitize output to prevent XSS attacks",
                    "Implement content security policies (CSP)"
                ],
                "difficulty": 3,
                "estimated_hours": 24,
                "effectiveness": 0.9
            },
            {
                "strategy": "Web Application Firewall",
                "description": "Deploy a WAF to filter malicious web traffic.",
                "steps": [
                    "Deploy WAF in front of web applications",
                    "Configure WAF rules to block common attack patterns",
                    "Regularly update WAF rules based on new threats",
                    "Monitor WAF logs for potential attacks"
                ],
                "difficulty": 3,
                "estimated_hours": 16,
                "effectiveness": 0.85
            },
            {
                "strategy": "Regular security testing",
                "description": "Conduct regular security testing to identify and remediate vulnerabilities.",
                "steps": [
                    "Perform regular automated vulnerability scanning",
                    "Conduct manual penetration testing annually",
                    "Implement security code reviews in development process",
                    "Test for OWASP Top 10 vulnerabilities"
                ],
                "difficulty": 4,
                "estimated_hours": 40,
                "effectiveness": 0.9
            }
        ]
    },
    "Botnet": {
        "description": "Networks of compromised devices controlled by attackers for various malicious purposes.",
        "severity": 4,
        "mitigations": [
            {
                "strategy": "Network behavior analysis",
                "description": "Monitor network traffic for suspicious behavior indicative of botnet activity.",
                "steps": [
                    "Deploy network monitoring tools to detect unusual communication patterns",
                    "Establish baselines for normal network behavior",
                    "Configure alerts for suspicious outbound connections",
                    "Monitor for traffic to known command and control servers"
                ],
                "difficulty": 3,
                "estimated_hours": 20,
                "effectiveness": 0.8
            },
            {
                "strategy": "Endpoint protection",
                "description": "Deploy comprehensive endpoint protection to prevent device compromise.",
                "steps": [
                    "Install and maintain up-to-date antivirus/anti-malware solutions",
                    "Implement application whitelisting where appropriate",
                    "Deploy endpoint detection and response (EDR) solutions",
                    "Regularly update and patch all devices"
                ],
                "difficulty": 3,
                "estimated_hours": 24,
                "effectiveness": 0.85
            },
            {
                "strategy": "Network segmentation",
                "description": "Segment networks to limit the spread and impact of botnet infections.",
                "steps": [
                    "Implement network segmentation to isolate critical systems",
                    "Deploy internal firewalls between network segments",
                    "Configure access control lists to limit lateral movement",
                    "Consider implementing a zero-trust architecture"
                ],
                "difficulty": 4,
                "estimated_hours": 40,
                "effectiveness": 0.9
            }
        ]
    },
    "Infiltration": {
        "description": "Attacks that attempt to penetrate a network and establish a presence within it.",
        "severity": 5,
        "mitigations": [
            {
                "strategy": "Defense in depth",
                "description": "Implement multiple layers of security controls to protect against infiltration.",
                "steps": [
                    "Deploy firewalls at network perimeters and between segments",
                    "Implement intrusion detection/prevention systems",
                    "Configure email security gateways with attachment scanning",
                    "Deploy web proxies with URL filtering"
                ],
                "difficulty": 4,
                "estimated_hours": 40,
                "effectiveness": 0.85
            },
            {
                "strategy": "Least privilege principle",
                "description": "Grant minimal access rights required for users to perform their duties.",
                "steps": [
                    "Review and revise user access permissions regularly",
                    "Implement role-based access control",
                    "Remove administrative rights from standard user accounts",
                    "Use just-in-time access for administrative functions"
                ],
                "difficulty": 3,
                "estimated_hours": 24,
                "effectiveness": 0.9
            },
            {
                "strategy": "Security awareness training",
                "description": "Train users to recognize and avoid security threats.",
                "steps": [
                    "Conduct regular security awareness training for all users",
                    "Perform simulated phishing exercises",
                    "Create clear procedures for reporting suspicious activities",
                    "Develop specific training for high-risk user groups"
                ],
                "difficulty": 2,
                "estimated_hours": 16,
                "effectiveness": 0.75
            }
        ]
    }
}

# Function to save the knowledge base
def save_knowledge_base(kb, filename="cicids_mitigations_kb.json"):
    with open(filename, 'w') as f:
        json.dump(kb, f, indent=4)
    print(f"Knowledge base saved to {filename}")

# Function to load the knowledge base
def load_knowledge_base(filename="cicids_mitigations_kb.json"):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Knowledge base file {filename} not found")
        return None

if __name__ == "__main__":
    # Save the knowledge base
    save_knowledge_base(cicids_mitigations)
    
    # Example of loading and accessing the knowledge base
    kb = load_knowledge_base()
    if kb:
        # Example: Print all mitigation strategies for DoS/DDoS attacks
        dos_mitigations = kb.get("DoS / DDoS", {}).get("mitigations", [])
        print(f"Found {len(dos_mitigations)} mitigation strategies for DoS/DDoS attacks:")
        for i, mitigation in enumerate(dos_mitigations, 1):
            print(f"{i}. {mitigation['strategy']}: {mitigation['description']}")