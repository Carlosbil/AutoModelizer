import numpy as np
import torch
from torch.utils.data import DataLoader, Dataset
import torchvision
import torchvision.datasets as datasets
import torchvision.transforms as transforms
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader, random_split
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import pandas as pd
from sklearn.model_selection import train_test_split
from customDataset import CustomDataset
import random
from tqdm import tqdm
from torchsummary import summary
import os
class Genetic:
    def __init__(self, num_classes):
        # DATOS DEL DATASET DE PRUEBA CIFAR 100
        self.num_channels = 3 # escala de colores
        self.px_h = 32
        self.px_w = 32
        self.batch_size = 128
        self.num_classes = num_classes

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Preparar los DataLoader para los conjuntos de entrenamiento y validación
        self.transform = transforms.Compose([
            transforms.Resize((self.px_h, self.px_w)),
            transforms.ToTensor(),
            transforms.Normalize((0.5,), (0.5,))
        ])
        self.learning_rates = [0.1, 0.01, 0.001, 0.0001, 0.00001, 0.000001]
        self.filter_range = [8,16,32,64,128]
        self.kernel_size_range = [1,3,5,7] 
        self.population_size = 4
        self.min_conv_layers = 1
        self.max_conv_layers = 3
        self.min_filters = 16
        self.max_filters = 128
        self.kernel_sizes = [3, 5]
        self.top_models = []

    def use_grey(self):
        self.num_channels = 1 # escala de grises
        self.px_h = 28
        self.px_w = 28
        self.batch_size = 32

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Preparar los DataLoader para los conjuntos de entrenamiento y validación
        self.transform = transforms.Compose([
            transforms.Resize((self.px_h, self.px_w)),
            transforms.Grayscale(num_output_channels=self.num_channels),
            transforms.ToTensor(),
            transforms.Normalize((0.5,), (0.5,))
        ])
    
    def load_data(self, csv_path):
        # Cargamos el CSV
        data = pd.read_csv(csv_path)

        # Dividimos en entrenamiento y testeo
        train_data, val_data = train_test_split(data, test_size=0.2, random_state=22)

        # Crear datasets personalizados
        train_dataset = CustomDataset(train_data, transform=self.transform)
        val_dataset = CustomDataset(val_data, transform=self.transform)

        # Crear DataLoader para los datasets
        train_loader = DataLoader(dataset=train_dataset, batch_size=self.batch_size, shuffle=True)
        val_loader = DataLoader(dataset=val_dataset, batch_size=self.batch_size, shuffle=False)

        return train_loader, val_loader
    
    def load_data_image(self, root_path):
        # Cargar conjuntos de datos de entrenamiento y validación (prueba)
        train_path = os.path.join(root_path, "train")
        test_path = os.path.join(root_path, "test")

        train_dataset = ImageFolder(root=train_path, transform=self.transform)
        test_dataset = ImageFolder(root=test_path, transform=self.transform)

        # Crear DataLoader para los datasets
        train_loader = DataLoader(dataset=train_dataset, batch_size=self.batch_size, shuffle=True)
        test_loader = DataLoader(dataset=test_dataset, batch_size=self.batch_size, shuffle=False)

        return train_loader, test_loader
    
    def load_data_image_not_splitted(self, csv_path):
        # Cargamos el dataset
        dataset = ImageFolder(root=csv_path, transform=self.transform)

        # Calcular el tamaño del conjunto de validación
        val_size = int(0.2 * len(dataset))
        train_size = len(dataset) - val_size

        # Dividir el dataset en entrenamiento y validación
        train_dataset, val_dataset = random_split(dataset, [train_size, val_size])

        # Crear DataLoader para los datasets
        train_loader = DataLoader(dataset=train_dataset, batch_size=self.batch_size, shuffle=True)
        val_loader = DataLoader(dataset=val_dataset, batch_size=self.batch_size, shuffle=False)

        return train_loader, val_loader
    
    
    def check_cuda(self):
        if torch.cuda.is_available():
            print("CUDA (GPU) está disponible en tu sistema.")
        else:
            print("CUDA (GPU) no está disponible en tu sistema.")
            
    def build_cnn_from_individual(self, individual):
        """ 
        Funcion para construir un modelo en base a un diccionario
        """
        layers = []
        num_layers = individual['num_conv_layers']
        fully_connected = int(individual['fully_connected'])
        dropout = individual['dropout']
        out_channels_previous_layer = self.num_channels

        for i in range(num_layers):
            out_channels = individual['filters'][i]
            kernel_size = individual['kernel_sizes'][i]
            
            conv_layer = nn.Conv2d(out_channels_previous_layer, out_channels, kernel_size=kernel_size, padding=1)
            layers.append(conv_layer)
            if out_channels_previous_layer > 1 or i > 0:
                layers.append(nn.BatchNorm2d(out_channels))
            layers.append(nn.ReLU())
            if i < 1:
                layers.append(nn.MaxPool2d(kernel_size=2, stride=2))
            else:
                layers.append(nn.MaxPool2d(kernel_size=2, stride=1))


            out_channels_previous_layer = out_channels


        # Temporalmente crear un modelo para calcular el tamaño de salida de las capas convolucionales
        temp_model = nn.Sequential(*layers)

        # Calcular el tamaño de salida usando un tensor dummy
        dummy_input = torch.zeros(1, self.num_channels, self.px_h, self.px_w)
        output_size = temp_model(dummy_input).view(-1).shape[0]

        # Ahora, sabiendo el tamaño de salida, podemos definir las capas lineales correctamente
        layers.append(nn.Flatten())

        for i in range(fully_connected):
            layers.append(nn.Linear(in_features=output_size, out_features=output_size))
            if dropout > 0:
                layers.append(nn.Dropout(0.2))
                dropout-= 1

        layers.append(nn.Linear(output_size, self.num_classes))
        return nn.Sequential(*layers)
    
    def generate_individual(self, min_conv_layers, max_conv_layers, min_filters, max_filters, kernel_sizes):
        """ 
        Funcion para generar un diccionario que representa a una arquitectura
        """
        individual = {
            'num_conv_layers': random.randint(min_conv_layers, max_conv_layers),
            'filters': [],
            'kernel_sizes': [],
            'learning_rate': random.choice(self.learning_rates),
            'fully_connected': random.randint(0,2),
            'dropout': random.randint(0,2)
        }

        for _ in range(individual['num_conv_layers']):
            individual['filters'].append(random.choice(self.filter_range))
            individual['kernel_sizes'].append(random.choice(self.kernel_size_range))
        
        # Agrega más parámetros según sea necesario, como capas completamente conectadas, etc.

        return individual

    def initialize_population(self):
        return [self.generate_individual(self.min_conv_layers, self.max_conv_layers, self.min_filters, self.max_filters, self.kernel_sizes) for _ in range(self.population_size)]


    def evaluate_individual(self,individual, train_loader, val_loader, device='cuda', epochs=5):
        """ 
        Funcion para entrenar y evaluar una arquitectura
        """
        # Construir el modelo basado en el individuo
        model = self.build_cnn_from_individual(individual).to(device)
        
        # Definir el optimizador y la función de pérdida
        # HACER QUE EL OPTIMIZADOR SEA OTRO GEN!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        optimizer = torch.optim.Adam(model.parameters(), lr=individual['learning_rate'])
        criterion = nn.CrossEntropyLoss()

        # Entrenamiento
        for epoch in range(epochs):
            model.train()
            progress_bar = tqdm(total=len(train_loader), desc=f'Epoch {epoch+1}/{epochs}', unit='batch')
            for data, targets in train_loader:
                data, targets = data.to(device), targets.to(device)
                optimizer.zero_grad()
                output = model(data)
                loss = criterion(output, targets)
                loss.backward()
                optimizer.step()

                # Actualizar la barra de progreso con la última información de pérdida
                progress_bar.set_postfix({'training_loss': '{:.3f}'.format(loss.item())})
                progress_bar.update()  # Forzar la actualización de la barra de progreso
                
            progress_bar.close()  # Cerrar la barra de progreso al final de cada época

        # Evaluación
        model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for data, targets in val_loader:
                data, targets = data.to(device), targets.to(device)
                outputs = model(data)
                _, predicted = torch.max(outputs.data, 1)
                total += targets.size(0)
                correct += (predicted == targets).sum().item()

        accuracy = correct / total
        return accuracy  # Esta es la "aptitud" del individuo
    
    def mutate_individual(self,individual):
        """
        Mutar un individuo cambiando aleatoriamente sus hiperparámetros.
        """
        mutation_rate = 0.3  # Probabilidad de mutar cada característica
        fully_connected_range = (0,5) #Rango para ver cuantas fully conected se añaden

        if random.random() < mutation_rate:
            # Mutar la tasa de aprendizaje
            individual['learning_rate'] = random.choice(self.learning_rates)


        # Asegurarse de que hay suficientes entradas en las listas 'filters' y 'kernel_sizes'
        for i in range(individual['num_conv_layers']):
            if random.random() < mutation_rate:
                # Mutar el número de filtros en la capa i
                individual['filters'][i] = random.choice(self.filter_range)
            if random.random() < mutation_rate:
                # Mutar el tamaño de filtro en la capa i
                individual['kernel_sizes'][i] = random.choice(self.kernel_size_range)

        if random.random() < mutation_rate:
            # Mutar la tasa de aprendizaje
            num_fully = random.randint(*fully_connected_range)
            individual['fully_connected'] = num_fully
            individual['dropout'] = random.randint(0, num_fully)
        return individual
    
    def crossover(self,parent1, parent2):
        """
        Realiza un cruce uniforme entre dos individuos.
        
        Args:
            parent1 (dict): El primer individuo padre.
            parent2 (dict): El segundo individuo padre.
        
        Returns:
            dict: Un nuevo individuo hijo.
        """
        child = {}
        for key in parent1:
            if key == "filters" or key == "kernel_sizes":
                if random.random() < 0.5:
                    child["filters"] = parent1["filters"]
                    child["kernel_sizes"] = parent1["kernel_sizes"]
                else:
                    child["filters"] = parent2["filters"]
                    child["kernel_sizes"] = parent2["kernel_sizes"]

            else:
                if key != "num_conv_layers":
                    if random.random() < 0.5:
                        child[key] = parent1[key]
                    else:
                        child[key] = parent2[key]
        child["num_conv_layers"] = len(child["filters"])

        return child

    def evaluate_population(self,population, train_loader, val_loader, device, epochs):
        """
        Funcion para evaluar a una poblacion de arquitecturas
        """
        fitness_scores = []
        
        for individual in population:
            print(individual)
            fitness = self.evaluate_individual(individual, train_loader, val_loader, device, epochs)
            fitness_scores.append(fitness)
        
        # sacamos los scores de la poblacion
        return fitness_scores
    
    def tournament_selection_best5(self,population):
        """
        Selecciona los 4 mejores individuos de la población mediante un torneo de tamaño fijo.

        Args:
            population: La lista de individuos con sus puntuaciones de fitness.

        Returns:
            Lista de los 4 mejores individuos.
        """
        winners = []
        for _ in range(3):
            candidates = random.sample(population, 2)
            winner = max(candidates, key=lambda x: x['fitness'])
            winners.append(winner)
        return winners
    

    def genetic_algorithm(self,population, train_loader, val_loader, device, max_desc, epochs):
        """ 
        Algoritmo genetico para evolucionar una poblacion de arquitecturas hacia la mejor puntuacion dado un dataset dado
        """
        desc = 0
        while desc < max_desc:
            print("***************************************")
            print()
            print(f"Generation: {desc}")
            print()
            print("***************************************")
            puntuaciones_aptitud = self.evaluate_population(population, train_loader, val_loader, device, epochs)

            # Ordenamos individuos
            # Añadimos las puntuaciones directamente a cada diccionario de la población
            for i, puntuacion in enumerate(puntuaciones_aptitud):
                population[i]['fitness'] = puntuacion

            population.sort(key=lambda x: x['fitness'], reverse=True)

            # Preservamos el mejor individuo (elitismo)
            mejor_individuo = population[0]
            self.top_models.append(mejor_individuo)
            # Seleccionamos los 4 mejores (excluyendo el mejor) para el torneo
            winners = self.tournament_selection_best5(population[1:])
            print(f"Los 4 mejores son: \n {winners}")

            # Realizamos cruce y mutación con descendientes que reemplazan a la población restante
            for i in range(1, 2):
                descendency = self.mutate_individual(self.crossover(winners[i-1], winners[i]))
                population[-i] = descendency   # Eliminamos las peores arquitecturas
            
            # Nos aseguramos que mantenemos el mejor de todos
            population[0] = mejor_individuo
            desc += 1

        return population

    def best_model(self):
        model = self.build_cnn_from_individual(self.top_models[len(self.top_models)-1])
        model = model.to(self.device)
        summary(model, (self.num_channels, self.px_h, self.px_w))