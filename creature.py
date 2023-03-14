import os
from random import randint, sample
import logging
from mongoengine import *
from filler_creatures import creatures, abilities

logging.basicConfig(level=logging.DEBUG)


class Ability(Document):
    name = StringField(required=True, unique=True)
    effect_stat = IntField()
    effect_status = StringField()

    description = StringField()

    meta = {'strict': False}


class Creature(Document):
    name = StringField(required=True, unique=True)
    image = StringField()

    hp = IntField(default=50, required=True)
    attack = IntField(required=True)
    defense = IntField(required=True)
    speed = IntField(required=True)
    ability = ReferenceField(Ability)
    description = StringField()
    lore = StringField()

    meta = {'strict': False}

    def __repr__(self):
        ability_name = self.ability.name if self.ability else "No Ability yet"
        return f"<Creature {self.name} - Atk {self.attack}: {ability_name}>"


if os.getenv("USE_LOCAL"):
    connect("Creatures")
    logging.debug("Running on local database.")
else:
    connect(host=os.getenv("CREATURE_DEN_DATABASE_URL"))
    logging.debug("Running on the cloud.")

Creature.drop_collection()
Ability.drop_collection()

# Your code goes here
a = Ability(name="Best Ability")
c = Creature(name="Pepe", hp=50, image="11", description="A thing.",
             attack=10, defense=10, speed=1)

a.save()
c.ability = a
c.save()

a = Ability(name="Second Best Ability, but still good")
c = Creature(name="Bill", hp=50, image="35", description="Another thing.",
             attack=10, defense=10, speed=1)

a.save()
c.ability = a
c.save()

# Generating filler creatures

# find already used images
pics_already_used = Creature.objects().distinct("image")

all_pics = [str(n) for n in range(1, 829)]

unused_pics = list(set(all_pics).difference(pics_already_used))

for each_filler_creature, each_ability in zip(creatures, abilities):
    creature_name = each_filler_creature
    ability_name = each_ability

    creature_description = creatures[creature_name]["description"]
    creature_lore = creatures[creature_name]["lore"]
    ability_description = abilities[ability_name]

    hp = randint(1, 100)
    attack = randint(1, 100)
    defense = randint(1, 100)
    speed = randint(1, 100)
    image = sample(unused_pics, 1)[0]

    c = Creature(name=creature_name, description=creature_description,
                 hp=hp, attack=attack, defense=defense, speed=speed,
                 lore=creature_lore, image=image)
    a = Ability(name=ability_name, description=ability_description)

    a.save()
    c.ability = a
    c.save()

    pass

pass
