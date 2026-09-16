from flask import Flask, request, render_template_string
import student_performance

app = Flask(__name__)


HTML = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Student Performance Predictor</title>

    <style>

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: Arial, sans-serif;
        }

        body {
            min-height: 100vh;
            background: linear-gradient(135deg, #071426, #102d4d, #071426);
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 30px;
        }

        .container {
            width: 100%;
            max-width: 1100px;
            min-height: 650px;

            display: flex;

            background: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.15);

            border-radius: 25px;

            overflow: hidden;

            box-shadow: 0 25px 70px rgba(0, 0, 0, 0.45);

            backdrop-filter: blur(15px);

            animation: appear 0.8s ease;
        }


        /* LEFT SIDE */

        .left {
            width: 55%;
            padding: 45px;

            background: linear-gradient(
                145deg,
                rgba(8, 27, 50, 0.95),
                rgba(14, 47, 78, 0.85)
            );
        }


        .badge {
            display: inline-block;

            padding: 8px 15px;

            border-radius: 20px;

            background: rgba(70, 160, 255, 0.15);

            border: 1px solid rgba(90, 180, 255, 0.3);

            color: #75c8ff;

            font-size: 13px;

            margin-bottom: 18px;
        }


        h1 {
            font-size: 42px;

            line-height: 1.1;

            margin-bottom: 12px;

            letter-spacing: 1px;
        }


        h1 span {
            color: #57c7ff;
        }


        .description {
            color: #aabbd0;

            font-size: 15px;

            line-height: 1.6;

            margin-bottom: 30px;
        }


        .form-grid {
            display: grid;

            grid-template-columns: 1fr 1fr;

            gap: 18px;
        }


        .input-box {
            position: relative;
        }


        label {
            display: block;

            margin-bottom: 8px;

            color: #cbd8e6;

            font-size: 13px;

            font-weight: bold;
        }


        input {
            width: 100%;

            padding: 15px;

            border-radius: 12px;

            border: 1px solid rgba(255, 255, 255, 0.12);

            outline: none;

            background: rgba(255, 255, 255, 0.07);

            color: white;

            font-size: 15px;

            transition: 0.3s;
        }


        input:focus {
            border-color: #52c7ff;

            box-shadow: 0 0 0 3px rgba(82, 199, 255, 0.12);

            transform: translateY(-2px);
        }


        input::placeholder {
            color: #71869c;
        }


        button {
            width: 100%;

            margin-top: 25px;

            padding: 16px;

            border: none;

            border-radius: 13px;

            background: linear-gradient(
                135deg,
                #3db9ff,
                #1679d3
            );

            color: white;

            font-size: 16px;

            font-weight: bold;

            cursor: pointer;

            transition: 0.3s;

            box-shadow: 0 10px 25px rgba(25, 139, 220, 0.25);
        }


        button:hover {
            transform: translateY(-3px);

            box-shadow: 0 15px 35px rgba(25, 139, 220, 0.4);
        }


        button:active {
            transform: scale(0.98);
        }


        /* RESULT */

        .result {
            margin-top: 25px;

            padding: 18px;

            border-radius: 15px;

            text-align: center;

            background: rgba(255, 255, 255, 0.07);

            border: 1px solid rgba(255, 255, 255, 0.12);

            animation: resultAppear 0.5s ease;
        }


        .result-title {
            font-size: 13px;

            color: #9db1c7;

            margin-bottom: 7px;
        }


        .result-value {
            font-size: 30px;

            font-weight: bold;
        }


        .pass {
            color: #4dff9a;
        }


        .fail {
            color: #ff6577;
        }


        /* RIGHT SIDE */

        .right {
            width: 45%;

            display: flex;

            justify-content: center;

            align-items: center;

            position: relative;

            overflow: hidden;

            background:
                radial-gradient(
                    circle at center,
                    rgba(50, 160, 255, 0.16),
                    transparent 65%
                );
        }


        .right::before {
            content: "";

            position: absolute;

            width: 280px;
            height: 280px;

            border-radius: 50%;

            background: rgba(51, 177, 255, 0.08);

            filter: blur(10px);

            animation: glow 4s infinite alternate;
        }


        .student-card {
            position: relative;

            width: 300px;

            padding: 40px 25px;

            text-align: center;

            background: rgba(255, 255, 255, 0.07);

            border: 1px solid rgba(255, 255, 255, 0.13);

            border-radius: 25px;

            backdrop-filter: blur(15px);

            box-shadow: 0 20px 50px rgba(0,0,0,0.25);

            animation: floating 4s ease-in-out infinite;
        }


        .student-icon {
            width: 120px;
            height: 120px;

            margin: auto;
            margin-bottom: 25px;

            border-radius: 50%;

            display: flex;

            justify-content: center;

            align-items: center;

            font-size: 60px;

            background: linear-gradient(
                135deg,
                #183c61,
                #246c9d
            );

            box-shadow:
                0 0 35px rgba(57, 181, 255, 0.25);
        }


        .student-card h2 {
            font-size: 25px;

            margin-bottom: 10px;
        }


        .student-card p {
            color: #9eb2c7;

            font-size: 14px;

            line-height: 1.6;
        }


        .powered {
            position: absolute;

            bottom: 25px;

            color: #71869c;

            font-size: 12px;

            letter-spacing: 1px;
        }


        /* ANIMATIONS */

        @keyframes appear {

            from {
                opacity: 0;
                transform: translateY(25px);
            }

            to {
                opacity: 1;
                transform: translateY(0);
            }

        }


        @keyframes floating {

            0%, 100% {
                transform: translateY(0);
            }

            50% {
                transform: translateY(-12px);
            }

        }


        @keyframes glow {

            from {
                transform: scale(1);
                opacity: 0.5;
            }

            to {
                transform: scale(1.25);
                opacity: 1;
            }

        }


        @keyframes resultAppear {

            from {
                opacity: 0;
                transform: scale(0.95);
            }

            to {
                opacity: 1;
                transform: scale(1);
            }

        }


        /* MOBILE */

        @media (max-width: 800px) {

            body {
                padding: 15px;
            }

            .container {
                flex-direction: column;
            }

            .left,
            .right {
                width: 100%;
            }

            .left {
                padding: 30px 22px;
            }

            .right {
                min-height: 400px;
            }

            h1 {
                font-size: 34px;
            }

        }


        @media (max-width: 500px) {

            .form-grid {
                grid-template-columns: 1fr;
            }

        }

    </style>

