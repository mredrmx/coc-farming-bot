import random
import time
import pyautogui

# --------------------------------------------- DE --------------------------------------------- #
# Hier sind alle Angriffe gecoded. Sehr nervige Handarbeit, 4 verschiedene Seiten der Base, um den Bot
# unauffälliger Supercell gegenüber zu machen.

# Simpel gesagt: Es wird in die korrespondierende Ecke/Seite der Base gedragged, dann werden entlang dieser Seite die
# War Machine, der King, die Queen, die E-Dragons platziert, danach der Warden, die Loons und die Rage-Spells.
# Anschließend wird die Warden-Fähigkeit gezündet und zwei weitere Rage-Spells weiter mittig in der Base + ein Zap
# in ca. der Mitte der Base abgeworfen.

# Beim  Zweit-Account (niedrigeres Rathaus-Level) passiert das gleiche, nur eben nur mit Dragons und dem King +
# Rage Spells

# --------------------------------------------- ENG --------------------------------------------- #
# All attacks are coded here. Very annoying manual work, 4 different sides of the base to make the bot
# to make it less conspicuous to Supercell.

# Simply put: It is dragged into the corresponding corner/side of the base, then along this side the
# War Machine, the King, the Queen, the E-Dragons, then the Warden, the Loons and the Rage Spells.
# The Warden ability is then ignited and two more Rage Spells are placed further down the center of the base + a Zap
# in the middle of the base.

# With the second account (lower Town Hall level), the same thing happens, but only with Dragons and the King +
# Rage Spells


# --------------------------------------------- CODE --------------------------------------------- #
# ACCOUNT: "1" (E-Drags)

def e_drags_top_right():
    time.sleep(1)
    pyautogui.moveTo(1400, 400)
    time.sleep(1)
    pyautogui.dragTo(900, 900, random.uniform(0.7, 2.1), button="left")
    time.sleep(1)

    # WAR MACHINE
    pyautogui.click(600, 1000)
    pyautogui.click(1250 + random.randint(3, 7), 400 + random.randint(3, 7))
    time.sleep(random.uniform(0.5, 0.8))
    time.sleep(random.uniform(0.7, 1.3))

    # KING
    pyautogui.click(737, 1000)
    pyautogui.click(950 + random.randint(3, 7), 160 + random.randint(3, 7))
    time.sleep(random.uniform(0.7, 1.3))
    # QUEEN
    pyautogui.click(830, 1000)
    pyautogui.click(1570 + random.randint(3, 7), 600 + random.randint(3, 7))
    time.sleep(random.uniform(0.7, 1.3))

    # E DRAGS
    pyautogui.click(470 + random.randint(3, 7), 970 + random.randint(3, 7))
    time.sleep(random.uniform(0.2, 0.4))
    pyautogui.click(779 + random.randint(3, 7), 120 + random.randint(3, 7))
    time.sleep(random.uniform(0.2, 0.4))
    pyautogui.click(877 + random.randint(3, 7), 198 + random.randint(3, 7))
    time.sleep(random.uniform(0.2, 0.4))
    pyautogui.click(987 + random.randint(3, 7), 270 + random.randint(3, 7))
    time.sleep(random.uniform(0.2, 0.4))
    pyautogui.click(1083 + random.randint(3, 7), 338 + random.randint(3, 7))
    time.sleep(random.uniform(0.2, 0.4))
    pyautogui.click(1181 + random.randint(3, 7), 418 + random.randint(3, 7))
    time.sleep(random.uniform(0.2, 0.4))
    pyautogui.click(1287 + random.randint(3, 7), 488 + random.randint(3, 7))
    time.sleep(random.uniform(0.2, 0.4))
    pyautogui.click(1379 + random.randint(3, 7), 562 + random.randint(3, 7))
    time.sleep(random.uniform(0.2, 0.4))
    pyautogui.click(1483 + random.randint(3, 7), 642 + random.randint(3, 7))
    time.sleep(random.uniform(0.2, 0.4))
    pyautogui.click(1567 + random.randint(3, 7), 706 + random.randint(3, 7))
    time.sleep(random.uniform(0.5, 0.8))
    time.sleep(random.uniform(0.7, 1.3))

    # WARDEN
    pyautogui.click(970, 1000)
    pyautogui.click(1120 + random.randint(3, 7), 380 + random.randint(3, 7))
    time.sleep(random.uniform(0.5, 0.8))

    # LOONS
    pyautogui.click(340, 970)
    pyautogui.click(1028 + random.randint(3, 7), 294 + random.randint(3, 7))
    pyautogui.click(1274 + random.randint(3, 7), 476 + random.randint(3, 7))
    time.sleep(random.uniform(0.5, 0.8))
    time.sleep(random.uniform(1, 2))

    # RAGE 1
    pyautogui.click(1210, 1000)
    pyautogui.click(820 + random.randint(20, 40), 398 + random.randint(20, 40))
    time.sleep(random.uniform(0.5, 0.8))
    pyautogui.click(1008 + random.randint(20, 40), 558 + random.randint(3, 40))
    time.sleep(random.uniform(0.5, 0.8))
    pyautogui.click(1232 + random.randint(20, 40), 762 + random.randint(20, 40))
    time.sleep(random.uniform(2, 4))

    # WARDEN ABILITY
    pyautogui.click(970, 1000)
    time.sleep(random.uniform(4, 6))

    # RAGE 2
    pyautogui.click(1210, 1000)
    pyautogui.click(748 + random.randint(20, 40), 590 + random.randint(20, 40))
    time.sleep(random.uniform(0.5, 0.8))
    pyautogui.click(964 + random.randint(20, 40), 758 + random.randint(20, 40))

    # ZAP
    pyautogui.click(1100, 1000)
    pyautogui.click(700 + random.randint(20, 50), 700 + random.randint(20, 50))
    time.sleep(random.randint(35, 45))


