# from stockfish import Stockfish
from model.stockfish.models import Stockfish, StockfishException
import selenium
import time
import random
import string

def formatCase(case):
    try:
        int(case)
    except ValueError: 
        #format 25 → b5
        fCase = str(string.ascii_lowercase.index(case[:1]) + 1) + case[1:2]    
    else:              
        #format b5 → 25
        fCase = string.ascii_lowercase[int(case[0]) - 1] + case[1:2]
    print("formatCase : " + case + " → " + fCase)    
    return fCase

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.implicitly_wait(5) #attendre si on ne trouve pas l'élément

stockfish = Stockfish("stockfish_15_x64_avx2.exe")

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

# si noir, attendre que l'autre joue
# tant que !checkmate 
    # jouer
    # attendre que l'autre joue
#garder la fenêtre ouverte

best_move = stockfish.get_best_move()
print(best_move)

#jouer le meilleur coup
caseDep = formatCase(best_move[0:2])
caseFin = formatCase(best_move[2:4])

time.sleep(5)

# case de départ
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#board-single > div.piece.wp.square-" + caseDep))).click()
#target = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/chess-board/div[24]") #fonctionne

time.sleep(1)

# case d'arrivée
target = driver.find_element(By.CSS_SELECTOR, "#board-single > div.hint.square-" + caseFin)
print(target.size)
#find_coordinates(caseFin, target.size)
action = ActionChains(driver)
action.move_to_element_with_offset(target, target.size['height'] // 2, target.size['width'] // 2) #pour bien cliquer bien au centre, ne marche pas sinon
action.click()
action.perform()

stockfish.make_moves_from_current_position([best_move])
# print(stockfish.get_board_visual())


time.sleep(10)
