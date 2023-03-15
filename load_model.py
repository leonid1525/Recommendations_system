from catboost import CatBoostClassifier

# Функция загрузки модели, заранее обученной и готовой к использованию
def load_models(name_model: str):
    model = CatBoostClassifier()
    model.load_model(name_model, format="cbm")
    return model