def e_drags_top_left():
    time.sleep(1)
    pyautogui.moveTo(650, 170)
    time.sleep(1)
    pyautogui.dragTo(1000, 450, random.uniform(0.7, 2.1), button="left")
    time.sleep(1)

    # WAR MACHINE
    pyautogui.click(600, 1000)
    pyautogui.click(685 + random.randint(3, 7), 340 + random.randint(3, 7))
    time.sleep(random.uniform(0.5, 0.8))
    time.sleep(random.uniform(0.7, 1.3))

    # KING
    pyautogui.click(737, 1000)
    pyautogui.click(399 + random.randint(3, 7), 532 + random.randint(3, 7))
    time.sleep(random.uniform(0.7, 1.3))
    # QUEEN
    pyautogui.click(830, 1000)
    pyautogui.click(937 + random.randint(3, 7), 158 + random.randint(3, 7))
    time.sleep(random.uniform(0.7, 1.3))

    pyautogui.click(470 + random.randint(3, 7), 970 + random.randint(3, 7))
    time.sleep(random.uniform(0.2, 0.4))
    pyautogui.click(250 + random.randint(3, 7), 640 + random.randint(3, 7))
    time.sleep(random.uniform(0.2, 0.4))
    pyautogui.click(375 + random.randint(3, 7), 550 + random.randint(3, 7))
    time.sleep(random.uniform(0.2, 0.4))
    pyautogui.click(450 + random.randint(3, 7), 520 + random.randint(3, 7))
    time.sleep(random.uniform(0.2, 0.4))
    pyautogui.click(540 + random.randint(3, 7), 450 + random.randint(3, 7))
    time.sleep(random.uniform(0.2, 0.4))
    pyautogui.click(625 + random.randint(3, 7), 370 + random.randint(3, 7))
    time.sleep(random.uniform(0.2, 0.4))
    pyautogui.click(730 + random.randint(3, 7), 310 + random.randint(3, 7))
    time.sleep(random.uniform(0.2, 0.4))
    pyautogui.click(840 + random.randint(3, 7), 230 + random.randint(3, 7))
    time.sleep(random.uniform(0.2, 0.4))
    pyautogui.click(930 + random.randint(3, 7), 165 + random.randint(3, 7))
    time.sleep(random.uniform(0.2, 0.4))
    pyautogui.click(985 + random.randint(3, 7), 105 + random.randint(3, 7))
    time.sleep(random.uniform(0.5, 0.8))
    time.sleep(random.uniform(0.7, 1.3))

    # WARDEN
    pyautogui.click(970, 1000)
    pyautogui.click(700 + random.randint(3, 7), 325 + random.randint(3, 7))
    time.sleep(random.uniform(0.5, 0.8))

    # LOONS
    pyautogui.click(340, 970)
    pyautogui.click(770 + random.randint(3, 7), 270 + random.randint(3, 7))
    pyautogui.click(587 + random.randint(3, 7), 408 + random.randint(3, 7))
    time.sleep(random.uniform(0.5, 0.8))
    time.sleep(random.uniform(1, 2))

    # RAGE 1
    pyautogui.click(1210, 1000)
    pyautogui.click(557 + random.randint(20, 40), 622 + random.randint(20, 40))
    time.sleep(random.uniform(0.5, 0.8))
    pyautogui.click(917 + random.randint(20, 40), 490 + random.randint(3, 40))
    time.sleep(random.uniform(0.5, 0.8))
    pyautogui.click(1057 + random.randint(20, 40), 310 + random.randint(20, 40))
    time.sleep(random.uniform(2, 4))

    # WARDEN ABILITY
    pyautogui.click(970, 1000)
    time.sleep(random.uniform(2, 4))

    # RAGE 2
    pyautogui.click(1210, 1000)
    pyautogui.click(1101 + random.randint(20, 40), 432 + random.randint(20, 40))
    time.sleep(random.uniform(0.5, 0.8))
    pyautogui.click(867 + random.randint(20, 40), 596 + random.randint(20, 40))
    time.sleep(random.uniform(1, 3))

    # ZAP
    pyautogui.click(1100, 1000)
    pyautogui.click(893 + random.randint(20, 50), 524 + random.randint(20, 50))
    time.sleep(random.randint(35, 45))


