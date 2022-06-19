class Comment:
    """Абстракция комментариев"""

    def __init__(self,
                 post_id,
                 commenter_name,
                 comment,
                 pk):
        self.post_id = post_id
        self.commenter_name = commenter_name
        self.comment = comment
        self.pk = pk

    def __repr__(self):
        return f"Comment(" \
            f"{self.post_id}, " \
            f"{self.commenter_name}, " \
            f"{self.comment}, " \
            f"{self.pk}" \
            f")"


