# Security Policy

This document outlines the security policy for the Django Application Template, including supported versions and the process for reporting vulnerabilities.

## Supported Versions

The following versions of the Django Application Template (based on Django) are currently supported with security updates. We recommend using a supported version to ensure your application remains secure.

| Version | Supported          |
|---------|--------------------|
| 5.1.x   | :white_check_mark: |
| 5.0.x   | :x:                |
| 4.2.x   | :white_check_mark: |
| < 4.2   | :x:                |

**Note**: The template is built with Django 5.1.3. Older versions may contain unpatched vulnerabilities. Always use the latest supported version.

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it responsibly by following these steps:

1. **Where to Report**:
   - Email vulnerabilities to `<your-security-email@example.com>` (replace with your preferred contact email).
   - Do not disclose the vulnerability publicly (e.g., in GitHub issues) until it has been addressed.

2. **What to Include**:
   - A detailed description of the vulnerability.
   - Steps to reproduce the issue.
   - Potential impact (e.g., data exposure, unauthorized access).
   - Any suggested fixes or mitigations.

3. **Response Timeline**:
   - You will receive an acknowledgment of your report within **48 hours**.
   - We aim to provide an initial assessment within **7 days**.
   - Regular updates will be provided as we investigate and address the issue.

4. **What to Expect**:
   - If the vulnerability is **accepted**, we will work on a fix and release a security update, crediting you (if desired) in the release notes.
   - If the vulnerability is **declined** (e.g., out of scope or invalid), we will provide a clear explanation.
   - We may coordinate with the Django Security Team if the issue affects upstream Django or dependencies like Django REST Framework or Simple JWT.

5. **Confidentiality**:
   - All reports are treated as confidential and will not be shared without your permission, except as needed to coordinate fixes with maintainers or upstream projects.

We appreciate your help in keeping this project secure!

## Additional Notes

- This project uses dependencies like Django REST Framework, Simple JWT, Celery, and Redis. For vulnerabilities in these libraries, we recommend checking their respective security advisories and upgrading to patched versions.
- For Docker-related security concerns, ensure you use the latest images for PostgreSQL (`postgres:15`) and Redis (`redis:7-alpine`) as specified in `docker-compose.yml`.

For further assistance, contact the maintainers via the repository’s issue tracker (for non-security issues) or the email above (for security issues).
