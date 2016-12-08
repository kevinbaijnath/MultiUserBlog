import hashlib
import random
from string import letters

class SecurePassword(object):
    """Secure Password implementation"""
    @classmethod
    def make_salt(cls, length=5):
        """Creates a salt that is 5 random letters joined together"""
        return ''.join(random.choice(letters) for x in xrange(length))

    @classmethod
    def make_password_hash(cls, name, password, salt=None):
        """Creates a password hash based off a given salt (or a new salt)"""
        if not salt:
            salt = cls.make_salt()
        new_hash = hashlib.sha256(name + password + salt).hexdigest()
        return "%s,%s" % (salt, new_hash)

    @classmethod
    def valid_password(cls, name, password, new_hash):
        """Checks to see if the input hash is equal to the user password hash"""
        salt = new_hash.split(',')[0]
        return new_hash == cls.make_password_hash(name, password, salt)
