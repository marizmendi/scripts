import instaloader
import getpass
import sys
from pathlib import Path
from tqdm import tqdm

def main():
    L = instaloader.Instaloader()

    username = "manmar92"
    print(f"Using username: {username}")
    
    # Try to load session from default location
    try:
        L.load_session_from_file(username)
        # Verify session
        try:
            logged_in_user = L.test_login()
            if logged_in_user:
                print(f"Session verified for {logged_in_user}.")
            else:
                print("Session loaded but verification failed. Re-logging in...")
                raise FileNotFoundError
        except Exception as e:
            print(f"Session verification failed: {e}. Re-logging in...")
            raise FileNotFoundError
            
    except FileNotFoundError:
        # If session file doesn't exist, log in and save session
        print(f"No session found for {username}. Logging in...")
        password = getpass.getpass(f"Enter password for {username}: ")
        try:
            L.login(username, password)
            L.save_session_to_file()
            print("Login successful and session saved.")
        except instaloader.exceptions.BadCredentialsException:
            print("Error: Invalid username or password.")
            sys.exit(1)
        except instaloader.exceptions.TwoFactorAuthRequiredException:
            print("Two-factor authentication is required.")
            code = input("Enter 2FA code: ")
            try:
                L.two_factor_login(code)
                L.save_session_to_file()
                print("2FA Login successful and session saved.")
            except Exception as e:
                print(f"Failed to complete 2FA login: {e}")
                sys.exit(1)
        except Exception as e:
            print(f"An error occurred during login: {e}")
            sys.exit(1)

    print("\nFetching followers and followees. This may take a while if you have many followers...")
    try:
        profile = instaloader.Profile.from_username(L.context, username)
        
        print(f"Getting {profile.followers} followers...")
        followers = set()
        for follower in tqdm(profile.get_followers(), total=profile.followers, unit="user"):
            followers.add(follower.username)
        
        print(f"Getting {profile.followees} accounts you follow (followees)...")
        followees = set()
        for followee in tqdm(profile.get_followees(), total=profile.followees, unit="user"):
            followees.add(followee.username)
        
        non_followers = followees - followers

        print("\n" + "="*40)
        print(f"RESULTS FOR {username}")
        print("="*40)
        print(f"Followers: {len(followers)}")
        print(f"Following: {len(followees)}")
        print(f"Not following you back: {len(non_followers)}")
        print("-" * 40)
        
        if non_followers:
            print("Users who don't follow you back:")
            for user in sorted(non_followers):
                print(f"- {user}")
        else:
            print("Everyone you follow follows you back! 🎉")
            
    except instaloader.exceptions.LoginRequiredException:
        print("Error: Session expired or login required.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
