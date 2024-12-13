from concurrent.futures import ThreadPoolExecutor
from typing import List, Callable, Any

def generate_suggestions_parallel(
    generator_func: Callable,
    count: int,
    max_workers: int,
    *args: Any,
    **kwargs: Any
) -> List[str]:
    """
    Generate multiple suggestions in parallel using a ThreadPoolExecutor.
    
    Args:
        generator_func: The function that generates a single suggestion
        count: Number of suggestions to generate
        max_workers: Maximum number of parallel workers
        *args, **kwargs: Arguments to pass to generator_func
    
    Returns:
        List of generated suggestions
    """
    with ThreadPoolExecutor(max_workers=min(count, max_workers)) as executor:
        futures = [
            executor.submit(generator_func, *args, **kwargs)
            for _ in range(count)
        ]
        return [future.result() for future in futures] 