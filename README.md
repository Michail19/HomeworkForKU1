# Конфигурационное управление

## Домашнее задание №1

**Вариант №6**

Разработать эмулятор для языка оболочки ОС. Необходимо сделать работу эмулятора как можно более похожей на сеанс shell в UNIX-подобной ОС. Эмулятор должен запускаться из реальной командной строки, а файл с виртуальной файловой системой не нужно распаковывать у пользователя. Эмулятор принимает образ виртуальной файловой системы в виде файла формата zip. Эмулятор должен работать в режиме CLI.
Конфигурационный файл имеет формат csv и содержит:
1. Имя пользователя для показа в приглашении к вводу.
2. Имя компьютера для показа в приглашении к вводу.
3. Путь к архиву виртуальной файловой системы.

Необходимо поддержать в эмуляторе команды ls, cd и exit, а также следующие команды:
1. date.
2. tail.

Все функции эмулятора должны быть покрыты тестами, а для каждой из поддерживаемых команд необходимо написать 3 теста.

## Описание всех функций и настроек

* ls - Команда вывода содержимого данного каталога;
* cd - Команда перехода к определённому каталогу;
* pwd - Команда вывода пути до данного каталога;
* exit - Команда для завершения процесса командной оболочки с кодом успешного завершения или кодом ошибки;
* date - Команда вывода текущей даты;
* tail - Команда вывода на экран последних 10 строк файла. Можно изменить количество выводимых строк.

## Команда для запуска проекта

Для запуска программы необходимо перейти из корневого каталога проекта в каталог ``Task_1`` посредством команды:

```
cd Task_1
```

После перехода в каталог ``Task_1`` запускаем программу:

```
python emulator.py
```

## Команда для запуска юнит-тестов

Для запуска юнит-тестов необходимо перейти из корневого каталога проекта в каталог ``Task_1`` посредством команды:

```
cd Task_1
```

Для запуска пишем команду:

```
python -m unittest main.py
```

## Описание работы программы

Программа запускается в каталоге ``Task_1``. Первоначально создана эмуляция образа Linux в VirtualDevice.zip архиве. Программа работает только с командами, указанными в условии задачи и разделе **``Описание всех функций и настроек``**. Результат работы команд выводится в консоль образа Linux. 

## Результат работы юнит-тестов

![2024-11-18 (1)](https://github.com/user-attachments/assets/33066e2d-9718-4efb-a58e-88ec02697813)

## Результат работы программы

![2024-11-18](https://github.com/user-attachments/assets/0b23a62e-56d5-4cb6-8175-240758c8594c)


