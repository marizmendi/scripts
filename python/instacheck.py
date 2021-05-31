import instaloader

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

    print(followees-followers)



if __name__ == "__main__":
    main()
