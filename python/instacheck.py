import instaloader
import requests

USER = "manmar92"

def main():
    # Get instance
    L = instaloader.Instaloader()

    # Login or load session
    L.load_session_from_file(USER) # (`instaloader -l USERNAME`)

    # Obtain profile metadata
    profile = instaloader.Profile.from_username(L.context, USER)

    followees = set()
    followers = set()

    # Print list of followees
    for followee in profile.get_followees():
        followees.add(followee.username)

    for follower in profile.get_followers():
        followers.add(follower.username)

    mismatch = followees-followers

    if(len(mismatch)):
        requests.post("https://ntfy.sh/manmar92_mismatch",
            data=f"Mismatch: {mismatch}".encode(encoding='utf-8'))

if __name__ == "__main__":
    main()
