import random

COUNT_NUMB = 90

class NumbSequence:

    def __init__(self):
        """
        Инициализация корзины
        """
        self.list_numbers = []

    def create(self, size):
        """
        Создание корзины, заполнение корзины цифрами от 1 до size + 1
        :param size: Размер корзины с номерами лото
        """
        self.list_numbers = list(range(1, size + 1))

    def next(self):
        """
        Метод возвращает следующее число из корзины. Данное число удаляется из корзины
        :return: Возвращает случайное число из корзины.
        """
        next_numb = -1
        if len(self.list_numbers) >= 1:
            next_numb = self.list_numbers[random.randint(1, len(self.list_numbers)) - 1]
            self.list_numbers.remove(next_numb)
        return next_numb


class Basket(NumbSequence):

    def __init__(self):
        """
        Инициализация корзины
        """
        super().__init__()
        self.create(COUNT_NUMB)     # Размер корзины = 90 бочёнков
        self.in_basket = COUNT_NUMB

    def next(self):
        self.in_basket -= 1
        return super(Basket, self).next()



def insert_numb_in_list(list, insert_numb):
    list_digit = [int(x) if x != '  ' else 0 for x in list]
    yes_insert = False
    inserted_numb = False
    for i, numb in enumerate(list_digit):
        if numb < insert_numb and insert_numb - numb <= 10:
            yes_insert = True
        if yes_insert and numb == 0:    # Можно вставлять число
            list[i] = '{:>2}'.format(insert_numb)
            inserted_numb = True
            break

    if not inserted_numb:
        yes_insert = False
        list_reverse = reversed(list_digit)
        for i, numb in enumerate(list_reverse):  # Идем в обратную сторону
            if numb < insert_numb and insert_numb - numb <= 10:
                yes_insert = True
            if yes_insert and numb == 0:  # Можно вставлять число
                list[8 - i] = '{:>2}'.format(insert_numb)
                inserted_numb = True
                break
    return list


class LottoCard:

    def __init__(self):
        """
        Инициализация игровой карточки лото
        В каждой карточке есть свойство - Имя игрока
        В каждой строке - 5 цифр на 9 полей
        В каждой карточке 3 строки
        """
        self.player_name = ""
        self.current_count_numbers = 15
        self.card = [['  '] * 9 for i in range(3)]
        self.list_count = []
        self.card_list = []
        self.add_list = []

    def create_card(self, name, size):
        self.player_name = name
        card_set = set()
        while len(card_set) < 15:
            card_set.add(random.randint(1, size))
        self.card_list = list(card_set)
        self.card_list.sort()
        #self.card_list = [8, 11, 12, 15, 16, 33, 54, 57, 68, 70, 80, 83, 86, 88, 90]

        self.list_count = []
        for i in range(9):
            self.list_count.append(len(list([x for x in self.card_list if i * 10 < x <= 10 + i * 10])))

        for i, count in enumerate(self.list_count):
            if count == 3:
                for j, numb in enumerate(list([x for x in self.card_list if i * 10 < x <= 10 + i * 10])):
                    self.card[j][i] = '{:>2}'.format(numb)
            elif 0 < count < 3:
                seq = NumbSequence()
                seq.create(3)
                for j, numb in enumerate(list([x for x in self.card_list if i * 10 < x <= 10 + i * 10])):
                    row = seq.next()
                    while len(list([x for x in self.card[row - 1] if x != '  '])) >= 5:
                        row = seq.next()
                    self.card[row - 1][i] = '{:>2}'.format(numb)
            elif count > 3:
                seq = NumbSequence()
                seq.create(3)
                for j, numb in enumerate(list([x for x in self.card_list if i * 10 < x <= 10 + i * 10])):
                    row = seq.next()
                    if j <= 2:
                        self.card[j][i] = '{:>2}'.format(numb)
                    else:
                        self.add_list.append(numb)

        for numb in self.add_list:     # Цикл по всем не распределенным числам
            seq = NumbSequence()        # Создаём случайную последовательность из 3 элементов
            seq.create(3)
            for ind in range(3):        # Цикл по всем строкам карточки
                row = seq.next()        # Получаем случайный индекс
                if len(list([x for x in self.card[row - 1] if x != '  '])) < 5:    # Проверяем в строке чисел меньше 5
                    self.card[row - 1] = insert_numb_in_list(self.card[row - 1], numb)
                    break

    def find_number(self, number):
        return True in [True if '{:>2}'.format(number) in row else False for row in self.card]

    def number_cross_out(self, number):
        result = False
        for i, row in enumerate(self.card):
            if '{:>2}'.format(number) in row:
                pos = row.index('{:>2}'.format(number))
                self.card[i][pos] = '--'
                self.current_count_numbers -= 1
                result = True
                break
        return result

    def print_card(self):
        frame_char = 26
        numb_char = int((frame_char - len(self.player_name)) / 2) if frame_char - len(self.player_name) > 4 else 2
        header = f'{numb_char * "="} {self.player_name} {numb_char * "="}'
        print(header)
        print(f'{" ".join(self.card[0])}')
        print(f'{" ".join(self.card[1])}')
        print(f'{" ".join(self.card[2])}')
        print(f'{len(header) * "="}')


class Player:

    def __init__(self):
        self.my_card = LottoCard()
        self.is_computer = True
        self.lost = False
        self.name = ""

    def create_game_card(self, name_player, is_comp):
        self.my_card.create_card(name_player, 90)
        self.is_computer = is_comp
        self.name = name_player

    def check_number(self, number):
        """
        Проверка наличия указанного номера в карточке игрока
        Метод не учитывает тип игрока - компьютер/человек
        :param number:
        :return:
        """
        return self.my_card.find_number(number)

    def examination_number(self, number):
        """
        Метод проверки наличия номера в карточке. Метод зачеркивает номер в случае наличия
        Метод учитывает тип игрока
        :param number:
        :return:
        """
        result = self.my_card.number_cross_out(number)
        if not self.is_computer and not result:
            self.lost = True   # Если проверяет человек и значение не найдено = игра завершается, человек проиграл
        return result



if __name__ == '__main__':
    # Создание игровой карточки
    player1 = Player()
    player1.create_game_card("Иванов", False)
    player1.my_card.print_card()
    print("current_count_numbers =", player1.my_card.current_count_numbers, ", lost = ", player1.lost,
          ", is_computer = ", player1.is_computer)
    print("check_number 33 = ", player1.check_number(33))
    print("current_count_numbers =", player1.my_card.current_count_numbers, ", lost = ", player1.lost,
          ", is_computer = ", player1.is_computer)
    print("check_number 33 = ", player1.examination_number(33))
    print("current_count_numbers =", player1.my_card.current_count_numbers, ", lost = ", player1.lost,
          ", is_computer = ", player1.is_computer)
    print("check_number 33 = ", player1.examination_number(71))
    print("current_count_numbers =", player1.my_card.current_count_numbers, ", lost = ", player1.lost,
          ", is_computer = ", player1.is_computer)
    player1.my_card.print_card()





