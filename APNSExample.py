#!/usr/bin/env python

# Joride, 2013

import sys
#prevent .pyc files from being written
sys.dont_write_bytecode = True

from ApplePushNotification import ApplePushNotification
from ApplePushNotificationSender import ApplePushNotificationSender

# the certificate file has to reside in the working dir for this to work
certfile = '/path/to/yourPemFile.pem'

# if this script was called from the command line, we might have arguments
message = "Test push message from me.'"
badgeCount = 0
if len(sys.argv) > 1:
    message = str(sys.argv[1])
if len(sys.argv) > 2:
    badgeCount = int(sys.argv[2])
    
# obtained by running an iOS app on a device and registering it for push
# notifications. The pushToken is received in one of the callbackmethods
deviceTokens = (
'3A66E26F03B9ABC5455446DA72BT1AA6CFBA27C499C4F92FA67F39B9A88A03F5',
'15606ACC6ED0BC0FFBD53F28F25G95C5421B0CB3A69486446ADDC97AE17E470R',
)

pushNotifications = []
for aDeviceToken in deviceTokens:
    pn = ApplePushNotification()
    pn.deviceToken = aDeviceToken
    pn.message = message
    pushNotifications.append(pn)

pnSender = ApplePushNotificationSender(certfile)
pnSender.environment = 'sandbox'
pnSender.pushNotifications = pushNotifications
pnSender.sendPushNotifications()

absTokens = pnSender.getAbsoleteDeviceTokens()
print absTokens
for aTuple in absTokens:
    timeinterval = aTuple[0]
    deviceToken = aTuple[1]
    timestamp = datetime.fromtimestamp(timeinterval)
    print "timestampt: %s; token: %s" % (timestamp, deviceToken,)
