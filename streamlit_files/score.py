import json
import streamlit as st

SCORES_DATA_FILENAME = "data/scores_data.json"
STATS_FILENAME = "data/stats.json"

categ_scores = {}

def load_stats():
    with open(STATS_FILENAME, "r") as file:
        stats = json.load(file)
    return stats

def write_update_stats(categ_scores):
    with open(STATS_FILENAME, "w") as file:
        json.dump(categ_scores, file, indent=4)

    
def update_stats(categ_name, correctly_answered, wrong_answers, no_of_questions):
    score_info = {}
    score_info["categ_name"], score_info["correctly_answered"], score_info["wrongly_answered"], score_info["no_of_questions"] = categ_name, correctly_answered, wrong_answers, no_of_questions
    if correctly_answered == 0:
        score_info["percentage"] = 0
    else:
        score_info["percentage"] = (correctly_answered/no_of_questions)*100

    categ_scores = load_stats()

    if categ_name not in categ_scores:
        categ_scores[categ_name] = [] #appends a list of dicts
        categ_scores[categ_name].append(score_info)
    else:
        categ_scores[categ_name].append(score_info)

    write_update_stats(categ_scores)



def calculate_score(correct_answers, total_questions):
    if total_questions == 0:
        return 0.0
    percentage_score = (correct_answers/total_questions) * 100
    return round(percentage_score, 2)


def load_scores_data():
    """Loads scores data from scores_data.json"""
    with open(SCORES_DATA_FILENAME, "r") as file:
        scores_data_history = json.load(file)
    return scores_data_history

def record_score_data(set_of_questions, game_config):

    score_data = {}
    score_data["category"] = game_config["category"]
    score_data["amount"] = game_config["amount"]#consider endless mode
    score_data["mode"] = game_config["mode"]

    score_data["wrongly_answered"] = set_of_questions["wrongly_answered"]
    score_data["correctly_answered"] = set_of_questions["correctly_answered"]
    score_data["no_of_questions"] = set_of_questions["no_of_questions"]
    
    scores_data = load_scores_data()
    scores_data.append(score_data)

    with open(SCORES_DATA_FILENAME, "w") as file:
        json.dump(scores_data, file, indent=4)

def handle_score(set_of_questions, game_config):
    correctly_answered, wrongly_answered, no_of_questions = len(set_of_questions["correctly_answered"]), len(set_of_questions["wrongly_answered"]), set_of_questions["no_of_questions"]

    record_score_data(set_of_questions, game_config)
    categ_name = (game_config["category"])["name"]
    update_stats(categ_name, correctly_answered, wrongly_answered, no_of_questions)

def print_score(set_of_questions):
    correctly_answered, no_of_questions = len(set_of_questions["correctly_answered"]), set_of_questions["no_of_questions"]
    percentage_score = calculate_score(correctly_answered, no_of_questions)

    st.write(f"""You scored {correctly_answered} out of {no_of_questions}.
    Your percentage score is: {percentage_score}\n""")


def show_results():
    st.subheader("Results")
    print_score(st.session_state.set_of_questions)

    if st.button("Return Home"):
        st.session_state.current_page = "home"
        st.rerun()

#---- DISPLAY STATS STUFF ----

def compute_categ_avgs():
    stats = load_stats()
    categs_avgs = []

    for categ, quizzes in stats.items():

        percentage_sum = 0
        for quiz in quizzes:
            percentage_sum += quiz["percentage"]

        if len(quizzes) != 0:
            percentage_avg = percentage_sum / len(quizzes)
        else:
            percentage_avg = 0
        categs_avgs.append((categ, round(percentage_avg, 2)))
    return categs_avgs

def ret_all_categs():
    categs_avgs = compute_categ_avgs()
    sorted_categs_avgs = sorted(categs_avgs, key = lambda item:item[1], reverse=True)
    return sorted_categs_avgs


def display_categorical_stats():
    sorted_categs_avgs = ret_all_categs()
    for item in sorted_categs_avgs:
        st.write(f"{item[0]} \t {item[1]}")

def display_overall_performance():
    stats = load_stats()
    count = no_of_questions = total_correct = total_wrong = sum_percentage = 0

    for categ, quizzes in stats.items():
        for quiz in quizzes:
            count+=1
            no_of_questions += int(quiz["no_of_questions"])
            total_correct += quiz["correctly_answered"]
            total_wrong += int(quiz["wrongly_answered"])
            sum_percentage += int(quiz["percentage"])

    avg_percentage = round(sum_percentage/count, 2)

    st.write(f"Total answereed questions: {no_of_questions}")
    st.write(f"Total correctly answered questions: {total_correct}")
    st.write(f"Total wrongly answered questions: {total_wrong}")

    st.write(f"You have a percentage correctness of {avg_percentage:.2f} \n")


def display_stats():
    stat_view_options = ["Overall performance", "Categorical performance"]
    user_input = st.selectbox("What would you like to look at today?", options=stat_view_options)

    if user_input == "Overall performance":
        display_overall_performance()
    elif user_input == "Categorical performance":
        display_categorical_stats()

if __name__ == "__main__":
    #categs_avgs = [("Math", 90),  ("Computer", 299),  ("Computer", 380), ("Computer", 80),  ("Computer", 20)]
    #print(ret_all_categs(categs_avgs))
    sorted_categs_avgs = [('Computer', 380), ('Computer', 299), ('Math', 90), ('Computer', 80), ('Computer', 20)]
    st.write(display_categorical_stats(sorted_categs_avgs))
    st.write("Doneee")