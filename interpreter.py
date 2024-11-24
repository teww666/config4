import struct
import xml.etree.ElementTree as ET
import sys

def interpret(binary_file, output_file, memory_range):
    # Инициализация памяти с тестовыми данными
    memory = [5, 10, 20, 40, 80, 160] + [0] * (1024 - 6)
    print("Начальная память:", memory[:6])  # Для проверки

    with open(binary_file, "rb") as f:
        binary_data = f.read()

    memory_range_start, memory_range_end = map(int, memory_range.split("-"))

    # Создаем корневой элемент XML
    root = ET.Element("Output")

    # Интерпретация инструкций
    for i in range(0, len(binary_data), 4):
        instruction = struct.unpack("<I", binary_data[i:i + 4])[0]
        opcode = instruction & 0xFF
        b = (instruction >> 8) & 0xFFFFFF

        print(f"Выполняем инструкцию: opcode=0x{opcode:02X}, B={b}")
        print(f"Память до выполнения команды: {memory[:6]}")

        if opcode == 0x49:  # LOAD
            accumulator = b
        elif opcode == 0xDD:  # READ
            accumulator = memory[b]
        elif opcode == 0x94:  # WRITE
            memory[b] = accumulator
        elif opcode == 0x83:  # POPCNT
            memory[b] = bin(memory[b]).count("1")
        else:
            raise ValueError(f"Unknown opcode: {opcode}")

        print(f"Память после выполнения команды: {memory[:6]}")

    # Записываем указанный диапазон памяти в XML
    for addr in range(memory_range_start, memory_range_end + 1):
        memory_element = ET.SubElement(root, "Memory")
        ET.SubElement(memory_element, "Address").text = str(addr)
        ET.SubElement(memory_element, "Value").text = str(memory[addr])

    # Генерация XML с нужным форматом
    xml_string = ET.tostring(root, encoding="utf-8").decode("utf-8")
    xml_string = xml_string.replace("><", ">\n<")  # Добавляем переносы строк между элементами

    # Сохраняем XML в файл
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(xml_string)

    print(f"Interpretation completed. Result saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python interpreter.py <binary_file> <output_file> <memory_range>")
        sys.exit(1)

    binary_file = sys.argv[1]
    output_file = sys.argv[2]
    memory_range = sys.argv[3]

    interpret(binary_file, output_file, memory_range)
