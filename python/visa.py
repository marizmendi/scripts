import datetime
import time

import requests

WAIT_TIME = 5

# Log in with your username and password in https://ais.usvisa-info.com/es-es/niv/users/sign_in
# Get the _yatri_session cookie using your prefered browser developer tools
COOKIE = "YmVLeXR6c0tVUk1hb0IwSGRtTWlQT25tVnBWQ3BWYW9aWkdlNWh6VXhybndsdTI2aWhKKzB5djc4ekNsUjVWUytwRXJWM3ZWZHpzOWZCOFFDSkNsdzE5S0ZibG9OamtYeFdSR1FEUWc3NFlwVjhKbm1pT1JzZk54KzhjdEdtckl3ZHBEbEJTT05zY1ZKdGNDeVFUT2RzdzBLNkRhK2dBR1l3Z2duSFRDM3drNUljeTQzVFVTc3BaTUIwckN3WWpCOVV0UElmQ0lVMEhVbDk4eWc4UHNkN3lYcmRqam1rSG5kNzlDUVJwZ1FkWlJLSDhxTUdPM1dLTnliRmtiS2dhc2JWeVFXR3RPb2ViQWxCbHF0NDUzNHRUN3dVdmU2TmdLKzBnVktRRUFRUENPUm1oNUFkNytZa21ONjIwSFlvZktINGdYSkpHWWo0RndXN2VVN0FHeEZzaDB1Wm9ESSsrN25LSUppV0lEVFI5RUdjQ0Vwd3hYRnovSFE2SU1Td1E0eEd1UW5RbWJjQkU1VUE3Q2tLNGJDOXRFM1l6ZzF3SHgrb3hUNzh0d3NiZ1hyMHFRZHhmWHo0bEsrL3hTZHJVdHRBMFMwNTJWY3o3Z2pNaVpKQ3ZnN2pFMDVvcjJsdjZqNm1TWGJnM0hkalIwSWFOTi8ydER1RjFXcjV0UUlZNHVFdzhRNHlGUFNWdDNUWGw5UjJUN2VJZzRFaXZZc1N5cE1KVjl1OHVNZ0E0PS0tckNiZm5kaWl1K3VEUlhLcUpqTXUydz09--3bf08e3f0ae2f5b2705d4bf3ab2496e02a7b984a"

# Click continue on your existing appointment and get the user_id from the URL: https://ais.usvisa-info.com/es-es/niv/schedule/<user_id>/continue_actions
USER_ID = "48703749"


def check_visa():
    s = requests.Session()
    url = f"https://ais.usvisa-info.com/en-es/niv/schedule/{USER_ID}/appointment/days/7.json?appointments\[expedite\]=false"

    s.headers.update({"Accept": "application/json, text/javascript, /; q=0.01"})
    s.headers.update({"Accept-Language": "en-US,en;q=0.9"})
    s.headers.update({"Connection": "keep-alive"})
    s.headers.update(
        {
            "Referer": "https://ais.usvisa-info.com/en-es/niv/schedule/48703749/appointment"
        }
    )
    s.headers.update({"Sec-Fetch-Dest": "empty"})
    s.headers.update({"Sec-Fetch-Mode": "cors"})
    s.headers.update({"Sec-Fetch-Site": "same-origin"})
    s.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
    )
    s.headers.update(
        {
            "X-CSRF-Token": "+Sz3E7wVyebfChSb4gxsXe8bQJVdW1GuXJHgI8oijBgBXyYPZzdKyE4Cg0eqeFZTntdPYDHfK59vXSR0Ng65jg=="
        }
    )
    s.headers.update({"X-Requested-With": "XMLHttpRequest"})
    s.headers.update(
        {
            "sec-ch-ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"'
        }
    )
    s.headers.update({"sec-ch-ua-mobile": "?0"})
    s.headers.update({"sec-ch-ua-platform": '"macOS"'})

    s.cookies.set("_yatri_session", COOKIE)
    # s.cookies.set("_ga", "GA1.2.757119143.1688058907")
    # s.cookies.set("_gid", "GA1.2.1002456638.1688058907")

    resp = s.get(url)
    print(resp.json())
    date_string = resp.json()[0].get("date")
    year = int(date_string.split("-")[0])
    month = int(date_string.split("-")[1])
    day = int(date_string.split("-")[2])
    date = datetime.date(year, month, day)
    max_date = datetime.date(year=2023, month=9, day=1)
    print(date)
    if resp.status_code != 200:
        return "ERROR CODE {}".format(resp.status_code)
    if date < max_date:
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
