import item_dict_gen as igen 
import img2img 
import card_generator as card
import utilities as u
import ctypes
import user_input as uinput
import os

# This is a fix for the way that python doesn't release system memory back to the OS and it was leading to locking up the system
libc = ctypes.cdll.LoadLibrary("libc.so.6")
M_MMAP_THRESHOLD = -3

# Set malloc mmap threshold.
libc.mallopt(M_MMAP_THRESHOLD, 2**20)

uinput.prompt_user_input()



    


   


