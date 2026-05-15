class DeclareVariable:
    def __init__(self):
        self.declared_var_list = {}

    def add_var_declaration(self, declaration_string: str):
        declaration = declaration_string.split("=")
        if len(declaration) > 0:
            self.declared_var_list[declaration[0].strip()] = declaration[1].strip()

    def get_var_declaration(self, dec_key: str) -> str:
        dec_val = self.declared_var_list.get(dec_key)
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


declare_var = DeclareVariable()
