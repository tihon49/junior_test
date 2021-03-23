"""
============================ 
Task 2:
В нашей школе мы не можем разглашать персональные данные пользователей, но чтобы преподаватель и ученик смогли 
объяснить нашей поддержке, кого они имеют в виду (у преподавателей, например, часто учится несколько Саш), мы 
генерируем пользователям уникальные и легко произносимые имена. Имя у нас состоит из прилагательного, имени 
животного и двузначной цифры. В итоге получается, например, "Перламутровый лосось 77". Для генерации таких 
имен мы и решали следующую задачу:
Получить с русской википедии список всех животных (Категория:Животные по алфавиту) и вывести количество животных 
на каждую букву алфавита. Результат должен получиться в следующем виде:
А: 642
Б: 412
В:....
============================ 
"""

import requests
from bs4 import BeautifulSoup as bs


URL = 'https://ru.wikipedia.org/w/index.php?title=Категория:Животные_по_алфавиту&from=а'
# получаем русский алфавит
a = ord('а')
letters_list = [chr(i) for i in range(a,a+6)] + [chr(a+33)] + [chr(i) for i in range(a+6,a+32)]


def animals_count(url: str, memo=[]) -> dict:
    """функция для получения всех названий животных из википедии

    входящие аргументы:
        url (str): url для парсинга
        memo (list): список в который рекурсивно будут добавляться названия животных

    Returns:
        dict: memo - список со всеми животными
    """

    request = requests.get(url)

    if request.status_code == 200:
        soup = bs(request.content, 'lxml')
        main_div = soup.find('div', id='mw-pages')
        groups = main_div.find_all('div', class_='mw-category-group')
        
        for group in groups:
            animals_list = [animal.text for animal in group.find('ul').find_all('li')]

            # если начнутся английские буквы, функция закончит работу
            if animals_list[-1][0].lower() not in letters_list:
                return memo

            memo.extend(animals_list)

        next_page_href = main_div.find_all('a')[1]

        if next_page_href.text == 'Следующая страница':
            animals_count('https://ru.wikipedia.org' + next_page_href.get('href'))

    return memo


def main():
    print('Task #2')
    result = animals_count(URL)

    for i in letters_list:
        print(f'{i.upper()}: {len([j for j in result if j[0].lower() == i])}')


if __name__ == '__main__':
    main()