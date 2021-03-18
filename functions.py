from random import choice, random
from texts_of_the_story import instruction, BEGIN_OF_THE_STORY, END_OF_THE_STORY
import numpy


def welcome_player():
    player_name = input('Введите имя игрока: ')
    print(
        'Добро пожаловать в игру "Охота на Вампуса"! Чтобы начать игру, введите "Начать". '
        'Чтобы прочитать инструкцию, введите "Правила". Приятного время препровождения!'
    )
    answer = input('> ')
    if 'начать' in answer.lower():
        game(player_name)
    elif 'правила' in answer.lower():
        instruction()
    else:
        count = 0
        wrong_answer = True
        while wrong_answer == True:
            print('Попробуйте ввести команду еще раз')
            answer = input('> ')
            if answer.lower() == 'начать':
                game(player_name)
                wrong_answer = False
            elif answer.lower() == 'правила':
                instruction()
                wrong_answer = False
            else:
                count += 1
                # print(count)
            if count > 5:
                wrong_answer = False
                return print('Возвращайся, когда перестанешь хулиганить =)')
    return game(player_name)


def create_caves():
    all_caves = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
    caves = []
    # Генерация комнат в пещере
    for cave_number in all_caves:
        cave = []
        while len(cave) != 3:
            passage_to = choice(all_caves)
            all_caves.remove(passage_to)
            cave.append(passage_to)
        caves.append(cave)
        if len(all_caves) == 3:
            caves.append(all_caves)
    return caves


def create_locations(caves):
    result = choice(caves[numpy.random.randint(0, 6)])
    return result


def create_player_location(caves):
    result = choice(caves)
    return result


def create_wumpus_awakening(caves, super_bat_1, super_bat_2, deep_pit, player_location, player_name,
                            answer, arrows, add_arrows):
    wumpus_location = choice(caves[numpy.random.randint(0, 6)])
    print('Судя по рычанию, Вампус проснулся и перешел в другую комнату. Нужно быть осторожнее.')
    if wumpus_location == answer:
        print('О нет! Вампус нашел вас!')
        return new_game(player_name)
    print('Нужно двигаться дальше.')
    # print('wumpus_location', wumpus_location)
    return question(caves, wumpus_location, super_bat_1, super_bat_2, deep_pit,
                    player_location, player_name, arrows, add_arrows)


def game(player_name):
    begin = True
    caves = create_caves()
    arrows = 5
    add_arrows = create_locations(caves)
    super_bat_1 = create_locations(caves)
    super_bat_2 = create_locations(caves)
    deep_pit = create_locations(caves)
    player_location = create_player_location(caves)
    wumpus_location = create_locations(caves)

    while add_arrows == super_bat_1 or add_arrows == super_bat_2 or add_arrows == deep_pit \
            or add_arrows == player_location or add_arrows == wumpus_location:
        add_arrows = create_locations(caves)

    while super_bat_1 == super_bat_2 or super_bat_1 == deep_pit or super_bat_1 == player_location \
            or super_bat_1 == wumpus_location or super_bat_1 == add_arrows:
        super_bat_1 = create_locations(caves)

    while super_bat_2 == add_arrows or super_bat_2 == super_bat_1 or super_bat_2 == deep_pit \
            or super_bat_2 == player_location or super_bat_2 == wumpus_location:
        super_bat_2 = create_locations(caves)

    while deep_pit == add_arrows or deep_pit == super_bat_1 or deep_pit == super_bat_2 \
            or deep_pit == wumpus_location or deep_pit == player_location:
        deep_pit = create_locations(caves)

    while player_location == add_arrows or player_location == super_bat_1 \
            or player_location == super_bat_2 or player_location == wumpus_location or player_location == deep_pit:
        player_location = create_locations(caves)

    # print('caves', caves)
    # print('player_location', player_location)
    # print('super_bat1', super_bat_1)
    # print('super_bat2', super_bat_2)
    # print('deep_pit', deep_pit)
    # print('add_arrows', add_arrows)
    # print('wumpus_location', wumpus_location)

    if begin:
        print(
            f'{choice(BEGIN_OF_THE_STORY)}\nВы оказались в глубокой пещере. '
            f'{player_name.capitalize()}, хорошо, что все комнаты освещены. У Вас {arrows} стрел')
        begin = False

    question(caves, wumpus_location, super_bat_1, super_bat_2, deep_pit, player_location, player_name, arrows,
             add_arrows)


def death(player_name):
    print(f'{player_name}, Вы ввели недопустимую команду. Наказание - смерть.')
    new_game(player_name)


def new_game(player_name):
    print('Желаете попробовать еще раз?')
    answer = input('> ')
    if 'да' in answer.lower():
        game(player_name)
    return print('До новых встреч')


def end_of_the_game():
    print(f'{choice(END_OF_THE_STORY)}')


