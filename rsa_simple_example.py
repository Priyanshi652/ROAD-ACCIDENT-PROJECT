"""
Simple RSA Encryption Example
This is a basic implementation for educational purposes.
For production use, please use established cryptographic libraries like 'cryptography'.
"""

from rsa_encryption import generate_keypair, encrypt_string, decrypt_string


def simple_rsa_demo():
    """Simple demonstration of RSA encryption and decryption."""
    
    print("🔐 Simple RSA Encryption Demo")
    print("-" * 30)
    
    # Step 1: Generate RSA key pair
    print("1. Generating RSA key pair (1024-bit)...")
    public_key, private_key = generate_keypair(1024)
    print("   ✓ Keys generated successfully!")
    
    # Step 2: Prepare message
    message = "This is a secret message! 🔒"
    print(f"\n2. Original message: '{message}'")
    
    # Step 3: Encrypt the message
    print("\n3. Encrypting message...")
    encrypted_message = encrypt_string(message, public_key)
    print(f"   ✓ Encrypted message: {encrypted_message}")
    
    # Step 4: Decrypt the message
    print("\n4. Decrypting message...")
    decrypted_message = decrypt_string(encrypted_message, private_key)
    print(f"   ✓ Decrypted message: '{decrypted_message}'")
    
    # Step 5: Verify
    print(f"\n5. Verification: {message == decrypted_message}")
    
    if message == decrypted_message:
        print("   🎉 RSA encryption/decryption successful!")
    else:
        print("   ❌ Something went wrong!")


if __name__ == "__main__":
    simple_rsa_demo()