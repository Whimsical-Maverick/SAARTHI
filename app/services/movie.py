from sentence_transformers import SentenceTransformer, util
movie_model = SentenceTransformer('all-MiniLM-L6-v2')

def find_closest_emotion(prompt, emotions):
    input_embedding = movie_model.encode([prompt], convert_to_tensor=True)
    emotion_embedding = movie_model.encode(list(emotions.values()), convert_to_tensor=True)
    cos_score = util.cos_sim(input_embedding, emotion_embedding)[0]
    result_index = cos_score.argmax().item()
    return list(emotions.keys())[result_index]