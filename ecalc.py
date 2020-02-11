#Module for energy calculation algorithm
import numpy as np
import math as math

# Returns a euclidean distance matrix between all pairs of atoms given the X, 
# Y, and Z coordinates for each atom.
def distance(df):
    x = np.array(df["X"]).astype(float)
    y = np.array(df["Y"]).astype(float)
    z = np.array(df["Z"]).astype(float)
    x = np.subtract.outer(x, x).T
    y = np.subtract.outer(y, y).T
    z = np.subtract.outer(z, z).T
    distance = np.sqrt(np.square(x) + np.square(y) + np.square(z))
    return distance

#Returns the 
def sigma(df):
    sigma = np.array(df["Sigma"]).astype(float)
    sigma = np.add.outer(sigma, sigma)
    sigma = np.divide(sigma, 2)
    return sigma

# Returns a simmetrical matrix of the epsilon value for all pairs of atoms. 
def epsilon(df):
    epsilon = np.array(df["Epsilon"]).astype(float)
    epsilon = np.multiply.outer(epsilon,epsilon)
    epsilon = np.sqrt(epsilon)
    return epsilon

# Returns an element-wise multiplication matrix of the charge for all pairs of atoms
def charge(df):
    charge = np.array(df["Charge"]).astype(float)
    charge = np.multiply.outer(charge,charge)
    return charge

# Returns the solvation energy as a sum of the element-wise product of the
# approximate atomic solvation parameter and accessable surface area.
def solvation(df):
    const = (0.2 * 4.0 * math.pi)
    asa = np.array(df["R"]).astype(float)
    asa = np.square(asa + 1.4).astype(float)
    asa = np.multiply(asa, const)
    asp = np.array(df["ASP"]).astype(float)
    solvation = np.multiply(asa, asp)
    return solvation

# Returns a matrix where each index of the input dataframe is paired with
# each element of the "Combined" column to insert zeros into a TRUE matrix, 
# creating a mask matrix.
def mask(df):
    nrow = df.shape[0]
    combined = np.array(df["Combined"])
    mask = np.full((nrow, nrow), 1)
    for i in range(nrow):
        x = combined[i]
        if x:
            for j in range(len(x)):
                y = x[j]
                mask[i,y] = 0
    return mask

# Currently computes the energy of one input dataframe. Full implementation will 
# take a list of protein objects and output a properly formatted text file. 
def energy(df):
    # Catch divide by zero and invalid value errors when running.
    with np.errstate(divide='ignore', invalid='ignore'):   
        sigma_div_dist = np.divide(sigma(df), distance(df))
        charge_div_dist = np.divide(charge(df), distance(df))
        x = np.multiply(epsilon(df), 
                        (np.power(sigma_div_dist, 12.0) - 
                         np.multiply(np.power(sigma_div_dist, 6.0), 2.0)))
        y = np.multiply(charge_div_dist, 
                        (1.0 / (4.0 * math.pi * 8.8541878128E-12 * 4.0)))
        flag = mask(df)
        vdw_matrix = x + y
        vdw_processed = np.multiply(flag, vdw_matrix)
        triangle = np.triu(vdw_processed, k=1)
        energy = np.sum(triangle) + np.sum(solvation(df))
        return energy
    
    
    
    