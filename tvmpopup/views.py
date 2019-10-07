import os
import re
import time

from django.http import JsonResponse
from django.shortcuts import render
from django.template.defaultfilters import lower
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

screenshots_folder_name = 'tvmpopup/static/screenshots'
screenshots = {}

options = None
browser = None
domain = None
lang = None
res = None
code = None
segment = 'element'

def initialize(domain_local, lang_local , res_local, code_local):
    global options
    global browser

    global domain
    global lang
    global res
    global code

    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--headless')
    options.add_argument("--test-type")
    options.add_argument('--disable-dev-shm-usage')
    browser = webdriver.Chrome(options=options)

    if not domain_local:
        domain = 'https://player.tvmucho.com'

    if not lang_local:
        lang = "English"

    if not code_local:
        code = "000000"
        browser.execute_script(("localStorage.setItem('activationcode', '{0}')").format(code))

    if res_local:
        res = lower(res_local)
        window_width = re.search(r"\d*(?=x)", res).group()
        window_height = re.search(r"(?<=x)\d*", res).group()
    else:
        window_width = "1920"
        window_height = "1080"

    browser.set_window_size(window_width, window_height)


def get_popup_screenshots(request):
    global screenshots_folder_name
    global options
    global browser
    global screenshots

    global domain
    global lang
    global res
    global code
    global segment

    progress = int(request.GET.get('progress'))

    if progress == 0:
        domain = request.GET.get('domain')
        lang = request.GET.get('language')
        res = request.GET.get('res')
        code = request.GET.get('code')
        segment = request.GET.get('segment')

        initialize(domain, lang, res, code)

        try:
            if not os.path.isdir(screenshots_folder_name):
                os.mkdir(screenshots_folder_name)
        except OSError:
            screenshots_folder_name = ""
        else:
            screenshots_folder_name += "/"

        browser.get(domain)



        if lang and lang != "English":
            browser.execute_script(("localStorage.setItem('selectedLanguage', '{0}')").format(lang))
            browser.refresh()

        return JsonResponse(screenshots, json_dumps_params={'indent': 4}, safe=False)

    if progress == 10:
        save_screenshot('signUpPopup', 'class', None)

        browser.execute_script("$('body').attr('data-state', 'login')")
        save_screenshot('signInPC', 'class', None)

        browser.execute_script("$('body').attr('data-state', 'forgot')")
        save_screenshot('forgotCodePopup', 'class', None)

        browser.execute_script("$('body').attr('data-state', 'signup')")
        save_screenshot('signInPC', 'class', None)

        browser.execute_script("$('body').attr('data-state', 'signupemail')")
        save_screenshot('signUpWithEmailPopup', 'class', None)

        browser.execute_script("$('body').attr('data-state', 'time_over')")
        save_screenshot('timeoverblock', 'class', None)

        browser.execute_script("$('body').attr('data-state', 'online_limit')")
        save_screenshot('online_limit', 'class', None)

        browser.execute_script("$('body').attr('data-state', 'renew')")
        save_screenshot('renewblock', 'class', None)

        browser.execute_script("$('body').attr('data-state', 'disabled_activation_code')")
        save_screenshot('disabled_activation_code', 'class', None)

        browser.execute_script("$('body').attr('data-state', 'smsvalidation')")
        save_screenshot('smsvalidationwindow', 'id', None)

        return JsonResponse(screenshots, json_dumps_params={'indent': 4}, safe=False)

    if progress == 20:
        browser.execute_script("$('body').attr('data-state', 'login')")
        browser.execute_script("$('#activatewindow').hide()")
        browser.execute_script("$('#notsupportedwindow').show()")
        save_screenshot('notsupportedwindow', 'class', None)

        browser.execute_script("$('#notsupportedwindow').hide()")
        browser.execute_script("$('#nomobilebrowsersupport').show()")
        save_screenshot('nomobilebrowsersupport', 'class', None)
        return JsonResponse(screenshots, json_dumps_params={'indent': 4}, safe=False)

    if progress == 30:
        browser.execute_script("$('#nomobilebrowsersupport').hide()")
        browser.execute_script("$('#activatewindow').show()")
        try:
            code_input_field = browser.find_element_by_id("activationcode")
            code_input_field.send_keys(code)
            browser.find_element_by_id("signin").click()
        except:
            pass

        return JsonResponse(screenshots, json_dumps_params={'indent': 4}, safe=False)

    def open_modal(modal_id, button_selector):
        browser.execute_script(("$('#{0}').remodal().open()").format(modal_id))
        time.sleep(1)
        save_screenshot(modal_id, 'id', None)
        if button_selector:
            try:
                browser.find_element_by_css_selector(button_selector).click()
                save_screenshot(modal_id, 'id', button_selector)
            except:
                pass

        browser.execute_script(("$('#{0}').remodal().close()").format(modal_id))

        return JsonResponse(screenshots, json_dumps_params={'indent': 4}, safe=False)

    wait = WebDriverWait(browser, 60)
    wait.until(EC.element_to_be_clickable((By.ID, 'settings_btn')))

    if progress == 40:
        open_modal('share-modal', '.share-button.email')
        open_modal('help-panel', None)

        return JsonResponse(screenshots, json_dumps_params={'indent': 4}, safe=False)

    if progress == 50:
        open_modal('continue-watching-modal', None)
        open_modal('registration-modal', None)

        return JsonResponse(screenshots, json_dumps_params={'indent': 4}, safe=False)

    if progress == 60:
        open_modal('congratulations-modal', None)
        open_modal('debug-data-modal', None)

        return JsonResponse(screenshots, json_dumps_params={'indent': 4}, safe=False)

    if progress == 70:
        open_modal('panel1-rate-modal', None)
        open_modal('panel2-rate-modal', None)
        open_modal('panel3-rate-modal', None)
        open_modal('tvbox-modal', None)

        return JsonResponse(screenshots, json_dumps_params={'indent': 4}, safe=False)

    if progress == 80:
        open_modal('modal1', None)
        open_modal('modal2', None)
        open_modal('fire-keyboard', None)
        open_modal('captcha-modal', None)

        return JsonResponse(screenshots, json_dumps_params={'indent': 4}, safe=False)

    if progress == 90:
        open_modal('account-exists-modal', None)
        open_modal('notifications-info-modal', None)

        return JsonResponse(screenshots, json_dumps_params={'indent': 4}, safe=False)

    browser.quit()
    return JsonResponse(screenshots, json_dumps_params={'indent': 4}, safe=False)

def index_view(request):
    return render(request, 'index.html')


def save_screenshot(name, by, button_selector):
    global screenshots_folder_name
    global screenshots
    global browser
    global segment

    if button_selector:
        filename = "{1}-{2}".format(screenshots_folder_name, button_selector, name)
        image_path = "{0}{1}.png".format(screenshots_folder_name, filename)
    else:
        filename = name
        image_path = "{0}{1}.png".format(screenshots_folder_name, filename)

    screenshots[filename] = image_path.replace('tvmpopup', '')

    if (segment == 'fullscreen'):
        return browser.save_screenshot(image_path)
    try:
        if by == 'class':
            browser.find_element_by_class_name(name).screenshot(image_path)
        else:
            browser.find_element_by_id(name).screenshot(image_path)
    except:
        return browser.save_screenshot(image_path)