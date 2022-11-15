# from stockfish import Stockfish
from model.stockfish.models import Stockfish, StockfishException
import selenium
import time
import random
import string
import re

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def formatCase(case):
    try:
        int(case)
    except ValueError: 
        #format 25 → b5
        fCase = str(string.ascii_lowercase.index(case[:1]) + 1) + case[1:2]    
    else:              
        #format b5 → 25
        fCase = string.ascii_lowercase[int(case[0]) - 1] + case[1:2]
    #print("formatCase : " + case + " → " + fCase)    
    return fCase

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.implicitly_wait(5) #attendre si on ne trouve pas l'élément

stockfish = Stockfish("stockfish_15_x64_avx2.exe")

def INIT():

    #stockfish.set_position(['e2e4', 'e7e5'])

    driver.get('https://www.chess.com/play/online')

    time.sleep(1)

    bPlay = driver.find_element(By.CSS_SELECTOR, ".ui_v5-button-component.ui_v5-button-primary.ui_v5-button-large.ui_v5-button-full")
    bPlay.click()

    time.sleep(1)

    bAdvanced = driver.find_element(By.XPATH, "//label[4]/div[2]")
    bAdvanced.click()

    time.sleep(1)

    bGuest = driver.find_element(By.ID, "guest-button")
    bGuest.click()

    #attendre que le board soit chargé
    time.sleep(5)   
    clockWhite = driver.find_element(By.CSS_SELECTOR, "div[id^='board-layout-player-'] > div > div.clock-component.clock-white.player-clock > span")
    clockBlack = driver.find_element(By.CSS_SELECTOR, "div[id^='board-layout-player-'] > div > div.clock-component.clock-black.player-clock > span")
    

    timeWhiteSec = int(clockWhite.text[-2:])
    timeBlackSec = int(clockBlack.text[-2:])

    print(timeWhiteSec)
    print(timeBlackSec)

    print("trouvé")
    while timeWhiteSec == 0 and timeBlackSec == 0:
        time.sleep(0.1)
    print("commencé")    

def JOUER_COUP():
    best_move = stockfish.get_best_move()
    print("jouer coup : " + best_move)

    caseDep = formatCase(best_move[0:2])
    caseFin = formatCase(best_move[2:4])

    time.sleep(1)

    # case de départ
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#board-single > div[class^='piece'][class$='square-" + caseDep + "']"))).click()

    time.sleep(1)

    # case d'arrivée
    target = driver.find_element(By.CSS_SELECTOR, "#board-single > [class*='hint'][class$='square-" + caseFin + "']")
    #print(target.size)
    action = ActionChains(driver)
    action.move_to_element_with_offset(target, target.size['height'] // 2, target.size['width'] // 2) #pour bien cliquer bien au centre, ne marche pas sinon
    action.click()
    action.perform()

    stockfish.make_moves_from_current_position([best_move])

def ATTENDRE_COUP_ADVERSE():
    onAttend = True
    """
    if onJoueLesNoirs and firstLoop:
        classRef = "element-pool"
    else:
        """
    classRef2 = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/chess-board/div[2]").get_attribute("class") #référence pour comparaison
    classRef3 = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/chess-board/div[3]").get_attribute("class") #référence pour comparaison
    while onAttend:
        classNow2 = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/chess-board/div[2]").get_attribute("class")
        classNow3 = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/chess-board/div[3]").get_attribute("class")
        if classNow2 != classRef2 or classNow3 != classRef3:
            onAttend = False
            break
        else:
            time.sleep(1)

    caseDep = formatCase(classNow2[-2:])
    caseFin = formatCase(classNow3[-2:])

    try:
        stockfish.make_moves_from_current_position([caseDep + caseFin])
        print("villain joue : " + caseDep + caseFin)

    except ValueError:
        #parfois, les highlights ne sont pas alimentés dans le bon sens...
        stockfish.make_moves_from_current_position([caseFin + caseDep])
        print("villain joue : " + caseFin + caseDep)



# MAIN    
INIT()
onJoueLesNoirs = re.search("flipped", driver.find_element(By.ID, "board-single").get_attribute("class"))
if onJoueLesNoirs: 
    print("noirs")
    ATTENDRE_COUP_ADVERSE()
else:
    print("blancs")
while True: #tant que !checkmate
    JOUER_COUP()
    # print(stockfish.get_board_visual())
    ATTENDRE_COUP_ADVERSE()
    
#garder la fenêtre ouverte
time.sleep(10)













