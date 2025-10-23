from Raspbot_Lib import Raspbot
import time

bot = Raspbot()             # bot Create the Rosmaster object bot   
bot.Ctrl_BEEP_Switch(1)
time.sleep(1)
bot.Ctrl_BEEP_Switch(0)

del bot                     # Release Object