import torch
import pandas as pd
from transformers import BertTokenizer, BertForSequenceClassification

df = pd.read_csv('ragnar_3_csv.csv')
tokenizer = BertTokenizer.from_pretrained('tokenizer_ragnar')
model = BertForSequenceClassification.from_pretrained('model_ragnar')

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


def predict(context, answer, tokenizer, model, device):
    # Убедимся, что контекст и ответ являются строками
    context = str(context)
    answer = str(answer)

    model.eval()
    inputs = tokenizer.encode_plus(context, answer, return_tensors="pt", max_length=512, padding=True, truncation=True)
    input_ids = inputs['input_ids'].to(device)
    attention_mask = inputs['attention_mask'].to(device)

    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask)
        logits = outputs.logits
        probabilities = torch.softmax(logits, dim=1)
        prediction = torch.argmax(probabilities, dim=1)

    return prediction.cpu().numpy(), probabilities.cpu().numpy()


def predict_best_answer(context):
    best_score = 0
    best_answer = None
    for index, row in df.iterrows():
        answer = row['answer']  # Используем реплику Рагнара как потенциальный ответ
        prediction, probabilities = predict(context, answer, tokenizer, model, device)

        # Проверяем вероятность релевантности (класс 1)
        score = probabilities[0][1]
        if score > best_score:
            best_score = score
            best_answer = answer

    return best_answer
