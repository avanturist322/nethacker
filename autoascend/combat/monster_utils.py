# heuristic monster types lists
ONLY_RANGED_SLOW_MONSTERS = ['floating eye', 'blue jelly', 'brown mold', 'gas spore', 'acid blob']
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
    # hypothesis: this list of genuinely hard-hitting early monsters was present but disabled, so
    # is_dangerous_monster() only ever flagged pets/insects. That meant the retreat threshold in
    # imminent_death_on_melee() (hp<=16 for "dangerous" monsters vs hp<=8 otherwise) and the extra
    # caution added in elbereth_action()/get_potential_wand_usages() never kicked in for monsters
    # like mumaks, rothes, orcs, weres, elves, leocrottas and mimics -- exactly the monster types
    # this bot's training runs were dying to (e.g. "killed by a mumak", "killed by a rothe"). Turning
    # this list back on should make the bot retreat/engrave/use wands earlier against these threats
    # instead of melee-ing them down to death like a trivial monster.
    is_dangerous = 'mumak' in mon.mname or 'orc' in mon.mname or 'rothe' in mon.mname \
        or 'were' in mon.mname or 'unicorn' in mon.mname or 'elf' in mon.mname or 'leocrotta' in mon.mname \
        or 'mimic' in mon.mname
    return is_pet or is_dangerous or mon.mname in INSECTS


def consider_melee_only_ranged_if_hp_full(agent, monster):
    return monster[3].mname in ('brown mold', 'blue jelly') and agent.blstats.hitpoints == agent.blstats.max_hitpoints
