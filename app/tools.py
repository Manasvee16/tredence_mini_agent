import random

# --- Tool Logic for Option A ---

def extract_functions(state: dict):
    """Step 1: Simulates extracting functions from code."""
    
    # --- INTENTIONAL ERROR FOR DEMO ---
    #raise ValueError("Simulated Critical Failure! The tool crashed.") 
    # ----------------------------------

    # The code below won't run because of the error above
    code = state.get("code", "")
    func_count = code.count("def ")
    state["functions_found"] = func_count
    state["logs"].append(f"Extracted {func_count} functions.")
    return state

def check_complexity(state: dict):
    """Step 2: Checks cyclomatic complexity (mocked by length)."""
    code_len = len(state.get("code", ""))
    complexity = "High" if code_len > 100 else "Low"
    state["complexity"] = complexity
    state["logs"].append(f"Complexity analysis: {complexity}")
    return state

def detect_issues(state: dict):
    """Step 3: Detect basic issues."""
    issues = []
    if "print(" in state.get("code", ""):
        issues.append("Avoid using print() in production.")
    state["issues"] = issues
    state["logs"].append(f"Issues found: {len(issues)}")
    return state

def suggest_improvements(state: dict):
    """Step 4: Suggest improvements and boost quality score."""
    current_score = state.get("quality_score", 0)
    
    # Simulate improvement by increasing score
    new_score = current_score + 20 
    if len(state.get("issues", [])) > 0:
        state["issues"].pop() # Simulate fixing an issue
        
    state["quality_score"] = new_score
    state["logs"].append(f"Applied fixes. New Quality Score: {new_score}")
    return state

# --- Registry ---
TOOL_REGISTRY = {
    "extract_functions": extract_functions,
    "check_complexity": check_complexity,
    "detect_issues": detect_issues,
    "suggest_improvements": suggest_improvements
}
