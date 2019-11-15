class BaseModel(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def from_dict(cls, model_dict):
        params = {
            field: model_dict.get(field) for field in cls.fields()
        }
        return cls(**params)

    @classmethod
    def fields(cls) -> list:
        raise NotImplemented
