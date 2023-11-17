import torch


def convert_weights(bin_path, ot_path):
    # Load the state dictionary from the .bin file
    state_dict = torch.load(bin_path, map_location=torch.device('cpu'))

    # Save the state dictionary in .ot format
    torch.save(state_dict, ot_path)


# Define the paths to the input and output files
bin_path = 'model/pytorch_model.bin'
ot_path = 'model/pytorch_model.pt'

# Convert the weights
convert_weights(bin_path, ot_path)
