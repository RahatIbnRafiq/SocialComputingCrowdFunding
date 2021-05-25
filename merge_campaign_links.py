import os

ROOT_PATH = "/Users/rahatibnrafiq/MyWorkSpace/SocialComputingCrowdFunding/fundraiser_links/"

link_files = os.listdir(ROOT_PATH)
all_links = []
for file in link_files:
    f = open(ROOT_PATH + file, "r")
    for line in f:
        line = line.strip()
        all_links.append(line)
    f.close()
print(len(all_links))

f = open(ROOT_PATH + "all_gofundme_links", "w")
for link in all_links:
    f.write(link+"\n")
f.close()
