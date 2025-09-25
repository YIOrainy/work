from cryptography.fernet import Fernet
from google.oauth2.credentials import Credentials

def get_credentials(user, fernetKey):
    fernet = Fernet(fernetKey)
    creds = Credentials(
        token=fernet.decrypt(user.access_token.encode()).decode(),
        refresh_token=fernet.decrypt(user.refresh_token.encode()).decode(),
        token_uri=user.token_uri,
        client_id=fernet.decrypt(user.client_id.encode()).decode(),
        client_secret=fernet.decrypt(user.client_secret.encode()).decode(),
    )
    return creds