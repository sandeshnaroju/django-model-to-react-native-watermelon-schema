import sys
import re


def remove_all_imports(f):
    classes_lines = []
    for line in f.readlines():
        line = remove_spaces(line)
        if not line.startswith("return") and not line.startswith("def") and not line.startswith(
                "import") and not line.startswith("from") and not len(line.strip()) == 0:
            classes_lines.append(line)
    return classes_lines


def count_classes(lines):
    count = 0
    for line in lines:
        if line.startswith("class"):
            count = count + 1
    return count


def remove_spaces(line):
    return line.replace(" ", "")


def get_model_name(line):
    line = remove_spaces(line)
    line = line.strip("class")
    line = remove_spaces(line)
    index = line.index("(")
    return line[:index]


def get_column(line):
    line = line.replace("models.", "")
    index1 = line.index("=")
    name = line[:index1]
    index2 = line.index("(")
    type = line[index1 + 1:index2]
    type = get_column_type(type)
    obj = {
        "name": name,
        "type": type
    }
    return obj


def get_column_type(type):
    if type == "UUIDField" or type == "ForeignKey" or type == "FloatField" or type == "IntegerField":
        return "number"
    elif type == "DateTimeField" or type == "TextField" or type == "CharField":
        return "string"
    elif type == "BooleanField":
        return "boolean"
    else:
        return "string"


def camel_case_to_snake_case(string):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', string).lower()


def create_table_schema(name, columns):
    object = {
        "name": camel_case_to_snake_case(name) + 's',
        "columns": columns
    }
    return 'tableSchema (' + str(object) + ')'


def remove_quotes(string):
    string = string.replace("\'name\':", "name:")
    string = string.replace("\'type\':", "type:")
    string = string.replace("\'tables\':", "tables:")
    string = string.replace("\"", "")
    return string


def add_imports(string):
    return "import {appSchema, tableSchema} from '@nozbe/watermelondb'\n" + 'export default appSchema(' + str(
        string) + ')'


def create_appschema(f):
    lines = remove_all_imports(f)
    if len(lines) == 0:
        print("file is empty")
        return
    model = 0
    name = ""
    columns = []
    tables = []
    for line in lines:
        if line.startswith("class"):  # detected class
            if model > 0:
                tables.append(create_table_schema(name, columns))
                columns = []
            name = get_model_name(line)
            model = 1
        else:
            columns.append(get_column(line))
    if model == 1:
        if model > 0:
            tables.append(create_table_schema(name, columns))
    schema = {
        'version': 1,
        'tables': tables
    }
    string = add_imports(schema)
    return remove_quotes(string)


if __name__ == "__main__":
    try:
        path = sys.argv[1]
        if path:
            f = open(path, "r")
            data = create_appschema(f)
            with open("schema.js", "w") as outfile:
                outfile.write(data)
        else:
            print("Provide models.py path as first argument")
    except Exception:
        print("Provide models.py as first argument")
