import pandas as pd
import numpy as np

class BranchAndBound:
    def __init__(self, revenues, days, max_days):
        self.revenues = revenues
        self.days = days
        self.max_days = max_days
        self.num_projects = len(revenues)
        
        self.best_solution = None
        self.best_revenue = -np.inf
    
    def branch_and_bound(self, current_solution=None, index=0, current_revenue=0, current_days=0):
        if current_solution is None:
            current_solution = [0] * self.num_projects
        
        if index == self.num_projects:
            if current_days <= self.max_days and current_revenue > self.best_revenue:
                self.best_solution = current_solution[:]
                self.best_revenue = current_revenue
            return
        
        remaining_revenue = self.calculate_upper_bound(index, current_revenue, current_days)
        if remaining_revenue <= self.best_revenue:
            return

        if current_days + self.days[index] <= self.max_days:
            current_solution[index] = 1
            self.branch_and_bound(current_solution, index + 1,
                                  current_revenue + self.revenues[index],
                                  current_days + self.days[index])
        
        current_solution[index] = 0
        self.branch_and_bound(current_solution, index + 1, current_revenue, current_days)
    
    def calculate_upper_bound(self, index, current_revenue, current_days):
        remaining_days = self.max_days - current_days
        upper_bound = current_revenue
        
        for i in range(index, self.num_projects):
            if self.days[i] <= remaining_days:
                remaining_days -= self.days[i]
                upper_bound += self.revenues[i]
            else:
                upper_bound += self.revenues[i] * (remaining_days / self.days[i])
                break
        return upper_bound
    
    def solve(self):
        self.branch_and_bound()
        return self.best_solution, self.best_revenue


def display_menu():
    print("\nMenu:")
    print("1. Add a new project")
    print("2. Delete a project")
    print("3. Modify a project")
    print("4. Display the current table")
    print("5. Solve the problem")
    print("6. Exit\n")


def add_project(df):
    try:
        project = len(df) + 1
        revenue = float(input("\nEnter revenue for the new project: "))
        days = int(input("Enter days required for the new project: "))
        df.loc[len(df)] = [project, revenue, days]
        print("\nProject added")
    except Exception as e:
        print("\nError adding project:", e)


def delete_project(df):
    try:
        print("\n",df)
        project = int(input("\nEnter the project number to delete: "))
        df.drop(df[df['Project'] == project].index, inplace=True)
        df.reset_index(drop=True, inplace=True)
        df['Project'] = range(1, len(df) + 1)
        print("\nProject deleted")
    except Exception as e:
        print("\nError deleting project:", e)


def modify_project(df):
    try:
        print("\n",df)
        project = int(input("\nEnter the project number to modify: "))
        row = df[df['Project'] == project]
        if not row.empty:
            new_revenue = float(input("\nEnter the new revenue: "))
            new_days = int(input("Enter the new days required: "))
            df.loc[row.index, 'Revenue'] = new_revenue
            df.loc[row.index, 'Days'] = new_days
            print("\nProject modified")
        else:
            print("\nProject not found")
    except Exception as e:
        print("\nError modifying project:", e)


def main():
    data = {
        "Project": [1, 2, 3, 4, 5, 6],
        "Revenue": [15, 20, 5, 25, 22, 17],
        "Days": [51, 60, 35, 60, 53, 10],
    }
    total_days_available = int(input("Enter the total available researcher days: "))
    df = pd.DataFrame(data)
    
    while True:
        display_menu()
        choice = input("Enter your choice: ")
        
        if choice == "1":
            add_project(df)
        elif choice == "2":
            delete_project(df)
        elif choice == "3":
            modify_project(df)
        elif choice == "4":
            print("\nCurrent table:")
            print(df)
        elif choice == "5":
            revenues = df["Revenue"].tolist()
            days = df["Days"].tolist()
            solver = BranchAndBound(revenues, days, total_days_available)
            best_solution, best_revenue = solver.solve()

            print("\nOptimal strategy:")
            for i, selected in enumerate(best_solution):
                status = "Selected" if selected else "Not selected"
                print(f"Project {df['Project'][i]}: {status}")
            print(f"\nMaximum revenue achievable: {best_revenue}")
        elif choice == "6":
            print("\nExiting the program.")
            break
        else:
            print("\nInvalid choice, try again")


if __name__ == "__main__":
    main()
