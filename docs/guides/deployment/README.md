# Deployment Guide

This guide covers different deployment scenarios for GraphFleet, from single-instance setups to distributed deployments.

## Deployment Models

### 1. Single Instance

Best for development and small deployments:

```bash
# Using Docker
docker run -d \
  --name graphfleet \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -e GRAPHFLEET_ENV=production \
  qredence/graphfleet:latest

# Using Python
python -m graphfleet serve --host 0.0.0.0 --port 8000
```

### 2. Docker Compose

For local development and small production deployments:

```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    image: qredence/graphfleet:latest
    ports:
      - "8000:8000"
    environment:
      - GRAPHFLEET_ENV=production
      - GRAPHFLEET_STORAGE=s3
    volumes:
      - ./data:/app/data
    depends_on:
      - redis
      - postgres

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  postgres:
    image: postgres:15-alpine
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=graphfleet
      - POSTGRES_PASSWORD=secret
      - POSTGRES_DB=graphfleet
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  redis_data:
  postgres_data:
```

### 3. Kubernetes

For production deployments:

```yaml
# kubernetes/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: graphfleet
spec:
  replicas: 3
  selector:
    matchLabels:
      app: graphfleet
  template:
    metadata:
      labels:
        app: graphfleet
    spec:
      containers:
      - name: graphfleet
        image: qredence/graphfleet:latest
        ports:
        - containerPort: 8000
        env:
        - name: GRAPHFLEET_ENV
          value: production
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
```

## Configuration

### 1. Environment Variables

Production environment variables:

```bash
# Core Settings
GRAPHFLEET_ENV=production
GRAPHFLEET_DEBUG=false
GRAPHFLEET_SECRET_KEY=your-secret-key

# Storage
GRAPHFLEET_STORAGE=s3
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_DEFAULT_REGION=us-west-2

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/graphfleet

# Cache
REDIS_URL=redis://localhost:6379/0

# API
API_CORS_ORIGINS=https://your-domain.com
API_RATE_LIMIT=1000
```

### 2. SSL/TLS Configuration

Using Nginx as a reverse proxy:

```nginx
# /etc/nginx/conf.d/graphfleet.conf
server {
    listen 443 ssl;
    server_name api.graphfleet.ai;

    ssl_certificate /etc/letsencrypt/live/api.graphfleet.ai/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.graphfleet.ai/privkey.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Scaling Strategies

### 1. Horizontal Scaling

```bash
# Scale API servers
kubectl scale deployment graphfleet --replicas=5

# Scale workers
kubectl scale deployment graphfleet-worker --replicas=3
```

### 2. Vertical Scaling

Adjust resource limits in Kubernetes:

```yaml
resources:
  requests:
    memory: "4Gi"
    cpu: "2000m"
  limits:
    memory: "8Gi"
    cpu: "4000m"
```

## Monitoring

### 1. Prometheus Metrics

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'graphfleet'
    static_configs:
      - targets: ['graphfleet:8000']
```

### 2. Logging

Using fluentd for log aggregation:

```yaml
# fluentd.conf
<source>
  @type forward
  port 24224
</source>

<match graphfleet.**>
  @type elasticsearch
  host elasticsearch
  port 9200
  logstash_format true
</match>
```

## Backup and Recovery

### 1. Database Backup

```bash
# Backup PostgreSQL
pg_dump -U graphfleet > backup.sql

# Backup to S3
aws s3 cp backup.sql s3://backups/graphfleet/
```

### 2. Document Storage Backup

```bash
# Sync document storage to backup
aws s3 sync s3://graphfleet-docs s3://backups/docs/

# Restore from backup
aws s3 sync s3://backups/docs/ s3://graphfleet-docs
```

## Security Considerations

1. **Network Security**
   - Use VPC/subnet isolation
   - Implement proper firewall rules
   - Enable SSL/TLS

2. **Access Control**
   - Use IAM roles
   - Implement RBAC
   - Regular audit logging

3. **Data Security**
   - Enable encryption at rest
   - Use secure communication
   - Regular security updates

## Troubleshooting

### Common Issues

1. **Memory Issues**
```bash
# Check memory usage
docker stats graphfleet

# Adjust JVM settings
export JAVA_OPTS="-Xmx4g -Xms2g"
```

2. **Connection Issues**
```bash
# Check network connectivity
nc -zv database 5432
nc -zv redis 6379

# Check logs
kubectl logs deployment/graphfleet
```

3. **Performance Issues**
```bash
# Enable debug logging
export GRAPHFLEET_LOG_LEVEL=debug

# Monitor metrics
curl localhost:8000/metrics
```

## Maintenance

### 1. Updates

```bash
# Update Docker images
docker-compose pull
docker-compose up -d

# Update Kubernetes deployments
kubectl set image deployment/graphfleet graphfleet=qredence/graphfleet:latest
```

### 2. Health Checks

```bash
# Check API health
curl https://api.graphfleet.ai/health

# Check worker health
curl https://api.graphfleet.ai/health/worker
```

## Support

For deployment support:
- Email: devops@graphfleet.ai
- Documentation: https://docs.graphfleet.ai/deployment
- Community: https://discord.gg/graphfleet 