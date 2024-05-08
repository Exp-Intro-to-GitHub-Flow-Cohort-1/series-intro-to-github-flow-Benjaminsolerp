import gurobipy as gp
from gurobipy import GRB
from gurobipy import quicksum


# Crear el modelo
model = gp.Model("Optimización de Trozado de Árboles y Transporte de Rollizos")

# Conjuntos
rodales = range(45)
destinos = range(5)  # Solo consideramos los 5 destinos con demanda específica
productos = range(10)
reglas = range(2)
periodos = range(4)

# Parámetros
# Define tus parámetros aquí

# Demandas de los destinos
demandas = [124, 126, 127, 124, 123]

# Crear variables de decisión
x = model.addVars(productos, rodales, destinos, periodos, name="x", vtype=GRB.CONTINUOUS)
y = model.addVars(rodales, reglas, periodos, name="y", vtype=GRB.BINARY)
z = model.addVars(productos, destinos, periodos, name="z", vtype=GRB.CONTINUOUS)

# Restricciones
# Restricciones de demanda
for k in destinos:
    for t in periodos:
        model.addConstr(sum(x[i, j, k, t] for i in productos for j in rodales) == demandas[k])

# Restricciones de reglas de trozado
for j in rodales:
    for t in periodos:
        model.addConstr(sum(y[j, l, t] for l in reglas) == 1)

# Función objetivo
obj = quicksum(u[i, j, k] * x[i, j, k, t] for i in productos for j in rodales for k in destinos for t in periodos) + \
      quicksum(v[i, k] * z[i, k, t] for i in productos for k in destinos for t in periodos)

model.setObjective(obj, GRB.MAXIMIZE)

# Optimizar el modelo
model.optimize()

# Imprimir la solución
if model.status == GRB.OPTIMAL:
    for v in model.getVars():
        print('%s %g' % (v.varName, v.x))
    print('Objetivo: %g' % model.objVal)
else:
    print('No se encontró solución óptima')