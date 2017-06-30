from termcolor import cprint

import evolve
import trainer

if __name__ == '__main__':
    print('Starting...')
    try:
        simulation = evolve.Evolve(trainer.Hello, per_gen=16)
        simulation.generate_solution()
    except KeyboardInterrupt:
        # NOTE: The '\b' are to delete the ^C that is placed by pressing CTRL + C
        if __debug__:
            cprint('\b\b[WARN]', 'yellow', sep='', end='\t')
            print('Keyboard interrupt received')

