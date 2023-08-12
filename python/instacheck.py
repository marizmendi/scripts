import instaloader
import requests

USER = "manmar92"

def noti(mismatch):
    requests.post("",
    data="Remote access to phils-laptop detected. Act right away.",
    headers={
        "Title": "Unauthorized access detected",
        "Priority": "urgent",
        "Tags": "warning,skull"
    })

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
