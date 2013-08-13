#!/usr/bin/env python

import json, struct

class ApplePushNotification (object):
    """Representation of an Apple Push Notification.
    Client code can simply set all the neccessary properties
    and this class will convert it to a ready-to send object, 
    'sendable'."""
    
    def __init__(self):
        self._message = ''
        self._badgeCount = 0
        self._soundName = 'default'
        self._deviceToken = None
        self._customData = {}
    
    def setMessage(self, message = ''):
        self._message = message;
    def getMessage(self):
        return self._message;
    message = property(getMessage, setMessage)
    
    def setBadgeCount(self, badgeCount = 0):
        self._badgeCount = badgeCount;
    def getBadgeCount(self):
        return self._badgeCount;
    badgeCount = property(getBadgeCount, setBadgeCount)
    
    def setSoundName(self, soundName = 'default'):
            self._soundName = soundName;
    def getSoundName(self):
            return self._soundName;
    soundName = property(getSoundName, setSoundName)
    
    def setDeviceToken(self, deviceToken):
        self._deviceToken = deviceToken;
    deviceToken = property(None, setDeviceToken)
    
    def addCustomDataForKey(self, customData = {}, key = "genericKey"):
        if key == "genericKey":
            key = "%s%i" % (key, len(self._customData))

        self._customData[key] = customData
         
    def sendable(self):
        payloadAsDictionary = {
            "aps" : {
                "alert" : self.message,
                "badge" : self.badgeCount,
                "sound" : self.soundName
            }
        }
        
        # add any custom data we might have
        for aKey in self._customData:
            payloadAsDictionary[aKey] = self._customData[aKey]
        
        # convert the dicionary to a json-string
        payloadAsString = json.dumps( payloadAsDictionary )
        
        # Clear out spaces in the device token and convert to hex
        deviceToken = self._deviceToken.replace(' ','')
        # byteToken = bytes.fromhex( deviceToken ) # Python 3
        byteToken = deviceToken.decode('hex') # Python 2

        format = '!BH32sH%ds' % len(payloadAsString)
        pushNotification = struct.pack( format, 0, 32, byteToken, len(payloadAsString), payloadAsString )
        
        return pushNotification
    sendable = property(sendable)
        
    def __str__(self):
        return "Message:\t\t'%s'\nBadgecount:\t%i\nSoundname:\t%s\nDevicetoken:\t%s\n\nSendable:\t%s" % (self.message, self.badgeCount, self.soundName, self._deviceToken, self.sendable)