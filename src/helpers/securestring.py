import hmac
SECRET = 'thisisasecurestringvalue'

class SecureString(object):
    """Secure String implementation"""
    @classmethod
    def make_secure_val(cls, plain_string):
        """Returns a secure string from an input string"""
        return "%s|%s" % (plain_string, hmac.new(SECRET, plain_string).hexdigest())

    @classmethod
    def check_secure_val(cls, secure_val):
        """Checks to see if the input is valid"""
        inp = secure_val.split('|')[0]
        return inp and (secure_val == cls.make_secure_val(inp))

    @classmethod
    def get_userid(cls, secure_string):
        """Gets the user id from a secure string"""
        return secure_string.split('|')[0] if secure_string else None

    @classmethod
    def is_valid_cookie(cls, inp_string):
        """Takes in a string and checks to see if it is a valid secure string"""
        return inp_string and cls.check_secure_val(inp_string)
