# coding=utf-8

import json

def response(flow):
    cases = {
        '/dff/party/list': 'inventory_main',
        '/dff/warehouse/get_equipment_list': 'vault_relic',
        '/dff/warehouse/get_record_materia_list': 'vault_rm'
    }

    if (flow.request.path not in cases.keys()):
        return

    data = json.loads(flow.response.content[3:].decode('utf8'))

    if (cases[flow.request.path] == 'inventory_main'):
        getRelics(data['equipments'], 'ffrk_inventory_relics')
        getAbilities(data['abilities'], 'ffrk_inventory_abilities')
        getOrbs(data['materials'], 'ffrk_inventory_orbs')
        getRMs(data['record_materias'], 'ffrk_inventory_rm')
        getSBs(data['soul_strikes'], 'ffrk_inventory_sb')

    elif (cases[flow.request.path] == 'vault_relic'):
        getRelics(data['equipments'], 'ffrk_vault_relics')

    elif (cases[flow.request.path] == 'vault_rm'):
        getRMs(data['record_materias'], 'ffrk_vault_rm')


def getRelics(data, filename):
    types = {
        1: 'Weapon',
        2: 'Armor',
        3: 'Accessory'
    }

    elems = []

    for elem in data:
        id       = elem['equipment_id']
        name     = elem['name'].replace(u'＋', '+')
        category = elem['category_name']
        type     = types[elem['equipment_type']]
        rarity   = elem['rarity']
        realm_id = int(str(elem['series_id'])[1:3]) if elem['series_id'] > 10 else 99

        elems.append([id, name, category, type, rarity, realm_id])

    elems = sorted(elems, key = lambda x: (-x[4], x[5], x[1]))

    with open('{}.csv'.format(filename), 'w') as f:
        f.write('ID, Item, Category, Type, Rarity, Synergy\n')

        for elem in elems:
            f.write('{}, {}, {}, {}, {}, {}\n'.format(elem[0], elem[1], elem[2], elem[3], elem[4], elem[5]))


def getRMs(data, filename):
    elems = []

    for elem in data:
        id   = elem['record_materia_id']
        name = elem['name']

        elems.append([id, name])

    elems = sorted(elems, key=lambda x: (x[1]))

    with open('{}.csv'.format(filename), 'w') as f:
        f.write('ID, RM\n')

        for elem in elems:
            f.write('{}, {}\n'.format(elem[0], elem[1]))


def getAbilities(data, filename):
    elems = []

    for elem in data:
        id       = elem['ability_id']
        name     = elem['name']
        category = elem['category_name']
        rarity   = elem['rarity']
        rank     = elem['grade']

        elems.append([id, name, category, rarity, rank])

    elems = sorted(elems, key=lambda x: (-x[3], x[2], x[1]))

    with open('{}.csv'.format(filename), 'w') as f:
        f.write('ID, Ability, Category, Rarity, Rank\n')

        for elem in elems:
            f.write('{}, {}, {}, {}, {}\n'.format(elem[0], elem[1], elem[2], elem[3], elem[4]))


def getOrbs(data, filename):
    elems = []

    for elem in data:
        id       = elem['id']
        name     = elem['name']
        rarity   = elem['rarity']
        amount   = elem['num']

        if (id <= 40000078 and amount > 0):
            elems.append([id, name, rarity, amount])

    elems = sorted(elems, key=lambda x: (-x[2], x[0]))

    with open('{}.csv'.format(filename), 'w') as f:
        f.write('ID, Orb, Rarity, Amount\n')

        for elem in elems:
            f.write('{}, {}, {}, {}\n'.format(elem[0], elem[1], elem[2], elem[3]))

def getSBs(data, filename):
    elems = []

    for elem in data:
        id         = elem['id']
        name       = elem['name']
        charId     = elem['allowed_buddy_id']
        char       = elem['allowed_buddy_name'] if 'allowed_buddy_name' in elem.keys() else None
        categoryId = elem['soul_strike_category_id']
        category   = elem['soul_strike_category_name'].title()

        if (categoryId >= 3) and (charId >= 10100000 or charId == 10000200):
            elems.append([id, name, charId, char, categoryId, category])

    elems = sorted(elems, key=lambda x: (x[2], x[4], x[0]))

    with open('{}.csv'.format(filename), 'w') as f:
        f.write('ID, Soul Break, Character ID, Character, Type ID, Type\n')

        for elem in elems:
            f.write('{}, {}, {}, {}, {}, {}\n'.format(elem[0], elem[1], elem[2], elem[3], elem[4], elem[5]))