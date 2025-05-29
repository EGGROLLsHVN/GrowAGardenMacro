import pyautogui # Keep these in
import ctypes
import threading
import time
import keyboard
import pytz # For timezone handling
import autoit, pydirectinput   # Direct input automations
import cv2
import numpy as np
from datetime import datetime, timedelta
from mss import mss

ctypes.windll.shcore.SetProcessDpiAwareness(2)
delay = .3

class Macro():
    def __init__(self, seedData, runCount):
       
        self.seedData = seedData  # Store the seeds dictionary
        self.runCount = runCount
        self.is_running = False
        self.thread = None
        self.est = pytz.timezone("US/Eastern")
        self.checkStopThread = None

        self.eventDetector = {
            "Bloodmoon": False,
            "Twilight": False
        }

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.thread = threading.Thread(target=self.mainLoop, daemon=True)
            self.checkStopThread = threading.Thread(target=self.checkStop, daemon=True)
            self.checkStopThread.start()
            autoit.win_activate("Roblox")
            autoit.win_activate("Roblox")
            self.thread.start()

    def checkStop(self):
        while self.is_running:
            if keyboard.is_pressed("ctrl+2"):
                print("Ctrl+2 Pressed")
                self.stop()
                break
            time.sleep(.001)  # Check every second

    def stop(self):
        if self.thread and self.thread.is_alive():
            self.is_running = False
            self.thread.join(timeout=.5)
            
    # Split time.sleep into smaller intervals so is_running can be checked more often
    def safeSleep(self, delay):
        for _ in range(int(delay * 10)):
            if not self.is_running:
                return
            time.sleep(0.1)    
    
    # Handles controling loop: starting, number of iterations, controlling the time
    def mainLoop(self):
        autoit.win_activate("Roblox")
        while self.is_running:
            self.runMacroCycle()
            self.waitUntilNextInterval()
            time.sleep(0.5)
            if not self.is_running:
                break

    # needs to repeat number of runCount times each time it finishes it alt tabes once
        # Could use alt + shift + tab to reverse through tabs in order which could work
    def runMacroCycle(self):
        for run in range(self.runCount):
            if not self.is_running:
                break

            print(f"Starting run {run + 1}/{self.runCount}")
            print(f"{self.runCount}")
            self.executeMacro()

            if run < (self.runCount - 1):
                 self.switchTabs()
            else:
                return
            
        if self.runCount > 1:
            self.switchTabs()

    # Run macros according to each seed setting
    def executeMacro(self):
        if not self.is_running:
            return
        
        autoit.send("\\")
        autoit.send("{RIGHT}")
        self.safeSleep(delay)
        autoit.send("{RIGHT}")
        self.safeSleep(delay)
        autoit.send("{RIGHT}")
        self.safeSleep(delay)
        autoit.send("{RIGHT}")
        self.safeSleep(delay)
        autoit.send("{ENTER}")
        self.safeSleep(delay)
        autoit.send("\\")
        self.safeSleep(0.5)
        pydirectinput.keyDown("i")
        self.safeSleep(2)
        pydirectinput.keyUp("i")
        self.safeSleep(0.3)
        pydirectinput.keyDown("o")
        self.safeSleep(0.15)
        pydirectinput.keyUp("o")
        self.safeSleep(1)

        if self.seedData.get("SeedShop") > 0 and self.is_running:
            self.regSeedMacro()
            self.exitShopGui()
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.safeSleep(delay)
            autoit.send("{RIGHT}")
            self.safeSleep(delay)
            autoit.send("{RIGHT}")
            self.safeSleep(delay)
            autoit.send("{RIGHT}")
            self.safeSleep(delay)
            autoit.send("{ENTER}")
            self.safeSleep(delay)
            autoit.send("\\")
            self.safeSleep(1)

        if self.seedData.get("EggShop") > 0 and self.is_running:
            self.eggShopMacro()
            # autoit.send("\\")
            # autoit.send("{RIGHT}")
            # self.safeSleep(delay)
            # autoit.send("{RIGHT}")
            # self.safeSleep(delay)
            # autoit.send("{RIGHT}")
            # self.safeSleep(delay)
            # autoit.send("{RIGHT}")
            # self.safeSleep(delay)
            # autoit.send("{ENTER}")
            # self.safeSleep(delay)
            # autoit.send("\\")
            self.safeSleep(1) 

        if self.seedData.get("GearShop") > 0 and self.is_running:
            self.gearShopMacro()
            self.exitShopGui()
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.safeSleep(delay)
            autoit.send("{RIGHT}")
            self.safeSleep(delay)
            autoit.send("{RIGHT}")
            self.safeSleep(delay)
            autoit.send("{RIGHT}")
            self.safeSleep(delay)
            autoit.send("{ENTER}")
            self.safeSleep(delay)
            autoit.send("\\")
            self.safeSleep(1)

        self.eventShopCheck()
        self.eventShopActivate()

    def eventShopActivate(self):
        if self.eventDetector["Bloodmoon"] is True:
            if self.seedData.get("BloodMoonShop") > 0 and self.is_running:
                self.bloodMoonShop()
                self.exitShopGui()

        if self.eventDetector["Twilight"] is True:
            if self.seedData.get("TwilightShop") > 0 and self.is_running:
                self.twilightShop()
                self.exitShopGui()

    def eventShopCheck(self):
        print("Checking for event shops")
        bloodmoonPath = r"images\bloodmoon.png"
        bloodmoonMatches = self.locateImage(bloodmoonPath, confidence=0.9)

        twilightPath = r"images\twilight.png"
        twilightMatches = self.locateImage(twilightPath, confidence=0.9)

        if len(twilightMatches) > 0:
            self.eventDetector["Twilight"] = True
            # print("Setting T as True")
        else:
            self.eventDetector["Twilight"] = False
            # print("Setting T as False")

        if len(bloodmoonMatches) > 0:
            self.eventDetector["Bloodmoon"] = True
            # print("Setting B as True")
        else:
            self.eventDetector["Bloodmoon"] = False
            # print("Setting B as False")

    def regSeedMacro(self): 
        if not self.is_running:
            return
        print("Calling: Regular Seed Shop")
        # Clicks seed shop
        autoit.send("\\")
        autoit.send("{RIGHT}")
        self.safeSleep(delay)
        autoit.send("{DOWN}")
        self.safeSleep(delay)
        autoit.send("{ENTER}")
        self.safeSleep(delay)
        autoit.send("e")
        autoit.send("\\")
        self.safeSleep(3)

        if self.seedData.get("Carrot", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(2)
            self.shopBuy()

        if self.seedData.get("Strawberry", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(3)
            self.shopBuy()

        if self.seedData.get("Blueberry", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(4)
            self.shopBuy()

        if self.seedData.get("OrangeTulip", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(5)
            self.shopBuy()

        if self.seedData.get("TomatoSeed", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(6)
            self.shopBuy()

        if self.seedData.get("CornSeed", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(7)
            self.shopBuy()
        
        if self.seedData.get("DaffodilSeed", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(8)
            self.shopBuy()
            
        if self.seedData.get("WatermelonSeed", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(9)
            self.shopBuy()

        if self.seedData.get("PumpkinSeed", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(10)
            self.shopBuy()

        if self.seedData.get("AppleSeed", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(11)
            self.shopBuy()

        if self.seedData.get("BambooSeed", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(12)
            self.shopBuy()

        if self.seedData.get("CoconutSeed", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(13)
            self.shopBuy()
        
        if self.seedData.get("CactusSeed", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(14)
            self.shopBuy()
       
        if self.seedData.get("DragonFruitSeed", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(15)
            self.shopBuy()

        if self.seedData.get("MangoSeed", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(16)
            self.shopBuy()
 
        if self.seedData.get("GrapeSeed", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(17)
            self.shopBuy()

        if self.seedData.get("MushroomSeed", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(18)
            self.shopBuy()

        if self.seedData.get("PepperSeed", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(19)
            self.shopBuy()

        if self.seedData.get("CacaoSeed", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(20)
            self.shopBuy()
       
        if self.seedData.get("BeanstalkSeed", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(21)
            self.shopBuy()

    def eggShopMacro(self):
        if not self.is_running:
            return
        print("Calling: Egg Shop") 
        # Walk to egg shop
        autoit.send("\\")
        autoit.send("{RIGHT}")
        self.safeSleep(delay)
        autoit.send("{RIGHT}")
        self.safeSleep(delay)
        autoit.send("{RIGHT}")
        self.safeSleep(delay)
        autoit.send("{RIGHT}")
        self.safeSleep(delay)
        autoit.send("{RIGHT}")
        self.safeSleep(delay)
        autoit.send("{ENTER}")
        self.safeSleep(delay)
        autoit.send("\\")
        self.safeSleep(1)

        autoit.send("d")
        autoit.send("d")
        autoit.send("d")

        pydirectinput.keyDown("d")
        self.safeSleep(20)
        pydirectinput.keyUp("d")
        self.safeSleep(.4)

        # The p2w sign 
        pydirectinput.keyDown("w")
        self.safeSleep(1)
        pydirectinput.keyUp("w")
        self.safeSleep(.2)

        if not self.is_running: return
        autoit.send("e")
        self.safeSleep(1)

        if not self.is_running: return
        cancelBtnPath = r"images\cancelButton.png"
        matches = self.locateImage(cancelBtnPath)

        bestMatch = max(matches, key=lambda m: m["confidence"])

        # Click the center of the button for better accuracy
        x = bestMatch["x"] + bestMatch["width"] // 2
        y = bestMatch["y"] + bestMatch["height"] // 2

        autoit.mouse_click("left", x, y, 1)   
        self.safeSleep(.2)

        # Egg 1
        pydirectinput.keyDown("s")
        self.safeSleep(.1)
        pydirectinput.keyUp("s")
        self.safeSleep(.2)

        if not self.is_running: return
        autoit.send("e")
        self.safeSleep(.6)

        if not self.is_running: return # Buy
        autoit.send("\\")
        autoit.send("{RIGHT}")
        self.safeSleep(delay)
        autoit.send("{RIGHT}")
        self.safeSleep(delay)
        autoit.send("{RIGHT}")
        self.safeSleep(delay)
        autoit.send("{RIGHT}")
        self.safeSleep(delay)
        autoit.send("{DOWN}")
        self.safeSleep(delay)
        autoit.send("{ENTER}")
        self.safeSleep(delay)
        autoit.send("\\")
        self.safeSleep(.2)    

        # Egg 2
        pydirectinput.keyDown("s")
        self.safeSleep(.1)
        pydirectinput.keyUp("s")
        self.safeSleep(.2)

        if not self.is_running: return
        autoit.send("e")
        self.safeSleep(.6)
        
        if not self.is_running: return  # Buy
        autoit.send("\\")
        autoit.send("{RIGHT}")
        self.safeSleep(delay)
        autoit.send("{RIGHT}")
        self.safeSleep(delay)
        autoit.send("{RIGHT}")
        self.safeSleep(delay)
        autoit.send("{RIGHT}")
        self.safeSleep(delay)
        autoit.send("{DOWN}")
        self.safeSleep(delay)
        autoit.send("{ENTER}")
        self.safeSleep(delay)
        autoit.send("\\")
        self.safeSleep(.2) 

        # Egg 3
        pydirectinput.keyDown("s")
        self.safeSleep(.1)
        pydirectinput.keyUp("s")
        self.safeSleep(.2)

        if not self.is_running: return
        autoit.send("e")
        self.safeSleep(.6)
        
        if not self.is_running: return  # Buy
        autoit.send("\\")
        autoit.send("{RIGHT}")
        self.safeSleep(delay)
        autoit.send("{RIGHT}")
        self.safeSleep(delay)
        autoit.send("{RIGHT}")
        self.safeSleep(delay)
        autoit.send("{RIGHT}")
        self.safeSleep(delay)
        autoit.send("{DOWN}")
        self.safeSleep(delay)
        autoit.send("{ENTER}")
        self.safeSleep(delay)
        autoit.send("\\")
        self.safeSleep(.2)

    def gearShopMacro(self):
        if not self.is_running:
            return
        autoit.send("a")
        autoit.send("d")
        autoit.send("a")
        autoit.send("d")

        autoit.send("2") 
        # autoit.mouse_click("left", 940, 1480)
        self.safeSleep(2)
        autoit.mouse_click("left", 800, 700)
        self.safeSleep(1)
        autoit.send("e")
        self.safeSleep(1.5)

        autoit.send("\\")
        autoit.send("{RIGHT}")
        self.safeSleep(delay)
        autoit.send("{RIGHT}")
        self.safeSleep(delay)
        autoit.send("{RIGHT}")
        self.safeSleep(delay)
        autoit.send("{RIGHT}")
        self.safeSleep(delay)
        autoit.send("{DOWN}")
        self.safeSleep(delay)
        autoit.send("{ENTER}")
        self.safeSleep(delay)
        autoit.send("\\")   
        self.safeSleep(1.5)
    
        # To close the buy (1770, 400)
        if self.seedData.get("WateringCan", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(2)
            self.shopBuy()

        # Scrolls y + 90
        if self.seedData.get("Trowel", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(3)
            self.shopBuy()

        # Scrolls y + 90
        if self.seedData.get("RecallWrench", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(4)
            self.shopBuy()

        # Scrolls y + 90
        if self.seedData.get("BasicSprinkler", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(5)
            self.shopBuy()

        # Scrolls y + 10
        if self.seedData.get("AdvancedSprinkler", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(6)
            self.shopBuy()
        
        #
        if self.seedData.get("GodlySprinkler", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(7)
            self.shopBuy()

        # 
        if self.seedData.get("LightningRod", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(8)
            self.shopBuy()

        # 
        if self.seedData.get("MasterSprinkler", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(9)
            self.shopBuy()

        #
        if self.seedData.get("FavoriteTool", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(10)
            self.shopBuy()

        # 
        if self.seedData.get("HarvestTool", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(11)
            self.shopBuy()

    def bloodMoonShop(self):
        if not self.is_running:
            return
        
        autoit.send("\\")
        autoit.send("{RIGHT}")
        self.safeSleep(delay)
        autoit.send("{DOWN}")
        self.safeSleep(delay)
        autoit.send("{ENTER}")
        self.safeSleep(delay)
        autoit.send("\\")
        self.safeSleep(2)

        autoit.send("d")
        autoit.send("d")
        autoit.send("d")

        pydirectinput.keyDown("w")
        self.safeSleep(.7)
        pydirectinput.keyUp("w")
        self.safeSleep(.4)

        pydirectinput.keyDown("d")
        self.safeSleep(9)
        pydirectinput.keyUp("d")
        self.safeSleep(.2)

        autoit.send("e")
        self.safeSleep(3)

        if self.seedData.get("MysteriousCrate(Bm)", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(2)
            self.shopBuy()

        if self.seedData.get("NightEgg(Bm)", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(3)
            self.shopBuy()

        if self.seedData.get("NightSeedPack(Bm)", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(4)
            self.shopBuy()

        if self.seedData.get("BloodBananaSeed(Bm)", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(5)
            self.shopBuy()

        if self.seedData.get("MoonMelonSeed(Bm)", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(6)
            self.shopBuy()
        
        if self.seedData.get("StarCaller(Bm)", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(7)
            self.shopBuy()

        if self.seedData.get("BloodKiwi(Bm)", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(8)
            self.shopBuy()

        if self.seedData.get("BloodHedgehog(Bm)", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(9)
            self.shopBuy()

        if self.seedData.get("BloodOwl(Bm)", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(10)
            self.shopBuy()

    def twilightShop(self):
        if not self.is_running:
            return
        
        autoit.send("\\")
        autoit.send("{RIGHT}")
        self.safeSleep(delay)
        autoit.send("{DOWN}")
        self.safeSleep(delay)
        autoit.send("{ENTER}")
        self.safeSleep(delay)
        autoit.send("\\")
        self.safeSleep(2)

        autoit.send("d")
        autoit.send("d")
        autoit.send("d")

        pydirectinput.keyDown("w")
        self.safeSleep(.7)
        pydirectinput.keyUp("w")
        self.safeSleep(.4)

        pydirectinput.keyDown("d")
        self.safeSleep(9)
        pydirectinput.keyUp("d")
        self.safeSleep(.2)

        autoit.send("e")
        self.safeSleep(3)

        if self.seedData.get("NightEgg(Tl)", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(2)
            self.shopBuy()

        if self.seedData.get("NightSeedPack(Tl)", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(3)
            self.shopBuy()

        if self.seedData.get("TwilightCrate(Tl)", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(4)
            self.shopBuy()

        if self.seedData.get("StarCaller(Tl)", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(5)
            self.shopBuy()

        if self.seedData.get("MoonCat(Tl)", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(6)
            self.shopBuy()
        
        if self.seedData.get("Celestiberry(Tl)", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(7)
            self.shopBuy()

        if self.seedData.get("MoonMango(Tl)", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(8)
            self.shopBuy()
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(8)
            self.shopBuy()

    def shopBuy(self):
        if not self.is_running:
            return

        self.safeSleep(delay)
        autoit.send("{ENTER}")
        self.safeSleep(.75)
        autoit.send("{DOWN}")
        self.safeSleep(delay)
        for i in range(30):
            autoit.send("{ENTER}")
            self.safeSleep(.05)
        autoit.send("{UP}")
        self.safeSleep(delay)
        autoit.send("{ENTER}")
        self.safeSleep(.75)
        autoit.send("\\")
        autoit.send("\\")
        autoit.send("\\")
    
    def moveDown(self, number):
        for i in range(number):
            self.safeSleep(.05)
            autoit.send("{DOWN}")

    def exitShopGui(self): 
        self.safeSleep(delay)
        autoit.send("\\")
        autoit.send("{RIGHT}")
        self.safeSleep(delay)
        autoit.send("{RIGHT}")
        self.safeSleep(delay)
        autoit.send("{RIGHT}")
        self.safeSleep(delay)
        autoit.send("{RIGHT}")
        self.safeSleep(delay)
        autoit.send("{RIGHT}")
        self.safeSleep(delay)
        autoit.send("{DOWN}")
        self.safeSleep(delay)
        autoit.send("{ENTER}")
        self.safeSleep(delay)
        autoit.send("\\")
        self.safeSleep(delay)

    def locateImage(self, imagePath, confidence=0.5):
        template = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)
        # h, w = template.shape[:-1]
        h, w = template.shape

        with mss() as sct:
            monitor = sct.monitors[1]
            screenshot = np.array(sct.grab(monitor))
        #     screen = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR) 
            screenGray = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2GRAY)

        # result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        result = cv2.matchTemplate(screenGray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= confidence)

        matches = []

        for pt in zip(*loc[::-1]): # Switches x and y
            matches.append({"x": pt[0], "y": pt[1], "width": w, "height": h, "confidence": result[pt[1], pt[0]]})       

        return matches
        
    def switchTabs(self):
            keyboard.press_and_release("alt + shift + tab")
            self.safeSleep(0.5)
            print("Switched to next tab")

    # Calculates time based on local time, or time zone in intervals of 5
    def waitUntilNextInterval(self):
        if not self.is_running:
            return

        now = datetime.now(self.est) # now = datetime.now(self.est)

        minutesPast = now.minute % 5
        secondsPast = now.second + now.microsecond/1_000_000

        if minutesPast == 4 or (minutesPast == 0 and now.second < 60):
            return
        
        minutesToWait = (4 - minutesPast) % 5
        nextRun = now.replace(second=0, microsecond=0) + timedelta(minutes=minutesToWait)
        wait_seconds = (nextRun - now).total_seconds()

        print(f"Current ET: {now.strftime('%H:%M:%S')}")
        print(f"Next run at: {nextRun.strftime('%H:%M:%S')}")
        print(f"Waiting {wait_seconds:.1f} seconds")

        while wait_seconds > 0 and self.is_running:
            time.sleep(min(1, wait_seconds))
            wait_seconds -= 1




