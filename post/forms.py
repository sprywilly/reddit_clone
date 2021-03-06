from django import forms

from .models import Post, Comment


#Форма добавления комментария
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['user_comment']
        widgets= {'user_comment':forms.TextInput(attrs={"class":"form-control form-control-sm",
            "placeholder":"текст комментария"}),
        }


#форма добавления статьи
class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['name', 'text']
        widgets= {'name':forms.TextInput(attrs={"class": "form-control","placeholder":"Название статьи"}),
                'text':forms.Textarea(attrs={"class": "form-control", "rows": "5", "placeholder":"Текст статьи"}),
        }