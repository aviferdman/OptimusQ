import os

from google.ads.googleads.client import GoogleAdsClient

# This interface allows the user to create and manage all the marketing fields,
# using Google Ads APIs.
dir_path = os.path.dirname(os.path.realpath(__file__))
curr_path = dir_path + "\google-ads.yaml"
client = GoogleAdsClient.load_from_storage(path=curr_path, version="v9")

Payments = {}
Payments.update({"CLICKS": lambda : client.get_type("PaymentModeEnum").PaymentMode.CLICKS})
Payments.update({"CONVERSIONS": lambda : client.get_type("PaymentModeEnum").PaymentMode.CONVERSIONS})
Payments.update({"CONVERSION_VALUE": lambda : client.get_type("PaymentModeEnum").PaymentMode.CONVERSION_VALUE})
Payments.update({"GUEST_STAY": lambda : client.get_type("PaymentModeEnum").PaymentMode.GUEST_STAY})












ChanelType = {}
ChanelType.update({"DISCOVERY": lambda : client.get_type("AdvertisingChannelTypeEnum").AdvertisingChannelType.DISCOVERY})
ChanelType.update({"DISPLAY": lambda : client.get_type("AdvertisingChannelTypeEnum").AdvertisingChannelType.DISPLAY})
ChanelType.update({"HOTEL": lambda : client.get_type("AdvertisingChannelTypeEnum").AdvertisingChannelType.HOTEL})
ChanelType.update({"LOCAL": lambda : client.get_type("AdvertisingChannelTypeEnum").AdvertisingChannelType.LOCAL})
ChanelType.update({"LOCAL_SERVICES": lambda : client.get_type("AdvertisingChannelTypeEnum").AdvertisingChannelType.LOCAL_SERVICES})
ChanelType.update({"MULTI_CHANNEL": lambda : client.get_type("AdvertisingChannelTypeEnum").AdvertisingChannelType.MULTI_CHANNEL})
ChanelType.update({"PERFORMANCE_MAX": lambda : client.get_type("AdvertisingChannelTypeEnum").AdvertisingChannelType.PERFORMANCE_MAX})
ChanelType.update({"SEARCH": lambda : client.get_type("AdvertisingChannelTypeEnum").AdvertisingChannelType.SEARCH})
ChanelType.update({"SHOPPING": lambda : client.get_type("AdvertisingChannelTypeEnum").AdvertisingChannelType.SHOPPING})
ChanelType.update({"SMART": lambda : client.get_type("AdvertisingChannelTypeEnum").AdvertisingChannelType.SMART})
ChanelType.update({"UNKNOWN": lambda : client.get_type("AdvertisingChannelTypeEnum").AdvertisingChannelType.UNKNOWN})
ChanelType.update({"UNSPECIFIED": lambda : client.get_type("AdvertisingChannelTypeEnum").AdvertisingChannelType.UNSPECIFIED})
ChanelType.update({"VIDEO": lambda : client.get_type("AdvertisingChannelTypeEnum").AdvertisingChannelType.VIDEO})

