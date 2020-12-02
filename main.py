import my_constants as consts, email.utils
import emails_db as db, random
from selenium import webdriver
from time import sleep

email_addresses_list = []

def create_browser():
    return webdriver.Chrome('C:\Program Files (x86)\webdrivers\chromedriver.exe')


def enter_mail_page():
    browser.maximize_window()
    browser.get(consts.MAIL_SERVER)
    browser.implicitly_wait(10)



def get_element_by_selector(selector):
    return browser.find_element_by_css_selector(selector)


def enter_input(input_element, input):
    input_element.send_keys(input)


def click_element(element_to_click):
    element_to_click.click()
    browser.implicitly_wait(10)


def enter_mail():
    selector = 'input[id="login-username"]'
    username_box = get_element_by_selector(selector)
    enter_input(username_box, consts.USER_NAME)
    selector = 'input[id="login-signin"]'
    next_button = get_element_by_selector(selector)
    click_element(next_button)
    selector = 'input[id="login-passwd"]'
    password_box = get_element_by_selector(selector)
    enter_input(password_box, consts.PASSWORD)
    selector = 'button[id="login-signin"]'
    login_button = get_element_by_selector(selector)
    click_element(login_button)


def validate_address(address):
    if len(address) < len('a@b.c'):
        return ''
    length = len(address)
    index = 0
    while index in range(length):
        if address[index].lower() not in "abcdefghijklmnopqrstuvwxyz@.!#$%&*+-/=?^_`{|}~0123456789":
            temp_address = address[:index]
            if len(temp_address) < 6:
                address = address[index + 1:]
                length = len(address)
                index -= 1
            else:
                address = temp_address
                break
        index += 1

    if '.' not in address or '@' not in address:
        return ''
    if address[0] == '.' or address[0] == '@':
        return ''
    if address.count('@') > 1:
        return ''
    if address.rfind('.') < address.rfind('@'):
        return ''
    return address


def sift_mails():
    selector = 'span[data-test-id="message-subject"][title*="הגשת מועמדות"]'
    mail_list = browser.find_elements_by_css_selector(selector)

    index = 0
    while index in range(len(mail_list)):
        click_element(mail_list[index])
        print('clicked ', index + 1, 'out of', len(mail_list))
        index += 1

        address = validate_address(parse_mail_text())
        if address != '':
            email_addresses_list[-1].append(address)
            print('email list after append: ',email_addresses_list)
        else:
            if len(email_addresses_list) > 0:
                if len(email_addresses_list[-1]) < 2:
                    email_addresses_list.pop()
                    print('email list after pop: ', email_addresses_list)
        selector = 'span[data-test-id="message-subject"][title*="הגשת מועמדות"]'
        mail_list = browser.find_elements_by_css_selector(selector)
        print('mail_list length', len(mail_list))


def check_for_phone():
    selector = 'div[class="jb_0 X_6MGW N_6Fd5"]'
    mail_body = browser.find_element_by_css_selector(selector)
    text = mail_body.text.replace('\n', ' ').replace('-','')
    words = text.split(' ')
    for word in words:
        if word.isdigit():
            print(word)
            sleep(2)
            return True
    print('No phone')
    sleep(2)
    return False


def parse_mail_text():
    if not check_for_phone():
        return return_to_inbox('')

    selector = 'div[class="jb_0 X_6MGW N_6Fd5"]'
    mail_body = browser.find_element_by_css_selector(selector)
    address = get_email_address(mail_body)
    if address != '':
        email_addresses_list.append([mail_body.text])
        print(email_addresses_list)
    return return_to_inbox(address)


def return_to_inbox(result):
    selector = 'span[data-test-folder-name="Inbox"]'
    inbox_button = browser.find_element_by_css_selector(selector)
    click_element(inbox_button)
    return result


def get_email_address(mail_body):
    text = mail_body.text.replace('\n', ' , ').replace('-',' ')
    email_addresses = email.utils.getaddresses([text])
    for tuple_element in email_addresses:
        if tuple_element[1] != '' and '@' in tuple_element[1]:
            if ' ' in tuple_element[1]:
                words = tuple_element[1].split(' ')
                for word in words:
                    if '@' in word:
                        print('email:', word)
                        return word
            else:
                print('email:', tuple_element[1])
                return tuple_element[1]
    print('No address')
    return ''


def save_applicant_to_db(index):
    applicant = {
        'email_address': email_addresses_list[index][1],
        'email_text': email_addresses_list[index][0]
    }
    db.push_entry(applicant)


def send_reply():
    # reply_address = 'enfer0666@gmail.com'
    print('email_addresses_list length: ', len(email_addresses_list))
    reply = 'Your application has been received and is being examined, good luck, john doe'
    selector = 'a[data-test-id="compose-button"]'
    compose_button = get_element_by_selector(selector)
    click_element(compose_button)

    for index in range(len(email_addresses_list)):
        reply_address = email_addresses_list[index][1]
        selector = 'a[data-test-id="compose-button"]'
        compose_button = get_element_by_selector(selector)
        click_element(compose_button)
        selector = 'input[id="message-to-field"]'
        recipient_box = get_element_by_selector(selector)
        selector = 'input[data-test-id="compose-subject"]'
        message_subject = get_element_by_selector(selector)
        selector = 'button[data-test-id="compose-send-button"]'
        send_button = get_element_by_selector(selector)

        enter_input(recipient_box, reply_address)
        enter_input(message_subject, reply)
        click_element(send_button)
        print(f'reply sent to {reply_address}')
        save_applicant_to_db(index)


browser = create_browser()
enter_mail_page()
enter_mail()
sift_mails()
send_reply()

if len(email_addresses_list) > 0:
    print('getting random entry')
    index = random.randint(0, len(email_addresses_list) - 1)
    db.get_entry(email_addresses_list[index][1])

browser.quit()
# if __name__ == '__main__':
#     pass
