from enum import Enum, auto

class ChannelType(Enum):
    DISCOVERY= auto(),
    DISPLAY= auto(),
    HOTEL= auto(),
    LOCAL= auto(),
    LOCAL_SERVICES= auto(),
    MULTI_CHANNEL= auto(),
    PERFORMANCE_MAX= auto(),
    SEARCH= auto(),
    SHOPPING= auto(),
    SMART= auto(),
    UNKNOWN= auto(),
    UNSPECIFIED= auto(),
    VIDEO= auto()

    @classmethod
    def value_of(cls, value):
        for k, v in cls.__members__.items():
            if k == value:
                return v
        else:
            raise ValueError(f"'{cls.__name__}' enum not found for '{value}'")

class PaymentMode(Enum):
    @classmethod
    def PaymentModeToEnum(cls, value):
        payments = {}

        payments.update({"CLICKS": lambda: client.get_type("PaymentModeEnum").PaymentMode.CLICKS})
        payments.update({"CONVERSIONS": lambda: client.get_type("PaymentModeEnum").PaymentMode.CONVERSIONS})
        payments.update({"CONVERSION_VALUE": lambda: client.get_type("PaymentModeEnum").PaymentMode.CONVERSION_VALUE})
        payments.update({"GUEST_STAY": lambda: client.get_type("PaymentModeEnum").PaymentMode.GUEST_STAY})

        if value in payments.keys():
            payments[value]()


if __name__ == '__main__':
    PaymentMode.PaymentModeToEnum('CLICKS')
    # sim = ChannelType.value_of('SEARCH')
    # print(sim)
    # print(ChannelType.SEARCH)
    # print(sim.name)
