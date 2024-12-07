import mod
import mod.com
import os
from fs import Files
from utils import cli
import sys
# import argparse

# parser = argparse.ArgumentParser()


# def tt(mem):
#     """Just a test function

#     Args:
#         mem (str): a good string
#     """
    
#     return "hello"


# # for k in dir(mod.com):
# #     print(k)
    
# # print(mod.com.com.__doc__)
# # print(tt.__doc__)


# fs = Files('mod')
# fs.run()
# print(fs.files)
cli = cli.Cli()
cli.run()
# print(sys.argv[1:])