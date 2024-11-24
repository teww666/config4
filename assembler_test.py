import struct
import os
import subprocess

def test_assembler():
    # Создаём тестовый входной XML-файл
    input_xml = "test_program.xml"
    output_bin = "test_program.bin"
    log_xml = "test_log.xml"

    with open(input_xml, "w", encoding="utf-8") as f:
        f.write("""<?xml version="1.0" encoding="utf-8"?>
<Program>
    <Instruction>
        <Command>LOAD</Command>
        <A>73</A>
        <B>898</B>
    </Instruction>
    <Instruction>
        <Command>READ</Command>
        <A>221</A>
        <B>939</B>
    </Instruction>
    <Instruction>
        <Command>WRITE</Command>
        <A>148</A>
        <B>739</B>
    </Instruction>
    <Instruction>
        <Command>POPCNT</Command>
        <A>131</A>
        <B>550</B>
    </Instruction>
</Program>
""")

    # Запускаем ассемблер
    try:
        subprocess.run(
            ["python", "assembler.py", input_xml, output_bin, log_xml],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при работе ассемблера: {e}")
        return

    # Проверяем бинарный файл
    expected_output = [
        (0x49, 0x82, 0x03, 0x00),  # LOAD 73, 898
        (0xDD, 0xAB, 0x03, 0x00),  # READ 221, 939
        (0x94, 0xE3, 0x02, 0x00),  # WRITE 148, 739
        (0x83, 0x26, 0x02, 0x00),  # POPCNT 131, 550
    ]

    with open(output_bin, "rb") as f:
        binary_data = f.read()

    actual_output = [
        struct.unpack("<I", binary_data[i:i + 4])[0]
        for i in range(0, len(binary_data), 4)
    ]

    # Преобразуем ожидаемые данные для сравнения
    expected_data = [
        int.from_bytes(bytearray(cmd), byteorder="little")
        for cmd in expected_output
    ]

    # Форматируем данные в шестнадцатеричном формате
    expected_hex = [f"0x{value:08X}" for value in expected_data]
    actual_hex = [f"0x{value:08X}" for value in actual_output]

    # Всегда выводим ожидаемое и фактическое
    print(f"Expected: {expected_hex}")
    print(f"Actual:   {actual_hex}")

    # Проверка результата
    if actual_output == expected_data:
        print("Тест успешен")
    else:
        print("Тест провален!")

    # Удаляем тестовые файлы после проверки
    os.remove(input_xml)
    os.remove(output_bin)
    os.remove(log_xml)

if __name__ == "__main__":
    test_assembler()
