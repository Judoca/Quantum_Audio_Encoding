# Quantum Audio Encoding

# Generating an mp3

from pydub.generators import Sine
import random

# Generate a random frequency between 200 Hz and 2000 Hz
random_frequency = random.randint(200, 2000)

# Create a 3-second sine wave
sine_wave = Sine(random_frequency).to_audio_segment(duration=1000)

# Export the audio as an MP3 file
sine_wave.export("random_audio.mp3", format="mp3")

print("Random audio sample saved as random_audio.mp3")

#-----------------------------------------------------------------------------------


# Converting mp3 to binary data

# Open the MP3 file in binary mode and read its contents
with open("random_audio.mp3", "rb") as mp3_file:
    binary_data = mp3_file.read()

# Convert binary data into a string of binary values (bits)
binary_values = ''.join(format(byte, '08b') for byte in binary_data)

# Print the first 100 bits of the binary data
print("Binary data (first 100 bits):", binary_values[:100])

# Print the binary data
# print("Binary data: ", binary_values)


# Optionally save the binary data (as raw bytes) to another file
with open("mp3_binary_data.bin", "wb") as binary_output:
    binary_output.write(binary_data)

print("MP3 file successfully converted to binary!")



#-----------------------------------------------------------------------------------


# Converting to q bits



import sys
sys.path.append("/home/justin/.local/lib/python3.12/site-packages")
from qiskit import QuantumCircuit, transpile, assemble
from qiskit_aer import Aer
# from qiskit.execute_function import execute

#from qiskit import QuantumCircuit, Aer, transpile, execute
from qiskit.quantum_info import Statevector
import numpy as np
#from qiskit.providers.aer import AerSimulator
from qiskit_aer import AerSimulator

# Function to prepare an entangled Bell state
def prepare_bell_state():
    qc = QuantumCircuit(2)
    qc.h(0)  # Apply Hadamard gate on qubit 0
    qc.cx(0, 1)  # Apply CNOT gate with qubit 0 as control and qubit 1 as target
    return qc

# Function to encode 2 classical bits into a qubit
def encode_bits(qc, bits):
    if bits == "01":
        qc.x(0)  # Apply Pauli-X gate
    elif bits == "10":
        qc.z(0)  # Apply Pauli-Z gate
    elif bits == "11":
        qc.x(0)  # Apply Pauli-X gate
        qc.z(0)  # Apply Pauli-Z gate
    # No operation for "00" (Identity)
    return qc

# Function to decode the Bell state and retrieve classical bits
def decode_bell_state():
    qc = QuantumCircuit(2)
    qc.cx(0, 1)  # Apply CNOT gate
    qc.h(0)  # Apply Hadamard gate
    return qc

# Main function to encode and simulate superdense coding
def superdense_coding(binary_data):
    # Group binary data into pairs of 2 bits
    pairs = [binary_data[i:i+2] for i in range(0, len(binary_data), 2)]
    
    results = []
    for pair in pairs:
        # Step 1: Prepare the entangled Bell state
        qc = prepare_bell_state()
        
        # Step 2: Encode the classical bits into the qubit
        qc = encode_bits(qc, pair)
        
        # Step 3: Decode the Bell state to verify
        qc.compose(decode_bell_state(), inplace=True)
        
        print(qc)
        
        #print(simulator.available_methods)
        
        # Simulate the statevector using Statevector class
        statevector = Statevector.from_instruction(qc)
        
        # Measure the classical bits (post-simulation analysis)
        classical_bits = measure_classical_bits(statevector)
        results.append(classical_bits)
        

        
    
    return results

# Function to measure classical bits from statevector
def measure_classical_bits(statevector):
    # Decode statevector into classical bits
    probabilities = np.abs(statevector) ** 2
    index = np.argmax(probabilities)
    classical_bits = f"{index:02b}"  # Convert index to 2-bit binary
    return classical_bits

# Example usage
if __name__ == "__main__":
    # Example binary data from an MP3 file
    #binary_data = "1100101010110001"  # Replace with actual MP3 binary data
    binary_data = binary_values  # Replace with actual MP3 binary data
    
    # Perform superdense coding
    results = superdense_coding(binary_data)
    print("Encoded and Decoded Bits:", results)
    
    # Print the number of qubits required
    num_qubits = len(results)
    print(f"Number of qubits required to store {len(binary_data)} classical bits: {num_qubits}")

    # Print the number of classical bits in the original data
    print(f"Number of classical bits in the original data: {len(binary_data)}")
    

