# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import random
from collections import deque
import math

# ────────────────────────────────БАЗОВОЕ БИНАРНОЕ ДЕРЕВО ПОИСКА (BST)────────────────────────────────

class BSTNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        
class BST:    
    def __init__(self):
        self.root = None
    
    # ────────────────────────────────ОПЕРАЦИЯ 1: ВСТАВКА (INSERT)────────────────────────────────
    
    def insert(self, key):
        """
        Вставить новый ключ в BST.
        Процесс:
        1. Если дерево пусто -> создаём корень
        2. Иначе -> рекурсивно ищем правое место
        """
        if self.root is None:
            self.root = BSTNode(key)
        else:
            self._insert_recursive(self.root, key)
    
    def _insert_recursive(self, node, key):
        """Рекурсивная вставка (внутренняя функция)"""
        if key < node.key:
            if node.left is None:
                node.left = BSTNode(key)
            else:
                self._insert_recursive(node.left, key)
        elif key > node.key:
            if node.right is None:
                node.right = BSTNode(key)
            else:
                self._insert_recursive(node.right, key)
    
    # ────────────────────────────────ОПЕРАЦИЯ 2: ПОИСК (SEARCH)────────────────────────────────
    
    def search(self, key):
        """
        Найти ключ в дереве.
        Параметры: key (int) - ищем этот ключ
        Возвращает: True если найден, False если нет
        """
        return self._search_recursive(self.root, key)
    
    def _search_recursive(self, node, key):
        """Рекурсивный поиск (внутренняя функция)"""
        if node is None:
            return False
        if key == node.key:
            return True
        elif key < node.key:
            return self._search_recursive(node.left, key)
        else:
            return self._search_recursive(node.right, key)
    
    # ────────────────────────────────ОПЕРАЦИЯ 3: УДАЛЕНИЕ (DELETE)────────────────────────────────
    
    def delete(self, key):
        """
        Удалить ключ из дерева.
        Обрабатывает 4 случая:
        1. Узел - лист -> просто удаляем
        2. Только левый потомок -> заменяем на него
        3. Только правый потомок -> заменяем на него
        4. Оба потомка -> находим в-во, копируем, удаляем в-во
        """
        self.root = self._delete_recursive(self.root, key)
    
    def _delete_recursive(self, node, key):
        """Рекурсивное удаление (внутренняя функция)"""
        if node is None:
            return node
        
        if key < node.key:
            node.left = self._delete_recursive(node.left, key)
        elif key > node.key:
            node.right = self._delete_recursive(node.right, key)
        else:
            # Нашли узел для удаления!
            if node.left is None and node.right is None:
                # СЛУЧАЙ 1: Лист
                return None
            elif node.left is None:
                # СЛУЧАЙ 2: Только правый
                return node.right
            elif node.right is None:
                # СЛУЧАЙ 3: Только левый
                return node.left
            else:
                # СЛУЧАЙ 4: Оба потомка
                min_node = self._find_min_node(node.right)
                node.key = min_node.key
                node.right = self._delete_recursive(node.right, min_node.key)
        
        return node

    # ────────────────────────────────ОПЕРАЦИЯ 4: МИНИМУМ И МАКСИМУМ────────────────────────────────
    
    def find_min(self):
        """Найти минимальное значение в дереве"""
        if self.root is None:
            return None
        return self._find_min_node(self.root).key
    
    def find_max(self):
        """Найти максимальное значение в дереве"""
        if self.root is None:
            return None
        node = self.root
        while node and node.right:
            node = node.right
        return node.key if node else None
    
    def _find_min_node(self, node):
        """Найти узел с минимальным ключом (внутренняя функция)"""
        while node.left:
            node = node.left
        return node
    
    # ────────────────────────────────ОПЕРАЦИЯ 5: ОБХОДЫ ДЕРЕВА────────────────────────────────
    
    def in_order(self):
        """
        Обход в порядке: ЛЕВОЕ -> УЗЕЛ -> ПРАВОЕ
        РЕЗУЛЬТАТ: отсортированный список
        Возвращает: список ключей в отсортированном порядке
        """
        result = []
        self._in_order_recursive(self.root, result)
        return result
    
    def _in_order_recursive(self, node, result):
        if node is not None:
            self._in_order_recursive(node.left, result)
            result.append(node.key)
            self._in_order_recursive(node.right, result)
    
    def pre_order(self):
        """Обход в порядке: УЗЕЛ -> ЛЕВОЕ -> ПРАВОЕ"""
        result = []
        self._pre_order_recursive(self.root, result)
        return result
    
    def _pre_order_recursive(self, node, result):
        if node is not None:
            result.append(node.key)
            self._pre_order_recursive(node.left, result)
            self._pre_order_recursive(node.right, result)
    
    def post_order(self):
        """Обход в порядке: ЛЕВОЕ → ПРАВОЕ → УЗЕЛ"""
        result = []
        self._post_order_recursive(self.root, result)
        return result
    
    def _post_order_recursive(self, node, result):
        if node is not None:
            self._post_order_recursive(node.left, result)
            self._post_order_recursive(node.right, result)
            result.append(node.key)
    
    def level_order(self):
        """Обход в ширину - по уровням"""
        if self.root is None:
            return []
        
        result = []
        queue = deque([self.root])
        
        while queue:
            node = queue.popleft()
            result.append(node.key)
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
        
        return result
    
    # ────────────────────────────────ОПЕРАЦИЯ 6: ВЫСОТА ДЕРЕВА────────────────────────────────
    
    def height(self):
        """
        Получить высоту дерева.
        - Пустое дерево: высота = 0
        - Формула: h(n) = 1 + max(h(left), h(right))
        """
        return self._height_recursive(self.root)
    
    def _height_recursive(self, node):
        if node is None:
            return 0
        return 1 + max(self._height_recursive(node.left), 
                       self._height_recursive(node.right))