def question(caves, wumpus_location, super_bat_1, super_bat_2, deep_pit, player_location, player_name, arrows,
             add_arrows):
    print(f'Вы находитесь в комнате с тремя дверьми {player_location}')

    if wumpus_location in player_location:
        print('Как же неприятно пахнет! Думаю, Вампус совсем близко')
    elif super_bat_1 in player_location or super_bat_2 in player_location:
        print('Слышется шелест крыльев. Поблизости летучие мыши.')
    print('Какую из них открыть?')
    try:
        answer = int(input('> '))
    except:
        print('Неверная команда. Попробуйте еще раз.')
        question(caves, wumpus_location, super_bat_1, super_bat_2, deep_pit, player_location, player_name, arrows,
                 add_arrows)
    flag = False

    try:
        # Проверка на правильность выбора следующей комнаты
        while flag == False:
            if not int(answer) in player_location:
                print(f'Вы можете выбрать только одну из {player_location} комнат')
                answer = int(input('> '))
            else:
                flag = True
    except:
        death(player_name)

    # Выбор действий
    print(
        'Выберите действие для продолжения: а) выстрелить в выбранную комнату; '
        'б) войти в выбранную комнату; в) выбрать другую комнату; г) остаться на месте')
    choice = input('> ')
    # print('choice', choice)
    if choice.lower() == 'а':
        if arrows > 0:
            answer = int(answer)
            return shoot(caves, wumpus_location, super_bat_1, super_bat_2, deep_pit, player_location, player_name,
                         answer, arrows, add_arrows)
        print('У вас больше нет стрел. Попробуйте поискать их в одной из комнат.')
        return question(caves, wumpus_location, super_bat_1, super_bat_2, deep_pit, player_location, player_name,
                        arrows, add_arrows)
    elif choice.lower() == 'б':
        return cave_location(caves, wumpus_location, super_bat_1, super_bat_2, deep_pit, player_name,
                             answer, arrows, add_arrows)
    elif choice.lower() == 'в':
        return question(caves, wumpus_location, super_bat_1, super_bat_2, deep_pit, player_location, player_name,
                        arrows, add_arrows)
    elif choice.lower() == 'г':
        print('Вы погибли от голода и холода. Нужно было больше двигаться :(')
        return new_game(player_name)
    return death(player_name)


def cave_location(caves, wumpus_location, super_bat_1, super_bat_2, deep_pit, player_name, location,
                  arrows, add_arrows):
    if location == wumpus_location:
        print(
            'О нет!! Вы оказались в комнате Вампуса. Его не обойти, а дверь позади предательски захлопнулась. Вам некуда бежать. Остается только смириться с тем, что Вы стали обедом.')
        return new_game(player_name)

    elif location == add_arrows:
        arrows += numpy.random.randint(0, 5)
        print(f'Вам крупно повезло! Вы нашли стрелы! Теперь у вас {arrows} стрел\n')

    elif location == deep_pit:
        print('За этой дверью оказалась глубока яма. Мне очень жаль, но Вы не выжили после падения :('
              )
        return new_game(player_name)

    elif location == super_bat_1 or location == super_bat_2:
        print(
            'Внезапно Вы почувствовали, что словно отрываетесь от земли! '
            'Это питомец Вампуса уносит вас подальше от своего уютного гнездышка. Держитесь крепче!'
        )
        if arrows < 1:
            print('У вас нет стрел. Вы ничего не потеряете.')
        print('Нажмите любую клавишу, чтобы бросить кубик')

        input('> ')
        cube = numpy.random.randint(1, 6)
        print(f'Выпало число {cube}.')
        if cube < 5:
            if arrows > 1:
                if arrows > cube:
                    arrows -= cube
                    print(f'Вы потеряли стрелы. Осталось всего {arrows}.')
            else:
                arrows = 0
        else:
            if arrows != 0:
                print('Вам повезло! Все стрелы на месте.')
            print('Вам нечего терять, так как у вас закончились стрелы :(.')

    player_location = create_player_location(caves)
    return question(caves, wumpus_location, super_bat_1, super_bat_2, deep_pit, player_location, player_name, arrows,
                    add_arrows)


def shoot(caves, wumpus_location, super_bat_1, super_bat_2, deep_pit, player_location, player_name, answer, arrows,
          add_arrows):
    if arrows:
        arrows -= 1
        print(f'Вы достаете стрелу. В колчане осталось всего {arrows}.')
        if answer == wumpus_location:
            print(
                'Вы попали В Вампуса!! Вижу, он испустил последний вздох. Надеюсь, '
                'он не мучился. Пора искать выход отсюда'
            )
            return end_of_the_game()
        else:
            print('Я слышу только свист от пролетающей стрелы. Будем молиться, чтобы Крампус не проснулся')
            if arrows < 1:
                print('У Вас больше нет стрел. Нужно найти хотя бы одну, иначе будем бессмысленно бродить тут.')
                return question(caves, wumpus_location, super_bat_1, super_bat_2, deep_pit, player_location,
                                player_name, arrows, add_arrows)
            return wumpus_activity(caves, wumpus_location, super_bat_1, super_bat_2, deep_pit, player_location,
                                   player_name, answer, arrows, add_arrows)


def wumpus_activity(caves, wumpus_location, super_bat_1, super_bat_2, deep_pit, player_location, player_name, answer,
                    arrows, add_arrows):
    wumpus_awakening = random()
    if round(wumpus_awakening, 2) > 0.25:
        return create_wumpus_awakening(caves, super_bat_1, super_bat_2, deep_pit, player_location,
                                       player_name, answer, arrows, add_arrows)
    return question(caves, wumpus_location, super_bat_1, super_bat_2, deep_pit, player_location, player_name, arrows,
                    add_arrows)
