import os
from typing import Dict

from flask import Flask, request, jsonify, render_template, redirect, url_for

from arena import Arena
from classes import unit_classes
from equipment import Equipment
from unit import Person

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
IS_WINDOWS = os.name != 'posix'

heroes: Dict[str, Person] = {}
equip = Equipment()
arena = Arena()


@app.route('/')
def hello_page():
    return render_template('index.html')


@app.route('/choose-hero/', methods=["GET", "POST"])
def choose_hero_page():
    if request.method == "GET":
        result = {
            "header": 'Choose hero',
            "classes": unit_classes,
            "weapons": equip.get_weapon_names(),
            "armors": equip.get_armor_names(),
            "action": '/choose-hero/'
        }
        return render_template('hero_choosing.html', result=result)
    if request.method == "POST":
        arena.player = Person(name=request.form['name'],
                              unit_class=unit_classes[request.form['unit_class']],
                              health=unit_classes[request.form['unit_class']].max_health,
                              stamina=unit_classes[request.form['unit_class']].max_stamina,
                              weapon=Equipment().get_weapon(request.form['weapon']),
                              armor=Equipment().get_armor(request.form['armor'])
                              )
        return redirect(url_for('choose_enemy_page'), code=302)


@app.route('/choose-enemy/', methods=["GET", "POST"])
def choose_enemy_page():
    if request.method == "GET":
        result = {
            "header": 'Choose enemy',
            "classes": unit_classes,
            "weapons": equip.get_weapon_names(),
            "armors": equip.get_armor_names(),
            "action": '/choose-enemy/'
        }
        return render_template('hero_choosing.html', result=result)
    if request.method == "POST":
        arena.enemy = Person(name=request.form['name'],
                             unit_class=unit_classes[request.form['unit_class']],
                             health=unit_classes[request.form['unit_class']].max_health,
                             stamina=unit_classes[request.form['unit_class']].max_stamina,
                             weapon=Equipment().get_weapon(request.form['weapon']),
                             armor=Equipment().get_armor(request.form['armor'])
                             )
        heroes.update({"player": arena.player, "enemy": arena.enemy})
        arena.game_running = True
        return redirect(url_for('fight'), code=302)


# arena.player = Person(name='Vlad',
#                       unit_class=unit_classes['Warrior'],
#                       health=unit_classes['Warrior'].max_health,
#                       stamina=unit_classes['Warrior'].max_stamina,
#                       weapon=Equipment().get_weapon('ножик'),
#                       armor=Equipment().get_armor('футболка')
#                       )
# arena.enemy = Person(name='thief',
#                      unit_class=unit_classes['Thief'],
#                      health=unit_classes['Thief'].max_health,
#                      stamina=unit_classes['Thief'].max_stamina,
#                      weapon=Equipment().get_weapon('ножик'),
#                      armor=Equipment().get_armor('кожаная броня')
#                      )
# heroes: Dict[str, Person] = {"player": arena.player, "enemy": arena.enemy}
# arena.game_running = True


@app.route('/fight/')
def fight():
    return render_template('fight.html', heroes=heroes, result='Бой начался!')

@app.route('/fight/hit/')
def fight_hit():
    arena.battle_result = arena.hero_hit()
    return render_template('fight.html', heroes=heroes, battle_result=arena.battle_result)


@app.route('/fight/use-skill/')
def fight_use_skill():
    arena.battle_result = arena.hero_use_skill()
    return render_template('fight.html', heroes=heroes, battle_result=arena.battle_result)


@app.route('/fight/pass-turn/')
def fight_pass_turn():
    arena.battle_result = arena.hero_skip_move()
    return render_template('fight.html', heroes=heroes, battle_result=arena.battle_result)


@app.route('/fight/end-fight/')
def fight_end_fight():
    arena.game_running = False
    return render_template('fight.html', heroes=heroes, battle_result=arena.battle_result)
