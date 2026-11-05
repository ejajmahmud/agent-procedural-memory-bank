"""CLI for agent-procedural-memory-bank."""
import sys
import argparse
from .bank import ProceduralBank


def main():
    parser = argparse.ArgumentParser(description="Agent Procedural Memory Bank")
    parser.add_argument("--demo", action="store_true", help="Run procedural recipe demonstration")
    args = parser.parse_args()

    bank = ProceduralBank()
    if args.demo:
        bank.register_recipe(
            task_name="build_and_test",
            steps=[
                {"tool": "git_checkout", "args": {"branch": "$branch"}},
                {"tool": "pip_install", "args": {"reqs": "requirements.txt"}},
                {"tool": "run_pytest", "args": {"path": "tests/"}}
            ],
            parameters=["branch"]
        )
        recipe = bank.get_recipe("build_and_test")
        plan = recipe.instantiate({"branch": "release-v1"})
        print("Instantiated Execution Plan:", plan)
        recipe.record_result(True)
        print("Registered Recipes:", bank.list_recipes())
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
