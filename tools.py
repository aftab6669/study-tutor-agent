import ast
import operator
from datetime import datetime, timedelta


# -----------------------------
# Calculator Tool
# -----------------------------

ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
}


def safe_calculator(expression):
    """
    Safely calculate a basic mathematical expression.
    """

    try:
        node = ast.parse(expression, mode="eval").body
        result = _evaluate(node)
        return str(result)

    except Exception:
        return "I could not calculate that expression."


def _evaluate(node):

    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Invalid value")

    if isinstance(node, ast.BinOp):
        left = _evaluate(node.left)
        right = _evaluate(node.right)

        operator_type = type(node.op)

        if operator_type not in ALLOWED_OPERATORS:
            raise ValueError("Operator not allowed")

        return ALLOWED_OPERATORS[operator_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _evaluate(node.operand)
        operator_type = type(node.op)

        if operator_type not in ALLOWED_OPERATORS:
            raise ValueError("Operator not allowed")

        return ALLOWED_OPERATORS[operator_type](operand)

    raise ValueError("Invalid expression")


# -----------------------------
# Study Planner Tool
# -----------------------------

def create_study_plan(subject, days, hours_per_day):
    """
    Create a simple study plan.
    """

    try:
        days = int(days)
        hours_per_day = float(hours_per_day)

        if days <= 0 or hours_per_day <= 0:
            return "Days and hours must be greater than zero."

        start_date = datetime.now().date()

        plan = []

        for i in range(days):

            date = start_date + timedelta(days=i)

            plan.append(
                f"Day {i + 1} ({date}): "
                f"Study {subject} for {hours_per_day:g} hour(s)."
            )

        return "\n".join(plan)

    except Exception:
        return "I could not create the study plan."


# -----------------------------
# Tool Dispatcher
# -----------------------------

def use_tool(tool_name, **kwargs):

    if tool_name == "calculator":
        return safe_calculator(kwargs.get("expression", ""))

    if tool_name == "study_plan":
        return create_study_plan(
            kwargs.get("subject", "General Study"),
            kwargs.get("days", 7),
            kwargs.get("hours_per_day", 2)
        )

    return "Unknown tool."
