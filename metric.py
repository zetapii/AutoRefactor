import ast

##The cyclomatic complexity is calculated by counting the number of decision points in the code
##CyclomaticComplexityVisitor calculate the cyclomatic complexity by visiting the AST 
class CyclomaticComplexityVisitor(ast.NodeVisitor): 
    def __init__(self): 
        self.complexity = 0

    def visit_If(self, node):
        is_orelse = isinstance(node, ast.If) or isinstance(node, ast.ElseIf)
        if is_orelse:
            self.complexity += 1  
        self.generic_visit(node)

    def visit_For(self, node):
        self.complexity += 1 
        self.generic_visit(node)        

    def visit_While(self, node):
        self.complexity += 1 
        self.generic_visit(node)
    
    def visit_TryExcept(self, node):
        self.complexity += 1 
        self.generic_visit(node)

    def visit_TryFinally(self, node):
        self.generic_visit(node)

    def visit_With(self, node):
        self.complexity += 1 
        self.generic_visit(node) 

    def visit_Assert(self, node):
        self.complexity += 1  
        self.generic_visit(node)

    def visit_BoolOp(self, node):
        self.complexity += 1
        self.generic_visit(node) 

    def visit_comprehension(self, node):
        self.complexity += 1 
        self.generic_visit(node)

import ast

##Generic class to calculate design metrics 
##Currently supports finding long methods and calculating cyclomatic complexity
##Other metrics can be added in the future
class DesignMetric:
    def __init__(self):
        pass

    def find_long_methods(self, code, max_lines=30):
        tree = ast.parse(code)
        long_methods = []

        class MethodVisitor(ast.NodeVisitor):
            def __init__(self):
                self.total_lines = 0
            def count_statements(self, node):
                self.total_lines +=1
                if isinstance(node, (ast.FunctionDef, ast.For, ast.While)):
                    for child in node.body : 
                        self.count_statements(child) 
                elif isinstance(node, ast.If):
                    for child in node.body : 
                        self.count_statements(child) 
                    for sub_node in node.orelse:
                        self.count_statements(sub_node)
            def visit_FunctionDef(self, node):
                self.total_lines = 0
                self.count_statements(node)
                if self.total_lines > max_lines:
                    long_methods.append(node.name)
        visitor = MethodVisitor()
        visitor.visit(tree)
        return long_methods

    def calculate_cyclomatic_complexity(self, code):
        tree = ast.parse(code)
        visitor = CyclomaticComplexityVisitor()
        visitor.visit(tree)
        print("Cyclomatic Complexity :", visitor.complexity)
        return visitor.complexity

## Basic test cases for the DesignMetric class
class TestDesignMetric:
    def test_find_long_methods(self):
        code_snippet = """

def long_method():
    print("Line 1")
    print("Line 2")
    print("Line 3")
    print("Line 4")
    print("Line 5")
    print("Line 6")
    print("Line 7")
    print("Line 8")
    print("Line 9")
    print("Line 10")
    print("Line 11")
    print("Line 12")
    print("Line 13")
    print("Line 14")
    print("Line 15")
    print("Line 16")
    print("Line 17")
    print("Line 18")
    print("Line 19")
    print("Line 20")
    print("Line 21")  # This line exceeds the threshold
    pass

def short_method():
    print("This is a short method.")
    # this is a comment
    print("this is not a comment")
    pass
"""
        design_metric = DesignMetric()
        long_methods = design_metric.find_long_methods(code_snippet,20)
        assert long_methods == ['long_method']
    def test_calculate_cyclomatic_complexity(self):
        code_snippet = """
def my_function(x):
    if x > 0:
        print("x is positive")
    elif x == 0:
        print("x is zero")
    elif x == 4:
        print("x is non-positive")
    else:
        if x > 0:
            print("x is positive")
        elif x == 0:
            print("x is non-positive")
        elif x == 4:
            print("x is non-positive")
            print("x is negative")
            print("hi")
"""
        design_metric = DesignMetric()
        complexity = design_metric.calculate_cyclomatic_complexity(code_snippet)
        assert complexity == 6

if __name__ == "__main__":
     test_design_metric = TestDesignMetric()
     test_design_metric.test_find_long_methods()
     test_design_metric.test_calculate_cyclomatic_complexity()