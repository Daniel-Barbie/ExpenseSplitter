from flask import Flask, render_template, request

app = Flask(__name__)

persons = ['person1', 'person2']

def calc_shared_expenses(expenses: list[float]) -> float:
    return sum(expenses)

def calc_total_paid_per_person(expenses_paid: dict[str, list[float]]) -> dict[str, float]:
    return {key: sum(expenses_paid[key]) for key in expenses_paid }

def calc_total_expenses_per_person(
    p1_paid_for_p2: list[float] = [0],
    p2_paid_for_p1: list[float] = [0],
    shared_expenses: float = 0
) -> dict[str, float]:
    return {
        "person1": sum(p2_paid_for_p1) + shared_expenses / 2,
        "person2": sum(p1_paid_for_p2) + shared_expenses / 2
    }

p1_paid_for_p2: list[float] = []
p2_paid_for_p1: list[float] = []
p1_paid_for_both: list[float] = []
p2_paid_for_both: list[float] = []
p1_owes_p2: float = 0
p2_owes_p1: float = 0

expenses: list[dict[str, str | float]] = []

# expenses = {person: 0 for person in persons}
# paid = {person: 0 for person in persons}
# individual_expenses = {person: 0 for person in persons}
#expenses_paid = {person: 0 for person in persons}


@app.route('/', methods=['GET', 'POST'])
def index():
    global p1_paid_for_both, p2_paid_for_both, p1_owes_p2, p2_owes_p1, expenses
    expense_type = ""
    payer = ""
    if request.method == 'POST':
        expense_type = request.form['expense_type']
        amount = float(request.form['amount'])
        payer = request.form['payer']
        if payer not in persons:
            return render_template('index.html', message='Invalid payer.')
        
        if expense_type == "1":
            if payer == "person1":
                p1_paid_for_both.append(amount)
                p2_owes_p1 += amount / 2
            else:
                p2_paid_for_both.append(amount)
                p1_owes_p2 += amount / 2
        else:
            if payer == "person1":
                p1_paid_for_p2.append(amount)
                p2_owes_p1 += amount
            else:
                p2_paid_for_p1.append(amount)
                p1_owes_p2 += amount

        expense = {
            'type': 'Shared' if expense_type == "1" else 'Individual',
            'payer': payer,
            'amount': amount
        }
        expenses.append(expense)
        
    person1_owes = p1_owes_p2 - p2_owes_p1
    person2_owes = p2_owes_p1 - p1_owes_p2
    shared_expenses = calc_shared_expenses(p1_paid_for_both + p2_paid_for_both)
    total_paid_per_person = calc_total_paid_per_person({"person1": p1_paid_for_both + p1_paid_for_p2, "person2": p2_paid_for_both + p2_paid_for_p1})
    total_expenses_per_person = calc_total_expenses_per_person(p1_paid_for_p2, p2_paid_for_p1, shared_expenses)

    return render_template(
        'index.html', 
        expense_type=expense_type,
        payer=payer,
        person1_owes=person1_owes, 
        person2_owes=person2_owes, 
        total_expenses_per_person=total_expenses_per_person, 
        shared_expenses=shared_expenses, 
        total_paid_per_person=total_paid_per_person,
        expenses=expenses
    )


if __name__ == '__main__':
    app.run()
