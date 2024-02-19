from kivymd.app import MDApp # MD App import for building app
from kivy.lang import Builder # Builder to use kivy language
from kivymd.toast import toast # Toast for popup messages
from kivy.utils import get_color_from_hex # get color from hex to use hex codes ->impot here to use in .kv file
from kivy.core.text import LabelBase # importing to register our custom fonts
from kivymd.uix.dialog import MDDialog # import dialog for popup windows
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton # import raised buttons for use on popup windows
from kivy.core.clipboard import Clipboard

# register custom font inter for input field hint text
LabelBase.register(name='Inter', 
                   fn_regular='fonts/Inter-VariableFont_slnt,wght.ttf')


# import window for development purposes !!! remove before compile !!!
# Resize kivy window to model that of a phone
# from kivy.core.window import Window
# Window.size = (540, 1200)


# import android permissions and ask for persmissions
'''
# import android permissions and ask for persmissions
from kivy import platform

if platform == "android":
    from android.permissions import request_permissions, Permission
    request_permissions([
        Permission.WRITE_EXTERNAL_STORAGE, 
        Permission.CAMERA, 
        Permission.READ_EXTERNAL_STORAGE
        ])
'''

class MainApp(MDApp):
    
    # create empty dialog variable set to None, this way we can check
    # if a popup already exists to avoid creating multipler popups
    dialog = None

    # This function closes the dialog box
    def close_dialog(self, obj):
        self.dialog.dismiss() # .dismiss closes the dialog
        self.clear_all() # call clear all to reset fields when dialog is closed

    # Function to copy position size to clipboard
    def copy_clipboard(self, obj):
        Clipboard.copy(str(round(float(self.position_size), 3))) # Use kivy's Clipboard.copy method
        self.dialog.dismiss() # .dismiss closes the dialog
        self.clear_all() # call clear all to reset fields when dialog is closed
        # Toast to let the user know the position size was copied
        toast("Position Size Copied To Clipboard")

    # this function gets slider value for risk and updates input field
    def get_risk_slider_value(self, *args):
        slider_value = str(int(args[1])) # slider has 2 arguments in a list, the value is at index 1
        self.root.ids.risk_percentage.text = slider_value # set risk inputfield to update according to slider
    
    # this functions gets slider value for multiplier and updates input field
    def get_multiplier_slider_value(self, *args):
        slider_value = str(int(args[1])) # slider has 2 arguments in a list, the value is at index 1
        self.root.ids.multiplier.text = slider_value # set multiplier inputfield to update according to slider

        # Function to reset everything
    def clear_all(self):
        print(self.root.ids.account_size.text)
        self.root.ids.account_size.text = ""
        self.root.ids.entry_price.text = ""
        self.root.ids.multiplier.text = "1"
        self.root.ids.risk_percentage.text = "2"
        self.root.ids.stoploss.text = ""
        self.root.ids.takeprofit.text = ""

    # Function to calculate long trade
    def long_trade(self):
        # Add try method to avoid crash on exception can not convert str to float (empty fields)
        try:
            account_size = float(self.root.ids.account_size.text)
            entry_price = float(self.root.ids.entry_price.text)
            multiplier = float(self.root.ids.multiplier.text)
            risk_percentage = float(self.root.ids.risk_percentage.text)
            stoploss = float(self.root.ids.stoploss.text)
            takeprofit = float(self.root.ids.takeprofit.text)
            
            # Add try method to avoid crash on exception can not divide by 0 (user inserts wrong number)
            try:
                # convert risk percentage integer to decimal percentage
                risk_percentage = float(risk_percentage / 100)

                # Calculate risk amount in currency
                risk_amount = float(account_size * risk_percentage)

                # calculate potential profit and risk
                potential_risk = float(entry_price - stoploss)
                potential_profit = float(takeprofit - entry_price)

                # Calculate risk percentage
                risk_percentage = float(potential_risk / entry_price * 100)
                
                # calculate risk with multiplier
                risk_plus_multiplier = float((risk_percentage * multiplier) / 100)

                # calculate trade size
                self.position_size = float(risk_amount / risk_plus_multiplier)
                print(f"\nposition size{self.position_size}")
                
                # Calculate asset amount to enter 
                self.asset_amount =float(self.position_size / stoploss)
                print(f"\nasset amount {self.asset_amount}")

                self.r_to_r = int(potential_profit / potential_risk)    
                print(f"\nrtor {self.r_to_r}")
                
                # Create dialog
                self.dialog = MDDialog(
                    # Use markup to change title color and font family
                    title= '[color=000000][font_family=<Inter>]Trade Size[/font_family][/color]', 
                    md_bg_color="white",
                    # Use markup to change title color and font family
                    text= f'[color=000000][font_family=<Inter>]\n\nPosition Size: {round(self.position_size, 2)}\nRisk to Reward: 1:{self.r_to_r}\nAsset Amount: {round(self.asset_amount,3)}[/font_family][/color]',
                    buttons=[
                        MDFlatButton(
                            text="CLOSE",
                            theme_text_color="Custom",
                            text_color="red",
                            on_release= self.close_dialog # button calls close method
                            
                        ),
                        MDRectangleFlatButton(
                            text="Copy Position Size",
                            theme_text_color="Custom",
                            text_color="green",
                            line_color="green",
                            on_release=self.copy_clipboard # butotn calls copy to clipboard method
                        ),
                    ],
                )
                print(f'\nafter dialog {self.dialog.text}')
                self.dialog.open()
            # catch exception for zero division
            except ZeroDivisionError:
                toast("Those Number's Don't Seem Quite Right?")
        # catch exception for value error
        except ValueError:
            toast("Are those numbers from our world?")

    def short_trade(self):
        # Add try method to avoid crash on exception can not divide by 0 (user inserts wrong number)
        try:
            account_size = float(self.root.ids.account_size.text)
            entry_price = float(self.root.ids.entry_price.text)
            multiplier = float(self.root.ids.multiplier.text)
            risk_percentage = float(self.root.ids.risk_percentage.text)
            stoploss = float(self.root.ids.stoploss.text)
            takeprofit = float(self.root.ids.takeprofit.text)
            
            # Add try method to avoid crash on exception can not divide by 0 (user inserts wrong number)
            try:
                # convert risk percentage integer to decimal percentage
                risk_percentage = float(risk_percentage / 100)

                # Calculate risk amount in currency
                risk_amount = float(account_size * risk_percentage)

                # calculate potential profit and risk
                potential_risk = float(stoploss - entry_price)
                potential_profit = float(entry_price - takeprofit)

                # Calculate risk percentage
                risk_percentage = float(potential_risk / entry_price  * 100)
                
                # calculate risk with multiplier
                risk_plus_multiplier = float((risk_percentage * multiplier) / 100)

                # calculate trade size
                self.position_size = float(risk_amount / risk_plus_multiplier)
                
                # Calculate asset amount to enter 
                self.asset_amount =float(self.position_size / stoploss)

                self.r_to_r = int(potential_profit / potential_risk)

                # Create dialog
                self.dialog = MDDialog(
                    # Use markup to change title color and font family
                    title= '[color=000000][font_family=<Inter>]Trade Size[/font_family][/color]', 
                    md_bg_color="white",
                    # Use markup to change title color and font family
                    text= f'[color=000000][font_family=<Inter>]\n\nPosition Size: {round(self.position_size, 2)}\nRisk to Reward: 1:{self.r_to_r}\nAsset Amount: {round(self.asset_amount,3)}[/font_family][/color]',
                    buttons=[
                        MDFlatButton(
                            text="CLOSE",
                            theme_text_color="Custom",
                            text_color="red",
                            on_release= self.close_dialog # button calls close method
                            
                        ),
                        MDRectangleFlatButton(
                            text="Copy Position Size",
                            theme_text_color="Custom",
                            text_color="green",
                            line_color="green",
                            on_release=self.copy_clipboard # butotn calls copy to clipboard method
                        ),
                    ],
                )
                print(f'\nafter dialog {self.dialog.text}')
                self.dialog.open()
                
            # catch exception for zero division
            except ZeroDivisionError:
                toast("Those Number's Don't Seem Quite Right?")
        # catch exception for value error
        except ValueError:
            print("caught")
            toast("Are those numbers from our world?")
    

    
    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Builder.load_file("my.kv")

MainApp().run()
