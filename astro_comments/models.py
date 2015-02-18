from django_comments import Comment


class CustomComment(Comment):

    class Meta:
        ordering = ["-submit_date"]
