import logging
from operator import itemgetter
import os
from pathlib import Path
import subprocess
import sys
import tempfile

import nlp_ws
from poldeepner.core.process_file import process_file

_log = logging.getLogger(__name__)


def check_models_paths(models_embeddings):
    for model_path, embedding_path in models_embeddings.items():
        if not (os.path.exists(model_path) and os.path.exists(embedding_path)):
            return False
    return True


class PolDeepNerWorker(nlp_ws.NLPWorker):
    def process(self, input_path, task_options, output_path):
        if task_options is None:
            task_options = {'models': {'./poldeepner/model/poldeepner-kgr10.plain.skipgram.dim300.neg10.bin':
                                       './poldeepner/model/kgr10.plain.skipgram.dim300.neg10.bin'}}
        elif 'models' not in task_options:
            raise WrongTaskOptions('Models not in task options: ' + str(task_options))

        elif not check_models_paths(task_options['models']):
            raise WrongTaskOptions('Wrong paths to models: ' + str(task_options['models']))

        # Process .iob file
        process_file(input_path, output_path, task_options['models'])


class WrongTaskOptions(Exception):
    def __init__(self, message):
        super(WrongTaskOptions, self).__init__(message)


if __name__ == '__main__':
    nlp_ws.NLPService.main(PolDeepNerWorker)
