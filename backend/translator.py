from transformers import MBartForConditionalGeneration, MBart50Tokenizer
from functools import cache, cached_property


class Translator:
    def __init__(self, model_name):
        self.tokenizer = MBart50Tokenizer.from_pretrained(model_name)
        self.model = MBartForConditionalGeneration.from_pretrained(model_name)

    def translate(self, text: str, max_length=200, num_beams=5, repetition_penalty=5.0):
        encoded = self.tokenizer(text, return_tensors="pt")
        generated_tokens = self.model.generate(
            **encoded.to(self.model.device),
            max_length=max_length,
            num_beams=num_beams,
            repetition_penalty=repetition_penalty
        )
        return self.tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]


@cache
def get_rus_bur_translator():
    return Translator('SaranaAbidueva/mbart50_ru_bua')
