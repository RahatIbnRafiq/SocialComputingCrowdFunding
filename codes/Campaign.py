class Campaign:
    def __init__(self, campaign_url):
        self.campaign_url = campaign_url
        self.raised_text = 0
        self.created_text = ""
        self.campaign_content_text = ""
        self.campaign_description = ""
        self.comments = {}
        self.updates = []
        self.total_donations_text = ""
        self.top_donations = []
        self.campaign_video = ""
        self.campaign_image = ""

    def print_attributes(self):
        attrs = vars(self)
        for item in attrs.items():
            print(item)

    def print_log(self):
        print("campaign url: " + self.campaign_url)
        print("Total collected comments: " + str(len(self.comments)))
        print("Total updates : " + str(len(self.updates)))

    def write_to_file(self):
        print("writing to file")
        index1 = self.campaign_url.index("com")
        filename = self.campaign_url[index1+6:]
        f = open(filename + ".txt", 'w')

        f.write("Campaign URL: " + "\n")
        f.write(self.campaign_url + "\n")
        f.write("\n")

        f.write("Campaign Description: " + "\n")
        f.write(self.campaign_description + "\n")
        f.write("\n")

        f.write("Campaign Updates: " + "\n")
        for i in range(0, len(self.updates)):
            f.write("Update : " + self.updates[i] + "\n")
        f.write("\n")

        f.write("Campaign Information: " + "\n")
        f.write(self.campaign_content_text + "\n")
        f.write("\n")

        f.write("Campaign Media Video: " + "\n")
        f.write(self.campaign_video + "\n")
        f.write("\n")

        f.write("Campaign Media Image: " + "\n")
        f.write(self.campaign_image + "\n")
        f.write("\n")

        f.write("Campaign Total Donations: " + "\n")
        f.write(self.total_donations_text + "\n")
        f.write("\n")

        f.write("Campaign Top Donations: " + "\n")
        for i in range(0, len(self.top_donations)):
            f.write("Donation : " + self.top_donations[i] + "\n")
        f.write("\n")

        f.write("Campaign Comments: " + "\n")
        for comment_id in self.comments.keys():
            f.write("Comment " + str(comment_id) + ":" + str(self.comments[comment_id].comment_text) + "\n")
        f.write("\n")

        f.close()
        print("writing to file done")
