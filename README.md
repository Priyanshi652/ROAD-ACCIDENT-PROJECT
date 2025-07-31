# RSA Encryption in Python

This repository contains three different implementations of RSA encryption in Python, ranging from educational to production-ready code.

## 📁 Files Overview

### 1. `rsa_encryption.py` - Educational Implementation
A complete, from-scratch implementation of RSA encryption including:
- Prime number generation using Miller-Rabin primality test
- Key pair generation (public/private keys)
- Encryption and decryption functions
- String to integer conversion utilities
- Comprehensive demo with both string and numerical encryption

**Features:**
- ✅ Pure Python implementation
- ✅ No external dependencies
- ✅ Educational value - shows how RSA works internally
- ✅ Supports both string and integer encryption
- ✅ Configurable key sizes

### 2. `rsa_simple_example.py` - Quick Start
A simplified demonstration that uses the educational implementation with clear step-by-step output.

**Features:**
- ✅ Easy to understand
- ✅ Step-by-step demonstration
- ✅ Perfect for learning RSA basics

### 3. `rsa_production_example.py` - Production Ready
Uses the industry-standard `cryptography` library with proper security practices.

**Features:**
- ✅ Industry-standard security
- ✅ Proper padding (OAEP)
- ✅ Key export/import in PEM format
- ✅ Large message handling (chunking)
- ✅ Password-protected private keys
- ✅ Production-ready code

## 🚀 Getting Started

### Prerequisites

```bash
# For educational implementations (rsa_encryption.py, rsa_simple_example.py)
python3  # No additional packages required

# For production implementation (rsa_production_example.py)
pip install cryptography
# OR on Ubuntu/Debian:
sudo apt install python3-cryptography
```

### Running the Examples

```bash
# Educational implementation with full demo
python3 rsa_encryption.py

# Simple step-by-step demo
python3 rsa_simple_example.py

# Production implementation (requires cryptography library)
python3 rsa_production_example.py
```

## 📚 Usage Examples

### Basic Usage (Educational Implementation)

```python
from rsa_encryption import generate_keypair, encrypt_string, decrypt_string

# Generate RSA key pair
public_key, private_key = generate_keypair(2048)

# Encrypt a message
message = "Hello, World!"
encrypted = encrypt_string(message, public_key)

# Decrypt the message
decrypted = decrypt_string(encrypted, private_key)

print(f"Original: {message}")
print(f"Decrypted: {decrypted}")
print(f"Success: {message == decrypted}")
```

### Production Usage (Cryptography Library)

```python
from rsa_production_example import RSAEncryption

# Create RSA encryption instance
rsa = RSAEncryption(key_size=2048)

# Encrypt and decrypt
message = "Confidential data"
encrypted = rsa.encrypt(message)
decrypted = rsa.decrypt(encrypted)

# Export keys
public_pem = rsa.export_public_key_pem()
private_pem = rsa.export_private_key_pem()

# Save to files
with open('public_key.pem', 'wb') as f:
    f.write(public_pem)
```

## 🔐 Security Considerations

### Educational Implementation
- **Purpose**: Learning and understanding RSA algorithms
- **Security**: Basic implementation, suitable for educational purposes
- **Not recommended for**: Production systems, sensitive data

### Production Implementation
- **Purpose**: Real-world applications
- **Security**: Industry-standard with proper padding (OAEP)
- **Features**: Secure random number generation, proper key management
- **Recommended for**: Production systems, sensitive data

## 📊 Performance Comparison

| Implementation | Key Generation | Encryption Speed | Security Level | Dependencies |
|----------------|----------------|------------------|----------------|--------------|
| Educational    | Slow           | Moderate         | Basic          | None         |
| Production     | Fast           | Fast             | High           | cryptography |

## 🛠️ Key Features Explained

### RSA Algorithm Steps

1. **Key Generation**:
   - Generate two large prime numbers (p, q)
   - Calculate n = p × q
   - Calculate φ(n) = (p-1)(q-1)
   - Choose e (commonly 65537)
   - Calculate d = e⁻¹ mod φ(n)

2. **Encryption**: `c = m^e mod n`

3. **Decryption**: `m = c^d mod n`

### Security Features

- **Miller-Rabin Primality Test**: Ensures strong prime generation
- **OAEP Padding**: Prevents chosen-plaintext attacks (production only)
- **Secure Key Sizes**: Supports 1024, 2048, 4096+ bit keys
- **Proper Random Generation**: Cryptographically secure random numbers

## 🎯 Use Cases

### Educational Implementation
- Learning cryptography concepts
- Understanding RSA internals
- Computer science coursework
- Prototyping and experimentation

### Production Implementation
- Secure communications
- Digital signatures
- Key exchange protocols
- Enterprise applications

## ⚠️ Important Notes

### Message Size Limitations
RSA can only encrypt messages smaller than the key size:
- **2048-bit key**: ~245 bytes max (with OAEP padding)
- **4096-bit key**: ~510 bytes max (with OAEP padding)

For larger messages, use hybrid encryption:
1. Generate symmetric key (AES)
2. Encrypt data with AES
3. Encrypt AES key with RSA

### Key Size Recommendations
- **1024-bit**: Deprecated, not secure
- **2048-bit**: Current minimum recommendation
- **3072-bit**: Good for high security
- **4096-bit**: Maximum practical size

## 🔧 Troubleshooting

### Common Issues

1. **"Message too large for key size"**
   ```python
   # Solution: Use chunking or hybrid encryption
   # See rsa_production_example.py for chunking implementation
   ```

2. **"cryptography library not found"**
   ```bash
   pip install cryptography
   # OR
   sudo apt install python3-cryptography
   ```

3. **Slow key generation**
   ```python
   # Use smaller key size for testing
   public_key, private_key = generate_keypair(1024)
   ```

## 📝 License

This code is provided for educational purposes. Use at your own risk for production applications.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📖 Further Reading

- [RSA Algorithm - Wikipedia](https://en.wikipedia.org/wiki/RSA_(cryptosystem))
- [Python Cryptography Library](https://cryptography.io/)
- [OAEP Padding](https://en.wikipedia.org/wiki/Optimal_asymmetric_encryption_padding)
- [Miller-Rabin Primality Test](https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test)
