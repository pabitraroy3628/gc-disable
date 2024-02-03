import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/admin.directory.user"]

def get_suspended_accounts(service):
    try:
        # Call the Admin SDK Directory API to retrieve suspended users
        results = service.users().list(customer="my_customer", query="isSuspended=true").execute()
        suspended_users = results.get("users", [])

        if not suspended_users:
            print("No suspended users in the domain.")
        else:
            print("Suspended Users:")
            for user in suspended_users:
                print(f"{user['primaryEmail']} ({user['name']['fullName']})")
    except Exception as e:
        print(f"Error retrieving suspended users: {e}")

def main():
    """Shows basic usage of the Admin SDK Directory API.
    Prints the emails and names of the first 10 users in the domain.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("admin", "directory_v1", credentials=creds)

    # Call the function to get the list of suspended accounts
    get_suspended_accounts(service)

if __name__ == "__main__":
    main()
