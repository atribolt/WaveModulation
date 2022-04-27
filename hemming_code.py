# добавляю чужой код, который умные люди написали за нас
# здесь добавляю математические функции логарифма и округления по верзней границе
# log2 - оотсветсвенно логарифм по 2
# ceil - округление, из 0.1 сделает 1 и из 0.7 сделает 1
from math import log2, ceil

# это либа для работы с матрицами, а точнее просто математическая либа
# array - функция, которая создает массив (или вектор), при это может содержать массивы внутри массива
# flip - функция, которая разворачивает массив. Было [1 2 3] делает [3 2 1]
from numpy import array, flip

# переменная, которая хранит кол-во бит для кодирования (одно слово)
WORD_LEN = 11

# минимальное входное число для кодирования
MIN = 0

# максимальное число для кодирования ("**" это возведение в степень, т.е 2 в степени 11)
MAX = 2 ** WORD_LEN

# кол-во контрольных битов. Берется логарифм от длины слова и округляет до целого в большую сторону
CONTROL_BITS = ceil(log2(WORD_LEN))

"""
Здесь создается матрица для вычисления контрольных битов
По факту, сначала создается набор чисел от 1 до "кол-во контрольных бит" ** 2 (или от 1 до 16)
Затем эти числа переводятся в бинарный вид и складываются в матрицу, получается такое
[[0, 0, 0, 1],   <- это 1
 [0, 0, 1, 0],   <- это 2
 [0, 0, 1, 1]    <- это 3
 ...
 
Далее нужно транспонировать это матрицу, чтобы получить 15 столбцов (отчет от 0, поэтому 15, а не 16)
Ну и просто инвертировать порядок, чтобы столбец с [0001] стоял слева, а [1110] справа
"""
MATRIX = [format(i, f'0>{CONTROL_BITS}b') for i in range(1, CONTROL_BITS ** 2)]
MATRIX = [[int(j) for j in i] for i in MATRIX]
MATRIX = flip(array(MATRIX).T, 0)

# это функция кодирования, получает число в биапазоне [MIN; MAX)
def encode(number: int):
  # для начала переведем это число в бинарный вид и дополним нулями до 11 символов (длина слова)
  data = reversed(format(number, f'0>{WORD_LEN}b'))

  # теперь каждый символ (0 или 1) переводим в число
  data = [int(i) for i in data]

  # наполняем контрольными битами. Каждый контрольный бит втыкаем в позицию,
  # которую можно посчитать как: "номер бита" ** 2 (т.е степень двойки) и втыкаем в эту позицию 0
  for i in range(CONTROL_BITS):
    index = i ** 2
    data.insert(index, 0)

  # теперь вычисляем каждый воткнутый бит
  for i in range(CONTROL_BITS):
    n1 = int(''.join([str(j) for j in data]), 2)
    n2 = int(''.join([str(j) for j in MATRIX[i]]))

    # здесь амперсанд это оператор побитового И, а процент - остаток от деления на 2
    bit = (n1 & n2) % 2

    # ну и устанавливаем бит
    data[i**2] = bit

  # здесь просто переводим закодированные биты в число
  n1 = int(''.join([str(j) for j in data]), 2)
  # находим кол-во 1 в числе, и если оно нечетное, то устанавливаем первый бит в 1.
  # это к общему числу бит добавит один и сделает кол-во четным
  data.insert(0, n1.bit_count() % 2)

  return int(''.join([str(j) for j in data]), 2)


def decode(encoded: int):
  data = format(encoded, f'0>{CONTROL_BITS ** 2}b')

  even_bit = int(data[0])
  data = [int(i) for i in data[1:]]

  bit_count = encoded.bit_count() - 1 if even_bit else encoded.bit_count()

  if bit_count % 2 != 0:
    print('Данные повреждены')

    bad_bit = []
    for i in range(CONTROL_BITS):
      n1 = encoded
      n2 = int(''.join([str(j) for j in MATRIX[i]]))

      bad_bit.append((n1 & n2) % 2)

    invalid_bit = int(''.join(str(i) for i in bad_bit), 2)
    print(f'Битый бит: {invalid_bit}')
    data[invalid_bit-1] = int(not data[invalid_bit-1])

  for i in range(CONTROL_BITS):
    data.pop(i**2 - i)

  data = reversed(data)
  return int(''.join(str(i) for i in data), 2)


if __name__ == '__main__':
  data = 240
  print('Вход: ', bin(data), data, hex(data))

  e = encode(data)
  print('Закодированное: ', bin(e), e, hex(e))

  d = decode(e)
  print('Декодированное: ', bin(d), d, hex(d))

  e |= 1
  print('Инвертированный бит в закодированном: ', bin(e), e, hex(e))
  d = decode(e)

  print('Восстановление: ', bin(d), d, hex(d))
