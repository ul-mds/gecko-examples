This repository contains example scripts for generating data with [Gecko](https://github.com/ul-mds/gecko) — a Python
library for generation and mutation of realistic data at scale.
It uses the [Gecko data repository](https://github.com/ul-mds/gecko-data) to equip Gecko's built-in generators and
mutators with the information they need to generate realistic datasets.

# Installation

You need to have [Poetry](https://python-poetry.org/) installed.

First, clone this repository.

```
$ git clone --recurse-submodules https://github.com/ul-mds/gecko-examples.git
```

Change into the repository's root directory.
Install the project and its dependencies, then use `poetry shell` to drop into the project's virtual environment.

```
$ cd gecko-examples
$ poetry install
$ poetry shell
```

# Usage

This project installs a script that you can invoke with the `gecko` command.

```
$ gecko --help
Usage: gecko [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  benchmark  Test Gecko's performance by timing data generation.
  generate   Generate realistic-looking data with Gecko.
```

The command exposes two subcommands: `benchmark` for testing Gecko's performance and `generate` to generate and
mutate a realistic dataset.
Currently, there are two options for datasets that you can generate.

- American population dataset with given name, gender and ethnicity
- German population dataset with given name, last name, gender, street name, municipality and postcode

[You can check out and modify the scripts that generate these datasets in this repository.](gecko_examples/dataset)

## Generating data

To generate datasets, use the `generate` subcommand.

```
$ gecko generate --help
Usage: gecko generate [OPTIONS] {german|american}

  Generate realistic-looking data with Gecko.

Options:
  -n INTEGER                  Number of records to generate.
  -s, --seed INTEGER          Seed for random number generator.
  -o, --output-dir DIRECTORY  Directory to save generated datasets to.
  --help                      Show this message and exit.
```

By default, the command will generate and mutate a million records, use the same fixed seed and store results in
a directory called "output" within the project repository.

```
$ gecko generate german
Generating 1000000 records for `german` dataset...
Mutating generated dataset...
Saving generated dataset to /home/mjugl/PycharmProjects/pprl-gecko-examples/output/german-generated.csv...
Saving mutated dataset to /home/mjugl/PycharmProjects/pprl-gecko-examples/output/german-mutated.csv...
Done!
$ ls output
german-generated.csv  german-mutated.csv
```

## Benchmarking Gecko

To measure the time Gecko needs to generate data, use the `benchmark` subcommand.

```
$ gecko benchmark --help
Usage: gecko benchmark [OPTIONS] {german|american}

  Test Gecko's performance by timing data generation.

Options:
  -n INTEGER                      Number of records to generate.
  -t, --time-unit [s|ms|us|ns]    Units to display execution times in.
  -w, --warmup-iterations INTEGER
                                  Number of times to run dataset generation
                                  before measuring execution times.
  -i, --iterations INTEGER        Number of times to run dataset generation.
  --help                          Show this message and exit.
```

By default, Gecko will generate and mutate a million records.
At first, five new datasets will be generated before measuring execution time 100 times.
The script will then print out a summary.

```
$ gecko benchmark german
Warming up  [####################################]  100%          
Measuring  [####################################]  100%          
Min: 4666.92ms / Max: 4940.43ms
Q5: 4674.10ms / Q10: 4680.11ms / Q25: 4690.75ms / Q50: 4769.14ms / Q75: 4845.33ms / Q90: 4891.32ms / Q95: 4904.24ms
```

Be aware that this command only gives a rough estimate of the performance you can expect from Gecko.
Since it uses Python's timeit module to measure execution time, there are a lot of other factors that can affect your
results.

# License

Gecko is released under the MIT License.