# ────────────────────────────────РАЗДЕЛ 2: АВЛ ДЕРЕВО (AVL TREE)────────────────────────────────

class AVLNode:
    """Узел АВЛ дерева с дополнительным полем height"""
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    """
    Определение:
        Самобалансирующееся BST, где для каждого узла:
        |height(left) - height(right)| ≤ 1
    
    Гарантии: ВЫСОТА ВСЕГДА O(log n)!
    Коэффициент баланса: ≤ 1.44 * log₂(n+2) - 0.328 (по статистике сайтов)
    """
    
    def __init__(self):
        self.root = None
    
    def insert(self, key):
        """Вставить с автоматической балансировкой"""
        self.root = self._insert_recursive(self.root, key)
    
    def _insert_recursive(self, node, key):
        """Рекурсивная вставка с балансировкой"""
        
        # ШАГ 1: BST вставка
        if node is None:
            return AVLNode(key)
        if key < node.key:
            node.left = self._insert_recursive(node.left, key)
        elif key > node.key:
            node.right = self._insert_recursive(node.right, key)
        else:
            return node
        
        # ШАГ 2: Обновление высоты
        node.height = 1 + max(self._get_height(node.left), 
                              self._get_height(node.right))
        
        # ШАГ 3: Проверка баланса
        balance = self._get_balance(node)
        
        # ШАГ 4: Балансировка (4 типа дисбаланса)
        
        # Left-Left
        if balance > 1 and key < node.left.key:
            return self._rotate_right(node)
        
        # Right-Right
        if balance < -1 and key > node.right.key:
            return self._rotate_left(node)
        
        # Left-Right
        if balance > 1 and key > node.left.key:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        
        # Right-Left
        if balance < -1 and key < node.right.key:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        
        return node
    
    def delete(self, key):
        """Удалить с автоматической балансировкой"""
        self.root = self._delete_recursive(self.root, key)
    
    def _delete_recursive(self, node, key):
        """Рекурсивное удаление с балансировкой"""
        if node is None:
            return None
        
        if key < node.key:
            node.left = self._delete_recursive(node.left, key)
        elif key > node.key:
            node.right = self._delete_recursive(node.right, key)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                min_node = self._find_min_node(node.right)
                node.key = min_node.key
                node.right = self._delete_recursive(node.right, min_node.key)
        
        if node is None:
            return None
        
        # Обновление высоты
        node.height = 1 + max(self._get_height(node.left), 
                              self._get_height(node.right))
        
        # Балансировка
        balance = self._get_balance(node)
        
        if balance > 1 and self._get_balance(node.left) >= 0:
            return self._rotate_right(node)
        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._rotate_left(node)
        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        
        return node
    
    def _get_height(self, node):
        """Получить высоту узла"""
        if node is None:
            return 0
        return node.height
    
    def _get_balance(self, node):
        """Получить коэффициент баланса"""
        if node is None:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)
    
    def _rotate_right(self, z):
        """
        Правый поворот
        """
        y = z.left
        T2 = y.right
        
        y.right = z
        z.left = T2
        
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        
        return y
    
    def _rotate_left(self, x):
        """
        Левый поворот
        """
        y = x.right
        T2 = y.left
        
        y.left = x
        x.right = T2
        
        x.height = 1 + max(self._get_height(x.left), self._get_height(x.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        
        return y
    
    def _find_min_node(self, node):
        while node.left is not None:
            node = node.left
        return node
    
    def height(self):
        return self._get_height(self.root)
    
    def search(self, key):
        return self._search_recursive(self.root, key)
    
    def _search_recursive(self, node, key):
        if node is None:
            return False
        if key == node.key:
            return True
        elif key < node.key:
            return self._search_recursive(node.left, key)
        else:
            return self._search_recursive(node.right, key)
    
    def find_min(self):
        if self.root is None:
            return None
        return self._find_min_node(self.root).key
    
    def find_max(self):
        if self.root is None:
            return None
        node = self.root
        while node.right is not None:
            node = node.right
        return node.key
    
    # ────────────────────────────────МЕТОДЫ ОБХОДА ДЛЯ AVL────────────────────────────────
    
    def in_order(self):
        """Обход в порядке возрастания"""
        result = []
        self._in_order_recursive(self.root, result)
        return result
    
    def _in_order_recursive(self, node, result):
        if node is not None:
            self._in_order_recursive(node.left, result)
            result.append(node.key)
            self._in_order_recursive(node.right, result)
    
    def pre_order(self):
        """Обход в порядке: узел, левое, правое"""
        result = []
        self._pre_order_recursive(self.root, result)
        return result
    
    def _pre_order_recursive(self, node, result):
        if node is not None:
            result.append(node.key)
            self._pre_order_recursive(node.left, result)
            self._pre_order_recursive(node.right, result)
    
    def post_order(self):
        """Обход в порядке: левое, правое, узел"""
        result = []
        self._post_order_recursive(self.root, result)
        return result
    
    def _post_order_recursive(self, node, result):
        if node is not None:
            self._post_order_recursive(node.left, result)
            self._post_order_recursive(node.right, result)
            result.append(node.key)
    
    def level_order(self):
        """Обход в ширину"""
        if self.root is None:
            return []
        
        result = []
        queue = deque([self.root])
        
        while queue:
            node = queue.popleft()
            result.append(node.key)
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
        
        return result

# ────────────────────────────────РАЗДЕЛ 3: КРАСНО-ЧЁРНОЕ ДЕРЕВО────────────────────────────────

class RBNode:
    """Узел красно-чёрного дерева"""
    def __init__(self, key, color='RED'):
        self.key = key
        self.color = color
        self.left = None
        self.right = None
        self.parent = None


class RBTree:
    """
    Свойства дерева:
    1. Каждый узел - красный или чёрный
    2. Корень - чёрный
    3. Все листы (NIL) - чёрные
    4. Если узел красный → оба потомка чёрные
    5. Все пути содержат одинаковое количество чёрных узлов
    ВЫСОТА ≤ 2 * log₂(n+1)   
    """
    
    def __init__(self):
        self.NIL = RBNode(None, 'BLACK')
        self.root = self.NIL
    
    def insert(self, key):
        """Вставить с балансировкой"""
        new_node = RBNode(key, 'RED')
        new_node.left = self.NIL
        new_node.right = self.NIL
        self.root = self._bst_insert(self.root, new_node)
        self._fix_insert(new_node)
    
    def _bst_insert(self, root, node):
        """BST вставка для дерева"""
        if root == self.NIL:
            node.parent = None
            return node
        
        if node.key < root.key:
            root.left = self._bst_insert(root.left, node)
            root.left.parent = root
        else:
            root.right = self._bst_insert(root.right, node)
            root.right.parent = root
        
        return root
    
    def _fix_insert(self, node):
        """Исправить нарушения после вставки"""
        while node != self.root and node.parent.color == 'RED':
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                
                if uncle.color == 'RED':
                    node.parent.color = 'BLACK'
                    uncle.color = 'BLACK'
                    node.parent.parent.color = 'RED'
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self._left_rotate(node)
                    
                    node.parent.color = 'BLACK'
                    node.parent.parent.color = 'RED'
                    self._right_rotate(node.parent.parent)
            else:
                uncle = node.parent.parent.left
                
                if uncle.color == 'RED':
                    node.parent.color = 'BLACK'
                    uncle.color = 'BLACK'
                    node.parent.parent.color = 'RED'
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self._right_rotate(node)
                    
                    node.parent.color = 'BLACK'
                    node.parent.parent.color = 'RED'
                    self._left_rotate(node.parent.parent)
        
        self.root.color = 'BLACK'
    
    def _left_rotate(self, x):
        """Левый поворот"""
        y = x.right
        x.right = y.left
        
        if y.left != self.NIL:
            y.left.parent = x
        
        y.parent = x.parent
        
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        
        y.left = x
        x.parent = y
    
    def _right_rotate(self, x):
        """Правый поворот"""
        y = x.left
        x.left = y.right
        
        if y.right != self.NIL:
            y.right.parent = x
        
        y.parent = x.parent
        
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        
        y.right = x
        x.parent = y
    
    def delete(self, key):
        """Удалить ключ"""
        node = self._search_node(self.root, key)
        if node != self.NIL:
            self._delete_node(node)
    
    def _search_node(self, node, key):
        while node != self.NIL and node.key != key:
            if key < node.key:
                node = node.left
            else:
                node = node.right
        return node
    
    def _delete_node(self, node):
        """Удалить узел с балансировкой"""
        node_to_fix = None
        
        if node.left == self.NIL:
            node_to_fix = node.right
            self._transplant(node, node.right)
        elif node.right == self.NIL:
            node_to_fix = node.left
            self._transplant(node, node.left)
        else:
            successor = self._find_min_node(node.right)
            node_to_fix = successor.right
            
            if successor.parent == node:
                node_to_fix.parent = successor
            else:
                self._transplant(successor, successor.right)
                successor.right = node.right
                successor.right.parent = successor
            
            self._transplant(node, successor)
            successor.left = node.left
            successor.left.parent = successor
            successor.color = node.color
        
        if node.color == 'BLACK':
            self._fix_delete(node_to_fix)
    
    def _fix_delete(self, node):
        """Исправить нарушения после удаления"""
        while node != self.root and node.color == 'BLACK':
            if node == node.parent.left:
                sibling = node.parent.right
                
                if sibling.color == 'RED':
                    sibling.color = 'BLACK'
                    node.parent.color = 'RED'
                    self._left_rotate(node.parent)
                    sibling = node.parent.right
                
                if sibling.left.color == 'BLACK' and sibling.right.color == 'BLACK':
                    sibling.color = 'RED'
                    node = node.parent
                else:
                    if sibling.right.color == 'BLACK':
                        sibling.left.color = 'BLACK'
                        sibling.color = 'RED'
                        self._right_rotate(sibling)
                        sibling = node.parent.right
                    
                    sibling.color = node.parent.color
                    node.parent.color = 'BLACK'
                    sibling.right.color = 'BLACK'
                    self._left_rotate(node.parent)
                    node = self.root
            else:
                sibling = node.parent.left
                
                if sibling.color == 'RED':
                    sibling.color = 'BLACK'
                    node.parent.color = 'RED'
                    self._right_rotate(node.parent)
                    sibling = node.parent.left
                
                if sibling.right.color == 'BLACK' and sibling.left.color == 'BLACK':
                    sibling.color = 'RED'
                    node = node.parent
                else:
                    if sibling.left.color == 'BLACK':
                        sibling.right.color = 'BLACK'
                        sibling.color = 'RED'
                        self._left_rotate(sibling)
                        sibling = node.parent.left
                    
                    sibling.color = node.parent.color
                    node.parent.color = 'BLACK'
                    sibling.left.color = 'BLACK'
                    self._right_rotate(node.parent)
                    node = self.root
        
        node.color = 'BLACK'
    
    def _transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent
    
    def _find_min_node(self, node):
        while node.left != self.NIL:
            node = node.left
        return node
    
    def search(self, key):
        node = self._search_node(self.root, key)
        return node != self.NIL
    
    def find_min(self):
        if self.root == self.NIL:
            return None
        return self._find_min_node(self.root).key
    
    def find_max(self):
        if self.root == self.NIL:
            return None
        node = self.root
        while node.right != self.NIL:
            node = node.right
        return node.key
    
    def height(self):
        return self._get_height(self.root)
    
    def _get_height(self, node):
        if node == self.NIL:
            return 0
        return 1 + max(self._get_height(node.left), self._get_height(node.right))
    
    def set_colors(self, color_map):
        """
        color_map: словарь {ключ: 'RED' или 'BLACK'}
        """
        def dfs(node):
            if node == self.NIL:
                return
            if node.key in color_map:
                node.color = color_map[node.key]
            dfs(node.left)
            dfs(node.right)

        dfs(self.root)
        # self.root.color = 'BLACK'

    
    # ────────────────────────────────МЕТОДЫ ОБХОДА ДЛЯ RBTree────────────────────────────────
    
    def in_order(self):
        """Обход в порядке возрастания"""
        result = []
        self._in_order_recursive(self.root, result)
        return result
    
    def _in_order_recursive(self, node, result):
        if node != self.NIL:
            self._in_order_recursive(node.left, result)
            result.append(node.key)
            self._in_order_recursive(node.right, result)
    
    def pre_order(self):
        """Обход в порядке: узел, левое, правое"""
        result = []
        self._pre_order_recursive(self.root, result)
        return result
    
    def _pre_order_recursive(self, node, result):
        if node != self.NIL:
            result.append(node.key)
            self._pre_order_recursive(node.left, result)
            self._pre_order_recursive(node.right, result)
    
    def post_order(self):
        """Обход в порядке: левое, правое, узел"""
        result = []
        self._post_order_recursive(self.root, result)
        return result
    
    def _post_order_recursive(self, node, result):
        if node != self.NIL:
            self._post_order_recursive(node.left, result)
            self._post_order_recursive(node.right, result)
            result.append(node.key)
    
    def level_order(self):
        """Обход в ширину"""
        if self.root == self.NIL:
            return []
        
        result = []
        queue = deque([self.root])
        
        while queue:
            node = queue.popleft()
            if node != self.NIL:
                result.append(node.key)
                if node.left != self.NIL:
                    queue.append(node.left)
                if node.right != self.NIL:
                    queue.append(node.right)
        
        return result

# ────────────────────────────────ТЕСТИРОВАНИЕ────────────────────────────────

def experiment_tree_heights():
    """
    Экспериментальное исследование зависимости высоты деревьев от количества ключей
    """
    import sys
    sys.setrecursionlimit(50000)
    
    print("\n" + "="*70)
    print("Экспериментальное исследование высоты деревьев")
    print("="*70)
    
    sizes = list(range(1000, 10001, 200))  # 46 точек от 1000 до 10000
    
    # Результаты
    bst_heights = []
    avl_random_heights = []
    rb_random_heights = []
    avl_monotone_heights = []
    rb_monotone_heights = []
    
    print("Выполняем эксперименты...")
    for i, n in enumerate(sizes):
        if i % 5 == 0:
            print(f"Прогресс: {i*200} ключей...")
        
        # Случайные уникальные ключи
        random_keys = random.sample(range(1, n * 10), n)
        
        # BST
        bst = BST()
        for k in random_keys:
            bst.insert(k)
        bst_heights.append(bst.height())
        
        # AVL
        avl = AVLTree()
        for k in random_keys:
            avl.insert(k)
        avl_random_heights.append(avl.height())
        
        # RB
        rb = RBTree()
        for k in random_keys:
            rb.insert(k)
        rb_random_heights.append(rb.height())
        
        # Монотонные ключи
        monotone_keys = list(range(1, n + 1))
        
        # AVL монотонные
        avl_mono = AVLTree()
        for k in monotone_keys:
            avl_mono.insert(k)
        avl_monotone_heights.append(avl_mono.height())
        
        # RB монотонные
        rb_mono = RBTree()
        for k in monotone_keys:
            rb_mono.insert(k)
        rb_monotone_heights.append(rb_mono.height())
    
    # Теоретические оценки
    logn = [math.log2(n) for n in sizes]
    avl_upper = [1.44 * math.log2(n + 2) - 0.328 for n in sizes]
    rb_upper = [2 * math.log2(n + 1) for n in sizes]
    
    # ------------------------------------------------------------
    # ГРАФИК 1: BST при случайных ключах (только эксперимент и log₂(n))
    # ------------------------------------------------------------
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, bst_heights, 'b-', linewidth=2, label='BST (эксперимент)')
    plt.plot(sizes, logn, 'g:', linewidth=1, label='log₂(n)')
    
    plt.title('BST: высота при случайных ключах', fontsize=14)
    plt.xlabel('Количество ключей (n)', fontsize=12)
    plt.ylabel('Высота дерева (h)', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.ylim(0, max(bst_heights) * 1.2)
    plt.tight_layout()
    plt.show()
    
    # ------------------------------------------------------------
    # ГРАФИК 2: AVL и RB при случайных ключах (увеличенный масштаб)
    # ------------------------------------------------------------
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, avl_random_heights, 'g-', linewidth=2, label='AVL (эксперимент)')
    plt.plot(sizes, rb_random_heights, 'r-', linewidth=2, label='RB (эксперимент)')
    plt.plot(sizes, avl_upper, 'g--', linewidth=1.5, alpha=0.7, label='AVL: верхняя граница')
    plt.plot(sizes, rb_upper, 'r--', linewidth=1.5, alpha=0.7, label='RB: верхняя граница')
    plt.plot(sizes, logn, 'k:', linewidth=1, alpha=0.5, label='log₂(n) (нижняя граница)')
    
    plt.title('AVL и RB: случайные ключи', fontsize=14)
    plt.xlabel('Количество ключей (n)', fontsize=12)
    plt.ylabel('Высота дерева (h)', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Увеличиваем масштаб по вертикали в 1.5 раза
    y_max = max(max(avl_random_heights), max(rb_random_heights), max(avl_upper), max(rb_upper)) * 1.5
    plt.ylim(0, y_max)
    plt.tight_layout()
    plt.show()
    
    # ------------------------------------------------------------
    # ГРАФИК 3: AVL и RB при монотонных ключах
    # ------------------------------------------------------------
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, avl_monotone_heights, 'g-', linewidth=2, label='AVL (монотонные)')
    plt.plot(sizes, rb_monotone_heights, 'r-', linewidth=2, label='RB (монотонные)')
    plt.plot(sizes, avl_upper, 'g--', linewidth=1.5, alpha=0.7, label='AVL: верхняя граница')
    plt.plot(sizes, rb_upper, 'r--', linewidth=1.5, alpha=0.7, label='RB: верхняя граница')
    plt.plot(sizes, logn, 'k:', linewidth=1, alpha=0.5, label='log₂(n) (нижняя граница)')
    
    plt.title('AVL и RB: монотонно возрастающие ключи', fontsize=14)
    plt.xlabel('Количество ключей (n)', fontsize=12)
    plt.ylabel('Высота дерева (h)', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    y_max_mono = max(max(avl_monotone_heights), max(rb_monotone_heights)) * 1.5
    plt.ylim(0, y_max_mono)
    plt.tight_layout()
    plt.show()

def test_trees():
    """Демонстрация работы всех трёх деревьев"""
    print("\n" + "="*70)
    print("ДЕМОНСТРАЦИЯ РАБОТЫ ДЕРЕВЬЕВ")
    print("="*70)
    
    keys = [100, 50, 200, 25, 75, 60, 80, 55, 65, 53, 58]
    
    print("\n БИНАРНОЕ ДЕРЕВО ПОИСКА (BST)")
    print("-" * 70)
    bst = BST()
    for key in keys:
        bst.insert(key)
    
    print(f"In-order (отсортировано): {bst.in_order()}")
    print(f"Pre-order: {bst.pre_order()}")
    print(f"Post-order: {bst.post_order()}")
    print(f"Level-order: {bst.level_order()}")
    print(f"Высота: {bst.height()}")
    print(f"Минимум: {bst.find_min()}, Максимум: {bst.find_max()}")
    print(f"Поиск 35: {bst.search(35)}, Поиск 100: {bst.search(100)}")
    
    print("\n АВЛ ДЕРЕВО")
    print("-" * 70)
    avl = AVLTree()
    for key in keys:
        avl.insert(key)
    
    print(f"Высота АВЛ: {avl.height()}")
    print(f"In-order: {avl.in_order()}")
    print(f"Pre-order: {avl.pre_order()}")
    print(f"Поиск 35: {avl.search(35)}, Поиск 100: {avl.search(100)}")
    
    print("\n КРАСНО-ЧЁРНОЕ ДЕРЕВО")
    print("-" * 70)
    rb = RBTree()  # ← СОЗДАЁМ СНАЧАЛА
    for key in keys:
        rb.insert(key)
    
    # ← ПОТОМ УСТАНАВЛИВАЕМ ЦВЕТА
    color_map = {
        100: 'BLACK',
        50:  'RED',
        200: 'BLACK',
        25:  'BLACK',
        75:  'BLACK',
        60:  'RED',
        80:  'RED',
        55:  'BLACK',
        65:  'BLACK',
        53:  'BLACK',
        58:  'BLACK',
    }
    rb.set_colors(color_map)
    
    print(f"Высота РБ: {rb.height()}")
    print(f"In-order: {rb.in_order()}")
    print(f"Минимум: {rb.find_min()}, Максимум: {rb.find_max()}")
    print(f"Поиск 35: {rb.search(35)}, Поиск 100: {rb.search(100)}")
    
    print("\n" + "="*70)
    print("ОПЕРАЦИЯ УДАЛЕНИЯ (BST)")
    print("-" * 70)
    print(f"До удаления 40 (BST): {bst.in_order()}")
    bst.delete(40)
    print(f"После удаления 40 (BST): {bst.in_order()}")
    print(f"Поиск 40 (BST): {bst.search(40)}")

    print("\n" + "="*70)
    print("ОПЕРАЦИЯ УДАЛЕНИЯ (RBTree)")
    print("-" * 70)
    print(f"До удаления 50 (RB): {rb.in_order()}")
    rb.delete(50)
    print(f"После удаления 50 (RB): {rb.in_order()}")
    print(f"Поиск 50 (RB): {rb.search(50)}")

if __name__ == "__main__":
    # Демонстрация работы деревьев
    test_trees()
    
    # Экспериментальное исследование высоты деревьев
    experiment_tree_heights()