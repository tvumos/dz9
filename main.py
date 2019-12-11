import lib


def is_correct_count_players(choice):
    return choice.isdigit() and 2 <= int(choice) and int(choice) <= 5


def is_correct_type_players(choice):
    return choice.isdigit() and (0 == int(choice) or int(choice) == 1)

def is_correct_yes_no(choice):
    return choice == "y" or choice == "n"


players_list = []
response_count = input('Укажите количество игроков (от 2 до 5) -> ')
if is_correct_count_players(response_count):
    for i in range(int(response_count)):
        response_type = input(f'Игрок № {i + 1} является компьютером (1) или человеком (0). Введите 1 или 0 -> ')
        if is_correct_type_players(response_type):
            player = lib.Player()
            if response_type == '0':
                response_name = input(f'Введите имя игрока № {i + 1} -> ')
                player.create_game_card(f"{response_name}", False)  # Создаём игрока - человек
            else:
                player.create_game_card(f"Компьютер {i + 1}", True)     # Создаём игрока - компьютер
            players_list.append(player)
        else:
            print(f"Не корректный тип игрока. Вы проиграли. Игра завершается")
else:
    print(f"Не корректное количество игроков. Вы проиграли. Игра завершается")
    exit(0)

# Список игроков заполнен, начинаем игру
basket = lib.Basket()
count_in_basket = lib.COUNT_NUMB
print()
print("=" * 50)
print("Начинаем игру")
for i in range(lib.COUNT_NUMB):
    # Выбираем всех игроков у которых не осталось номеров в карточках
    winners = list([x for x in players_list if x.my_card.current_count_numbers == 0])
    if len(winners) > 0:    # Есть победитель
        for winner in winners:
            print(f"Есть победитель! Победил {winner.name}")
        print("Игра завершается.")
        exit(0)

    players = list([x for x in players_list if not x.lost])  # Выбираем всех не проигравших игроков
    if len(players) == 1:
        print(f"Игра завершается. Остался один игрок. Победил {players[0].name}")
        exit(0)

    temp_numb = basket.next()
    count_in_basket -= 1
    print(f"Новый бочонок: {temp_numb} (осталось {count_in_basket})")

    for temp_player in players:
        print("\n".join(temp_player.my_card.print_card()))

    for temp_player in players:
        if not temp_player.is_computer:     # Если игрок человек, то спаршиваем его
            response = input(f'Игрок {temp_player.name}, зачеркнуть цифру? (y / n) -> ')
            if not is_correct_yes_no(response):
                print("Не корректный ввод. Вы проиграли. Игра завершается. ")
                exit(0)
            is_exists = temp_player.check_number(temp_numb)
            if response == "y":     # Проверяем цифру в карточке
                if not is_exists:  # Пользователь ошибся, проверял, а значение в карточке отсутствует
                    print(f"Игрок {temp_player.name} проиграл и выбывает из игры. Значение {temp_numb} "
                          f"отсутствует в карточке")
                    temp_player.lost = True
                else:
                    temp_player.examination_number(temp_numb)  # Вычёркиваем
            else:
                if is_exists:  # Пользователь ошибся, не проверял, а значение в карточке присутствует
                    print(f"Игрок {temp_player.name} проиграл и выбывает из игры. Значение {temp_numb} "
                          f"присутствует в карточке")
                    temp_player.lost = True
        else:
            is_exists = temp_player.check_number(temp_numb)
            if is_exists:
                temp_player.examination_number(temp_numb)  # Вычёркиваем





