from z3 import *


class PathSolver:
    def __init__(self, var_names, var_types):
        self.var_names = var_names
        self.var_types = var_types
        self.variables = {}
        self._init_variables()
    
    def _init_variables(self):
        for name, typ in zip(self.var_names, self.var_types):
            if typ == "int":
                self.variables[name] = Int(name)
            elif typ == "float":
                self.variables[name] = Real(name)
            elif typ == "bool":
                self.variables[name] = Bool(name)
            else:
                self.variables[name] = Int(name)  #Default

    def solve_conditions(self, conditions):
        unique_conditions = set()

        for path in conditions:
            for cond_type, cond in path:
                if cond_type in ('if', 'else'):
                    unique_conditions.add((cond_type, cond))
        
        solutions = []
        solver = Solver()

        for cond_type, cond in unique_conditions:
            solver.push()
            
            try:
                parsed = eval(cond, {}, self.variables)
                if cond_type == 'else':
                    solver.add(Not(parsed))
                else:
                    solver.add(parsed)
                
                if solver.check() == sat:
                    model = solver.model()
                    solution = {}
                    for name in self.var_names:
                        if name in self.variables:
                            if self.var_types[self.var_names.index(name)] == "int":
                                solution[name] = model[self.variables[name]].as_long()
                            elif self.var_types[self.var_names.index(name)] == "float":
                                solution[name] = float(model[self.variables[name]].as_decimal(3))
                            elif self.var_types[self.var_names.index(name)] == "bool":
                                solution[name] = bool(model[self.variables[name]])
                    solutions.append(solution)
            except:
                continue
                
            solver.pop()
        
        return solutions

def solve_conditions(conditions, args_names, args_types):
    solver = PathSolver(args_names, args_types)
    solutions = solver.solve_conditions(conditions)
    return solutions