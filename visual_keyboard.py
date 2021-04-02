# import kivy module  
import kivy  
      
# this restricts the kivy version i.e  
# below this kivy version you cannot  
# use the app or software  
kivy.require("1.9.1")  
      
# base Class of your App inherits from the App class.  
# app:always refers to the instance of your application  
from kivy.app import App
  
# VKeyboard is an onscreen keyboard
# for Kivy. Its operation is intended
# to be transparent to the user. 
from kivy.uix.vkeyboard import VKeyboard
  
# Create the vkeyboard
class Test(VKeyboard):
    player = VKeyboard()
  
# Create the App class
class VkeyboardApp(App):
    def build(self):
        return Test()
  
# run the App
if __name__ == '__main__':
    VkeyboardApp().run()