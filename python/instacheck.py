import instaloader
import getpass
import sys
import os
import requests
from pathlib import Path
from tqdm import tqdm

def send_ntfy(topic, message, title="InstaCheck Update"):
    try:
        requests.post(
            f"https://ntfy.sh/{topic}",
            data=message.encode('utf-8'),
            headers={
                "Title": title,
                "Priority": "default",
                "Tags": "camera,instagram"
            }
        )
    except Exception as e:
        print(f"Failed to send notification: {e}")

def main():
    L = instaloader.Instaloader()
    username = "manmar92"
    ntfy_topic = "d3b8e7c2-9f1a-4b5d-8e6c-7a9b0c1d2e3f"
    
    # Check if we are running in a non-interactive shell (like cron)
    is_interactive = sys.stdin.isatty()

    try:
        L.load_session_from_file(username)
        logged_in_user = L.test_login()
        if not logged_in_user:
            raise FileNotFoundError
    except FileNotFoundError:
        if not is_interactive:
            msg = "Session expired and running in non-interactive mode. Please run manually once to log in."
            print(msg)
            if ntfy_topic:
                send_ntfy(ntfy_topic, msg, title="InstaCheck Error")
            sys.exit(1)
            
        print(f"No valid session found for {username}. Logging in...")
        password = getpass.getpass(f"Enter password for {username}: ")
        try:
            L.login(username, password)
            L.save_session_to_file()
        except Exception as e:
            print(f"Login failed: {e}")
            sys.exit(1)

    try:
        profile = instaloader.Profile.from_username(L.context, username)
        
        # Collect followers/followees
        followers = {f.username for f in profile.get_followers()}
        followees = {f.username for f in profile.get_followees()}
        non_followers = followees - followers

        # Build report
        report = []
        report.append(f"Followers: {len(followers)}")
        report.append(f"Following: {len(followees)}")
        report.append(f"Not following back: {len(non_followers)}")
        
        if non_followers:
            report.append("\nUsers who don't follow you back:")
            for user in sorted(non_followers):
                report.append(f"- {user}")
        else:
            report.append("\nEveryone you follow follows you back! 🎉")

        full_report = "\n".join(report)
        print("\n" + "="*40)
        print(f"RESULTS FOR {username}")
        print("="*40)
        print(full_report)

        if ntfy_topic and non_followers:
            send_ntfy(ntfy_topic, full_report, title=f"InstaCheck: {username}")
            
    except Exception as e:
        error_msg = f"An error occurred: {e}"
        print(error_msg)
        if ntfy_topic:
            send_ntfy(ntfy_topic, error_msg, title="InstaCheck Error")

if __name__ == "__main__":
    main()
