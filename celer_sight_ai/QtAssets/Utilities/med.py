import torch
import cv2
import numpy
from torchvision import models, transforms
from PIL import Image
import torch.nn as nn
import numpy as np
def abnormalities_NIH_2_class(img):
    	# -------------------- SETTINGS: CXR DATA TRANSFORMS -------------------
    normalizer = [[0.485, 0.456, 0.406], [0.229, 0.224, 0.225]]
    mytransformer = transforms.Compose(
        [
        transforms.Resize(256),
        # transforms.RandomResizedCrop(crop_size),
        transforms.CenterCrop(244),
        transforms.ToTensor(),
        transforms.Normalize(normalizer[0], normalizer[1])
        ]
        )

    model_path = 'L:\\Medical\\NatureAbnormalities Non Commcercial\\CADLab\\CXR-Binary-Classifier\\trained_models_nih\\densenet121_256_4_0.001'
    model = models.__dict__['densenet121'](pretrained=True)
    torch.cuda.set_device(0)
    # number of classes
    numClass = 1
    # modify the last FC layer to number of classes
    num_ftrs = model.classifier.in_features
    model.classifier = nn.Linear(num_ftrs, numClass)

    model.load_state_dict(torch.load(model_path)['state_dict'])

    model.eval()
    model.cuda(0)    

    totalResult = []
    totalTally = 0
    # for myFile in allFiles:
    #     img = cv2.imread(myFile)
    img = Image.fromarray(img)
    img=mytransformer(img)

    img = img.unsqueeze(0)
    # print(img.shape)



    with torch.no_grad():
        inputs = img.cuda(0, non_blocking=True)
        # forward
        outputs = model(inputs)
        # print(outputs.cpu().numpy()*100)
        # _, preds = torch.max(outputs.data, 1)
        score = torch.sigmoid(outputs)
        score_np = score.data.cpu().numpy()
        preds = score>0.5
        preds_np = preds.data.cpu().numpy()
        return preds_np[0][0]

def abnormalities_kaggle_bbox(img):
    from mmdet.apis import inference_detector, init_detector, show_result_pyplot
    import cv2
    import pandas as pd
    # Choose to use a config and initialize the detector
    # config = 'C:\\Users\\manos\\Downloads\\mmdetectionLATEST\\mmdetMODS\\iterdet\\configs\\iterdet\\toy_v2_retinanet_r50_fpn_2x.py'
    # # Setup a checkpoint file to load



    checkpoint = "C:\\Users\\manos\\Downloads\\mmdetectionLATEST\\mmdetection\\work_dirs\\detectors_cascade_rcnn_r50_1x_coco_VinBigData\\epoch_12.pth"
    config = 'C:\\Users\\manos\\Downloads\\mmdetectionLATEST\\mmdetection\\work_dirs\\detectors_cascade_rcnn_r50_1x_coco_VinBigData\\detectors_cascade_rcnn_r50_1x_coco_VinBigData.py'

    detectionMap = [
                "Aortic_enlargement",
                "Atelectasis",
                "Calcification",
                "Cardiomegaly",
                "Consolidation",
                "ILD",
                "Infiltration",
                "Lung_Opacity",
                "Nodule/Mass",
                "Other_lesion",
                "Pleural_effusion",
                "Pleural_thickening",
                "Pneumothorax",
                "Pulmonary_fibrosis"
                ]


    # initialize the detector
    model = init_detector(config, checkpoint, device='cuda:0')
    model.eval()
    import mmcv
    import numpy as np
    from PIL import Image
    widthV = img.shape[0]/1024
    heightV = img.shape[1]/1024
    img = cv2.resize(img, (1024,1024), interpolation = cv2.INTER_AREA)
    maskListsOrig = []

    result = inference_detector(model, img)
    print(result)
    # print("it took ",time.time() - start  )
    # myImageCopy = myImage.copy()
    # r, myImageCopy ,c = cv2.split(myImageCopy)
    # for aMaks in maskListsOrig:
    #     myImageCopy[aMaks.astype(bool)] = 255

    iteration = 0
    allMasks = []
    for i in range(len(result)):
        for x in range(len(result[i])):
            x1 = result[i][x][0] * widthV
            y1 = result[i][x][1] * heightV
            x2 = result[i][x][2] * widthV
            y2 = result[i][x][3]* heightV
            precision =  result[i][x][4]
            if precision >= 0.5:
                allMasks.append([(x1,y1),(x2,y1),(x2,y2),(x1,y2),detectionMap[i]] )
    return allMasks


def pneumothorax_kaggle_bbox(img):
    from mmdet.apis import inference_detector, init_detector, show_result_pyplot
    import cv2
    import pandas as pd
    # Choose to use a config and initialize the detector
    # config = 'C:\\Users\\manos\\Downloads\\mmdetectionLATEST\\mmdetMODS\\iterdet\\configs\\iterdet\\toy_v2_retinanet_r50_fpn_2x.py'
    # # Setup a checkpoint file to load



    checkpoint = "C:\\Users\\manos\\Downloads\\mmdetectionLATEST\\mmdetection\\work_dirs\\detectors_cascade_rcnn_r50_1x_coco_PNEUMOTHORAX\\epoch_15.pth"
    config = 'C:\\Users\\manos\\Downloads\\mmdetectionLATEST\\mmdetection\\work_dirs\\detectors_cascade_rcnn_r50_1x_coco_PNEUMOTHORAX\\detectors_cascade_rcnn_r50_1x_coco_PNEUMOTHORAX.py'

    # initialize the detector
    model = init_detector(config, checkpoint, device='cuda:0')
    model.eval()
    import mmcv
    import numpy as np
    from PIL import Image
    widthV = img.shape[0]/1024
    heightV = img.shape[1]/1024
    img = cv2.resize(img, (1024,1024), interpolation = cv2.INTER_AREA)
    maskListsOrig = []

    result = inference_detector(model, img)
    print(result)
    # print("it took ",time.time() - start  )
    # myImageCopy = myImage.copy()
    # r, myImageCopy ,c = cv2.split(myImageCopy)
    # for aMaks in maskListsOrig:
    #     myImageCopy[aMaks.astype(bool)] = 255

    iteration = 0
    allMasks = []
    for i in range(len(result)):
        for x in range(len(result[i])):
            x1 = result[i][x][0]* widthV
            y1 = result[i][x][1]* heightV
            x2 = result[i][x][2]* widthV
            y2 = result[i][x][3]* heightV
            precision =  result[i][x][4]
            if precision >= 0.5:
                allMasks.append([(x1,y1),(x2,y1),(x2,y2),(x1,y2),'Pneumothorax'] )
    return allMasks



def getPredictionsMD(img, mytype= 'abnormalities'):
    if mytype == 'abnormalities':
        result1 = abnormalities_NIH_2_class(img)
        resultClassesBbox = abnormalities_kaggle_bbox(img)
        return result1 , resultClassesBbox

    elif mytype == 'pneumothorax':
        resultClassesBbox =pneumothorax_kaggle_bbox(img)    
        return True, resultClassesBbox
if __name__ == "__main__":
    pass