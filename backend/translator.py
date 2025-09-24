from transformers import NllbTokenizer, AutoModelForSeq2SeqLM
import torch
import gc


class Translator:
    def __init__(self, model_path: str):
        self.tokenizer = NllbTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            model_path,
            torch_dtype=torch.float32  # Оставляем float32 для качества
        )
        # Настройка для экономии памяти
        self.model.eval()

    def translate(self, text, src_lang='rus_Cyrl', tgt_lang='bxr_Cyrl', max_input_length=1024, num_beams=4):
        """Переводит введённый текст."""
        try:
            # Очищаем память перед началом
            gc.collect()
            
            self.tokenizer.src_lang = src_lang
            self.tokenizer.tgt_lang = tgt_lang
            inputs = self.tokenizer(
                text, return_tensors='pt', padding=True, truncation=True, max_length=max_input_length
            )
            
            # Оставляем входы на CPU
            inputs = {k: v for k, v in inputs.items()}
            
            # Принудительно очищаем кэш PyTorch перед генерацией
            torch.cuda.empty_cache() if torch.cuda.is_available() else None
            
            with torch.no_grad():
                result = self.model.generate(
                    **inputs,
                    forced_bos_token_id=self.tokenizer.convert_tokens_to_ids(tgt_lang),
                    max_new_tokens=max_input_length,
                    num_beams=num_beams,
                    do_sample=False,  # Отключаем сэмплирование для стабильности
                    early_stopping=True,  # Останавливаем генерацию раньше
                    pad_token_id=self.tokenizer.pad_token_id
                )
            
            # Декодируем результат
            translation = self.tokenizer.batch_decode(result, skip_special_tokens=True)[0]
            
            # Агрессивная очистка памяти
            del inputs, result
            gc.collect()
            torch.cuda.empty_cache() if torch.cuda.is_available() else None
            
            return translation
            
        except Exception as e:
            # В случае ошибки также очищаем память
            if 'inputs' in locals():
                del inputs
            if 'result' in locals():
                del result
            gc.collect()
            torch.cuda.empty_cache() if torch.cuda.is_available() else None
            raise e


def get_translator():
    return Translator('./model/nllb-rus-bxr')


