from typing import Dict, AsyncIterator, List, Tuple
from aqora_cli import PipelineConfig, LayerEvaluation

Input = List[Tuple[int, int, float]]
Output = Tuple[List[int], List[int]]
EvaluationResults = Dict[str, List[LayerEvaluation]]


async def generator(_: PipelineConfig) -> AsyncIterator[Input]:
    graphs = [
        [
            (0, 1, 1.0),
            (0, 2, 1.0),
            (0, 4, 1.0),
            (1, 2, 1.0),
            (2, 3, 1.0),
            (3, 4, 1.0),
        ],
        [
            (0, 1, 1.0),
            (0, 3, 1.0),
            (1, 2, 1.0),
            (1, 4, 1.0),
            (2, 3, 1.0),
            (3, 4, 1.0),
        ],
        [
            (0, 1, 1.0),
            (0, 2, 1.0),
            (1, 3, 1.0),
            (1, 4, 1.0),
            (2, 4, 1.0),
            (3, 4, 1.0),
        ],
    ]
    for graph in graphs:
        yield graph


async def metric(solution: Output, original_input: Input) -> float:
    s, t = set(solution[0]), set(solution[1])
    cut = sum(
        weight
        for node1, node2, weight in original_input
        if (node1 in s and node2 in t) or (node1 in t and node2 in s)
    )
    total_input_weight = sum(weight for _, _, weight in original_input)
    if total_input_weight == 0:
        return 0.0
    return cut / total_input_weight


async def aggregate(outputs: AsyncIterator[EvaluationResults]) -> float:
    total = 0
    count = 0
    async for output in outputs:
        total += output["solution"][0]["metric"]
        count += 1
    if count == 0:
        return 0
    return total / count
