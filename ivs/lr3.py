"""
Задача о трёх миссионерах и трёх каннибалах.
Три миссионера и три каннибала должны переправиться с левого берега на правый.
Лодка вмещает максимум 2 человека.
На любом берегу не должно быть каннибалов больше, чем миссионеров (если миссионеры есть).
Решение через поиск в ширину (BFS).
"""

from collections import deque

def is_valid_state(left_missionaries, left_cannibals, right_missionaries, right_cannibals):
    """
    Проверяет, является ли состояние допустимым.
    На каждом берегу миссионеров не должно быть меньше каннибалов,
    если миссионеры есть.
    """
    # Проверка левого берега
    if left_missionaries > 0 and left_missionaries < left_cannibals:
        return False
    
    # Проверка правого берега
    if right_missionaries > 0 and right_missionaries < right_cannibals:
        return False
    
    # Количество людей не может быть отрицательным
    if (left_missionaries < 0 or left_cannibals < 0 or 
        right_missionaries < 0 or right_cannibals < 0):
        return False
    
    # Всего людей не может быть больше 6
    if (left_missionaries + left_cannibals + right_missionaries + right_cannibals) != 6:
        return False
    
    return True

def get_next_states(state):
    """
    Генерирует все возможные следующие состояния из текущего.
    state = (левые_миссионеры, левые_каннибалы, правые_миссионеры, правые_каннибалы, лодка)
    лодка: 0 - на левом берегу, 1 - на правом
    """
    left_m, left_c, right_m, right_c, boat = state
    
    next_states = []
    
    # Возможные варианты перевозки людей в лодке
    # (миссионеры, каннибалы) в лодке
    moves = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]
    
    for m_in_boat, c_in_boat in moves:
        if boat == 0:  # Лодка на левом берегу - едем на правый
            new_left_m = left_m - m_in_boat
            new_left_c = left_c - c_in_boat
            new_right_m = right_m + m_in_boat
            new_right_c = right_c + c_in_boat
            new_boat = 1
        else:  # Лодка на правом берегу - едем на левый
            new_left_m = left_m + m_in_boat
            new_left_c = left_c + c_in_boat
            new_right_m = right_m - m_in_boat
            new_right_c = right_c - c_in_boat
            new_boat = 0
        
        # Проверяем, что в лодке не больше 2 человек и они есть на нужном берегу
        if boat == 0 and (m_in_boat > left_m or c_in_boat > left_c):
            continue
        if boat == 1 and (m_in_boat > right_m or c_in_boat > right_c):
            continue
        
        # Создаём новое состояние
        new_state = (new_left_m, new_left_c, new_right_m, new_right_c, new_boat)
        
        # Проверяем, допустимо ли новое состояние
        if is_valid_state(new_left_m, new_left_c, new_right_m, new_right_c):
            next_states.append(new_state)
    
    return next_states

def solve_missionaries_cannibals():
    """
    Решает задачу о миссионерах и каннибалах с помощью BFS.
    Возвращает путь от начального состояния до конечного.
    """
    # Начальное состояние: все на левом берегу, лодка слева
    start_state = (3, 3, 0, 0, 0)
    # Конечное состояние: все на правом берегу, лодка справа
    goal_state = (0, 0, 3, 3, 1)
    
    # Очередь для BFS: хранит (состояние, путь_до_него)
    queue = deque()
    queue.append((start_state, [start_state]))
    
    # Множество посещённых состояний (чтобы не ходить по кругу)
    visited = set()
    visited.add(start_state)
    
    while queue:
        current_state, path = queue.popleft()
        
        # Проверяем, достигли ли цели
        if current_state == goal_state:
            return path
        
        # Генерируем все возможные следующие состояния
        for next_state in get_next_states(current_state):
            if next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, path + [next_state]))
    
    return None  # Решения не найдено

