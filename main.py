from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep, time
from collections.abc import Iterable
from time import sleep
import traceback

# print(bcolors.FAIL + text + bcolors.ENDC)
from bcolors import bcolors


def vk_print(msg):
    file = open('vk_data.txt', 'r', encoding="utf8")
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]
    lines = [line for line in lines if line]
    file.close()

    if len(lines) < 3:
        raise Warning(
            bcolors.WARNING + """Внесите в начало файла vk_data.txt 2 строчки: свои Логин и Пароль от Вконтакте
3 строчка - это адрес диалога, куда вы хотите отправить сообщение""" + bcolors.ENDC)

    vk_driver.get(lines[2].strip())

    time_start = time()
    while len(vk_driver.find_elements(By.XPATH, '//*[@autocomplete="username"]')) == 0 and \
            time() - time_start < 5.0:
        sleep(0.1)
    vk_driver.find_elements(By.XPATH, '//*[@autocomplete="username"]')[0].send_keys(lines[0] + "\n")
    time_start = time()
    while len(vk_driver.find_elements(By.XPATH, '//*[@autocomplete="current-password"]')) == 0 and \
            len(vk_driver.find_elements(By.XPATH, "//*[text()='Войти при помощи пароля']")) == 0 and \
            time() - time_start < 5.0:
        sleep(0.1)
    if len(vk_driver.find_elements(By.XPATH, "//*[text()='Войти при помощи пароля']")) != 0:
        vk_driver.find_elements(By.XPATH, "//*[text()='Войти при помощи пароля']")[0].click()
    time_start = time()
    while len(vk_driver.find_elements(By.XPATH, '//*[@autocomplete="current-password"]')) == 0 and \
            time() - time_start < 5.0:
        sleep(0.1)
    vk_driver.find_elements(By.XPATH, '//*[@autocomplete="current-password"]')[0].send_keys(lines[1] + "\n")

    while len(vk_driver.find_elements(By.XPATH, '//*[@role="textbox"]')) == 0:
        sleep(0.1)

    for line in msg.splitlines():
        vk_driver.find_elements(By.XPATH, '//*[@role="textbox"]')[0].send_keys(line)
        vk_driver.find_elements(By.XPATH, '//*[@role="textbox"]')[0].send_keys(Keys.LEFT_SHIFT + Keys.RETURN)

    vk_driver.find_elements(By.XPATH, '//*[@role="textbox"]')[0].send_keys("\n")

    time_start = time()
    while len(vk_driver.find_elements(By.XPATH, '//*[@role="textbox"]')[0].text) != 0 and \
            time() - time_start < 5.0:
        sleep(0.1)


def load_data():
    file = open('user_data.txt', 'r', encoding="utf8")
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]
    lines = [line for line in lines if line]
    file.close()
    if len(lines) < 2:
        raise Warning(
            bcolors.WARNING + "Внесите в начало файла user_data.txt 2 строчки: свои Логин и Пароль от ИСУ" + bcolors.ENDC)

    ISU_LOGIN = lines[0].strip()
    ISU_PASSWORD = lines[1].strip()

    SELECTED_DISCIPLINES = [lines[i].strip() for i in range(2, len(lines))]
    if len(SELECTED_DISCIPLINES) == 0:
        print(bcolors.WARNING + """Вы не выбрали дисциплины, которые должен автоматически выбирать бот. 
    После успешного входа в систему, отобразится весь список имён доступных дисциплин.
    Пожалуйста, скопируйте имена выбранных из них и вставьте как новые строчки в user_data.txt

    Если у какой-то дисциплины можно выбрать семестр, поставьте номер семестра после имени через знак |
    номер семестра начинается с 1""" + bcolors.ENDC)

    return ISU_LOGIN, ISU_PASSWORD, SELECTED_DISCIPLINES


