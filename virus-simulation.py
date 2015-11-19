# coding: utf-8
import numpy
import random
import pylab
import matplotlib.pyplot as plt


class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """


class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.
        maxBirthProb: Maximum reproduction probability (a float between 0-1)
        clearProb: Maximum clearance probability (a float between 0-1).
        """

        self.maxBirthProb = float(maxBirthProb)
        self.clearProb = float(clearProb)


    def getMaxBirthProb(self):
        """
        Returns the max birth probability.
        """
        return self.maxBirthProb

    def getClearProb(self):
        """
        Returns the clear probability.
        """
        return self.clearProb

    def doesClear(self):
        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step.
        returns: True with probability self.getClearProb and otherwise returns
        False.
        """
        if random.random() <= self.getClearProb():
            return True
        else:
            return False



    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.

        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """
        if random.random() <= self.maxBirthProb * (1.0 - popDensity):
            return SimpleVirus(self.getMaxBirthProb(),self.getClearProb())
        else:
            raise NoChildException('Didnt reproduce!')


class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the maximum virus population for this patient (an integer)
        """
        self.viruses = viruses
        self.maxPop = int(maxPop)

    def getViruses(self):
        """
        Returns the viruses in this Patient.
        """
        return self.viruses


    def getMaxPop(self):
        """
        Returns the max population.
        """
        return self.maxPop


    def getTotalPop(self):
        """
        Gets the size of the current total virus population.
        returns: The total virus population (an integer)
        """
        return float(len(self.viruses))


    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:

        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.

        - The current population density is calculated. This population density
          value is used until the next call to update()

        - Based on this value of population density, determine whether each
          virus particle should reproduce and add offspring virus particles to
          the list of viruses in this patient.

        returns: The total virus population at the end of the update (an
        integer)
        """
        survivors = list()
        for virus in self.getViruses():
            if not virus.doesClear():
                survivors.append(virus)

        popDensity = float(len(survivors))/float(self.getMaxPop())

        self.viruses = survivors

        new_viruses = list()
        for virus in self.getViruses():
            try:
                new_viruses.append(virus.reproduce(popDensity))
            except NoChildException:
                pass
        self.viruses += new_viruses

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

class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)

        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'srinol':False}, means that this virus
        particle is resistant to neither guttagonol nor srinol.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """

        SimpleVirus.__init__(self, float(maxBirthProb),float(clearProb))

        self.resistances = resistances
        self.mutProb = float(mutProb)

    def getResistances(self):
        """
        Returns the resistances for this virus.
        """
        return self.resistances

    def getMutProb(self):
        """
        Returns the mutation probability for this virus.
        """
        return self.mutProb

    def isResistantTo(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in TreatedPatient to determine how many virus
        particles have resistance to a drug.

        drug: The drug (a string)

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        try:
            if self.getResistances()[drug]:
                return True
            else:
                return False
        except:
            return False

    def reproduce(self, popDensity, activeDrugs):
        if all(self.isResistantTo(drug) == True for drug in activeDrugs) or not bool(activeDrugs):
            if random.random() <= self.getMaxBirthProb() * (1.0 - popDensity):
                mutated_resistances = dict()
                for key,value in self.resistances.iteritems():
                    if value:
                        if random.random() <= self.mutProb:
                            mutated_resistances[key] = False

                        else:
                            mutated_resistances[key] = True
                    else:
                        if random.random() <= self.mutProb:
                            mutated_resistances[key] = True

                        else:
                            mutated_resistances[key] = False
                return ResistantVirus(self.getMaxBirthProb(),self.getClearProb(), mutated_resistances, self.getMutProb())
            else:
                raise NoChildException('Didnt reproduce!')
        else:
            raise NoChildException('Didnt reproduce!')


class TreatedPatient(Patient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).

        viruses: The list representing the virus population (a list of
        virus instances)

        maxPop: The  maximum virus population for this patient (an integer)
        """
        Patient.__init__(self, viruses,maxPop)
        self.activeDrugs = list()


    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: The list of drugs being administered to a patient is updated
        """
        postcondition = set(self.activeDrugs)
        postcondition.add(newDrug)
        self.activeDrugs = list(postcondition)


    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """
        return self.activeDrugs


    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        count = 0
        for virus in self.viruses:
            condition = all([virus.isResistantTo(drug) for drug in drugResist])
            if condition:
                count += 1
        return count


    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly

        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Based on this value of population density, determine whether each
          virus particle should reproduce and add offspring virus particles to
          the list of viruses in this patient.
          The list of drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: The total virus population at the end of the update (an
        integer)
        """
        survivors = list()
        for virus in self.getViruses():
            if not virus.doesClear():
                survivors.append(virus)

        popDensity = float(len(survivors))/float(self.getMaxPop())

        self.viruses = survivors
        new_viruses = list()

        for virus in self.getViruses():
            try:
                new_virus = virus.reproduce(popDensity, self.getPrescriptions())
                new_viruses.append(new_virus)
            except NoChildException:
                pass
        self.viruses += new_viruses


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



# ## Running simulation
#
# #### simulation for 100 viruses with 0.1 prob of reproduction, 0.05 probability of clearing, no resistance to guttagonol, 0.005 prob of mutation, and 50 trials.
#simulationWithDrug(100,1000,0.1,0.05,{'guttagonol': False},0.005,50)
