# Google Sign-In Setup Instructions

## Overview
Your online grocery store now supports "Sign in with Google" functionality on both the login and sign-up pages. Users can authenticate using their Google account instead of creating a traditional username/password account.

## Setting Up Google OAuth

### Step 1: Create a Google Cloud Project
1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Enter a project name (e.g., "Online Grocery Store")
4. Click "Create"

### Step 2: Enable Google+ API
1. In your project, go to "APIs & Services" → "Library"
2. Search for "Google+ API"
3. Click on it and then click "Enable"

### Step 3: Create OAuth 2.0 Credentials
1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted, configure the OAuth consent screen:
   - Choose "External" for User Type
   - Fill in the required fields (App name, User support email, Developer contact)
   - Add scopes: `userinfo.email`, `userinfo.profile`, `openid`
   - Save and continue

4. Back to creating OAuth client ID:
   - Application type: "Web application"
   - Name: "Online Grocery Store Web Client"
   - Authorized JavaScript origins: `http://localhost:5000`
   - Authorized redirect URIs: `http://localhost:5000/login/google/callback`
   - Click "Create"

5. **Important**: Copy the Client ID and Client Secret

### Step 4: Configure Your Application
1. Create a `.env` file in your project root (copy from `.env.example`):
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file and add your credentials:
   ```
   GOOGLE_CLIENT_ID=your_actual_client_id_here
   GOOGLE_CLIENT_SECRET=your_actual_client_secret_here
   ```

3. **Never commit the `.env` file to version control!**

### Step 5: Test the Integration
1. Start your Flask application:
   ```bash
   python app.py
   ```

2. Navigate to the login page (http://localhost:5000/login)

3. You should see:
   - Traditional login form
   - "OR" divider
   - "Continue with Google" button

4. Click "Continue with Google" and test the OAuth flow

## Production Deployment

When deploying to production:

1. Add your production URL to authorized redirect URIs in Google Cloud Console:
   ```
   https://yourdomain.com/login/google/callback
   ```

2. Update your production environment variables with the Google credentials

3. Consider publishing your OAuth consent screen for verified access

## How It Works

### User Flow
1. User clicks "Continue with Google" on login or sign-up page
2. User is redirected to Google's OAuth page
3. User authenticates and grants permissions
4. Google redirects back to your application with an authorization code
5. Your application exchanges the code for user information
6. If the user exists, they are logged in
7. If the user doesn't exist, a new account is created automatically using their Google email

### Backend Logic
- `google_login()` route initiates the OAuth flow
- `google_callback()` route handles the callback and creates/updates user accounts
- User accounts created via Google have auto-generated usernames and secure random passwords
- Email from Google is used as the primary identifier

## Security Notes

- Google OAuth credentials should be kept secret
- Use environment variables for sensitive data
- In production, use HTTPS for all OAuth redirect URIs
- Implement rate limiting to prevent abuse
- Store minimal user information from Google

## Troubleshooting

### "Google login is not configured" error
- Ensure your `.env` file exists and contains valid credentials
- Restart the Flask application after adding/changing `.env` values

### Redirect URI mismatch
- Verify the redirect URI in Google Cloud Console exactly matches: `http://localhost:5000/login/google/callback`
- For production, ensure production URLs are added

### OAuth consent screen errors
- Complete all required fields in the OAuth consent screen configuration
- Add test users if your app is in testing mode

## Features

✅ "Sign in with Google" button on login page  
✅ "Sign in with Google" button on sign-up page  
✅ Automatic user account creation  
✅ Material Design 3 styling  
✅ Dark mode support  
✅ Responsive design  
✅ Smooth animations and transitions  

## Need Help?

If you encounter issues, check:
1. Google Cloud Console credentials are correct
2. `.env` file is properly configured
3. Redirect URIs match exactly
4. OAuth consent screen is configured
5. Flask application has been restarted

---

**Last Updated**: February 2026
