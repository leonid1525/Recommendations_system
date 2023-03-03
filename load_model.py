from catboost import CatBoostClassifier

# Model loading function, returns a pre-trained model, ready to use
def load_models():
    model = CatBoostClassifier()
    model.load_model("catboost (3)")
    return model
