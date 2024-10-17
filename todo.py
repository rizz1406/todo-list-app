import streamlit as st
from datetime import datetime, timedelta

# Initialize session state to hold tasks and due dates
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

if 'due_dates' not in st.session_state:
    st.session_state.due_dates = []

# Function to add a task with a due date
def add_task(task, due_date):
    st.session_state.tasks.append(task)
    st.session_state.due_dates.append(due_date)

# Function to delete a task
def delete_task(task_index):
    if 0 <= task_index < len(st.session_state.tasks):
        st.session_state.tasks.pop(task_index)
        st.session_state.due_dates.pop(task_index)
        return True
    return False

# Streamlit UI
st.title("To-Do List App with Reminders")

# Sidebar menu options
st.sidebar.header("Options")
menu_choice = st.sidebar.radio("Select an option:", ["Add Task", "View Tasks", "Delete Task", "View Reminders", "Quit"])

# Add Task Section
if menu_choice == "Add Task":
    st.subheader("Add a Task")
    task_input = st.text_input("Enter the task:")
    due_date_input = st.date_input("Due date:")
    due_time_input = st.time_input("Due time:")
    due_datetime = datetime.combine(due_date_input, due_time_input)

    if st.button("Add Task"):
        if task_input and due_datetime:
            add_task(task_input, due_datetime)
            st.success(f"'{task_input}' added with a reminder set for {due_datetime}.")
        else:
            st.error("Please enter a valid task and due date.")

# View Tasks Section
elif menu_choice == "View Tasks":
    st.subheader("Your Tasks")
    if not st.session_state.tasks:
        st.write("No tasks in the list.")
    else:
        for idx, (task, due_date) in enumerate(zip(st.session_state.tasks, st.session_state.due_dates), start=1):
            st.write(f"{idx}. {task} (Due: {due_date})")

# Delete Task Section
elif menu_choice == "Delete Task":
    st.subheader("Delete a Task")
    if not st.session_state.tasks:
        st.write("No tasks available to delete.")
    else:
        for idx, task in enumerate(st.session_state.tasks, start=1):
            st.write(f"{idx}. {task}")

        task_num = st.number_input("Enter the task number to delete:", min_value=1, max_value=len(st.session_state.tasks), step=1)
        if st.button("Delete Task"):
            if delete_task(task_num - 1):
                st.success(f"Task {task_num} deleted successfully.")
            else:
                st.error("Invalid task number.")

# View Reminders Section
elif menu_choice == "View Reminders":
    st.subheader("Upcoming Reminders")
    if not st.session_state.tasks:
        st.write("No tasks in the list.")
    else:
        current_time = datetime.now()
        for idx, (task, due_date) in enumerate(zip(st.session_state.tasks, st.session_state.due_dates), start=1):
            time_remaining = due_date - current_time
            if time_remaining <= timedelta(days=1):
                st.warning(f"Reminder: Task '{task}' is due soon! (Due: {due_date})")
            elif time_remaining < timedelta(seconds=0):
                st.error(f"Task '{task}' is overdue! (Was due: {due_date})")
