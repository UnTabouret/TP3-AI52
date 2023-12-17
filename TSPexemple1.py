# Résolution du problème du voyageur de commerce ou TCS à l'aide du recuit simulé
# import de la librairie
import random
import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
import time

# Données du problème (générées aléatoirement)
ITERATIONS = 100
NOMBRE_DE_VILLES = 20
LARGEUR = 750
HAUTEUR = 500
MAX_DISTANCE = np.sqrt(pow(LARGEUR,2)+pow(HAUTEUR,2))
positionsVilles = []
for ville in range(NOMBRE_DE_VILLES):
    positionsVilles.append((random.randint(0,HAUTEUR),random.randint(0,LARGEUR)))

distances = np.zeros((NOMBRE_DE_VILLES, NOMBRE_DE_VILLES))
for ville in range(NOMBRE_DE_VILLES):
    for autreVille in range(ville+1,NOMBRE_DE_VILLES):
        distances[ville][autreVille] = np.sqrt(
            pow(positionsVilles[ville][0]-positionsVilles[autreVille][0],2)+
            pow(positionsVilles[ville][1]-positionsVilles[autreVille][1],2)
        )
        distances[autreVille][ville] = distances[ville][autreVille]
print('voici la matrice des distances entres les villes \n',distances)



def cal_distance(solution,distances,NOMBRE_DE_VILLES):
    eval_distance=0
    for i in range (len(solution)):
        origine,destination=solution[i],solution[(i+1)%NOMBRE_DE_VILLES]
        eval_distance+=distances[origine][destination]
    return eval_distance


def voisinage(solution,NOMBRE_DE_VILLES):
    echange=random.sample(range(NOMBRE_DE_VILLES),2)
    sol_voisine=solution
    (sol_voisine[echange[0]],sol_voisine[echange[1]])=(sol_voisine[echange[1]],sol_voisine[echange[0]])
    return sol_voisine
 
    
# recuit simulé
start_recuit = time.time()
meilleurs_recuit = []
solution=random.sample(range(NOMBRE_DE_VILLES),NOMBRE_DE_VILLES)
cout0=cal_distance(solution,distances,NOMBRE_DE_VILLES)
T=1000
facteur=0.99
T_intiale=MAX_DISTANCE/2
min_sol=solution
cout_min_sol=cout0
for i in range(ITERATIONS):
    print('la ',i,'�me solution = ',solution,' donne la distance totale= ',cout0,' la temp�rature actuelle =',T)
    meilleurs_recuit.append(cout0)
    T=T*facteur
    for j in range(50):
        nouv_sol=voisinage(solution*1,NOMBRE_DE_VILLES)
        cout1=cal_distance(nouv_sol,distances,NOMBRE_DE_VILLES)
      #  print('la ',j,'�me recherche de voisinage de',solution,'donne la solution=' ,nouv_sol,' distance totale= ',cout1)
        if cout1<cout0:
            cout0=cout1
            solution=nouv_sol
            if cout1<cout_min_sol:
                cout_min_sol=cout1
                min_sol=solution
        else:
            x=np.random.uniform()
            if x<np.exp((cout0-cout1)/T):
                cout0=cout1
                solution=nouv_sol
end_recuit = time.time()
time_recuit = end_recuit-start_recuit
print('voici la solution retenue ',min_sol,' et son coût ', cal_distance(min_sol,distances,NOMBRE_DE_VILLES))

def croisementSinglePoint(chromosome1,chromosome2):
    fils = [-1]*NOMBRE_DE_VILLES
    midpoint = int(NOMBRE_DE_VILLES/2)
    fils[:midpoint] = chromosome1[:midpoint]
    for i in range(midpoint,NOMBRE_DE_VILLES):
        j=0
        while chromosome2[j] in fils:
            j+=1
        fils[i] = chromosome2[j]
    return fils


def mutation(chromosome):
    fils = chromosome.copy()
    source = random.randint(0,NOMBRE_DE_VILLES-1)
    destination = random.randint(0,NOMBRE_DE_VILLES-1)
    fils[source],fils[destination]= fils[destination],fils[source]  
    return fils

#colonie de fourmis
start_fourmis = time.time()
meilleurs_fourmis = []
ALPHA = 0.9
BETA = 0.4
Q = 1
RHO = 0.1   
THETA_ZERO = .001
TAILLE_POPULATION_FOURMIS = 100 

trace = np.zeros((NOMBRE_DE_VILLES,NOMBRE_DE_VILLES))
deltaTrace = trace.copy()
trace += THETA_ZERO

