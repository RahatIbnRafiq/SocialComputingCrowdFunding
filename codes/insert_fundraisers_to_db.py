from os import listdir
from os.path import isfile, join
import re
import pymongo

LOCATION = "/Users/rahatibnrafiq/MyWorkSpace/SocialComputingCrowdFunding/dataset/fundraiser_data/"
client = pymongo.MongoClient()


def get_mongo_collection(db_name, col_name):
    db = client[db_name]
    col = db[col_name]
    return col


def get_all_files(location):
    files = [f for f in listdir(location) if isfile(join(location, f))]
    return files


def collect_fundraisers():
    campaign_collection = get_mongo_collection("gofundme", "campaigns")
    files = get_all_files(LOCATION)
    for file in files:
        if ".txt" not in file:
            continue
        campaign = dict()
        campaign_data = get_fundraiser_info(file)
        campaign["fundraiser_link"] = campaign_data["fundraiser_link"]
        campaign["data"] = campaign_data
        campaign_collection.insert_one(campaign)


def get_fundraiser_info(file):
    campaign_dict = {}
    f = open(LOCATION+file, "r")
    full_data = ""
    for line in f:
        full_data += line
    index1 = full_data.index("Campaign URL:") + len("Campaign URL:")
    index2 = full_data.index("Campaign Description:")
    fundraiser_link = full_data[index1:index2].strip()
    #print("fund link: " + fundraiser_link)
    campaign_dict["fundraiser_link"] = fundraiser_link

    index1 = full_data.index("Campaign Description:") + len("Campaign Description:")
    index2 = full_data.index("Campaign Updates:")
    campaign_description = full_data[index1:index2].strip()
    #print("description: " + campaign_description)
    campaign_dict["description"] = campaign_description

    index1 = full_data.index("Campaign Updates:") + len("Campaign Updates:")
    index2 = full_data.index("Campaign Information:")
    campaign_updates = full_data[index1:index2].strip()
    campaign_updates = campaign_updates.split("Update :")
    all_updates = []
    for update in campaign_updates:
        if len(update) > 10:
            all_updates.append((update.strip()))
    # print("total updates for this campaign: " + str(len(all_updates)))
    campaign_dict["updates"] = all_updates



    if "followers\nShare" in full_data:
        info_dict = {}
        index1 = full_data.index("Campaign Information:") + len("Campaign Information:")
        index2 = full_data.index("followers\nShare")
        campaign_info = full_data[index1:index2+len("followers")]
        campaign_info = campaign_info.split("\n")
        for i in range(0, len(campaign_info)):
            if campaign_info[i] == "donors":
                info_dict["num_donor"] = campaign_info[i-1].strip()
            if campaign_info[i] == "shares":
                info_dict["num_shares"] = campaign_info[i-1].strip()
            if campaign_info[i] == "followers":
                info_dict["followers"] = campaign_info[i-1].strip()
            if "raised of" in campaign_info[i]:
                index1 = campaign_info[i].index("raised of")
                raised = campaign_info[i][1:index1].strip().replace(",", "").strip()
                info_dict["raised"] = raised

                index1 = campaign_info[i].index("raised of") + len("raised of") + 2
                index2 = campaign_info[i].index("goal")
                goal = campaign_info[i][index1:index2].replace(",", "").strip()
                info_dict["goal"] = goal

        for key in info_dict.keys():
            if "K" in info_dict[key] or "M" in info_dict[key]:
                info_dict[key] = int(convert_str_to_number(info_dict[key]))
            else:
                if "CAD" in info_dict[key]:
                    index1 = info_dict[key].index("CAD")
                    info_dict[key] = int(info_dict[key][:index1].strip())
                elif "AUD" in info_dict[key]:
                    index1 = info_dict[key].index("AUD")
                    info_dict[key] = int(info_dict[key][:index1].strip())
                elif "HF" in info_dict[key]:
                    index1 = info_dict[key].index("HF") + len("HF")
                    info_dict[key] = int(info_dict[key][index1:].strip())
        campaign_dict["information"] = info_dict


    index1 = full_data.index("Campaign Information:") + len("Campaign Information:")
    full_data = full_data[index1:]
    if "Organizer and beneficiary" in full_data or "Organizer\n" in full_data:
        if "Organizer\n" in full_data:
            index1 = full_data.index("Organizer")
        else:
            index1 = full_data.index("Organizer and beneficiary")
        index2 = full_data.index("Campaign Media Video: ")
        campaign_organizer_data = full_data[index1:index2].strip()
        campaign_dict["organizer_data"] = campaign_organizer_data


    index1 = full_data.index("Campaign Media Video:") + len("Campaign Media Video:")
    index2 = full_data.index("Campaign Media Image: ")
    campaign_video_link = full_data[index1:index2].strip()
    if len(campaign_video_link) > 5:
        campaign_dict["video_link"] = campaign_video_link

    index1 = full_data.index("Campaign Media Image:") + len("Campaign Media Image:")
    index2 = full_data.index("Campaign Total Donations: ")
    campaign_image_link = full_data[index1+25:index2-5].strip()
    if len(campaign_image_link) > 5:
        campaign_dict["image"] = campaign_image_link

    index1 = full_data.index("Campaign Total Donations:") + len("Campaign Total Donations:")
    index2 = full_data.index("Campaign Top Donations:")
    campaign_total_donations = full_data[index1:index2].strip()
    campaign_total_donations = re.sub("[^0-9]", "", campaign_total_donations)
    if len(campaign_total_donations) > 0:
        campaign_dict["campaign_total_donations"] = campaign_total_donations

    index2 += len("Campaign Top Donations:")
    full_data = full_data[index2:]
    index1 = full_data.index("Campaign Comments: ")
    campaign_top_donations = full_data[:index1].strip()
    campaign_top_donations = campaign_top_donations.split("Donation : ")
    campaign__all_top_donations = []
    for donation in campaign_top_donations:
        if len(donation):
            single_donation = {}
            donation = donation.strip()
            donation_items = donation.split(",")
            if len(donation_items) == 3:
                single_donation["donor"] = donation_items[0]
                single_donation["amount"] = donation_items[1]
                single_donation["time"] = donation_items[2]
                campaign__all_top_donations.append(single_donation)
            if len(donation_items) == 4:
                single_donation["donor"] = donation_items[0]
                single_donation["amount"] = donation_items[1] + donation_items[2]
                single_donation["time"] = donation_items[3]
                campaign__all_top_donations.append(single_donation)
    campaign_dict["top_donations"] = campaign__all_top_donations


    index1 = full_data.index("Campaign Comments: ") + len("Campaign Comments: ")
    full_data = full_data[index1:]
    comments = full_data.split("Comment ")
    all_comments = []
    for comment in comments:
        single_comment = {}
        comment = comment.strip()
        comment_items = comment.split("\n")
        if len(comment_items) > 3:
            commenter_name = comment_items[0]
            index1 = commenter_name.index(":") + len(":")
            index2 = commenter_name.index("donated")
            name = commenter_name[index1:index2]
            index2 += len("donated")
            donated = commenter_name[index2:]

            single_comment["commenter"] = name
            single_comment["donation"] = donated
            single_comment["comment_text"] = comment_items[1]
            if len(comment_items) == 3:
                single_comment["time"] = comment_items[2]
            else:
                single_comment["time"] = comment_items[3]
        if len(single_comment):
            all_comments.append(single_comment)
    campaign_dict["all_comments"] = all_comments
    f.close()
    # print("================================================")
    return campaign_dict


def convert_str_to_number(x):
    total_stars = 0
    num_map = {'K':1000, 'M':1000000, 'B':1000000000}
    if x.isdigit():
        total_stars = int(x)
    else:
        if len(x) > 1:
            total_stars = float(x[:-1]) * num_map.get(x[-1].upper(), 1)
    return int(total_stars)


collect_fundraisers()
client.close()
