from textblob import TextBlob
texts=["j'ai bien aimé aller au ciné","i love it, it's awesome"]
text = "I love using this product. It's fantastic!"
texts.append(text)
text = "I hate this movie. It sucks!"
texts.append(text)
text = "I hate this iphone on amazon. this is shit"
texts.append(text)
for text in texts:
  blob = TextBlob(text)
  sentiment = blob.sentiment.polarity
  print(text)
  print(sentiment)
