from .actions import  getLinkedinData
from .googlesheet_operations import  getInput



def main():
    input_data = getInput()
    print(input_data)
    for each in input_data:
        if (each['Status'] != 'completed'):
            getLinkedinData(each['sheet name'], each['tab name'])


main()