def e_drags_bottom_left():
    time.sleep(1)
    pyautogui.moveTo(460, 790)
    time.sleep(1)
    pyautogui.dragTo(1200, 500, random.uniform(0.7, 2.1), button="left")
    time.sleep(1)

    # WAR MACHINE
    pyautogui.click(600, 1000)
    pyautogui.click(655 + random.randint(3, 7), 636 + random.randint(3, 7))
    time.sleep(random.uniform(0.5, 0.8))
    time.sleep(random.uniform(0.7, 1.3))

    # KING
    pyautogui.click(737, 1000)
    pyautogui.click(430 + random.randint(3, 7), 285 + random.randint(3, 7))
    time.sleep(random.uniform(0.7, 1.3))
    # QUEEN
    pyautogui.click(830, 1000)
    pyautogui.click(1117 + random.randint(3, 7), 776 + random.randint(3, 7))
    time.sleep(random.uniform(0.7, 1.3))

    pyautogui.click(470 + random.randint(3, 7), 970 + random.randint(3, 7))
    time.sleep(random.uniform(0.2, 0.4))
    pyautogui.click(330 + random.randint(3, 7), 290 + random.randint(3, 7))
    time.sleep(random.uniform(0.2, 0.4))
    pyautogui.click(380 + random.randint(3, 7), 335 + random.randint(3, 7))
    time.sleep(random.uniform(0.2, 0.4))
    pyautogui.click(455 + random.randint(3, 7), 400 + random.randint(3, 7))
    time.sleep(random.uniform(0.2, 0.4))
    pyautogui.click(505 + random.randint(3, 7), 445 + random.randint(3, 7))
    time.sleep(random.uniform(0.2, 0.4))
    pyautogui.click(600 + random.randint(3, 7), 490 + random.randint(3, 7))
    time.sleep(random.uniform(0.2, 0.4))
    pyautogui.click(690 + random.randint(3, 7), 575 + random.randint(3, 7))
    time.sleep(random.uniform(0.2, 0.4))
    pyautogui.click(780 + random.randint(3, 7), 630 + random.randint(3, 7))
    time.sleep(random.uniform(0.2, 0.4))
    pyautogui.click(870 + random.randint(3, 7), 705 + random.randint(3, 7))
    time.sleep(random.uniform(0.2, 0.4))
    pyautogui.click(950 + random.randint(3, 7), 750 + random.randint(3, 7))
    time.sleep(random.uniform(0.5, 0.8))
    time.sleep(random.uniform(0.7, 1.3))

    # WARDEN
    pyautogui.click(970, 1000)
    pyautogui.click(771 + random.randint(3, 7), 530 + random.randint(3, 7))
    time.sleep(random.uniform(0.5, 0.8))

    # LOONS
    pyautogui.click(340, 970)
    pyautogui.click(635 + random.randint(3, 7), 422 + random.randint(3, 7))
    pyautogui.click(879 + random.randint(3, 7), 606 + random.randint(3, 7))
    time.sleep(random.uniform(0.5, 0.8))
    time.sleep(random.uniform(1, 2))

    # RAGE 1
    pyautogui.click(1210, 1000)
    pyautogui.click(679 + random.randint(20, 40), 224 + random.randint(20, 40))
    time.sleep(random.uniform(0.5, 0.8))
    pyautogui.click(913 + random.randint(20, 40), 364 + random.randint(3, 40))
    time.sleep(random.uniform(0.5, 0.8))
    pyautogui.click(1125 + random.randint(20, 40), 580 + random.randint(20, 40))
    time.sleep(random.uniform(2, 4))

    # WARDEN ABILITY
    pyautogui.click(970, 1000)
    time.sleep(random.uniform(2, 4))

    # RAGE 2
    pyautogui.click(1210, 1000)
    pyautogui.click(1185 + random.randint(20, 40), 392 + random.randint(20, 40))
    time.sleep(random.uniform(0.5, 0.8))
    pyautogui.click(901 + random.randint(20, 40), 216 + random.randint(20, 40))
    time.sleep(random.uniform(1, 3))

    # ZAP
    pyautogui.click(1100, 1000)
    pyautogui.click(861 + random.randint(20, 50), 422 + random.randint(20, 50))
    time.sleep(random.randint(35, 45))