def login():
    """
    https://my.itmo.ru/election
    https://dev.my.itmo.su/election
    :return:
    """
    driver.get("https://my.itmo.ru/election")

    """
    Ожидание прогрузки страницы
    """
    while len(driver.find_elements(By.XPATH, '//*[@id="username"]')) == 0:
        sleep(0.1)

    user_textfields = driver.find_elements(By.XPATH, '//*[@id="username"]')
    user_textfields[0].send_keys(ISU_LOGIN)

    password_textfields = driver.find_elements(By.XPATH, '//*[@id="password"]')
    password_textfields[0].send_keys(ISU_PASSWORD)

    log_in_button = driver.find_element(By.XPATH, '//*[@id="kc-login"]')
    log_in_button.click()

    """
    Ожидание прогрузки страницы
    """
    time_start = time()
    while len(driver.find_elements(By.CLASS_NAME, 'disciplines-grid')) == 0 and time() - time_start < 5.0:
        sleep(0.1)
    if len(driver.find_elements(By.CLASS_NAME, 'disciplines-grid')) == 0:
        raise Exception(bcolors.FAIL + "Расписание не грузится" + bcolors.ENDC)

    print(bcolors.OKGREEN + f"""logged into {ISU_LOGIN}""" + bcolors.ENDC)

    get_disciplines()


def get_disciplines():
    """
    Ожидание прогрузки страницы
    """
    while len(driver.find_elements(By.CLASS_NAME, 'card-body')) == 0:
        sleep(0.1)

    """
    Тела карточек для записи:
    /html/body/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div[1]/div/div/div[1]/div
    
    Имя дисциплины:
    /html/body/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div[1]/div/div/div[1]/div/div/div[1]/div/div/div[1]/text()
    div/div[1]/div/div/div[1] -> text
    
    Кнопка:
    /html/body/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div[1]/div/div/div[2]/div/div/div[2]/div[2]/button[1]
    /html/body/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div[1]/div/div/div[2]/div/div/div[2]/div[2]/button[1]
    
    div/div[2]/div[2]/button[1] -> click()
    """
    discipline_classes = driver.find_elements(By.CLASS_NAME, "card-body")

    discipline_map = {}
    if len(SELECTED_DISCIPLINES) == 0:
        print(bcolors.WARNING + f"Дисциплин для записи доступно: {len(discipline_classes)}" + bcolors.ENDC)
    for discipline in discipline_classes:
        name = discipline.find_elements(By.XPATH, "div/div[1]/div/div/div[1]")[0].text
        discipline_map[name.strip()] = discipline
        if len(SELECTED_DISCIPLINES) == 0:
            print(name)
    if len(SELECTED_DISCIPLINES) == 0:
        raise Warning(bcolors.WARNING + """Пожалуйста, занесите названия выбранных вами дисциплин в файл user_data.txt
как новые строчки после первых двух с логином и паролем""" + bcolors.ENDC)

    return discipline_map


def make_vote(discipline, semesters=None):
    discipline.find_elements(By.XPATH, "div/div[2]/div[2]/button[1]")[0].click()
    if semesters is not None:
        while len(driver.find_elements(By.CLASS_NAME, "popover")) == 0:
            sleep(0.1)
        popover = driver.find_elements(By.CLASS_NAME, "popover")[0]
        info = []
        unparsed_info = popover.text.splitlines()
        line_id = 0
        while line_id < len(unparsed_info) - 2:
            line = unparsed_info[line_id]
            if line[0].isdigit() and "/" not in line[0]:
                info.append([])
                places = unparsed_info[line_id + 2].split("/")
                if len(places) == 2:
                    info[-1].append(int(line[0]))
                    info[-1].append(int(places[1]) - int(places[0]))
                line_id += 3
            else:
                line_id += 1

        buttons = popover.find_elements(By.CLASS_NAME, "custom-control-label")
        semesters_vector = list(map(int, semesters.split(" ")))

        for selected_semester in semesters_vector:
            for pair_id in range(len(info)):
                pair = info[pair_id]
                if pair[0] == selected_semester and pair[1] > 0:
                    buttons[pair_id].click()
                    popover.find_elements(By.CLASS_NAME, "btn-primary")[0].click()
                    return

        name = discipline.find_elements(By.XPATH, "div/div[1]/div/div/div[1]")[0].text
        raise Warning(bcolors.FAIL + f"""Не удалось записаться на дисциплину:
{name}
в семестры:
{semesters_vector}
Пожалуйста, измените свой выбор или подождите, пока люди поменяют свои записи""" + bcolors.ENDC)


