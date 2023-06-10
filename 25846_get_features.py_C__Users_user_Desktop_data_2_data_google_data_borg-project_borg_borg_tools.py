"""@author: Bryan Silverthorn <bcs@cargo-cult.org>"""

import os.path
import csv
import borg
import borg.distributors

logger = borg.get_logger(__name__, default_level = "INFO")

def features_for_path(domain, task_path):
    # bring back relevant globals
    import os.path
    import borg

    logger = borg.get_logger(__name__, default_level = "INFO")

    # collect features
    logger.info("getting features of %s", os.path.basename(task_path))

    with domain.task_from_path(task_path) as task:
        with borg.accounting() as accountant:
            (names, values) = domain.compute_features(task)

        return (
            task_path,
            ["cpu_cost"] + list(names),
            [accountant.total.cpu_seconds] + list(values))

@borg.annotations(
    domain_name = ("suite path, or name of the problem domain", "positional"),
    instances_root = ("path to instances files", "positional", None, os.path.abspath),
    suffix = ("file suffix to apply", "positional"),
    skip_existing = ("skip existing features?", "flag"),
    distributor_name = ("name of task distributor", "option"),
    workers = ("submit jobs?", "option", "w", int),
    )
def main(
    domain_name,
    instances_root,
    suffix = ".features.csv",
    skip_existing = False,
    distributor_name = "ipython",
    workers = 0):
    """Collect task features."""

    def yield_runs():
        if os.path.exists(domain_name):
            domain = borg.load_solvers(domain_name).domain
        else:
            domain = borg.get_domain(domain_name)

        paths = list(borg.util.files_under(instances_root, domain.extensions))
        count = 0

        for path in paths:
            if skip_existing and os.path.exists(path + suffix):
                continue

            count += 1

            yield (features_for_path, [domain, path])

        logger.info("collecting features for %i instances", count)

    distributor = borg.distributors.make(
        distributor_name,
        workers=workers)

    for (cnf_path, names, values) in distributor.do(yield_runs()):
        csv_path = cnf_path + suffix

        with open(csv_path, "wb") as csv_file:
            csv.writer(csv_file).writerow(names)
            csv.writer(csv_file).writerow(values)

if __name__ == "__main__":
    borg.script(main)