def e_drags_bottom_right():
    time.sleep(1)
    pyautogui.moveTo(1292, 740)
    time.sleep(1)
    pyautogui.dragTo(1000, 450, random.uniform(0.7, 2.1), button="left")
    time.sleep(1)

    # WAR MACHINE
    pyautogui.click(600, 1000)
    pyautogui.click(1355 + random.randint(3, 7), 526 + random.randint(3, 7))
    time.sleep(random.uniform(0.5, 0.8))
    time.sleep(random.uniform(0.7, 1.3))

    # KING
    pyautogui.click(737, 1000)
    pyautogui.click(1091 + random.randint(3, 7), 748 + random.randint(3, 7))
    time.sleep(random.uniform(0.7, 1.3))

    # QUEEN
    pyautogui.click(830, 1000)
    pyautogui.click(1509 + random.randint(3, 7), 418 + random.randint(3, 7))
    time.sleep(random.uniform(0.7, 1.3))

    pyautogui.click(470 + random.randint(3, 7), 970 + random.randint(3, 7))
    time.sleep(random.uniform(0.2, 0.4))
    pyautogui.click(1634 + random.randint(3, 7), 308 + random.randint(3, 7))
    time.sleep(random.uniform(0.2, 0.4))
    pyautogui.click(1552 + random.randint(3, 7), 380 + random.randint(3, 7))
    time.sleep(random.uniform(0.2, 0.4))
    pyautogui.click(1474 + random.randint(3, 7), 436 + random.randint(3, 7))
    time.sleep(random.uniform(0.2, 0.4))
    pyautogui.click(1396 + random.randint(3, 7), 486 + random.randint(3, 7))
    time.sleep(random.uniform(0.2, 0.4))
    pyautogui.click(1336 + random.randint(3, 7), 556 + random.randint(3, 7))
    time.sleep(random.uniform(0.2, 0.4))
    pyautogui.click(1230 + random.randint(3, 7), 626 + random.randint(3, 7))
    time.sleep(random.uniform(0.2, 0.4))
    pyautogui.click(1166 + random.randint(3, 7), 672 + random.randint(3, 7))
    time.sleep(random.uniform(0.2, 0.4))
    pyautogui.click(1066 + random.randint(3, 7), 758 + random.randint(3, 7))
    time.sleep(random.uniform(0.2, 0.4))
    pyautogui.click(948 + random.randint(3, 7), 810 + random.randint(3, 7))
    time.sleep(random.uniform(0.5, 0.8))
    time.sleep(random.uniform(0.7, 1.3))

    # WARDEN
    pyautogui.click(970, 1000)
    pyautogui.click(1315 + random.randint(3, 7), 560 + random.randint(3, 7))
    time.sleep(random.uniform(0.5, 0.8))

    # LOONS
    pyautogui.click(340, 970)
    pyautogui.click(1221 + random.randint(3, 7), 638 + random.randint(3, 7))
    pyautogui.click(1423 + random.randint(3, 7), 470 + random.randint(3, 7))
    time.sleep(random.uniform(0.5, 0.8))
    time.sleep(random.uniform(1, 2))

    # RAGE 1
    pyautogui.click(1210, 1000)
    pyautogui.click(1359 + random.randint(20, 40), 310 + random.randint(20, 40))
    time.sleep(random.uniform(0.5, 0.8))
    pyautogui.click(1135 + random.randint(20, 40), 450 + random.randint(3, 40))
    time.sleep(random.uniform(0.5, 0.8))
    pyautogui.click(943 + random.randint(20, 40), 576 + random.randint(20, 40))
    time.sleep(random.uniform(2, 4))

    # WARDEN ABILITY
    pyautogui.click(970, 1000)
    time.sleep(random.uniform(2, 4))

    # RAGE 2
    pyautogui.click(1210, 1000)
    pyautogui.click(1241 + random.randint(20, 40), 214 + random.randint(20, 40))
    time.sleep(random.uniform(0.5, 0.8))
    pyautogui.click(909 + random.randint(20, 40), 416 + random.randint(20, 40))
    time.sleep(random.uniform(1, 3))

    # ZAP
    pyautogui.click(1100, 1000)
    pyautogui.click(1029 + random.randint(20, 50), 386 + random.randint(20, 50))
    time.sleep(random.randint(35, 45))


