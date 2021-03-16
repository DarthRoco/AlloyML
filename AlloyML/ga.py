import pygad
import constants
import tensorflow as tf
from collections import OrderedDict
import numpy as np

global VAR,TARGET,MODEL,THRESHOLD

#From constants.py
MEANVALS=constants.meanconstant()
MAXVALS=constants.maxconstant()
MINVALS=constants.minconstant()

#Load appropriate model
def load_models(opn):
    if opn=='el':
        model = tf.keras.models.load_model('models/el.h5')
    elif opn=='ts':
        model = tf.keras.models.load_model('models/ts.h5')
    elif opn=='ys':
        model = tf.keras.models.load_model('models/ys.h5')
    return model


#Preprocess user input
def preprocess(arr,var,meanval):
    counter=0
    for key,value in var.items():
        var[key]=arr[counter]
        counter+=1
    for key,value in var.items():
        meanval[key]=var[key]
    values=[]
    for key,val in meanval.items():
        values.append(val)
    values=np.array(values)
    values=np.reshape(values,(1,26))
    return values

#Initialise OrderedDict for storing user input
def vars(arr):
    s={}
    for prop in arr:
        s[prop]=0
    return OrderedDict(s)

#Postprocess model output to human interpretable format
def postprocess(soln):
    global VAR
    answer={}
    solun={}
    for key in MEANVALS:
        solun[key]=MEANVALS[key]
    counter=0
    for key in VAR:
        solun[key]=soln[counter]
        counter+=1

    for key in MEANVALS:
        answer[key]=(solun[key]*(MAXVALS[key]-MINVALS[key]))+MINVALS[key]
    return OrderedDict(answer),OrderedDict(solun)

#Fitness function for the Genetic Algorithm
def fitness_func(solution, solution_idx):
    global VAR,MODEL,TARGET
    a=preprocess(solution,VAR,MEANVALS)
    prediction=float(MODEL.predict(a))
    mse=(TARGET-prediction)**2
    fitness = 1/(mse+0.001)
    return fitness

#Callback on generation end
def on_generation(ga_instance):
    global THRESHOLD
    fitness = ga_instance.best_solution()[1]
    if fitness>THRESHOLD:
        return 'stop'

#Initiate Genetic Algorithm.Return ga_instance
def initiate_ga(num_genes,num_generations=20,num_parents_mating=40,sol_per_pop=200,crossover_probability=0.5):
    params = {"fitness_func": fitness_func, 'num_generations': num_generations, 'num_parents_mating': num_parents_mating, 'sol_per_pop': sol_per_pop,
              'num_genes': num_genes, 'parent_selection_type': "sss",
              'init_range_low': 0, 'init_range_high': 1, 'crossover_probability': crossover_probability, 'mutation_type': "random",
              'mutation_probability': 0.5,
              'random_mutation_min_val': -0.50, 'random_mutation_max_val': +0.50,'on_generation': on_generation,'gene_space':{'low':0,'high':1}}
    ga_instance = pygad.GA(**params)
    return ga_instance

#Primary function.Takes user input and return theoretical composition for alloy with desired property
def ga_solver(target,variables,model,generations=20,threshold=100):
    global MODEL,TARGET,VAR,THRESHOLD
    MODEL=load_models(model)
    TARGET=target
    VAR=vars(variables)
    THRESHOLD=threshold
    ngene=len(VAR)
    ga=initiate_ga(ngene,num_generations=generations)
    ga.run()
    bs=ga.best_solution()[0]
    out=postprocess((bs))
    return out



