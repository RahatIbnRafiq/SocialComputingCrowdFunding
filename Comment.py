# class Comment:
#     def __init__(self, comment_id, commenter_name, commenter_donated, comment, comment_time):
#         self.comment_id = comment_id
#         self.commenter_name = commenter_name
#         self.commenter_donated = commenter_donated
#         self.comment = comment
#         self.comment_time = comment_time
#
#     def print_attributes(self):
#         attrs = vars(self)
#         for item in attrs.items():
#             print(item)


class Comment:
    def __init__(self, comment_text):
        self.comment_text = comment_text

    def print_attributes(self):
        attrs = vars(self)
        for item in attrs.items():
            print(item)
