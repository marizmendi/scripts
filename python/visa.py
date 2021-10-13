import time

import requests

WAIT_TIME = 3

def check_visa():
    s = requests.Session()

    # Log in with your username and password in https://ais.usvisa-info.com/es-es/niv/users/sign_in
    # Get the _yatri_session cookie using your prefered browser developer tools
    cookie = ""

    # Click continue on your existing appointment and get the user_id from the URL: https://ais.usvisa-info.com/es-es/niv/schedule/<user_id>/continue_actions
    user_id = ""

    url = "https://ais.usvisa-info.com/en-es/niv/schedule/{}/appointment/days/7.json?appointments[expedite]=false".format(user_id)
    headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:92.0) Gecko/20100101 Firefox/92.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
    }

    s.cookies.set("_yatri_session",cookie)

    resp = s.get(url, headers=headers)
    print(resp.json()[0].get('date'))
    if resp.status_code != 200:
        return "ERROR CODE {}".format(resp.status_code)
    if resp.json()[0].get('date').split('-')[0] == "2021":
        return "https://ais.usvisa-info.com/en-es/niv"

    return False

def main():
    while True:
        resp = check_visa()
        if resp:
            print(resp)
            break
        time.sleep(WAIT_TIME)


if __name__ == "__main__":
    main()