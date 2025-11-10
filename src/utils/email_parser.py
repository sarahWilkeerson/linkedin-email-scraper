thonimport re

def parse_email(email):
    """
    Parse and validate the email address.
    """
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(email_regex, email):
        return email
    else:
        raise ValueError(f"Invalid email format: {email}")