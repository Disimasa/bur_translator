from transformers import AutoModelForSeq2SeqLM, NllbTokenizer
from functools import cache, cached_property

from config import global_config


class Translator:
    def __init__(self, model_name):
        self.tokenizer = NllbTokenizer.from_pretrained(model_name, low_cpu_mem_usage=True, use_auth_token=global_config.HF_TOKEN)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name, low_cpu_mem_usage=True, use_auth_token=global_config.HF_TOKEN)
        self.fix_tokenizer()

    def translate(self, text, src_lang='rus_Cyrl', tgt_lang='bxr_Cyrl', a=32, b=3, max_input_length=1024, num_beams=4, **kwargs):
        self.tokenizer.src_lang = src_lang
        self.tokenizer.tgt_lang = tgt_lang
        inputs = self.tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=max_input_length)
        result = self.model.generate(
            **inputs.to(self.model.device),
            forced_bos_token_id=self.tokenizer.convert_tokens_to_ids(tgt_lang),
            max_new_tokens=int(a + b * inputs.input_ids.shape[1]),
            num_beams=num_beams,
            **kwargs
        )
        return self.tokenizer.batch_decode(result, skip_special_tokens=True)

    def fix_tokenizer(self, new_lang='bxr_Cyrl'):
        old_len = len(self.tokenizer) - int(new_lang in self.tokenizer.added_tokens_encoder)
        self.tokenizer.lang_code_to_id[new_lang] = old_len - 1
        self.tokenizer.id_to_lang_code[old_len - 1] = new_lang
        self.tokenizer.fairseq_tokens_to_ids["<mask>"] = len(self.tokenizer.sp_model) + len(
            self.tokenizer.lang_code_to_id) + self.tokenizer.fairseq_offset

        self.tokenizer.fairseq_tokens_to_ids.update(self.tokenizer.lang_code_to_id)
        self.tokenizer.fairseq_ids_to_tokens = {v: k for k, v in self.tokenizer.fairseq_tokens_to_ids.items()}
        if new_lang not in self.tokenizer._additional_special_tokens:
            self.tokenizer._additional_special_tokens.append(new_lang)

        self.tokenizer.added_tokens_encoder = {}
        self.tokenizer.added_tokens_decoder = {}


@cache
def get_translator():
    return Translator('SaranaAbidueva/nllb-200-bxr-ru')
