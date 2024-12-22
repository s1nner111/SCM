import graphviz

# Задайте параметры здесь
PACKAGE_NAME = "example_package"
MAX_DEPTH = 2

# Пример зависимостей для демонстрации (замените на реальные данные, если нужно)
EXAMPLE_DEPENDENCIES = {
    "example_package": ["dependency1", "dependency2"],
    "dependency1": ["sub_dependency1", "sub_dependency2"],
    "dependency2": ["sub_dependency3"],
    "sub_dependency1": [],
    "sub_dependency2": [],
    "sub_dependency3": []
}

# Функция для получения зависимостей пакета из предопределённого словаря
def get_dependencies(package_name, depth, current_depth=0, visited=None):
    if visited is None:
        visited = set()

    # Остановка на максимальной глубине
    if current_depth >= depth:
        return []

    # Проверяем, есть ли пакет в словаре зависимостей
    if package_name not in EXAMPLE_DEPENDENCIES:
        print(f"Warning: {package_name} not found in dependencies.")
        return []

    dependencies = EXAMPLE_DEPENDENCIES[package_name]

    all_dependencies = []
    for dep in dependencies:
        if dep not in visited:
            visited.add(dep)
            all_dependencies.append(dep)
            all_dependencies.extend(
                get_dependencies(dep, depth, current_depth + 1, visited)
            )

    return all_dependencies

# Функция для построения графа зависимостей с использованием Graphviz
def build_dependency_graph(package_name, dependencies):
    dot = graphviz.Digraph(format="png")
    dot.node(package_name, package_name)  # Добавляем узел для основного пакета

    for dep in dependencies:
        dot.node(dep, dep)  # Добавляем узел для каждой зависимости
        dot.edge(package_name, dep)  # Создаем ребро между пакетом и зависимостью

    return dot

# Главная функция для выполнения программы
def main():
    print(f"Анализируем зависимости для пакета: {PACKAGE_NAME}")

    # Получаем зависимости
    dependencies = get_dependencies(PACKAGE_NAME, MAX_DEPTH)

    if not dependencies:
        print("Не удалось получить зависимости или их нет.")
        return

    # Строим граф зависимостей
    dot = build_dependency_graph(PACKAGE_NAME, dependencies)

    # Сохраняем или отображаем граф
    output_file = "dependency_graph.png"
    dot.render(output_file, view=True)  # Сохраняем изображение и сразу открываем его

    print(f"Граф зависимостей сгенерирован: {output_file}")

if __name__ == "__main__":
    main()
