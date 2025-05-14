from transformers import NllbTokenizer, AutoModelForSeq2SeqLM
import torch


class Translator:
    def __init__(self, model_path: str):
        self.tokenizer = NllbTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_path)

    def translate(self, text, src_lang='rus_Cyrl', tgt_lang='bxr_Cyrl', max_input_length=1024, num_beams=4):
        """Переводит введённый текст."""
        self.tokenizer.src_lang = src_lang
        self.tokenizer.tgt_lang = tgt_lang
        inputs = self.tokenizer(
            text, return_tensors='pt', padding=True, truncation=True, max_length=max_input_length
        )
        self.model.eval()
        with torch.no_grad():
            result = self.model.generate(
                **inputs.to(self.model.device),
                forced_bos_token_id=self.tokenizer.convert_tokens_to_ids(tgt_lang),
                max_new_tokens=max_input_length,
                num_beams=num_beams
            )
        return self.tokenizer.batch_decode(result, skip_special_tokens=True)[0]


def get_translator():
    return Translator('./model/nllb-rus-bxr')


