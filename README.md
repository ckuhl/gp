# Genetic Programming
Define the problem and expected outputs, and a solution will be evolved to
solved the defined problem.


## Quickstart
Call `make setup` to set up the virtual environment and then `make debug` to
watch it start churning away at an example problem.


## Project Info
- `requirements.txt` containts the requirements
- tests in `./tests`, can be run using `make test`
- to run the program call `make run` or `make debug`
- documentation in `./docs`, can be updated using `make docs`


## Useful Tools
`python -m cProfile -s tottime gp/__main__.py` profile, sorted by total time
in each function.

To profile a specific function:
```python
import pprofile
profiler = pprofile.Profile()
with profiler:
    ...
```
and then start it from the command line as such: 
`pprofile --threads 0 main.py`

## To do
- [ ] change gene.run into a generator
  - i.e. terminate as soon as sufficient output is generated
- [ ] make generation running async
  - each gene.run is _not_ dependant on any other
- [ ] create a custom logging formatter to colourize "WARN", etc.
- [ ] add a few utility classes to making typing simpler
  - i.e. make it harder to mess up what we're returning
