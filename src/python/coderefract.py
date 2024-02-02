def extract_function_info(code):
    file_info_refract = ""
    # split code into lines
    lines = code.split('\n')

    # variables to store func info
    functions = {}
    current_function = None

    # track the function body
    inside_function_body = False
    inside_if_block = False

    for line in lines:
        if line.strip().startswith("fn"):
            if current_function is not None:
                functions[current_function['name']] = current_function

            function_declaration = line.strip().split("(")
            current_function = {
                'name': function_declaration[0][3:].strip(),
                'input_params': function_declaration[1].split(")")[0].strip(),
                'body_variables': {},
                'return_statements': []
            }

            inside_function_body = True

        elif inside_function_body and ("=" in line or ":" in line):
            parts = line.strip().replace(";", "").split("=" if "=" in line else ":")
            var_name = parts[0].strip()
            var_type = parts[1].strip() if len(parts) == 2 else "unknown"
            current_function['body_variables'][var_name] = var_type

        elif inside_function_body and line.strip().startswith("if"):
            inside_if_block = True

        elif inside_function_body and line.strip().startswith("else"):
            inside_if_block = False

        elif inside_function_body and line.strip().startswith("return"):
            current_function['return_statements'].append(line.strip())

    if current_function is not None:
        functions[current_function['name']] = current_function

    for func_name, func_info in functions.items():
        file_info_refract += f"Function Name: {func_info['name']}\n"
        file_info_refract += f"Input parameter/variables: {func_info['input_params']}\n"
        file_info_refract += "Variables in body:\n"
        for var, var_type in func_info['body_variables'].items():
            file_info_refract += f"  {var}: {var_type}\n"

        file_info_refract += "Return statements:\n"
        for statement in func_info['return_statements']:
            file_info_refract += f"  {statement}\n"
        file_info_refract += "\n"

    return file_info_refract

file_path = 'test4.rs'
with open(file_path, 'r') as file:
    file_content = file.read()

extract_function_info(file_content)

# print(extract_function_info(file_content))
