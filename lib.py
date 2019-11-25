import random


class Basket:

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
        if len(self.list_numbers) >= 1:
            numb = self.list_numbers[random.randint(1, len(self.list_numbers)) - 1]
            self.list_numbers.remove(numb)
        else:
            numb = -1
        return numb


if __name__ == '__main__':
    # Создание объекта класса Bill
    test_basket = Basket()
    test_basket.create(4)
    print(len(test_basket.list_numbers))
    print(test_basket.list_numbers)
    print(test_basket.next())
    print(test_basket.list_numbers)
    print(test_basket.next())
    print(test_basket.list_numbers)
    print(test_basket.next())
    print(test_basket.list_numbers)
    print(test_basket.next())
    print(test_basket.list_numbers)
    print(test_basket.next())
    print(test_basket.list_numbers)
    test_basket.create(3)
    print(test_basket.next())
    print(test_basket.list_numbers)
    print(test_basket.next())
    print(test_basket.list_numbers)