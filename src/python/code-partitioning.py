import re

def extract_function_info(code):
    function_declaration_pattern = re.compile(r'fn\s+(\w+)\s*\(([^)]*)\)\s*{', re.DOTALL)
    variable_declaration_pattern = re.compile(r'\b(\w+)(?:\s*:\s*([^,\n]+))?\s*(?:,|\n|{)')
    return_statement_pattern = re.compile(r'return\s*(.+?)\s*;', re.DOTALL)

    function_declaration_match = function_declaration_pattern.search(code)

    if function_declaration_match:
        function_name = function_declaration_match.group(1)
        input_params = function_declaration_match.group(2)

        body_code = code[function_declaration_match.end():]
        return_statement_match = return_statement_pattern.search(body_code)
        # return_content = return_statement_match.group(1)
        if return_statement_match:
            return_content = return_statement_match.group(1)
        else:
            return_content = "No return statement found"


        variable_matches = variable_declaration_pattern.findall(body_code)
        variable_types = {var: var_type for var, var_type in variable_matches}

        print(f"Function Name: {function_name.strip()}")
        print(f"Input Parameter Types: {input_params.strip()}")
        # print(f"Expected Return Type: {return_type.strip()}")
        print("Variable Types in Body:")
        for var, var_type in variable_types.items():
            print(f"  {var}: {var_type}")
        print(f"Return Content: {return_content.strip()}")
    else:
        print("Not a valid function declaration!")

file_path = 'test4.rs'
with open(file_path, 'r') as file:
    file_content = file.read()

extract_function_info(file_content)


# example_code = """
# fn calculate(x: i32, y: i32) -> i32 {
#     let result: i32 = x + y;
#     return result;
# }
# """

# extract_function_info(example_code)

# function_declaration_pattern = re.compile(r'fn\s+(\w+)\s*\(([^)]*)\)\s*->\s*([^{\n]+)\s*{', re.DOTALL)