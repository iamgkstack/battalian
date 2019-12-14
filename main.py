from army import Army
from battalion_processor import BattalionProcessor
from battalion_types import BattalionType
from battle_planner import BattlePlanner
from copy import deepcopy


def main():
    battalion_processor = BattalionProcessor(2,horses=1, elephants=2, armoured_tanks=3, sling_guns=4);
    battalion_processor.add_battalion_substituation(BattalionType.ELEPHANTS, BattalionType.HORSES, 2);
    battalion_processor.add_battalion_substituation(BattalionType.ARMOUREDTANKS, BattalionType.ELEPHANTS, 2);
    battalion_processor.add_battalion_substituation(BattalionType.SLINGGUNS, BattalionType.ARMOUREDTANKS, 2)                                          
    lengaburu_army = Army(horses=100, elephants=50, armoured_tanks=10, sling_guns=5);

    
    with open("input.txt", "r") as testcases:
        for testcase in testcases:
            input = [int(x.strip()) for x in testcase.split(",")];
            enemy_army = Army(horses=input[0], elephants=input[1], armoured_tanks=input[2], sling_guns=input[3]);
            planner = BattlePlanner(battalion_processor, deepcopy(lengaburu_army));
            result, army = planner.get_winning_army(enemy_army);
            display_result(input, result, army);
    
def display_result(input, result, army):
    print("Input : Falicornia attacks with {0} H, {1} E, {2} AT, {3} SG ".format(input[0], input[1], input[2], input[3]))
    print("Output : Lebangaru deploys")
    for k, v in army.items():
        print("{0} : {1}".format(k.name, v))
    print("Lebangaru {0}".format("Wins" if result is True else "Loses"))
    print()
    
if __name__ == "__main__":
    main()