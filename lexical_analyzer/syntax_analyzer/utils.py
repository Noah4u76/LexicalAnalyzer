def pretty_print_parse_tree(node, indent=0):
    """
    Utility function to print a parse tree in a structured format.
    For debugging purposes.
    """
    indentation = "  " * indent
    print(f"{indentation}{node}")
    
    if hasattr(node, 'children'):
        for child in node.children:
            pretty_print_parse_tree(child, indent + 1)

def format_production_rule(rule):
    """
    Format a production rule string for better readability.
    """
    # Split the rule by '->'
    parts = rule.split('->')
    
    if len(parts) == 2:
        left = parts[0].strip()
        right = parts[1].strip()
        
        # Indent the right part
        return f"{left} ->\n    {right}"
    
    return rule