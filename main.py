from rich.console import Console
from rich.table import Table
import json
import uuid


console = Console()

USERS_FILE = "users.json"
APPLICANTS_FILE = "applicants.json"
EMPLOYEES_FILE = "employees.json"
# Initialize data
users = []
applicants = []
employees = []
# Load data from files
def load_data():
    global users, applicants, employees
    # Load users
    try:
        with open(USERS_FILE, "r") as file:
            users.extend(json.load(file))
    except (FileNotFoundError, json.JSONDecodeError):
        save_data()  # Create files if they don't exist
    # Load applicants
    try:
        with open(APPLICANTS_FILE, "r") as file:
            applicants.extend(json.load(file))
    except (FileNotFoundError, json.JSONDecodeError):
        save_data()
    # Load employees
    try:
        with open(EMPLOYEES_FILE, "r") as file:
            employees.extend(json.load(file))
    except (FileNotFoundError, json.JSONDecodeError):
        save_data()
# Save data to files
def save_data():
    with open(USERS_FILE, "w") as file:
        json.dump(users, file, indent=4)
    with open(APPLICANTS_FILE, "w") as file:
        json.dump(applicants, file, indent=4)
    with open(EMPLOYEES_FILE, "w") as file:
        json.dump(employees, file, indent=4)
# Find user by username

def generate_id():
    return str(uuid.uuid4())

def find_user(username):
    for user in users:
        if user["username"] == username:
            return user
    return None

def display_users():
    if not users:
        console.print("[red]No users found.[/red]")
    else:
        table = Table(title="Users")
        table.add_column("#", style="dim", width=5)
        table.add_column("Username", style="cyan")
        table.add_column("Role", style="magenta")

        for idx, user in enumerate(users, start=1):
            table.add_row(str(idx), user["username"], user["role"])
        console.print(table)
def add_user():
    username = input("Enter username: ")
    role = input("Enter role (superadmin/admin/hr/user): ").strip().lower()
    password = input("Enter password: ")
    
    # Cek apakah sudah ada user dengan username dan password yang sama serta role user
    existing_user = next((user for user in users if user['username'] == username and user['password'] == password and user['role'] == 'user'), None)
    
    if existing_user:
        console.print("[red]Username and password already exist for a user account.[/red]")
        return  # Menghentikan fungsi jika data sudah ada
    
    if role not in ["superadmin", "admin", "hr", "user"]:
        console.print("[red]Invalid role.[/red]")
        return
    
    # Menambahkan user baru ke list users
    users.append({"id": generate_id(), "username": username, "role": role, "password": password})
    
    # Menyimpan data ke JSON setelah memastikan data valid
    save_data()
    
    console.print(f"[green]User {username} added successfully.[/green]")


def edit_user():
    display_users()
    username = input("Enter username to edit: ")
    user = find_user(username)
    if not user:
        console.print("[red]User not found.[/red]")
        return
    user["role"] = input(f"Enter new role for {username} (current: {user['role']}): ").strip().lower()
    user["password"] = input(f"Enter new password for {username}: ")
    save_data()
    console.print(f"[green]User {username} updated successfully.[/green]")
def delete_user():
    display_users()
    username = input("Enter username to delete: ")
    global users
    users = [user for user in users if user["username"] != username]
    save_data()
    console.print(f"[green]User {username} deleted successfully.[/green]")
    
