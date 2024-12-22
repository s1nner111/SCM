import yaml
import argparse
import re

class ConfigTranslator:
    def __init__(self):
        self.constants = {}  # Сохраняем константы, заданные на этапе трансляции

    def translate(self, data):
        if isinstance(data, dict):
            return self.translate_dict(data)
        elif isinstance(data, list):
            return self.translate_list(data)
        elif isinstance(data, str):
            return self.translate_value(data)
        elif isinstance(data, int) or isinstance(data, float):
            return str(data)
        else:
            raise ValueError(f"Unsupported data type: {type(data)}")

    def translate_dict(self, data):
        result = "struct {\n"
        for key, value in data.items():
            if re.match(r"^[a-zA-Z][_a-zA-Z0-9]*$", key):
                result += f"  {key} = {self.translate(value)},\n"
            else:
                raise ValueError(f"Invalid key name: {key}")
        result = result.rstrip(",\n") + "\n}"  # Удаляем последнюю запятую
        return result

    def translate_list(self, data):
        return f"[ {' '.join(self.translate(value) for value in data)} ]"

    def translate_value(self, value):
        # Проверяем, является ли значение ссылкой на константу
        if value.startswith("$") and value[1:] in self.constants:
            return str(self.constants[value[1:]])
        # Проверяем, является ли это объявлением константы
        if ":" in value:
            name, const_value = value.split(":", 1)
            if re.match(r"^[a-zA-Z][_a-zA-Z0-9]*$", name.strip()):
                self.constants[name.strip()] = const_value.strip()
                return ""
            else:
                raise ValueError(f"Invalid constant name: {name}")
        return value

    def parse_comments(self, text):
        return f"(comment\n{text}\n)"

def main():
    parser = argparse.ArgumentParser(description="YAML to Educational Config Language Converter")
    parser.add_argument("input_file", help="Path to the input YAML file")
    parser.add_argument("output_file", help="Path to the output file")
    args = parser.parse_args()

    # Отладочная информация
    print(f"Reading YAML file: {args.input_file}")
    print(f"Output will be saved to: {args.output_file}")

    # Читаем YAML-файл
    try:
        with open(args.input_file, "r") as file:
            yaml_data = yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Error: Input file '{args.input_file}' not found.")
        return
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML format in file '{args.input_file}': {e}")
        return

    translator = ConfigTranslator()

    # Переводим данные
    try:
        print("Translating YAML to Educational Config Language...")
        result = translator.translate(yaml_data)
    except ValueError as e:
        print(f"Error during translation: {e}")
        return

    # Сохраняем результат в выходной файл
    try:
        with open(args.output_file, "w") as file:
            file.write(result)
        print("Translation completed successfully.")
    except Exception as e:
        print(f"Error while writing to output file '{args.output_file}': {e}")

if __name__ == "__main__":
    main()
