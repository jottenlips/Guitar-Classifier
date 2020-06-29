
from PIL import Image
import tfcoreml as tf_converter

coreml_model = tf_converter.convert(tf_model_path = '/Users/johnottenlips/ml-exercise/tf_files/retrained_graph.pb',
	mlmodel_path = 'MyModel.mlmodel',
	output_feature_names = ['final_result:0'],
	input_name_shape_dict = {'input:0':[1,224,224,4]},
	image_input_names = ['input:0'],
	class_labels = '/Users/johnottenlips/ml-exercise/tf_files/retrained_labels.txt',
	image_scale=2/255.0,
red_bias=-1,
green_bias=-1,
blue_bias=-1
)



# python -m tensorflow.python.tools.optimize_for_inference \
# --input retrained_graph.pb \
# --output graph_optimized.pb \
# --input_names=input\
# --output_names=final_result



import PIL

import numpy as np

im = Image.open("../../Desktop/mustang.jpg")

final_size = 224;
size = im.size
ratio = float(final_size) / max(size)
new_image_size = tuple([int(x*ratio) for x in size])
im = im.resize(new_image_size, Image.ANTIALIAS)
new_im = Image.new("RGB", (final_size, final_size))
coreml_inputs = {'input__0': new_im}
coreml_output = coreml_model.predict(coreml_inputs, useCPUOnly=False)
probs = coreml_output['final_result__0']
label_idx = np.argmax(probs)

# This label file comes with the model
# label_file = '/Users/john/ml-exercise/tf_files/retrained_labels.txt' 
# with open(label_file) as f:
#     labels = f.readlines()
print(probs)