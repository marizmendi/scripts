import time
import os
import requests
import re

WAIT_TIME = 60

# Log in with your username and password in https://ais.usvisa-info.com/es-es/niv/users/sign_in
# Get the _yatri_session cookie using your prefered browser developer tools
# export it in env var YATRI_SESSION
# Use env var USER_AGENT to overwrite the default user agent in the script

# In order to use automatic log in, export this env vars
# export USER=<user>
# export PASSWORD=<password>

# Click continue on your existing appointment and get the user_id from the URL: https://ais.usvisa-info.com/es-es/niv/schedule/<user_id>/continue_actions
# export USER_ID = "42425124"
USER_ID = os.environ["USER_ID"]


class CheckVisaResponse:

    def __init__(self, success, error, date):
        self.success = success
        self.error = error
        self.date = date

    def retriable(self):
        return self.error == "" \
            or self.error == "No dates available" \
            or self.error == "Connection error, will try again" \
            or self.error == "Website is down for planned maintenance"

    def unauth_session(self):
        return self.error == "Your session expired, please sign in again to continue." \
            or self.error == "You need to sign in or sign up before continuing."


def success_response(date):
    return CheckVisaResponse(True, "", date)


def failure_response(error):
    return CheckVisaResponse(False, error, None)


def is_session_expired_html(resp_content):
    return "Your session has expired. Please log back in to continue." in resp_content

def is_website_maintenance_html(resp_content):
    return "Our website is down for planned maintenance. We should be back up momentarily. Check back soon." in resp_content

def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}" sound name "x"'
              """.format(text, title))


def new_session():
    s = requests.Session()
    if 'YATRI_SESSION' in os.environ:
        yatri = os.environ["YATRI_SESSION"]
        if yatri != None:
            s.cookies.set("_yatri_session", yatri)

    if 'USER_AGENT' in os.environ:
       s.headers['User-Agent'] = os.environ["USER_AGENT"] 
    else
        s.headers['User-Agent'] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:100.0) Gecko/20100105 Firefox/100.0"
    
    return s

def login(session):
    # session.cookies.unset("_yatri_session")
    session.cookies.clear()
    user = os.environ["USER"]
    password = os.environ["PASSWORD"]

    if user == None:
        print("Please provide USER env var")
        return False

    if password == None:
        print("Please provide PASSWORD env var")

    url = "https://ais.usvisa-info.com/en-es/niv/users/sign_in"
    headers = {
        "Accept":
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://ais.usvisa-info.com"
    }
    get_resp = session.get(url, headers=headers)
    regex = "name=\"authenticity_token\"\s+value=\"(?P<authenticity_token>[^\"]*)\""
    matches = re.search(regex, str(get_resp.content), re.MULTILINE)
    auth_token = matches.group('authenticity_token')
    if auth_token == None:
        print("auth token not found")
        return False

    data = {
        "utf8": "✓",
        "authenticity_token": auth_token,
        "user[email]": user,
        "user[password]": password,
        "policy_confirmed": "1",
        "commit": "Sign+In",
    }
    resp = session.post(url, headers=headers, data=data)
    if resp.status_code != 200:
        print("Logging in ERROR CODE {}".format(resp.status_code))
        return False

    return True


def check_visa(session):
    url = "https://ais.usvisa-info.com/en-es/niv/schedule/{}/appointment/days/7.json?appointments[expedite]=false".format(
        USER_ID)
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
    }
    try:
        resp = session.get(url, headers=headers)
    except (requests.exceptions.ConnectionError,
            requests.exceptions.ReadTimeout):
        return failure_response("Connection error, will try again")

    # print(resp.content)
    try:
        resp_json = resp.json()
    except requests.exceptions.JSONDecodeError:
        if is_session_expired_html(str(resp.content)):
            return failure_response(
                "Your session expired, please sign in again to continue.")
        elif is_website_maintenance_html(str(resp.content)):
            return failure_response(
                "Website is down for planned maintenance")
        print("Error decoding response to json. Body: \n" + str(resp.content))
        return failure_response("Invalid JSON body")
    # print("Resp: {}".format(resp_json))
    if not isinstance(resp_json, list) and resp_json["error"]:
        return failure_response(resp_json["error"])
    if resp.status_code != 200:
        return failure_response("ERROR CODE {}".format(resp.status_code))

    if len(resp_json) == 0:
        return failure_response("No dates available")

    print(resp_json[0].get("date"))

    if should_notify(resp_json[0].get("date")):
        notify(
            "New date available Embassy",
            "Go change appointment to https://ais.usvisa-info.com/en-es/niv",
        )

    return success_response(resp_json[0].get("date"))

def should_notify(date):
    date_split = date.split("-")
    year = date_split[0]
    month = date_split[1]
    day = date_split[2]

    # modify this logic based on your situation
    return year == "2023"

def main():
    session = new_session()
    while True:
        resp = check_visa(session)
        if not resp.success:
            print(resp.error)

        if resp.retriable():
            time.sleep(WAIT_TIME)
        elif resp.unauth_session():
            print("Logging in...")
            if not login(session):
                break
        else:
            break


if __name__ == "__main__":
    main()
