# virus-treatment-simulation
#### A stochastic model to simulate virus spread on a patient.


### Simple simulation function without drugs:
simulationWithoutDrug(viruses, maxPop, maxBirthProb, clearProb, trials)

- viruses: list of viruses
- maxPop: maximum population of viruses in the patient
- maxBirthProb: probability of reproduction for a virus
- clearProb: probability of decay for virus
- trials: trials to run and average simulation


### Complex simulation function with drug treatment:
simulationWithDrug(viruses,maxPop,maxBirthProb,clearProb,resistances,mutProb,trials)
  - resistances: dictionary of resistances for viruses
  - mutProb: probabuility of virus mutation in each time step


### TreatedPatient(viruses,maxPop)
  
| Method        | Description           | Arguments  |
| ------------- |:-------------:| ----------|
|`.addPrescription(drug)`| Adds a drug to patient, takes drug as string| pos = 'ibuprofen' |
|`.getPrescriptions()`| Returns drugs in patient| **Takes no argument** |
|`.getResistPop(drugResist)`| Returns the number of viruses that resist all of drugs in the arguement list| drugResist =['ibuprofen','octamox']|
|`.update()`| Update the state of the virus population in this patient for a single time step| **Takes no argument**|


## Sample Code:

```python

simulationWithoutDrug(100, 1000, 0.1, 0.05, 50)

simulationWithDrug(100,1000,0.1,0.05,{'guttagonol': False},0.005,50)

```

## Screenshots:
visit https://gist.github.com/nicosandller/43e4a11f59017fa28925 for a Gist. Scroll to the bottom to see the results of the simulation!

