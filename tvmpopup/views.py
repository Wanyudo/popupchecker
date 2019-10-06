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


def getPopupScreenshots(request):
    screenshots_folder_name = 'tvmpopup/static/screenshots'

    screenshots = {}

    try:
        if not os.path.isdir(screenshots_folder_name):
            os.mkdir(screenshots_folder_name)
    except OSError:
        screenshots_folder_name = ""
    else:
        screenshots_folder_name += "/"

    domain = request.GET.get('domain')
    if not domain:
        domain = 'https://player.tvmucho.com'

    lang = request.GET.get('language')
    if not lang:
        lang = "English"

    res = request.GET.get('res')
    if res:
        res = lower(res)
        window_width = re.search(r"\d*(?=x)", res).group()
        window_height = re.search(r"(?<=x)\d*", res).group()
    else:
        window_width = "1920"
        window_height = "1080"

    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--headless')
    options.add_argument("--test-type")
    options.add_argument('--disable-dev-shm-usage')
    browser = webdriver.Chrome(options=options)
    browser.get(domain)

    code = request.GET.get('code')
    if not code:
        code = "000000"
        browser.execute_script(("localStorage.setItem('activationcode', '{0}')").format(code))

    if lang and lang != "English":
        browser.execute_script(("localStorage.setItem('selectedLanguage', '{0}')").format(lang))
        browser.refresh()

    browser.set_window_size(window_width, window_height)

    def save_screenshot(name, by, button_selector):
        if button_selector:
            filename = "{1}-{2}".format(screenshots_folder_name, button_selector, name)
            image_path = "{0}{1}.png".format(screenshots_folder_name, filename)
        else:
            filename = name
            image_path = "{0}{1}.png".format(screenshots_folder_name, filename)

        screenshots[filename] = image_path.replace('tvmpopup', '')

        if by == 'class':
            browser.find_element_by_class_name(name).screenshot(image_path)
        else:
            browser.find_element_by_id(name).screenshot(image_path)

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
    save_screenshot('smsvalidation', 'id', None)

    browser.execute_script("$('body').attr('data-state', 'login')")
    browser.execute_script("$('#activatewindow').hide()")
    browser.execute_script("$('#notsupportedwindow').show()")
    save_screenshot('notsupportedwindow', 'class', None)

    browser.execute_script("$('#notsupportedwindow').hide()")
    browser.execute_script("$('#nomobilebrowsersupport').show()")
    save_screenshot('nomobilebrowsersupport', 'class', None)

    browser.execute_script("$('#nomobilebrowsersupport').hide()")
    browser.execute_script("$('#activatewindow').show()")
    code_input_field = browser.find_element_by_id("activationcode")
    code_input_field.send_keys(code)
    browser.find_element_by_id("signin").click()

    def open_modal(modal_id, button_selector):
        browser.execute_script(("$('#{0}').remodal().open()").format(modal_id))
        time.sleep(1)
        save_screenshot(modal_id, 'id', None)
        if button_selector:
            browser.find_element_by_css_selector(button_selector).click()
            save_screenshot(modal_id, 'id', button_selector)

        browser.execute_script(("$('#{0}').remodal().close()").format(modal_id))


    # Wait until website loads
    browser.implicitly_wait(60)
    try:
        wait = WebDriverWait(browser, 60)
        wait.until(EC.element_to_be_clickable((By.ID, 'settings_btn')))

        open_modal('share-modal', '.share-button.email')
        open_modal('help-panel', None)
        open_modal('continue-watching-modal', None)
        open_modal('registration-modal', None)
        open_modal('congratulations-modal', None)
        open_modal('debug-data-modal', None)
        open_modal('panel1-rate-modal', None)
        open_modal('panel2-rate-modal', None)
        open_modal('panel3-rate-modal', None)
        open_modal('tvbox-modal', None)
        open_modal('modal1', None)
        open_modal('modal2', None)
        open_modal('fire-keyboard', None)
        open_modal('captcha-modal', None)
        open_modal('account-exists-modal', None)
        open_modal('notifications-info-modal', None)

    finally:
        browser.quit()
        return JsonResponse(screenshots, json_dumps_params={'indent': 4}, safe=False)

def index_view(request):
    return render(request, 'index.html')