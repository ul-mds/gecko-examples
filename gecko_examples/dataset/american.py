import numpy as np
import pandas as pd
from gecko import generator, mutator

from gecko_examples.common import gecko_data_dir


def generate_data_frame(count: int, rng: np.random.Generator):
    return generator.to_data_frame(
        {
            (
                "given_name",
                "gender",
                "ethnicity",
            ): generator.from_multicolumn_frequency_table(
                gecko_data_dir / "en_US" / "given-name-gender-ethnicity.csv",
                value_columns=["given_name", "gender_code", "ethnicity_code"],
                freq_column="count",
                rng=rng,
            )
        },
        count,
    )


def mutate_data_frame(df: pd.DataFrame, rng: np.random.Generator):
    return mutator.mutate_data_frame(
        df,
        {
            "gender": (
                0.02,
                mutator.with_categorical_values(
                    gecko_data_dir / "en_US" / "given-name-gender-ethnicity.csv",
                    value_column="gender_code",
                    rng=rng,
                ),
            ),
            "ethnicity": (0.01, mutator.with_delete(rng)),
        },
        rng,
    )
