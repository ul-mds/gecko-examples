import time
import timeit
from pathlib import Path
from typing import Callable, Any, Optional

import click
import numpy as np
import pandas as pd

from gecko_examples.dataset import german, american

_default_output_dir = Path(__file__).parent.parent / "output"


@click.group()
def cli():
    pass


@cli.command()
@click.argument(
    "dataset", type=click.Choice(["german", "american"], case_sensitive=False)
)
@click.option("-n", default=1_000_000, help="Number of records to generate.")
@click.option(
    "--time-unit",
    "-t",
    default="ms",
    type=click.Choice(["s", "ms", "us", "ns"], case_sensitive=False),
    help="Units to display execution times in.",
)
@click.option(
    "--warmup-iterations",
    "-w",
    default=5,
    help="Number of times to run dataset generation before measuring execution times.",
)
@click.option(
    "--iterations", "-i", default=100, help="Number of times to run dataset generation."
)
@click.option(
    "--output-file",
    "-o",
    default=None,
    type=click.Path(dir_okay=False, file_okay=True, path_type=Path),
    help="File to write recorded times (in nanoseconds) to.",
)
def benchmark(
    dataset: str,
    n: int,
    time_unit: str,
    warmup_iterations: int,
    iterations: int,
    output_file: Optional[Path],
):
    """Test Gecko's performance by timing data generation."""

    rng = np.random.default_rng(727)

    def _generate_german():
        german.mutate_data_frame(german.generate_data_frame(n, rng), rng)

    def _generate_american():
        american.mutate_data_frame(american.generate_data_frame(n, rng), rng)

    def _ftime(val: float):
        if time_unit == "ns":
            return f"{int(val)}{time_unit}"
        else:
            return f"{val:.2f}{time_unit}"

    dataset_fn_dict: dict[str, Callable[[], Any]] = {
        "german": _generate_german,
        "american": _generate_american,
    }

    time_unit_div_dict: dict[str, int] = {
        "ns": 10**0,
        "us": 10**3,
        "ms": 10**6,
        "s": 10**9,
    }

    def _measure_once(bench_fn: Callable[[], Any]):
        return timeit.timeit(
            bench_fn,
            timer=time.perf_counter_ns,
            number=1,
        )

    dataset_fn = dataset_fn_dict.get(dataset, None)
    time_unit_div = time_unit_div_dict.get(time_unit, None)

    if dataset_fn is None:
        click.echo(f"Unimplemented dataset `{dataset}`", err=True)
        exit(1)

    if time_unit_div is None:
        click.echo(f"Unimplemented time unit `{time_unit}`", err=True)
        exit(2)

    with click.progressbar(range(warmup_iterations), label="Warming up") as bar:
        for _ in bar:
            _measure_once(dataset_fn)

    with click.progressbar(range(iterations), label="Measuring") as bar:
        dataset_fn_times = np.array(
            [_measure_once(dataset_fn) for _ in bar], dtype=float
        )

    if output_file is not None:
        with output_file.open(mode="w", encoding="utf-8") as f:
            f.writelines([f"{int(t)}\n" for t in dataset_fn_times])

    dataset_fn_times /= time_unit_div

    quantiles = [5, 10, 25, 50, 75, 90, 95]
    t_min, t_max = np.min(dataset_fn_times), np.max(dataset_fn_times)
    t_quantiles = [np.quantile(dataset_fn_times, q / 100) for q in quantiles]

    click.echo(f"Min: {_ftime(t_min)} / Max: {_ftime(t_max)}")
    click.echo(" / ".join(f"Q{q}: {_ftime(t)}" for q, t in zip(quantiles, t_quantiles)))


@cli.command()
@click.argument(
    "dataset", type=click.Choice(["german", "american"], case_sensitive=False)
)
@click.option("-n", default=1_000_000, help="Number of records to generate.")
@click.option("--seed", "-s", default=727, help="Seed for random number generator.")
@click.option(
    "--output-dir",
    "-o",
    default=_default_output_dir,
    type=click.Path(dir_okay=True, file_okay=False, path_type=Path),
    help="Directory to save generated datasets to.",
)
def generate(dataset: str, n: int, seed: int, output_dir: Path):
    """Generate realistic-looking data with Gecko."""

    def _generate_and_save(
        gen_fn: Callable[[], pd.DataFrame],
        mut_fn: Callable[[pd.DataFrame], pd.DataFrame],
    ):
        click.echo(f"Generating {n} records for `{dataset}` dataset...")
        gen_df = gen_fn()

        click.echo("Mutating generated dataset...")
        mut_df = mut_fn(gen_df)

        output_dir.mkdir(parents=True, exist_ok=True)

        gen_df_output_path = output_dir / f"{dataset}-generated.csv"
        mut_df_output_path = output_dir / f"{dataset}-mutated.csv"

        click.echo(f"Saving generated dataset to {gen_df_output_path}...")
        gen_df.to_csv(gen_df_output_path, index_label="id")

        click.echo(f"Saving mutated dataset to {mut_df_output_path}...")
        mut_df.to_csv(mut_df_output_path, index_label="id")

        click.echo("Done!")

    rng = np.random.default_rng(seed)

    if dataset == "german":
        _generate_and_save(
            lambda: german.generate_data_frame(n, rng),
            lambda df: german.mutate_data_frame(df, rng),
        )
    elif dataset == "american":
        _generate_and_save(
            lambda: american.generate_data_frame(n, rng),
            lambda df: american.mutate_data_frame(df, rng),
        )
    else:
        click.echo(f"Unimplemented dataset `{dataset}`", err=True)
        exit(1)


if __name__ == "__main__":
    cli()
