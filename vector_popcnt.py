import subprocess
import os

def create_program_xml(file_name):
    """
    Создаёт XML-файл с программой, которая выполняет popcnt() для каждого элемента вектора.
    """
    with open(file_name, "w", encoding="utf-8") as f:
        f.write("""<?xml version="1.0" encoding="utf-8"?>
<Program>
    <Instruction>
        <Command>POPCNT</Command>
        <A>0</A>
        <B>0</B>
    </Instruction>
    <Instruction>
        <Command>POPCNT</Command>
        <A>0</A>
        <B>1</B>
    </Instruction>
    <Instruction>
        <Command>POPCNT</Command>
        <A>0</A>
        <B>2</B>
    </Instruction>
    <Instruction>
        <Command>POPCNT</Command>
        <A>0</A>
        <B>3</B>
    </Instruction>
    <Instruction>
        <Command>POPCNT</Command>
        <A>0</A>
        <B>4</B>
    </Instruction>
    <Instruction>
        <Command>POPCNT</Command>
        <A>0</A>
        <B>5</B>
    </Instruction>
</Program>
""")

def run_vector_popcnt():
    """
    Выполняет всю цепочку: генерация программы, сборка, интерпретация и вывод результата.
    """
    program_xml = "vector_popcnt_program.xml"
    program_bin = "vector_popcnt.bin"
    program_log = "vector_popcnt_log.xml"
    result_xml = "vector_popcnt_test.xml"

    # Создаём программу
    create_program_xml(program_xml)

    # Запускаем ассемблер
    subprocess.run(["python", "assembler.py", program_xml, program_bin, program_log], check=True)

    # Запускаем интерпретатор
    subprocess.run(["python", "interpreter.py", program_bin, result_xml, "0-5"], check=True)

    # Сообщение об успешном выполнении
    print(f"Программа успешно выполнена. Результаты сохранены в {result_xml}")

    # Удаляем временные файлы, кроме результата
    os.remove(program_xml)
    os.remove(program_bin)
    os.remove(program_log)

if __name__ == "__main__":
    run_vector_popcnt()
