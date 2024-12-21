import xml.etree.ElementTree as ET
import sys
import argparse
import re
import math

NAME_REGEX = r"^[_a-zA-Z]\w*$"
EXPRESSION_REGEX = r"^@\[([+-])(\s*[a-zA-Z_]\w*\s*)(\s*[\d.]+\s*)(?:\s*pow\(\s*(\d+)\s*\))?\]$"
MULTILINE_COMMENT_REGEX = r'/\+(.*?)\+/'
SINGLE_LINE_COMMENT_REGEX = r'\\(.*?)$'

def process_xml(xml_data):
    try:
        comments = re.findall(MULTILINE_COMMENT_REGEX, xml_data, flags=re.DOTALL)
        single_line_comments = re.findall(SINGLE_LINE_COMMENT_REGEX, xml_data, re.MULTILINE)
        xml_data = re.sub(MULTILINE_COMMENT_REGEX, '', xml_data, flags=re.DOTALL)
        xml_data = re.sub(SINGLE_LINE_COMMENT_REGEX, '', xml_data, flags=re.MULTILINE)
        root = ET.fromstring(xml_data)
    except ET.ParseError as e:
        raise ValueError(f"Ошибка парсинга XML: {e}")

    constants = {}
    dictionaries = {}
    values = []

    for element in root:
        if element.tag == "constant":
            name = element.get("name")
            if not re.match(NAME_REGEX, name):
                raise ValueError(f"Некорректное имя константы: {name}")
            value_str = element.text.strip()
            try:
                value = float(value_str)
            except ValueError:
                value = value_str
            constants[name] = value
        elif element.tag == "dictionary":
            name = element.get("name")
            if not re.match(NAME_REGEX, name):
                raise ValueError(f"Некорректное имя словаря: {name}")
            items = {}
            for item in element:
                key = item.get("key")
                value_str = item.text.strip()
                try:
                    value = float(value_str)
                except ValueError:
                    value = value_str
                items[key] = value
            dictionaries[name] = items
        elif element.tag == "value":
            values.append(element.text.strip())

    output = ""
    for comment in comments:
        output += f"<# {comment.strip()} #>\n"
    for comment in single_line_comments:
        output += f"<# {comment.strip()} #>\n"
    for name, value in constants.items():
        output += f"{name} is {value}\n"

    for name, items in dictionaries.items():
        output += f"{{ {name} = {{\n"
        for key, value in items.items():
            output += f"  {key} = {value},\n"
        output += "}}\n"

    for value in values:
        try:
            val = float(value)
            output += f"{val}\n"
        except ValueError:
            match = re.match(EXPRESSION_REGEX, value)
            if match:
                op, name, num_str, pow_str = match.groups()
                pow_str = int(pow_str) if pow_str else 1
                name = name.strip()
                try:
                  num = float(num_str.strip())
                except ValueError:
                  raise ValueError(f"Некорректное число в выражении: {num_str}")
                result = constants.get(name, 0)

                if op == '+':
                    result += num
                elif op == '-':
                    result -= num

                result = math.pow(result, pow_str)
                output += f"{result}\n"
            else:
                output += f"{value}\n"

    return output


def main():
    parser = argparse.ArgumentParser(description='Конвертер XML в конфигурационный язык')
    parser.add_argument('output_file', help='Путь к выходному файлу')
    args = parser.parse_args()

    xml_data = sys.stdin.read()
    try:
        with open("input.xml", "r", encoding="utf-8") as f:  # Чтение из файла
            xml_data = f.read()
        output_data = process_xml(xml_data)
        with open(args.output_file, 'w', encoding="utf-8") as f:
            f.write(output_data)
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()