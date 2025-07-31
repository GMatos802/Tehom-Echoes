from .base_player import Player
from settings import *
from powers.skills.light_skills import HolySpear, LuminousPulse
from powers.skills.fury_skills import Slash, RushHitbox
from powers.skills.soul_skills import SpectralScythe, SoulBurst, SoulShard

class Caim(Player):
    def __init__(self, game, kit_class):
        super().__init__(game, kit_class)

    def get_damage_multiplier(self):
        """Sobrescreve o método base para a passiva 'No Fio da Navalha'."""
        health_ratio = self.health / self.max_health

        if health_ratio < CAIM_LOW_HEALTH_THRESHOLD:
            bonus_progress = 1 - (health_ratio / CAIM_LOW_HEALTH_THRESHOLD)
            return 1.0 + (CAIM_MAX_DAMAGE_BONUS * bonus_progress)

        return 1.0
    
    def use_skill_1(self, group):
        if hasattr(self.kit, 'activate_skill_1'):
            was_used = self.kit.activate_skill_1(group)
            if was_used:
                self.health -= CAIM_ABILITY_HEALTH_COST 
    
    def use_skill_2(self, group):
        if hasattr(self.kit, 'activate_skill_2'):
            was_used = self.kit.activate_skill_2(group)
            if was_used:
                self.health -= CAIM_ABILITY_HEALTH_COST

    def on_ability_hit(self, hitbox):

        if isinstance(hitbox, (HolySpear, Slash, SoulBurst, SoulShard)): 
            if hasattr(self.kit, 'reduce_cooldowns'):
                self.kit.reduce_cooldowns(skill_number=2)

        elif isinstance(hitbox, (LuminousPulse, RushHitbox, SpectralScythe)): 
            if hasattr(self.kit, 'reduce_cooldowns'):
                self.kit.reduce_cooldowns(skill_number=1)