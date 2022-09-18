# This is a sample Python script.
from cfenginetest import CfEngineTest


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def test_kaxengine():
    # Use a breakpoint in the code line below to debug your script.
    cftest = CfEngineTest()
    #rdata = cftest.getrandomdata(50)
    cftest.executesinglemodel()
    #print(rdata)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    test_kaxengine()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
