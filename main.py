from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivymd.toast import toast


class MainApp(MDApp):
                              

    def long_trade(self):
            account_size = float(self.root.ids.account_size.text)
            entry_price = float(self.root.ids.entry_price.text)
            multiplier = float(self.root.ids.multiplier.text)
            risk_percentage = float(self.root.ids.risk_percentage.text)
            stoploss = float(self.root.ids.stoploss.text)
            takeprofit = float(self.root.ids.takeprofit.text)

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
            position_size = float(risk_amount / risk_plus_multiplier)
            
            # Calculate asset amount to enter 
            asset_amount =float(position_size / stoploss)

            r_to_r = float(potential_profit / potential_risk)

            # Update labels -> this label shows the dollar amount
            self.root.ids.dollar_amount_label.text = f"Dollar Amount: {round(position_size, 2)}"
            # Update labels -> this label shows the asset amount to buy
            self.root.ids.position_size_label.text = f"Position Size: {round(asset_amount, 2)}"
            #Update labels -> this label show the risk to reward ration
            self.root.ids.r_to_r_label.text = f'Risk To Reward: {round(r_to_r, 2)}'
            toast("Calculation Completed Successfully")
    def short_trade(self):

        account_size = float(self.root.ids.account_size.text)
        entry_price = float(self.root.ids.entry_price.text)
        multiplier = float(self.root.ids.multiplier.text)
        risk_percentage = float(self.root.ids.risk_percentage.text)
        stoploss = float(self.root.ids.stoploss.text)
        takeprofit = float(self.root.ids.takeprofit.text)

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
        position_size = float(risk_amount / risk_plus_multiplier)
        
        # Calculate asset amount to enter 
        asset_amount =float(position_size / stoploss)

        r_to_r = float(potential_profit / potential_risk)

        # Update labels -> this label shows the dollar amount
        self.root.ids.dollar_amount_label.text = f"Dollar Amount: {round(position_size, 2)}"
        # Update labels -> this label shows the asset amount to buy
        self.root.ids.position_size_label.text = f"Position Size: {round(asset_amount, 2)}"
        #Update labels -> this label show the risk to reward ration
        self.root.ids.r_to_r_label.text = f'Risk To Reward: {round(r_to_r, 2)}'
        toast("Calculation Completed Successfully")
    def clear_all(self):
         # Update labels -> this label shows the dollar amount
        self.root.ids.dollar_amount_label.text = f"Dollar Amount:"
        # Update labels -> this label shows the asset amount to buy
        self.root.ids.position_size_label.text = f"Position Size:"
        #Update labels -> this label show the risk to reward ration
        self.root.ids.r_to_r_label.text = f'Risk To Reward:'
        

        self.root.ids.account_size.text = ""
        self.root.ids.entry_price.text = ""
        self.root.ids.multiplier.text = ""
        self.root.ids.risk_percentage.text = ""
        self.root.ids.stoploss.text = ""
        self.root.ids.takeprofit.text = ""

    def build(self):
        self.theme_cls.theme_style = "Light"
        return Builder.load_file("Main.kv")
    
    


MainApp().run()