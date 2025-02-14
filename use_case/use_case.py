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
    (s, t) = solution
    weight = 0
    for u in s:
        for v in t:
            for node1, node2, weight in original_input:
                if (node1 == u and node2 == v) or (node1 == v and node2 == u):
                    weight += weight
    total_input_weight = sum([weight for _, _, weight in original_input])
    return weight / total_input_weight


async def aggregate(outputs: AsyncIterator[EvaluationResults]) -> float:
    total = 0
    count = 0
    async for output in outputs:
        total += output["solution"][0]["metric"]
        count += 1
    if count == 0:
        return 0
    return total / count
