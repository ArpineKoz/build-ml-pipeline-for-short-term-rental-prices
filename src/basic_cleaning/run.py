#!/usr/bin/env python
"""
Performs basic cleaning on the data and save the results in Weights & Biases
"""

import pandas as pd
import argparse
import logging
import wandb
import os


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    logger.info("Downloading artifact")
    artifact_local_path = run.use_artifact(args.input_artifact).file()
    df = pd.read_csv(artifact_local_path)

    logger.info("Cleaning outliers")
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()
    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])

    df.to_csv(args.output_artifact, index=False)

    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file(args.output_artifact)

    logger.info("Logging artifact")
    run.log_artifact(artifact)

    os.remove(args.output_artifact)



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This steps cleans the data")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="name of the input artifact",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="name of the output artifact",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="type of the output artifact",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="description of the output artifact",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help="minimum price to consider",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="maximum price to consider",
        required=True
    )

    args = parser.parse_args()

    go(args)