def visualize_solution(path):
    """
    Красиво визуализирует найденное решение.
    """
    if not path:
        print("Решение не найдено!")
        return
    
    print("\n" + "="*70)
    print("РЕШЕНИЕ ЗАДАЧИ О ТРЁХ МИССИОНЕРАХ И ТРЁХ КАННИБАЛАХ")
    print("="*70)
    
    step_num = 0
    for i, state in enumerate(path):
        left_m, left_c, right_m, right_c, boat = state
        
        print(f"\n--- Шаг {step_num} ---")
        
        # Текстовое описание
        if i == 0:
            print("Начальное состояние:")
        elif boat != path[i-1][4]:
            print("Лодка переплыла на другой берег:")
        else:
            print("Продолжение переправы:")
        
        # Визуализация берегов
        print("\n  ЛЕВЫЙ БЕРЕГ" + " " * 30 + "ПРАВЫЙ БЕРЕГ")
        print("  " + "-" * 40 + " " + "-" * 40)
        
        # Отображение миссионеров
        left_m_str = "М" * left_m if left_m > 0 else "—"
        right_m_str = "М" * right_m if right_m > 0 else "—"
        print(f"  Миссионеры: {left_m_str:<15}   |   Миссионеры: {right_m_str}")
        
        # Отображение каннибалов
        left_c_str = "К" * left_c if left_c > 0 else "—"
        right_c_str = "К" * right_c if right_c > 0 else "—"
        print(f"  Каннибалы:  {left_c_str:<15}   |   Каннибалы:  {right_c_str}")
        
        # Отображение лодки
        boat_pos = "ЛОДКА НА ЛЕВОМ БЕРЕГУ <<<" if boat == 0 else ">>> ЛОДКА НА ПРАВОМ БЕРЕГУ"
        print(f"\n  {boat_pos}")
        
        # Подсчёт количества людей на каждом берегу
        print(f"\n  Всего людей: {left_m + left_c} на левом, {right_m + right_c} на правом")
        
        step_num += 1
    
    print("\n" + "="*70)
    print(f"РЕШЕНИЕ НАЙДЕНО! Всего шагов: {len(path)-1}")
    print("="*70)

# ==================== ТЕСТЫ ====================

def test_is_valid_state():
    """Тест 1: Проверка функции проверки допустимых состояний"""
    # Корректные состояния (должны вернуть True)
    assert is_valid_state(3, 3, 0, 0) == True   # Все на левом
    assert is_valid_state(0, 0, 3, 3) == True   # Все на правом
    assert is_valid_state(2, 2, 1, 1) == True   # 2-2 и 1-1
    assert is_valid_state(1, 1, 2, 2) == True   # 1-1 и 2-2
    assert is_valid_state(3, 2, 0, 1) == True   # 3-2 и 0-1
    
    # Некорректные состояния (должны вернуть False)
    assert is_valid_state(1, 2, 2, 1) == False  # На левом каннибалов больше
    assert is_valid_state(2, 1, 1, 2) == False  # На правом каннибалов больше
    assert is_valid_state(2, 3, 1, 0) == False  # На левом каннибалов больше
    assert is_valid_state(1, 1, 2, 3) == False  # На правом каннибалов больше
    assert is_valid_state(-1, 3, 4, 0) == False # Отрицательное количество
    assert is_valid_state(2, 2, 2, 2) == False  # Всего 8 человек (не 6)
    
    print("✅ Тест 1 (is_valid_state) пройден!")

def test_get_next_states():
    """Тест 2: Проверка генерации следующих состояний"""
    start_state = (3, 3, 0, 0, 0)
    next_states = get_next_states(start_state)
    
    # Выведем полученные состояния для отладки
    print(f"\nПолучено {len(next_states)} состояний:")
    for state in next_states:
        print(f"  {state}")
    
    # Проверяем, что количество состояний больше 0
    assert len(next_states) > 0
    
    # Проверяем, что все сгенерированные состояния допустимы
    for state in next_states:
        left_m, left_c, right_m, right_c, boat = state
        assert is_valid_state(left_m, left_c, right_m, right_c) == True
        # Лодка должна быть на правом берегу
        assert boat == 1
    
    # Проверяем, что все состояния имеют правильную сумму (6 человек)
    for state in next_states:
        left_m, left_c, right_m, right_c, boat = state
        assert left_m + left_c + right_m + right_c == 6
    
    print("✅ Тест 2 (get_next_states) пройден!")

def test_solution_exists():
    """Тест 3: Проверка наличия и корректности решения"""
    solution = solve_missionaries_cannibals()
    
    # Решение должно существовать
    assert solution is not None
    
    # Начальное состояние должно быть (3,3,0,0,0)
    assert solution[0] == (3, 3, 0, 0, 0)
    
    # Конечное состояние должно быть (0,0,3,3,1)
    assert solution[-1] == (0, 0, 3, 3, 1)
    
    # Проверяем, что каждый шаг в решении допустим
    for i in range(len(solution) - 1):
        current = solution[i]
        next_state = solution[i + 1]
        # Проверяем, что следующее состояние достижимо из текущего
        assert next_state in get_next_states(current)
    
    print("✅ Тест 3 (solution_exists) пройден!")

# ==================== ЗАПУСК ====================

if __name__ == "__main__":
    print("Запуск тестов...")
    print("-" * 50)
    test_is_valid_state()
    test_get_next_states()
    test_solution_exists()
    print("-" * 50)
    print("🎉 Все тесты пройдены успешно!\n")
    
    # Решаем задачу и визуализируем
    print("Поиск решения...")
    solution_path = solve_missionaries_cannibals()
    
    if solution_path:
        print(f"\nНайдено решение из {len(solution_path)-1} шагов!")
        visualize_solution(solution_path)
    else:
        print("Решение не найдено!")

