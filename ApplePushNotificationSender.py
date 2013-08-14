#!/usr/bin/env python

import socket, ssl, struct, sys, binascii
from ApplePushNotification import ApplePushNotification 
import select

class ApplePushNotificationSender(object):
    """An object encapsulating the details that are required for sending
    Apple Push notifications. It has one dependencies: the certificate file (.pem)
    obtained through the Apple Developer Portal.
    It is required to set the 'environment' variable to either 'sandbox' or 'production' for
    the receiver to be able to execute the 'send' method.
    @properties:
        certificate (readonly)
        environment
        pushNotifications - an array of ApplePushNotification objects
    """
    
    def __init__(self, filename = None):
        if filename == None:
            raise ValueError, "Invalid argument filename"
            
        self._certificateFileName = filename
        self._pushNotifications = []
        self._environment = None
        self._APNSHost = (None,None,)
        self._APNSFeedbackHost = (None,None,)
        

    def getCertificateFileName(self):
        return self._certificateFileName
    certificate = property(getCertificateFileName)
        
    def setEnvironment(self, environment = None):
        self._environment = environment
        if self._environment == "sandbox":
            self._APNSHost = ( 'gateway.sandbox.push.apple.com', 2195 )
            self._APNSFeedbackHost = ('feedback.sandbox.push.apple.com', 2196)
        elif self._environment == "production":
            self._APNSHost = ( 'gateway.push.apple.com', 2195 )
            self._APNSFeedbackHost = ('feedback.push.apple.com', 2196)
        else:
            raise ValueError, "Invalid argument: '%s'. Use 'sandbox' or 'production'" % (environment)
   
    def getEnvironment(self):
        return self._environment
    environment = property(getEnvironment, setEnvironment)
        
    def setPushNotifications(self, pushNotifications):
        self._pushNotifications = pushNotifications;
    def getPushNotifications(self):
        return self._pushNotifications
    pushNotifications = property(getPushNotifications, setPushNotifications)
    
    def sendPushNotifications(self):
        """Sends the pushnotifications. After sending, the pushnotifications are removed from the object."""
        
        # open the gates to Apples Push Notifications Server
        ssl_sock = ssl.wrap_socket( socket.socket( socket.AF_INET, socket.SOCK_STREAM ), certfile = self._certificateFileName )
        ssl_sock.connect( self._APNSHost )

        ssl_sock.settimeout(0.1)
        # send the actual pushMessages
        for aPushNotification in self.pushNotifications:
            # Write out our data
            ssl_sock.write( aPushNotification.sendable)
            
            # ideally the return value from the write action should be
            # obtained here. When we get an error-packet, the connection
            # is closed by Apple and all subsequent push messages will
            # end up not reaching APNS (thus failing without us knowing!).
            # problem is: my skills are too limited to make this work.
            
            # If you know how to read out the socket, please do, and use
            # these Apple docs to find out the detais:
            # http://developer.apple.com/library/ios/documentation/NetworkingInternet/Conceptual/RemoteNotificationsPG/Chapters/CommunicatingWIthAPS.html#//apple_ref/doc/uid/TP40008194-CH101-SW4
            
        # Close the connection, our push messages have been sent
        ssl_sock.close()
        
        self._pushNotifications = []
        
    def getAbsoleteDeviceTokens(self, maxNumberOfTokens = sys.maxint):
        """
        This method connects to Apples Push Notification Feedback Service and
        retrieves all deviceTokens and timestamps that indicates when it was
        discovered when these were rendered absolete.
        Returns an array of tuples, each tuples contains a UTC timestam (as int)
        and the deviceToken (as ascii string).
        N.b.: when a device is sent a Push notification while the app is no longer
        present on the device, the token will be retrieved here, whether the 
        user re-installed the app or not. So that's what the timestamp is for:
        we need to maintain a list of tokens and when they were last registered with 
        our server. Is that is past the retrieved timestamp, the token is actually
        still valid.
        """
        # open the gates to Apples Push Notifications Server
        ssl_sock = ssl.wrap_socket( socket.socket( socket.AF_INET, socket.SOCK_STREAM ), certfile = self._certificateFileName )
        ssl_sock.connect( self._APNSFeedbackHost )
        
        """
        Parse header of Feedback Service tuple.
        Format of Buff is |xxxx|yy|zzzzzzzz|
        where:
        x is time_t (UNIXTIME, long, 4 bytes)
        y is length of z (two bytes)
        z is device token
        """
        
        timestampsAndTokens = []
        headerBuffer = ssl_sock.read(6)
        iteration = 0
        # while the headerbuffer yields some value, we process it (as a 
        # security measure, an option is built in to limit the number
        # of iterations (preventing an infinite loop)
        while (len(headerBuffer) > 0) and (iteration < maxNumberOfTokens):
            (timestamp,  tokenLength) = struct.unpack(">lh", headerBuffer)
            
            buffer = ssl_sock.read(tokenLength)
            deviceTokenHex = struct.unpack_from('%ds' % tokenLength, buffer)
            # deviceTokenHex is a tuple containing one item
            deviceToken = binascii.b2a_hex(deviceTokenHex[0])
            
            # read next header, returns zero-length buffer if EOF
            headerBuffer = ssl_sock.read(6)
            
            timestampsAndTokens.append((timestamp, deviceToken,))
            iteration += 1
            
                    
        ssl_sock.close()
        
        return timestampsAndTokens