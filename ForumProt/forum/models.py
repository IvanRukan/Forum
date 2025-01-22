from django.db import models
from django.contrib.auth.models import User, Group


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.PositiveIntegerField()


class UserPublication(models.Model):
    title = models.CharField(max_length=30)
    category = models.CharField(max_length=20)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)
    desc = models.TextField()
    upvotes = models.PositiveSmallIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    publication = models.ForeignKey(UserPublication, on_delete=models.CASCADE, null=False)
    desc = models.CharField(max_length=50)


class User_upvotes(models.Model):
    publication = models.ForeignKey(UserPublication, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


UserPublication.objects.raw(
    """
CREATE PROCEDURE GetPublicationsCategory
@PublCategory varchar(45)
AS
BEGIN
    
    SELECT title, desc 
    FROM UserPublication 
    WHERE category = @PublCategory;
END;
     """
)

Comment.objects.raw(
    """
CREATE PROCEDURE GetUserComments
@User_id int
AS
BEGIN

    SELECT desc, id 
    FROM Comment 
    WHERE user = @User_id;
END;
     """
)


User_upvotes.objects.raw(
    """
CREATE TRIGGER UpdateUpvotes
ON User_upvotes
AFTER INSERT
AS
BEGIN
    UPDATE UserPublication
    SET upvotes = upvotes + 1
    WHERE id = (SELECT publication FROM INSERTED));
END;

     """
)


# superuser : Ivan , 777Rukan777
