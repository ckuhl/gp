import logging

import evolve
import trainer


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger(__name__)
    log.info('Starting...')
    try:
        simulation = evolve.Evolve(trainer.Hello, per_gen=16)
        simulation.generate_solution()
    except KeyboardInterrupt:
        if __debug__:
            log.warn('Keyboard interrupt received')

