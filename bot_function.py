# For Api calls
from itertools import chain
from datetime import datetime
import requests
import socket
import json

# base_url = "http://127.0.0.1:8000/"
base_url =  "http://mediatechtemple.ml/"


def getIpAddress():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address


def check_ip_auth(token, api):
    if api == 'whatsapp':
        url = base_url + 'IpAPI/whatsapp'
    if api == 'telegram':
        url = base_url + 'IpAPI/telegram'
    if api == 'instagram':
        url = base_url + 'IpAPI/instagram'
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers)
    local_ip = getIpAddress()
    data = list(chain.from_iterable(response.json()))
    print(data)
    if local_ip in data:
        return False
    else:
        return True


def createIp(token, api):
    local_ip_address = getIpAddress()
    if api == 'whatsapp':
        url = base_url + 'createIP/whatsapp'
    if api == 'telegram':
        url = base_url + 'createIP/telegram'
    if api == 'instagram':
        url = base_url + 'createIP/instagram'
    x = {'ip_address': local_ip_address}
    payload = json.dumps(x)
    headers = {'Authorization': f'Token {token}',
               'Content-Type': 'application/json'}
    requests.request("PUT", url, headers=headers, data=payload)


def get_today(token):
    url = base_url + 'serverDateAPI/'
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    response = requests.request("GET", url)
    data = response.json()
    print(data)
    today = datetime.strptime(data, '%Y-%m-%d').date()
    return today


def auth(token, api):
    if api == 'whatsapp':
        url = base_url + 'whatsappAPI/'
    if api == 'telegram':
        url = base_url + 'telegramAPI/'
    if api == 'instagram':
        url = base_url + 'instagramAPI/'

    headers = {'Authorization': f'Token {token}',
               'Content-Type': 'application/json'}
    today = get_today(token)

    response = requests.request("GET", url, headers=headers)
    print(response.json())
    if response.status_code == 200:
        local_ip_address = getIpAddress()
        json_data = response.json()
        remote_ip_address = json_data['ip_address']
        print('remote_ip_address', remote_ip_address,
              'local_ip_address', local_ip_address)
        if remote_ip_address == None:
            check_ip_response = check_ip_auth(token, api)
            if check_ip_response:
                createIp(token, api)
            else:
                print(
                    "Your Ip is already associate with other account Please check your account")
                return False, 'Your Ip is already associate with other account Please check your account'

        if json_data['isActive']:
            demo_date = datetime.strptime(
                json_data['DemoDate'], '%Y-%m-%d').date()
            license_expire_date = json_data['licenceExpireDate']
            print(type(today), type(demo_date), type(license_expire_date))
            print("today", today)
            print('demo_date', demo_date)
            print('license_expire_date', license_expire_date,
                  type(license_expire_date))
            if license_expire_date != None:
                license_expire_date = datetime.strptime(
                    license_expire_date, '%Y-%m-%d').date()
                print('license_expire_date', license_expire_date)
                if(license_expire_date >= today):
                    print("allow with license")
                    return True, f'License valid till {license_expire_date}'
                else:
                    print("Not allowed your License expired")
                    return False, 'Not allowed your License expired'

            elif (demo_date == today):
                print("allow for demo")
                return True, f'License valid till {demo_date}'
            else:
                print('Not allowed Please Activate your account by paying')
                return False, 'Not allowed Please Activate your account by paying'
        else:
            print("Not allowed your account is deactive")
            return False, 'Not allowed your account is deactive'

    else:
        print('Invalid Token')
        return False, 'Invalid Token'


def getVariable(api):
    url = base_url + f"variableAPI/{api}"
    headers = {'Content-Type': 'application/json'}
    response = requests.request("GET", url, headers=headers)
    data = list(chain.from_iterable(response.json()))
    variable = data[0].split("\n")
    print(variable)
    return variable

token = '601827614677c86aef12135972d2767f9b613fe7'
auth(token,'telegram')
# print(get_today(token))

