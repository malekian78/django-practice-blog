from django.db import models

class Comment(models.Model):
    post = models.ForeignKey(
        "blog.Post", on_delete=models.CASCADE, related_name="comment"
    )
    author = models.ForeignKey("accounts.Profile", on_delete=models.PROTECT)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.content[:30] + " . . ."
