"""Procedural memory bank caching verified multi-step tool recipes."""
import time
from typing import Dict, List, Any, Optional


class Recipe:
    def __init__(self, task_name: str, steps: List[Dict[str, Any]], parameters: List[str]):
        self.task_name = task_name
        self.steps = steps  # list of {"tool": str, "args": dict}
        self.parameters = parameters
        self.success_count = 0
        self.failure_count = 0
        self.last_used = time.time()

    def instantiate(self, param_values: Dict[str, Any]) -> List[Dict[str, Any]]:
        self.last_used = time.time()
        instantiated_steps = []
        for step in self.steps:
            args = dict(step.get("args", {}))
            for k, v in args.items():
                if isinstance(v, str) and v.startswith("$"):
                    param_name = v[1:]
                    if param_name in param_values:
                        args[k] = param_values[param_name]
            instantiated_steps.append({"tool": step["tool"], "args": args})
        return instantiated_steps

    def record_result(self, success: bool):
        if success:
            self.success_count += 1
        else:
            self.failure_count += 1

    def success_rate(self) -> float:
        total = self.success_count + self.failure_count
        return (self.success_count / total) if total > 0 else 1.0


class ProceduralBank:
    def __init__(self):
        self._recipes: Dict[str, Recipe] = {}

    def register_recipe(self, task_name: str, steps: List[Dict[str, Any]], parameters: List[str]) -> Recipe:
        recipe = Recipe(task_name, steps, parameters)
        self._recipes[task_name] = recipe
        return recipe

    def get_recipe(self, task_name: str) -> Optional[Recipe]:
        return self._recipes.get(task_name)

    def list_recipes(self) -> List[Dict[str, Any]]:
        return [{
            "task_name": r.task_name,
            "steps_count": len(r.steps),
            "parameters": r.parameters,
            "success_rate": round(r.success_rate(), 2)
        } for r in self._recipes.values()]
