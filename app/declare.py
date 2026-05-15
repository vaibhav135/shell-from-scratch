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


declare_var = DeclareVariable()
