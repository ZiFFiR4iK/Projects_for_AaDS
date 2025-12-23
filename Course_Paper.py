import time
from typing import List, Tuple, Optional, Set
from concurrent.futures import ThreadPoolExecutor, as_completed

# Ввод судоку 
SUDOKU_INPUT = """
200080300
060070084
030500209
000105408
000000000
402706000
301007040
720040060
004010003
"""

""" Преобразование строк в числовую матрицу """
def parse_sudoku(input_str: str) -> List[List[int]]:
    lines = input_str.strip().split('\n')
    puzzle = []  
    for line in lines:
        row = [int(char) if char != '0' else 0 for char in line.strip()]
        puzzle.append(row)  
    return puzzle

""" Создаем исходную головоломку """
ORIGINAL_PUZZLE = parse_sudoku(SUDOKU_INPUT)



# Наивный перебор
""" Проверка, можно ли вставить число в клетку"""
def is_valid_move(board: List[List[int]], row: int, col: int, num: int) -> bool:
     
    for j in range(9):
        if board[row][j] == num:
            return False  
     
    for i in range(9):
        if board[i][col] == num:
            return False  
    
    start_row, start_col = 3 * (row // 3), 3 * (col // 3) 
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False  
    return True  

""" Находим первую пустую клетку """
def find_empty_cell(board: List[List[int]]) -> Optional[Tuple[int, int]]:
    for i in range(9):  
        for j in range(9):  
            if board[i][j] == 0:  
                return (i, j)  
    return None  

""" Сам алгоритм наивного перебора """
def naive_backtrack_solve(board: List[List[int]], stats: dict) -> bool:
    stats['iterations'] += 1  
    empty = find_empty_cell(board)  
    if not empty:  
        return True  
    row, col = empty  
    
    for num in range(1, 10):
        if is_valid_move(board, row, col, num):  
            board[row][col] = num  
            
            if naive_backtrack_solve(board, stats):
                return True  
            
            board[row][col] = 0  
            stats['backtracks'] += 1  
    return False  

""" Запуск наивного перебора """
def run_naive_algorithm() -> dict:
    puzzle = [row[:] for row in ORIGINAL_PUZZLE]  
    stats = {'iterations': 0, 'backtracks': 0}  
    start_time = time.perf_counter()  
    solved = naive_backtrack_solve(puzzle, stats)  
    elapsed = time.perf_counter() - start_time  
    
    return {
        'algorithm': 'Наивный перебор',
        'solved': solved,
        'time': elapsed,
        'iterations': stats['iterations'],
        'backtracks': stats['backtracks'],
        'solution': puzzle if solved else None
    }



# Перебор с ограничениями
""" Возвращает множество возможных чисел(кандидатов) """
def get_candidates(board: List[List[int]], row: int, col: int) -> Set[int]:
    if board[row][col] != 0:  
        return set()  
    
    candidates = set(range(1, 10))
    
    for j in range(9):
        if board[row][j] != 0:
            candidates.discard(board[row][j])
    
    for i in range(9):
        if board[i][col] != 0:
            candidates.discard(board[i][col])
    
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] != 0:
                candidates.discard(board[i][j])
    return candidates  

""" Поиск клетки с минимальным количеством возможных чисел """
def get_most_constrained_cell(board: List[List[int]]) -> Optional[Tuple[int, int, Set[int]]]:
    best_cell = None  
    min_candidates = 10  
    for i in range(9):  
        for j in range(9):  
            if board[i][j] == 0:  
                candidates = get_candidates(board, i, j)  
                if len(candidates) == 0:  
                    return None  
                if len(candidates) < min_candidates:  
                    min_candidates = len(candidates)  
                    best_cell = (i, j, candidates)  
    return best_cell  

""" Сам алгоритм перебора с ограничениями """
def constrained_backtrack_solve(board: List[List[int]], stats: dict) -> bool:
    stats['iterations'] += 1  
    cell_info = get_most_constrained_cell(board)  
    if not cell_info:  
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return False  
        return True  
    row, col, candidates = cell_info  
    
    for num in candidates:
        board[row][col] = num  
        
        if constrained_backtrack_solve(board, stats):
            return True  
        board[row][col] = 0  
        stats['backtracks'] += 1  
    return False  

