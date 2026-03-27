from sklearn.linear_model import LogisticRegression
import numpy as np

# Dummy training data
X = np.array([
    [50, 1, 0, 0],
    [120, 0, 1, 1],
    [80, 1, 0, 1],
    [200, 0, 1, 1]
])

y = [0, 1, 0, 1]  # 0 = SAFE, 1 = PHISHING

model = LogisticRegression()
model.fit(X, y)