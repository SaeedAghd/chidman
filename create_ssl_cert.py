#!/usr/bin/env python3
"""
اسکریپت ایجاد SSL Certificate خودامضا برای Django
"""

import os
import ssl
import socket
import ipaddress
from datetime import datetime, timedelta
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa

def create_self_signed_cert():
    """ایجاد SSL certificate خودامضا"""
    
    # ایجاد کلید خصوصی
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    
    # اطلاعات certificate
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "IR"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Tehran"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Tehran"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Chideman"),
        x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
    ])
    
    # ایجاد certificate
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.utcnow()
    ).not_valid_after(
        datetime.utcnow() + timedelta(days=365)
    ).add_extension(
        x509.SubjectAlternativeName([
            x509.DNSName("localhost"),
            x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")),
        ]),
        critical=False,
    ).sign(private_key, hashes.SHA256())
    
    # ذخیره کلید خصوصی
    with open("ssl/key.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
    
    # ذخیره certificate
    with open("ssl/cert.pem", "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    
    print("✅ SSL Certificate با موفقیت ایجاد شد!")
    print("📁 فایل‌ها در پوشه ssl/ ذخیره شدند:")
    print("   - ssl/cert.pem (Certificate)")
    print("   - ssl/key.pem (Private Key)")

if __name__ == "__main__":
    # ایجاد پوشه ssl اگر وجود ندارد
    os.makedirs("ssl", exist_ok=True)
    
    try:
        create_self_signed_cert()
    except ImportError:
        print("❌ کتابخانه cryptography نصب نیست!")
        print("💡 برای نصب: pip install cryptography")
    except Exception as e:
        print(f"❌ خطا در ایجاد certificate: {e}")
