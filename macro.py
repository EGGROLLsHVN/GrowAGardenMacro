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

ctypes.windll.user32.SetProcessDPIAware()
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
            if self.is_running:
                return
            
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
        time.sleep(.05)  # Check every second

    def stop(self):
        if self.thread and self.thread.is_alive():
            print("Macro Stopped")
            self.is_running = False
            keyboard.unhook_all()
            self.cleanup()
            self.thread.join(timeout=.5)
    
    def cleanup(self):
        releaseKeys = ['w', 'a', 's', 'd', 'i', 'o', 'e']  # Keys used in the macro
        for key in releaseKeys:
            try:
                pydirectinput.keyUp(key)
            except:
                pass
            
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
            self.cleanup()
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
        
        autoit.mouse_click("Left", 1000, 150) # Clicks garden button
        self.safeSleep(0.5)
        pydirectinput.keyDown("i")
        self.safeSleep(2)
        pydirectinput.keyUp("i")
        self.safeSleep(0.3)
        pydirectinput.keyDown("o")
        self.safeSleep(.5)
        pydirectinput.keyUp("o")
        self.safeSleep(1)

        if self.seedData.get("SeedShop") > 0 and self.is_running:
            self.regSeedMacro()
            self.exitShopGui()
            autoit.mouse_click("Left", 1000, 150) # Clicks garden button
            self.safeSleep(1)

        if self.seedData.get("EggShop") > 0 and self.is_running:
            self.eggShopMacro()
            self.safeSleep(1) 

        if self.seedData.get("GearShop") > 0 and self.is_running:
            self.gearShopMacro()
            self.exitShopGui()
            autoit.mouse_click("Left", 1000, 150) # Clicks garden button
            self.safeSleep(1)

        # self.eventShopCheck()
        self.eventShopActivate()

    def eventShopActivate(self):
        # if self.eventDetector["Bloodmoon"] is True:
        #     if self.seedData.get("BloodMoonShop") > 0 and self.is_running:
        #         self.bloodMoonShop()
        #         self.exitShopGui()

        # if self.eventDetector["Twilight"] is True:
        #     if self.seedData.get("TwilightShop") > 0 and self.is_running:
        #         self.twilightShop()
        #         self.exitShopGui()

        if self.seedData.get("BeeShop") > 0:
            self.beeShop()
            self.exitShopGui()

            if self.seedData.get("CompressHoney", False) and self.is_running:
                pydirectinput.keyDown("w")
                self.safeSleep(.75)
                pydirectinput.keyUp("w")
                self.safeSleep(.75)
                pydirectinput.keyDown("d")
                self.safeSleep(1)
                pydirectinput.keyUp("d")
                self.safeSleep(.75)
                pydirectinput.keyDown("s")
                self.safeSleep(.85)     # Pushdown time
                pydirectinput.keyUp("s")
                self.safeSleep(.75)
                pydirectinput.keyDown("a")
                self.safeSleep(.5)
                pydirectinput.keyUp("a")
                self.safeSleep(.75)


                autoit.send("~")
                self.safeSleep(delay=.5)
                autoit.mouse_click("Left", 1350, 560, 2) # Clicks inventory search and types in poll for pollinated
                self.safeSleep(delay=.5)
                autoit.send("p")
                self.safeSleep(delay=.1)
                autoit.send("o")
                self.safeSleep(delay=.1)
                autoit.send("l")
                self.safeSleep(delay=.1)
                autoit.send("l")
                self.safeSleep(delay=.1)
                autoit.send("i")
                self.safeSleep(delay=.1)
                autoit.send("n")
                self.safeSleep(delay=.1)
                autoit.send("a")
                self.safeSleep(delay=.1)
                autoit.send("t")
                self.safeSleep(delay=.1)
                autoit.send("e")
                self.safeSleep(delay=.1)
                autoit.send("d")
                self.safeSleep(delay=.1)
                autoit.send("{SPACE}")
                self.safeSleep(delay=.1)
                autoit.send("m")
                self.safeSleep(delay=.1)
                autoit.send("o")
                self.safeSleep(delay=.1)
                autoit.send("o")
                self.safeSleep(delay=.1)
                autoit.send("n")
                self.safeSleep(delay=.1)
                autoit.mouse_click("Left", 600, 615, 1) # Selects first plant slot in inventory 
                self.safeSleep(delay=.5)
                autoit.send("e")
                self.safeSleep(delay=.5)
                autoit.send("e")
                self.safeSleep(delay=.5)
                autoit.send("e")
                self.safeSleep(delay=.5)
                autoit.send("e")
                self.safeSleep(delay=.5)
                autoit.send("~")

    # TODO: Might need to update confidence levels create be event
    # def eventShopCheck(self):

    def beeShop(self): # 1200 , 520
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
        autoit.send("a")
        autoit.send("d")
        autoit.send("a")

        pydirectinput.keyDown("w")
        self.safeSleep(.6)
        pydirectinput.keyUp("w")
        self.safeSleep(.4)

        pydirectinput.keyDown("d")
        self.safeSleep(8.3)
        pydirectinput.keyUp("d")
        self.safeSleep(.2)

        pydirectinput.keyDown("s")
        self.safeSleep(.075)
        pydirectinput.keyUp("s")
        self.safeSleep(.2)

        autoit.send("e")
        self.safeSleep(3)
        autoit.mouse_click("Left", 1200, 520, 2)
        self.safeSleep(1.5)

        if self.seedData.get("FlowerSeedPack", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(2)

            self.safeSleep(delay) 
            autoit.send("{ENTER}")
            self.safeSleep(.1)
            autoit.send("{DOWN}")
            self.safeSleep(.1)
            autoit.send("{DOWN}")
            self.safeSleep(delay)

            for i in range(10):
                autoit.send("{ENTER}")

            autoit.send("{UP}")
            self.safeSleep(delay)
            autoit.send("{ENTER}")

            self.safeSleep(.75)
            autoit.send("\\")
            self.safeSleep(.1)
            autoit.send("\\")
            self.safeSleep(.1)
            autoit.send("\\")
            self.safeSleep(0.5)
                
        #
        if self.seedData.get("NectarineSeed", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(4)
            self.eggShopBuy()
            self.moveUp(1)
            autoit.send("{ENTER}")
            autoit.send("{ENTER}")
            self.safeSleep(.75)
            autoit.send("\\")
            self.safeSleep(.1)
            autoit.send("\\")
            self.safeSleep(.1)
            autoit.send("\\")
            self.safeSleep(0.5)

        #
        if self.seedData.get("HiveFruitSeed", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(5)
            self.eggShopBuy()
            self.moveUp(2)
            autoit.send("{ENTER}")
            autoit.send("{ENTER}")
            self.safeSleep(.75)
            autoit.send("\\")
            self.safeSleep(.1)
            autoit.send("\\")
            self.safeSleep(.1)
            autoit.send("\\")
            self.safeSleep(0.5)

        #
        if self.seedData.get("HoneySprinkler", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(6)
            self.eggShopBuy()
            self.moveUp(3)
            autoit.send("{ENTER}")
            autoit.send("{ENTER}")
            self.safeSleep(.75)
            autoit.send("\\")
            self.safeSleep(.1)
            autoit.send("\\")
            self.safeSleep(.1)
            autoit.send("\\")
            self.safeSleep(0.5)
        #
        if self.seedData.get("BeeEgg", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(7)

            self.safeSleep(delay) 
            autoit.send("{ENTER}")
            self.safeSleep(.1)
            autoit.send("{DOWN}")
            self.safeSleep(.1)
            autoit.send("{DOWN}")
            self.safeSleep(delay)

            for i in range(10):
                autoit.send("{ENTER}")

            autoit.send("{UP}")
            self.safeSleep(delay)
            autoit.send("{ENTER}")
            self.moveUp(5)
            autoit.send("{ENTER}")
            autoit.send("{ENTER}")

            self.safeSleep(.75)
            autoit.send("\\")
            self.safeSleep(.1)
            autoit.send("\\")
            self.safeSleep(.1)
            autoit.send("\\")
            self.safeSleep(0.5)
            
        #
        if self.seedData.get("BeeCrate", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(9)

            self.safeSleep(delay) 
            autoit.send("{ENTER}")
            self.safeSleep(.1)
            autoit.send("{DOWN}")
            self.safeSleep(.1)
            autoit.send("{DOWN}")
            self.safeSleep(delay)

            for i in range(10):
                autoit.send("{ENTER}")

            autoit.send("{UP}")
            self.safeSleep(delay)
            autoit.send("{ENTER}")
            self.moveUp(7)
            autoit.send("{ENTER}")
            autoit.send("{ENTER}")

            self.safeSleep(.75)
            autoit.send("\\")
            self.safeSleep(.1)
            autoit.send("\\")
            self.safeSleep(.1)
            autoit.send("\\")
            self.safeSleep(0.5)
        # 
        if self.seedData.get("HoneyComb", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(11)
            self.eggShopBuy()
            self.moveUp(8)
            autoit.send("{ENTER}")
            autoit.send("{ENTER}")
            self.safeSleep(.75)
            autoit.send("\\")
            self.safeSleep(.1)
            autoit.send("\\")
            self.safeSleep(.1)
            autoit.send("\\")
            self.safeSleep(0.5)

        # 
        if self.seedData.get("BeeChair", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(12)
            self.eggShopBuy()
            self.moveUp(9)
            autoit.send("{ENTER}")
            autoit.send("{ENTER}")
            self.safeSleep(.75)
            autoit.send("\\")
            self.safeSleep(.1)
            autoit.send("\\")
            self.safeSleep(.1)
            autoit.send("\\")
            self.safeSleep(0.5)

        #
        if self.seedData.get("HoneyTorch", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(13)
            self.eggShopBuy()
            self.moveUp(10)
            autoit.send("{ENTER}")
            autoit.send("{ENTER}")
            self.safeSleep(.75)
            autoit.send("\\")
            self.safeSleep(.1)
            autoit.send("\\")
            self.safeSleep(.1)
            autoit.send("\\")
            self.safeSleep(0.5)

        # 
        if self.seedData.get("HoneyWalkway", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(14)
            self.eggShopBuy()
            self.moveUp(11)
            autoit.send("{ENTER}")
            autoit.send("{ENTER}")
            self.safeSleep(.75)
            autoit.send("\\")
            self.safeSleep(.1)
            autoit.send("\\")
            self.safeSleep(.1)
            autoit.send("\\")
            self.safeSleep(0.5)
                
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

        # The p2w sign TODO: Edit it for 1920 x 1080 100% resolution
        pydirectinput.keyDown("w")
        self.safeSleep(1)
        pydirectinput.keyUp("w")
        self.safeSleep(.2)

        if not self.is_running: return
        autoit.send("e")
        self.safeSleep(1)
        autoit.mouse_click("Left", 850, 680)

        # if not self.is_running: return
        # cancelBtnPath1920x1080 = r"images\cancelButton1920x1080.png"
        # matches = self.locateImage(cancelBtnPath1920x1080)

        # if not self.is_running: return
        # # Click the center of the button for better accuracy
        # bestMatch = max(matches, key=lambda m: m["confidence"]) 

        # # Click the center of the button for better accuracy
        # x = bestMatch["x"] + bestMatch["width"] // 2
        # y = bestMatch["y"] + bestMatch["height"] // 2

        # autoit.mouse_click("left", x, y, 1)   
        # self.safeSleep(.2)

        # Egg 1
        pydirectinput.keyDown("s")
        self.safeSleep(.1)
        pydirectinput.keyUp("s")
        self.safeSleep(.2)

        if not self.is_running: return
        autoit.send("e")
        self.safeSleep(.6)

        if not self.is_running: return # Buy
        autoit.mouse_click("Left", 900, 670) 
        autoit.mouse_click("Left", 1300, 360) 
        self.safeSleep(.2)    

        # Egg 2
        pydirectinput.keyDown("s")
        self.safeSleep(.075)
        pydirectinput.keyUp("s")
        self.safeSleep(.2)

        if not self.is_running: return
        autoit.send("e")
        self.safeSleep(.6)
        
        if not self.is_running: return  # Buy
        autoit.mouse_click("Left", 900, 670) 
        autoit.mouse_click("Left", 1300, 360) 
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
        autoit.mouse_click("Left", 900, 670) 
        autoit.mouse_click("Left", 1300, 360) 
        self.safeSleep(.2)

    # TODO: Fix
    def gearShopMacro(self):
        if not self.is_running:
            return
        # autoit.send("a")
        # autoit.send("d")
        # autoit.send("a")
        # autoit.send("d")

        # autoit.send("2") 
        autoit.mouse_click("left", 675, 980)
        self.safeSleep(2)
        autoit.mouse_click("left", 800, 700)
        self.safeSleep(2)
        autoit.send("e")
        self.safeSleep(2)
        autoit.mouse_click("Left", 1150, 510)
        self.safeSleep(1.5)
    
        # To close the buy (1770, 400)
        if self.seedData.get("WateringCan", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(2)
            self.shopBuy()

        # 
        if self.seedData.get("Trowel", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(3)
            self.shopBuy()

        # TODO: Fix this doesnt work for some reason
        if self.seedData.get("RecallWrench", False) and self.is_running:
            autoit.send("\\")
            autoit.send("{RIGHT}")
            self.moveDown(4)
            self.shopBuy()

        #
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
            # self.safeSleep(.01)
        autoit.send("{UP}")
        self.safeSleep(delay)
        autoit.send("{ENTER}")
        self.safeSleep(.75)
        autoit.send("\\")
        self.safeSleep(.1)
        autoit.send("\\")
        self.safeSleep(.1)
        autoit.send("\\")
        self.safeSleep(0.5)

    def eggShopBuy(self):
        if not self.is_running:
            return

        self.safeSleep(delay) 
        autoit.send("{ENTER}")
        self.safeSleep(.75)
        autoit.send("{DOWN}")
        self.safeSleep(delay)
        for i in range(10):
            autoit.send("{ENTER}")
            # self.safeSleep(.01)
        autoit.send("{UP}")
        self.safeSleep(delay)
        autoit.send("{ENTER}")
        self.safeSleep(.75)

    def moveUp(self, number):
        if not self.is_running:
            return
        
        for i in range(number):
            self.safeSleep(.07)
            autoit.send("{UP}")
        
    def moveDown(self, number):
        if not self.is_running:
            return
        
        for i in range(number):
            self.safeSleep(.05)
            autoit.send("{DOWN}")

    def exitShopGui(self): 
        if not self.is_running:
            return
        
        self.safeSleep(delay)
        autoit.mouse_click("Left", 1280, 280) # 1300, 290, 1280, 275
        # autoit.send("\\")
        # autoit.send("{RIGHT}")
        # autoit.send("{RIGHT}")
        # self.safeSleep(delay)
        # autoit.send("{RIGHT}")
        # self.safeSleep(delay)
        # autoit.send("{RIGHT}")
        # self.safeSleep(delay)
        # autoit.send("{RIGHT}")
        # self.safeSleep(delay)
        # autoit.send("{RIGHT}")
        # self.safeSleep(delay)
        # autoit.send("{DOWN}")
        # self.safeSleep(delay)
        # autoit.send("{ENTER}")
        # self.safeSleep(delay)
        # autoit.send("\\")
        self.safeSleep(1)

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
        if not self.is_running:
            return
    
        keyboard.press_and_release("alt + shift + tab")
        self.safeSleep(0.5)
        print("Switched to next tab")

    # Calculates time based on local time, or time zone in intervals of 5
    def waitUntilNextInterval(self):
        if not self.is_running:
            return

        now = datetime.now(self.est) # now = datetime.now(self.est)
        minutesPast = now.minute % 5

        if minutesPast >= 4:
            minutesToWait = (5 - minutesPast) % 5 # Wait until next 5 minutes
            nextRun = now.replace(second=0, microsecond=0) + timedelta(minutes=minutesToWait)
            waitSeconds = max(0, (nextRun - now).total_seconds())

            print(f"Current ET: {now.strftime('%H:%M:%S')}")
            print(f"Next run at: {nextRun.strftime('%H:%M:%S')}")
            print(f"Waiting {waitSeconds:.1f} seconds")

            self.safeSleep(waitSeconds)

        else:
            return