</head>


<body>


<div class="container">


    <!-- LEFT -->

    <div class="left">

        <div class="badge">
            🤖 MACHINE LEARNING PROJECT
        </div>


        <h1>
            Student <span>Performance</span> Predictor
        </h1>


        <p class="description">
            Enter the student's academic details below and
            our Machine Learning model will predict whether
            the student is likely to PASS or FAIL.
        </p>


        <form method="POST">

            <div class="form-grid">


                <div class="input-box">

                    <label>📚 Study Hours</label>

                    <input
                        type="number"
                        name="study_hours"
                        placeholder="Example: 8"
                        min="0"
                        step="0.1"
                        required
                    >

                </div>


                <div class="input-box">

                    <label>📅 Attendance (%)</label>

                    <input
                        type="number"
                        name="attendance"
                        placeholder="Example: 85"
                        min="0"
                        max="100"
                        step="0.1"
                        required
                    >

                </div>


                <div class="input-box">

                    <label>📝 Previous Score</label>

                    <input
                        type="number"
                        name="previous_score"
                        placeholder="Example: 75"
                        min="0"
                        max="100"
                        step="0.1"
                        required
                    >

                </div>


                <div class="input-box">

                    <label>📖 Assignments</label>

                    <input
                        type="number"
                        name="assignments"
                        placeholder="Example: 8"
                        min="0"
                        step="1"
                        required
                    >

                </div>


            </div>


            <button type="submit">
                🚀 Predict Student Result
            </button>

        </form>


        {% if result %}

        <div class="result">

            <div class="result-title">
                PREDICTION RESULT
            </div>

            {% if result == "PASS" %}

                <div class="result-value pass">
                    ✅ PASS
                </div>

            {% else %}

                <div class="result-value fail">
                    ❌ FAIL
                </div>

            {% endif %}

        </div>

        {% endif %}


    </div>



    <!-- RIGHT -->

    <div class="right">


        <div class="student-card">

            <div class="student-icon">
                🎓
            </div>


            <h2>
                AI Student Analysis
            </h2>


            <p>
                This application uses
                <b>Machine Learning</b>
                to analyse academic performance
                and predict the student's result.
            </p>

        </div>


        <div class="powered">
            ⚡ Powered by Machine Learning
        </div>


    </div>


</div>


</body>

</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():

    result = None

    if request.method == "POST":

        study_hours = float(request.form["study_hours"])

        attendance = float(request.form["attendance"])

        previous_score = float(request.form["previous_score"])

        assignments = float(request.form["assignments"])


        result = student_performance.predict_result(
            study_hours,
            attendance,
            previous_score,
            assignments
        )


    return render_template_string(
        HTML,
        result=result
    )


if __name__ == "__main__":
    app.run(debug=True)