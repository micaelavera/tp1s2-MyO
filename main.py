import pharmacy

if __name__ == '__main__':
    pharmacy.readFiles()
    pharmacy.addVarConstraints()
    pharmacy.optimize()
    pharmacy.printSolution()