def superadmin_menu():
    while True:
        console.print("\n[bold blue]Superadmin Menu:[/bold blue]")
        console.print("1. View Users\n2. Add User\n3. Edit User\n4. Delete User\n5. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            display_users()
        elif choice == "2":
            add_user()
        elif choice == "3":
            edit_user()
        elif choice == "4":
            delete_user()
        elif choice == "5":
            break
        else:
            console.print("[red]Invalid choice.[/red]")
# Display applicants
def display_applicants():
    if not applicants:
        console.print("[red]No applicants available.[/red]")
    else:
        table = Table(title="Applicants")
        table.add_column("#", style="dim", width=5)
        table.add_column("Name", style="green")
        table.add_column("Salary", style="magenta")
        table.add_column("Position", style="yellow")
        table.add_column("Address", style="cyan")
        table.add_column("Status", style="green")

        for idx, applicant in enumerate(applicants, start=1):
            table.add_row(
                str(idx),
                applicant["name"],
                str(applicant["salary"]),
                applicant["position"],
                applicant["address"],
                applicant["status"]
            )
        console.print(table)

# Display employees
def display_employees(employees_list):
    if not employees_list:
        console.print("[red]No employees available.[/red]")
    else:
        table = Table(title="Employees")
        table.add_column("#", style="dim", width=5)
        table.add_column("Name", style="cyan")
        table.add_column("Salary", style="green")
        table.add_column("Position", style="magenta")
        table.add_column("Address", style="yellow")
        table.add_column("Status", style="green")

        for idx, employee in enumerate(employees_list, start=1):
            table.add_row(
                str(idx),
                employee["name"],
                str(employee["salary"]),
                employee["position"],
                employee["address"],
                employee["status"]
            )
        console.print(table)

def sort_employees():
    console.print("\n[bold blue]Sort Employees:[/bold blue]")
    console.print("1. By Salary\n2. By Name")
    choice = input("Choose an option: ")
    if choice == "1":
        sorted_employees = sorted(employees, key=lambda x: x["salary"], reverse=True)
        console.print("[green]Employees sorted by salary:[/green]")
        display_employees(sorted_employees)
    elif choice == "2":
        sorted_employees = sorted(employees, key=lambda x: x["name"].lower())
        console.print("[green]Employees sorted by name:[/green]")
        display_employees(sorted_employees)
    else:
        console.print("[red]Invalid choice.[/red]")

def search_employees():
    query = input("Enter name or position to search: ").strip().lower()
    results = [emp for emp in employees if query in emp["name"].lower() or query in emp["position"].lower()]
    if results:
        console.print(f"[green]Found {len(results)} matching employees:[/green]")
        display_employees(results)
    else:
        console.print("[red]No matching employees found.[/red]")

# Add applicant
def add_applicant(username):
    applicant_data = {
        "id": generate_id(),
        "name": input("Enter your name: "),
        "salary": float(input("Enter expected salary: ")),
        "position": input("Enter desired position: "),
        "address": input("Enter your address: "),
        "status": "pending",
        "added_by": username
    }
    applicants.append(applicant_data)
    save_data()
    console.print(f"[green]Applicant {applicant_data['name']} added successfully.[/green]")

# Edit applicant data
def edit_applicant(username):
    display_applicants()
    app_id = input("Enter the name of the applicant to edit: ")
    applicant = next((app for app in applicants if app["name"] == app_id), None)
    if not applicant:
        console.print("[red]Applicant not found.[/red]")
        return
    if applicant["added_by"] != username:
        console.print("[red]You are not authorized to edit this applicant.[/red]")
        return
    applicant["name"] = input(f"Enter new name (current: {applicant['name']}): ") or applicant["name"]
    applicant["salary"] = float(input(f"Enter new expected salary (current: {applicant['salary']}): ") or applicant["salary"])
    applicant["position"] = input(f"Enter new desired position (current: {applicant['position']}): ") or applicant["position"]
    applicant["address"] = input(f"Enter new address (current: {applicant['address']}): ") or applicant["address"]
    save_data()
    console.print(f"[green]Applicant {applicant['name']} updated successfully.[/green]")

# Accept applicant
def accept_applicant():
    if not applicants:
        console.print("[red]No applicants available.[/red]")
        return hr_menu()  # Langsung kembali ke HR menu jika tidak ada pelamar

    display_applicants()
    app_name = input("Enter the name of the applicant to accept: ").strip()
    applicant = next((app for app in applicants if app["name"].lower() == app_name.lower()), None)

    if not applicant:
        console.print("[red]Applicant not found.[/red]")
        return hr_menu()  # Kembali ke HR menu jika pelamar tidak ditemukan
    
    # Pindahkan pelamar dari daftar ke karyawan
    applicants.remove(applicant)
    applicant["status"] = "accepted"
    employees.append(applicant)
    save_data()
    console.print(f"[green]Applicant {applicant['name']} accepted and added as employee.[/green]")


# Admin menu
def admin_menu():
    while True:
        console.print("\n[bold blue]Admin Menu:[/bold blue]")
        console.print("1. View Employees\n2. View Applicants\n3. Search Employees\n4. Sort Employees\n5. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            display_employees(employees)
        elif choice == "2":
            display_applicants()
        elif choice == "3":
            search_employees()
        elif choice == "4":
            sort_employees()
        elif choice == "5":
            break
        else:
            console.print("[red]Invalid choice.[/red]")

# User menu
def user_menu(username):
    while True:
        console.print("\n[bold blue]User Menu:[/bold blue]")
        console.print("1. Add Applicant\n2. Edit Your Data\n3. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            add_applicant(username)
        elif choice == "2":
            edit_applicant(username)
        elif choice == "3":
            break
        else:
            console.print("[red]Invalid choice.[/red]")

# HR menu
def hr_menu():
    while True:
        console.print("\n[bold blue]HR Menu:[/bold blue]")
        console.print("1. View Employees\n2. Accept Aplicants\n3. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            display_employees(employees)
        elif choice == "2":
            accept_applicant()
        elif choice == "3":
            break
        else:
            console.print("[red]Invalid choice.[/red]")

def login():
    console.print("\n[bold blue] WELLCOME TO STAFF SYNC  [/bold blue]")
    console.print("\n[bold blue]Login As:[/bold blue]")
    console.print("1. Superadmin\n2. Admin\n3. HR\n4. User")
    role_choice = input("Choose your role: ").strip()
    
    if role_choice == "1":
        username = input("Enter username: ")
        password = input("Enter password: ")
        user = find_user(username)
        if user and user["role"] == "superadmin" and user["password"] == password:
            console.print(f"[green]Welcome, {username}![/green]")
            superadmin_menu()
        else:
            console.print("[red]Invalid credentials.[/red]")
    elif role_choice in ["2", "3"]:
        username = input("Enter username: ")
        password = input("Enter password: ")
        user = find_user(username)
        if user and user["role"] in ["admin", "hr"] and user["password"] == password:
            console.print(f"[green]Welcome, {username}![/green]")
            admin_menu() if user["role"] == "admin" else hr_menu()
        else:
            console.print("[red]Invalid credentials.[/red]")
    elif role_choice == "4":
        username = input("Enter your username: ")
        password = input("Create your password: ")
        users.append({"username": username, "role": "user", "password": password})
        save_data()
        console.print(f"[green]Account created for {username}. Welcome![/green]")
        user_menu(username)
    else:
        console.print("[red]Invalid choice.[/red]")
def main():
    load_data()
    login()

if __name__ == "__main__":
    main()