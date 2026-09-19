import pandas as pd
import numpy as np
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
data = {
    "Study_Hours": [
        1, 2, 2, 3, 3, 4, 4, 5, 5, 6,
        6, 7, 7, 8, 8, 9, 9, 10, 10, 11,
        11, 12, 12, 13, 13, 14, 14, 15, 15, 16],

    "Attendance": [
        50, 55, 60, 62, 65, 68, 70, 72, 75, 78,
        80, 82, 84, 86, 88, 90, 91, 92, 93, 94,
        75, 79, 83, 87, 89, 95, 96, 97, 98, 99],

    "Previous_Score": [
        35, 40, 42, 45, 48, 50, 52, 55, 58, 60,
        62, 65, 67, 70, 72, 75, 77, 80, 82, 84,
        55, 61, 66, 71, 76, 81, 86, 90, 93, 95],

    "Assignments": [
        2, 3, 3, 4, 4, 5, 5, 6, 6, 7,
        7, 8, 8, 8, 9, 9, 9, 10, 10, 10,
        5, 6, 7, 7, 8, 9, 9, 10, 10, 10],

    "Final_Score": [
        32, 36, 39, 42, 45, 48, 51, 55, 58, 61,
        64, 67, 69, 72, 74, 77, 79, 82, 84, 86,
        53, 59, 65, 70, 75, 80, 85, 89, 92, 95]
}

df = pd.DataFrame(data)
print(df)

X = df[[
        "Study_Hours",
        "Attendance",
        "Previous_Score",
        "Assignments"
    ]]

y = df["Final_Score"]

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42)

from sklearn.linear_model import LinearRegression

model = LinearRegression()

model.fit(X_train, y_train)


train_data = model.predict(X_train)

train_score = r2_score(
    y_train,
    train_data
)

test_data = model.predict(X_test)

test_score = r2_score(
    y_test,
    test_data
)

mae = mean_absolute_error(
    y_test,
    test_data
)

mse = mean_squared_error(
    y_test,
    test_data
)

rmse = np.sqrt(mse)

print("\nTraining R2 Score:", train_score)

print("Testing R2 Score:", test_score)

print("MAE:", mae)

print("MSE:", mse)

print("RMSE:", rmse)

def predict_result(
    study_hours,
    attendance,
    previous_score,
    assignments
):

    input_data = pd.DataFrame(
        [[
            float(study_hours),
            float(attendance),
            float(previous_score),
            float(assignments)
        ]],
        columns=[
            "Study_Hours",
            "Attendance",
            "Previous_Score",
            "Assignments"
        ]
    )

    prediction = model.predict(input_data)[0]
    prediction = max(0, min(100, prediction))
    return round(float(prediction), 2)
