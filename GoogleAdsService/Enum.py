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


Gender = {}
Gender.update({"UNSPECIFIED" : lambda: client.get_type("GenderTypeEnum").GenderType.UNSPECIFIED})
Gender.update({"UNKNOWN" : lambda: client.get_type("GenderTypeEnum").GenderType.UNKNOWN})
Gender.update({"MALE" : lambda: client.get_type("GenderTypeEnum").GenderType.MALE})
Gender.update({"FEMALE" : lambda: client.get_type("GenderTypeEnum").GenderType.FEMALE})
Gender.update({"UNDETERMINED" : lambda: client.get_type("GenderTypeEnum").GenderType.UNDETERMINED})

Device = {}
Device.update({"UNSPECIFIED" : lambda: client.get_type("DeviceEnum").Device.UNSPECIFIED })
Device.update({"UNKNOWN" : lambda: client.get_type("DeviceEnum").Device.UNKNOWN })
Device.update({"MOBILE" : lambda: client.get_type("DeviceEnum").Device.MOBILE })
Device.update({"TABLET" : lambda: client.get_type("DeviceEnum").Device.TABLET })
Device.update({"DESKTOP" : lambda: client.get_type("DeviceEnum").Device.DESKTOP })
Device.update({"CONNECTED_TV" : lambda: client.get_type("DeviceEnum").Device.CONNECTED_TV })
Device.update({"OTHER" : lambda: client.get_type("DeviceEnum").Device.OTHER })


Age_1 = {}
Age_1.update({"UNSPECIFIED" : lambda : client.get_type("AgeRangeTypeEnum").AgeRangeType.UNSPECIFIED})
Age_1.update({"UNKNOWN" : lambda : client.get_type("AgeRangeTypeEnum").AgeRangeType.UNKNOWN})
Age_1.update({"AGE_RANGE_18_24" : lambda : client.get_type("AgeRangeTypeEnum").AgeRangeType.AGE_RANGE_18_24})
Age_1.update({"AGE_RANGE_25_34" : lambda : client.get_type("AgeRangeTypeEnum").AgeRangeType.AGE_RANGE_25_34})
Age_1.update({"AGE_RANGE_35_44" : lambda : client.get_type("AgeRangeTypeEnum").AgeRangeType.AGE_RANGE_35_44})
Age_1.update({"AGE_RANGE_45_54" : lambda : client.get_type("AgeRangeTypeEnum").AgeRangeType.AGE_RANGE_45_54})
Age_1.update({"AGE_RANGE_55_64" : lambda : client.get_type("AgeRangeTypeEnum").AgeRangeType.AGE_RANGE_55_64})
Age_1.update({"AGE_RANGE_65_UP" : lambda : client.get_type("AgeRangeTypeEnum").AgeRangeType.AGE_RANGE_65_UP})
Age_1.update({"AGE_RANGE_UNDETERMINED" : lambda : client.get_type("AgeRangeTypeEnum").AgeRangeType.AGE_RANGE_UNDETERMINED})

Age_2= {}
Age_2.update({(0,1) : lambda : client.get_type("AgeRangeTypeEnum").AgeRangeType.UNSPECIFIED})
Age_2.update({(0,0): lambda : client.get_type("AgeRangeTypeEnum").AgeRangeType.UNKNOWN})
Age_2.update({(18,24) : lambda : client.get_type("AgeRangeTypeEnum").AgeRangeType.AGE_RANGE_18_24})
Age_2.update({(25,34) : lambda : client.get_type("AgeRangeTypeEnum").AgeRangeType.AGE_RANGE_25_34})
Age_2.update({(35,44) : lambda : client.get_type("AgeRangeTypeEnum").AgeRangeType.AGE_RANGE_35_44})
Age_2.update({(45,54): lambda : client.get_type("AgeRangeTypeEnum").AgeRangeType.AGE_RANGE_45_54})
Age_2.update({(55,64) : lambda : client.get_type("AgeRangeTypeEnum").AgeRangeType.AGE_RANGE_55_64})
Age_2.update({(65,120) : lambda : client.get_type("AgeRangeTypeEnum").AgeRangeType.AGE_RANGE_65_UP})
Age_2.update({(1,1) : lambda : client.get_type("AgeRangeTypeEnum").AgeRangeType.AGE_RANGE_UNDETERMINED})



















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

