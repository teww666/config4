import struct
import xml.etree.ElementTree as ET
import sys

def assemble(input_file, output_file, log_file):
    # Парсим XML-файл
    tree = ET.parse(input_file)
    root = tree.getroot()

    binary_output = bytearray()
    log_root = ET.Element("Log")

    for instruction in root.findall("Instruction"):
        command = instruction.find("Command").text.upper()
        a = int(instruction.find("A").text)
        b = int(instruction.find("B").text)

        if command == "LOAD":
            opcode = 0x49
        elif command == "READ":
            opcode = 0xDD
        elif command == "WRITE":
            opcode = 0x94
        elif command == "POPCNT":
            opcode = 0x83
        else:
            raise ValueError(f"Unknown command: {command}")

        # Формируем команду
        instruction_code = (opcode & 0xFF) | ((b & 0xFFFFFF) << 8)
        binary_output.extend(struct.pack("<I", instruction_code))

        # Логирование
        instruction_element = ET.SubElement(log_root, "Instruction")
        ET.SubElement(instruction_element, "Command").text = command
        ET.SubElement(instruction_element, "A").text = str(a)
        ET.SubElement(instruction_element, "B").text = str(b)
        ET.SubElement(instruction_element, "Hex").text = "0x" + "".join(f"{byte:02X}" for byte in struct.pack("<I", instruction_code))

    # Сохраняем бинарный файл
    with open(output_file, "wb") as f:
        f.write(binary_output)

    # Сохраняем лог-файл
    tree = ET.ElementTree(log_root)
    tree.write(log_file, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python assembler.py <input_file> <output_file> <log_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    log_file = sys.argv[3]

    assemble(input_file, output_file, log_file)
    print(f"Assembly completed. Binary file: {output_file}, Log file: {log_file}")
