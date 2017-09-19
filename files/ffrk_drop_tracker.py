import json
import time
import re

def response(flow):
    if len(re.findall('/get_battle_init_data', flow.request.path)) == 0:
        return

    data   = json.loads(flow.response.content.decode('utf-8-sig'))
    rounds = data['battle']['rounds']

    results = {
        'materias': [],
        'potions':  [],
        'drops':    {},
        'exp2X':    []
    }

    for round in rounds:
        for enemy_set in round['enemy']:
            for enemy in enemy_set['children']:
                for item in enemy['drop_item_list']:
                    item_id = item['item_id'] if ('item_id' in item) else '0'
                    amount  = item['num'] if ('num' in item) else item['amount']

                    if (item_id not in results['drops'].keys()):
                        results['drops'][item_id] = {
                            'type':   item['type'],
                            'amount': 0
                        }

                    results['drops'][item_id]['amount'] += int(amount)

        for potion in round['drop_item_list']:
            results['potions'].append({
                'type':  potion['type'],
                'round': potion['round']
            })

        for materia in round['drop_materias']:
            results['materias'].append(materia['name'])
            
    for charUID in data['battle']['buddy_boost_map']['exp']:
        if (data['battle']['buddy_boost_map']['exp'][charUID] == '200'):
            results['exp2X'].append(int(charUID))

    print('######################################')
    print(time.strftime("%Y-%m-%d %H:%M:%S"))
    print('-------------------\n')

    multi_segment = False

    if len(results['drops']):
        with open('ffrk_drop_tracker_db.csv') as f:
            lines    = f.read().splitlines()[1:]
            drop_ids = {x.split(',')[0]: x.split(',')[1] for x in lines}

        if (multi_segment):
            print('\n-------------------\n')

        multi_segment = True

        print('Drops:\n')

        for drop in sorted(results['drops']):
            if (drop in drop_ids.keys()):
                name = drop_ids[drop]

            elif (int(drop) in range(21000000, 24000000)):
                name = 'Relic {0}'.format(drop)

            else:
                name = 'Unknown {0} (type {1})'.format(drop, results['drops'][drop]['type'])

            amount = ': {0}'.format(results['drops'][drop]['amount'])

            print('{0}{1}'.format(name, amount))

    if len(results['potions']):
        potion_types = {
            '21': 'Blue Potion',
            '22': 'Green Potion',
            '23': 'Purple Potion',
            '31': 'Ether',
            '32': 'Orange Ether'
        }

        if (multi_segment):
            print('\n-------------------\n')

        multi_segment = True

        print('Potions:\n')

        for potion in results['potions']:
            print('Round {0}: {1}'.format(potion['round'], potion_types[potion['type']]))

    if len(results['materias']):
        if (multi_segment):
            print('\n-------------------\n')

        multi_segment = True

        print('Record Materias:\n')

        for materia in results['materias']:
            print(materia)
            
    if len(results['exp2X']):
        if (multi_segment):
            print('\n-------------------\n')

        multi_segment = True

        charNames = []

        for charData in data['battle']['buddy']:
            if charData['uid'] in results['exp2X']:
                charNames.append(charData['params'][0]['disp_name'])

        print('Double XP: ' + ', '.join(charNames))

    print('\n\n')