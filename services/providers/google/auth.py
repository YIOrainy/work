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
def callback(request: Request):
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
        
        if(save_user_credentials(credentials_data)):
            return "Success and saved to database"
        else:
            return "Failed"
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }


def save_user_credentials(creds: dict):
    fernet = Fernet(fernetKey)
    user = User(
        name = 'Yazeed',
        access_token=fernet.encrypt(creds['access_token'].encode()).decode(),
        refresh_token=fernet.encrypt(creds['refresh_token'].encode()).decode(),
        token_uri=creds['token_uri'],
        client_id=fernet.encrypt(creds['client_id'].encode()).decode(),
        client_secret=fernet.encrypt(creds['client_secret'].encode()).decode(),
        expiry=creds['expiry'])

    session = Session()
    session.add(user)
    session.commit()
    session.close()
    return True

@app.get("/refresh")
def refreshToken():
    fernet = Fernet(fernetKey)  
    session = Session()

    user = session.query(User).filter(User.name == "Yazeed").first()
    
    if not user:
        session.close()
        return {"error": "User not found. Please authenticate first."}

    creds = get_credentials(user, fernetKey)

    

    creds.refresh(GoogleRequest())
    user.access_token = fernet.encrypt(creds.token.encode()).decode()
    if creds.refresh_token:  # In case it changed
        user.refresh_token = fernet.encrypt(creds.refresh_token.encode()).decode()
    user.expiry = creds.expiry.isoformat() if creds.expiry else None
    
    session.commit()
    session.close()

    return {
        "access_token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "expiry": creds.expiry,
        "message": "Refreshed successfully"
    }

@app.get("/connected")
def is_connected():
    session = Session()
    user = session.query(User).filter(User.name == "Yazeed").first()
    session.close()
    return user is not None
