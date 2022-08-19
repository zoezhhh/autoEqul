from readfile import *
from equl import *

data = read_input()

print(data.iloc[0])

start = int(input("Start from Test Case #"))
end = int(input("End at Test Case #")) + 1
test_cases_to_complete = range(start, end)
# test_cases_to_complete = [20, 40, 60, 80, 100]

equlGUI = EqulGUI()

failed = []

for i in test_cases_to_complete:

    if not isFolderEmpty(i):
        pass

    print(f"Auto completing Test Case {i}...")

    row_data = data.iloc[i-1]

    equlGUI.focus_window()
    equlGUI.auto_complete(row_data)

    save()

    passed = check_existance(row_data)

    if not passed:
        failed.append(i)
        pass

    equlGUI.export_to_excel()

    copyToWorkSpace(i)

    print()

print("Failed Test Cases:")
print(*failed)