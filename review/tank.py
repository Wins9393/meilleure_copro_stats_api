class Tank:
    def __init__(self, armor, penetration, armor_type):
        self.armor = armor
        self.penetration = penetration
        self.armor_type = armor_type
        if not (armor_type == 'chobham' or armor_type == 'composite' or armor_type == 'ceramic'):
            raise Exception('Invalid armor type %s' % (armor_type))
        self.tank = "Tank"

    def set_name(self, name):
        self.name = name

    def vulnerable(self, tank):
        real_armor = self.armor
        if self.armor_type == 'chobham':
            real_armor += 100
        elif self.armor_type == 'composite':
            real_armor += 50
        elif self.armor_type == 'ceramic':
            real_armor += 50
        if real_armor <= tank.penetration: return True
        return False

    def swap_armor(self, othertank):
        tmp = othertank.armor
        othertank.armor = self.armor
        self.armor = tmp
        return othertank

    def __repr__(self):
        tmp = self.name.lower()
        tmp = self.name.replace(' ', '-')
        return tmp

m1_1 = Tank(600, 670, 'chobham')
m1_2 = Tank(620, 670, 'chobham')

if m1_1.vulnerable(m1_2) is True:
    print('Vulnerable to self')

m1_1.swap_armor(m1_2)

tanks = []
test = []

for i in range(5):
    """
    Le armor_type "steel" n'est pas un type défini et lève donc une Exception
    """
    # tanks.append(Tank(400, 400, 'steel'))
    tanks.append(Tank(400, 400, 'composite'))


"""
Utilisation de enumerate au lieu d'un index déclaré et incrémenté à la main
"""    
for index, tank in enumerate(tanks):
    tank.set_name('Tank' + str(index) + "_Small")
    test.append(tank.vulnerable(m1_1))

print(tanks)

"""
Suppression de la boucle while inutile ici.
La boucle for parcourt déjà toutes les occurences du tableau tanks.
Ajout du test de vulnérabilité dans la boucle for.
"""
# while index < len(tanks):
#     test.append(tanks[i].vulnerable(m1_1))

def test_tank_safe(shooter, test_vehicles=[]):
    at_least_one_safe = False
    for t in test:
        if t:
            at_least_one_safe = True
    if at_least_one_safe:
        print("A tank is safe")
    else:
        print("No tank is safe")

test_tank_safe(m1_1, tanks)