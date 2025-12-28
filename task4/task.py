import json
import numpy as np
from typing import List, Dict, Tuple, Any

def load_json_from_path(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()

def calculate_membership_value(x: float, points: List[Tuple[float, float]]) -> float:
    points = sorted(points, key=lambda p: p[0])
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    
    if len(points) < 2:
        return 0.0
    
    if x <= xs[0]:
        return ys[0]
    if x >= xs[-1]:
        return ys[-1]
    
    for i in range(len(xs) - 1):
        if xs[i] <= x <= xs[i + 1]:
            dx = xs[i + 1] - xs[i]
            if dx == 0:
                return (ys[i] + ys[i + 1]) / 2
            dy = ys[i + 1] - ys[i]
            return ys[i] + dy * (x - xs[i]) / dx
    return 0.0

def determine_term_activations(value: float, linguistic_variable: List[Dict[str, Any]]) -> Dict[str, float]:
    activations = {}
    for term in linguistic_variable:
        activations[term['id']] = calculate_membership_value(value, term['points'])
    return activations

def find_control_variable_bounds(control_linguistic_variable: List[Dict[str, Any]]) -> Tuple[float, float]:
    all_x = [p[0] for term in control_linguistic_variable for p in term['points']]
    if not all_x:
        return 0, 10
    return min(all_x), max(all_x)

def build_aggregated_membership(activations: List[float], rules: List[Tuple[str, str]], 
                                control_linguistic_variable: List[Dict[str, Any]], 
                                control_samples: np.ndarray) -> np.ndarray:
    aggregated_membership_curve = np.zeros_like(control_samples, dtype=float)
    
    for activation_level, rule in zip(activations, rules):
        _, output_id = rule
        output_term = next((t for t in control_linguistic_variable if t['id'] == output_id), None)
        
        if output_term is None or activation_level == 0:
            continue

        mu_out = np.array([calculate_membership_value(s, output_term['points']) for s in control_samples])
        mu_clipped = np.minimum(activation_level, mu_out)
        aggregated_membership_curve = np.maximum(aggregated_membership_curve, mu_clipped)
        
    return aggregated_membership_curve

def get_crisp_output_mom(control_samples: np.ndarray, aggregated_membership_curve: np.ndarray) -> float:
    if aggregated_membership_curve.size == 0:
        return 0.0
        
    max_mu = np.max(aggregated_membership_curve)
    if max_mu == 0:
        return 0.0
        
    indices = np.where(np.isclose(aggregated_membership_curve, max_mu, atol=1e-6))[0]
    if indices.size == 0:
        return 0.0
        
    s_left = control_samples[indices[0]]
    s_right = control_samples[indices[-1]]
    return (s_left + s_right) / 2

def calculate_fuzzy_control_output(temperature: float, temp_linguistic_variable: List[Dict[str, Any]], 
                                   control_linguistic_variable: List[Dict[str, Any]], rules: List[Tuple[str, str]], 
                                   steps: int = 1001) -> float:
    s_min, s_max = find_control_variable_bounds(control_linguistic_variable)
    control_samples = np.linspace(s_min, s_max, steps)

    mu_input = determine_term_activations(temperature, temp_linguistic_variable)
    rule_activations = [mu_input.get(rule[0], 0.0) for rule in rules]

    aggregated_curve = build_aggregated_membership(rule_activations, rules, control_linguistic_variable, control_samples)
    
    optimal_control_value = get_crisp_output_mom(control_samples, aggregated_curve)
    return optimal_control_value

def run_fuzzy_logic_system(lvinput_path: str = 'lvinput.json', lvoutput_path: str = 'lvoutput.json', 
                           rules_path: str = 'rules.json', input_temp: float = 19.0) -> float:
    lvinput_json = load_json_from_path(lvinput_path)
    lvoutput_json = load_json_from_path(lvoutput_path)
    rules_json = load_json_from_path(rules_path)

    temp_data = json.loads(lvinput_json)
    control_data = json.loads(lvoutput_json)
    rules_data = json.loads(rules_json)

    temp_ling_var = temp_data["температура"]
    control_ling_var = control_data["нагрев"]

    optimal_s = calculate_fuzzy_control_output(input_temp, temp_ling_var, control_ling_var, rules_data)
    return optimal_s

if __name__ == "__main__":
    test_temp = 19.0
    optimal_value = run_fuzzy_logic_system(input_temp=test_temp)
    print(f"Для температуры {test_temp:.2f}°C оптимальное управление: {optimal_value:.2f}")
