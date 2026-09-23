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
    # hypothesis: many training deaths are to nominally "trivial" monsters (kobolds,
    # kittens, geckos, giant rats, giant bats, foxes) that never trip the retreat/avoid
    # logic because it only kicks in for the small is_dangerous_monster() list, or once
    # HP is already critically low (<=8). A single unlucky hit at hp=9..12 can then kill
    # outright. Raising the generic (non-"dangerous") retreat threshold from 8 to 12 gives
    # a bit more buffer against any monster's bad damage roll, not just the flagged ones.
    if is_dangerous_monster(monster):
        return agent.blstats.hitpoints <= 16
    return agent.blstats.hitpoints <= 12


def is_dangerous_monster(monster):
    _, y, x, mon, _ = monster
    is_pet = 'dog' in mon.mname or 'cat' in mon.mname or 'kitten' in mon.mname or 'pony' in mon.mname \
             or 'horse' in mon.mname
    # 'mumak' in mon.mname or 'orc' in mon.mname or 'rothe' in mon.mname \
    # or 'were' in mon.mname or 'unicorn' in mon.mname or 'elf' in mon.mname or 'leocrotta' in mon.mname \
    # or 'mimic' in mon.mname
    # hypothesis: an angered shopkeeper is a well-known outlier threat in early NetHack --
    # far harder-hitting than its dungeon level suggests, and (unlike most monsters)
    # unaffected by Elbereth -- but it wasn't flagged dangerous, so it only ever got the
    # generic hp<=12 retreat threshold like a kobold (recorded training death: "killed by
    # ... the shopkeeper" at Xp:10). A wider list of "merely tough" monsters (orcs/rothes/
    # elves/unicorns) was tried and made things worse, likely because they're common enough
    # that constant retreating from them wastes too much time; shopkeepers are rare enough
    # that giving them the higher hp<=16 buffer shouldn't have that same cost.
    is_shopkeeper = 'shopkeeper' in mon.mname
    return is_pet or is_shopkeeper or mon.mname in INSECTS


def consider_melee_only_ranged_if_hp_full(agent, monster):
    return monster[3].mname in ('brown mold', 'blue jelly') and agent.blstats.hitpoints == agent.blstats.max_hitpoints
