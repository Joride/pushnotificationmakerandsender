#!/usr/bin/env python

import unittest, sys
sys.dont_write_bytecode = True


from ApplePushNotificationSender import ApplePushNotificationSender

class TestApplePushNotificationSender(unittest.TestCase):
    """Tests the edge cases of the ApplePushNotificationclass.
    """
    def setUp(self):
        pass
        
    def testEnvironment(self):
        certfile = 'iOS APNS DEV On The Move.pem'
        pns = ApplePushNotificationSender(certfile)
        
        pns.environment = 'production'
        self.assertEqual(pns.environment, 'production')
        
        pns.environment = 'sandbox'
        self.assertEqual(pns.environment, 'sandbox')
        
        # misspelled
        self.assertRaises(ValueError, pns.setEnvironment, 'sanbox')
        self.assertRaises(ValueError, pns.setEnvironment, 'productio')
        
        
if __name__ == '__main__':
    unittest.main()