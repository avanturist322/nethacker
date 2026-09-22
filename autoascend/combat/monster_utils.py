from .utils import wielding_melee_weapon

# heuristic monster types lists
# hypothesis: fighting a cockatrice/chickatrice barehanded (not wielding a
# weapon) risks instant petrification on a successful hit, same as touching its
# corpse -- one of this bot's training deaths was exactly this ("petrified by a
# cockatrice corpse"). Wielding a weapon avoids that risk entirely, so unlike
# the other ONLY_RANGED_SLOW_MONSTERS (which should basically never be meleed),
# cockatrices only need to be added here to gate the *unarmed* case; see
# consider_melee_only_ranged_if_hp_full below, which allows melee whenever a
# weapon is wielded so an armed character keeps fighting them normally.
ONLY_RANGED_SLOW_MONSTERS = ['floating eye', 'blue jelly', 'brown mold', 'gas spore', 'acid blob',
                              'cockatrice', 'chickatrice']
EXPLODING_MONSTERS = ['yellow light', 'gas spore', 'flaming sphere', 'freezing sphere', 'shocking sphere']
INSECTS = ['giant ant', 'killer bee', 'soldier ant', 'fire ant', 'giant beetle', 'queen bee']
WEAK_MONSTERS = ['lichen', 'newt', 'shrieker', 'grid bug']
WEIRD_MONSTERS = ['leprechaun', 'nymph']


def is_monster_faster(agent, monster):
    _, y, x, mon, _ = monster
    # TOOD: implement properly
    return 'bat' in mon.mname or 'dog' in mon.mname or 'cat' in mon.mname \
           or 'kitten' in mon.mname or 'pony' in mon.mname or 'horse' in mon.mname \
           or 'bee' in mon.mname or 'fox' in mon.mname


def imminent_death_on_melee(agent, monster):
    if is_dangerous_monster(monster):
        return agent.blstats.hitpoints <= 16
    return agent.blstats.hitpoints <= 8


def is_dangerous_monster(monster):
    _, y, x, mon, _ = monster
    is_pet = 'dog' in mon.mname or 'cat' in mon.mname or 'kitten' in mon.mname or 'pony' in mon.mname \
             or 'horse' in mon.mname
    # 'mumak' in mon.mname or 'orc' in mon.mname or 'rothe' in mon.mname \
    # or 'were' in mon.mname or 'unicorn' in mon.mname or 'elf' in mon.mname or 'leocrotta' in mon.mname \
    # or 'mimic' in mon.mname
    return is_pet or mon.mname in INSECTS


def consider_melee_only_ranged_if_hp_full(agent, monster):
    if monster[3].mname in ('cockatrice', 'chickatrice'):
        # safe to melee while wielding a weapon: petrification only comes from
        # touching it with bare hands, not from a weapon strike
        return wielding_melee_weapon(agent)
    return monster[3].mname in ('brown mold', 'blue jelly') and agent.blstats.hitpoints == agent.blstats.max_hitpoints
