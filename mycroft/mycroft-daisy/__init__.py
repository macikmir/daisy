# Copyright 2016 Mycroft AI, Inc.
#
# This file is part of Mycroft Core.
#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.

from adapt.intent import IntentBuilder

from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger

from . import pixels 
from . import humidityReader

__author__ = 'macikmir'

LOGGER = getLogger(__name__)

pixelsInstance = pixels.Pixels()

class DaisyFlowerSkill(MycroftSkill):
    def __init__(self):
        super(DaisyFlowerSkill, self).__init__(name="DaisyFlowerSkill")

    def initialize(self):

        who_are_you_intent = IntentBuilder("WhoAreYouIntent"). \
            require("WhoAreYouKeyword").build()
        self.register_intent(who_are_you_intent, self.handle_who_are_you_intent)

        how_are_you_intent = IntentBuilder("HowAreYouIntent"). \
            require("HowAreYouKeyword").build()
        self.register_intent(how_are_you_intent,
                             self.handle_how_are_you_intent)

        can_i_tell_you_something_intent = IntentBuilder("CanITellYouSomethingIntent").require("CanITellYouSomething").build()
        self.register_intent(can_i_tell_you_something_intent, self.handle_can_i_tell_you_something_intent)
    
        watering_plant_first_intent = IntentBuilder("WateringPlantFirstIntent").require("Wateringplantfirst").build()
        self.register_intent(watering_plant_first_intent, self.handle_watering_plant_first_intent)

        self.humidityReaderInstance = humidityReader.I2C_Humidity_Reader()
        
    def ask_for_name(self):
        newUser = self.settings.get('new.user')
        if (newUser == True):
            userName = self.get_response('what.is.your.name')
            self.settings['new.user'] = False
            self.settings['user.name'] = userName
            self.speak(self.settings.get('user.name'),expect_response=False)
            self.speak_dialog("is.nice.name",expect_response=False)

    def handle_who_are_you_intent(self, message):
        pixelsInstance.speak()
        self.speak_dialog("hello",expect_response=False)
        newUser = self.settings.get('new.user')
        if (newUser == False):
            self.speak(self.settings.get('user.name'))
        self.speak_dialog("who.am.i",expect_response=False)
        
        self.ask_for_name()
        
        somethingOnMind = self.ask_yesno('something.on.mind')
        pixelsInstance.listen()
        if somethingOnMind == "yes":
            pixelsInstance.speak()
            userHasOnMind = self.ask_yesno('whats.on.your.mind')
            pixelsInstance.listen()
            userHasOnMindTransformed = userHasOnMind.replace('i', 'you', 1)
            self.speak(self.translate("i.am.sorry.to.hear") + " " + userHasOnMindTransformed,expect_response=False)
        else:
            pixelsInstance.speak() 
            wantsPoem = self.ask_yesno('do.you.want.poem')
            pixelsInstance.listen
            if wantsPoem == "yes":
                pixelsInstance.speak()
                self.speak_dialog("speak.poem",expect_response=False)
            else:
                pixelsInstance.speak() 
                self.speak_dialog("ok.talk.later",expect_response=False)

    def handle_how_are_you_intent(self, message):
        self.speak_dialog("hello",expect_response=False)
        newUser = self.settings.get('new.user')
        if (newUser == False):
            self.speak(self.settings.get('user.name'))       
        self.speak_dialog("how.are.you",expect_response=False)
        self.ask_for_name()
        humidityReading = self.humidityReaderInstance.get_data()
        if (humidityReading < 5):
            self.speak_dialog("i.feel.thirsty",expect_response=False)
    
    def handle_watering_plant_first_intent(self, message):
        self.speak_dialog("watering.plant.first.positive")
        self.speak_dialog("watering.plant.first.negative")
    def handle_can_i_tell_you_something_intent(self, message):
        self.speak_dialog("can.i.tell.you.something")
      
        something = self.get_response("whats.on.your.mind")
        self.speak_dialog("compliment")   
        

    def stop(self):
        pass


def create_skill():
    return DaisyFlowerSkill()
