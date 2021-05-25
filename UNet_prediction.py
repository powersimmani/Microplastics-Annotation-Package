import code
import torch,cv2, torchvision
from PIL import Image
from torchvision.transforms import transforms
from torchvision.transforms.functional import crop
from torchvision.utils import save_image
import segmentation_models_pytorch as smp
import numpy as np
from segmentation_models_pytorch.utils import metrics, losses

def SizeAdjustment(pil_img, patch_size=256):
	"""
	Addition of width and height if the original image is not divisible by 256. 
	(Added regions are black in color.)
	"""
	w, h = pil_img.size
	if w % patch_size == 0 and h % patch_size == 0:	# The width and height of the image are divisible by 256.
		return pil_img

	added_w, added_h = 0, 0

	if w % patch_size != 0:
		added_w = patch_size - (w % patch_size)
		w += added_w
	if h % patch_size != 0:
		added_h = patch_size - (h % patch_size)
		h += added_h

	new_img = Image.new(pil_img.mode, (w, h), (0, 0, 0))
	new_img.paste(pil_img)
	return new_img, added_w, added_h


def predict(model, original_image, parameterPath, patch_size=256, threshold=0.5):
	"""
	flPath
	"""
	device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
	
	# Initialize the model with saved parameters
	#loaded_state = torch.load(model_path+seq_to_seq_test_model_fname,map_location='cuda:0'
	try:
		model.load_state_dict(torch.load(parameterPath,map_location='cuda:0'))
	except:
		model.load_state_dict(torch.load(parameterPath,map_location='cpu'))
		device = torch.device('cpu')

	print(device)
	model.to(device)
	model.eval()

	T = transforms.Compose([transforms.ToTensor(),
							transforms.Normalize(
							mean=[0.1034, 0.0308, 0.0346],
							std=[0.0932, 0.0273, 0.0302])])

	#fl = Image.open(flPath).convert('RGB')	# PIL Image
	#fl = Image.open("023_fl.png").convert('RGB')	# PIL Image

	fl, added_w, added_h = SizeAdjustment(original_image, patch_size=patch_size)
	w, h = fl.size

	prediction = None

	for y in range(0, h, patch_size):
		row = None
		for x in range(0, w, patch_size):
			fl_patch = crop(fl, y, x, patch_size, patch_size)

			p_patch = ((model(T(fl_patch).unsqueeze(0).to(device, dtype=torch.float32))) > threshold).float().squeeze(0)	# Predicted mask patch
			
			if x + patch_size == w and y + patch_size == h:		# If there are added black region on both right and bottom side, cut them out.
				p_patch = p_patch[:, :patch_size - added_h, :patch_size - added_w]
			elif x + patch_size == w:		# If there are added black region on the right side, cut it out.
				p_patch = p_patch[:, :, :patch_size - added_w]
			elif y + patch_size == h:		# If there are added black region on the bottom side, cut it out.
				p_patch = p_patch[:, :patch_size - added_h, :]

			if row is None:
				row = p_patch
			else:	
				row = torch.cat((row, p_patch), dim=2)	# Appending patches from left to right, forming a row

		if prediction is None:
			prediction = row
		else:
			prediction = torch.cat((prediction, row), dim=1)	# Appending predicted patches row by row

	return (~(prediction.bool())).float().cpu().numpy().astype(np.uint8) # Prediction mask as torch.tensor with MP represented as 0., which is black when saved as PNG file.


def UNet(ori_image, model = None, parameterpath = None):
	#import time
	#start_time = time.time()
	ori_image=Image.fromarray(ori_image)
	if model == None:
		model = smp.Unet("resnet101", in_channels=3, classes=1, encoder_weights="imagenet")
		parameterPath = "./best_model/best_model.pth"
	mask_image = predict(model, ori_image, parameterPath, patch_size=256, threshold=0.5)
	mask_image = np.transpose(mask_image*255,(1,2,0))
	mask_image = cv2.cvtColor(mask_image, cv2.COLOR_GRAY2BGR)
	#print(time.time() - start_time)
	return mask_image

def parameter_tuning(original_image, masked_image,patch_size = 256,threshold=0.5):
	print("parameter_tuning") # 이거 흑으로 예측하는 문제 해결해야할 듯 


	print(masked_image.shape)
	original_image=Image.fromarray(original_image)
	masked_image=Image.fromarray(~masked_image)
	model = smp.Unet("resnet101", in_channels=3, classes=1, encoder_weights="imagenet")
	parameterPath = "./best_model/best_model.pth"

	device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
	
	# Initialize the model with saved parameters
	#loaded_state = torch.load(model_path+seq_to_seq_test_model_fname,map_location='cuda:0'
	try:
		model.load_state_dict(torch.load(parameterPath,map_location='cuda:0'))
	except:
		model.load_state_dict(torch.load(parameterPath,map_location='cpu'))
		device = torch.device('cpu')

	print(device)
	model.to(device)
	model.train()

	T = transforms.Compose([transforms.ToTensor(),
							transforms.Normalize(
							mean=[0.1034, 0.0308, 0.0346],
							std=[0.0932, 0.0273, 0.0302])])

	T_mask = transforms.Compose([transforms.Grayscale(),transforms.ToTensor()])

	#fl = Image.open(flPath).convert('RGB')	# PIL Image
	#fl = Image.open("023_fl.png").convert('RGB')	# PIL Image

	ori_image, added_w, added_h = SizeAdjustment(original_image, patch_size=patch_size)

	mask_image, added_w, added_h = SizeAdjustment(masked_image, patch_size=patch_size)
	w, h = ori_image.size

	prediction = None

	optimizer = torch.optim.SGD(model.parameters(), momentum=0.9, lr=0.00001)
	criterion = losses.DiceLoss().to(device)

	for y in range(0, h, int(patch_size/3)):
		row = None
		for x in range(0, w, int(patch_size/3)):
			fl_patch = crop(ori_image, y, x, patch_size, patch_size)
			mask_patch = crop(mask_image, y, x, patch_size, patch_size)

			p_patch = (model(T(fl_patch).unsqueeze(0).to(device, dtype=torch.float32))).squeeze(0)	# Predicted mask patch
			
			mask_patch = T_mask(mask_patch).unsqueeze(0).to(device, dtype=torch.float32).squeeze(0)

			loss = criterion(p_patch, mask_patch)
			loss.backward()
			optimizer.step()
	
	torch.save(model.state_dict(), parameterPath)


	#해당 파라미터 다시 저장
	#code.interact(local=dict(globals(), **locals()))

	return # Prediction mask as torch.tensor with MP represented as 0., which is black when saved as PNG file.
"""
from PIL import Image

model = smp.Unet("resnet101", in_channels=3, classes=1, encoder_weights="imagenet")
parameterPath = "./best_model/best_model.pth"


ori_image = Image.open("023_fl_original.png").convert('RGB')
mask_image = Image.open("023_mask.png").convert('RGB')

#ori_image=Image.fromarray(ori_image_PIL)
#mask_image=Image.fromarray(mask_image_PIL)
parameter_tuning(model,parameterPath,ori_image, mask_image)

"""
#UNet(ori_image)
# To save the predicted mask as PNG file,
# save_image((~(prediction.bool())).float().cpu(), '''SAVING_PATH''')