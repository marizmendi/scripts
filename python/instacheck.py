import instaloader
import requests
import json
import configparser

config = configparser.ConfigParser()

config.read("instaloader.cfg")

USER = config["default"]["user"]
UUID = config["default"]["uuid"]


def noti(user):
    requests.post(
        "https://ntfy.sh/",
        data=json.dumps(
            {
                "topic": f"{USER}_{UUID}",
                "message": f"{user} is not following you!",
                "actions": [
                    {
                        "action": "view",
                        "label": "Open Instagram",
                        "url": f"https://instagram.com/{user}",
                    }
                ],
            }
        ),
    )


def main():
    # Get instance
    L = instaloader.Instaloader()

    # Login or load session
    L.load_session_from_file(USER)  # (`instaloader -l USERNAME`)

    # Obtain profile metadata
    profile = instaloader.Profile.from_username(L.context, USER)

    followees = set()
    followers = set()

    # Print list of followees
    for followee in profile.get_followees():
        followees.add(followee.username)

    for follower in profile.get_followers():
        followers.add(follower.username)

    mismatch = followees - followers

    if len(mismatch):
        for user in mismatch:
            noti(user)


if __name__ == "__main__":
    main()
