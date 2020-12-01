import my_constants as consts, email.utils, re
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
    for index in range(len(address)):
        if address[index].lower() not in "abcdefghijklmnopqrstuvwxyz@.!#$%&*+-/=?^_`{|}~0123456789":
            address = address[:index]
            break

    if '.' not in address or '@' not in address:
        return ''
    if address[0] == '.':
        return ''
    if address.count('@') > 1:
        return ''
    if address.rfind('.') < address.rfind('@'):
        return ''
    return address



def sift_mails():
    # email_addressess = []
    selector = 'span[data-test-id="message-subject"][title*="הגשת מועמדות"]'
    mail_list = browser.find_elements_by_css_selector(selector)
    for index in range(len(mail_list)):
        click_element(mail_list[index])
        address = validate_address(parse_mail_text())
        if address != '':
            email_addresses_list.append(address)
        selector = 'span[data-test-id="message-subject"][title*="הגשת מועמדות"]'
        mail_list = browser.find_elements_by_css_selector(selector)


def look_for_phone():
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
    look_for_phone()
    selector = 'div[class="jb_0 X_6MGW N_6Fd5"]'
    mail_body = browser.find_element_by_css_selector(selector)
    address = get_email_addresss(mail_body)
    #return to inbox
    selector = 'span[data-test-folder-name="Inbox"]'
    inbox_button = browser.find_element_by_css_selector(selector)
    click_element(inbox_button)
    return address


def get_email_addresss(mail_body):
    email_addresses = email.utils.getaddresses([mail_body.text])
    for tuple_element in email_addresses:
        if tuple_element[1] != '' and '@' in tuple_element[1]:
            if ' ' in tuple_element[1]:
                words = tuple_element[1].split(' ')
                for word in words:
                    if '@' in word:
                        return word
            else:
                return tuple_element[1]


def send_reply():
    reply_address = 'enfer0666@gmail.com'
    reply = 'Your application has been received and is being examined, good luck, john doe'
    #<input role="combobox" aria-autocomplete="both" aria-owns="react-typehead-list-to" aria-expanded="false" aria-label="" id="message-to-field" class="select-input react-typeahead-input input-to Z_N ir_0 j_n y_Z2hYGcu q_52qC k_w W_6D6F H_6NIX M_0 b_0 P_SMJKi A_6EqO D_X p_a L_0 B_0" placeholder="" type="text" spellcheck="false" autocapitalize="off" autocomplete="off" autocorrect="off" value="">
    #<input data-test-id="compose-subject" spellcheck="true" autocorrect="off" aria-label="Subject" placeholder="Subject" class="q_T y_Z2hYGcu je_0 jb_0 X_0 N_fq7 G_e A_6EqO C_Z281SGl ir_0 P_0 bj3_Z281SGl b_0 j_n d_72FG em_N" value="">
    #<button tabindex="-1" class="q_Z2aVTcY e_dRA k_w r_P H_6VdP s_3mS2U en_0 M_1gLo4F V_M cZ1RN91d_n y_Z2hYGcu A_6EqO u_e69 b_0 C_52qC I4_Z29WjXl ir3_1JO2M7 it3_dRA" type="button" data-test-id="compose-send-button" title="Send this email"><span>Send</span></button>
    selector = 'a[data-test-id="compose-button"]'
    compose_button = get_element_by_selector(selector)
    click_element(compose_button)
    # selector = 'input[id="message-to-field"]'
    # recipient_box = get_element_by_selector(selector)
    # selector = 'input[data-test-id="compose-subject"]'
    # message_subject = get_element_by_selector(selector)
    # selector = 'button[data-test-id="compose-send-button"]'
    # send_button = get_element_by_selector(selector)

    for index in range(len(email_addresses_list)):
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

browser = create_browser()
enter_mail_page()
enter_mail()
sift_mails()
# look_for_phone()
#save_to_data_base()
# send_reply()

# if __name__ == '__main__':
#     pass