# ACCOUNT: "2" (Normal Dragons)

def dragons_top_right():
    time.sleep(1)
    pyautogui.moveTo(1400, 400)
    time.sleep(1)
    pyautogui.dragTo(900, 900, random.uniform(0.7, 2.1), button="left")
    time.sleep(1)

    # DRAGONS
    pyautogui.click(354, 1004)
    time.sleep(0.5)
    pyautogui.click(779 + random.randint(3, 7), 120 + random.randint(3, 7))
    pyautogui.click(877 + random.randint(3, 7), 198 + random.randint(3, 7))
    pyautogui.click(939 + random.randint(3, 7), 179 + random.randint(3, 7))
    pyautogui.click(987 + random.randint(3, 7), 270 + random.randint(3, 7))
    pyautogui.click(1083 + random.randint(3, 7), 338 + random.randint(3, 7))
    pyautogui.click(1181 + random.randint(3, 7), 418 + random.randint(3, 7))
    pyautogui.click(1287 + random.randint(3, 7), 488 + random.randint(3, 7))
    pyautogui.click(1379 + random.randint(3, 7), 562 + random.randint(3, 7))
    pyautogui.click(1483 + random.randint(3, 7), 642 + random.randint(3, 7))
    pyautogui.click(1567 + random.randint(3, 7), 706 + random.randint(3, 7))
    time.sleep(random.randint(1, 3))

    # KING
    pyautogui.click(463, 987)
    pyautogui.click(1181 + random.randint(3, 7), 418 + random.randint(3, 7))
    time.sleep(random.randint(6, 9))

    # RAGE
    pyautogui.click(615, 991)
    pyautogui.click(886 + random.randint(20, 40), 408 + random.randint(20, 40))
    time.sleep(random.uniform(0.5, 0.8))
    pyautogui.click(1008 + random.randint(20, 40), 514 + random.randint(3, 40))
    time.sleep(random.uniform(0.5, 0.8))
    pyautogui.click(1204 + random.randint(20, 40), 632 + random.randint(20, 40))
    time.sleep(random.uniform(2, 4))

    # KING ABILITY
    pyautogui.click(463, 987)

    time.sleep(random.randint(45, 55))


