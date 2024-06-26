from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post, LikePost, CommentPost, MyUser, FollowMyUser, Notification, FavoritePost
from django.db.models import Q

import requests

BOT_TOKEN = '6189703946:AAGb1TA2yDg-sdu0c_AIDn39_07AuzvlZgE'
CHAT_ID = '1209619850'


def filter_favourites(user, posts):
    for post in posts:
        if post.user == user.user.user_id:
            return post


# Create your views here.
@login_required(login_url='auth/signin')
def home_view(request):
    follower = MyUser.objects.filter(user_id=request.user.id).first()
    following = FollowMyUser.objects.filter(follower=follower).values('following_id')
    # print(following)

    # posts = Post.objects.all()[::-1]
    posts = Post.objects.filter(author__in=following)[::-1]
    comments = CommentPost.objects.all()
    user = MyUser.objects.filter(user=request.user).first()
    users = MyUser.objects.exclude(user=request.user).exclude(followmyuser__follower__user=request.user)
    # favorited_posts = list(map(filter_favourites, FavoritePost.objects.all(), user))
    favourited_posts = FavoritePost.objects.all()

    notifications = Notification.objects.filter(is_read=False)
    likes = LikePost.objects.all()
    d = {
        "posts": posts,
        'users': users[:5],
        "user": user,
        "comments": comments,
        "likes": likes,
        "searched": False,
        "notifications": notifications,
        "favourited_posts": favourited_posts,
    }
    return render(request, 'index.html', context=d)


def profile_view(request):
    user_id = request.GET.get('user_id')
    user = MyUser.objects.filter(user_id=user_id).first()
    current_user = MyUser.objects.filter(user=request.user).first()
    posts = Post.objects.filter(author=user)
    follower_count = FollowMyUser.objects.filter(following=user).count()
    following_count = FollowMyUser.objects.filter(follower=user).count()

    if user.id == current_user.id:
        actual_user = True
    else:
        actual_user = False
    d = {
        "user": user,
        "actual_user": actual_user,
        "posts": posts,
        "post_count": posts.count(),
        "following_count": following_count,
        "follower_count": follower_count,
    }
    return render(request, 'profile.html', context=d)


def profile_image_view(request):
    user_id = request.user.id
    my_user = MyUser.objects.filter(user=request.user).first()
    if request.method == "POST":
        files = request.FILES
        cover_image = files.get('cover_image', None)
        user_image = files.get('user_image', None)
        if cover_image is not None:
            my_user.cover_image = request.FILES['cover_image']
            my_user.save(update_fields=['cover_image', ])
        elif user_image is not None:
            my_user.user_image = request.FILES['user_image']
            my_user.save(update_fields=['user_image', ])
    return redirect('/profile?user_id={}'.format(user_id))


def post_upload_view(request):
    if request.method == "POST":
        my_user = MyUser.objects.filter(user=request.user).first()
        post = Post.objects.create(post_image=request.FILES['post_image'], author=my_user)
        post.save()
        return redirect('/')
    return redirect('/')


def post_comment_view(requsts):
    if requsts.method == "POST":
        data = requsts.POST
        message = data["message"]
        post_id = data["post_id"]
        author = MyUser.objects.filter(user=requsts.user).first()
        obj = CommentPost.objects.create(message=message, post_id=post_id, author=author)
        post = Post.objects.filter(id=post_id).first()
        obj.save()
        message = "Postingizga fikr bildirildi"
        notification = Notification.objects.create(user=post.author, message=message, reporter_user=author, post=post)
        notification.save()
        rf = requests.get('http://127.0.0.1:8000/media/{}'.format(post.post_image))
        file = {"photo": post.post_image}
        TEXT = """
        
                Name: {} 
                Lastname: {} 
                Email: {} 
                -------------------------
                {} {} postiga fikir bildirdi 
                -------------------------------
                Comment: {}
                -------------------------------
                korish: http://127.0.0.1:8000/%23{}
                -------------------------------

                """.format(author.user.first_name, author.user.last_name, author.user.email,
                           post.author.user.first_name,
                           post.author.user.last_name, data['message'], post_id)

        url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto?chat_id={CHAT_ID}&caption={TEXT}'
        response = requests.post(url, files=file)
        return redirect('/#{}'.format(post_id))
    return render(requsts, 'index.html')


def post_like_view(request):
    if request.method == "POST":
        data = request.POST
        print(data)
        post_id = data['post_id']
        author = MyUser.objects.filter(user=request.user).first()
        is_liked = LikePost.objects.filter(author=author, post_id=post_id)
        post = Post.objects.filter(id=post_id).first()
        if not is_liked:
            liked = LikePost.objects.create(author=author, post_id=post_id, )
            liked.save()
            post.like_count += 1
            post.save(update_fields=['like_count'])
            message = "Postingizga like bosdi"
            notification = Notification.objects.create(user=post.author, message=message, reporter_user=author,
                                                       post=post)
            notification.save()
        else:
            disliked = is_liked.delete()
            post.like_count -= 1
            post.save(update_fields=['like_count'])
            message = "Postingizga dislike bosdi"
            notification = Notification.objects.create(user=post.author, message=message, reporter_user=author,
                                                       post=post)
            notification.save()
        return redirect('/#{}'.format(post_id))
    return render(request, 'index.html')


