"""
Caesar alphbetic substitution cipher.

Example NLTK tokenization:
    word_tokens = nltk.tokenize.word_tokenize(sample_text)
    untokenized_words = \
    nltk.tokenize.treebank.TreebankWordDetokenizer().detokenize(word_tokens)
"""


class Cipher:
    """Base class for encrypting and decrypting text."""

    def __init__(self, n, text):
        self.n = n
        self.text = text
        self.word_tokens = text.split()  # Tokenize on spaces.
        self.encrypted_text = None
        self.decrypted_text = None

    def _encrypt(self) -> str:
        """Helper function to encrypt word tokens."""
        raise NotImplementedError

    def _decrypt(self) -> str:
        """Helper function to decrypt encrypted word tokens."""
        raise NotImplementedError

    def encrypt(self):
        if self.encrypted_text is None:
            self.encrypted_text = self._encrypt()
        return self.encrypted_text

    def decrypt(self):
        if self.encrypted_text is None:
            raise RuntimeError("No encrypted text to decrypt.")
        if self.decrypted_text is None:
            self.decrypted_text = self._decrypt()
        return self.decrypted_text

    def get_text(self):
        return self.text


class Caesar(Cipher):
    """
    Substitution cipher, permutes uppercase and lowercase alphabet by n characters.
    """

    def __init__(self, n, text):
        assert isinstance(n, int), "Permutation n must be an integer."
        assert 0 <= n <= 25, "Permutation n must lie in {0, ..., 25}."
        super().__init__(n, text)

    def _encrypt(self) -> str:
        """Helper function to encrypt word tokens."""
        word_list = []
        for word in self.word_tokens:
            encrypted_word = ""
            for c in word:
                # Unicode code point value offset makes logic ugly.
                # Essentially just modulo last letter in alphabet.
                if c.islower():
                    offset = ord("a")
                    char = chr(
                        (ord(c) + self.n - offset) % (ord("z") - offset) + offset
                    )
                elif c.isupper():
                    offset = ord("A")
                    char = chr(
                        (ord(c) + self.n - offset) % (ord("Z") - offset) + offset
                    )
                else:
                    char = c
                encrypted_word += char
            word_list.append(encrypted_word)

        return " ".join(word_list)

    def _decrypt(self) -> str:
        """Helper function to decrypt encrypted word tokens."""
        word_list = []
        for word in self.encrypted_text.split():
            encrypted_word = ""
            for c in word:
                # Unicode code point value offset makes logic ugly.
                # Essentially just modulo last letter in alphabet.
                if c.islower():
                    offset = ord("a")
                    char = chr(
                        (ord(c) - self.n - offset) % (ord("z") - offset) + offset
                    )
                elif c.isupper():
                    offset = ord("A")
                    char = chr(
                        (ord(c) - self.n - offset) % (ord("Z") - offset) + offset
                    )
                else:
                    char = c
                encrypted_word += char
            word_list.append(encrypted_word)

        return " ".join(word_list)


class Unicode_Substitution(Cipher):
    """Unicode substitution cipher."""

    def __init__(self, n, text):
        assert isinstance(n, int), "Permutation n must be an integer."
        assert 0 <= n <= 65534, "Permutation n must lie in {0, ..., 25}."
        super().__init__(n, text)
        self.max_ord = 65535

    def _encrypt(self) -> str:
        """Helper function to encrypt word tokens."""
        word_list = []
        for word in self.word_tokens:
            encrypted_word = ""
            for c in word:
                char = chr((ord(c) + self.n) % self.max_ord)
                encrypted_word += char
            word_list.append(encrypted_word)

        return " ".join(word_list)

    def _decrypt(self) -> str:
        """Helper function to decrypt encrypted word tokens."""
        word_list = []
        for word in self.encrypted_text.split():
            encrypted_word = ""
            for c in word:
                char = chr((ord(c) - self.n) % self.max_ord)
                encrypted_word += char
            word_list.append(encrypted_word)

        return " ".join(word_list)


def main():
    """Test out ciphers."""
    sample_text = (
        "Here's some text that I am writing, look at these characters go."
        + "'spect to the Romans."
    )

    caesar_cipher = Caesar(20, sample_text)
    unicode_cipher = Unicode_Substitution(6000, sample_text)

    print("Caesar Cipher", "#" * 14, sep="\n", end="\n\n")
    print("Original Text", "-" * 14, caesar_cipher.get_text(), sep="\n", end="\n\n")
    print("Encrypted Text", "-" * 14, caesar_cipher.encrypt(), sep="\n", end="\n\n")
    print("Decrypted Text", "-" * 14, caesar_cipher.decrypt(), sep="\n", end="\n\n")

    print("Unicode Cipher", "#" * 14, sep="\n", end="\n\n")
    print("Original Text", "-" * 14, unicode_cipher.get_text(), sep="\n", end="\n\n")
    print("Encrypted Text", "-" * 14, unicode_cipher.encrypt(), sep="\n", end="\n\n")
    print("Decrypted Text", "-" * 14, unicode_cipher.decrypt(), sep="\n", end="\n\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting ..")
        exit()