def dragons_top_left():
    time.sleep(1)
    pyautogui.moveTo(650, 170)
    time.sleep(1)
    pyautogui.dragTo(1000, 450, random.uniform(0.7, 2.1), button="left")
    time.sleep(1)

    # DRAGONS
    pyautogui.click(354, 1004)
    time.sleep(0.5)
    pyautogui.click(250 + random.randint(3, 7), 640 + random.randint(3, 7))
    pyautogui.click(375 + random.randint(3, 7), 550 + random.randint(3, 7))
    pyautogui.click(450 + random.randint(3, 7), 520 + random.randint(3, 7))
    pyautogui.click(540 + random.randint(3, 7), 450 + random.randint(3, 7))
    pyautogui.click(567 + random.randint(3, 7), 489 + random.randint(3, 7))
    pyautogui.click(625 + random.randint(3, 7), 370 + random.randint(3, 7))
    pyautogui.click(730 + random.randint(3, 7), 310 + random.randint(3, 7))
    pyautogui.click(840 + random.randint(3, 7), 230 + random.randint(3, 7))
    pyautogui.click(930 + random.randint(3, 7), 165 + random.randint(3, 7))
    pyautogui.click(985 + random.randint(3, 7), 105 + random.randint(3, 7))
    time.sleep(random.randint(1, 3))

    # KING
    pyautogui.click(463, 987)
    pyautogui.click(625 + random.randint(3, 7), 370 + random.randint(3, 7))
    time.sleep(random.randint(6, 9))

    # RAGE
    pyautogui.click(615, 991)
    pyautogui.click(746 + random.randint(20, 40), 684 + random.randint(20, 40))
    time.sleep(random.uniform(0.5, 0.8))
    pyautogui.click(916 + random.randint(20, 40), 558 + random.randint(3, 40))
    time.sleep(random.uniform(0.5, 0.8))
    pyautogui.click(1066 + random.randint(20, 40), 442 + random.randint(20, 40))
    time.sleep(random.uniform(2, 4))

    # KING ABILITY
    pyautogui.click(463, 987)

    time.sleep(random.randint(45, 55))


