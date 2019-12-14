from enum import Enum


class BattalionType(Enum):
    HORSES = "horses"
    ELEPHANTS = "elephants"
    ARMOUREDTANKS = "armoured_tanks"
    SLINGGUNS = "sling_guns"

    @staticmethod
    def is_valid_battalion(battalion_name: str) -> bool:
        btn_names = [bat.value for bat in BattalionType]
        return battalion_name in btn_names
