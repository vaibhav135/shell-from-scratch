class DeclareVariable:
    def __init__(self):
        self.declared_var_map = {}

    def add_var_declaration(self, declaration_string: str):
        declaration = declaration_string.split("=")
        if len(declaration) > 0:
            self.declared_var_map[declaration[0].strip()] = declaration[1].strip()

    def get_var_declaration(self, dec_key: str) -> str:
        dec_val = self.declared_var_map.get(dec_key)
        if dec_val:
            return f'{dec_key}="{dec_val}"'
        return ""

    def validate_declaration(self, declaration: str) -> bool:
        declaration_list = declaration.split("=")
        if len(declaration_list) > 0:
            dec_key = declaration_list[0]
            if dec_key[0].isnumeric():
                return False
            if not all(ch.isalpha() or ch.isdigit() or ch == "_" for ch in dec_key):
                return False

        return True

    def extract_values(self, input: str) -> list[str]:
        vars = []
        for inp in input.split(" "):
            idx_var = inp.rfind("$")
            if idx_var > -1:
                # extracting the key from the string
                dec_key = inp[idx_var + 1 :]

                start_braces_idx = inp.rfind("{")
                ending_brace_idx = inp.rfind("}")
                if start_braces_idx > -1:
                    dec_key = inp[idx_var + 2 : ending_brace_idx]

                val = self.declared_var_map.get(dec_key.strip(), "")

                if idx_var > 0:
                    val = inp[:idx_var] + val

                if start_braces_idx > -1:
                    val = val + inp[ending_brace_idx + 1 :]

                if val:
                    vars.append(val)
                else:
                    vars.append("")

        return vars


declare_var = DeclareVariable()
