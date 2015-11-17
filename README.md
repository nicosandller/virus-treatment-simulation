# virus-treatment-simulation
#### A stochastic model to simulate virus spread on a patient.



simulationWithoutDrug(100, 1000, 0.1, 0.05, 50)

simulationWithDrug(100,1000,0.1,0.05,{'guttagonol': False},0.005,50)

| Method        | Description           | Arguments  |
| ------------- |:-------------:| ----------|
|`.add_cell(pos = (x,y))`| Adds an alive cell at the defined position| pos = (x,y) |
|`.insert_random_cells(n)`| Adds n alive cells at random positions| n = number |
|`.insert_blinker()`| Inserts a Blinker figure to the board at a random position| **Takes no argument** |
|`.insert_toad()`| Adds an alive cell at the defined position| **Takes no argument** |
|`.next()`| Moves one period in time to the next generation of cells| **Takes no argument** |
|`.show()`| Shows the board with living cells marked with an 'X'.| **Takes no argument** |


## Sample Code:

```python

simulationWithoutDrug(100, 1000, 0.1, 0.05, 50)

simulationWithDrug(100,1000,0.1,0.05,{'guttagonol': False},0.005,50)

```

## Screenshots:

<script src="https://gist.github.com/nicosandller/43e4a11f59017fa28925.js"></script>
