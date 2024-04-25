# Warning
---
**In development**

This project is por my own TFM for my Master's Degree in Artificial Intelligence. So it should not be copied or used before 08/2024.


# Artificial Intelligence
---
As part of this final project for my Master, I have develop an Automodelizer CNN, using genetic algorithms in order to search the best architecture. Read `TFM.docx` in order to learn more about it.

## Interface
---
As part of this final project for my Master, I have develop an Interface to let the user use this Automodelizer, letting him to modify some parameters as the number od descendants, number of epochs....Read `TFM.docx` in order to learn more about it.

## Project Structure
---
- `python`: hold the python server with the Automodelizer.
- `web`: Holds the user interface of the app, implemented in React.
- `AutoModelizer.ipynb`: a jupyer notebook with all the information and development of the Automodelizer with some use examples.

## Installation
---
To test the application locally, follow these steps:

### Install User Interface Dependencies

1. Navigate to the `questionary` directory:
   ```sh
   cd web   
    ```
2. Install dependencies with npm:
```sh 
    npm install
```
3.(Optional) Install concurrently to run both servers at the same time:
```sh
   npm install concurrently
```

## Install Python Server Dependencies
---
Navigate to the `python` directory and install the libraries:

```sh
    cd python
    pip install -r requirements.txt
```

## To Use With Docker and K8s enviroment
---
### Mac

First of all be sure that you have installed and available a k8s enviroment, and be sure that Docker is running:

```bash
brew install minikube
minikube start
```

### Windows
First of all be sure that you have installed and available a k8s enviroment, and be sure that Docker is running
```bash
winget install Kubernetes.minikube
winget install Kubernetes.kubectl
exit
```
Open CMD or Powershell again:
```bash
minikube start
```

### Both
After You have installed both of them, lets use our application:
```bash
docker-compose up -d
```

To use k8s use:

**This section are going to be completed...** 


## Usage
---

To test the application, navigate to the questionary directory and use one of the following commands:
From `/web`

* `npm start`: Runs only the React server.
* `npm run both`: Runs both servers, React and Python.(need to have installed `npm install concurrently` )

## Contributing

If you wish to contribute to the project, please fork the repository, make your changes in your fork, and then submit a pull request.

## License

This project is licensed under the [Creative Commons Attribution-NonCommercial 4.0 International Public License](./LICENSE).
