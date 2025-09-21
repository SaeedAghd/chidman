# Environment Configuration Guide

## Overview
This guide explains how to properly configure environment variables for the Chidmano project in different environments.

## Files Structure

### 1. `env.example` - Template File
- **Purpose**: Template for all environments
- **Usage**: Copy to `.env` and customize
- **Contains**: All possible environment variables with example values

### 2. `liara.env` - Production Environment
- **Purpose**: Production configuration for Liara deployment
- **Usage**: Upload to Liara environment variables
- **Contains**: Production-ready values for Liara

### 3. `.env` - Local Development
- **Purpose**: Local development environment
- **Usage**: Create from `env.example` and customize
- **Contains**: Development-specific values

## Environment Variables Categories

### 🔧 Django Core Settings
```bash
DEBUG=True/False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=domain1,domain2,*.liara.run
```

### 🗄️ Database Configuration
```bash
# For SQLite (Development)
DATABASE_URL=sqlite:///db.sqlite3

# For PostgreSQL (Production)
DATABASE_URL=postgresql://user:pass@host:port/db
```

### 🔐 Security Settings
```bash
CSRF_TRUSTED_ORIGINS=https://domain.com
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
```

### 🤖 AI Configuration
```bash
# Liara AI (Recommended)
LIARA_AI_API_KEY=your-liara-ai-key
LIARA_AI_MODEL=openai/gpt-4.1
USE_LIARA_AI=True
FALLBACK_TO_OLLAMA=True

# OpenAI (Alternative)
OPENAI_API_KEY=your-openai-key
OPENAI_MODEL=gpt-4
```

### 📧 Email Configuration
```bash
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
SITE_URL=https://yourdomain.com
```

### 💳 Payment Gateway (Zarinpal)
```bash
ZARINPAL_MERCHANT_ID=your-merchant-id
ZARINPAL_SANDBOX=True
ZARINPAL_CALLBACK_URL=https://yourdomain.com/store/zarinpal/callback/
```

### 📁 Static & Media Files
```bash
STATIC_URL=/static/
STATIC_ROOT=staticfiles
MEDIA_URL=/media/
MEDIA_ROOT=media
```

### 📊 Performance Settings
```bash
DB_CONN_MAX_AGE=600
DB_CONN_HEALTH_CHECKS=True
FILE_UPLOAD_MAX_MEMORY_SIZE=5242880
DATA_UPLOAD_MAX_MEMORY_SIZE=10485760
```

### 🚀 Deployment Environment
```bash
LIARA=true/false
PRODUCTION=true/false
ENVIRONMENT=development/production
```

### 🔍 Monitoring & Health Checks
```bash
HEALTH_CHECK_ENABLED=True
HEALTH_CHECK_TIMEOUT=30
```

### 🎛️ Feature Flags
```bash
ENABLE_AI_ANALYSIS=True
ENABLE_WALLET_SYSTEM=True
ENABLE_SUPPORT_SYSTEM=True
ENABLE_ADMIN_DASHBOARD=True
ENABLE_PAYMENT_SYSTEM=True
```

### ⚡ Rate Limiting
```bash
RATE_LIMIT_ENABLED=True
RATE_LIMIT_REQUESTS_PER_MINUTE=60
RATE_LIMIT_BURST=10
```

### 💼 Business Logic Settings
```bash
# Store Analysis
MAX_ANALYSIS_PER_USER=10
ANALYSIS_EXPIRE_DAYS=30
ANALYSIS_PRICE_BASE=50000

# Wallet System
WALLET_MIN_DEPOSIT=10000
WALLET_MAX_DEPOSIT=10000000
WALLET_MIN_WITHDRAWAL=5000

# Support System
SUPPORT_TICKET_PRIORITY_HIGH=1
SUPPORT_TICKET_PRIORITY_MEDIUM=2
SUPPORT_TICKET_PRIORITY_LOW=3
SUPPORT_RESPONSE_TIME_HOURS=24
```

## Setup Instructions

### For Local Development
1. Copy `env.example` to `.env`
2. Update values for your local environment
3. Run `python manage.py runserver`

### For Liara Production
1. Go to Liara Dashboard
2. Navigate to your app → Settings → Environment Variables
3. Copy values from `liara.env`
4. Paste each variable with its value
5. Deploy your application

### For Other Production Environments
1. Copy `env.example` to `.env`
2. Update values for your production environment
3. Ensure all security settings are properly configured
4. Deploy your application

## Security Best Practices

### 🔒 Secret Key
- Use a strong, unique secret key
- Never commit secret keys to version control
- Use different keys for different environments

### 🌐 Allowed Hosts
- Always specify exact domains in production
- Use wildcards carefully
- Include all possible domains and subdomains

### 🔐 CSRF Protection
- Always configure CSRF_TRUSTED_ORIGINS
- Include all domains that will make requests
- Use HTTPS in production

### 📧 Email Configuration
- Use app-specific passwords for Gmail
- Never use your main account password
- Consider using dedicated email services for production

### 💳 Payment Gateway
- Use sandbox mode for testing
- Keep merchant IDs secure
- Test thoroughly before going live

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Check DATABASE_URL format
   - Ensure database service is running
   - Verify credentials

2. **CSRF Errors**
   - Check CSRF_TRUSTED_ORIGINS
   - Ensure all domains are included
   - Verify HTTPS configuration

3. **Email Sending Issues**
   - Check email credentials
   - Verify SMTP settings
   - Check firewall settings

4. **AI Service Errors**
   - Verify API keys
   - Check service availability
   - Review rate limits

5. **Payment Gateway Issues**
   - Verify merchant ID
   - Check sandbox/production mode
   - Test callback URLs

### Debug Mode
- Set `DEBUG=True` for detailed error messages
- Use `LOG_LEVEL=DEBUG` for verbose logging
- Check application logs for specific errors

## Environment-Specific Notes

### Development
- Use SQLite for simplicity
- Enable debug mode
- Use console email backend
- Disable rate limiting

### Production
- Use PostgreSQL for reliability
- Disable debug mode
- Use SMTP email backend
- Enable all security features
- Configure proper logging

### Liara Specific
- Database URL is auto-generated
- Static files are handled automatically
- Use Liara AI for best performance
- Configure health checks properly

## Maintenance

### Regular Tasks
- Rotate secret keys periodically
- Update API keys when needed
- Monitor log files for errors
- Review security settings

### Updates
- Keep environment files in sync
- Test changes in development first
- Document any new variables
- Update this guide as needed

## Support

For issues related to environment configuration:
1. Check this guide first
2. Review application logs
3. Test in development environment
4. Contact support if needed

---

**Last Updated**: 2025-01-21  
**Version**: 1.0.0  
**Maintainer**: Development Team
