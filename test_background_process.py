import time

f = open("my_output.txt", "w")
for i in range(200):
    f.write("Now the value of i is: " + str(i))
    print("Now the value of i is: " + str(i))
    time.sleep(1)

f.close()
