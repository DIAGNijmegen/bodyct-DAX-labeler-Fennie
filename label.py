"""Entry-point script to label radiology reports."""
import pandas as pd

from args import ArgParser
from loader import Loader
from stages import Extractor, Classifier, Aggregator
from constants import *
import os
from glob import glob
from tqdm import tqdm

def count(reports_path):
    print(f"Counting reports.")
    reports = pd.read_csv(reports_path, names=['laudos'])
    num_reports = reports.laudos.count()
    num_batches = num_reports//5000
    print(f"Found {num_reports} reports. Label in {num_batches} batches.")
    return num_batches

def write(reports, labels, output_path, verbose=False):
    """Write labeled reports to specified path."""
    labeled_reports = pd.DataFrame({REPORTS: reports})
    for index, category in enumerate(CATEGORIES):
        labeled_reports[category] = labels[:, index]

    if verbose:
        print(f"Writing reports and labels to {output_path}.")
    labeled_reports[[REPORTS] + CATEGORIES].to_csv(output_path,
                                                   index=False)

def label(args):
    """Label the provided report(s)."""

    loader = Loader(args.reports_path, args.extract_impression)

    extractor = Extractor(args.mention_phrases_dir,
                          args.unmention_phrases_dir,
                          verbose=args.verbose)
    classifier = Classifier(args.pre_negation_uncertainty_path,
                            args.negation_path,
                            args.post_negation_uncertainty_path,
                            verbose=args.verbose)
    aggregator = Aggregator(CATEGORIES,
                            verbose=args.verbose)

    n_batches = count(args.reports_path)

    print(f"Numero de batches: {n_batches}.")

    if n_batches == 0:

        # Load reports in place.
        loader.load()
        # Extract observation mentions in place.
        extractor.extract(loader.collection)
        # Classify mentions in place.
        classifier.classify(loader.collection)
        # Aggregate mentions to obtain one set of labels for each report.
        labels = aggregator.aggregate(loader.collection)
        # Write CSV
        write(loader.reports, labels, args.output_path, args.verbose)

    else: 
        lista_output_batch_path = []
        for i in range(n_batches + 1):
            print(f"Batch {i}.")

            #cria nome para o output deste batch
            output_dirname = os.path.dirname(args.output_path)
            print(output_dirname)
            output_filename = os.path.basename(args.output_path)
            print(output_filename)
            output_batch_path = (f"{output_dirname}/{i}_batch_{output_filename}")

            lista_output_batch_path.append(output_batch_path)

            #verifica se já há esse arquivo no diretório output
            lista_dir_out = glob("output/*.csv")
            if output_batch_path in lista_dir_out:
                if args.verbose:
                    print(f"Output do batch {i} encontrado: {output_batch_path}\nPassando para proximo batch")
                continue
            
            # Load reports in place.
            loader.load(batch = i)
            # Extract observation mentions in place.
            extractor.extract(loader.collection)
            # Classify mentions in place.
            classifier.classify(loader.collection)
            # Aggregate mentions to obtain one set of labels for each report.
            labels = aggregator.aggregate(loader.collection)
            # Write CSV for this batch.
            write(loader.reports, labels, output_batch_path, args.verbose)
        
        # le todos os CSVs intermediarios e os concatena
        df_fim = pd.read_csv(lista_output_batch_path[0])

        lista_batches_restantes = lista_output_batch_path[1:]
        if args.verbose:
            print("Agregating all batches...")
            lista_batches_restantes = tqdm(lista_batches_restantes)

        for o in lista_batches_restantes:
            df_int = pd.read_csv(o)
            df_fim = df_fim.append(df_int)
        df_fim.to_csv(args.output_path, index=False)


if __name__ == "__main__":
    parser = ArgParser()
    label(parser.parse_args())