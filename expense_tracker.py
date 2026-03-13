from expense import Expense

def main():
    print("Welcome to the expense tracker app")

    expense_file_path = "expendses.csv"
    budget = 300000
    # Get user input for expense
    expense = get_user_expense()
    
    # write their expense to a file
    save_expense_to_file(expense, expense_file_path)
    # read file and summarize expense
    summarize_expenses(expense, expense_file_path, budget)  # budget now included


def get_user_expense():
    print("Getting user expense")
    expense_name = input("Enter expense name: ")

    # Ensure valid float input
    while True:
        try:
            expense_amount = float(input("Enter expense amount: "))
            break
        except ValueError:
            print("Please enter a valid number.")

    expense_categories = [
        "=🍉=Food",
        "=🏠=Home",
        "=💼=work",
        "=🎉=other",
        "=💰=savings",
    ]

    while True:
        print("Select expense category:")
        for i, category in enumerate(expense_categories):
            print(f"{i + 1}. {category}")

        try:
            value_range = f"[1 - {len(expense_categories)}]"
            selected_index = int(input(f"Enter category number {value_range}: ")) - 1

            if selected_index in range(len(expense_categories)):
                selected_category = expense_categories[selected_index]
                new_expense = Expense(name=expense_name, category=selected_category, amount=expense_amount)
                return new_expense
            else:
                print("Invalid category number. Please try again.")
        except ValueError:
            print("Please enter a valid number.")


def save_expense_to_file(expense, expense_file_path):
    print(f"Saving user Expense: {expense.name}, {expense.category}, {expense.amount} to {expense_file_path}")
    with open(expense_file_path, "a", encoding="utf-8") as f:
        f.write(f"{expense.name},{expense.category},{expense.amount}\n")


def summarize_expenses(expense, expense_file_path, budget):
    print(f"Summarizing expenses from {expense_file_path}")
    expenses: list[Expense] = []
    amount_by_category = {}

    try:
        with open(expense_file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                stripped_line = line.strip()
                expense_name, expense_category, expense_amount = stripped_line.split(",")
                line_expense = Expense(name=expense_name, category=expense_category, amount=float(expense_amount))
                expenses.append(line_expense)

                # Sum by category
                key = line_expense.category
                if key in amount_by_category:
                    amount_by_category[key] += line_expense.amount
                else:
                    amount_by_category[key] = line_expense.amount

        # Print results
        print("\nExpenses By Category:")
        for key, amount in amount_by_category.items():
            print(f"Category: {key}, Total Amount: {amount:.2f}")

        total_spent = sum(ex.amount for ex in expenses)
        print(f"\nYou've spent: KES {total_spent:.2f} this month")
        remaining_budget = budget - total_spent
        print(f"Budget remaining: KES {remaining_budget:.2f}")

    except FileNotFoundError:
        print("No expenses recorded yet.")


if __name__ == "__main__":
    main()