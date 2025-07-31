import random
import math
from typing import Tuple


def gcd(a: int, b: int) -> int:
    """Calculate the Greatest Common Divisor of two numbers."""
    while b:
        a, b = b, a % b
    return a


def mod_inverse(a: int, m: int) -> int:
    """Calculate the modular multiplicative inverse of a modulo m."""
    if gcd(a, m) != 1:
        raise ValueError("Modular inverse does not exist")
    
    # Extended Euclidean Algorithm
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    _, x, _ = extended_gcd(a, m)
    return (x % m + m) % m


def is_prime(n: int, k: int = 5) -> bool:
    """Miller-Rabin primality test."""
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    
    # Write n-1 as d * 2^r
    r = 0
    d = n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    
    # Witness loop
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        
        if x == 1 or x == n - 1:
            continue
        
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    
    return True


def generate_prime(bits: int) -> int:
    """Generate a random prime number with specified bit length."""
    while True:
        num = random.getrandbits(bits)
        # Ensure the number has the correct bit length
        num |= (1 << bits - 1) | 1  # Set MSB and LSB to 1
        if is_prime(num):
            return num


def generate_keypair(keysize: int = 1024) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """
    Generate RSA public and private key pair.
    
    Args:
        keysize: Size of the key in bits (default 1024)
    
    Returns:
        Tuple containing (public_key, private_key)
        public_key: (e, n)
        private_key: (d, n)
    """
    # Step 1: Generate two distinct prime numbers
    p = generate_prime(keysize // 2)
    q = generate_prime(keysize // 2)
    
    # Ensure p and q are different
    while p == q:
        q = generate_prime(keysize // 2)
    
    # Step 2: Compute n = p * q
    n = p * q
    
    # Step 3: Compute Euler's totient function φ(n) = (p-1)(q-1)
    phi = (p - 1) * (q - 1)
    
    # Step 4: Choose e such that 1 < e < φ(n) and gcd(e, φ(n)) = 1
    e = 65537  # Common choice for e
    while gcd(e, phi) != 1:
        e += 2
    
    # Step 5: Compute d, the modular multiplicative inverse of e
    d = mod_inverse(e, phi)
    
    # Return public and private keys
    public_key = (e, n)
    private_key = (d, n)
    
    return public_key, private_key


def encrypt(message: int, public_key: Tuple[int, int]) -> int:
    """
    Encrypt a message using RSA public key.
    
    Args:
        message: The message to encrypt (as an integer)
        public_key: Tuple containing (e, n)
    
    Returns:
        Encrypted message as integer
    """
    e, n = public_key
    if message >= n:
        raise ValueError("Message too large for key size")
    
    return pow(message, e, n)


def decrypt(ciphertext: int, private_key: Tuple[int, int]) -> int:
    """
    Decrypt a message using RSA private key.
    
    Args:
        ciphertext: The encrypted message
        private_key: Tuple containing (d, n)
    
    Returns:
        Decrypted message as integer
    """
    d, n = private_key
    return pow(ciphertext, d, n)


def string_to_int(text: str) -> int:
    """Convert string to integer for encryption."""
    return int.from_bytes(text.encode('utf-8'), 'big')


def int_to_string(num: int) -> str:
    """Convert integer back to string after decryption."""
    byte_length = (num.bit_length() + 7) // 8
    return num.to_bytes(byte_length, 'big').decode('utf-8')


def encrypt_string(message: str, public_key: Tuple[int, int]) -> int:
    """
    Encrypt a string message.
    
    Args:
        message: The string message to encrypt
        public_key: RSA public key (e, n)
    
    Returns:
        Encrypted message as integer
    """
    message_int = string_to_int(message)
    return encrypt(message_int, public_key)


def decrypt_string(ciphertext: int, private_key: Tuple[int, int]) -> str:
    """
    Decrypt an encrypted message back to string.
    
    Args:
        ciphertext: The encrypted message
        private_key: RSA private key (d, n)
    
    Returns:
        Decrypted string message
    """
    decrypted_int = decrypt(ciphertext, private_key)
    return int_to_string(decrypted_int)


def main():
    """Demonstration of RSA encryption/decryption."""
    print("RSA Encryption/Decryption Demo")
    print("=" * 40)
    
    # Generate key pair
    print("Generating RSA key pair...")
    public_key, private_key = generate_keypair(2048)
    
    e, n = public_key
    d, _ = private_key
    
    print(f"Public Key (e, n): ({e}, {n})")
    print(f"Private Key (d, n): ({d}, {n})")
    print()
    
    # Test with a string message
    original_message = "Hello, RSA Encryption!"
    print(f"Original message: {original_message}")
    
    # Encrypt the message
    encrypted = encrypt_string(original_message, public_key)
    print(f"Encrypted message: {encrypted}")
    
    # Decrypt the message
    decrypted_message = decrypt_string(encrypted, private_key)
    print(f"Decrypted message: {decrypted_message}")
    
    # Verify
    print(f"Decryption successful: {original_message == decrypted_message}")
    
    print("\n" + "=" * 40)
    
    # Test with numerical message
    print("Testing with numerical message...")
    num_message = 12345
    print(f"Original number: {num_message}")
    
    encrypted_num = encrypt(num_message, public_key)
    print(f"Encrypted number: {encrypted_num}")
    
    decrypted_num = decrypt(encrypted_num, private_key)
    print(f"Decrypted number: {decrypted_num}")
    
    print(f"Numerical decryption successful: {num_message == decrypted_num}")


if __name__ == "__main__":
    main()