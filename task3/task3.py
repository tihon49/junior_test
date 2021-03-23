"""
============================ 
Task 3:
Мы сохраняем время присутствия каждого пользователя на уроке  виде интервалов. В функцию передается словарь, содержащий три списка с таймстемпами 
(время в секундах): — lesson – начало и конец урока 
— pupil – интервалы присутствия ученика 
— tutor – интервалы присутствия учителя 
Интервалы устроены следующим образом – это всегда список из четного количества элементов. Под четными индексами (начиная с 0) время входа на урок, 
под нечетными - время выхода с урока.
Нужно написать функцию, которая получает на вход словарь с интервалами и возвращает время общего присутствия ученика и учителя на уроке (в секундах). 
Будет плюсом: Написать WEB API с единственным endpoint’ом для вызова этой функции.
============================ 
"""

from datetime import date, datetime
import time


tests = [
   {'data': {'lesson': [1594663200, 1594666800],
             'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
             'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
    'answer': 3117
    },
   {'data': {'lesson': [1594702800, 1594706400],
             'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
             'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
    'answer': 6757 # 3577
    },
   {'data': {'lesson': [1594692000, 1594695600],
             'pupil': [1594692033, 1594696347],
             'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
    'answer': 3565
    },
]


# вспомогательная функция
def get_intevals(lst: list, pupil: list):
    """получаем список интервалов когда преподаватель на занятии
       возвращаем общее время присутствия на занатии (в секундах)   
    """

    total_time = 0

    for i, v  in enumerate(lst):
        if i % 2 == 0:
            start = v
            end = lst[i+1]

            # print(f'Интервал присутствия преподавателя на занятии:\n{start} - {end}')
            
            for pi, pv in enumerate(pupil):
                if pi % 2 == 0:
                    pupil_start = datetime.fromtimestamp(pv)
                    pupil_end = datetime.fromtimestamp(pupil[pi+1])

                    # print(f'Ученик: {pupil_start} - {pupil_end}')

                    if start <= pupil_start and pupil_end <= end:
                        # print('И препод и ученик на занятии')
                        # print(f'Препод: {start} - {end}')
                        # print(f'ученик: {pupil_start} - {pupil_end}')
                        # print(f'просидел: {pupil_end - pupil_start}\n')

                        if not total_time:
                            total_time = pupil_end - pupil_start
                        else:
                            total_time += pupil_end - pupil_start

                    elif start > pupil_start and start <= pupil_end <= end:
                    #     print(f'Ученик пришел раньше препода\nПрепод: {start} - {end}\nученик: {pupil_start} - {pupil_end}')
                    #     print(f'Время лекции: {start} - {pupil_end}')
                        # print(f'просидел: {pupil_end - start}\n')

                        if not total_time:
                            total_time = pupil_end - start
                        else:
                            total_time += pupil_end - start

                    elif start <= pupil_start < end and pupil_end > end:
                    #     print('Ученик задержался без препода')
                    #     print(f'Время занятия: {start} - {end}\nученик сидит с: {pupil_start} до {pupil_end}')
                        # print(f'просидел: {end - pupil_start}\n')

                        if not total_time:
                            total_time = end - pupil_start
                        else:
                            total_time += end - pupil_start

                    elif start > pupil_start and pupil_end > end:
                        # print(f'ученик пришел раньше и ушел позже: {pupil_start} - {pupil_end}')
                        # print(f'Время на занятии: {start} - {end}')
                        # print(f'просидел: {end - start}\n')

                        if not total_time:
                            total_time = end - start
                        else:
                            total_time += end - start

    return int(total_time.total_seconds())



def appearance(intervals: dict):
    lesson_time = intervals['lesson']
    tutor_time = intervals['tutor']
    pupil_time = intervals['pupil']

    for i, v  in enumerate(lesson_time):
        if i % 2 == 0:
            lesson_start = datetime.fromtimestamp(v)
            lesson_end = datetime.fromtimestamp(lesson_time[i+1])

            # print(f'\nЗанятие {lesson_start} - {lesson_end}\n')

            # время пресутствия преподавателя на занятии
            tutor_lesson_time = []

            for ij, jv in enumerate(tutor_time):
                if ij % 2 == 0:
                    tutor_start = datetime.fromtimestamp(jv)
                    tutor_end = datetime.fromtimestamp(tutor_time[ij+1])

                    if lesson_start <= tutor_start and tutor_end <= lesson_end:
                        # print(f'Преподаватель весь интервал на занятии: {tutor_start} - {tutor_end}\n')
                        tutor_lesson_time.append(tutor_start)
                        tutor_lesson_time.append(tutor_end)
                    elif lesson_start > tutor_start and lesson_start < tutor_end <= lesson_end:
                        # print(f'Преподаватель пришел раньше: {tutor_start} - {tutor_end}')
                        # print(f'Время преподавателя на занятии: {lesson_start} - {tutor_end}\n')
                        tutor_lesson_time.append(lesson_start)
                        tutor_lesson_time.append(tutor_end)
                    elif lesson_start <= tutor_start < lesson_end and tutor_end > lesson_end:
                        # print(f'Преподаватель задержадся после занятий: {tutor_start} - {tutor_end}')
                        # print(f'Время преподавателя на занятии: {tutor_start} - {lesson_end}\n')
                        tutor_lesson_time.append(tutor_start)
                        tutor_lesson_time.append(lesson_end)

            result = get_intevals(tutor_lesson_time, pupil_time)
            print(result)
            return result


def main():
    flask_data = {'data': []}

    for i, test in enumerate(tests):
        test_answer = appearance(test['data'])
        flask_data['data'].append(test_answer)
        assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'

    return flask_data

if __name__ == '__main__':
    main()
