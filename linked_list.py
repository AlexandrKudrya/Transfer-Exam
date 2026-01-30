from typing import Optional, List, Any


class EmptyListError(Exception):
    """Исключение для пустого списка"""
    pass


class InvalidIndexError(Exception):
    """Исключение для невалидного индекса"""
    pass


class Node:
    """Узел односвязного списка"""
    
    def __init__(self, data: Any) -> None:
        if data is None:
            raise ValueError("Данные узла не могут быть None")
        self.data: Any = data
        self.next: Optional['Node'] = None
    
    def __repr__(self) -> str:
        return f"Node({self.data})"


class LinkedList:
    """Односвязный список с проверкой симметричности"""
    
    def __init__(self) -> None:
        self.head: Optional[Node] = None
        self._size: int = 0
    
    def add(self, value: Any) -> None:
        """Добавление элемента в конец списка"""
        if value is None:
            raise ValueError("Невозможно добавить None в список")
        
        try:
            new_node = Node(value)
        except Exception as e:
            raise ValueError(f"Ошибка создания узла: {e}")
        
        if not self.head:
            self.head = new_node
            self._size = 1
            return
        
        curr = self.head
        while curr.next:
            curr = curr.next
        curr.next = new_node
        self._size += 1
    
    def get(self, index: int) -> Any:
        """Получение элемента по индексу"""
        if index < 0 or index >= self._size:
            raise InvalidIndexError(f"Индекс {index} вне диапазона [0, {self._size - 1}]")
        
        curr = self.head
        for _ in range(index):
            if curr is None:
                raise InvalidIndexError("Некорректная структура списка")
            curr = curr.next
        
        if curr is None:
            raise InvalidIndexError("Элемент не найден")
        
        return curr.data
    
    def size(self) -> int:
        """Получение размера списка"""
        return self._size
    
    def is_empty(self) -> bool:
        """Проверка на пустоту"""
        return self.head is None
    
    def print_list(self) -> None:
        """Вывод списка"""
        if self.is_empty():
            print("Список пуст")
            return
        
        curr = self.head
        elements: List[str] = []
        while curr:
            elements.append(str(curr.data))
            curr = curr.next
        print(' '.join(elements))
    
    def to_list(self) -> List[Any]:
        """Преобразование в обычный список Python"""
        elements: List[Any] = []
        curr = self.head
        while curr:
            elements.append(curr.data)
            curr = curr.next
        return elements
    
    def is_symmetric(self) -> bool:
        """Проверка списка на симметричность"""
        if self.is_empty():
            return True
        
        try:
            elements = self.to_list()
        except Exception as e:
            raise RuntimeError(f"Ошибка при преобразовании списка: {e}")
        
        n = len(elements)
        
        # Проверяем симметричность
        for i in range(n // 2):
            try:
                if elements[i] != elements[n - 1 - i]:
                    return False
            except IndexError as e:
                raise RuntimeError(f"Ошибка при сравнении элементов: {e}")
        
        return True
    
    def clear(self) -> None:
        """Очистка списка"""
        self.head = None
        self._size = 0
    
    def __len__(self) -> int:
        """Длина списка"""
        return self._size
    
    def __str__(self) -> str:
        """Строковое представление"""
        if self.is_empty():
            return "LinkedList([])"
        return f"LinkedList({self.to_list()})"
    
    def __repr__(self) -> str:
        return self.__str__()


def test_symmetric_list():
    """Проверка симметричного списка с нечетным количеством элементов"""
    lst = LinkedList()
    for x in [1, 2, 3, 2, 1]:
        lst.add(x)
    assert lst.is_symmetric() == True
    assert lst.size() == 5
    assert lst.to_list() == [1, 2, 3, 2, 1]


def test_non_symmetric_list():
    """Проверка несимметричного списка"""
    lst = LinkedList()
    for x in [1, 2, 3, 45, 2, 1]:
        lst.add(x)
    assert lst.is_symmetric() == False
    assert lst.size() == 6


def test_even_elements():
    """Проверка симметричного списка с четным количеством элементов"""
    lst = LinkedList()
    for x in [1, 2, 2, 1]:
        lst.add(x)
    assert lst.is_symmetric() == True
    assert lst.size() == 4


def test_single_element():
    """Проверка списка из одного элемента"""
    lst = LinkedList()
    lst.add(42)
    assert lst.is_symmetric() == True
    assert lst.size() == 1


def test_empty_list():
    """Проверка пустого списка"""
    lst = LinkedList()
    assert lst.is_empty() == True
    assert lst.is_symmetric() == True
    assert lst.size() == 0


def test_add_none():
    """Проверка попытки добавления None в список"""
    lst = LinkedList()
    try:
        lst.add(None)
        assert False, "Должно было выброситься исключение"
    except ValueError:
        pass


def test_get_by_index():
    """Проверка получения элементов по индексу"""
    lst = LinkedList()
    for x in [10, 20, 30, 40, 50]:
        lst.add(x)
    assert lst.get(0) == 10
    assert lst.get(2) == 30
    assert lst.get(4) == 50


def test_invalid_index():
    """Проверка обработки невалидного индекса"""
    lst = LinkedList()
    for x in [1, 2, 3]:
        lst.add(x)
    try:
        lst.get(10)
        assert False, "Должно было выброситься исключение"
    except InvalidIndexError:
        pass


def test_negative_index():
    """Проверка обработки отрицательного индекса"""
    lst = LinkedList()
    for x in [1, 2, 3]:
        lst.add(x)
    try:
        lst.get(-1)
        assert False, "Должно было выброситься исключение"
    except InvalidIndexError:
        pass


def test_string_elements():
    """Проверка работы со строковыми элементами"""
    lst = LinkedList()
    for s in ['a', 'b', 'c', 'b', 'a']:
        lst.add(s)
    assert lst.is_symmetric() == True


def read_from_file(filename: str) -> Optional[LinkedList]:
    """Чтение чисел из файла и создание списка"""
    lst = LinkedList()
    
    try:
        with open(filename, 'r') as f:
            content = f.read().strip()
            if not content:
                return lst
            
            numbers = content.split()
            for num_str in numbers:
                try:
                    num = int(num_str)
                    lst.add(num)
                except ValueError:
                    print(f"Предупреждение: '{num_str}' не является числом, пропускаем")
        
        return lst
    except FileNotFoundError:
        print(f"Файл '{filename}' не найден")
        return None
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return None


def run_all_tests():
    test_symmetric_list()
    test_non_symmetric_list()
    test_even_elements()
    test_single_element()
    test_empty_list()
    test_add_none()
    test_get_by_index()
    test_invalid_index()
    test_negative_index()
    test_string_elements()
    print("Все тесты пройдены")


if __name__ == "__main__":
    # Сначала запускаем тесты
    run_all_tests()
    print()
    
    # Потом читаем из файла
    filename = "numbers.txt"
    lst = read_from_file(filename)
    
    if lst is not None:
        if lst.is_empty():
            print(f"Файл '{filename}' пуст или не содержит чисел")
        else:
            print(f"Список из файла '{filename}':")
            lst.print_list()
            print(f"Симметричен: {'да' if lst.is_symmetric() else 'нет'}")
    else:
        print(f"Создаю тестовый файл '{filename}' с содержимым: 1 2 3 2 1")
        with open(filename, 'w') as f:
            f.write("1 2 3 2 1")
        print("Запустите программу снова для проверки")
