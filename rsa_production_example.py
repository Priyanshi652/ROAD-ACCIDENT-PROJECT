"""
Production RSA Encryption Example using the 'cryptography' library.
This is recommended for real-world applications.

Install required library:
pip install cryptography
"""

try:
    from cryptography.hazmat.primitives.asymmetric import rsa, padding
    from cryptography.hazmat.primitives import serialization, hashes
    from cryptography.hazmat.backends import default_backend
except ImportError:
    print("Please install the cryptography library: pip install cryptography")
    exit(1)


class RSAEncryption:
    """RSA Encryption class using the cryptography library."""
    
    def __init__(self, key_size: int = 2048):
        """Initialize with key generation."""
        self.private_key = None
        self.public_key = None
        self.generate_keys(key_size)
    
    def generate_keys(self, key_size: int):
        """Generate RSA key pair."""
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()
    
    def encrypt(self, message: str) -> bytes:
        """Encrypt a message using the public key."""
        message_bytes = message.encode('utf-8')
        
        encrypted = self.public_key.encrypt(
            message_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted
    
    def decrypt(self, encrypted_message: bytes) -> str:
        """Decrypt a message using the private key."""
        decrypted_bytes = self.private_key.decrypt(
            encrypted_message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted_bytes.decode('utf-8')
    
    def export_public_key_pem(self) -> bytes:
        """Export public key in PEM format."""
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    
    def export_private_key_pem(self, password: bytes = None) -> bytes:
        """Export private key in PEM format."""
        encryption_algorithm = serialization.NoEncryption()
        if password:
            encryption_algorithm = serialization.BestAvailableEncryption(password)
        
        return self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=encryption_algorithm
        )
    
    def load_public_key_pem(self, pem_data: bytes):
        """Load public key from PEM format."""
        self.public_key = serialization.load_pem_public_key(
            pem_data,
            backend=default_backend()
        )
    
    def load_private_key_pem(self, pem_data: bytes, password: bytes = None):
        """Load private key from PEM format."""
        self.private_key = serialization.load_pem_private_key(
            pem_data,
            password=password,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()


def production_rsa_demo():
    """Demonstration of production RSA encryption."""
    print("🔐 Production RSA Encryption Demo")
    print("=" * 40)
    
    # Create RSA encryption instance
    rsa_encryptor = RSAEncryption(key_size=2048)
    print("✓ RSA keys generated (2048-bit)")
    
    # Message to encrypt
    message = "This is a confidential message for production use! 🏢"
    print(f"\nOriginal message: '{message}'")
    
    # Encrypt the message
    encrypted_data = rsa_encryptor.encrypt(message)
    print(f"Encrypted data (bytes): {len(encrypted_data)} bytes")
    print(f"Encrypted data (hex): {encrypted_data.hex()[:100]}...")
    
    # Decrypt the message
    decrypted_message = rsa_encryptor.decrypt(encrypted_data)
    print(f"Decrypted message: '{decrypted_message}'")
    
    # Verify
    success = message == decrypted_message
    print(f"Encryption/Decryption successful: {success}")
    
    if success:
        print("🎉 Production RSA encryption works perfectly!")
    
    # Demonstrate key export/import
    print("\n" + "-" * 40)
    print("Key Export/Import Demo:")
    
    # Export keys
    public_pem = rsa_encryptor.export_public_key_pem()
    private_pem = rsa_encryptor.export_private_key_pem()
    
    print(f"Public key PEM (first 100 chars):\n{public_pem.decode()[:100]}...")
    print(f"Private key PEM (first 100 chars):\n{private_pem.decode()[:100]}...")
    
    # Create new instance and load keys
    new_rsa = RSAEncryption.__new__(RSAEncryption)  # Create without auto-generation
    new_rsa.load_private_key_pem(private_pem)
    
    # Test with loaded keys
    test_message = "Testing with loaded keys!"
    encrypted_test = new_rsa.encrypt(test_message)
    decrypted_test = new_rsa.decrypt(encrypted_test)
    
    print(f"\nKey loading test: {test_message == decrypted_test}")
    if test_message == decrypted_test:
        print("✓ Key export/import works correctly!")


def encrypt_large_message_demo():
    """Demo for handling large messages (chunking)."""
    print("\n🔐 Large Message Encryption Demo")
    print("=" * 40)
    
    rsa_encryptor = RSAEncryption(key_size=2048)
    
    # For RSA with OAEP padding, max message size is key_size/8 - 2*hash_size - 2
    # For 2048-bit key with SHA-256: 2048/8 - 2*32 - 2 = 190 bytes
    max_chunk_size = 190
    
    large_message = "This is a very long message that exceeds the RSA encryption limit. " * 5
    print(f"Large message length: {len(large_message)} bytes")
    print(f"Message preview: {large_message[:100]}...")
    
    # Split message into chunks
    chunks = [large_message[i:i+max_chunk_size] 
              for i in range(0, len(large_message), max_chunk_size)]
    
    print(f"Split into {len(chunks)} chunks")
    
    # Encrypt each chunk
    encrypted_chunks = []
    for i, chunk in enumerate(chunks):
        encrypted_chunk = rsa_encryptor.encrypt(chunk)
        encrypted_chunks.append(encrypted_chunk)
        print(f"Encrypted chunk {i+1}: {len(encrypted_chunk)} bytes")
    
    # Decrypt each chunk
    decrypted_chunks = []
    for i, encrypted_chunk in enumerate(encrypted_chunks):
        decrypted_chunk = rsa_encryptor.decrypt(encrypted_chunk)
        decrypted_chunks.append(decrypted_chunk)
        print(f"Decrypted chunk {i+1}: {len(decrypted_chunk)} bytes")
    
    # Reconstruct message
    reconstructed_message = ''.join(decrypted_chunks)
    
    print(f"\nOriginal length: {len(large_message)}")
    print(f"Reconstructed length: {len(reconstructed_message)}")
    print(f"Messages match: {large_message == reconstructed_message}")
    
    if large_message == reconstructed_message:
        print("🎉 Large message encryption/decryption successful!")


if __name__ == "__main__":
    production_rsa_demo()
    encrypt_large_message_demo()