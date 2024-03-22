import numpy as np
import pandas as pd
from gecko import generator, mutator

from gecko_examples.common import gecko_data_dir, assets_dir


def generate_data_frame(count: int, rng: np.random.Generator):
    gen_last_name = generator.from_frequency_table(
        gecko_data_dir / "de_DE" / "last-name.csv",
        value_column="last_name",
        freq_column="count",
        rng=rng,
    )

    gen_given_name_gender = generator.from_multicolumn_frequency_table(
        gecko_data_dir / "de_DE" / "given-name-gender.csv",
        value_columns=["given_name", "gender"],
        freq_column="count",
        rng=rng,
    )

    gen_street_municip_postcode = generator.from_multicolumn_frequency_table(
        gecko_data_dir / "de_DE" / "street-municipality-postcode.csv",
        value_columns=["street_name", "municipality", "postcode"],
        freq_column="count",
        rng=rng,
    )

    return generator.to_data_frame(
        {
            ("given_name", "gender"): gen_given_name_gender,
            "last_name": gen_last_name,
            ("street_name", "municipality", "postcode"): gen_street_municip_postcode,
        },
        count,
    )


def mutate_data_frame(df: pd.DataFrame, rng: np.random.Generator):
    return mutator.mutate_data_frame(
        df,
        {
            ("given_name", "last_name"): (0.01, mutator.with_permute()),
            "gender": [
                (
                    0.02,
                    mutator.with_categorical_values(
                        gecko_data_dir / "de_DE" / "given-name-gender.csv",
                        value_column="gender",
                        rng=rng,
                    ),
                ),
                (0.05, mutator.with_missing_value("", "all")),
            ],
            "postcode": (
                0.01,
                mutator.with_cldr_keymap_file(
                    assets_dir / "de-t-k0-windows.xml",
                    charset="0123456789",
                    rng=rng,
                ),
            ),
        },
        rng,
    )
