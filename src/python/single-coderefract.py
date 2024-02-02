def extract_function_info(code):
    file_info_refract = ""
    # split code into lines
    lines = code.split('\n')

    # variables to store func info
    function_name = None
    input_params = None
    body_variables = {}
    return_statements = []

    # track the function body
    inside_function_body = False
    inside_if_block = False

    for line in lines:
        if line.strip().startswith("fn"):
            function_declaration = line.strip().split("(")
            function_name = function_declaration[0][3:].strip()
            input_params = function_declaration[1].split(")")[0].strip()

            inside_function_body = True

        elif inside_function_body and line.strip().startswith("var"):
            variable_declaration = line.strip().split(";")[0].split(" ")
            var_name = variable_declaration[1].strip()
            var_type = variable_declaration[2].strip() if len(variable_declaration) == 3 else "unknown"
            body_variables[var_name] = var_type

        elif inside_function_body and line.strip().startswith("if"):
            inside_if_block = True

        elif inside_function_body and line.strip().startswith("else"):
            inside_if_block = False

        elif inside_function_body and line.strip().startswith("return"):
            return_statements.append(line.strip())

    file_info_refract += f"Function Name: {function_name}\n"
    file_info_refract += f"Input parameter/variable: {input_params}\n"
    file_info_refract += "Variables in body:\n"
    for var, var_type in body_variables.items():
        file_info_refract += f"  {var}: {var_type}\n"
    
    file_info_refract += "Return statements:\n"
    for statement in return_statements:
        file_info_refract += f"  {statement}\n"

    # print(file_info_refract)
    return file_info_refract


file_path = 'test4.rs'
with open(file_path, 'r') as file:
    file_content = file.read()

extract_function_info(file_content)




# print(f"Function Name: {function_name}")
# print(f"Input parameter/variable: {input_params}")
# print("Variables in body:")
# for var, var_type in body_variables.items():
#     print(f"  {var}: {var_type}")

# print("Return statements:")
# for statement in return_statements:
#     print(f"  {statement}")