def post_comment_disabled_view(request):
    post_id = request.GET.get('post_id')
    post = Post.objects.filter(id=post_id).first()
    if post.write_comment:
        post.write_comment = False
        post.disable_btn_title = "Enable"
    else:
        post.write_comment = True
        post.disable_btn_title = "Disabled"
    post.save(update_fields=['write_comment', 'disable_btn_title'])
    return redirect('/#{}'.format(post_id))


def post_delete_view(request):
    post_id = request.GET.get('post_id')
    post = Post.objects.filter(id=post_id).first()
    post.delete()
    return redirect('/')


def following_view(request):
    user_id = request.GET.get('user_id')
    my_user = MyUser.objects.filter(user=request.user).first()
    follow_c = MyUser.objects.filter(id=user_id).first()
    following = FollowMyUser.objects.filter(follower=my_user, following_id=user_id)
    if not following:

        follow = FollowMyUser.objects.create(follower=my_user, following_id=user_id)
        follow.save()
        follow_c.follower_count += 1
        follow_c.save(update_fields=['follower_count'])
        message = "Yangi follower"
        notification = Notification.objects.create(user=follow_c, message=message, reporter_user=my_user, )
        notification.save()
    else:
        following.delete()
        follow_c.follower_count -= 1
        follow_c.save(update_fields=['follower_count'])
        message = " Sizni Follow qilishni to'xtatdi"
        notification = Notification.objects.create(user=follow_c, message=message, reporter_user=my_user, )
        notification.save()
    return redirect('/')


def follower_view(request):
    # uid = request.GET.get('uid')
    follower_uid = request.GET.get('follower_uid', None)
    following_uid = request.GET.get('following_uid', None)
    print("following_uid", following_uid, "follower_uid", follower_uid)
    if follower_uid is not None:
        follower = FollowMyUser.objects.filter(following__id=follower_uid)
        followed = []
        title = "Your Followers"
        unfollow = False
        for i in MyUser.objects.all():
            print(type(i))
            for j in follower:
                print(type(j))
                if j.follower == i:
                    followed.append(i)

    elif following_uid is not None:
        follower = FollowMyUser.objects.filter(follower__id=following_uid)
        title = "Your are Following"
        unfollow = True
        followed = []
        for i in MyUser.objects.all():
            print(type(i))
            for j in follower:
                print(type(j))
                if j.following == i:
                    followed.append(i)
    print("follower", followed)
    my_user = MyUser.objects.filter(user=request.user).first()
    followers = FollowMyUser.objects.filter(following=my_user)
    d = {
        "users": followed,
        "user": my_user,
        "searched": True,
        "title": title,
        "unfollow": unfollow
    }
    return render(request, 'searched.html', context=d)


def searched_view(request):
    d = {}
    if request.method == "POST":
        data = request.POST
        query = data['searched_text']
        return redirect(f'/searched?q={query}')
    query = request.GET.get('q')
    my_user = MyUser.objects.filter(user=request.user).first()
    if query is not None and len(query) >= 1:
        users = MyUser.objects.exclude(user=request.user).filter(
            Q(user__first_name__icontains=query) | Q(user__username__icontains=query) | Q(
                user__last_name__icontains=query) | Q(
                about_me__icontains=query))
    else:
        # users = MyUser.objects.exclude(user=request.user)
        return redirect('/')
    d = {
        "users": users,
        "user": my_user,
        "searched": True,
        "title": "Users You Searched",
    }
    return render(request, 'searched.html', context=d)


def notification_read_view(request):
    notification_id = request.GET.get('notification_id')
    notification = Notification.objects.filter(id=notification_id).first()
    if not notification.post:
        # notification.is_read = True
        # notification.save(update_fields=['is_read'])
        notification.delete()
        return redirect('/profile/?user_id={}'.format(notification.reporter_user.user.id))
    else:
        # notification.is_read = True
        # notification.save(update_fields=['is_read'])
        notification.delete()
        return redirect('/#{}'.format(notification.post.id))


def notification_mark_read_view(request):
    user = MyUser.objects.filter(user=request.user).first()
    notifications = Notification.objects.filter(user=user)
    notifications.delete()

    return redirect('/')


def add_favorite_view(request):
    if request.method == "POST":
        pid = request.POST.get('pid')
        post = Post.objects.filter(id=pid).first()
        user = MyUser.objects.filter(user=request.user).first()
        favorite = FavoritePost.objects.filter(post=post, user=user).first()
        if not favorite:
            favorited = FavoritePost.objects.create(user=user, post=post, favorited=True, )
            favorited.save()
        else:
            favorite.delete()
        return redirect('/#{}'.format(pid))
    else:
        return redirect('/')
