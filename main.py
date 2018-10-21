import logging

from gp.evolve import Evolve
from gp.trainer import Hello


if __name__ == '__main__':
    if __debug__:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    log = logging.getLogger(__name__)
    log.info('Starting...')

    try:
        print(Evolve(Hello(), genes_per_gen=16).generate_solution())
    except KeyboardInterrupt:
        log.critical('Keyboard interrupt received')
