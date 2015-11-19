from virus import *
from patient import *
import pylab

def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
                          numTrials):
    """
    Run the simulation and plot the graph for problem 3 (no drugs are used,
    viruses do not have any drug resistance).
    For each of numTrials trial, instantiates a patient, runs a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.

    numViruses: number of SimpleVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)
    clearProb: Maximum clearance probability (a float between 0-1)
    numTrials: number of simulation runs to execute (an integer)
    """
    averages = [0.0 for x in range(300)]
    for trial in range(numTrials):
        patient_zero = Patient([SimpleVirus(maxBirthProb, clearProb) for virus in range(numViruses)],maxPop)

        for timestep in range(300):
            patient_zero.update()
            averages[timestep] += patient_zero.getTotalPop()

    averages = [x/numTrials for x in averages]

    pylab.figure()
    pylab.legend(['viruses'])
    pylab.title('SimpleVirus simulation')
    pylab.xlabel('Time Steps')
    pylab.ylabel('Average Virus Population')
    pylab.plot(range(300), averages)
    pylab.show()


#simulationWithoutDrug(100, 1000, 0.1, 0.05, 50)


def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb, numTrials):
    """
    For each of numTrials trials, instantiates a patient, runs a simulation for
    150 timesteps, adds guttagonol, and runs the simulation for an additional
    150 timesteps.  At the end plots the average virus population size
    (for both the total virus population and the guttagonol-resistant virus
    population) as a function of time.

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)
    clearProb: maximum clearance probability (a float between 0-1)
    resistances: a dictionary of drugs that each ResistantVirus is resistant to
                 (e.g., {'guttagonol': False})
    mutProb: mutation probability for each ResistantVirus particle
             (a float between 0-1).
    numTrials: number of simulation runs to execute (an integer)

    """
    averages = [0.0 for x in range(300)]
    guttagonol_averages = [0.0 for x in range(300)]

    for trial in range(numTrials):
        viruses = list()
        for item in range(numViruses):
            viruses.append(ResistantVirus(maxBirthProb, clearProb, resistances, mutProb))
        patient = TreatedPatient(viruses,maxPop)


        for timestep in range(150):
            patient.update()
            averages[timestep] += patient.getTotalPop()
            guttagonol_averages[timestep] += patient.getResistPop(['guttagonol'])

        patient.addPrescription('guttagonol')
        for timestep in range(150,300):
            patient.update()
            averages[timestep] += patient.getTotalPop()
            guttagonol_averages[timestep] += patient.getResistPop(['guttagonol'])

    averages = [x/numTrials for x in averages]
    guttagonol_averages = [x/numTrials for x in guttagonol_averages]

    pylab.title('Treatment simulation')
    pylab.xlabel('Time Steps')
    pylab.ylabel('Average Virus Population')
    pylab.plot(range(300), averages, 'b--', label='Total Population')
    pylab.plot(range(300), guttagonol_averages, '-r', label='Guttagonol Population')
    pylab.legend()
    pylab.show()

#simulationWithDrug(100,1000,0.1,0.05,{'guttagonol': False},0.005,50)