""" Запуск алгоритма перебора с ограничениями """
def run_constrained_algorithm() -> dict:
    puzzle = [row[:] for row in ORIGINAL_PUZZLE]  
    stats = {'iterations': 0, 'backtracks': 0}  
    start_time = time.perf_counter()  
    solved = constrained_backtrack_solve(puzzle, stats)  
    elapsed = time.perf_counter() - start_time  
    return {
        'algorithm': 'Перебор с ограничениями',
        'solved': solved,
        'time': elapsed,
        'iterations': stats['iterations'],
        'backtracks': stats['backtracks'],
        'solution': puzzle if solved else None
    }



# Алгоритм Dancing Links
""" Узел """
class DLinksNode:
    def __init__(self):
        self.left = self  
        self.right = self  
        self.up = self  
        self.down = self  
        self.column = None  
        self.row_id = -1  
        self.col_id = -1  
        self.size = 0  

""" Реализация алгоритма """
class DancingLinksSolver:
    
    def __init__(self, puzzle: List[List[int]]):
        self.puzzle = puzzle  
        self.header = DLinksNode()  
        self.solution = []  
        self.solution_rows = []  
        self.columns = 324  
        self.total_rows = 0  
        self.rows_data = []  
        self._create_matrix()  

    """ Создание матрицы """
    def _create_matrix(self):
        column_nodes = []  
        prev = self.header  
        for i in range(self.columns):
            col_node = DLinksNode()  
            col_node.col_id = i  
            col_node.column = col_node  
            col_node.size = 0  
            col_node.left = prev
            col_node.right = self.header
            prev.right = col_node
            self.header.left = col_node
            prev = col_node
            column_nodes.append(col_node)  
        for row in range(9):  
            for col in range(9):  
                for num in range(1, 10):  
                    if self.puzzle[row][col] != 0 and self.puzzle[row][col] != num:
                        continue
                    
                    cell_constraint = row * 9 + col  
                    row_constraint = 81 + row * 9 + (num - 1)  
                    col_constraint = 162 + col * 9 + (num - 1)  
                    block = (row // 3) * 3 + (col // 3)  
                    block_constraint = 243 + block * 9 + (num - 1)  
                    constraints = [cell_constraint, row_constraint, col_constraint, block_constraint]
                    
                    row_nodes = []
                    for constraint in constraints:
                        node = DLinksNode()  
                        node.row_id = self.total_rows  
                        node.col_id = constraint  
                        node.column = column_nodes[constraint]  
                        
                        last = column_nodes[constraint].up
                        node.up = last
                        node.down = column_nodes[constraint]
                        last.down = node
                        column_nodes[constraint].up = node
                        column_nodes[constraint].size += 1  
                        row_nodes.append(node)  
                    
                    for i in range(4):
                        row_nodes[i].right = row_nodes[(i + 1) % 4]  
                        row_nodes[i].left = row_nodes[(i - 1) % 4]  
                    
                    self.rows_data.append((row, col, num))
                    self.total_rows += 1  

    """ Удаление столбца и связанных строк """
    def _cover(self, column: DLinksNode):
        column.right.left = column.left
        column.left.right = column.right
        
        row = column.down
        while row != column:
            right_node = row.right
            while right_node != row:
                right_node.down.up = right_node.up
                right_node.up.down = right_node.down
                right_node.column.size -= 1 
                right_node = right_node.right  
            row = row.down  

    """ Восстановление столбца и связанных строк """
    def _uncover(self, column: DLinksNode):
        row = column.up
        while row != column:
            left_node = row.left
            while left_node != row:
                left_node.down.up = left_node
                left_node.up.down = left_node
                left_node.column.size += 1  
                left_node = left_node.left  
            row = row.up  
        column.right.left = column
        column.left.right = column

    """ Сам алгоритм Dancing Links """
    def _search(self, k: int, stats: dict) -> bool:
        stats['iterations'] += 1  
        if self.header.right == self.header:
            return True
        min_col = None
        min_size = float('inf')  
        col = self.header.right
        while col != self.header:  
            if col.size < min_size:  
                min_size = col.size
                min_col = col  
            col = col.right  
        if min_size == 0:
            return False
        self._cover(min_col)
        row = min_col.down
        while row != min_col:
            self.solution.append(row)
            self.solution_rows.append(row.row_id)
            right_node = row.right
            while right_node != row:
                self._cover(right_node.column)  
                right_node = right_node.right  
            if self._search(k + 1, stats):
                return True  
            self.solution.pop()
            self.solution_rows.pop()
            left_node = row.left
            while left_node != row:
                self._uncover(left_node.column)  
                left_node = left_node.left  
            row = row.down  
            stats['backtracks'] += 1  
        self._uncover(min_col)
        return False

    "Решение судоку"
    def solve(self, stats: dict) -> bool:
        return self._search(0, stats)  

    """ Преобразование решения """
    def get_solution_board(self) -> List[List[int]]:
        solution_board = [[0 for _ in range(9)] for _ in range(9)]  
        for row_id in self.solution_rows:
            row, col, num = self.rows_data[row_id]  
            solution_board[row][col] = num  
        return solution_board  

""" Запуск алгоритма Dancing Links """
def run_dancing_links_algorithm() -> dict:
    puzzle = [row[:] for row in ORIGINAL_PUZZLE]  
    stats = {'iterations': 0, 'backtracks': 0}  
    start_time = time.perf_counter()  
    solver = DancingLinksSolver(puzzle)  
    solved = solver.solve(stats)  
    elapsed = time.perf_counter() - start_time  
    solution = solver.get_solution_board() if solved else None  
    return {
        'algorithm': 'Dancing Links',
        'solved': solved,
        'time': elapsed,
        'iterations': stats['iterations'],
        'backtracks': stats['backtracks'],
        'solution': solution
    }



# Распараллеливание алгоритмов
""" Запуск всех алгоритмов параллельно """
def parallel_solve_algorithms() -> dict:
    algorithms = [
        ('Наивный перебор', run_naive_algorithm),
        ('Перебор с ограничениями', run_constrained_algorithm),
        ('Dancing Links', run_dancing_links_algorithm),
    ]
    start_time = time.perf_counter()  
    with ThreadPoolExecutor(max_workers=len(algorithms)) as executor:
        futures = {executor.submit(func): name for name, func in algorithms}
        for future in as_completed(futures):
            result = future.result()  
            if result['solved']:  
                elapsed = time.perf_counter() - start_time  
                result['time'] = elapsed  
                result['algorithm'] = f"Параллельный ({result['algorithm']})"  
                return result  
    elapsed = time.perf_counter() - start_time
    return {
        'algorithm': 'Параллельный (все алгоритмы)',
        'solved': False,
        'time': elapsed,
        'iterations': 0,
        'backtracks': 0,
        'solution': None
    }



# Проверка
""" Вывод решения судоку """
def print_sudoku(board: List[List[int]]):
    print("\n" + "="*25)  
    for i in range(9):  
        if i % 3 == 0 and i != 0:  
            print("-" * 25)  
        row_str = ""  
        for j in range(9):  
            if j % 3 == 0 and j != 0:  
                row_str += "| "  
            val = board[i][j] if board[i][j] != 0 else "."  
            row_str += f"{val} "  
        print(row_str)  
    print("="*25)  

""" Запуск алгоритмов и вывод результатов """
def test_all_algorithms():
    print("Исходное судоку:")  
    print_sudoku(ORIGINAL_PUZZLE)  
    print("\n" + "="*60)  
    print("ТЕСТИРОВАНИЕ АЛГОРИТМОВ")  
    print("="*60)  
    results = [
        run_naive_algorithm(),  
        run_constrained_algorithm(),  
        run_dancing_links_algorithm(),  
        parallel_solve_algorithms(),  
    ]
    for result in results:
        print(f"\n{'─'*60}")  
        print(f"Алгоритм: {result['algorithm']}")  
        print(f"{'─'*60}")  
        print(f"Решено: {'Да' if result['solved'] else 'Нет'}")  
        print(f"Время: {result['time']*1000:.2f} мс")  
        print(f"Итераций: {result['iterations']:,}".replace(",", " "))  
        print(f"Откатов: {result['backtracks']:,}".replace(",", " "))  
        if result['solved']:  
            print("Решение найдено")  
            print_sudoku(result['solution'])  
    

if __name__ == "__main__":
    test_all_algorithms()  