def vote_for_disciplines(selected_disciplines):
    for selected_discipline in selected_disciplines:
        discipline_map = get_disciplines()

        discipline_info = list(map(str.strip, selected_discipline.split("|")))
        if len(discipline_info) == 1:
            discipline_info.append(None)

        discipline = None
        if discipline_info[0] in discipline_map.keys():
            discipline = discipline_map[discipline_info[0]]
            make_vote(discipline, discipline_info[1])
        else:
            for discipline_key in discipline_map.keys():
                if discipline_key.startswith(discipline_info[0]):
                    # WARNING
                    discipline = discipline_map[discipline_key]
                    make_vote(discipline, discipline_info[1])
                    break

        if discipline is None:
            raise Warning(bcolors.WARNING + f"""Дисциплина н существует:
{discipline_info[0]}
""" + bcolors.ENDC)


def accept_disciplines():
    time_start = time()
    while len(driver.find_elements(By.XPATH, '//*[@id="schedule-btn"]')) == 0 and time() - time_start < 5.0:
        sleep(0.1)
    if len(driver.find_elements(By.XPATH, '//*[@id="schedule-btn"]')) == 0:
        raise Exception(bcolors.FAIL + "Расписание не грузится" + bcolors.ENDC)
    schedule_btn = driver.find_elements(By.XPATH, '//*[@id="schedule-btn"]')[0]
    button = schedule_btn.find_elements(By.XPATH, 'button')[0]

    button.click()
    while schedule_btn.get_attribute("aria-describedby") is None:
        sleep(0.1)
    aria_describedby = schedule_btn.get_attribute("aria-describedby")
    aria_describedby = driver.find_elements(By.XPATH, f'//*[@id="{aria_describedby}"]')[0]
    CRINGE = aria_describedby.text
    class_sign_up_left = CRINGE[CRINGE.rfind(":") + 1:]
    class_sign_up_left = int(class_sign_up_left)

    if class_sign_up_left != 0:
        raise Warning(bcolors.WARNING + CRINGE + bcolors.ENDC)

    disabled = button.get_attribute("disabled")
    if disabled is not None and disabled:
        print(bcolors.OKCYAN + """Кнопка выбора не активна""" + bcolors.ENDC)
        driver.execute_script("arguments[0].removeAttribute('disabled')", button)
    button.click()

    time_start = time()
    while len(driver.find_elements(By.XPATH,
                                   '//*[@src="/img/election/error_robot.svg"]')) == 0 and time() - time_start < 5.0:
        sleep(0.1)
    if len(driver.find_elements(By.XPATH, '//*[@src="/img/election/error_robot.svg"]')) == 0:
        raise EOFError(f"""
Запись успешно осуществлена (во всяком случае, не возникло ошибки). Текст во время записи:
{CRINGE}
""")

    if class_sign_up_left == 0:
        raise Exception(bcolors.FAIL + CRINGE + bcolors.ENDC)


while True:
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--disable-setuid-sandbox")
        options.add_argument("--start-maximized")
        options.add_argument("--window-position=10000,0")
        driver = webdriver.Chrome(chrome_options=options)

        # executable_path=r'C:\PROGRAMS\chromedriver_win32\chromedriver.exe'
        options.add_argument('--headless')
        vk_driver = webdriver.Chrome(chrome_options=options)

        ISU_LOGIN, ISU_PASSWORD, SELECTED_DISCIPLINES = load_data()

        login()

        vote_for_disciplines(SELECTED_DISCIPLINES)

        accept_disciplines()

    except EOFError as e:
        print(e)
        msg = f"""@all

Запись Открыта! Слава ИСУ-мительному качеству сервиса!

{e}"""
        driver.set_window_position(0, 0)
        driver.fullscreen_window()
        try:
            vk_print(msg)
        except Exception as e:
            print(e)
        sleep(1e6)
    except Warning as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        driver.close()
        vk_driver.close()
