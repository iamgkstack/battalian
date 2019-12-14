from __future__ import division
from battalion_processor import BattalionProcessor
from battalion_types import BattalionType
from army import Army
from math import ceil


class BattlePlanner:
    
    def __init__(self, battalion_processor: BattalionProcessor, our_army: Army):
        self.battalion_processor: BattalionProcessor = battalion_processor
        self.our_army: Army = our_army
        self.__result_army: Army = Army()
    
    def update_battalion_stats(self, our_battalion: BattalionType, our_strength: int, enemy_battalion: BattalionType, enemy_strength: int, resolvable: int) -> int:
        enemy_strength -= resolvable
        self.our_army.update_battalion_strength(our_battalion, -our_strength)
        self.__result_army.update_battalion_strength(our_battalion, our_strength)
        return enemy_strength

    def resolve_battalion(self, enemy_battalion: BattalionType, enemy_strength: int) -> bool:
        
        remaining_strength: int = self.apply_power_rule(enemy_strength)
        if self.our_army.has_battalion(enemy_battalion): remaining_strength = self.resolve_with_similar_battalion(enemy_battalion, remaining_strength)
        
        if remaining_strength > 0: remaining_strength = self.resolve_with_substitution_battalion(enemy_battalion, remaining_strength)
        return remaining_strength == 0

    def resolve_with_similar_battalion(self, enemy_battalion: BattalionType, enemy_strength: int) -> int:
        our_strength = self.our_army.get_battalion_strength(enemy_battalion)
        resolvable_strength = min(our_strength, enemy_strength)
        resolved_strength = self.update_battalion_stats(enemy_battalion, resolvable_strength, enemy_battalion, enemy_strength, resolvable_strength) 
        return resolved_strength

    def apply_power_rule(self, enemy_strength: int) -> int:
        return int(ceil(enemy_strength / self.battalion_processor.multiplier))

    def resolve_with_substitution_battalion(self, enemy_battalion: BattalionType, enemy_strength: int) -> int:
        substitution_battalions = self.battalion_processor.get_substitution_battalion(enemy_battalion)
        for substitution_battalion in substitution_battalions:
            if enemy_strength == 0:
                break
            required_strength = ceil(substitution_battalion[1] * enemy_strength)
            actual_strength = self.our_army.get_battalion_strength(substitution_battalion[0])

            resolvable_strength = min(required_strength, actual_strength)
            normalized_resolvable = min(int(ceil(resolvable_strength *(1 / substitution_battalion[1]))),enemy_strength)
            enemy_strength = self.update_battalion_stats(substitution_battalion[0], resolvable_strength, enemy_battalion, enemy_strength, normalized_resolvable)
            
        return enemy_strength

    def get_winning_army(self, enemy_army: Army):
        
        battle_result: bool = True
        for enemy_battalion in enemy_army.get_battalions():
            enemy_strength = enemy_army.get_battalion_strength(enemy_battalion)
            battle_result &= self.resolve_battalion(enemy_battalion, enemy_strength)
        required_battalions = self.__result_army.get_all_battalion_with_strength()
        return battle_result, required_battalions
    