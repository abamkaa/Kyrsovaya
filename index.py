import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk

def run_syntax_analyzer(file_path):
    """Вызов C++ программы для синтаксического анализа."""
    try:
        result = subprocess.run(
            ["/Users/vasilij/Downloads/syntax_analizer/application/mainsa", file_path],
            text=True,
            capture_output=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Ошибка", e.stderr)
        return ""

def parse_output(output):
    """Парсинг вывода C++ программы."""
    lexemes_table = []
    tree_lines = []
    tree_started = False

    for line in output.strip().split("\n"):
        if line.startswith("TREE:"):
            tree_started = True
            tree_lines.append(line[5:])  # Убираем "TREE:" и сохраняем строку дерева
        elif tree_started:
            tree_lines.append(line)  # Сохраняем последующие строки дерева
        else:
            parts = line.split(",", 2)
            if len(parts) == 3:
                line_number, token_type, value = parts
                lexemes_table.append({
                    '№': line_number,
                    'Тип': token_type,
                    'Значение': value
                })

    tree = "\n".join(tree_lines)  # Собираем дерево в виде строки
    print("DEBUG Tree Output:\n", tree)  # Отладочный вывод
    return lexemes_table, tree

def open_file_and_analyze():
    """Выбор файла и анализ."""
    file_path = filedialog.askopenfilename(title="Выберите файл для анализа", filetypes=[("Text Files", "*.txt")])
    if file_path:
        try:
            # Открытие и отображение содержимого файла
            with open(file_path, 'r', encoding='utf-8') as file:
                file_content = file.read()
                file_content_text.delete(1.0, tk.END)  # Очистка текстового поля
                file_content_text.insert(tk.END, file_content)  # Вставка содержимого файла

            # Вызов C++ программы для анализа
            output = run_syntax_analyzer(file_path)
            if output:
                lexemes_table, tree = parse_output(output)
                display_lexemes_in_table(lexemes_table)
                display_parse_tree(tree)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть файл: {e}")
    else:
        messagebox.showwarning("Файл не выбран", "Пожалуйста, выберите файл для анализа.")

def display_lexemes_in_table(lexemes_table):
    """Отображение таблицы лексем в Treeview."""
    for item in result_table.get_children():
        result_table.delete(item)

    for lexeme in lexemes_table:
        result_table.insert("", "end", values=(lexeme['№'], lexeme['Тип'], lexeme['Значение']))

def display_parse_tree(tree):
    """Отображение дерева синтаксического разбора."""
    parse_tree_text.delete(1.0, tk.END)
    parse_tree_text.insert(tk.END, tree)
    
# Интерфейс tkinter
root = tk.Tk()
root.title("Синтаксический анализатор")
root.geometry("1200x500")

# Основной фрейм для горизонтального разделения
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

# Левый фрейм для выбора файла и отображения его содержимого
left_frame = tk.Frame(main_frame)
left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

# Кнопка для выбора файла
select_file_button = tk.Button(left_frame, text="Выбрать файл для анализа", command=open_file_and_analyze)
select_file_button.pack(pady=5)

# Поле для отображения содержимого файла
file_content_label = tk.Label(left_frame, text="Содержимое файла:")
file_content_label.pack(anchor="w")
file_content_text = scrolledtext.ScrolledText(left_frame, wrap=tk.WORD, width=40, height=20)
file_content_text.pack(pady=5, fill="both", expand=True)

# Средний фрейм для таблицы лексем
middle_frame = tk.Frame(main_frame)
middle_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

# Таблица для отображения результата анализа
result_label = tk.Label(middle_frame, text="Результаты лексического анализа:")
result_label.pack(anchor="w")
columns = ("№", "Тип", "Значение")
result_table = ttk.Treeview(middle_frame, columns=columns, show="headings")
result_table.heading("№", text="№")
result_table.heading("Тип", text="Тип")
result_table.heading("Значение", text="Значение")
result_table.column("№", width=50, anchor="center")
result_table.column("Тип", width=150, anchor="center")
result_table.column("Значение", width=150, anchor="center")

# Прокрутка для таблицы
scrollbar = ttk.Scrollbar(middle_frame, orient="vertical", command=result_table.yview)
result_table.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")
result_table.pack(pady=5, fill="both", expand=True)

# Правый фрейм для дерева синтаксического разбора
right_frame = tk.Frame(main_frame)
right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

# Поле для отображения дерева разбора
parse_tree_label = tk.Label(right_frame, text="Дерево синтаксического разбора:")
parse_tree_label.pack(anchor="w")
parse_tree_text = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, width=40, height=20)
parse_tree_text.pack(pady=5, fill="both", expand=True)

# Запуск интерфейса
root.mainloop()
