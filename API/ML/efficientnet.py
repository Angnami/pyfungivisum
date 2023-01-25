from tensorflow.keras.models  import load_model
import cv2
import numpy as np
class EfficientNetModel():
    
    class_indices = ['Amanita flavoconia', 'Amanita muscaria', 'Baorangia bicolor',
                 'Boletus edulis', 'Coprinus comatus', 'Galerina marginata',
                 'Ganoderma applanatum', 'Hypholoma fasciculare',
                 'Laetiporus sulphureus', 'Phaeolus schweinitzii',
                 'Pleurotus ostreatus', 'Pluteus cervinus',
                 'Psathyrella candolleana', 'Psilocybe cyanescens',
                 'Psilocybe zapotecorum']
    
    
    def __init__(self,model_path):     
        self.model = load_model(model_path)
    
    
    def transform(self,image):      
        x = np.array(image)
        x = cv2.resize(x,(224,224))
        x= np.expand_dims(x, axis=0)
        return x
    
     
    def make_prediction(self,image):   
        x = self.transform(image)
        predictions = self.model.predict(x, verbose=0)
        pred_index =int(predictions.argmax(axis=-1))
        pred_class = self.class_indices[pred_index]   
        return {"predicted_specy":f'{pred_class}', 'confidence':f'{predictions.max():.4}'}
