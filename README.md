# Config_3
Гаврина Екатерина ИКБО-20-23 (5 Вариант)
# Задание №3
  Разработать инструмент командной строки для учебного конфигурационного
языка, синтаксис которого приведен далее. Этот инструмент преобразует текст из
входного формата в выходной. Синтаксические ошибки выявляются с выдачей
сообщений.
#### Входной текст на языке xml принимается из стандартного ввода. Выходной
текст на учебном конфигурационном языке попадает в файл, путь к которому
задан ключом командной строки.
#### Однострочные комментарии:
  \ Это однострочный комментарий
####  Многострочные комментарии:
####  / +
####  Это многострочный комментарий
####  +/
####  Словари:
#####  {
#####   имя = значение
#####   имя = значение
#####   имя = значение
#####   ...
#####  }
#####  Имена:
  [_a-zA-Z]+
  26
#####  Значения:
  1. Числа.
  2. Словари.
####  Объявление константы на этапе трансляции:
  имя is значение
####  Вычисление константного выражения на этапе трансляции (префиксная форма), пример:
  @[+ имя 1]
####  Результатом вычисления константного выражения является значение.
  Для константных вычислений определены операции и функции:
  1. Сложение.
  2. Вычитание.
  3. pow().
  Все конструкции учебного конфигурационного языка (с учетом их
возможной вложенности) должны быть покрыты тестами. Необходимо показать 3
примера описания конфигураций из разных предметных областей.