def dragons_bottom_left():
    time.sleep(1)
    pyautogui.moveTo(460, 790)
    time.sleep(1)
    pyautogui.dragTo(1200, 500, random.uniform(0.7, 2.1), button="left")
    time.sleep(1)

    # DRAGONS
    pyautogui.click(354, 1004)
    time.sleep(0.5)
    pyautogui.click(330 + random.randint(3, 7), 290 + random.randint(3, 7))
    pyautogui.click(380 + random.randint(3, 7), 335 + random.randint(3, 7))
    pyautogui.click(455 + random.randint(3, 7), 400 + random.randint(3, 7))
    pyautogui.click(505 + random.randint(3, 7), 445 + random.randint(3, 7))
    pyautogui.click(600 + random.randint(3, 7), 490 + random.randint(3, 7))
    pyautogui.click(690 + random.randint(3, 7), 575 + random.randint(3, 7))
    pyautogui.click(737 + random.randint(3, 7), 678 + random.randint(3, 7))
    pyautogui.click(780 + random.randint(3, 7), 630 + random.randint(3, 7))
    pyautogui.click(870 + random.randint(3, 7), 705 + random.randint(3, 7))
    pyautogui.click(950 + random.randint(3, 7), 750 + random.randint(3, 7))
    time.sleep(random.randint(1, 3))

    # KING
    pyautogui.click(463, 987)
    pyautogui.click(600 + random.randint(3, 7), 490 + random.randint(3, 7))
    time.sleep(random.randint(6, 9))

    # RAGE
    pyautogui.click(615, 991)
    pyautogui.click(732 + random.randint(20, 40), 248 + random.randint(20, 40))
    time.sleep(random.uniform(0.5, 0.8))
    pyautogui.click(916 + random.randint(20, 40), 348 + random.randint(3, 40))
    time.sleep(random.uniform(0.5, 0.8))
    pyautogui.click(1032 + random.randint(20, 40), 464 + random.randint(20, 40))
    time.sleep(random.uniform(2, 4))

    # KING ABILITY
    pyautogui.click(463, 987)

    time.sleep(random.randint(45, 55))


def dragons_bottom_right():
    time.sleep(1)
    pyautogui.moveTo(1292, 740)
    time.sleep(1)
    pyautogui.dragTo(1000, 450, random.uniform(0.7, 2.1), button="left")
    time.sleep(1)

    # DRAGONS
    pyautogui.click(354, 1004)
    time.sleep(0.5)
    pyautogui.click(1634 + random.randint(3, 7), 308 + random.randint(3, 7))
    pyautogui.click(1552 + random.randint(3, 7), 380 + random.randint(3, 7))
    pyautogui.click(1474 + random.randint(3, 7), 436 + random.randint(3, 7))
    pyautogui.click(1396 + random.randint(3, 7), 486 + random.randint(3, 7))
    pyautogui.click(1336 + random.randint(3, 7), 556 + random.randint(3, 7))
    pyautogui.click(1261 + random.randint(3, 7), 620 + random.randint(3, 7))
    pyautogui.click(1230 + random.randint(3, 7), 626 + random.randint(3, 7))
    pyautogui.click(1166 + random.randint(3, 7), 672 + random.randint(3, 7))
    pyautogui.click(1066 + random.randint(3, 7), 758 + random.randint(3, 7))
    pyautogui.click(948 + random.randint(3, 7), 810 + random.randint(3, 7))
    time.sleep(random.randint(1, 3))
    
    # KING
    pyautogui.click(463, 987)
    pyautogui.click(1336 + random.randint(3, 7), 556 + random.randint(3, 7))
    time.sleep(random.randint(6, 9))
    
    # RAGE
    pyautogui.click(615, 991)
    pyautogui.click(1236 + random.randint(20, 40), 238 + random.randint(20, 40))
    time.sleep(random.uniform(0.5, 0.8))
    pyautogui.click(1066 + random.randint(20, 40), 350 + random.randint(3, 40))
    time.sleep(random.uniform(0.5, 0.8))
    pyautogui.click(844 + random.randint(20, 40), 524 + random.randint(20, 40))
    time.sleep(random.uniform(2, 4))
    
    # KING ABILITY
    pyautogui.click(463, 987)

    time.sleep(random.randint(45, 55))
