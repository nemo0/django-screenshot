
from cmath import e
from html2image import Html2Image
from hashlib import sha1
import hmac
from rest_framework.decorators import api_view


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

import urllib.parse as ul

import requests
import base64
import json

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep


def sayhello(request):
    return JsonResponse({'message': 'Hello, World!'})

# Method 1: Take Screenshot with Selenium


@csrf_exempt
@api_view(['GET', 'POST'])
def screenshotWithSelenium(request):
    if request.method == 'POST':
        DATA = json.loads(request.body)
        if DATA['website'] == '':
            return JsonResponse({'error': 'No website provided'})
        else:
            try:
                driver = webdriver.Chrome(ChromeDriverManager().install())
                driver.get(DATA['website'])
                sleep(5)
                driver.get_screenshot_as_file('selenium.png')
                driver.quit()
                print('screenshot taken')
                return JsonResponse({'status': 'success'})
            except:
                return JsonResponse({'error': 'Error taking screenshot'})
    elif request.method == 'GET':
        return JsonResponse({'message': 'Hello. Try passing a website in the POST body.'})

# Method 2: Take Screenshot with Google PageSpeed Insights


@csrf_exempt
@api_view(['GET', 'POST'])
def screenshotWithPageSpeed(request):
    if request.method == 'POST':
        DATA = json.loads(request.body)
        if DATA['website'] == '':
            return JsonResponse({'error': 'No website provided'})
        else:
            url = DATA['website']
            urle = ul.quote_plus(url)
            image_path = 'pagespeed.png'

            try:
                strategy = 'desktop'
                u = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?strategy={strategy}&url={urle}"

                j = requests.get(u).json()
                ss_encoded = j['lighthouseResult']['audits']['final-screenshot']['details']['data'].replace(
                    "data:image/jpeg;base64,", "")
                ss_decoded = base64.b64decode(ss_encoded)
                with open(image_path, 'wb+') as f:
                    f.write(ss_decoded)

                return JsonResponse({'status': 'success'})
            except Exception as e:
                raise e
                return JsonResponse({'error': 'Error taking screenshot'})

    elif request.method == 'GET':
        return JsonResponse({'message': 'Hello. Try passing a website in the POST body.'})


# Method 3: Take Screenshot with HTML2Image


@csrf_exempt
@api_view(['GET', 'POST'])
def screenshotWithHtml2Image(request):
    if request.method == 'POST':
        DATA = json.loads(request.body)
        if DATA['website'] == '':
            return JsonResponse({'error': 'No website provided'})
        else:
            url = DATA['website']
            hti = Html2Image()
            hti.screenshot(url=url, save_as='html2image.png')
            return JsonResponse({'status': 'success'})
    elif request.method == 'GET':
        return JsonResponse({'message': 'Hello. Try passing a website in the POST body.'})
    else:
        return JsonResponse({'error': 'Error taking screenshot'})


try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

# Initialize urlbox


def urlbox(args):
    apiKey = 'xxxxxxxxxxxxxx'
    apiSecret = 'xxxxxxxxxxxxxxxxxxxxxxxx'
    queryString = urlencode(args, True)
    hmacToken = hmac.new(str.encode(apiSecret), str.encode(queryString), sha1)
    token = hmacToken.hexdigest().rstrip('\n')
    return "https://api.urlbox.io/v1/%s/%s/png?%s" % (apiKey, token, queryString)

# Method 4: Take Screenshot with urlbox


@csrf_exempt
@api_view(['GET', 'POST'])
def screenshotWithUrlbox(request):
    if request.method == 'POST':
        DATA = json.loads(request.body)
        if DATA['website'] == '':
            return JsonResponse({'error': 'No website provided'})
        else:
            url = DATA['website']
            argsDict = {
                'url': url,
                'width': '1920',
                'height': '1080',
                'format': 'png',
                'quality': '100',
            }
            try:
                urlBoxUrl = urlbox(argsDict)
                print('screenshot taken')
                resp = requests.get(urlBoxUrl)
                open('urlbox.png', 'wb').write(resp.content)
                return JsonResponse({'status': 'success', 'url': urlBoxUrl})
            except:
                return JsonResponse({'error': 'Error taking screenshot'})
    elif request.method == 'GET':
        return JsonResponse({'message': 'Hello. Try passing a website in the POST body.'})