def attractivity(origine,destination):
    return pow(trace[origine][destination],ALPHA) * pow(1/distances[origine][destination],BETA)

def chooseNextCity(fourmi):
    targetList = []
    attractivities = []
    for i in range(NOMBRE_DE_VILLES):
        if i in fourmi:continue
        targetList.append(i)
        attractivities.append(attractivity(fourmi[-1],i))
    return random.choices(population=targetList,weights=attractivities,k=1)


def deposerTrace(fourmi):
    longueur = cal_distance(fourmi,distances,NOMBRE_DE_VILLES)
    for i in range(NOMBRE_DE_VILLES-1):
        deltaTrace[fourmi[i]][fourmi[i+1]]+=Q/longueur
    
def evaporation():
    for row in trace:
        for element in row:
            element *= (1-RHO)


for i in range(ITERATIONS):
    populationFourmis = [[] for i in range(TAILLE_POPULATION_FOURMIS)]
    for fourmi in populationFourmis:
        fourmi.append(random.randint(0,NOMBRE_DE_VILLES-1))
        for j in range(NOMBRE_DE_VILLES-1):
            fourmi.append(chooseNextCity(fourmi)[0])
        deposerTrace(fourmi)
    evaporation()
    trace += deltaTrace
    deltaTrace = np.zeros((NOMBRE_DE_VILLES,NOMBRE_DE_VILLES))
    populationFourmis.sort(key = lambda x: cal_distance(x,distances,NOMBRE_DE_VILLES))
    meilleurs_fourmis.append(cal_distance(populationFourmis[0],distances,NOMBRE_DE_VILLES))

end_fourmis = time.time()
time_fourmis = end_fourmis-start_fourmis



#algo génétique
start_genetique = time.time()
meilleurs_genetique = []
baseChromosome = list(range(NOMBRE_DE_VILLES))
TAILLE_POPULATION_GENETIQUE = 500
populationGenetique = []
for i in range(TAILLE_POPULATION_GENETIQUE):
    random.shuffle(baseChromosome)
    newChromosome = baseChromosome.copy()
    populationGenetique.append(newChromosome)
print("Population initiale génétique : ",populationGenetique)

for i in range(ITERATIONS):
    populationGenetique.sort(key = lambda x: cal_distance(x,distances,NOMBRE_DE_VILLES))
    meilleurs_genetique.append(cal_distance(populationGenetique[0],distances,NOMBRE_DE_VILLES))
    populationGenetique = populationGenetique[:TAILLE_POPULATION_GENETIQUE-1]
    for i in range(TAILLE_POPULATION_GENETIQUE):
        populationGenetique.append(mutation(populationGenetique[i]))
        populationGenetique.append(croisementSinglePoint(populationGenetique[i],populationGenetique[(i+1)%TAILLE_POPULATION_GENETIQUE]))

end_genetique = time.time()
time_genetique = end_genetique-start_genetique

for individu in populationGenetique:
    print("Path : ",individu, " with distance : ",cal_distance(individu,distances,NOMBRE_DE_VILLES))


def create_circle(x, y, r, canvas): #center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvas.create_oval(x0, y0, x1, y1,fill = "white")

def tracerChemin(etapes,canvas,color="black",width=1):
    for i in range(1,len(etapes)):
        positionVille1 = positionsVilles[etapes[i-1]]
        positionVille2 = positionsVilles[etapes[i]]
        canvas.create_line(positionVille1[1],positionVille1[0],positionVille2[1],positionVille2[0],fill=color,width = width)

top = tk.Tk()
graph = tk.Canvas(top, bg="white", height=HAUTEUR, width=LARGEUR)
graph.pack()


#Dessin chemin
tracerChemin(min_sol,graph,"red",15)
tracerChemin(populationGenetique[0],graph,"green",10)
tracerChemin(populationFourmis[0],graph,"blue",5)

#Dessin villes
i=0
for ville in positionsVilles:
    create_circle(ville[1],ville[0],10,graph)
    graph.create_text(ville[1],ville[0],text=i)
    i+=1

print("Temps pour recuit, genetique, fourmis : ",time_recuit,time_genetique,time_fourmis)

#Plotting
xpoints = np.array(range(ITERATIONS))
plt.plot(xpoints,np.array(meilleurs_recuit),'r')
plt.plot(xpoints,np.array(meilleurs_genetique),'g')
plt.plot(xpoints,np.array(meilleurs_fourmis),'b')
plt.show()


graph.pack()
graph.mainloop()