import os
from fastapi import FastAPI, Request
import google_auth_oauthlib.flow
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware

# ✅ FIX: Allow HTTP for development (REMOVE IN PRODUCTION!)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'



app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="AQ16TpRoS1IexgkPXMTqDPDpfwa06ItQGOh3RsAUkC4=")




@app.get("/auth")
def auth(request: Request):
    # Required, call the from_client_secrets_file method to retrieve the client ID from a
    # client_secret.json file. The client ID (from that file) and access scopes are required. (You can
    # also use the from_client_config method, which passes the client configuration as it originally
    # appeared in a client secrets file but doesn't access the file itself.)
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('client_secret.json',
        scopes=['https://www.googleapis.com/auth/calendar'])

    # Required, indicate where the API server will redirect the user after the user completes
    # the authorization flow. The redirect URI is required. The value must exactly
    # match one of the authorized redirect URIs for the OAuth 2.0 client, which you
    # configured in the API Console. If this value doesn't match an authorized URI,
    # you will get a 'redirect_uri_mismatch' error.
    flow.redirect_uri = 'http://localhost:8000/oauth2/callback'
    # Generate URL for request to Google's OAuth 2.0 server.
    # Use kwargs to set optional request parameters.
    authorization_url, state = flow.authorization_url(
        # Recommended, enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Optional, enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true',
        # Optional, if your application knows which user is trying to authenticate, it can use this
        # parameter to provide a hint to the Google Authentication Server.
        # login_hint='hint@example.com',
        # Optional, set prompt to 'consent' will prompt the user for consent
        prompt='consent')   

    request.session['state'] = state
    return RedirectResponse(authorization_url)


@app.get("/oauth2/callback")
def callback_fixed(request: Request):
    """Extract and return serializable credential data for database storage"""
    try:
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('client_secret.json',
            scopes=['https://www.googleapis.com/auth/calendar'])
        flow.redirect_uri = 'http://localhost:8000/oauth2/callback'
        
        authorization_response = str(request.url)
        flow.fetch_token(authorization_response=authorization_response)
        credentials = flow.credentials
        
        credentials_data = {
            "access_token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "token_uri": credentials.token_uri,
            "client_id": credentials.client_id,
            "client_secret": credentials.client_secret,
            "expiry": credentials.expiry.isoformat() if credentials.expiry else None,
            "success": True,
            "message": "OAuth completed successfully!"
        }
        
        return credentials_data
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }
        
@app.get("/")
def read_root():
    return {"Hello": "World"}


