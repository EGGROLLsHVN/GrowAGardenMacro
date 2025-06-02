import tkinter as tk
import keyboard
import os, sys
import threading, subprocess
import json
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageDraw, ImageTk
from macro import Macro


class Newlv():
    def __init__(self, window, reruns):
        self.toplv = window
        self.reruns = reruns
        self.seed_vars = {}
        self.macro = None
        self.setup_global_hotkeys()
        # Max Columns
        self.seedMaxC = 2
        self.gearMaxC = 1
        self.eggMaxC=1
        self.bloodMC=1
        self.twilightMC=1
        self.beeShopMC=1

        # NOTE: Edit upon newer updates
        self.shopCategories = {
            # Seed Shop
            "Carrot": "SeedShop",
            "Strawberry": "SeedShop",
            "Blueberry": "SeedShop",
            "OrangeTulip": "SeedShop",
            "TomatoSeed": "SeedShop",
            "CornSeed": "SeedShop",
            "DaffodilSeed": "SeedShop",
            "WatermelonSeed": "SeedShop",
            "PumpkinSeed": "SeedShop",
            "AppleSeed": "SeedShop",
            "BambooSeed": "SeedShop",
            "CoconutSeed": "SeedShop",
            "CactusSeed": "SeedShop",
            "DragonFruitSeed": "SeedShop",
            "MangoSeed": "SeedShop",
            "GrapeSeed": "SeedShop",
            "MushroomSeed": "SeedShop",
            "PepperSeed": "SeedShop",
            "CacaoSeed": "SeedShop",
            "BeanstalkSeed": "SeedShop",

            # Gear Shop
            "WateringCan": "GearShop",
            "Trowel": "GearShop",
            "RecallWrench": "GearShop",
            "BasicSprinkler": "GearShop",
            "AdvancedSprinkler": "GearShop",
            "GodlySprinkler": "GearShop",
            "LightningRod": "GearShop",
            "MasterSprinkler": "GearShop",
            "FavoriteTool": "GearShop",
            "HarvestTool": "GearShop",

            # Bee Shop:
            "FlowerSeedPack": "BeeShop",
            "NectarineSeed": "BeeShop",
            "HiveFruitSeed": "BeeShop",
            "HoneySprinkler": "BeeShop",
            "BeeEgg": "BeeShop",
            "BeeCrate": "BeeShop",
            "HoneyComb":"BeeShop",
            "BeeChair": "BeeShop",
            "HoneyTorch": "BeeShop",
            "HoneyWalkway": "BeeShop",
            "CompressHoney": "BeeShop",

            # Egg Shop
            "All": "EggShop",
        }

        # NOTE: Edit upon newer updates
        self.seeds = {
            # Seed Shop:
            "SeedShop": 0,
            "Carrot": False,
            "Strawberry": False,
            "Blueberry": False,
            "OrangeTulip": False,
            "TomatoSeed": False,
            "CornSeed": False,
            "DaffodilSeed": False,
            "WatermelonSeed": False,
            "PumpkinSeed": False,
            "AppleSeed": False,
            "BambooSeed": False,
            "CoconutSeed": False,
            "CactusSeed": False,
            "DragonFruitSeed": False,
            "MangoSeed": False,
            "GrapeSeed": False,
            "MushroomSeed": False,
            "PepperSeed": False,
            "CacaoSeed": False,
            "BeanstalkSeed": False,

            # Gear:
            "GearShop": 0,
            "WateringCan": False,
            "Trowel": False,
            "RecallWrench": False,
            "BasicSprinkler": False,
            "AdvancedSprinkler": False,
            "GodlySprinkler": False,
            "LightningRod": False,
            "MasterSprinkler": False,
            "FavoriteTool": False,
            "HarvestTool": False,

            # Bee Shop:
            "BeeShop": 0,
            "FlowerSeedPack": False,
            "NectarineSeed": False,
            "HiveFruitSeed": False,
            "HoneySprinkler": False,
            "BeeEgg": False,
            "BeeCrate": False, 
            "HoneyComb": False,
            "BeeChair": False,
            "HoneyTorch": False,
            "HoneyWalkway": False,
            "CompressHoney": False,
            
            # Eggshop:
            "EggShop": 0,
            "All": False
        }

        for seed in self.seeds:
            self.seed_vars[seed] = tk.BooleanVar(value=self.seeds[seed])

        self.loadOptions()

    def saveOptions(self):
        settings = {}
        for seed in self.seeds:
            settings[seed] = self.seed_vars[seed].get()

        try:
            with open("MacroSettings.json", "w") as file:
                json.dump(settings, file, indent=4)  # Adds indent
        except Exception as e:
            print(f"Error saving settings: {e}")

    def loadOptions(self):
        if os.path.exists("MacroSettings.json") and os.path.getsize("MacroSettings.json") > 0:
            with open("MacroSettings.json", "r") as file:
                settings = json.load(file)
                
                # Update variables from loaded settings
                for seed in settings:
                    if seed in self.seed_vars:
                        self.seed_vars[seed].set(settings[seed])    # Ttinker set method
                        self.seeds[seed] = settings[seed]           # Dictionary set method
                
                # Recalculate category counts
                self.recalculateCategory()
        else:
            # Create a default settings file
            self.saveOptions()

    def recalculateCategory(self):
        for category in ["SeedShop", "GearShop", "BeeShop", "EggShop"]:
            self.seeds[category] = 0

        for seed, category in self.shopCategories.items():
            if self.seeds.get(seed, False):
                self.seeds[category] += 1


    def onClose(self):
        if self.macro is not None and self.macro.is_running:
            self.macro.stop()

        keyboard.unhook_all()    
        self.saveOptions()

        for thread in threading.enumerate():
            if thread != threading.current_thread():
                thread.join(timeout=0.1)  # Try to close nicely first
    
        # Destroy the window
        self.toplv.destroy()
        subprocess.run(["taskkill", "/F", "/PID", str(os.getpid())], shell=True)
        os._exit(0)

    def setup_global_hotkeys(self):
        # Bind Ctrl+2 to stopMacro
        keyboard.add_hotkey('ctrl+2', self.stopMacroKeybind, suppress=True, timeout=0.001)

    def newlvBuilder(self):
        toplv = self.toplv
        xGeo, yGeo = 600, 800

        toplv.geometry(f"{xGeo}x{yGeo}")
        toplv.title("Grow A Garden Multi Alt Macro")
        toplv.config(background="#292928")
        toplv.resizable(False, False)

        # Create style for notebook
        style = ttk.Style()
        style.theme_create("custom", parent="default", settings={
            "TNotebook": {      # Notebook styles
                "configure": {
                    "background": "#1e1e1e",  # Dark background for tab bar
                    "tabmargins": [5, 5, 0, 0],  # Margins around tabs
                }
            },
            "TNotebook.Tab": {      # Individual Tab Styles
                "configure": {
                    "background": "#3d3d3d",  # Inactive tab color
                    "foreground": "white",
                    "padding": [15, 5],  # Horizontal, vertical padding
                    "font": ('Comic Sans MS', 10)
                },
                "map": {        # State dependant tab styles
                    "background": [("selected", "#4d4d4d")],  # Active tab color
                    "expand": [("selected", [1, 1, 1, 0])]  # Stretch selected tab
                }
            }
        })
        style.theme_use("custom")

        # Pack notebook to fill window
        containFrame = Frame(toplv, bg="#292928")
        containFrame.pack(expand=True, fill="both", padx=20, pady=20)

        # Create notebook with top tab bar
        shopBook = ttk.Notebook(containFrame)
        shopBook.pack(expand=True, fill="both")
        
        # Create frames with dark background
        regSeeds = Frame(shopBook, bg="#292928")
        gearShop = Frame(shopBook, bg="#292928")
        eggShop = Frame(shopBook, bg="#292928")
        eventShop = Frame(shopBook, bg="#292928")
        startTab = Frame(shopBook, bg="#292928")

        # Add tabs to notebook
        shopBook.add(regSeeds, text="Regular")
        shopBook.add(gearShop, text="Gear")
        shopBook.add(eggShop, text="Eggs")
        shopBook.add(eventShop, text="Events")
        shopBook.add(startTab, text="Start Macro")

        # Event shop dropdown combo menu NOTE: Change this for event things
        eventsVar = tk.StringVar()
        events = ["BeeShop", "Bloodmoon", "Twilight"]

        
        # Configure the Combobox style
        style.configure('TCombobox', 
                        foreground="#ffffff",  # Text color
                        fieldbackground='#1e1e1e',  # Background color of the entry
                        background='#1e1e1e',  # Background color of the dropdown button
                        selectbackground="#333333",  # Background of selected item in dropdown
                        selectforeground="#ffffff")  # Text color of selected item
        
        eventDropdown = ttk.Combobox(eventShop, textvariable=eventsVar, values=events, font=("Comic Sans MS", 10), style="TCombobox")
        eventDropdown.config(background="#1e1e1e")
        eventDropdown.pack()
        eventDropdown.current(0)
        
        # Create a container frame for the different tabs
        seedGrid = Frame(regSeeds, bg="#292928")
        seedGrid.pack(fill="both", expand=True, padx=10, pady=10)

        gearGrid = Frame(gearShop, bg="#292928")
        gearGrid.pack(fill="both", expand=True, padx=10, pady=10)

        eggGrid = Frame(eggShop, bg="#292928")
        eggGrid.pack(fill="both", expand=True, padx=10, pady=10)

        eventShopGrid = Frame(eventShop, bg="#292928")
        eventShopGrid.pack(fill="both", expand=True, padx=10, pady=10)

        # TODO: Changes combobox
        def eventMenuChange(select):
            # Bee Shop
            if select == "BeeShop":
                for col in range(self.beeShopMC):
                    eventShopGrid.grid_columnconfigure(col, weight=1)

                # NOTE: Edit upon newer updates
                beeshopItems = ["FlowerSeedPack", "NectarineSeed", "HiveFruitSeed", "HoneySprinkler", 
                                "BeeEgg", "BeeCrate", "HoneyComb", "BeeChair", "HoneyTorch", "HoneyWalkway", "CompressHoney"]
            
                for i, bItems in enumerate(beeshopItems):
                    row = i // self.beeShopMC
                    column = i % self.beeShopMC

                    Checkbutton(
                        eventShopGrid,
                        text=bItems,
                        variable=self.seed_vars[bItems],
                        onvalue=True,
                        offvalue=False,
                        command=lambda b=bItems: self.updateSeed(b),
                        bg="#292928",
                        fg="white",
                        selectcolor="#1e1e1e",
                        activebackground="#292928",
                        activeforeground="white",
                        anchor="w",
                        width=18 
                        ).grid(
                        row=row,
                        column=column,
                        sticky="nsew",  # Expand to fill cell
                        padx=5,
                        pady=2
                    )

                # Expanding Rows
                total_rows = (len(beeshopItems) // self.beeShopMC) + 1
                for row in range(total_rows):
                    eventShopGrid.grid_rowconfigure(row, weight=1)

        def onShopChange(event=None):
            for frame in eventShopGrid.winfo_children():
                frame.destroy()  

            selected = eventsVar.get()

            eventMenuChange(selected)

        eventDropdown.bind("<<ComboboxSelected>>", onShopChange)
        onShopChange()   


        # Reg Seeds
        for col in range(self.seedMaxC):
            seedGrid.grid_columnconfigure(col, weight=1)

        # NOTE: Edit upon newer updates
        regularSeeds = ["Carrot", "Strawberry", "Blueberry", "OrangeTulip", "TomatoSeed", "CornSeed", 
                        "DaffodilSeed", "WatermelonSeed", "PumpkinSeed", "AppleSeed", "BambooSeed", 
                        "CoconutSeed", "CactusSeed", "DragonFruitSeed", "MangoSeed", "GrapeSeed", "MushroomSeed", 
                        "PepperSeed", "CacaoSeed", "BeanstalkSeed"]
                        
        # Add checkbuttons in grid layout
        for i, seed in enumerate(regularSeeds):
            row = i // self.seedMaxC
            column = i % self.seedMaxC

            Checkbutton(
                seedGrid,
                text=seed,
                variable=self.seed_vars[seed],
                onvalue=True,
                offvalue=False,
                command=lambda s=seed: self.updateSeed(s),
                bg="#292928",
                fg="white",
                selectcolor="#1e1e1e",
                activebackground="#292928",
                activeforeground="white",
                anchor="w",
                width=18  
                ).grid(
                row=row,
                column=column,
                sticky="nsew",  # Expand to fill cell
                padx=5,
                pady=2
            )

        # Expanding Rows
        total_rows = (len(regularSeeds) // self.seedMaxC) + 1
        for row in range(total_rows):
            seedGrid.grid_rowconfigure(row, weight=1)

        # Gear Shop
        for col in range(self.gearMaxC):
            gearGrid.grid_columnconfigure(col, weight=1)

        # NOTE: Edit upon newer updates
        gearItems = ["WateringCan", "Trowel", "RecallWrench", "BasicSprinkler", "AdvancedSprinkler", 
                     "GodlySprinkler", "LightningRod", "MasterSprinkler", "FavoriteTool", "HarvestTool"]

        for i, gear in enumerate(gearItems):
            row = i // self.gearMaxC
            column = i % self.gearMaxC

            Checkbutton(
                gearGrid,
                text=gear,
                variable=self.seed_vars[gear],
                onvalue=True,
                offvalue=False,
                command=lambda g=gear: self.updateSeed(g),
                bg="#292928",
                fg="white",
                selectcolor="#1e1e1e",
                activebackground="#292928",
                activeforeground="white",
                anchor="w",
                width=18  
                ).grid(
                row=row,
                column=column,
                sticky="nsew",  # Expand to fill cell
                padx=5,
                pady=2
            )

        # Expanding Rows
        total_rows = (len(gearItems) // self.gearMaxC) + 1
        for row in range(total_rows):
            gearGrid.grid_rowconfigure(row, weight=1)

        # Egg Shop
        for col in range(self.eggMaxC):
            eggGrid.grid_columnconfigure(col, weight=1)

        # NOTE: Edit upon newer updates
        eggShopList = ["All"]

        for i, egg in enumerate(eggShopList):
            row = i // self.eggMaxC
            column = i % self.eggMaxC

            Checkbutton(
                eggGrid,
                text=egg,
                variable=self.seed_vars[egg],
                onvalue=True,
                offvalue=False,
                command=lambda e=egg: self.updateSeed(e),
                bg="#292928",
                fg="white",
                selectcolor="#1e1e1e",
                activebackground="#292928",
                activeforeground="white",
                anchor="w",
                width=18  
                ).grid(
                row=row,
                column=column,
                sticky="nsew",  # Expand to fill cell
                padx=5,
                pady=2
            )

        # Expanding Rows
        total_rows = (len(eggShopList) // self.eggMaxC) + 1
        for row in range(total_rows):
            eggGrid.grid_rowconfigure(row, weight=1)
        
        Button(startTab, 
            text="Start Macro",
            font=("Comic Sans MS", 12, 'bold'),  
            width=14, 
            height=2,  
            bd=0,
            highlightthickness=0,
            highlightbackground="#4d4d4d",
            highlightcolor="#4d4d4d",
            fg="White",
            bg="#4d4d4d",  
            activebackground="#3d3d3d",
            padx=10,  
            pady=5,   
            takefocus=0,
            command=self.startMacro # lambda: self.runMacro(self.seeds, self.reruns, True)
            ).pack(pady=(20,0), expand=True)
        
        Button(startTab, 
            text="Stop: Ctrl + 2",
            font=("Comic Sans MS", 12, 'bold'), 
            width=14,  
            height=2, 
            bd=0,
            highlightthickness=0,
            highlightbackground="#4d4d4d",
            highlightcolor="#4d4d4d",
            fg="White",
            bg="#4d4d4d",  
            activebackground="#3d3d3d",
            padx=10, 
            pady=5,   
            takefocus=0,
            command=self.stopMacro  
            ).pack(pady=(0,20), expand=True)
        
        self.toplv.protocol("WM_DELETE_WINDOW", self.onClose)

    # TODO: Make it update into a file so it saves the settings
    def updateSeed(self, seedName):
        self.seeds[seedName] = self.seed_vars[seedName].get()
        category = self.shopCategories.get(seedName)

        if self.seed_vars[seedName].get() is True:
            self.seeds[category] +=1
        else:
            self.seeds[category] -=1

        # print(f"{seedName} state: {self.seeds[seedName]}") 
        # print(f"{category} Buying: {self.seeds[category]}")

        self.saveOptions()

    def startMacro(self):  
        if self.macro is None or not self.macro.is_running:
            self.macro = Macro(self.seeds, self.reruns)
            self.macro.start()
            print("Macro started")


    def stopMacroKeybind(self, event=None):  
        self.stopMacro()

    def stopMacro(self):  
        if  self.macro is not None and self.macro.is_running:
            self.macro.stop()
            self.macro = None
            # self.macro.thread.join(timeout=0.5)
            print("Macro stopped")
        else:
            print("No active macro to stop")





