import os
from dotenv import load_dotenv
load_dotenv()
ironing_file = os.getenv('IRONING_FILE')
normal_file = os.getenv('NORMAL_FILE')
output_file = os.getenv('OUTPUT_FILE')
start_height = float(os.getenv('START_HEIGHT'))
layer_height = float(os.getenv('LAYER_HEIGHT'))

layers_to_iron = []

input_layer_num = int(input("What layer number do you want to iron?"))
layers_to_iron.append(input_layer_num)

# ironing_file = "ironing.gcode"
# normal_file = "no_ironing.gcode"
# output_file = "output.gcode"

# start_height = 0.3
# layer_height = 0.2

# layers_to_iron = [
    # 14,
# ]
layer_bounds = []
layer_positions_in_file = []
print(f"Start Height: {start_height}")
print(f"Layer Height: {layer_height}")
print(f"Layers to Iron: {layers_to_iron}\n")

start_layer = None
end_layer = None
for layer in layers_to_iron:
    # print("HOW MANY TIMES DOES THIS RUN?")  # JUST ONCE.. good
    start_layer = round(start_height + (layer-1)*layer_height , 1)
    end_layer = round(start_height + layer*layer_height, 1)
    layer_bounds.append([start_layer, end_layer])

f = open(ironing_file, "r")
file_contents = f.read().split("\n")

#print(f"HERE --> {layer_bounds}")  # ['0.30.20.20.20.20.20.20.20.20.20.20.20.20.20.20.20.20.20.20.20.20.20.20.20.2' ..
print("Searching GCODE file with ironing..")
for index, line in enumerate(file_contents):
    for bound in layer_bounds:
        if line.find(f"Z{bound[0]}") != -1 or line.find(f"Z{bound[1]}") != -1:
            if line[0:2] == "G0":
                layer_positions_in_file.append(index+1)
# print(layer_positions_in_file)  # empty here 
replacement_gcode = file_contents[layer_positions_in_file[0]-2:layer_positions_in_file[1]-2]  # ERROR : list index out of range
replacement_gcode_str = ""
for line in replacement_gcode:
    replacement_gcode_str = replacement_gcode_str + line + "\n"
replacement_gcode_str = replacement_gcode_str[:-1]

output_ironed_GCODE = False
if output_ironed_GCODE:
    f = open("layer_gcode.txt", "w")
    f.write(replacement_gcode_str)
    f.close()

f = open(normal_file, "r")
file_contents = f.read().split("\n")
layer_positions_in_file = []

print("Searching GCODE file without ironing..")
for index, line in enumerate(file_contents):
    for bound in layer_bounds:
        if line.find(f"Z{bound[0]}") != -1 or line.find(f"Z{bound[1]}") != -1:
            if line[0:2] == "G0":
                layer_positions_in_file.append(index+1)

print("Combining GCODE files..\n(this could take several minutes)")
start_of_file = file_contents[:layer_positions_in_file[0]-2]
end_of_file = file_contents[layer_positions_in_file[1]-2:]
replacement_gcode = replacement_gcode_str.split("\n")
reassembled_file_contents = ""

output_start_of_file = False
if output_start_of_file:
    start_of_file_str = ""
    for line in start_of_file:
        start_of_file_str = start_of_file_str + line + "\n"
    start_of_file_str = start_of_file_str[:-1]

    f = open("start_of_file.txt", "w")
    f.write(start_of_file_str)
    f.close()

output_end_of_file = False
if output_end_of_file:
    end_of_file_str = ""
    for line in end_of_file:
        end_of_file_str = end_of_file_str + line + "\n"
    end_of_file_str = end_of_file_str[:-1]

    f = open("end_of_file.txt", "w")
    f.write(end_of_file_str)
    f.close()

for line in start_of_file:
    reassembled_file_contents = reassembled_file_contents + line + "\n"
for line in replacement_gcode:
    reassembled_file_contents = reassembled_file_contents + line + "\n"
for line in end_of_file:
    reassembled_file_contents = reassembled_file_contents + line + "\n"
reassembled_file_contents = reassembled_file_contents[:-1]

f = open(output_file, "w")
f.write(reassembled_file_contents)
f.close()
print("\nFinished!")
