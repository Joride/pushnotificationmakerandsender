pushnotificationmakerandsender
==============================

Python implementation to construct and send iOS push notifications.

Ther is one class representing the actual push-message: 'ApplePushNotification'. You can simply set some properties on it and hand it to the second class: 'ApplePushNotificationSender'. This class will send it over the connection to APNS, sandbox or production, depending on a property you can set. This class can also readout the feedback service and return the invalud tokens+timestamps.

N.b.! Sending a pushmessage over a connection might result in Apple returning an error package and closing the connection. This is not handled. There is a comment in the ApplePushNotificationSender about this. If you know how to do this, please let me know!
