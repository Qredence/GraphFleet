# Security Guide

This guide covers security best practices, configurations, and considerations for GraphFleet deployments.

## Authentication & Authorization

### 1. JWT Authentication

```python
# Configure JWT settings
GRAPHFLEET_JWT_SECRET=your-secret-key
GRAPHFLEET_JWT_ALGORITHM=HS256
GRAPHFLEET_JWT_EXPIRATION=3600  # 1 hour
```

Example JWT implementation:
```python
from graphfleet.security import create_jwt_token

# Create token
token = create_jwt_token(
    user_id="user123",
    scopes=["read:documents", "write:documents"]
)

# Verify token
from graphfleet.security import verify_jwt_token
user = verify_jwt_token(token)
```

### 2. OAuth2 Integration

```python
# Configure OAuth providers
GRAPHFLEET_OAUTH_PROVIDERS = {
    "github": {
        "client_id": "your-client-id",
        "client_secret": "your-client-secret",
        "redirect_uri": "https://api.graphfleet.ai/auth/github/callback"
    },
    "google": {
        "client_id": "your-client-id",
        "client_secret": "your-client-secret",
        "redirect_uri": "https://api.graphfleet.ai/auth/google/callback"
    }
}
```

### 3. Role-Based Access Control (RBAC)

```python
# Define roles and permissions
GRAPHFLEET_ROLES = {
    "admin": ["*"],
    "editor": [
        "read:documents",
        "write:documents",
        "read:graphs",
        "write:graphs"
    ],
    "viewer": [
        "read:documents",
        "read:graphs"
    ]
}

# Check permissions
from graphfleet.security import requires_permission

@requires_permission("write:documents")
def create_document(document_data):
    # Implementation
    pass
```

## Data Security

### 1. Encryption at Rest

```python
# Configure encryption
GRAPHFLEET_ENCRYPTION = {
    "algorithm": "AES-256-GCM",
    "key_management": "aws-kms",
    "kms_key_id": "your-kms-key-id"
}

# Example usage
from graphfleet.security import encrypt_data, decrypt_data

# Encrypt sensitive data
encrypted = encrypt_data(sensitive_data)

# Decrypt when needed
decrypted = decrypt_data(encrypted)
```

### 2. Network Security

```nginx
# Nginx SSL configuration
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
ssl_prefer_server_ciphers off;
ssl_session_tickets off;
ssl_session_timeout 1d;
ssl_session_cache shared:SSL:50m;
add_header Strict-Transport-Security "max-age=63072000" always;
```

### 3. API Security

```python
# Configure API security settings
GRAPHFLEET_API_SECURITY = {
    "rate_limit": {
        "default": "1000/hour",
        "authenticated": "10000/hour"
    },
    "cors": {
        "allow_origins": ["https://app.graphfleet.ai"],
        "allow_methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Authorization", "Content-Type"]
    }
}
```

## Audit Logging

### 1. Security Events

```python
# Configure audit logging
GRAPHFLEET_AUDIT = {
    "enabled": True,
    "storage": "elasticsearch",
    "retention_days": 90
}

# Example audit log
from graphfleet.security import audit_log

audit_log.security_event(
    event_type="user.login",
    user_id="user123",
    ip_address="192.168.1.1",
    success=True
)
```

### 2. Data Access Logging

```python
# Log data access
audit_log.data_access(
    action="document.read",
    user_id="user123",
    resource_id="doc456",
    metadata={
        "ip": "192.168.1.1",
        "user_agent": "Mozilla/5.0..."
    }
)
```

## Secure Development

### 1. Dependency Security

```bash
# Scan dependencies
safety check

# Update vulnerable packages
uv sync --upgrade-only

# Configure allowed licenses
GRAPHFLEET_ALLOWED_LICENSES = [
    "MIT",
    "Apache-2.0",
    "BSD-3-Clause"
]
```

### 2. Code Security

```python
# Configure security checks
GRAPHFLEET_SECURITY_CHECKS = {
    "static_analysis": True,
    "dependency_scan": True,
    "secret_scan": True
}

# Pre-commit hooks
from graphfleet.security import scan_code

def pre_commit_hook():
    results = scan_code()
    if results.has_vulnerabilities:
        raise Exception("Security issues found")
```

## Compliance

### 1. Data Privacy

```python
# Configure privacy settings
GRAPHFLEET_PRIVACY = {
    "data_retention": {
        "documents": "90d",
        "user_data": "365d",
        "audit_logs": "730d"
    },
    "pii_detection": True,
    "auto_redaction": True
}
```

### 2. Regulatory Compliance

```python
# GDPR compliance settings
GRAPHFLEET_COMPLIANCE = {
    "gdpr": {
        "enabled": True,
        "data_export": True,
        "right_to_forget": True
    },
    "hipaa": {
        "enabled": False
    }
}
```

## Security Monitoring

### 1. Intrusion Detection

```python
# Configure security monitoring
GRAPHFLEET_SECURITY_MONITORING = {
    "intrusion_detection": True,
    "anomaly_detection": True,
    "alert_endpoints": [
        "email:security@graphfleet.ai",
        "slack:security-alerts"
    ]
}
```

### 2. Vulnerability Scanning

```bash
# Regular security scans
graphfleet-security scan --full

# Configure automated scanning
GRAPHFLEET_SECURITY_SCAN = {
    "schedule": "0 0 * * *",  # Daily
    "scan_types": ["deps", "code", "config"],
    "alert_on": ["high", "critical"]
}
```

## Incident Response

### 1. Security Alerts

```python
# Configure alert settings
GRAPHFLEET_ALERTS = {
    "channels": {
        "email": ["security@graphfleet.ai"],
        "slack": ["#security-alerts"],
        "pagerduty": ["security-team"]
    },
    "severity_levels": {
        "critical": ["all"],
        "high": ["security-team"],
        "medium": ["security-team"],
        "low": ["logs"]
    }
}
```

### 2. Incident Handling

```python
# Incident response automation
from graphfleet.security import handle_incident

def security_incident_handler(incident):
    # Log incident
    audit_log.security_incident(incident)
    
    # Take immediate action
    if incident.severity == "critical":
        handle_incident.lockdown_affected_resources(incident)
    
    # Notify team
    handle_incident.notify_team(incident)
```

## Best Practices

1. **Access Control**
   - Use principle of least privilege
   - Regularly review permissions
   - Implement MFA for sensitive operations

2. **Data Protection**
   - Encrypt sensitive data
   - Use secure communication channels
   - Implement proper backup strategies

3. **Monitoring**
   - Enable comprehensive logging
   - Set up alerts for suspicious activity
   - Regular security audits

## Support

For security-related issues:
- Email: security@graphfleet.ai
- Emergency: +1-XXX-XXX-XXXX
- Bug Bounty: https://hackerone.com/graphfleet 