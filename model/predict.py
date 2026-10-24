import pickle
import pandas as pd

# import the ml model
with open('model/model.pkl', 'rb') as f:  # rb -- read binary mode
    model = pickle.load(f)
    
# Ideally --> MLFlow software - model registry component which automatically track which version of model you have
# here we are manually created it and pass to health endpoint
MODEL_VERSION = '1.0.0'

# get class labels from model (important for matching probabilities to class names)
class_labels = model.classes_.tolist()

def predict_output(user_input: dict):
    
    df = pd.DataFrame([user_input])
    
    # predict the class
    predicted_class = model.predict(df)[0]
    
   # get probabilities for all classes
    probabilities = model.predict_proba(df)[0]
    confidence = max(probabilities)
   
   # create mapping: {class_name: probabilities}
    class_probs = dict(zip(class_labels, map(lambda p: round(p,4), probabilities)))
   
    
    return {
        "predicted_category": str(predicted_class),
        "confidence": round(float(confidence), 4),
        "class_probabilities": { key: round(float(value), 4) for key, value in class_probs.items()}
    }