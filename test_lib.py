import pytest
from lib import NumbSequence, Basket, Player, LottoCard, BasketIterator, RandomIterator
import random
# pip install pytest-cov
# pytest --cov
# pytest --cov-report=html

class TestRandomIterator:
    LEN_10 = 10

    def setup(self):
        self.numbers = RandomIterator(self.LEN_10)

    def teardown(self):
        pass

    def test_init(self):
        assert len(self.numbers.list_numbers) == self.LEN_10

    def test_next(self):
        for numb in self.numbers:
            assert 1 <= numb <= self.LEN_10


class TestBasketIterator:
    LEN_90 = 90

    def setup(self):
        self.numbers = BasketIterator(self.LEN_90)

    def teardown(self):
        pass

    def test_init(self):
        assert len(self.numbers.list_numbers) == self.LEN_90

    def test_next(self):
        for numb in self.numbers:
            assert 1 <= numb <= self.LEN_90


class TestNumbSequence:
    LEN_20 = 20
    LEN_1 = 1
    LEN_0 = 0

    def setup(self):
        pass

    def teardown(self):
        pass

    def test_len_list(self):
        sec = NumbSequence(self.LEN_20)
        assert len(sec.list_numbers) == self.LEN_20, "Ошибка проверки длины списка после инициализации"
        assert min(sec.list_numbers) == 1, "Нумерация списка должна начинаться с 1"
        assert max(sec.list_numbers) == self.LEN_20, "Последнее число списка = размеру массива"
        sec = NumbSequence(self.LEN_1)
        assert len(sec.list_numbers) == self.LEN_1, "Ошибка проверки длины списка после инициализации"
        assert min(sec.list_numbers) == 1, "Нумерация списка должна начинаться с 1"
        assert max(sec.list_numbers) == self.LEN_1, "Последнее число списка = размеру массива"
        with pytest.raises(ValueError):
            sec = NumbSequence(self.LEN_0)


    def test_next_number(self):
        sec = NumbSequence(self.LEN_20)
        numb = sec.next()
        while numb != -1:           # Выход при значении = -1
            assert 0 < numb <= self.LEN_20, "Ошибка проверки длины списка после инициализации"
            numb = sec.next()


class TestBasket:
    LEN_90 = 90

    def setup(self):
        self.sec = Basket()

    def teardown(self):
        pass

    def test_len_list(self):
        assert len(self.sec.list_numbers) == self.LEN_90, "Ошибка проверки длины списка после инициализации"
        assert min(self.sec.list_numbers) == 1, "Нумерация списка должна начинаться с 1"
        assert max(self.sec.list_numbers) == self.LEN_90, "Последнее число списка = размеру массива"
        assert self.sec.in_basket == self.LEN_90, "После инициализации в корзине 90 шаров"

    def test_next_number(self):
        numb = self.sec.next()
        i = 1
        while numb != -1:           # Выход при значении = -1
            assert 0 < numb <= self.LEN_90, "Число лежит в диапазоне от 1 до 90"
            assert self.sec.in_basket == self.LEN_90 - i, "Отсаток шаров в корзине - правильный"
            numb = self.sec.next()
            i += 1


class TestLottoCard:
    LEN_90 = 90
    NAME_PLAYER = "Владимир"

    def setup(self):
        random.seed(88)
        self.loto_card = LottoCard()
        self.loto_card.create_card(self.NAME_PLAYER)

    def teardown(self):
        pass

    def test_create_card(self):
        assert self.loto_card.player_name == self.NAME_PLAYER
        assert len(self.loto_card.card) == 3, "В карточке не 3 строки"
        assert len(self.loto_card.card[0]) == 9, "В карточке не 9 колонок"
        assert self.loto_card.current_count_numbers == 15, "В карточке не 15 бочёнков"

    def test_find_number(self):
        assert self.loto_card.find_number(10) == False
        assert self.loto_card.find_number(0) == True
        assert self.loto_card.find_number(-1) == False

    def test_number_cross_out(self):
        assert self.loto_card.number_cross_out(16) == True
        assert self.loto_card.number_cross_out(10) == False

    def test_print_card(self):
        result = self.loto_card.print_card()
        assert len(result) == 5


class TestPlayerComp:
    IS_COMP = True
    NAME_PLAYER = "Компьютер 1"

    def setup(self):
        random.seed(88)
        self.player = Player()
        self.player.create_game_card(self.NAME_PLAYER, self.IS_COMP)

    def teardown(self):
        pass

    def test_create_game_card(self):
        assert self.player.name == self.NAME_PLAYER
        assert self.player.is_computer == self.IS_COMP
        assert self.player.lost == False
        assert self.player.is_computer == True

    def test_check_number(self):
        assert self.player.check_number(10) == False
        assert self.player.check_number(16) == True
        assert self.player.check_number(0) == True
        assert self.player.check_number(-1) == False


class TestPlayerHuman:
    IS_COMP = False
    NAME_PLAYER = "Владимир"
    LEN_90 = 90

    def setup(self):
        random.seed(88)
        self.player = Player()
        self.player.create_game_card(self.NAME_PLAYER, self.IS_COMP)

    def teardown(self):
        pass

    def test_create_game_card(self):
        assert self.player.name == self.NAME_PLAYER
        assert self.player.is_computer == self.IS_COMP
        assert self.player.lost == False
        assert self.player.is_computer == False

    def test_check_number(self):
        assert self.player.check_number(10) == False
        assert self.player.check_number(16) == True
        assert self.player.check_number(0) == True
        assert self.player.check_number(-1) == False

    def test_examination_number(self):
        numb = 0
        for i in range(1, self.LEN_90):
            if not self.player.check_number(i): # Если значения нет, а игрок сказал вычеркнуть значение = проиграл
                numb = i
                break
        self.player.examination_number(numb)
        assert self.player.lost == True, "Игрок должен проиграть при проверке отсутствующего значения"








