import random

COUNT_NUMB = 90

class NumbSequence:

    def __init__(self, size):
        """
            Инициализация корзины, заполнение корзины цифрами от 1 до size + 1
            :param size: Размер корзины с номерами лото
        """
        if size <= 0:
            raise ValueError()
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
        super().__init__(COUNT_NUMB)
        self.in_basket = COUNT_NUMB

    def next(self):
        self.in_basket -= 1
        return super(Basket, self).next()


class LottoCard:

    COUNT_NUMB_IN_CARD = 15
    COUNT_NUMB_IN_LINE = 5

    def __init__(self):
        """
        Инициализация игровой карточки лото
        В каждой карточке есть свойство - Имя игрока
        В каждой строке - 5 цифр на 9 полей
        В каждой карточке 3 строки
        """
        self.player_name = ""
        self.current_count_numbers = self.COUNT_NUMB_IN_CARD
        self.card = [[0] * 9 for i in range(3)]

    def create_card(self, name):
        self.player_name = name
        card_set = set()
        while len(card_set) < self.COUNT_NUMB_IN_CARD:
            card_set.add(random.randint(1, COUNT_NUMB))
        card_int = list(card_set)
        #self.card_int = [65, 67, 68, 3, 72, 41, 42, 74, 12, 13, 79, 48, 19, 25, 90]
        #print(self.card_int)

        for line in range(3):
            seq = NumbSequence(5)
            temp_line_list = []
            for col in range(5):
                numb = seq.next()
                next_numb = card_int[numb - 1]
                temp_line_list.append(next_numb)

            for ind in range(5):    # Удаляем 5 элементов извлеченных из массива
                card_int.remove(temp_line_list[ind - 1])
            temp_line_list.sort()   # Сортируем список

            for i, x in enumerate(range(1, 5)):
                if i == 4:
                    break
                numb = random.randint(1, len(temp_line_list))
                if 1 < numb <= len(temp_line_list):
                    temp_line_list.insert(numb - 1, 0)
                elif 1 == numb:
                    temp_line_list.insert(1, 0)
                elif numb >= len(temp_line_list):
                    temp_line_list.insert(len(temp_line_list) - 1, 0)

            self.card[line] = temp_line_list

    def find_number(self, number):
        return True in [True if number in row else False for row in self.card]

    def number_cross_out(self, number):
        result = False
        for i, row in enumerate(self.card):
            if number in row:
                pos = row.index(number)
                self.card[i][pos] = -1      # Если мы вычеркиваем цифру из карточки, то значение меняем на -1
                self.current_count_numbers -= 1
                result = True
                break
        return result

    def print_card(self):
        frame_char = 26
        numb_char = int((frame_char - len(self.player_name)) / 2) if frame_char - len(self.player_name) > 4 else 2
        header = f'{numb_char * "="} {self.player_name} {numb_char * "="}'
        result = []
        result.append(header)
        result.append(" ".join(list(['{:>2}'.format(x) if len(str(x)) == 1 else str(x) for x in self.card[0]])).
              replace(" 0", "  ").replace("-1", "--"))
        result.append(" ".join(list(['{:>2}'.format(x) if len(str(x)) == 1 else str(x) for x in self.card[1]])).
                      replace(" 0", "  ").replace("-1", "--"))
        result.append(" ".join(list(['{:>2}'.format(x) if len(str(x)) == 1 else str(x) for x in self.card[2]])).
                      replace(" 0", "  ").replace("-1", "--"))
        result.append(f'{len(header) * "="}')
        return result


class Player:

    def __init__(self):
        self.my_card = LottoCard()
        self.is_computer = True
        self.lost = False
        self.name = ""

    def create_game_card(self, name_player, is_comp):
        self.my_card.create_card(name_player)
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



# if __name__ == '__main__':
#
#     player = Player()
#     player.create_game_card("Владимир", False)
#     print("\n".join(player.my_card.print_card()))
#     print("check_number(10) = ", player.check_number(10))
#     print("my_card.find_number(10) = ", player.my_card.find_number(10))
#     print("examination_number(10) = ", player.examination_number(10))
#     print("\n".join(player.my_card.print_card()))
#     print("lost = ", player.lost)







