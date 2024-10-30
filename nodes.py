import yaml
import os

class NS_ManySliders:
    @classmethod
    def INPUT_TYPES(s):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        settings_path = os.path.join(current_dir, 'settings.yaml')

        with open(settings_path, 'r') as f:
            settings = yaml.safe_load(f)

        required = {
            "slider_count": ("INT", {
                "default": settings['sliders']['count'],
                "min": 1,
                "max": settings['sliders']['count']
            })
        }

        # 各スライダーをrequiredとして定義
        for i in range(settings['sliders']['count']):
            required[f"value_{i}"] = ("FLOAT", {
                "default": settings['sliders']['default_value'],
                "min": settings['sliders']['min_value'],
                "max": settings['sliders']['max_value'],
                "step": step,
                "display": "slider"
            })

        return {"required": required}

    RETURN_TYPES = ("STRING",)
    FUNCTION = "run"
    CATEGORY = "utils"

    def run(self, slider_count, **kwargs):
        settings_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'settings.yaml')

        with open(settings_path, 'r') as f:
            settings = yaml.safe_load(f)

        max_sliders = settings['sliders']['count']
        effective_count = min(slider_count, max_sliders)
        values = []

        for i in range(effective_count):
            value_key = f'value_{i}'
            value = kwargs.get(value_key, settings['sliders']['default_value'])
            value = max(min(float(value), settings['sliders']['max_value']),
                    settings['sliders']['min_value'])
            values.append(str(value))

        return (",".join(values),)

    @classmethod
    def VALIDATE_INPUTS(cls, slider_count, **kwargs):
        try:
            settings_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'settings.yaml')
            with open(settings_path, 'r') as f:
                settings = yaml.safe_load(f)

            if not (1 <= slider_count <= settings['sliders']['count']):
                return False

            for i in range(slider_count):
                value_key = f'value_{i}'
                if value_key in kwargs:
                    value = kwargs[value_key]
                    if not (settings['sliders']['min_value'] <= value <= settings['sliders']['max_value']):
                        return False
            return True
        except:
            return False