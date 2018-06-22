
from PIL import Image
import tfcoreml as tf_converter

coreml_model = tf_converter.convert(tf_model_path = '/Users/john/ml-exercise/tf_files/retrained_graph.pb',
	mlmodel_path = 'MyModel.mlmodel',
	output_feature_names = ['final_result:0'],
	input_name_shape_dict = {'input:0':[1,224,224,4]},
	image_input_names = ['input:0'],
	class_labels = '/Users/john/ml-exercise/tf_files/retrained_labels.txt'
)



# python -m tensorflow.python.tools.optimize_for_inference \
# --input retrained_graph.pb \
# --output graph_optimized.pb \
# --input_names=input\
# --output_names=final_result


# Now we're ready to test out the CoreML model with a real image!
# Load an image
import PIL
import requests
from io import BytesIO
from matplotlib.pyplot import imshow
import numpy as np
# This is an image of a golden retriever from Wikipedia
# img_url = ''
# response = requests.get(img_url)
# img = PIL.Image.open(response.content)
# imshow(np.asarray(img))
im = Image.open("../../Desktop/mine.jpg")
# Run CoreML prediction
# Pay attention to '__0'. We change ':0' to '__0' to make sure 
# MLModel's generated Swift/Obj-C code is semantically correct
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